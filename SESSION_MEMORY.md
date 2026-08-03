# fin·calc — FULL SESSION MEMORY (complete handoff)

Everything from this working session, preserved so a new Cowork session resumes with zero loss.
Read together with `SESSION_STATUS.md` (short status), `CLAUDE.md` (rules), `INDEXING_PLAYBOOK.md`
(off-site plan), `GROWTH_PLAN.md`, and `CTO_AUDIT_2026.md`.

---

## 0. PROJECT IN ONE PARAGRAPH
Static finance-calculator site (vanilla HTML/CSS/JS, no framework, no build step) on Netlify,
live at **https://fincalcyou.com**. GitHub: `sakarayasakit-eng/fincalcyou-analysis-eorjmb`, deploy
on push to `main`. The interactive app is one hand-maintained file `index.html` (~414KB, inline
CSS+JS). ~274 SEO landing pages in `/pages/` share `pages/landing.css`. The car-loan/SIP/fixed-
deposit country pages are **generated** (see §3). Theme: NerdWallet-style light (white bg, green
`#0e7a4a`). Owner: Sheryar (sakarayasakit@gmail.com).

## 1. FOLDER RULE (critical)
- WORK ONLY IN: `C:\Users\HP\Downloads\fincalc_v21_READY_FOR_NETLIFY_101\fincalcyou`
  (bash mount: `/sessions/<id>/mnt/fincalcyou/`). This is the ONE source of truth AND deploy target.
- The sibling `...\fincalc` folder is DEPRECATED/STALE — never read, copy, or work there.
- NEVER use `robocopy` or folder-to-folder sync (caused divergence + near data loss).

## 2. HARD RULES (audit mandate — never violate)
Never migrate the framework · never delete calculators · never reduce countries · never replace
static HTML · preserve all URLs · preserve all rankings · never sacrifice SEO for engineering
elegance · always inspect the codebase before concluding, never assume · make the smallest safe
presentation/string change · never change calculator math, element IDs, or country-switch logic
(math is verified against real bank examples — re-verify if touched) · don't refactor `index.html`.

## 3. THE GENERATOR (how cluster pages are single-sourced)
- **`countries.json`** — data registry. Top-level keys: `car_loan`, `sip`, `fixed_deposit`; each a
  list of per-country entries (country, currency, locale, rate, local note, related links…).
  Entries with `"custom": true` are hand-written and SKIPPED by the generator.
- **`templates/`** — one skeleton per cluster: `car-loan.html`, `sip.html`, `fixed-deposit.html`.
  A template is NOT a generated page — never overwrite a template with an enriched page.
- **`build.py`** — reads json+templates, computes money figures with Node `Intl.NumberFormat`
  (same formatter as the live calculator, so static hint numbers match the live tool), writes
  `/pages/`. Functions: `render`/`enrich` (car), `render_sip`/`enrich_sip`, `render_fd`/`enrich_fd`;
  `NODE` JS block does car/sip/fd math (matches live page JS exactly);
  `CLUSTERS=[("car_loan",render,"car"),("sip",render_sip,"SIP"),("fixed_deposit",render_fd,"FD")]`.
  Env var `FINCALC_OUT` can redirect output.
- **GOLDEN RULE:** to change a generated page, edit `countries.json` or `templates/*.html` /
  `build.py`, then `python build.py`. NEVER hand-edit `pages/{car-loan,sip,fixed-deposit}-*.html`.
- **Idempotency check after any generator change:** `python build.py && git status` → tree CLEAN.
- Counts after India removal: car_loan 33, sip ~34→33, fixed_deposit 33 (was car_loan 34 originally).
- **HAND-MAINTAINED (edit page directly, NOT via generator):** home-loan/mortgage, retirement,
  education-loan, rent-vs-buy, zakat, DSCR, the 8 hub pages, and every `"custom": true` variant.
- **Deep-link embeds:** every standard embed's script updates the "Open the full tool →" link with
  the visitor's entered amount/rate/years so it opens the homepage calculator pre-filled. Marker to
  preserve: `_nl=el.querySelector('.fc-note a')`. Lives in embed `<script>` AND in `templates/`.

## 4. WORK COMPLETED THIS SESSION (all committed & pushed unless noted in §6)
### 4a. Generator + enrichment
- Proved byte-parity generator on car-loan, adopted + enriched car/SIP/FD clusters.
- Enriched country pages carry real local data (rates, lenders, deposit/tenure norms, fund houses,
  tax notes) + expanded FAQs. Deep-link embeds completed across clusters.
### 4b. Canonical host migration (Task 2, CRITICAL — custom domain went live)
- Migrated netlify.app → `fincalcyou.com` everywhere (0 netlify.app remaining). Updated
  `scripts/submit-indexnow.js` HOST, `scripts/update-sitemap-lastmod.js` HOST, `generate_pages.py`
  HOST (line 4), robots.txt Sitemap line, canonicals.
### 4c. India removal (user: "hide india from whole project" → "Everything (full purge)")
Reason = personal/legal/brand (remove regardless of SEO). Removed from:
- `index.html`: `COUNTRY_PROFILES.INR` block (now starts `PKR:`), `BANKS.INR`, `REGION_CUR`
  (`{IN:'INR',…}`→`{PK:'PKR',`), currencies array INR entry, timezones
  (`'Asia/Kolkata':'INR','Asia/Calcutta':'INR'`), quick-convert INR buttons, popular list INR,
  SOUTH_ASIA_CODES INR, FALLBACK_RATES INR, INR default-inputs, India tax note (80C/NPS/ELSS),
  meta/FAQ/JSON-LD India mentions, worked-example labels neutralized. Hardened default:
  `if (!initialCode || !currencies.some(c => c.code === initialCode)) initialCode = 'USD';`
- `countries.json`: India entries removed from all 3 clusters + all `related` arrays (87 links).
- ~43 pages removed (incl. lakh/crore/salary/INR-converter/glossary/guide mentions found via
  content scan, not just filename inventory). `_redirects`: 46 rules, India pages 301 → cluster hubs.
- Content copy scrubbed on `how-to-calculate-emi`, `what-is-sip`, `central-bank-rates-2026`
  (removed India/RBI/₹). `llms.txt`, `sitemap.xml`, hreflang all India-free.
- VERIFIED LIVE via incognito/web_fetch: hero "United States", no INR, "Pakistan" in FAQ lists.
### 4d. Structured data / SEO/GEO
- Added `SoftwareApplication` JSON-LD to all **87 cluster pages** via generator (swap subs in each
  `render*` function keyed on the SoftwareApplication name/url; block also in each `templates/*.html`
  before `</head>`). Block shape: `{"@type":"SoftwareApplication","name":"…","url":".../pages/….html",
  "applicationCategory":"FinanceApplication","applicationSubCategory":"Calculator","operatingSystem":
  "Any (web-based)","browserRequirements":"Requires JavaScript","offers":{"@type":"Offer","price":"0",
  "priceCurrency":"USD"},"isAccessibleForFree":true,"publisher":{"@id":"https://fincalcyou.com/#organization"}}`.
- Homepage has `WebApplication`; also present: FAQPage (245 pages), Organization/WebSite/
  SearchAction/BreadcrumbList (@graph, `@id` `https://fincalcyou.com/#organization`), DefinedTerm.
- **Removed fake `aggregateRating`** (was 4.8 / 2400 / bestRating 5) — Google policy / manual-action
  risk. Updated "34 countries/340 banks" → "33/330" in the WebApplication schema (body marketing
  badges still say 34/340 — branding decision still OPEN, user hasn't decided).
- Fixed currency **mojibake** (NBSP U+00A0 double-encoded as `Â `) via Node-Intl regeneration.
- `llms.txt` rewritten: 33 countries, India removed (dropped HDFC/ICICI/SBI; added Bankrate/Chase/
  HSBC/Barclays/Maybank/Scotiabank), date → July 2026, contact → `https://fincalcyou.com/contact`.
- GEO: robots.txt allows GPTBot/ClaudeBot/PerplexityBot/Google-Extended/OAI-SearchBot/CCBot.
- `sitemap.xml`: regenerated clean = **274 URLs** (fixed 296→0 backslash bug, India removed, valid
  `</urlset>`).
- Bing/IndexNow: `scripts/submit-indexnow.js` HOST=`fincalcyou.com` + user-requested verified-domain
  filter: `const VERIFIED_DOMAIN=HOST; submitUrls=urlList.filter(url=>{try{const h=new URL(url).hostname;
  return h===VERIFIED_DOMAIN||h===\`www.${VERIFIED_DOMAIN}\`;}catch(e){return false;}}); if(!submitUrls.length){console.error(...);process.exit(1);}`
  payload uses `urlList: submitUrls`.
- Added `SoftwareApplication` to the **8 hub pages** (home-loan, car-loan, sip, fixed-deposit,
  education-loan, zakat, retirement, rent-vs-buy) — all 8 valid JSON, end with `</html>`. **NOT yet
  committed** (see §6).
### 4e. Docs created
`CLAUDE.md` (generator discipline + rules), `GROWTH_PLAN.md` (indexing → custom domain → backlinks),
`CTO_AUDIT_2026.md` (full 10-task audit), `INDEXING_PLAYBOOK.md` (off-site execution),
`SESSION_STATUS.md` (short status), this `SESSION_MEMORY.md`.

## 5. BING SUBMISSION PROGRESS (manual, Bing Webmaster Tools "Submit URLs")
Submitting all 263 non-priority sitemap URLs in batches of 50, ordered mortgage/home-loan → car →
FD → SIP → rest, India-free, pulled fresh from `sitemap.xml` each time.
- Already submitted: priority ~20 (in `INDEXING_PLAYBOOK.md`) + batches covering sitemap URLs 1–200.
- **~200 of 263 submitted. 62 URLs REMAIN** (final localized bank/converter/guide/DSCR-city tail).
- To resume: ask "give me the last 62 Bing URLs" — regenerate with this pipeline:
  `grep -oP '(?<=<loc>)[^<]+' sitemap.xml` minus the priority list, ordered as above, `sed -n '201,$p'`.

## 6. UNCOMMITTED — DO FIRST in the new session
On disk but NOT committed: (1) the 8-hub `SoftwareApplication` schema, (2) `INDEXING_PLAYBOOK.md`,
`SESSION_STATUS.md`, `SESSION_MEMORY.md`.
```
git add -A
git commit -m "SEO: SoftwareApplication on 8 hubs + indexing playbook + session memory"
git pull --rebase origin main   # REBASE, never plain merge (see §8)
git push
```

## 7. STILL TO DO (priority order)
1. Commit the uncommitted work (§6).
2. Finish Bing — submit the final 62 URLs.
3. **GSC (biggest lever):** add Domain property for fincalcyou.com, submit `sitemap.xml`, request-
   index the ~20 priority URLs (spread ~10–15/day). See `INDEXING_PLAYBOOK.md` Part 1. Change-of-
   Address only if the old netlify.app property was verified.
4. **GEO TL;DR build (item 2, NOT STARTED):** add a compact extractable "Key facts" callout near
   the top of each calculator page (what the tool does, coverage, free/no-signup, formula in one
   line) for AI answer engines. Plan: wire through generator (templates + `build.py`) for the 87
   cluster pages, then add to the 8 hubs directly; keep idempotent. OPEN QUESTION asked, not yet
   answered: **visible styled callout (recommended) vs SR-only.**
5. Backlinks/revenue: embed landing page ("embed this calculator, free" + attribution link) → pitch
   10 sites; one original data study (e.g. "car-loan/mortgage rates across 33 countries 2026") →
   pitch journalists; guest posts (expat/study-abroad/remittance); tool roundups/directories;
   helpful Reddit/Quora answers. DSCR lead capture already built — confirm `RESEND_API_KEY` in
   Netlify env; add 1–2 DSCR lender partners; add affiliate CTAs to results area of US/UK/CA/AU
   high-intent pages. Later: display ads (Ezoic/Mediavine). North-star metric: RPM (revenue per
   1,000 organic sessions). See `GROWTH_PLAN.md` + `INDEXING_PLAYBOOK.md` Parts 2–3.

## 8. ENVIRONMENT GOTCHAS & LESSONS (important)
- **Bash mount truncates large-file reads/writes** intermittently (seen on index.html, build.py,
  templates, sitemap). Host Read/Edit/Write tools are AUTHORITATIVE; bash mount is the flaky layer.
  Read truth from git: `git show HEAD:<path>`. Verify every write ends with `</html>`. Never write a
  file you couldn't fully read. Process big batches in small chunks (a single loop over ~300 files
  can time out and corrupt mid-write — this corrupted 28 SIP pages once; restored from git HEAD).
- **Heredoc quoting:** don't nest `cat >…<<"EOF"` inside `bash -c '…'` when the body contains
  `<script`/`</head>` — bash mis-parsed `<script` as a redirect ("bash: script: No such file").
  FIX that worked: run python directly with a quoted heredoc: `python3 << 'PYEOF' … PYEOF`
  (no `cat`, no nested `bash -c`). In `re.sub`, use lambda replacements (literal `\u`/backslashes in
  replacement strings raise bad-escape).
- **`rm` "Operation not permitted"** → call `mcp__cowork__allow_cowork_file_delete` first.
- **GIT MERGE DISASTER (never repeat):** user ran plain `git pull` (merge) → opened Vim (stuck in
  INSERT) → an aborted rebase landed on a pre-India commit → the merge REVERTED all India removal and
  got pushed (India back live). Recovery: exit Vim (`Esc`,`:wq`,Enter), find good state via reflog
  (`19080e2e`), `git reset --hard 19080e2e` + `git push --force origin main` (--force-with-lease was
  rejected "stale info"). LESSON: **always `git pull --rebase origin main`, never plain `git pull`.**
- User feedback "still showing same effect" (twice) was caused by un-pushed commits / the reverting
  merge / Netlify HTML cache (~5 min) + `localStorage('fincalc_cur')` — verify in INCOGNITO with a
  cache-buster `?v=NN`.

## 9. USER PREFERENCES & STYLE
- Be concise and direct; minimal formatting/verbosity. Works task-by-task, pushes to git himself
  after each batch, confirms with short messages ("pushed", "next", "give more"). Acts as the
  business owner directing CTO/SEO/full-stack work. Chose: full purge of India; SoftwareApplication
  schema; off-site playbook before GEO build.
