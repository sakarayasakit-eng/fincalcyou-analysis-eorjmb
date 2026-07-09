#!/usr/bin/env python3
"""
fin-calc cluster generator (single source of truth).

Renders the *templated* landing pages for each calculator cluster from
`countries.json` using one shared HTML template per cluster, and leaves the
hand-differentiated pages (marked "custom": true) untouched.

Clusters currently generated:
  - car_loan   (template: car-loan-calculator-usa.html)
  - sip        (template: sip-calculator-usa.html)

Currency figures are formatted by Node's Intl.NumberFormat with each country's
locale + currency -- the SAME call the live calculator uses -- so the static
"hint" numbers on the page always match what the live tool computes.

Usage (from the repo root):
    python build.py                      # regenerate all clusters into ./pages/
    FINCALC_OUT=/tmp/x python build.py   # dry run: write elsewhere, diff first

Requires: python3 and node (node is used only for locale-accurate money formatting).
Workflow: edit countries.json -> python build.py -> git add -A && git commit && git push
"""
import os, re, json, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
OUT = os.environ.get("FINCALC_OUT", PAGES)
REG = json.load(open(os.path.join(HERE, "countries.json"), encoding="utf-8"))

TEMPLATES = os.path.join(HERE, "templates")

def _tpl(name):
    # stable skeleton templates (original section structure), NOT the generated
    # pages -- so re-runs stay idempotent even after enrichment.
    return open(os.path.join(TEMPLATES, name + ".html"), encoding="utf-8").read()

T = _tpl("car-loan")               # car skeleton template
SIP_T = _tpl("sip")                # sip skeleton template
# reuse the car template's own reducing-balance answer (keeps its unicode correct)
REDBAL = re.search(r'<h3>How is car loan installment calculated[^<]*</h3>\s*<p>(.+?)</p>', T, re.S).group(1).strip()
FD_T = _tpl("fixed-deposit")       # fixed-deposit skeleton template
FDCALC = re.search(r'<h3>How is FD maturity calculated[^<]*</h3>\s*<p>(.+?)</p>', FD_T, re.S).group(1).strip()

# ---- locale-accurate money via Node (same formatter as the live pages) ----
NODE = r"""
const fs=require('fs');
const doc=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
function M(loc,cur){const nf=new Intl.NumberFormat(loc,{style:'currency',currency:cur,maximumFractionDigits:0});return v=>nf.format(Math.round(v));}
function emi(P,r,y){const n=Math.round(y*12),m=r/1200;let e;if(m===0){e=P/n;}else{const g=Math.pow(1+m,n);e=P*m*g/(g-1);}const t=e*n;return{e,t,interest:t-P};}
function sipfv(P,r,y){const i=r/1200,n=Math.round(y*12),inv=P*n,fv=(i===0?inv:P*((Math.pow(1+i,n)-1)/i)*(1+i));return{fv,inv,gain:fv-inv};}
function fddep(P,r,y){const k=4,Mv=P*Math.pow(1+r/(100*k),k*y);return{M:Mv,a:P,b:Mv-P};}
const out={car_loan:{},sip:{},fixed_deposit:{}};
for(const d of (doc.car_loan||[])){
  if(d.custom) continue;
  const f=M(d.locale,d.cur_code);
  const fin=80000,x=emi(fin,d.rate,5),w=emi(100000,d.rate,5);
  const barA=Math.max(2,Math.min(98,fin/x.t*100));
  out.car_loan[d.slug]={headline:f(x.e),a:f(fin),b:f(x.interest),total:f(x.t),
    barA:barA.toFixed(1),barB:(100-barA).toFixed(1),
    we:f(w.e),wt:f(w.t),wi:f(w.interest),hundredk:f(100000)};
}
for(const d of (doc.sip||[])){
  if(d.custom) continue;
  const f=M(d.locale,d.cur_code);
  const x=sipfv(10000,d.rate,15),barA=Math.max(2,Math.min(98,x.inv/x.fv*100));
  out.sip[d.slug]={monthly:f(10000),headline:f(x.fv),a:f(x.inv),b:f(x.gain),total:f(x.fv),
    barA:barA.toFixed(1),barB:(100-barA).toFixed(1),mult:(x.fv/x.inv).toFixed(1)};
}
for(const d of (doc.fixed_deposit||[])){
  if(d.custom) continue;
  const f=M(d.locale,d.cur_code);
  const x=fddep(100000,d.rate,5),barA=Math.max(2,Math.min(98,x.a/x.M*100));
  out.fixed_deposit[d.slug]={headline:f(x.M),a:f(x.a),b:f(x.b),total:f(x.M),
    barA:barA.toFixed(1),barB:(100-barA).toFixed(1),hundredk:f(100000),mat:f(x.M),intr:f(x.b)};
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

def _plist(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]

# ============================ CAR LOAN ============================
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
    if d.get("rate_range") and d.get("lenders"):
        h = enrich(h, d, N, c, r2)
    return h

def enrich(h, d, N, country, rate2):
    """Richer, locally specific car content from the structured fields."""
    rr = d["rate_range"]; rr = rr[:-1] if rr.endswith(".") else rr
    L = _plist(d["lenders"])
    dep = ("A deposit of around %s of the car's price is typical. " % d["deposit"]) if d.get("deposit") else "Deposit requirements vary by lender. "
    ten = ("Loan terms run up to about %s. " % d["tenure"]) if d.get("tenure") else ""
    depq = ("Lenders typically look for a deposit of around %s of the price. " % d["deposit"]) if d.get("deposit") else "Deposit requirements vary by lender. "
    faq = [
        ("What is the typical car loan rate in %s?" % country,
         "As a 2026 reference, car finance in %s runs about %s. Your actual rate depends on the lender, your credit profile, and whether the car is new or used." % (country, rr)),
        ("How much deposit do I need for a car loan in %s?" % country,
         depq + "A larger deposit lowers both your monthly payment and the total interest you pay."),
        ("Which lenders offer car loans in %s?" % country,
         "Commonly used providers include %s. It pays to compare two or three offers, since rates and terms vary by lender and by your credit profile." % L),
        ("How is the car loan installment calculated?", REDBAL),
    ]
    secs = [
        '    <section>\n      <h2>Car finance rates in %s (2026)</h2>\n      <p>Car loans in %s typically run about %s. %s</p>\n      <p class="note">These are reference figures for 2026 - always confirm the current rate and the effective (reducing-balance) APR with the lender before you commit.</p>\n    </section>' % (country, country, rr, d["nuance"]),
        '    <section>\n      <h2>Where to get a car loan in %s</h2>\n      <p>Commonly used providers include %s. Rates and terms vary by lender, your credit profile, and whether you are buying new or used - it pays to compare at least two or three offers.</p>\n    </section>' % (country, L),
        '    <section>\n      <h2>Deposit and loan term</h2>\n      <p>%s%sA bigger deposit and a shorter term both cut the total interest you pay - use the calculator above to see the trade-off for your own numbers.</p>\n    </section>' % (dep, ten),
        '    <section>\n      <h2>Worked example</h2>\n      <p>For every <strong>%s</strong> financed at <strong>%s%%</strong> over <strong>5 years</strong>:</p>\n      <ul>\n        <li>Monthly installment: <strong>%s</strong></li>\n        <li>Total repaid: <strong>%s</strong></li>\n        <li>Total interest: <strong>%s</strong></li>\n      </ul>\n      <p>Scale to your financed amount, and remember a bigger deposit and shorter term lower the total interest.</p>\n    </section>' % (N["hundredk"], rate2, N["we"], N["wt"], N["wi"]),
        '    <section>\n      <h2>How to pay less interest on your car loan</h2>\n      <ul>\n        <li>Put down a larger deposit - it reduces both the monthly payment and the total interest.</li>\n        <li>Pick the shortest term you can comfortably afford; a longer term lowers the monthly cost but raises the total.</li>\n        <li>Compare the effective reducing-balance rate, not a headline flat rate - a flat rate looks cheaper than it really is.</li>\n        <li>A stronger credit profile usually earns a lower rate, so it is worth checking before you apply.</li>\n      </ul>\n    </section>',
        '    <section>\n      <h2>Frequently Asked Questions</h2>\n' + "\n".join('      <h3>%s</h3>\n      <p>%s</p>' % (q, a) for q, a in faq) + '\n    </section>',
    ]
    cta = re.search(r'    <a href="[^"]*" class="cta">[^<]*</a>', h).group(0)
    content = "\n".join(secs) + "\n" + cta
    h = re.sub(r'    <section>\s*<h2>Local rates.*?    <a href="[^"]*" class="cta">[^<]*</a>', lambda m: content, h, count=1, flags=re.S)
    ent = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    faqld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}, ensure_ascii=True, separators=(",", ":"))
    h = re.sub(r'  <script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage".*?\}\s*</script>',
               lambda m: '  <script type="application/ld+json">\n  ' + faqld + '\n  </script>', h, count=1, flags=re.S)
    return h

# ============================ SIP ============================
def render_sip(d, N):
    c = d["country"]; art = d["country_article"]; lc = c.lower()
    sym = d["cur_symbol"]; cur = d["cur_code"]; loc = d["locale"]; rate = d["rate"]
    rs = "%g" % rate; note = d["invest_note"]
    h = SIP_T
    h = s1(r'(<title>SIP Calculator in ).+?( . Monthly Investment)', lambda m: m.group(1) + art + m.group(2), h)
    h = s1(r'(Calculate how your monthly SIP grows in ).+?( over 10)', lambda m: m.group(1) + art + m.group(2), h)
    h = s1(r'(name="keywords" content="sip calculator )usa(, mutual fund calculator )usa(, monthly investment )usa(, monthly investment calculator, investment growth )usa(")', lambda m: m.group(1) + lc + m.group(2) + lc + m.group(3) + lc + m.group(4) + lc + m.group(5), h)
    h = s1(r'(rel="canonical" href="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:url" content="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:title" content="Monthly Investment Calculator ).+?( 2026)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(property="og:description" content="Free ).+?( monthly investment calculator\. See how a monthly investment grows at ~)[\d.]+(% historical returns\. Compounding, total gains in )[A-Z]+', lambda m: m.group(1) + c + m.group(2) + rs + m.group(3) + cur, h)
    h = s1(r'("name":"Monthly Investment Calculator . )USA(","item":"[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + c + m.group(2) + d["slug"] + ".html" + m.group(3), h)
    h = s1(r'(<h1>Monthly Investment Calculator . )USA(</h1>)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r"(<p class=\"sub\">See how a monthly investment grows over time at )USA('s historical returns)", lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(<div class="fc-in"><span>)[^<]+(</span><input data-f="amount")', lambda m: m.group(1) + sym + m.group(2), h)
    h = s1(r'(<input data-f="rate"[^>]*value=")[\d.]+(")', lambda m: m.group(1) + rs + m.group(2), h)
    h = s1(r'(<strong data-o="headline">)[^<]+(</strong>)', lambda m: m.group(1) + N["headline"] + m.group(2), h)
    h = s1(r'(<b data-o="a">)[^<]+(</b>)', lambda m: m.group(1) + N["a"] + m.group(2), h)
    h = s1(r'(<b data-o="b">)[^<]+(</b>)', lambda m: m.group(1) + N["b"] + m.group(2), h)
    h = s1(r'(<b data-o="total">)[^<]+(</b>)', lambda m: m.group(1) + N["total"] + m.group(2), h)
    h = s1(r'(<i data-bar="a" style="width:)[\d.]+(%;background:#0e7a4a"></i><i data-bar="b" style="width:)[\d.]+(%)', lambda m: m.group(1) + N["barA"] + m.group(2) + N["barB"] + m.group(3), h)
    h = s1(r'(\?cur=)USD(&tab=sip&amount=10000&rate=)[\d.]+(&years=15)', lambda m: m.group(1) + cur + m.group(2) + rs + m.group(3), h)
    h = s1(r'("type":"sip","cur":")USD(","locale":")en-US(","def":\{"amount":10000,"rate":)[\d.]+(,"years":15\})', lambda m: m.group(1) + cur + m.group(2) + loc + m.group(3) + rs + m.group(4), h)
    h = s1(r'(\?cur=)USD(&amp;tab=sip&amp;amount=10000&amp;rate=)[\d.]+(&amp;years=15)', lambda m: m.group(1) + cur + m.group(2) + rs + m.group(3), h)
    h = enrich_sip(h, d, N, c, rs, note)
    relhtml = "\n".join("        " + l for l in d["related"])
    h = re.sub(r'(<h2>Related calculators</h2>\s*<ul>).*?(\s*</ul>)', lambda m: m.group(1) + "\n" + relhtml + "\n      </ul>", h, count=1, flags=re.S)
    return h

def enrich_sip(h, d, N, country, rs, note):
    faq = [
        ("How does a monthly investment work in %s?" % country,
         "You invest a fixed amount each month into funds or an index. You buy more units when prices are low and fewer when high (cost averaging), and returns compound over time."),
        ("What return can I expect in %s?" % country,
         "Long-term historical equity returns are around %s%% per year here, though any single year can be sharply up or down. %s" % (rs, note)),
        ("How much do I need to start investing in %s?" % country,
         "Most platforms let you start small and increase later. Setting up an automatic monthly investment builds discipline and smooths out market timing."),
        ("Should I invest a lump sum or monthly in %s?" % country,
         "Investing monthly spreads your entry across market ups and downs (cost averaging) and is easier to budget. A lump sum can do better in a steadily rising market but carries more timing risk."),
        ("Is investing better than a fixed deposit in %s?" % country,
         "Investing targets higher long-term growth but carries market risk; fixed deposits are safer but usually return less. Many people hold both, matched to their time horizon."),
    ]
    secs = [
        '    <section>\n      <h2>Where to invest in %s</h2>\n      <p>%s</p>\n      <p class="note">Returns are long-term historical averages, not guarantees - markets fall as well as rise. Invest for the long term and diversify.</p>\n    </section>' % (country, note),
        '    <section>\n      <h2>The power of compounding</h2>\n      <p>Investing <strong>%s per month for 15 years</strong> at <strong>%s%%</strong> p.a.:</p>\n      <ul>\n        <li>Future value: <strong>%s</strong></li>\n        <li>Total invested: <strong>%s</strong></li>\n        <li>Estimated gains: <strong>%s</strong></li>\n      </ul>\n      <p>That is roughly <strong>%s&#215;</strong> your money - most of it from compounding. Scale the %s to your own monthly amount, and remember that starting earlier matters more than investing more.</p>\n    </section>' % (N["monthly"], rs, N["headline"], N["a"], N["b"], N["mult"], N["monthly"]),
        '    <section>\n      <h2>How to start - and stay - invested in %s</h2>\n      <ul>\n        <li>Automate a fixed monthly amount so you invest through good months and bad.</li>\n        <li>Start small; you can raise the amount as your income grows.</li>\n        <li>Favour low-cost, diversified funds over picking individual stocks.</li>\n        <li>Stay invested through market dips - time in the market beats timing the market.</li>\n      </ul>\n    </section>' % country,
        '    <section>\n      <h2>Frequently Asked Questions</h2>\n' + "\n".join('      <h3>%s</h3>\n      <p>%s</p>' % (q, a) for q, a in faq) + '\n    </section>',
    ]
    cta = re.search(r'    <a href="[^"]*" class="cta">[^<]*</a>', h).group(0)
    content = "\n".join(secs) + "\n" + cta
    h = re.sub(r'    <section>\s*<h2>Where to invest.*?    <a href="[^"]*" class="cta">[^<]*</a>', lambda m: content, h, count=1, flags=re.S)
    ent = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    faqld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}, ensure_ascii=True, separators=(",", ":"))
    h = re.sub(r'  <script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage".*?\}\s*</script>',
               lambda m: '  <script type="application/ld+json">\n  ' + faqld + '\n  </script>', h, count=1, flags=re.S)
    return h

# ============================ FIXED DEPOSIT ============================
def render_fd(d, N):
    c = d["country"]; art = d["country_article"]; lc = c.lower()
    sym = d["cur_symbol"]; cur = d["cur_code"]; loc = d["locale"]; rate = d["rate"]
    rs = "%g" % rate; r1 = "%.1f" % rate; r2 = "%.2f" % rate; note = d["fd_note"]
    h = FD_T
    h = s1(r'(<title>Fixed Deposit Calculator in ).+?( . Maturity)', lambda m: m.group(1) + art + m.group(2), h)
    h = s1(r'(total interest earned in )[^ ]+( for ).+?(, using current bank)', lambda m: m.group(1) + sym + m.group(2) + art + m.group(3), h)
    h = s1(r'(fixed deposit calculator )usa(, fd calculator )usa(, term deposit )usa(, fd interest rate )usa( 2026, fd maturity calculator)', lambda m: m.group(1) + lc + m.group(2) + lc + m.group(3) + lc + m.group(4) + lc + m.group(5), h)
    h = s1(r'(rel="canonical" href="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:url" content="[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + d["slug"] + ".html" + m.group(2), h)
    h = s1(r'(property="og:title" content="Fixed Deposit Calculator ).+?( 2026 . FD Maturity)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(property="og:description" content="Free ).+?( fixed deposit calculator\. Maturity value and interest at ~)[\d.]+(% p\.a\. \(quarterly compounding\) in )[A-Z]+', lambda m: m.group(1) + c + m.group(2) + r1 + m.group(3) + cur, h)
    h = s1(r'("name":"Fixed Deposit Calculator . )USA(","item":"[^"]*/pages/)[^"]+(")', lambda m: m.group(1) + c + m.group(2) + d["slug"] + ".html" + m.group(3), h)
    h = s1(r'(<h1>Fixed Deposit Calculator . )USA(</h1>)', lambda m: m.group(1) + c + m.group(2), h)
    h = s1(r'(fixed-deposit maturity value and interest in )USD( at current rates)', lambda m: m.group(1) + cur + m.group(2), h)
    h = s1(r'(<div class="fc-in"><span>)[^<]+(</span><input data-f="amount")', lambda m: m.group(1) + sym + m.group(2), h)
    h = s1(r'(<input data-f="rate"[^>]*value=")[\d.]+(")', lambda m: m.group(1) + rs + m.group(2), h)
    h = s1(r'(<strong data-o="headline">)[^<]+(</strong>)', lambda m: m.group(1) + N["headline"] + m.group(2), h)
    h = s1(r'(<b data-o="a">)[^<]+(</b>)', lambda m: m.group(1) + N["a"] + m.group(2), h)
    h = s1(r'(<b data-o="b">)[^<]+(</b>)', lambda m: m.group(1) + N["b"] + m.group(2), h)
    h = s1(r'(data-o="total">)[^<]+(<)', lambda m: m.group(1) + N["total"] + m.group(2), h)
    h = s1(r'(<i data-bar="a" style="width:)[\d.]+(%;background:#0e7a4a"></i><i data-bar="b" style="width:)[\d.]+(%)', lambda m: m.group(1) + N["barA"] + m.group(2) + N["barB"] + m.group(3), h)
    h = s1(r'(\?cur=)USD(&tab=fd&amount=100000&rate=)[\d.]+(&years=5)', lambda m: m.group(1) + cur + m.group(2) + rs + m.group(3), h)
    h = s1(r'("type":"fd","cur":")USD(","locale":")en-US(","def":\{"amount":100000,"rate":)[\d.]+(,"years":5\})', lambda m: m.group(1) + cur + m.group(2) + loc + m.group(3) + rs + m.group(4), h)
    h = s1(r'(\?cur=)USD(&amp;tab=fd&amp;amount=100000&amp;rate=)[\d.]+(&amp;years=5)', lambda m: m.group(1) + cur + m.group(2) + r1 + m.group(3), h)
    h = enrich_fd(h, d, N, c, rs, r2, note)
    relhtml = "\n".join("        " + l for l in d["related"])
    h = re.sub(r'(<h2>Related calculators</h2>\s*<ul>).*?(\s*</ul>)', lambda m: m.group(1) + "\n" + relhtml + "\n      </ul>", h, count=1, flags=re.S)
    return h

def enrich_fd(h, d, N, country, rs, r2, note):
    faq = [
        ("How is FD maturity calculated in %s?" % country, FDCALC),
        ("What is the current FD rate in %s?" % country,
         "As a 2026 reference, fixed-deposit rates are around %s%% per year, varying by bank and tenure. %s" % (rs, note)),
        ("Is FD interest taxable in %s?" % country,
         "In most countries FD interest is taxable as income; some offer tax-advantaged or senior-citizen options. Check your local rules - the calculator shows the pre-tax maturity value."),
        ("Is a fixed deposit safe in %s?" % country,
         "Fixed deposits carry no market risk and are often protected by a deposit-insurance scheme up to a limit. They trade higher safety for lower long-term returns than equities."),
        ("Should I choose a fixed deposit or invest instead in %s?" % country,
         "A fixed deposit gives a guaranteed return and suits money you cannot afford to risk. Investing targets higher long-term growth but can fall in value. Many people keep an FD for safety and invest separately for growth."),
    ]
    secs = [
        '    <section>\n      <h2>Fixed deposit rates in %s (2026)</h2>\n      <p>%s</p>\n      <p class="note">Reference figures, ~2026. FD interest is often taxable and rates vary by bank and tenure - verify the current rate before depositing.</p>\n    </section>' % (country, note),
        '    <section>\n      <h2>Worked example</h2>\n      <p>For every <strong>%s</strong> deposited at <strong>%s%%</strong> for <strong>5 years</strong> (quarterly compounding):</p>\n      <ul>\n        <li>Maturity value: <strong>%s</strong></li>\n        <li>Interest earned: <strong>%s</strong></li>\n      </ul>\n      <p>Scale to your deposit amount. Longer tenures and higher rates grow the maturity value; compare banks before locking in.</p>\n    </section>' % (N["hundredk"], r2, N["mat"], N["intr"]),
        '    <section>\n      <h2>How to get the best fixed-deposit return in %s</h2>\n      <ul>\n        <li>Compare several banks - smaller and digital banks often pay more than the big high-street names.</li>\n        <li>Ladder your deposits across different tenures so some matures regularly and you can reinvest at new rates.</li>\n        <li>Check how often interest compounds; more frequent compounding grows the maturity value.</li>\n        <li>Factor in tax on the interest, and compare against short-term government bills or bonds.</li>\n      </ul>\n    </section>' % country,
        '    <section>\n      <h2>Frequently Asked Questions</h2>\n' + "\n".join('      <h3>%s</h3>\n      <p>%s</p>' % (q, a) for q, a in faq) + '\n    </section>',
    ]
    cta = re.search(r'    <a href="[^"]*" class="cta">[^<]*</a>', h).group(0)
    content = "\n".join(secs) + "\n" + cta
    h = re.sub(r'    <section>\s*<h2>Local FD rates.*?    <a href="[^"]*" class="cta">[^<]*</a>', lambda m: content, h, count=1, flags=re.S)
    ent = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    faqld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}, ensure_ascii=True, separators=(",", ":"))
    h = re.sub(r'  <script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage".*?\}\s*</script>',
               lambda m: '  <script type="application/ld+json">\n  ' + faqld + '\n  </script>', h, count=1, flags=re.S)
    return h

CLUSTERS = [("car_loan", render, "car"), ("sip", render_sip, "SIP"), ("fixed_deposit", render_fd, "FD")]

def main():
    nums = compute_numbers()
    os.makedirs(OUT, exist_ok=True)
    for key, fn, label in CLUSTERS:
        gen = skip = 0
        for d in REG.get(key, []):
            if d.get("custom"):
                skip += 1
                continue
            html = fn(d, nums[key][d["slug"]])
            with open(os.path.join(OUT, d["slug"] + ".html"), "w", encoding="utf-8", newline="") as f:
                f.write(html)
            gen += 1
        print("%-9s: generated %d templated pages, left %d custom untouched" % (label, gen, skip))

if __name__ == "__main__":
    main()
