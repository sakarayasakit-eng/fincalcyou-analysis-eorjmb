# fin·calc — Off-Site Indexing & Backlink Playbook

The on-page/technical foundation is done (migration, canonicals, clean sitemap, hreflang,
SoftwareApplication + FAQ schema, `llms.txt`). From here, **traffic comes from getting indexed
and earning links** — this is the execution checklist for that.

---

## PART 1 — INDEXING (do this week)

### 1. Google Search Console
1. **Add a Domain property** for `fincalcyou.com` (not URL-prefix). GSC → Add property → Domain →
   add the TXT record to your DNS. A Domain property covers http/https + apex + www in one.
2. **Submit the sitemap**: GSC → Sitemaps → `sitemap.xml`. (It's now clean — 274 URLs, no India,
   no backslash bug, all `fincalcyou.com`.)
3. **Change of Address** — only if you had verified the old `fincalcyou.netlify.app` property:
   old property → Settings → Change of Address → `fincalcyou.com`. If you never verified the
   subdomain, skip it (the 301 + canonicals already do the job).
4. **Request indexing** for the priority set below (URL Inspection → Request Indexing). GSC caps
   this ~10–15/day, so spread over 2 days. **Do NOT bulk-request all pages** — depth first.

**Priority URLs (request-index these first):**
```
https://fincalcyou.com/
https://fincalcyou.com/pages/
https://fincalcyou.com/pages/home-loan-calculator
https://fincalcyou.com/pages/car-loan-calculator
https://fincalcyou.com/pages/sip-calculator
https://fincalcyou.com/pages/fixed-deposit-calculator
https://fincalcyou.com/pages/education-loan-calculator
https://fincalcyou.com/pages/retirement-calculator
https://fincalcyou.com/pages/zakat-calculator
https://fincalcyou.com/pages/rent-vs-buy-calculator
https://fincalcyou.com/dscr-calculator
```
Then the highest commercial-intent country pages (US/UK/Gulf/AU/CA monetize best):
```
https://fincalcyou.com/pages/mortgage-calculator-usa.html
https://fincalcyou.com/pages/mortgage-calculator-uk.html
https://fincalcyou.com/pages/mortgage-calculator-canada.html
https://fincalcyou.com/pages/car-loan-calculator-usa.html
https://fincalcyou.com/pages/car-loan-calculator-uae.html
https://fincalcyou.com/pages/car-finance-calculator-uk.html
https://fincalcyou.com/pages/fixed-deposit-calculator-usa.html
https://fincalcyou.com/pages/home-loan-calculator-australia.html
https://fincalcyou.com/pages/home-loan-calculator-singapore.html
https://fincalcyou.com/pages/sip-calculator-usa.html
```

### 2. Bing Webmaster Tools
- Add `fincalcyou.com` → **Import from GSC** (one click; carries sitemap + verification).
- Bing powers **DuckDuckGo, Yahoo, Ecosia, Qwant** — no separate submission needed for those.
- Submit `sitemap.xml`.

### 3. IndexNow (already wired)
- Your GitHub Action + key file are set (host fixed to `fincalcyou.com`). Confirm the key file
  resolves: open `https://fincalcyou.com/7094e86a5ce8fe76b528041a968212c9.txt`. IndexNow pings
  Bing/Yandex instantly on each deploy.

### 4. Monitor (weekly, first 4 weeks)
GSC → **Pages** report. What each status means:
- *Crawled – currently not indexed* / *Discovered – not indexed* → authority/quality signal
  (fixed by the custom domain — done — and by backlinks in Part 2, not by more pages).
- *Duplicate, Google chose different canonical* → should now be ~0 (canonicals fixed).
- *Soft 404* → flag me the URLs; usually a thin page.
Track: **indexed count**, impressions, top queries, avg position.

---

## PART 2 — BACKLINKS (the real authority lever; start after indexing is submitted)

Calculator sites earn links through **utility**. Ranked by ROI:

### A. Embeddable calculators (highest ROI — you already have the embed markup)
- Package a copy-paste `<iframe>`/snippet of each calculator with a small "Powered by fin·calc"
  attribution link. Pitch to: personal-finance bloggers, mortgage brokers, real-estate agents,
  study-abroad consultants, expat forums. **Each embed = a backlink.**
- First move: build one clean embed landing page ("Embed this calculator on your site — free"),
  then email 10 relevant site owners.

### B. One original data study (link bait)
- Publish a single data-driven post from your own numbers, e.g. **"Car-loan / mortgage rates
  across 33 countries, 2026"** or **"Where in the world is a home loan cheapest?"**. Journalists
  and bloggers link to data + charts. Add a simple chart and a "methodology" note (you already
  have an editorial-policy + methodology page — cite them for E-E-A-T).

### C. Guest posts (targeted)
- Your country pages fit **expat, study-abroad, and remittance** audiences. Pitch guest posts to
  those blogs; link the relevant country calculator (e.g. education-loan pages ↔ study-abroad sites,
  Gulf mortgage pages ↔ expat-in-UAE sites).

### D. Tool roundups & niche directories
- Get listed in "best free financial calculators" roundups and finance-tool directories.
  Search `"best mortgage calculator" + "list"` / `"free financial calculators"` and request inclusion.

### E. Genuinely helpful answers + reclaim mentions
- Answer real questions on Reddit (r/personalfinance, country-specific finance subs), Quora, and
  finance forums with the specific calculator link — value first, never spam.
- Reclaim any unlinked brand mentions.

**Quality > quantity:** a few links from relevant finance/expat sites beat many low-quality ones.

---

## PART 3 — REVENUE (runs in parallel; see GROWTH_PLAN.md)
- **Fastest cash:** DSCR lead capture is already built (confirm `RESEND_API_KEY` in Netlify; add
  1–2 DSCR lender partners). Add lead forms / affiliate CTAs to the **results area** of
  mortgage/car/FD pages in US/UK/CA/AU (where finance affiliates pay).
- **Later:** display ads (Ezoic/Mediavine) once traffic qualifies, on high-traffic low-intent
  pages (currency converters, SIP, zakat).

---

## 30-DAY CADENCE
- **Week 1:** GSC domain property + sitemap; request-index the ~20 priority URLs; Bing import;
  verify IndexNow key file.
- **Week 2:** Build the embed page; pitch 10 sites. Confirm DSCR lead capture works.
- **Week 3:** Publish the data-study post; pitch it to 5 finance blogs/journalists.
- **Week 4:** Review GSC (indexed count, top queries); double down on whichever pages earn
  impressions; add affiliate CTAs to the top-performing high-intent pages.

## North-star metric
**Revenue per 1,000 organic sessions (RPM)** — forces both traffic and monetization. Track it monthly.
