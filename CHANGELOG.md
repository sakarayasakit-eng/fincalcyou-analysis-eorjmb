# fincalcyou — Changelog

## 2026-08-11 - Cycle 3
### New calculators (pure-math, formulas verified in Node)
- Mortgage Refinance (`/pages/mortgage-refinance-calculator.html`) - current vs new loan, monthly saving, break-even months, interest comparison.
- Amortization (`/pages/amortization-calculator.html`) - payment, total interest, year-by-year principal/interest schedule, extra-payment effect.
### Internal linking
- Wired both into sitemap, directory (Main calculators), and cross-linked with affordability + debt-payoff + US mortgage. Zero orphans (6 inbound each).
### Next (P1/P2)
- CAGR, extra-payment/early-payoff, debt-consolidation, savings/APY calculators; then country finance hubs.


## 2026-08-11 - Cycle 2
### New calculators (all pure-math, formulas verified in Node)
- Credit Card Payoff (`/pages/credit-card-payoff-calculator.html`) - balance/APR/payment -> months + interest, with neg-amortization guard.
- Debt-to-Income (DTI) (`/pages/debt-to-income-calculator.html`) - front/back ratios + lender-band verdict.
- Balance Transfer (`/pages/balance-transfer-calculator.html`) - stay vs transfer (intro/go-to rate + fee), net saving.
- Compound Interest (`/pages/compound-interest-calculator.html`) - FV of principal + monthly contributions.
### Internal linking
- Wired all 4 into sitemap, directory (Main calculators), and cross-linked a "debt & credit" cluster with debt-payoff + affordability + retirement. Zero orphans (3-6 inbound each).
### Tooling
- Added `.gitattributes` (normalize line endings to LF) to end the recurring CRLF churn. Commit separately with: git add --renormalize . (one-time).
### Next (P1)
- Mortgage refinance, standalone amortization, CAGR, extra-payment calculators.


## 2026-08-11 — Cycle 1 (global platform initiative)
### Security
- Added site-wide Content-Security-Policy via netlify.toml, in REPORT-ONLY mode (addresses WebIntelPro P0 "no CSP on 296 pages"). Report-Only is deliberate: Google only supports nonce-based strict CSP for AdSense and warns allow-list CSPs may disrupt ad serving, so during the active AdSense review this cannot block ads or the EEA consent (CMP) message. Allow-list kept complete (AdSense + Funding Choices CMP + adtrafficquality) to flip to enforcing after approval.
### New calculators
- Debt Payoff Calculator (`/pages/debt-payoff-calculator.html`) — multi-debt avalanche vs snowball with minimum-payment rollover. Algorithm verified in Node (avalanche interest <= snowball; neg-amortization guard; zero-APR sanity). Full methodology, FAQ, schema, trust footer.
### Internal linking
- Wired debt-payoff into sitemap, the directory (Main calculators), and the affordability + retirement guides (3 inbound links — not an orphan).
### Research / roadmap
- Market research on calculator demand + credit-card data/affiliate reality.
- Growth reports under `reports/fincalcyou/growth/` (opportunities, calculator_roadmap, revenue_opportunities, STRATEGY). Blocked from public serving via robots.txt + _redirects.
### Decisions
- Credit-card & bank COMPARISON directories = GATED on verified data + affiliate + compliance (not built; no fake data).
### Next (P0)
- Credit-card payoff, DTI, balance-transfer, compound-interest calculators (pure math, no data).
