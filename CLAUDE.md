# fin·calc — Working Rules for Claude Code / AI sessions

## ⚠️ FOLDER RULE (most important)

**This repo — `fincalcyou` (GitHub: `sakarayasakit-eng/fincalcyou-analysis-eorjmb`) — is the ONE source of truth AND the deploy target. Do ALL work here.**

- **Do NOT** use, read from, or copy from the old folder
  `C:\Users\HP\Downloads\fincalc_v21_READY_FOR_NETLIFY_101\fincalc`.
  It is **deprecated and stale**.
- **Do NOT use `robocopy`** or any folder-to-folder sync. It caused divergence and nearly lost work. Retired.
- Edit files here, commit, and push. That is the entire deploy.

---

## 🏗️ GENERATOR — change cluster pages WITHOUT hand-editing hundreds of files

**Read this before touching any `car-loan-*`, `sip-*`, or `fixed-deposit-*` page.**

The problem it solves: those country pages used to be near-identical, hand-frozen HTML.
Changing one thing (a rate, a line of copy, the domain) meant editing 26–34 files per
cluster by hand, and they drifted out of sync. They are now **generated from data**, so
one edit + one command updates the whole cluster.

### The pieces
- **`countries.json`** — the single data registry. Top-level keys are clusters:
  `car_loan`, `sip`, `fixed_deposit`. Each is a list of per-country entries
  (country, currency, locale, rate, the local note, related links, etc.).
  Entries marked `"custom": true` are hand-written pages the generator **skips**.
- **`templates/`** — one skeleton per cluster: `car-loan.html`, `sip.html`,
  `fixed-deposit.html`. These hold the *original* section structure with placeholder
  content the generator fills in. **A template is NOT the generated page** — never
  overwrite a template with an enriched/generated page, or re-runs break.
- **`build.py`** — reads `countries.json` + `templates/`, computes the money figures
  with Node's `Intl.NumberFormat` (the *same* formatter the live calculator uses, so the
  static "hint" numbers on the page always match the live tool), and writes the pages
  into `/pages/`.

### 🔑 THE GOLDEN RULE
**To change a generated page, edit `countries.json` (data) or the cluster's
`templates/*.html` / the `render_*`/`enrich_*` function in `build.py` (structure & wording),
then run `python build.py`. NEVER hand-edit
`pages/car-loan-calculator-*.html`, `pages/sip-calculator-*.html`, or
`pages/fixed-deposit-calculator-*.html` — the next `build.py` run overwrites it.**

### Which pages are generated vs hand-maintained
- **GENERATED (edit via the generator):** car-loan (26), sip (28), fixed-deposit (34).
- **HAND-MAINTAINED (edit the page directly — already country-differentiated, do NOT
  run through the generator):** home-loan/mortgage, retirement, education-loan,
  rent-vs-buy, zakat, DSCR, and every `"custom": true` variant (e.g. the India / UAE /
  Turkey car & sip pages). Flattening these into a template would destroy unique content.

### Common tasks
- **Update a country's rate:** change its `rate` in `countries.json` → `python build.py`.
- **Change wording for a whole cluster** (new FAQ, disclaimer, section): edit that
  cluster's `enrich_*`/`render_*` in `build.py` (or its `templates/*.html`) → `python build.py`.
- **Add a country to a cluster:** copy an existing entry's shape in `countries.json`,
  fill its data, add it to the cluster's hreflang set → `python build.py` → add the URL to `sitemap.xml`.
- **Custom-domain migration:** change the host once in the data/templates → `python build.py`
  (fixes all 88 generated pages); then find-replace the host in the hand-maintained pages.
- **Add a whole new cluster to the generator:** add `templates/<cluster>.html`, a data list
  in `countries.json`, a `render_<x>`/`enrich_<x>` in `build.py`, its math to the Node block,
  and an entry in `CLUSTERS`. Then run the idempotency check below.

### ✅ Idempotency check (run after ANY generator change)
```
python build.py
git status        # a correct no-op leaves the tree CLEAN
```
If `git status` shows diffs you didn't intend, the templates/data and the on-disk pages
have drifted — investigate before committing. Requires `python3` + `node`.

### Deep-link embeds
Every standard embed's script updates the "Open the full tool →" link with the visitor's
entered amount/rate/years on input (so clicking it opens the homepage calculator pre-filled).
This block lives in the embed `<script>` **and** in `templates/`, so regeneration keeps it.
If you edit an embed script, preserve it (marker: `_nl=el.querySelector('.fc-note a')`).

---

## Deploy

Netlify auto-builds and publishes on every push to `main`:
```
git add -A
git commit -m "your message"
git pull --rebase origin main   # if the remote has moved
git push
```
Verify live with a cache-buster in an **incognito** window
(e.g. `https://fincalcyou.netlify.app/?v=NN`). Netlify caches HTML ~5 min and the site
remembers the visitor's currency in `localStorage('fincalc_cur')`, so a normal refresh
may show a stale version.

## What this project is
- A **static** finance-calculator site: vanilla HTML/CSS/JS, hosted on Netlify.
- The interactive app is one file: **`index.html`** (~400 KB, inline CSS + JS). No framework.
  (This file is hand-maintained, NOT generated.)
- ~298 SEO landing pages in **`/pages/`**, sharing `pages/landing.css` + a small inline
  embedded calculator each. The car/sip/fd country pages are **generated** (see above).
- Theme: **NerdWallet-style light** (white bg, green `#0e7a4a` accent); dark mode optional.
  Colors are CSS variables in `:root` — retheme via tokens, not per-rule.

## Guardrails (don't break the site)
- **Never change the calculator math, formulas, element IDs, or the country-switch logic.**
  Make the smallest safe presentation/string change that achieves the goal.
- Math is verified against real bank examples — if you touch a calc, re-verify it.
- Do NOT refactor `index.html` into modules unless explicitly asked; it works and is fragile.
- Per-country profiles must stay intact (site is global; USD is the neutral default).

## Features already built (don't duplicate or break)
- **Generator** (`build.py` + `countries.json` + `templates/`) for the car/sip/fd clusters — see above.
- **Enriched content**: car/sip/fd country pages carry real local data (rates, lenders,
  deposit/tenure norms, fund houses, tax notes) + expanded FAQs. Keep that quality bar.
- **8 calculator hub pages** in `/pages/` with country-links blocks (hub-and-spoke linking).
- **hreflang clusters** (reciprocal, x-default = root/hub).
- **Lead capture**: `netlify/functions/lead_capture.js` via Resend. Needs env var
  **`RESEND_API_KEY`** in Netlify → Site settings → Environment variables.
- **IndexNow**: `.github/workflows/indexnow.yml` + `scripts/`.
- Favicons, `sitemap.xml` (add new pages here), `robots.txt`.

## SEO reality
Biggest levers are **backlinks** and a **real custom domain** (currently on `.netlify.app`).
Adding more thin pages does not help until existing pages index. **See `GROWTH_PLAN.md`**
for the prioritized plan (indexing → custom domain → backlinks).

---

## Note for AI agents (Cowork sandbox / mount reliability)
In the Cowork sandbox, the bash **mount can intermittently return truncated or stale reads**
of files in this repo (seen on `index.html`, `build.py`, and template files). To stay safe:
- When a mount read looks short, read authoritative content from git: `git show HEAD:<path>`.
- **Verify every write** by re-reading and confirming the file ends correctly (e.g. `</html>`).
  Never write a file you could not fully read first.
- Process large batches in **small chunks** — a single loop over ~300 files can time out and
  corrupt files mid-write. Prefer editing `countries.json` + templates and running `build.py`
  over sweeping edits across many `pages/*.html`.
- The host file tools (Read/Write/Edit) are authoritative; the bash mount is the flaky layer.
