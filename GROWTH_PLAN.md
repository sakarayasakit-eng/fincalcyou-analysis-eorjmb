# fin·calc — Growth Plan (2026)

## Where things stand
- Static finance-calculator site on **fincalcyou.netlify.app** (a shared Netlify subdomain).
- ~298 pages. **88 are now single-sourced + enriched** (car-loan, SIP, fixed-deposit via `build.py`); the rest are hand-maintained and already country-differentiated (home-loan/mortgage, retirement, education, rent-vs-buy, zakat, DSCR).
- Already built: hreflang clusters, `sitemap.xml`, IndexNow automation, lead capture, and deep-link embeds that carry entered values into the full calculator.
- The core problem is **not "too few pages" — it's that pages aren't indexing**, and a subdomain caps authority.

The three levers below are in priority order. Do them in order; don't skip to #3.

---

## Lever 1 — Get indexed (highest priority, cheapest)
You already have content that Google isn't fully seeing. Fix the seeing before making more.

- **Google Search Console**: submit `sitemap.xml`; use URL Inspection → *Request Indexing* on the 8 hub pages and your best ~20 country pages. Don't request all 298 — depth over breadth.
- **Understand the coverage report**: "Crawled – currently not indexed" and "Discovered – not indexed" are quality/authority signals, not bugs. "Duplicate without user-selected canonical" is the thin-page signal — the enrichment work directly reduces this.
- **Why indexing was capped**: a low-authority subdomain with many near-identical pages gets a small crawl/quality budget. Making pages genuinely unique (done for the big clusters) is what earns more of that budget.
- **Internal linking**: keep every page ≤3 clicks from home (hub-and-spoke is good). Link your *best* pages from the homepage, not all of them.
- **Target**: get the hubs + top 20–30 pages indexed first. Prove the pattern, then widen.

## Lever 2 — Move to a custom domain (do this soon)
A real domain matters more than the exact name. Subdomains inherit less trust, look weaker for backlinks, and `.netlify.app` is shared.

Migrate cleanly so you don't lose the indexing you have:
1. Buy the domain (Netlify Domains or any registrar) and point DNS at Netlify.
2. Set it as the **primary** domain in Netlify; keep `.netlify.app` as a redirect.
3. Update every absolute URL: canonical, `og:url`, hreflang, `sitemap.xml`, JSON-LD `@id`/`url`, and the IndexNow host/key. **For the generated clusters this is one edit + `python build.py`** (fixes 88 pages at once); the hand-maintained pages need a find-replace of the host.
4. Netlify issues the 301 old→new at the host level.
5. Add the new property in GSC, resubmit the sitemap, and use the Change-of-Address tool.

**Timing matters:** every backlink you earn on the subdomain has to be migrated later. The fewer links you have now, the cheaper the move — so do it before a link-building push.

## Lever 3 — Backlinks (highest ceiling, slowest)
Calculator sites earn links through *utility*. Ranked by ROI:
- **Embeddable calculators** — package a copy-paste embed of your calculators for bloggers, real-estate agents, and personal-finance writers. Each embed is a link. Your embed markup already exists; wrap it as a shareable snippet.
- **A small data study** — publish one original piece from your own data (e.g. "car-loan rates across 30 countries, 2026"). Journalists and bloggers link to data.
- **Guest posts** on personal-finance, expat, and study-abroad blogs — your country pages fit expat and study-abroad audiences especially well (pair education-loan pages with study-abroad sites).
- **Tool roundups & niche directories** ("best free financial calculators").
- **Genuinely helpful answers** on Reddit/Quora/forums (a real answer + the relevant calculator, never spam).
- **HARO / journalist requests** for finance quotes; **reclaim unlinked mentions**.

A few quality links from relevant sites beat many low-quality ones.

---

## Content strategy (mostly done — hold the line)
- You've moved from thin duplicates to differentiated pages. **Keep that bar.** Every new page must carry genuine local data, or don't make it.
- Keep the 88 generated pages **current** — update rates yearly via `countries.json` + `build.py`. Stale "2026 rates" erode trust.
- Add depth to winners; don't add breadth of losers.

## Measurement (weekly)
- GSC: indexed count, impressions, top queries, coverage errors.
- Find pages earning impressions → double down on those topics/countries.
- Core Web Vitals: the static, no-framework build is fast — protect that.

## What NOT to do
- Don't mass-produce more country pages hoping volume helps — that's what capped indexing.
- Don't rename the site/repo for SEO — it doesn't matter.
- Don't buy links.

## First 30 days, in order
1. GSC: submit sitemap; request-index the hubs + top 20 pages.
2. Buy + migrate the custom domain (before earning more links).
3. Package the embeddable calculator; pitch 10 relevant sites.
4. Publish one data-study post; use it as link bait.
5. Refresh rates via `build.py` so nothing reads as stale.
