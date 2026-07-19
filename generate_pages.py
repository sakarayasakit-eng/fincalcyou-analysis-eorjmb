import os, re, glob
from datetime import date

HOST = "https://fincalcyou.com"

# Top 10 US Real Estate Markets for Airbnb/STR Investments
markets = [
    {"city": "Austin", "state": "Texas", "abbr": "TX"},
    {"city": "Miami", "state": "Florida", "abbr": "FL"},
    {"city": "Dallas", "state": "Texas", "abbr": "TX"},
    {"city": "Phoenix", "state": "Arizona", "abbr": "AZ"},
    {"city": "Atlanta", "state": "Georgia", "abbr": "GA"},
    {"city": "Nashville", "state": "Tennessee", "abbr": "TN"},
    {"city": "Denver", "state": "Colorado", "abbr": "CO"},
    {"city": "Charlotte", "state": "North Carolina", "abbr": "NC"},
    {"city": "Tampa", "state": "Florida", "abbr": "FL"},
    {"city": "Las Vegas", "state": "Nevada", "abbr": "NV"},
]

def slug_for(m):
    return "dscr-calculator-{}-{}.html".format(
        m["city"].lower().replace(" ", "-"), m["abbr"].lower())

# Shared building blocks (plain strings + str.format — robust on all Python versions)
HEAD = (
    '    <meta charset="UTF-8">\n'
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '    <meta name="theme-color" content="#ffffff">\n'
    '    <title>{title}</title>\n'
    '    <meta name="description" content="{desc}">\n'
    '    <link rel="canonical" href="{host}/{slug}">\n'
    '    <meta property="og:type" content="website">\n'
    '    <meta property="og:title" content="{title}">\n'
    '    <meta property="og:description" content="{desc}">\n'
    '    <meta property="og:url" content="{host}/{slug}">\n'
    '    <meta property="og:image" content="{host}/og-image.png">\n'
    '    <meta property="og:site_name" content="fin·calc">\n'
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
    '    <link rel="stylesheet" href="pages/landing.css">'
)
HEADER = (
    '    <header>\n'
    '      <a href="index.html" class="brand">fin<span class="dot">·</span>calc</a>\n'
    '      <nav>\n        <a href="index.html">Home</a>\n        <a href="pages/">Guides</a>\n      </nav>\n'
    '    </header>'
)
FOOTER = (
    '    <footer>\n'
    '      <div style="margin-bottom:10px; line-height:2;">\n'
    '        <a href="pages/">All calculators</a> · <a href="about.html">About</a> · '
    '<a href="methodology.html">Methodology</a> · <a href="editorial-policy.html">Editorial policy</a> · '
    '<a href="privacy.html">Privacy</a> · <a href="contact.html">Contact</a>\n'
    '      </div>\n'
    '      © 2026 fin·calc · Made for better financial decisions. No signup. No tracking.\n'
    '    </footer>'
)
STYLE = (
    '    <style>\n'
    '      .calculator-box{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;margin:18px 0;box-shadow:0 1px 2px rgba(16,38,58,.05),0 2px 6px rgba(16,38,58,.05)}\n'
    '      .form-group{margin-bottom:16px}\n'
    '      .calculator-box label{display:block;margin-bottom:6px;font-weight:600;font-size:13px;color:var(--muted)}\n'
    '      .calculator-box input{width:100%;padding:12px;border:1px solid var(--line);border-radius:9px;box-sizing:border-box;font-family:inherit;font-size:15px;background:var(--bg);color:var(--ink)}\n'
    '      .calculator-box button{background:var(--accent);color:#fff;padding:13px 20px;border:none;border-radius:10px;cursor:pointer;font-size:15px;font-weight:700;width:100%;font-family:inherit;margin-top:4px}\n'
    '      .calculator-box button:hover{background:#0b6a40}\n'
    '      .result{margin-top:20px;padding:16px;background:rgba(14,122,74,.08);border:1px solid rgba(14,122,74,.22);border-radius:10px;display:none}\n'
    '      .result h3{margin:0 0 6px;color:var(--accent)}\n'
    '      .lead-gate{margin-top:20px;padding:20px;border:1px solid rgba(14,122,74,.3);border-radius:12px;display:none;background:rgba(14,122,74,.05)}\n'
    '      .lead-gate h3{margin-top:0;color:var(--accent)}\n'
    '      .lead-gate input{width:100%;padding:12px;border:1px solid var(--line);border-radius:9px;box-sizing:border-box;margin-bottom:10px;font-family:inherit}\n'
    '    </style>'
)

def city_page(m):
    c, s, a = m["city"], m["state"], m["abbr"]
    slug = slug_for(m)
    title = "DSCR Calculator for Short-Term Rentals in {}, {} | fin·calc".format(c, a)
    desc = ("Calculate the Debt Service Coverage Ratio (DSCR) for your Airbnb or short-term rental "
            "property in {}, {}. Free, accurate, and built for {} real estate investors.").format(c, s, c)
    head = HEAD.format(title=title, desc=desc, slug=slug, host=HOST)
    body = "\n".join([
        '<!DOCTYPE html>', '<html lang="en">', '<head>', head, STYLE, '</head>', '<body>', '  <main>', HEADER,
        '    <h1>DSCR Calculator for Short-Term Rentals in {}, {}</h1>'.format(c, a),
        '    <p class="intro">Calculate the Debt Service Coverage Ratio (DSCR) for your Airbnb or short-term rental investment in {}, {}. Local {} lenders require a DSCR of 1.25 or higher to approve investment property loans.</p>'.format(c, s, c),
        '    <div class="calculator-box">',
        '      <div class="form-group"><label for="rentalIncome">Estimated Annual {} Short-Term Rental Income ($)</label><input type="number" id="rentalIncome" placeholder="e.g., 45000"></div>'.format(c),
        '      <div class="form-group"><label for="operatingExpenses">Annual Operating Expenses (Taxes, Insurance, HOA, etc.) ($)</label><input type="number" id="operatingExpenses" placeholder="e.g., 12000"></div>',
        '      <div class="form-group"><label for="annualDebtService">Annual Debt Service (Mortgage Principal &amp; Interest) ($)</label><input type="number" id="annualDebtService" placeholder="e.g., 20000"></div>',
        '      <button onclick="calculateDSCR()">Calculate DSCR</button>',
        '      <div class="result" id="resultBox"><h3>Your DSCR: <span id="dscrValue"></span></h3><p id="dscrMessage"></p></div>',
        '      <div class="lead-gate" id="leadGate"><h3>Unlock Full {} Investment Analysis</h3><p>Enter your email to get your detailed DSCR breakdown, cash-on-cash return, and connect with a {} DSCR lender.</p><input type="email" id="userEmail" placeholder="Investor@example.com"><button onclick="submitLead()">Get My Analysis</button></div>'.format(c, a),
        '    </div>',
        '    <h2>Why DSCR Matters for {} Real Estate</h2>'.format(c),
        '    <p>The {} short-term rental market is highly competitive. Lenders in {} use DSCR to evaluate deals without relying on your personal income. A strong DSCR proves your {} property generates enough rent to cover its own mortgage, making it easier to scale your real estate portfolio.</p>'.format(c, s, c),
        '    <p><a href="dscr-calculator-locations.html">See DSCR calculators for other US markets &rarr;</a> · <a href="dscr-calculator.html">General DSCR calculator</a></p>',
        FOOTER, '  </main>', '  <script src="script.js"></script>', '</body>', '</html>', '',
    ])
    with open(slug, "w", encoding="utf-8") as f:
        f.write(body)
    print("Generated:", slug)

def locations_hub():
    slug = "dscr-calculator-locations.html"
    title = "DSCR Calculators by City | fin·calc"
    desc = ("Free DSCR (Debt Service Coverage Ratio) calculators for short-term rental investors "
            "in the top US real estate markets.")
    head = HEAD.format(title=title, desc=desc, slug=slug, host=HOST)
    links = "\n".join('        <a href="{}">{}, {}</a>'.format(slug_for(m), m["city"], m["abbr"]) for m in markets)
    body = "\n".join([
        '<!DOCTYPE html>', '<html lang="en">', '<head>', head, '</head>', '<body>', '  <main>', HEADER,
        '    <h1>DSCR Calculators by City</h1>',
        '    <p class="intro">Select your market to calculate the Debt Service Coverage Ratio for a short-term rental:</p>',
        '    <div class="country-links">', links, '    </div>',
        '    <p style="margin-top:20px;"><a href="dscr-calculator.html">General DSCR calculator (all markets) &rarr;</a></p>',
        FOOTER, '  </main>', '</body>', '</html>', '',
    ])
    with open(slug, "w", encoding="utf-8") as f:
        f.write(body)
    print("Generated:", slug)

def _noindex(path):
    try:
        return bool(re.search(r'name=["\']robots["\'][^>]*noindex',
                              open(path, encoding="utf-8").read(4000), re.I))
    except Exception:
        return True

def generate_sitemap():
    """Rebuild a COMPLETE, VALID sitemap by scanning every .html file (skipping
    noindex pages). Prevents the sitemap from ever being truncated or stale."""
    HUBS = {"home-loan-calculator", "car-loan-calculator", "sip-calculator", "fixed-deposit-calculator",
            "education-loan-calculator", "zakat-calculator", "retirement-calculator", "rent-vs-buy-calculator"}
    INFO = {"about", "contact", "privacy", "methodology", "editorial-policy"}
    today = date.today().isoformat()
    entries, seen = [], set()
    def push(u, p):
        if u in seen:
            return
        seen.add(u)
        entries.append((u, p))
    push(HOST + "/", "1.0")
    if os.path.exists("pages/index.html"):
        push(HOST + "/pages/index.html", "0.9")
    for f in sorted(glob.glob("*.html")):
        b = f[:-5]
        if f == "index.html" or _noindex(f):
            continue
        if b in INFO:
            push(HOST + "/" + f, "0.4")
        elif b == "dscr-calculator":
            push(HOST + "/" + f, "0.8")
        elif b.startswith("dscr-calculator-"):
            push(HOST + "/" + f, "0.7")
        else:
            push(HOST + "/" + f, "0.6")
    for f in sorted(glob.glob("pages/*.html")):
        f = f.replace("\\", "/")   # normalize Windows backslash -> URL forward slash
        b = os.path.basename(f)[:-5]
        if b == "index.html" or _noindex(f):
            continue
        push(HOST + "/" + f, "0.9" if b in HUBS else "0.8")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, p in entries:
        out.append('  <url><loc>{}</loc><lastmod>{}</lastmod><priority>{}</priority><changefreq>weekly</changefreq></url>'.format(u, today, p))
    out.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Generated: sitemap.xml ({} URLs)".format(len(entries)))

if __name__ == "__main__":
    for m in markets:
        city_page(m)
    locations_hub()
    generate_sitemap()
