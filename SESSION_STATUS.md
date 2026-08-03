# fin·calc — Session Status & Handoff (as of 2026-07-31)

Read this first in any new session, alongside `CLAUDE.md` (working rules) and
`INDEXING_PLAYBOOK.md` (off-site plan). Repo = `fincalcyou` (the ONE source of truth
+ Netlify deploy target). Live site: https://fincalcyou.com.

---

## ✅ DONE THIS SESSION (committed & pushed, verified live)
- **Canonical host migration** netlify.app → `fincalcyou.com` across all pages (0 netlify.app left).
- **India fully removed** from the whole project (app logic in `index.html`, all cluster data in
  `countries.json`, ~43 pages, glossary/guides/converter mentions, sitemap, hreflang, `llms.txt`).
  Redirects added in `_redirects` (India URLs 301 → cluster hubs). Verified live: India gone.
- **Structured data / SEO:**
  - `SoftwareApplication` JSON-LD on all **87 cluster pages** (via generator) + homepage `WebApplication`.
  - Removed fake `aggregateRating` (Google policy risk).
  - Fixed currency mojibake (`Â ` NBSP) via Node-Intl regeneration.
  - `llms.txt` cleaned (33 countries, India removed, date fixed).
  - `sitemap.xml` clean = 274 URLs, no India, no backslash bug.
  - Bing/IndexNow: host fixed to fincalcyou.com; verified-domain URL filter added to
    `scripts/submit-indexnow.js`.
- **Docs created:** `CLAUDE.md`, `GROWTH_PLAN.md`, `CTO_AUDIT_2026.md`, `INDEXING_PLAYBOOK.md`.

## ⚠️ UNCOMMITTED — COMMIT THIS FIRST in the new session
Two changes are on disk but NOT yet committed/pushed:
1. `SoftwareApplication` JSON-LD added to the **8 hub pages** (home-loan, car-loan, sip,
   fixed-deposit, education-loan, zakat, retirement, rent-vs-buy) — inserted before `</head>`,
   all verified valid JSON + end with `</html>`.
2. `INDEXING_PLAYBOOK.md` (+ this `SESSION_STATUS.md`).

Commit command (use REBASE, never plain `git pull` — a plain merge once reverted the India work):
```
git add -A
git commit -m "SEO: SoftwareApplication on 8 hubs + indexing playbook + session status"
git pull --rebase origin main
git push
```

---

## 🔎 BING SUBMISSION PROGRESS (manual, in Bing Webmaster Tools)
Submitting all 263 non-priority sitemap URLs in batches of 50. **~200 of 263 submitted.**
**62 URLs remain** (final batch: remaining localized bank/converter/guide pages).
→ In a new session, ask me for "the last 62 Bing URLs" and I'll pull them fresh from `sitemap.xml`,
   ordered and India-free. (The priority ~20 + 4 batches of 50 are already submitted.)

## 📋 STILL TO DO (priority order)
1. **Commit the uncommitted hub schema + docs** (above).
2. **Finish Bing** — submit the final 62 URLs.
3. **GSC (biggest lever)** — add Domain property for fincalcyou.com, submit `sitemap.xml`,
   request-index the ~20 priority URLs. See `INDEXING_PLAYBOOK.md` Part 1.
4. **GEO TL;DR build (item 2, NOT started)** — add a compact, extractable "Key facts" callout
   near the top of each calculator page (what the tool does, coverage, free/no-signup, formula
   in one line) so AI answer engines can cite it. Plan: wire through the generator (templates +
   `build.py`) for the 87 cluster pages, then add to the 8 hubs directly. Open question I asked:
   **visible styled callout (recommended) vs SR-only** — user hadn't answered yet.
5. **Backlinks / revenue** — embed landing page, one data study, DSCR lead capture (confirm
   `RESEND_API_KEY` in Netlify). See `INDEXING_PLAYBOOK.md` Parts 2–3 + `GROWTH_PLAN.md`.

---

## 🛑 HARD RULES (carried from the audit mandate — do not violate)
- Never migrate the framework, never delete calculators, never reduce countries, never replace
  static HTML, preserve all URLs + rankings. Never sacrifice SEO for engineering elegance.
- **Generator discipline:** to change car/sip/fd country pages, edit `countries.json` +
  `templates/*.html` / `build.py`, then run `python build.py`. NEVER hand-edit generated
  `pages/{car-loan,sip,fixed-deposit}-*.html`. Idempotency check: `python build.py && git status`
  must be clean. (Hubs + home-loan/dscr/education/zakat/retirement/rent-vs-buy are hand-maintained.)
- **Env reliability:** bash mount truncates large-file reads/writes — host Read/Edit/Write are
  authoritative; use `git show HEAD:<path>` for truth; verify every write ends with `</html>`.
- **Git:** always `git pull --rebase origin main` before push (plain merge once reverted India work).
