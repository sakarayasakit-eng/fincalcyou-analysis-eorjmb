# fin·calc — CTO / SEO / Netlify Engineering Audit (2026)

**Scope:** live-domain migration to `fincalcyou.com`, SEO preservation, maintainability, and
revenue. **Method:** every finding below was verified against the actual repo and the live
Netlify project — not assumed. **Constraint respected:** no framework migration, no deleted
calculators, no reduced countries, no URL changes, static HTML preserved.

---

## 0. Executive summary — the one thing that matters right now

**🔴 P0 BLOCKER: the domain migration is only half done.** Netlify's primary domain is
correctly `https://fincalcyou.com`, but the **HTML still declares `fincalcyou.netlify.app`
as canonical everywhere**:

| Signal | State | Count (verified) |
|---|---|---|
| `<link rel=canonical>` → netlify.app | ❌ | 298/298 landing pages + 17 root pages |
| `og:url` / `twitter:url` → netlify.app | ❌ | every page |
| `hreflang` alternates → netlify.app | ❌ | 34 per cluster page |
| JSON-LD `@id`/`url` (Organization, WebSite, Breadcrumb) → netlify.app | ❌ | every page |
| `og:image` → netlify.app | ❌ | every page |
| `sitemap.xml` `<loc>` → netlify.app | ❌ | 315 URLs |
| `robots.txt` `Sitemap:` → netlify.app | ❌ | 1 |
| `generate_pages.py` `HOST` constant | ❌ | `https://fincalcyou.netlify.app` |

**Why this is urgent:** a canonical tag pointing at `netlify.app` tells Google *"the real
page is the subdomain."* Google will keep the subdomain as canonical and treat
`fincalcyou.com` as a duplicate — so you get the *worst* of both: the new domain doesn't
accumulate authority, and the migration's ranking-transfer never completes. **Until this is
fixed, every other SEO effort is wasted.** It is also low-difficulty (a uniform find-replace
+ one `build.py` run). This is Phase 1, item 1.

Everything else in this report is real but secondary to fixing the canonical host.

---

## TASK 1 — Netlify audit checklist

| Item | Status | Notes / action |
|---|---|---|
| Primary domain | ✅ | `fincalcyou.com` is primary (verified via API). |
| Domain alias (www) | ⚠ | Confirm `www.fincalcyou.com` is added as an alias and 301s to the apex (or vice-versa). Pick ONE canonical host and make the other redirect. |
| HTTPS | ✅ | Live on HTTPS; HSTS header present in `netlify.toml`. |
| SSL certificate | ⚠ | Auto-provisioned by Netlify; confirm the cert covers **both** apex and www in Domain settings. |
| Force HTTPS | ⚠ | HSTS is set, but verify the "Force HTTPS" toggle is ON in Netlify UI (redirects http→https). |
| netlify.app → .com redirect | ✅ | Automatic at host level once primary domain is set. Verify it returns **301** (not 302) with `curl -I https://fincalcyou.netlify.app`. |
| WWW vs non-WWW | ⚠ | Decide apex-canonical (recommended: `https://fincalcyou.com`). Canonical tags MUST match this exact host (see P0). |
| Canonical host (in HTML) | ❌ | **All pages canonical to netlify.app.** Fix in Phase 1. |
| Branch deploy settings | ⚠ | `main--fincalcyou.netlify.app` exists. Ensure deploy-previews/branch deploys are **noindex** (add `X-Robots-Tag: noindex` for the Deploy Preview context) so they don't become duplicate-content competitors. |
| Environment variables | ⚠ | Confirm `RESEND_API_KEY` is set (lead capture depends on it). Confirm **no** Anthropic/API key is committed (rotate if it ever was) — `.env*` should be git-ignored. |
| Build settings | ✅ | Static; no build command needed. `functions = "netlify/functions"` set. `build.py` runs **locally** and its output is committed — intentional, keep it that way. |
| Publish directory | ✅ | Repo root — correct for this static site. |
| Asset optimization | ⚠ | Optional. Netlify CSS/JS bundling could shave bytes but risks touching inline scripts; low priority, leave off for now. |
| Pretty URLs | ❌→keep OFF | Netlify "Pretty URLs" strips `.html`, which would **change every URL** and break the migration. Do **NOT** enable it. |
| Headers | ✅ | `netlify.toml` has strong security headers (XFO, nosniff, HSTS, Referrer-Policy, Permissions-Policy, CORP/COOP). |
| Redirects | ⚠ | Only one (`/pages/sip-calculator-india` → `-20-years`). Fine. Host redirect is automatic. |
| Cache behavior | ✅ | HTML `max-age=300`, CSS/JS `immutable, 1yr` — correct pattern for fast updates + cached assets. |
| Compression | ✅ | Netlify serves gzip/brotli automatically. |
| Forms | ✅ N/A | Netlify Forms not enabled; you use a Resend function instead. No action. |

---

## TASK 2 — Domain migration report

**Files still referencing `fincalcyou.netlify.app` (must be changed to `https://fincalcyou.com`):**

- `pages/*.html` — **298 files** (canonical, og:url, twitter:url, 34× hreflang, JSON-LD @id/url, og:image).
- Root `*.html` — **17 files** (same set).
- `sitemap.xml` — **315 `<loc>` URLs**.
- `robots.txt` — the `Sitemap:` line.
- `generate_pages.py` — `HOST` constant (line 4).
- `countries.json` — **0 references** ✅ (the host lives in the templates, not the data — good).

**The clean way to do it (leverages the generator, minimizes hand-edits):**
1. **Templates + generator (fixes 88 pages at once):** replace the host in `templates/car-loan.html`,
   `templates/sip.html`, `templates/fixed-deposit.html`, then run `python build.py`. Also set
   `HOST` in `generate_pages.py`.
2. **Hand-maintained pages (~210) + root (17) + sitemap + robots:** one uniform, reversible
   find-replace (the string is unique, so this is safe):
   ```
   grep -rl "fincalcyou.netlify.app" pages/ *.html sitemap.xml robots.txt \
     | xargs sed -i 's#fincalcyou\.netlify\.app#fincalcyou.com#g'
   ```
   (On Windows, do this in Git Bash, or let me/Claude Code run it on a clean checkout.)
3. **Verify zero remain:** `grep -rl "netlify.app" pages/ *.html sitemap.xml robots.txt` → empty.
4. **Idempotency:** `python build.py` then `git status` → generated pages must be clean.

**Migration-safe already (no change needed):** favicons and manifest icons use **root-relative**
paths (`/favicon.ico`, `/apple-touch-icon.png`) — host-independent ✅. There is **no RSS/feed**
and **no `site.webmanifest`** in the repo (see Task 5).

**Google best-practice checklist for the move:**
- ✅ 301 (host-level, automatic) — verify it's 301 not 302.
- ❌ Canonicals — fix per above (the critical piece).
- ❌ OG/Twitter/JSON-LD/sitemap/robots URLs — fix per above.
- ⚠ Keep the old `netlify.app` responding (redirecting) for months — do **not** unpublish it.
- ⚠ In GSC use the **Change of Address** tool (old property → new) after both are verified.

---

## TASK 3 — Search Console preparation

- **Ownership:** add `https://fincalcyou.com` as a **Domain property** (DNS TXT verification via
  your registrar/Netlify DNS) — this covers http/https + www/apex in one property. Keep the old
  `netlify.app` URL-prefix property verified so Change-of-Address works.
- **Sitemap:** after the host fix, submit `https://fincalcyou.com/sitemap.xml`. (It currently lists
  315 netlify.app URLs — do not submit until fixed.)
- **robots.txt:** fix the `Sitemap:` line to the .com host. Crawlers are already allowed (good).
- **Indexability:** confirm no stray `noindex`. (You previously noindexed a DEMO stub — that's
  correct; keep it.)
- **Canonical consistency:** every page's canonical must equal its live .com URL exactly (trailing
  slash, `.html`, case). The generator guarantees this for 88 pages once the host is fixed.
- **Redirect chains:** `_redirects` has one internal 301 — fine. Ensure no chains
  (netlify.app→.com→www→apex). Pick one host; make everything land in ≤1 hop.
- **Duplicate canonicals:** the split `home-loan-` / `mortgage-` naming is **not** a duplicate
  problem (different URLs, different content) — leave as-is; do not 301-merge (would drop rankings).
- **Soft 404s / orphans:** the guides directory + hub pages link everything; keep every page ≤3
  clicks from home. Spot-check GSC "Crawled – not indexed" after migration.
- **Actions, in order:** (1) fix host, (2) add domain property, (3) submit sitemap, (4) Change of
  Address, (5) request-index the 8 hubs + top 20 country pages (not all 298).

---

## TASK 4 — Bing / other engines

- **Bing Webmaster Tools:** add `fincalcyou.com`; **import from GSC** (one click) to carry over
  sitemap + settings. Bing powers DuckDuckGo, Yahoo, Ecosia, and Qwant — so Bing coverage handles
  all of those. Submit the sitemap.
- **IndexNow (already built):** you have `.github/workflows/indexnow.yml` + the public key file.
  **Update the host** in the IndexNow scripts/workflow to `fincalcyou.com` and confirm the key file
  is reachable at `https://fincalcyou.com/<key>.txt`. IndexNow feeds Bing/Yandex instantly.
- **Yandex Webmaster:** optional; add the domain + sitemap if you want RU/CIS coverage (you have
  Russia pages). IndexNow already pings Yandex.
- **Prereq for all of them:** the host fix (Task 2) must land first, or you'll submit subdomain URLs.

---

## TASK 5 — Technical SEO audit (prioritized)

**P0 (blocks everything):**
- Canonical/OG/hreflang/JSON-LD/sitemap host = netlify.app (see Task 2).

**P1 (high impact, do next):**
- **Sitemap host + freshness:** regenerate `sitemap.xml` with .com host; keep `<lastmod>` honest.
- **Calculator schema missing:** pages have Organization/WebSite/Breadcrumb/FAQPage ✅ but **no
  `SoftwareApplication`/`WebApplication`** schema on the calculators themselves (only the DSCR page
  had one). Adding it (name, applicationCategory: FinanceApplication, offers price 0) is a strong
  rich-result signal for tool pages. Add via the templates → regenerate.
- **Thin/near-duplicate content:** largely resolved — car/SIP/FD are enriched + single-sourced.
  Retirement/rent-vs-buy/home-loan are already differentiated. Keep the bar; don't add thin pages.

**P2 (worth doing):**
- **No `site.webmanifest`:** add a small manifest (name, theme-color `#0e7a4a`, icons) for PWA/mobile
  polish and a cleaner mobile-add-to-home experience. Reference it from the shared `<head>`.
- **DefinedTerm schema:** optional glossary schema for finance terms (EMI, DSCR, SIP) — modest AEO
  benefit; only if you add a glossary.
- **Image ALT / lazy-loading / CLS/LCP/INP:** the site is static, no framework, inline CSS — LCP/CLS
  are naturally good; verify with PageSpeed on 3 templates (home, a calculator, a country page).
  Add `loading="lazy"` to any below-the-fold images and explicit width/height to prevent CLS.
- **Unused JS/CSS / render-blocking:** the biggest lever is the **400 KB inline `index.html`** and
  the **calc math duplicated inline in 231 pages** (see Task 6/7). Extracting one cached engine.js
  cuts bytes and duplication. Google Fonts `<link>` is render-blocking — add `preconnect` (present)
  and consider `font-display: swap` (verify).
- **Broken links/assets:** run a crawl (Screaming Frog free ≤500 URLs, or `wget --spider`) after the
  host fix to catch any netlify.app links that 3xx unexpectedly.

**Priority order:** host fix → sitemap → calculator schema → manifest → PageSpeed pass → crawl for breaks.

---

## TASK 6 — Calculator architecture (design only, not implemented)

**What actually exists today (verified):**
- **11 embed types** across ~17 calculators: `emi` (93 pages), `sip` (41), `car` (39), `fd` (38),
  `convert` (22), `zakat` (15), `edu` (5), `rentbuy` (4), `retire` (4), `afford` (3), `gratuity` (3).
- **Math is duplicated inline in 231 pages** + `index.html`. There is **no shared engine** and **no
  project TypeScript file** (the only `.ts` are in `node_modules`). *Correction to the stated stack:
  the "TypeScript source-of-truth engine" is not present in the deployed repo — the engine is copy-
  pasted JS.*
- **Header/nav is inline in 297 pages.**
- **Generator exists for 3 clusters** (`build.py` + `countries.json` + `templates/`) — the proven
  pattern to generalize.

**Proposed layered architecture (evolution of what you have — no rewrite, no framework):**

```
 Finance Engine        engine.js — ONE file with every calc (emi, sip, fd, car, edu, retire,
   (single source)     rentbuy, zakat, convert, afford, gratuity). Authored in TS if you want,
        │              compiled to one immutable, cached engine.js the pages <script src>.
        ▼
 Country Registry      countries.json — all 34 countries × {currency, locale, default rate,
        │              banks, tax notes, ...}. Extend beyond car/sip/fd to every cluster.
        ▼
 Calculator Registry   calculators.json — 17 calculators × {type, engine fn, default inputs,
        │              schema template, title/desc/FAQ copy, related-links rule}.
        ▼
 Page Registry         derived = calculators × countries (+ custom overrides). Emits the slug
        │              list, hreflang sets, and the sitemap — one source, not 298 filenames.
        ▼
 Template Engine        templates/ + render_*/enrich_* in build.py (already real for 3 clusters).
        ▼
 Static Generator       build.py → writes /pages/*.html + sitemap.xml.
        ▼
 HTML Output            /pages/ (unchanged URLs, unchanged output — SEO-safe).
```

**Key point:** this is additive. Every layer already half-exists; the design just names them and
extends the registry/generator to all clusters, plus extracts the engine and the shared header into
single sources. Output HTML and URLs stay identical, so **zero SEO risk** when done via the
idempotency check.

---

## TASK 7 — Single-Source-of-Truth violations (prioritized by maintenance pain)

| # | Violation | Where | Impact | Fix |
|---|---|---|---|---|
| 1 | **Domain host string** duplicated | ~300 files | 🔴 Extreme — you're living it now (the migration) | Config constant / build var; fix now (Task 2). |
| 2 | **Calculator math** copy-pasted inline | 231 pages + index.html | 🔴 High — a formula fix = 232 edits, and they can drift | Extract one `engine.js`; pages `<script src>` it (cached, SEO-safe). |
| 3 | **Header / nav / footer** inline | 297 pages | 🔴 High — a nav change = 297 edits | Generate chrome from a partial via the template engine (build-time, not JS-rendered, to stay crawlable). |
| 4 | **Country data** (rates, banks, currency) hardcoded | home-loan/retirement/education/etc. pages | 🟠 Medium — yearly rate updates are manual | Move into `countries.json`; render via generator. |
| 5 | **Metadata / title-desc / OG patterns** | hand pages | 🟠 Medium | Registry-driven in the generator (done for 3 clusters). |
| 6 | **FAQ / schema / related-links** | hand pages | 🟠 Medium | Generator-driven (done for 3 clusters). |
| 7 | **Sitemap** hand-maintained vs generated | sitemap.xml + generate_pages.py | 🟡 Low | Single generator emits it from the page registry. |

**Do in this order:** #1 (now) → #2 (engine.js) → #3 (chrome) → #4 (country data) → extend generator to remaining clusters.

---

## TASK 8 — Business / revenue roadmap (think like the founder)

**Commercial-intent ranking (finance = high affiliate payouts):**
1. **Mortgage / home-loan** — highest search volume + highest affiliate value (brokers, rate-comparison). **Pillar product.**
2. **Car loan / auto finance** — strong intent, auto-finance affiliates. **Pillar.**
3. **DSCR** — already monetized via **lead capture** (Resend). Real-estate-investor leads are high-value. **Pillar / fastest revenue.**
4. **Fixed deposit / savings** — bank-account & high-yield-savings affiliates (esp. US/UK).
5. **Education loan** — study-abroad + student-loan-refi affiliates (pairs with expat SEO).
6. **Currency convert (22 pages)** — high traffic, lower intent → ad revenue, remittance affiliates (Wise etc.).

**Supporting (traffic/authority, monetize with ads not affiliates):** SIP, zakat, retirement, rent-vs-buy, gratuity, affordability.

**Revenue mechanisms, fastest → slowest:**
- **Now:** DSCR lead capture is built — confirm `RESEND_API_KEY` + add 1–2 DSCR lender partners to sell/route leads.
- **Weeks:** affiliate CTAs on the **results area** of mortgage/car/FD/education pages ("Check your rate with [partner]") targeting US/UK/CA/AU/AE (where finance affiliates pay). Put lead-capture forms on mortgage + car-loan + education (mirror the DSCR pattern).
- **After indexing/traffic:** display ads (Ezoic/Mediavine once you hit their thresholds) on high-traffic low-intent pages (convert, SIP, zakat).
- **Later:** sponsored placements / "featured lender."

**Placement rules:** affiliate widget appears **after** the user computes a result (intent peak),
never above the calculator; one primary CTA per page. Lead forms only on high-intent calculators.

---

## TASK 9 — Analytics & KPI dashboard

**Install (all free):** GA4 + Search Console (link them) + **Microsoft Clarity** (heatmaps/session
recordings). Add via the shared `<head>` (one snippet, generated into all pages).

**Events to track (GA4 custom events):**
- `calculator_start` (first input focus), `calculator_complete` (result rendered),
- `open_full_tool_click` (the deep-link you just shipped — measures embed→app flow),
- `country_switch`, `affiliate_click` (with partner + calculator), `lead_submit`,
- `outbound_click`, `return_visit`.

**KPI dashboard (Looker Studio, GSC + GA4):**
- **Acquisition:** indexed pages, impressions, clicks, CTR, avg position — by page & country.
- **Engagement:** calculator completion rate, deep-link CTR, pages/session, top countries.
- **Revenue:** affiliate CTR, lead conversion rate, **RPM (revenue per 1,000 sessions)**, revenue by calculator/country.
- **Retention:** return-visitor %, branded vs non-branded queries.

**North-star:** revenue per 1,000 organic sessions (RPM) — it forces both traffic *and* monetization.

---

## TASK 10 — Phased implementation plan

Each item: **Why · SEO impact · Business impact · Difficulty · Time · Risk · Files.**

### Phase 1 — CRITICAL (1–3 days)
1. **Fix canonical host everywhere → fincalcyou.com**
   - Why: canonicals point to the old subdomain; migration can't complete otherwise.
   - SEO: 🔴 Critical (unlocks all ranking transfer). Business: 🔴 Critical (all organic revenue).
   - Difficulty: Low. Time: 1–2 h. Risk: Low–Med (mass edit — mitigate: generator for 88, scripted
     find-replace for the rest, `git` safety, idempotency check).
   - Files: `templates/*.html` (3) → `build.py`; `pages/*.html` (210 hand), root `*.html` (17),
     `sitemap.xml`, `robots.txt`, `generate_pages.py`.
2. **Verify Netlify: Force HTTPS on, 301 (not 302) for netlify.app→.com, www alias + cert, branch deploys noindex.**
   - Why/SEO: correct redirect + one canonical host. Difficulty: Low. Time: 30 m. Risk: Low. Files: Netlify UI + `netlify.toml` (branch noindex header).
3. **Confirm `RESEND_API_KEY` set; confirm no secrets committed.**
   - Why: lead capture (revenue) + security. Difficulty: Low. Time: 15 m. Risk: Low.

### Phase 2 — HIGH (1–2 weeks)
4. **GSC + Bing + IndexNow on the new host** (domain property, submit sitemap, Change of Address, update IndexNow host).
   - SEO: 🔴 High (gets the fixed pages indexed). Business: High. Difficulty: Low. Time: 2–3 h. Risk: Low. Files: `robots.txt`, IndexNow workflow/scripts.
5. **Add `SoftwareApplication` schema + `site.webmanifest`; run a PageSpeed pass.**
   - SEO: Med–High (rich results for tools). Difficulty: Low–Med. Time: half-day. Risk: Low. Files: `templates/*` + regenerate; new `site.webmanifest`; shared `<head>`.
6. **Analytics: GA4 + Clarity + core events.**
   - Business: High (you can't optimize what you can't see). Difficulty: Low. Time: half-day. Risk: Low. Files: shared `<head>` (generated into all pages).
7. **First revenue: DSCR lead partners + affiliate CTA on mortgage/car/FD (US/UK).**
   - Business: 🔴 High (fastest cash). Difficulty: Med (partner signup). Time: 1 wk. Risk: Low. Files: high-intent page templates.

### Phase 3 — ARCHITECTURE (≈1 month)
8. **Extract `engine.js` (single math source) and generate the shared header/footer.**
   - Why: kills the 231×/297× duplication (SSOT #2, #3). SEO: neutral-positive (fewer bytes, no
     content change). Difficulty: Med–High. Time: 1–2 wk. Risk: Med (touches calc JS — do behind the
     idempotency check, verify every embed with `node --check` and a live spot-check). Files: new
     `engine.js`; `templates/*`; `build.py`; pages via regenerate.
9. **Extend the country registry + generator to the remaining thin-ish clusters where it helps** (not
   the already-differentiated ones). Difficulty: Med. Time: 1 wk. Risk: Low (proven pattern). Files:
   `countries.json`, `build.py`, `templates/`.

### Phase 4 — REVENUE (ongoing, starts after Phase 2)
10. Roll affiliate widgets + lead forms across all pillar calculators by geo; add display ads once
    traffic qualifies. Business: 🔴 High. Difficulty: Med. Risk: Low. Files: templates + generator.

### Phase 5 — SCALE
11. Add new calculators/countries via the registry (no new hand-HTML). Programmatic-SEO discipline:
    every new page must carry unique local data. Publish data-study content for backlinks
    (see `GROWTH_PLAN.md`). Business: compounding. Risk: Low if the SSOT rules are followed.

---

## Bottom line
The engineering is in good shape and the generator foundation is real. **One thing is on fire —
the canonical host still says `netlify.app` on 300+ files — and it is cheap to fix.** Do Phase 1
today; it's the difference between "we migrated" and "Google thinks we migrated." Everything after
that is about turning the (soon-to-be-indexing) traffic into revenue.
