# fin·calc — Working Rules for Claude Code / AI sessions

## ⚠️ FOLDER RULE (most important)

**This repo — `fincalcyou` (GitHub: `sakarayasakit-eng/fincalcyou-analysis-eorjmb`) — is the ONE source of truth AND the deploy target. Do ALL work here.**

- **Do NOT** use, read from, or copy from the old folder
  `C:\Users\HP\Downloads\fincalc_v21_READY_FOR_NETLIFY_101\fincalc`.
  It is **deprecated and stale** — it does not have lead capture, IndexNow, favicons,
  the DSCR calculator, or the latest `index.html`.
- **Do NOT use `robocopy`** or any folder-to-folder sync. The old two-folder
  (`fincalc` → `fincalcyou`) workflow caused divergence and nearly lost work. It is retired.
- Edit files here, commit, and push. That is the entire deploy.

## Deploy

Netlify auto-builds and publishes this repo on every push to `main`:

```
git add -A
git commit -m "your message"
git push
```

After pushing, verify live with a cache-buster in an **incognito** window
(e.g. `https://fincalcyou.netlify.app/?v=NN`). Netlify caches HTML for 5 min and the
site remembers the visitor's chosen currency in `localStorage('fincalc_cur')`, so a
normal refresh in your own browser may show a stale version.

## What this project is

- A **static** finance-calculator site: vanilla HTML/CSS/JS, **no build step**, no framework.
- The whole interactive app is one file: **`index.html`** (~400 KB, inline CSS + JS).
- ~298 SEO landing pages live in **`/pages/`**, sharing `pages/landing.css` + a small
  inline embedded calculator per page.
- Theme: **NerdWallet-style light** (white bg, green `#0e7a4a` accent). Dark mode is the
  optional toggle. Colors are CSS variables in `:root` — retheme via tokens, not per-rule.

## Guardrails (don't break the site)

- **Never change the calculator math, formulas, element IDs, or the country-switch logic.**
  Make the smallest safe presentation/string change that achieves the goal.
- The math is verified against real bank examples — if you touch a calc, re-verify it.
- Do NOT refactor the single `index.html` into modules unless explicitly asked; it works and is fragile.
- India profile data and per-country profiles must stay intact (site is global; USD is the neutral default).

## Features already built (don't duplicate or break)

- **8 calculator hub pages** in `/pages/`: home-loan, car-loan, sip, fixed-deposit,
  education-loan, zakat, retirement, rent-vs-buy — each with an embedded calculator and
  a "choose your country" links block (hub-and-spoke internal linking).
- **hreflang clusters** across the country pages (reciprocal, x-default = root/hub).
- **Lead capture**: `netlify/functions/lead_capture.js` emails leads via Resend.
  Requires env var **`RESEND_API_KEY`** set in Netlify → Site settings → Environment variables.
- **IndexNow**: `.github/workflows/indexnow.yml` + `scripts/` auto-submit URLs to search engines.
- Favicons, `sitemap.xml` (keep new pages added here), `robots.txt`.

## SEO reality (for prioritizing work)

The biggest levers are **backlinks** and a **real custom domain** (currently on the
`.netlify.app` subdomain). Adding more thin pages does not help until existing pages index.
