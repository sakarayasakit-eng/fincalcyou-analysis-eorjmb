#!/usr/bin/env python3
"""
fin-calc car-loan cluster generator (single source of truth).

Renders the 26 *templated* car-loan pages from `countries.json` using one shared
HTML template, and leaves the 8 hand-differentiated pages (India, UAE, Turkey,
South Africa, Indonesia, Pakistan, Philippines, Nigeria) untouched.

Currency figures are formatted by Node's Intl.NumberFormat with each country's
locale + currency -- the SAME call the live calculator uses -- so the static
"hint" numbers on the page always match what the live tool computes.

Usage (from the repo root):
    python build.py            # regenerates the 26 pages in ./pages/
    FINCALC_OUT=/tmp/x python build.py   # dry run: write elsewhere, diff first

Requires: python3 and node (node is used only for locale-accurate money formatting).
Workflow: edit countries.json -> python build.py -> git add -A && git commit && git push
"""
import os, re, json, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
OUT = os.environ.get("FINCALC_OUT", PAGES)
REG = json.load(open(os.path.join(HERE, "countries.json"), encoding="utf-8"))
CARS = REG["car_loan"]
TEMPLATE_SLUG = "car-loan-calculator-usa"
T = open(os.path.join(PAGES, TEMPLATE_SLUG + ".html"), encoding="utf-8").read()

# ---- locale-accurate money via Node (same formatter as the live page) ----
NODE = r"""
const fs=require('fs');
const cars=JSON.parse(fs.readFileSync(process.argv[1],'utf8')).car_loan;
function emi(P,r,y){const n=Math.round(y*12),m=r/1200;let e;if(m===0){e=P/n;}else{const g=Math.pow(1+m,n);e=P*m*g/(g-1);}const t=e*n;return{e,t,interest:t-P};}
const out={};
for(const d of cars){
  if(d.custom) continue;
  const nf=new Intl.NumberFormat(d.locale,{style:'currency',currency:d.cur_code,maximumFractionDigits:0});
  const M=v=>nf.format(Math.round(v));
  const fin=80000,x=emi(fin,d.rate,5),w=emi(100000,d.rate,5);
  const barA=Math.max(2,Math.min(98,fin/x.t*100));
  out[d.slug]={headline:M(x.e),a:M(fin),b:M(x.interest),total:M(x.t),
    barA:barA.toFixed(1),barB:(100-barA).toFixed(1),
    we:M(w.e),wt:M(w.t),wi:M(w.interest),hundredk:M(100000)};
}
process.stdout.write(JSON.stringify(out));
"""

def compute_numbers():
    p = subprocess.run(["node", "-e", NODE, os.path.join(HERE, "countries.json")],
                       capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("node formatting failed:\n" + p.stderr)
    return json.loads(p.stdout)

def s1(pat, repl, s):
    return re.sub(pat, lambda m: repl(m), s, count=1, flags=re.S)

def render(d, N):
    c = d["country"]; art = d["country_article"]; lc = c.lower()
    sym = d["cur_symbol"]; cur = d["cur_code"]; loc = d["locale"]; rate = d["rate"]
    rs = ("%g" % rate); r2 = ("%.2f" % rate)
    kw = d.get("keywords", "car loan calculator %s, auto loan %s, vehicle finance %s, car finance rate %s 2026" % (lc, lc, lc, lc))
    h1 = d.get("h1", "Car Loan Calculator — " + c)
    note = d["car_note"]; jnote = json.dumps(note, ensure_ascii=True)[1:-1]
    h = T
    h = s1(r'(<title>Car Loan Calculator in ).+?( \S+ Monthly)', lambda m: m.group(1) + art + m.group(2), h)
    h = s1(r'(content="Calculate your car loan monthly installment in ).+?( for ).+?( using)', lambda m: m.group(1) + sym + m.group(2) + art + m.group(3), h)
    h = s1(r'(name="keywords" content=")[^"]*(")', lambda m: m.group(1) + kw + m.group(2), h)
    h = s1(r'(rel="canonical" href="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:url" content="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'("name":"Car Loan Calculator [^"]*","item":"[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:title" content="Car Loan Calculator ).+?( 2026 \S+ Monthly)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(property="og:description" content="Free ).+?( car loan calculator[^~]*~)[\d.]+(% p\.a\.\), total interest in )[A-Z]+', lambda m: m.group(1) + c + m.group(2) + rs + m.group(3) + cur, h)
    h = s1(r'(How is car loan installment calculated in )USA(\?)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(What is the current car loan rate in )USA(\?)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(rate in ' + re.escape(c) + r'\?","acceptedAnswer":\{"@type":"Answer","text":"As a 2026 reference, auto-finance rates are around )[\d.]+(% per year\. ).+?("\}\})', lambda m: m.group(1) + rs + m.group(2) + jnote + m.group(3), h)
    h = s1(r'("name":"Car Loan Calculator )\S+ USA(","item")', lambda m: m.group(1) + "— " + c + m.group(2), h)
    h = s1(r'(<h1>).*?(</h1>)', lambda m: m.group(1) + h1 + m.group(2), h)
    h = s1(r"(installment in )USD( using ).+?('s typical)", lambda m: m.group(1) + cur + m.group(2) + c + m.group(3), h)
    h = s1(r'(<div class="fc-in"><span>)[^<]+(</span><input data-f="amount")', lambda m: m.group(1) + sym + m.group(2), h)
    h = s1(r'(<input data-f="rate"[^>]*value=")[\d.]+(")', lambda m: m.group(1) + rs + m.group(2), h)
    h = s1(r'(<strong data-o="headline">)[^<]+(</strong>)', lambda m: m.group(1) + N["headline"] + m.group(2), h)
    h = s1(r'(<b data-o="a">)[^<]+(</b>)', lambda m: m.group(1) + N["a"] + m.group(2), h)
    h = s1(r'(<b data-o="b">)[^<]+(</b>)', lambda m: m.group(1) + N["b"] + m.group(2), h)
    h = s1(r'(<b data-o="total">)[^<]+(</b>)', lambda m: m.group(1) + N["total"] + m.group(2), h)
    h = s1(r'(<i data-bar="a" style="width:)[\d.]+(%;background:#0e7a4a"></i><i data-bar="b" style="width:)[\d.]+(%)', lambda m: m.group(1) + N["barA"] + m.group(2) + N["barB"] + m.group(3), h)
    h = s1(r'(\?cur=)USD(&tab=car)', lambda m: m.group(1) + cur + m.group(2), h)
    h = s1(r'("tab":"car","cur":")USD(","locale":")en-US(")', lambda m: m.group(1) + cur + m.group(2) + loc + m.group(3), h)
    h = s1(r'(<h2>Local rates [^<]*providers</h2>\s*<p>).+?(</p>)', lambda m: m.group(1) + note + m.group(2), h)
    h = s1(r'(For every <strong>)[^<]+(</strong> financed at <strong>)[\d.]+(%</strong>)', lambda m: m.group(1) + N["hundredk"] + m.group(2) + r2 + m.group(3), h)
    h = s1(r'(Monthly installment: <strong>)[^<]+(</strong>)', lambda m: m.group(1) + N["we"] + m.group(2), h)
    h = s1(r'(Total repaid: <strong>)[^<]+(</strong>)', lambda m: m.group(1) + N["wt"] + m.group(2), h)
    h = s1(r'(Total interest: <strong>)[^<]+(</strong>)', lambda m: m.group(1) + N["wi"] + m.group(2), h)
    h = s1(r'(<p>As a 2026 reference, auto-finance rates are around )[\d.]+(% per year\. ).+?(</p>)', lambda m: m.group(1) + rs + m.group(2) + note + m.group(3), h)
    h = s1(r'(\?cur=)USD(&amp;tab=car&amp;amount=100000&amp;rate=)[\d.]+(&amp;years=5)', lambda m: m.group(1) + cur + m.group(2) + rs + m.group(3), h)
    relhtml = "\n".join("        " + l for l in d["related"])
    h = s1(r'(<h2>Related calculators</h2>\s*<ul>).*?(\s*</ul>)', lambda m: m.group(1) + "\n" + relhtml + "\n      </ul>", h)
    h = h.replace("installment calculated in USA?", "installment calculated in " + c + "?")
    h = h.replace("current car loan rate in USA?", "current car loan rate in " + c + "?")
    return h

def main():
    nums = compute_numbers()
    os.makedirs(OUT, exist_ok=True)
    gen = skip = 0
    for d in CARS:
        if d.get("custom"):
            skip += 1
            continue
        html = render(d, nums[d["slug"]])
        with open(os.path.join(OUT, d["slug"] + ".html"), "w", encoding="utf-8", newline="") as f:
            f.write(html)
        gen += 1
    print("generated %d templated car pages -> %s" % (gen, OUT))
    print("left %d hand-differentiated pages untouched" % skip)

if __name__ == "__main__":
    main()
