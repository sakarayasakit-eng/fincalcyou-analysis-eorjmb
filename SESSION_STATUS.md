# fin·calc — Session Status & Handoff (as of 2026-08-06)

Read this first in any new session, alongside `CLAUDE.md` (working rules) and
`INDEXING_PLAYBOOK.md` (off-site plan). Repo = `fincalcyou` (the ONE source of truth
+ Netlify deploy target). Live site: https://fincalcyou.com.

---

## ✅ DONE & SHIPPED (2026-08-06 session — verified live)

**Security / privacy**
- **Public-file exposure closed.** Netlify was serving the whole repo root, so internal docs
  (`SESSION_MEMORY.md`, `CTO_AUDIT_2026.md`, `STRATEGIC_ADVISORY.md`, …), `build.py`,
  `countries.json`, scripts, `node_modules/`, `templates/` were all publicly fetchable.
  Fixed via `_redirects`: **force-301 (`301!`) block** on those paths → homepage. (Note:
  Netlify **ignores force on `404`** for existing files — `301!` is what works.) Verified live:
  `build.py`, `countries.json`, the `.md` docs now 301 to `/`. Added a branded `404.html`.
- `node_modules/` added to `.gitignore` (run `git rm -r --cached node_modules` to untrack).

**Content correctness**
- **India purge completed** (leftovers the prior pass missed): `about.html` (country list + SBI/
  HDFC/ICICI + anecdote), Zakat page `INR` nisab row + "zakat india" keyword, homepage `HDFC`
  mention, `/pages/` Zakat `INR`, the India related-links in all 3 `templates/*.html`, and the
  dead `sip-calculator-1-crore` custom stub in `countries.json`. Verified: 0 India refs in
  shipped files (Japanese "SBI Securities" + Pakistani "Lakh" are legit, left in place).
- **Counts corrected 34/340 → 33/330** across 30 pages (titles, meta, OG/Twitter, hero, about,
  hubs, schema) + "34 economies" + homepage "290+"→"250+". Confirmed exactly **33 country
  profiles** in `index.html`.
- **DSCR scoped to US** (it's a US-only product): `/pages/` directory cards set
  `data-country="us"`; homepage "Explore" link gated in `applyCountryProfile()` (shows only when
  `currentCur.code==='USD'`, mirrors the existing Islamic-tab toggle — no switch-logic/math change).

**New backlink assets (live)**
- **Data study:** `pages/where-home-loans-are-cheapest-2026.html` — 33-country home/car loan
  rate ranking (Japan 1.5% → Türkiye 44%, 29× gap), CSS bar charts, Article+Breadcrumb schema.
  In sitemap + linked from `central-bank-rates-2026.html` and the `/pages/` directory.
- **Embeddable widget:** `embed.js` (root) + `pages/embed.html` landing page with copy-paste
  script-embed snippets (EMI/car/SIP/FD), each carrying a "by fin·calc" backlink. No iframe (so
  no `X-Frame-Options` change needed). Math copied verbatim from the existing inline widget.
  In sitemap + directory.

**Indexing (GSC)**
- Domain property verified; `sitemap.xml` **Success, 274 discovered**. **38 indexed / 312 not**
  (300 "Discovered – not indexed" = authority/crawl-budget signal → fixed by backlinks, not by
  more requests). Hubs + `mortgage-calculator-usa` already indexed. **Request-indexed:** homepage
  + the new data study.

---

## 📋 PENDING — YOUR ACTIONS (nothing here needs code)
1. **Push any uncommitted local work**, then verify: `git add -A && git commit -m "…" &&
   git pull --rebase origin main && git push`.
2. **Send 3 outreach emails** — finished + personalized in `outputs/emails-to-send.md`
   (calculators.org, The Calculator Site, Patrik Shore). Paste into Gmail, Send. (I cannot send/
   forward mail — no tool available does; the Gmail connector only *drafts*, and it's currently
   read-only. Grant it "compose & manage drafts" if you want me to create drafts.)
3. **GSC:** request-index `pages/embed.html` (Inspect URL → Test Live URL → Request Indexing).
4. **Bing:** sign in at bing.com/webmasters (usman.aa12024) so backlinks can be read; optionally
   finish the ~62-URL manual submission (ask me to regenerate the list).
5. **DSCR revenue — decision needed.** The Resend function `netlify/functions/lead_capture.js`
   is fine, but **NO page has a lead form** wired to it — lead capture currently captures nothing.
   Decide: wire an opt-in form on the DSCR page(s)? Also confirm `RESEND_API_KEY` in Netlify env
   and line up a DSCR lender partner. (User asked to HOLD wiring the form for now.)

## 🔜 OPTIONAL / NOT STARTED
- **GEO "Key facts" callout** — compact extractable summary near the top of each calculator page
  for AI answer engines. Wire via generator (templates + `build.py`) for 87 cluster pages, then
  the 8 hubs. Open question: visible styled callout (recommended) vs SR-only.
- More backlink outreach (target list in `outputs/backlink-target-list.md`); embed on partner
  sites; guest posts; directory listings.
- Weekly GSC monitoring (indexed count, impressions, top queries).

---

## 🛑 HARD RULES (carried from the audit mandate — do not violate)
- Never migrate the framework, never delete calculators, never reduce countries, never replace
  static HTML, preserve all URLs + rankings. Never sacrifice SEO for engineering elegance.
- **Generator discipline:** to change car/sip/fd country pages, edit `countries.json` +
  `templates/*.html` / `build.py`, then run `python build.py`. NEVER hand-edit generated
  `pages/{car-loan,sip,fixed-deposit}-*.html`. Idempotency check: `python build.py && git status`
  must be clean. (Hubs + home-loan/dscr/education/zakat/retirement/rent-vs-buy are hand-maintained.)
- **Env reliability:** bash mount truncates/goes stale on large files — host Read/Edit/Write are
  authoritative; use `git show HEAD:<path>` for truth; verify every write ends with `</html>`.
- **Git:** always `git pull --rebase origin main` before push (a plain merge once reverted India work).
- **Security headers:** keep `X-Frame-Options: DENY` global; the `_redirects` `301!` block hides
  internal files — don't remove it.
