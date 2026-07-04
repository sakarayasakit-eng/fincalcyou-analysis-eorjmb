"""
fix_seo.py — rewrite <title>, <meta name="description">, and the
"Related calculators" link block across pages/*.html.

Scope (deliberately narrow, per the task):
  - Only <title>, <meta name="description">, and an EXISTING
    "Related calculators" / "Related" <h2> section are touched.
  - Everything else (calculator HTML/JS, FAQ, worked examples, CSS,
    footer text) is left byte-for-byte alone.
  - Pages with no existing Related-calculators <h2> are NOT given a new
    one (country hubs use a different .hub-grid pattern; a few generic
    tool pages use "Other calculators" instead) -- these are flagged,
    not modified, so as not to bolt a redundant section onto a page
    that already links out a different way.

Run with DRY_RUN = True first to preview title/description/link output
without writing anything, then set to False to apply.
"""
import os
import re
import sys

DRY_RUN = "--apply" not in sys.argv

PAGES_DIR = "pages"
BASE_URL = "https://fincalcyou.netlify.app"

# ================================================================
# COUNTRY LOOKUP: slug suffix -> (display name, currency symbol/code
# for use in English prose, "in <country>" phrase)
# ================================================================
COUNTRY = {
    "india": ("India", "₹"),
    "pakistan": ("Pakistan", "₨"),
    "bangladesh": ("Bangladesh", "৳"),
    "sri-lanka": ("Sri Lanka", "LKR"),
    "usa": ("the USA", "$"),
    "uk": ("the UK", "£"),
    "canada": ("Canada", "C$"),
    "australia": ("Australia", "A$"),
    "new-zealand": ("New Zealand", "NZ$"),
    "uae": ("the UAE", "AED"),
    "saudi-arabia": ("Saudi Arabia", "SAR"),
    "qatar": ("Qatar", "QAR"),
    "kuwait": ("Kuwait", "KWD"),
    "bahrain": ("Bahrain", "BHD"),
    "egypt": ("Egypt", "EGP"),
    "nigeria": ("Nigeria", "₦"),
    "kenya": ("Kenya", "KSh"),
    "south-africa": ("South Africa", "R"),
    "malaysia": ("Malaysia", "RM"),
    "indonesia": ("Indonesia", "Rp"),
    "philippines": ("the Philippines", "₱"),
    "singapore": ("Singapore", "S$"),
    "thailand": ("Thailand", "฿"),
    "vietnam": ("Vietnam", "₫"),
    "hong-kong": ("Hong Kong", "HK$"),
    "china": ("China", "¥"),
    "japan": ("Japan", "¥"),
    "south-korea": ("South Korea", "₩"),
    "taiwan": ("Taiwan", "NT$"),
    "russia": ("Russia", "₽"),
    "eurozone": ("the Eurozone", "€"),
    "mexico": ("Mexico", "MX$"),
    "brazil": ("Brazil", "R$"),
    "turkey": ("Turkey", "₺"),
}

# filename -> (Bank display name, country slug for related-links lookup)
BANK = {
    "hdfc-home-loan-emi-calculator": ("HDFC Bank", "india"),
    "hdfc-fd-calculator": ("HDFC Bank", "india"),
    "icici-home-loan-emi-calculator": ("ICICI Bank", "india"),
    "icici-fd-calculator": ("ICICI Bank", "india"),
    "sbi-home-loan-emi-calculator": ("SBI", "india"),
    "sbi-fd-calculator": ("SBI", "india"),
    "axis-home-loan-emi-calculator": ("Axis Bank", "india"),
    "chase-mortgage-calculator": ("Chase", "usa"),
    "bank-of-america-mortgage-calculator": ("Bank of America", "usa"),
    "wells-fargo-mortgage-calculator": ("Wells Fargo", "usa"),
    "rocket-mortgage-mortgage-calculator": ("Rocket Mortgage", "usa"),
    "hsbc-uk-mortgage-calculator": ("HSBC UK", "uk"),
    "barclays-mortgage-calculator": ("Barclays", "uk"),
    "halifax-mortgage-calculator": ("Halifax", "uk"),
    "natwest-mortgage-calculator": ("NatWest", "uk"),
    "santander-uk-mortgage-calculator": ("Santander UK", "uk"),
    "nationwide-mortgage-calculator": ("Nationwide", "uk"),
    "rbc-mortgage-calculator": ("RBC", "canada"),
    "td-canada-mortgage-calculator": ("TD Canada", "canada"),
    "scotiabank-mortgage-calculator": ("Scotiabank", "canada"),
    "cba-home-loan-calculator": ("CommBank (CBA)", "australia"),
    "nab-home-loan-calculator": ("NAB", "australia"),
    "anz-home-loan-calculator": ("ANZ", "australia"),
    "westpac-home-loan-calculator": ("Westpac", "australia"),
    "maybank-home-loan-calculator": ("Maybank", "malaysia"),
    "cimb-home-loan-calculator": ("CIMB", "malaysia"),
    "public-bank-home-loan-calculator": ("Public Bank", "malaysia"),
    "rhb-home-loan-calculator": ("RHB", "malaysia"),
    "al-rajhi-home-finance-calculator": ("Al Rajhi Bank", "saudi-arabia"),
    "alinma-home-finance-calculator": ("Alinma Bank", "saudi-arabia"),
    "snb-home-finance-calculator": ("Saudi National Bank (SNB)", "saudi-arabia"),
    "adcb-mortgage-calculator": ("ADCB", "uae"),
    "emirates-nbd-mortgage-calculator": ("Emirates NBD", "uae"),
    "fab-mortgage-calculator": ("FAB (First Abu Dhabi Bank)", "uae"),
    "dib-mortgage-calculator": ("Dubai Islamic Bank", "uae"),
    "hbl-home-financing-calculator": ("HBL", "pakistan"),
    "hbl-car-finance-calculator": ("HBL", "pakistan"),
    "mcb-home-financing-calculator": ("MCB Bank", "pakistan"),
    "meezan-home-financing-calculator": ("Meezan Bank", "pakistan"),
    "meezan-car-finance-calculator": ("Meezan Bank", "pakistan"),
    "ubl-car-finance-calculator": ("UBL", "pakistan"),
    "bank-alfalah-car-finance-calculator": ("Bank Alfalah", "pakistan"),
    "bca-kpr-calculator": ("BCA", "indonesia"),
    "bri-kpr-calculator": ("BRI", "indonesia"),
    "btn-kpr-calculator": ("BTN", "indonesia"),
    "mandiri-kpr-calculator": ("Bank Mandiri", "indonesia"),
    "brac-bank-home-loan-calculator": ("BRAC Bank", "bangladesh"),
    "dbbl-home-loan-calculator": ("Dutch-Bangla Bank", "bangladesh"),
    "city-bank-home-loan-calculator": ("City Bank", "bangladesh"),
    "access-bank-loan-calculator": ("Access Bank", "nigeria"),
    "gtbank-loan-calculator": ("GTBank", "nigeria"),
    "uba-loan-calculator": ("UBA", "nigeria"),
    "zenith-bank-loan-calculator": ("Zenith Bank", "nigeria"),
    "pag-ibig-housing-loan-calculator": ("Pag-IBIG", "philippines"),
}

# Known slugs that exist (from the sitemap mapping given), used to check
# an internal link target actually exists before wiring it in.
KNOWN_EXTRA_SLUGS = {
    "housing-loan-calculator-sri-lanka.html",
    "konut-kredisi-hesaplama.html", "tasit-kredisi-hesaplama.html",
    "credito-hipotecario-mexico.html", "financiamento-imobiliario-brasil.html",
    "kpr-calculator-indonesia.html", "loan-calculator-nigeria.html",
    "vehicle-finance-south-africa.html", "home-finance-calculator-saudi-arabia.html",
    "end-of-service-calculator-saudi-arabia.html", "home-loan-emi-calculator-india.html",
    "home-loan-emi-pakistan.html", "mera-pakistan-mera-ghar-calculator.html",
}

def existing_slugs():
    return set(f for f in os.listdir(PAGES_DIR) if f.endswith(".html"))

EXISTING = None  # populated in main()

def slug_for(country_key, category):
    """Best-effort existing filename for category+country, else None."""
    candidates = {
        ("home", "india"): "home-loan-emi-calculator-india.html",
        ("home", "pakistan"): "home-loan-emi-pakistan.html",
        ("home", "sri-lanka"): "housing-loan-calculator-sri-lanka.html",
        ("home", "indonesia"): "kpr-calculator-indonesia.html",
        ("home", "mexico"): "credito-hipotecario-mexico.html",
        ("home", "brazil"): "financiamento-imobiliario-brasil.html",
        ("home", "turkey"): "konut-kredisi-hesaplama.html",
        ("home", "saudi-arabia"): "home-finance-calculator-saudi-arabia.html",
        ("home", "qatar"): "home-finance-calculator-qatar.html",
        ("home", "kuwait"): "home-finance-calculator-kuwait.html",
        ("home", "bahrain"): "home-finance-calculator-bahrain.html",
        ("home", "nigeria"): "loan-calculator-nigeria.html",
        ("home", "south-africa"): "home-loan-calculator-south-africa.html",
        ("car", "turkey"): "tasit-kredisi-hesaplama.html",
        ("car", "south-africa"): "vehicle-finance-south-africa.html",
        ("gratuity", "saudi-arabia"): "end-of-service-calculator-saudi-arabia.html",
    }
    if (category, country_key) in candidates:
        return candidates[(category, country_key)]
    prefix_map = {
        "home": "mortgage-calculator-{c}.html",
        "car": "car-loan-calculator-{c}.html",
        "sip": "sip-calculator-{c}.html",
        "fd": "fixed-deposit-calculator-{c}.html",
        "retirement": "retirement-calculator-{c}.html",
        "rentbuy": "rent-vs-buy-calculator-{c}.html",
        "edu": "education-loan-calculator-{c}.html",
        "zakat": "zakat-calculator-{c}.html",
        "gratuity": "gratuity-calculator-{c}.html",
    }
    guess = prefix_map.get(category, "").format(c=country_key)
    if guess and guess in EXISTING:
        return guess
    # try home-loan-calculator-<c> variant
    if category == "home":
        alt = "home-loan-calculator-{c}.html".format(c=country_key)
        if alt in EXISTING:
            return alt
    return None

# ================================================================
# CLASSIFY a filename -> dict with category/country/bank/amount/etc.
# ================================================================
def classify(fname):
    stem = fname[:-5]  # strip .html

    m = re.match(r"^(\d[\d.]*)-(crore|lakh)-home-loan-emi-calculator$", stem)
    if m:
        amt = m.group(1) + " " + m.group(2).capitalize()
        return {"cat": "home-amount", "amount": "₹" + amt}

    m = re.match(r"^home-loan-on-(.+)-salary$", stem)
    if m:
        salary = "₹" + format_indian_amount(m.group(1))
        return {"cat": "home-salary", "salary": salary}

    m = re.match(r"^sip-(\d+)-per-month$", stem)
    if m:
        return {"cat": "sip-amount", "amount": "₹" + format_indian_amount(m.group(1))}
    if stem == "sip-calculator-1-crore":
        return {"cat": "sip-amount", "amount": "₹1 Crore"}

    m = re.match(r"^([a-z]{3})-to-([a-z]{3})-converter$", stem)
    if m:
        return {"cat": "converter", "src": m.group(1).upper(), "dst": m.group(2).upper()}

    if stem in BANK:
        bank_name, country_key = BANK[stem]
        sub = ("fd" if "fd-calculator" in stem or "fd-calculator" in fname
               else "car" if "car-finance" in stem
               else "home")
        return {"cat": "bank-" + sub, "bank": bank_name, "country": country_key}

    if stem.startswith("what-is-"):
        return {"cat": "glossary", "term": stem[len("what-is-"):]}
    if stem == "glossary":
        return {"cat": "glossary-index"}
    if stem == "how-to-calculate-emi":
        return {"cat": "emi-formula"}
    if stem.startswith("central-bank-rates"):
        return {"cat": "central-bank"}
    if stem.endswith("-financial-calculators"):
        country_key = stem[:-len("-financial-calculators")]
        return {"cat": "country-hub", "country": country_key}

    if stem.startswith("gratuity-calculator-") or stem.startswith("end-of-service-calculator-"):
        country_key = stem.split("-calculator-")[-1]
        return {"cat": "gratuity", "country": country_key}

    if stem.startswith("zakat-calculator"):
        rest = stem[len("zakat-calculator"):].lstrip("-")
        if not rest or rest == "2026":
            return {"cat": "zakat-generic"}
        return {"cat": "zakat", "country": rest}

    if stem.startswith("rent-vs-buy-calculator"):
        rest = stem[len("rent-vs-buy-calculator"):].lstrip("-")
        return {"cat": "rentbuy", "country": rest} if rest else {"cat": "rentbuy-generic"}

    if stem.startswith("retirement-calculator"):
        rest = stem[len("retirement-calculator"):].lstrip("-")
        return {"cat": "retirement", "country": rest} if rest else {"cat": "retirement-generic"}

    if stem.startswith("education-loan-calculator"):
        rest = stem[len("education-loan-calculator"):].lstrip("-")
        return {"cat": "edu", "country": rest} if rest else {"cat": "edu-generic"}

    if stem.startswith("fixed-deposit-calculator"):
        rest = stem[len("fixed-deposit-calculator"):].lstrip("-")
        return {"cat": "fd", "country": rest} if rest else {"cat": "fd-generic"}

    if stem.startswith("sip-calculator"):
        rest = stem[len("sip-calculator"):].lstrip("-")
        if rest in ("india-20-years",):
            return {"cat": "sip", "country": "india"}
        return {"cat": "sip", "country": rest} if rest else {"cat": "sip-generic"}

    # Home loan / mortgage family (broad, various historical prefixes)
    home_prefixes = [
        "home-loan-calculator-", "mortgage-calculator-", "home-finance-calculator-",
        "housing-loan-calculator-",
    ]
    for p in home_prefixes:
        if stem.startswith(p):
            return {"cat": "home", "country": stem[len(p):]}
    special_home = {
        "home-loan-emi-calculator-india": "india",
        "home-loan-emi-pakistan": "pakistan",
        "konut-kredisi-hesaplama": "turkey",
        "kpr-calculator-indonesia": "indonesia",
        "credito-hipotecario-mexico": "mexico",
        "financiamento-imobiliario-brasil": "brazil",
        "loan-calculator-nigeria": "nigeria",
        "mera-pakistan-mera-ghar-calculator": "pakistan",
    }
    if stem in special_home:
        return {"cat": "home", "country": special_home[stem]}
    if stem == "home-loan-calculator":
        return {"cat": "home-generic"}

    # Car loan / auto finance family
    car_prefixes = ["car-loan-calculator-", "car-finance-calculator-"]
    for p in car_prefixes:
        if stem.startswith(p):
            return {"cat": "car", "country": stem[len(p):]}
    special_car = {"tasit-kredisi-hesaplama": "turkey", "vehicle-finance-south-africa": "south-africa"}
    if stem in special_car:
        return {"cat": "car", "country": special_car[stem]}
    if stem == "car-loan-calculator":
        return {"cat": "car-generic"}

    if stem == "index":
        return {"cat": "guides-index"}
    if stem.startswith("DEMO-"):
        return {"cat": "demo"}

    return {"cat": "unknown"}


def country_name(key):
    return COUNTRY.get(key, (key.replace("-", " ").title(), ""))[0]


def country_name_cap(key):
    """Country name without a leading 'the', for use at the START of a title."""
    name = country_name(key)
    return name[4:] if name.startswith("the ") else name


def country_cur(key):
    return COUNTRY.get(key, ("", ""))[1]


def format_indian_amount(raw):
    """'50000' -> '50,000'; '1-lakh' -> '1 Lakh'; '1.5-crore' -> '1.5 Crore'."""
    m = re.match(r"^(\d+(?:\.\d+)?)-(lakh|crore)$", raw)
    if m:
        return f"{m.group(1)} {m.group(2).capitalize()}"
    if raw.isdigit():
        return f"{int(raw):,}"
    return raw


ACRONYMS = {"emi": "EMI", "sip": "SIP", "ltv": "LTV", "foir": "FOIR", "eblr": "EBLR"}

def format_glossary_term(term_slug):
    """'compound-interest' -> 'Compound Interest'; 'emi' -> 'EMI'."""
    words = term_slug.split("-")
    return " ".join(ACRONYMS.get(w.lower(), w.capitalize()) for w in words)


# ================================================================
# TITLE generation
# ================================================================
def make_title(info):
    cat = info["cat"]
    if cat == "home-amount":
        return f"{info['amount']} Home Loan EMI Calculator – Monthly Payment Estimate"
    if cat == "home-salary":
        return f"Home Loan on {info['salary']} Salary – How Much You Can Borrow"
    if cat == "sip-amount":
        return f"SIP {info['amount']} Per Month – Future Value After 10/20 Years"
    if cat == "converter":
        return f"{info['src']} to {info['dst']} Converter – Live Mid-Market Rate"
    if cat == "bank-home":
        return f"{info['bank']} Home Loan Calculator – Monthly Payment Estimate"
    if cat == "bank-car":
        return f"{info['bank']} Car Finance Calculator – Monthly Installment Estimate"
    if cat == "bank-fd":
        return f"{info['bank']} FD Calculator – Interest & Maturity Estimate"
    if cat == "glossary":
        term = format_glossary_term(info["term"])
        return f"What is {term}? – Plain-English Definition & Example"
    if cat == "glossary-index":
        return "Finance Glossary – Plain-English Definitions for Loan & Investment Terms"
    if cat == "emi-formula":
        return "How to Calculate Loan EMI – Formula & Worked Examples"
    if cat == "central-bank":
        return "Central Bank & Loan Rates Across 34 Countries (2026)"
    if cat == "country-hub":
        cname = country_name_cap(info["country"])
        return f"{cname} Financial Calculators – Home Loan, Car, SIP, FD & More"
    if cat == "gratuity":
        cname = country_name_cap(info["country"])
        return f"{cname} End of Service Gratuity Calculator – Estimate Your Benefit"
    if cat == "zakat-generic":
        return "Zakat Calculator 2026 – Calculate 2.5% on Net Wealth"
    if cat == "zakat":
        cname = country_name(info["country"])
        return f"Zakat Calculator in {cname} – Calculate 2.5% on Wealth"
    if cat in ("rentbuy", "rentbuy-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Rent vs Buy Calculator in {cname} – Which Saves More" if info.get("country")
                else "Rent vs Buy Calculator – Which Saves More")
    if cat in ("retirement", "retirement-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Retirement Calculator in {cname} – Monthly SIP Needed to Retire" if info.get("country")
                else "Retirement Calculator – Monthly Savings Needed to Retire")
    if cat in ("edu", "edu-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Education Loan Calculator in {cname} – Repayment After Moratorium" if info.get("country")
                else "Education Loan Calculator – Repayment After Moratorium")
    if cat in ("fd", "fd-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Fixed Deposit Calculator in {cname} – Maturity Value Estimate" if info.get("country")
                else "Fixed Deposit Calculator – Maturity Value Estimate")
    if cat in ("sip", "sip-generic"):
        cname = country_name(info.get("country", ""))
        return (f"SIP Calculator in {cname} – Monthly Investment Growth Estimate" if info.get("country")
                else "SIP Calculator – Monthly Investment Growth Estimate")
    if cat in ("home", "home-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Home Loan Calculator in {cname} – Monthly Mortgage Estimate" if info.get("country")
                else "Home Loan Calculator – Monthly Mortgage Estimate")
    if cat in ("car", "car-generic"):
        cname = country_name(info.get("country", ""))
        return (f"Car Loan Calculator in {cname} – Monthly Auto Finance Estimate" if info.get("country")
                else "Car Loan Calculator – Monthly Auto Finance Estimate")
    return None


# ================================================================
# META DESCRIPTION generation (140-160 chars target)
# ================================================================
def make_description(info):
    cat = info["cat"]

    def fit(s):
        # Nudge toward 140-160 chars without truncating mid-word/breaking meaning.
        if len(s) > 160:
            s = s[:157].rsplit(" ", 1)[0] + "..."
        return s

    if cat == "home-amount":
        return fit(f"Estimate your {info['amount']} home loan EMI across 10–30 year tenures at current rates. See monthly payment and total interest. Free, no signup.")
    if cat == "home-salary":
        return fit(f"Work out the maximum home loan you can afford on a {info['salary']} salary using the standard FOIR rule. Free, no signup.")
    if cat == "sip-amount":
        return fit(f"Calculate how a {info['amount']} monthly SIP grows over 10 and 20 years at historical market returns. Free, no signup.")
    if cat == "converter":
        return fit(f"Convert {info['src']} to {info['dst']} at the live mid-market rate and compare the cheapest ways to send money. Free, no signup.")
    if cat == "bank-home":
        cname = country_name(info["country"])
        cur = country_cur(info["country"])
        return fit(f"Estimate your {info['bank']} home loan monthly payment in {cur} using current 2026 rates for {cname}. See total interest over your loan tenure. Free, no signup.")
    if cat == "bank-car":
        cname = country_name(info["country"])
        cur = country_cur(info["country"])
        return fit(f"Calculate your {info['bank']} car finance monthly installment in {cur} for {cname} at current 2026 auto-finance rates. Free, no signup.")
    if cat == "bank-fd":
        cname = country_name(info["country"])
        cur = country_cur(info["country"])
        return fit(f"Estimate your {info['bank']} fixed deposit maturity value and interest earned in {cur} for {cname} at current 2026 rates. Free, no signup.")
    if cat == "glossary":
        term = format_glossary_term(info["term"])
        return fit(f"Work out what {term} means in plain English, with a worked example using real loan numbers. Free, no signup.")
    if cat == "glossary-index":
        return fit("Work out what EMI, SIP, LTV, FOIR and other finance terms mean in plain English, with worked examples. Free, no signup.")
    if cat == "emi-formula":
        return fit("Work out the EMI formula step by step, with a worked example on a real loan amount, rate and tenure. Free, no signup.")
    if cat == "central-bank":
        return fit("Compare central bank policy rates and typical home/car loan and savings rates across 34 countries for 2026. Free, no signup.")
    if cat == "country-hub":
        cname = country_name(info["country"])
        return fit(f"Calculate home loan, car loan, SIP, fixed deposit and Zakat for {cname} with real local bank rates. Free, no signup.")
    if cat == "gratuity":
        cname = country_name(info["country"])
        cur = country_cur(info["country"])
        return fit(f"Estimate your end-of-service gratuity in {cur} for {cname} based on your salary and years of service. Free, no signup.")
    if cat == "zakat-generic":
        return fit("Calculate the 2.5% Zakat due on your cash, gold, silver and investments above the nisab threshold. Free, no signup.")
    if cat == "zakat":
        cname = country_name(info["country"])
        cur = country_cur(info["country"])
        return fit(f"Calculate Zakat in {cname} on cash, gold and investments using live nisab in {cur}. Free, no signup.")
    if cat in ("rentbuy", "rentbuy-generic"):
        cname = info.get("country") and country_name(info["country"])
        return fit(f"Compare renting versus buying in {cname} over the years you plan to stay, using real rent and price growth. Free, no signup." if cname
                   else "Compare renting versus buying over the years you plan to stay, using real rent and price growth. Free, no signup.")
    if cat in ("retirement", "retirement-generic"):
        cname = info.get("country") and country_name(info["country"])
        return fit(f"Work out the monthly SIP you need to retire comfortably in {cname}, adjusted for inflation. Free, no signup." if cname
                   else "Work out the monthly savings you need to retire comfortably, adjusted for inflation. Free, no signup.")
    if cat in ("edu", "edu-generic"):
        cname = info.get("country") and country_name(info["country"])
        return fit(f"Estimate your education loan repayment after the moratorium period in {cname}, including accrued interest. Free, no signup." if cname
                   else "Estimate your education loan repayment after the moratorium period, including accrued interest. Free, no signup.")
    if cat in ("fd", "fd-generic"):
        cname = info.get("country") and country_name(info["country"])
        cur = info.get("country") and country_cur(info["country"])
        return fit(f"Estimate your fixed deposit maturity value and total interest earned in {cur} for {cname}, using current bank rates and your chosen term. Free, no signup." if cname
                   else "Estimate your fixed deposit maturity value and total interest earned at current bank rates and your chosen term. Free, no signup.")
    if cat in ("sip", "sip-generic"):
        cname = info.get("country") and country_name(info["country"])
        return fit(f"Calculate how your monthly SIP grows in {cname} over 10, 20 or 30 years using historical market return assumptions. Free, no signup." if cname
                   else "Calculate how your monthly SIP grows over 10, 20 or 30 years using historical market return assumptions. Free, no signup.")
    if cat in ("home", "home-generic"):
        cname = info.get("country") and country_name(info["country"])
        cur = info.get("country") and country_cur(info["country"])
        return fit(f"Calculate your home loan monthly payment in {cur} for {cname} using current bank interest rates and your chosen loan tenure. Free, no signup." if cname
                   else "Calculate your home loan monthly payment using current bank interest rates and your chosen loan tenure. Free, no signup.")
    if cat in ("car", "car-generic"):
        cname = info.get("country") and country_name(info["country"])
        cur = info.get("country") and country_cur(info["country"])
        return fit(f"Calculate your car loan monthly installment in {cur} for {cname} using current auto-finance rates and your loan term. Free, no signup." if cname
                   else "Calculate your car loan monthly installment using current auto-finance rates and your loan term. Free, no signup.")
    return None


# ================================================================
# RELATED CALCULATORS: contextual link list per category mapping
# ================================================================
def add_link(links, seen, text, slug):
    """Append (text, slug) if the target file exists and isn't a dup."""
    if not slug or slug in seen:
        return
    if slug not in EXISTING and slug not in KNOWN_EXTRA_SLUGS:
        return
    seen.add(slug)
    links.append((text, slug))


def make_related_links(fname, info):
    cat = info["cat"]
    country_key = info.get("country")
    links, seen = [], set()
    seen.add(fname)  # never link a page to itself

    def cslug(category, key=country_key):
        return slug_for(key, category) if key else None

    cname = country_name(country_key) if country_key else ""

    if cat in ("home", "home-generic", "home-amount", "home-salary", "bank-home"):
        ck = info.get("country") or (BANK.get(fname[:-5], (None, None))[1])
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Car Loan Calculator – {cn}", cslug("car", ck))
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, f"Rent vs Buy Calculator – {cn}", cslug("rentbuy", ck))
        add_link(links, seen, f"Retirement Calculator – {cn}", cslug("retirement", ck))
        add_link(links, seen, "Affordability Calculator", "home-loan-calculator.html")
        add_link(links, seen, "Home Loan EMI Calculator – India", "home-loan-emi-calculator-india.html")

    elif cat in ("car", "car-generic", "bank-car"):
        ck = info.get("country") or (BANK.get(fname[:-5], (None, None))[1])
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, "Debt Payoff Optimizer", "home-loan-calculator.html")
        add_link(links, seen, "Affordability Calculator", "home-loan-calculator.html")
        add_link(links, seen, "Car Loan Calculator – India", "car-loan-calculator-india.html")

    elif cat in ("sip", "sip-generic", "sip-amount"):
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"Retirement Calculator – {cn}", cslug("retirement", ck))
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, "SIP Calculator – India", "sip-calculator-india-20-years.html")

    elif cat in ("fd", "fd-generic", "bank-fd"):
        ck = info.get("country") or (BANK.get(fname[:-5], (None, None))[1])
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, f"Retirement Calculator – {cn}", cslug("retirement", ck))
        add_link(links, seen, "Fixed Deposit Calculator – India", "fixed-deposit-calculator-india.html")

    elif cat in ("retirement", "retirement-generic"):
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, "Retirement Calculator – India", "retirement-calculator-india.html")

    elif cat in ("rentbuy", "rentbuy-generic"):
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, "How Much Loan Can I Afford", "home-loan-calculator.html")
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, "Rent vs Buy Calculator – India", "rent-vs-buy-calculator-india.html")

    elif cat in ("edu", "edu-generic"):
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, "Financial Health Check", "../index.html?tab=health")
        add_link(links, seen, "Education Loan Calculator – India", "education-loan-calculator-india.html")

    elif cat in ("zakat", "zakat-generic"):
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Home Loan Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"SIP Calculator – {cn}", cslug("sip", ck))
        add_link(links, seen, "Zakat Calculator 2026", "zakat-calculator-2026.html")
        add_link(links, seen, "Zakat Calculator – Pakistan", "zakat-calculator-pakistan.html")

    elif cat == "converter":
        src_key = next((k for k, v in COUNTRY.items() if v[1] == info["src"] or k == info["src"].lower()), None)
        # currency code -> country slug isn't 1:1 from COUNTRY (keyed by symbol);
        # fall back to a small explicit map for the converter pairs actually used.
        cur_country = {
            "AED": "uae", "PKR": "pakistan", "INR": "india", "SAR": "saudi-arabia",
            "GBP": "uk", "BDT": "bangladesh", "NGN": "nigeria", "AUD": "australia",
            "CAD": "canada", "EGP": "egypt", "KES": "kenya", "LKR": "sri-lanka",
            "MXN": "mexico", "PHP": "philippines", "TRY": "turkey", "VND": "vietnam",
            "USD": "usa",
        }
        src_ck = cur_country.get(info["src"])
        dst_ck = cur_country.get(info["dst"])
        if src_ck:
            add_link(links, seen, f"Home Loan Calculator – {country_name(src_ck)}", cslug("home", src_ck))
            add_link(links, seen, f"SIP Calculator – {country_name(src_ck)}", cslug("sip", src_ck))
        if dst_ck:
            add_link(links, seen, f"Home Loan Calculator – {country_name(dst_ck)}", cslug("home", dst_ck))
            add_link(links, seen, f"Fixed Deposit Calculator – {country_name(dst_ck)}", cslug("fd", dst_ck))

    elif cat == "gratuity":
        ck = country_key
        cn = country_name(ck) if ck else ""
        add_link(links, seen, f"Home Finance Calculator – {cn}", cslug("home", ck))
        add_link(links, seen, f"Fixed Deposit Calculator – {cn}", cslug("fd", ck))
        add_link(links, seen, f"Retirement Calculator – {cn}", cslug("retirement", ck))
        add_link(links, seen, "Financial Health Check", "../index.html?tab=health")

    elif cat in ("glossary",):
        add_link(links, seen, "Finance Glossary", "glossary.html")
        add_link(links, seen, "How to Calculate Loan EMI", "how-to-calculate-emi.html")
        add_link(links, seen, "Central Bank & Loan Rates Across 34 Countries", "central-bank-rates-2026.html")
        term_target = {
            "emi": "home-loan-emi-calculator-india.html", "sip": "sip-calculator-india-20-years.html",
            "fixed-deposit": "fixed-deposit-calculator-india.html", "zakat": "zakat-calculator-2026.html",
            "murabaha": "al-rajhi-home-finance-calculator.html", "ijarah": "meezan-car-finance-calculator.html",
            "repo-rate": "central-bank-rates-2026.html", "eblr": "home-loan-emi-calculator-india.html",
            "ltv": "home-loan-calculator.html", "down-payment": "home-loan-calculator.html",
            "moratorium": "education-loan-calculator-india.html", "mutual-fund": "sip-calculator-india-20-years.html",
            "foir": "home-loan-calculator.html", "compound-interest": "fixed-deposit-calculator-india.html",
            "amortization": "home-loan-emi-calculator-india.html", "nisab": "zakat-calculator-2026.html",
        }
        tgt = term_target.get(info["term"])
        if tgt:
            add_link(links, seen, "Try the related calculator", tgt)

    return links


TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', re.DOTALL)
RELATED_RE = re.compile(
    r'<section>\s*<h2>Related(?: calculators)?</h2>.*?</section>',
    re.DOTALL,
)


def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def build_related_html(links):
    items = "".join(f'\n        <li><a href="{slug}">{html_escape(text)}</a></li>' for text, slug in links)
    return f'<section>\n      <h2>Related calculators</h2>\n      <ul>{items}\n      </ul>\n    </section>'


def main():
    global EXISTING
    EXISTING = existing_slugs()

    stats = {
        "total": 0, "title_fixed": 0, "desc_fixed": 0, "links_replaced": 0,
        "skipped": [], "flagged_missing": [],
    }

    for fname in sorted(EXISTING):
        stats["total"] += 1
        fpath = os.path.join(PAGES_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        orig_html = html

        # Skip non-content utility files outright.
        if fname == "index.html":
            stats["skipped"].append((fname, "guides index page, not an SEO landing page"))
            continue
        if fname.startswith("DEMO-"):
            stats["skipped"].append((fname, "demo/test file, not a real SEO page"))
            continue
        if "noindex" in re.search(r"<meta[^>]*name=\"robots\"[^>]*>", html).group(0) if re.search(r"<meta[^>]*name=\"robots\"[^>]*>", html) else "":
            stats["skipped"].append((fname, "noindex redirect stub"))
            continue

        info = classify(fname)
        if info["cat"] == "unknown":
            stats["skipped"].append((fname, "could not classify filename into a known category"))
            continue

        # ---- Title ----
        new_title = make_title(info)
        if new_title:
            replacement = f"<title>{html_escape(new_title)}</title>"
            new_html, n = TITLE_RE.subn(replacement, html, count=1)
            if n:
                html = new_html
                stats["title_fixed"] += 1

        # ---- Meta description ----
        new_desc = make_description(info)
        if new_desc:
            replacement = f'<meta name="description" content="{html_escape(new_desc)}" />'
            new_html, n = DESC_RE.subn(replacement, html, count=1)
            if n:
                html = new_html
                stats["desc_fixed"] += 1
            elif "<title>" in html:
                # No existing description tag -- add one right after <title>.
                html = re.sub(r"(</title>)", r"\1\n  " + replacement, html, count=1)
                stats["desc_fixed"] += 1

        # ---- Related calculators ----
        if RELATED_RE.search(html):
            links = make_related_links(fname, info)
            if links:
                html = RELATED_RE.sub(lambda m: build_related_html(links), html, count=1)
                stats["links_replaced"] += 1
            else:
                stats["flagged_missing"].append((fname, "Related section exists but no contextual links could be derived"))
        else:
            stats["flagged_missing"].append((fname, "no 'Related calculators' section found (not added, per scope)"))

        if html != orig_html and not DRY_RUN:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)

    # ---- Summary ----
    mode = "DRY RUN (no files written)" if DRY_RUN else "APPLIED"
    print(f"\n=== fix_seo.py summary [{mode}] ===")
    print(f"Total files processed: {stats['total']}")
    print(f"Titles fixed: {stats['title_fixed']}")
    print(f"Descriptions added/fixed: {stats['desc_fixed']}")
    print(f"Related-links sections replaced: {stats['links_replaced']}")
    print(f"\nSkipped ({len(stats['skipped'])}):")
    for fname, reason in stats["skipped"]:
        print(f"  - {fname}: {reason}")
    print(f"\nFlagged / missing Related section ({len(stats['flagged_missing'])}):")
    for fname, reason in stats["flagged_missing"]:
        print(f"  - {fname}: {reason}")


if __name__ == "__main__":
    main()
