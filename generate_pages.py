import os

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
    {"city": "Las Vegas", "state": "Nevada", "abbr": "NV"}
]

def slug_for(market):
    city = market["city"]
    abbr = market["abbr"]
    return f"dscr-calculator-{city.lower().replace(' ', '-')}-{abbr.lower()}.html"

def generate_html(market):
    city = market["city"]
    state = market["state"]
    abbr = market["abbr"]
    slug = slug_for(market)

    # HTML Template with dynamic SEO variables
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSCR Calculator for Short-Term Rentals in {city}, {abbr} | FinCalcYou</title>
    <meta name="description" content="Calculate the Debt Service Coverage Ratio (DSCR) for your Airbnb or short-term rental property in {city}, {state}. Free, accurate, and built for {city} real estate investors.">

    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; background-color: #f9f9f9; }}
        .calculator-box {{ background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }}
        button {{ background: #007bff; color: #fff; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }}
        button:hover {{ background: #0056b3; }}
        .result {{ margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; display: none; }}
        .lead-gate {{ margin-top: 20px; padding: 20px; border: 2px solid #007bff; border-radius: 8px; display: none; }}
        .lead-gate h3 {{ margin-top: 0; color: #007bff; }}
    </style>
</head>
<body>

    <h1>DSCR Calculator for Short-Term Rentals in {city}, {abbr}</h1>
    <p>Calculate the Debt Service Coverage Ratio (DSCR) for your Airbnb or short-term rental investment in {city}, {state}. Local {city} lenders require a DSCR of 1.25 or higher to approve investment property loans.</p>

    <div class="calculator-box">
        <div class="form-group">
            <label for="rentalIncome">Estimated Annual {city} Short-Term Rental Income ($)</label>
            <input type="number" id="rentalIncome" placeholder="e.g., 45000">
        </div>
        <div class="form-group">
            <label for="operatingExpenses">Annual Operating Expenses (Taxes, Insurance, HOA, etc.) ($)</label>
            <input type="number" id="operatingExpenses" placeholder="e.g., 12000">
        </div>
        <div class="form-group">
            <label for="annualDebtService">Annual Debt Service (Mortgage Principal & Interest) ($)</label>
            <input type="number" id="annualDebtService" placeholder="e.g., 20000">
        </div>

        <button onclick="calculateDSCR()">Calculate DSCR</button>

        <div class="result" id="resultBox">
            <h3>Your DSCR: <span id="dscrValue"></span></h3>
            <p id="dscrMessage"></p>
        </div>

        <div class="lead-gate" id="leadGate">
            <h3>Unlock Full {city} Investment Analysis</h3>
            <p>Enter your email to get your detailed DSCR breakdown, cash-on-cash return, and connect with a {abbr} DSCR lender.</p>
            <input type="email" id="userEmail" placeholder="Investor@example.com">
            <button onclick="submitLead()">Get My Analysis</button>
        </div>
    </div>

    <h2>Why DSCR Matters for {city} Real Estate</h2>
    <p>The {city} short-term rental market is highly competitive. Lenders in {state} use DSCR to evaluate deals without relying on your personal income. A strong DSCR proves your {city} property generates enough rent to cover its own mortgage, making it easier to scale your real estate portfolio.</p>

    <p><a href="dscr-calculator-locations.html">See DSCR calculators for other US markets &rarr;</a></p>

    <script src="script.js"></script>
</body>
</html>"""

    with open(slug, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {slug}")

def generate_locations_hub():
    # A dedicated hub page (NOT the site's real homepage/index.html) so Google
    # has one place to discover all city pages via internal links + sitemap.
    links = "\n".join(
        f'        <li><a href="{slug_for(m)}">{m["city"]}, {m["abbr"]}</a></li>'
        for m in markets
    )
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSCR Calculators by City | FinCalcYou</title>
    <meta name="description" content="Free DSCR (Debt Service Coverage Ratio) calculators for short-term rental investors in the top US real estate markets.">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>DSCR Calculators by City</h1>
    <p>Select your market to calculate DSCR for Short-Term Rentals:</p>
    <ul>
{links}
    </ul>
    <p><a href="dscr-calculator.html">General DSCR Calculator (all markets)</a></p>
</body>
</html>"""

    with open("dscr-calculator-locations.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated: dscr-calculator-locations.html")

# Run the generator
for market in markets:
    generate_html(market)
generate_locations_hub()
