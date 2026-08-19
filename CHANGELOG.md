# fincalcyou — Changelog

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
