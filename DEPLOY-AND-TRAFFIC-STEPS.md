# fin·calc — Deploy the fixes & drive traffic

## ✅ What I already fixed in your source files
- **Canonical bug** — replaced `https://example.com` → `https://fincalcyou.netlify.app` in `index.html` and **all 12 landing pages** in `/pages/`. This was telling Google your whole site was a copy of example.com.
- **sitemap.xml** — all 14 URLs now use your real domain.
- **robots.txt** — `Sitemap:` line now points to your real domain.
- **Breadcrumb structured data** in index.html — fixed to your domain.
- **Social share tags** — added `og:url`, `og:image`, `twitter:image` to index.html.
- **og-image.png** — created a 1200×630 share image (in the site root).

## ⚠️ One thing you must do — the contact email
`index.html` and `privacy.html` still say `hello@example.com`. Tell me the email you want public and I'll set it, or edit those two `mailto:hello@example.com` links yourself.

---

## STEP 1 — Redeploy to Netlify (makes the fixes live)
Your folder isn't connected to Git, so use drag-and-drop:
1. Go to https://app.netlify.com and open the **fincalcyou** project.
2. Click the **Deploys** tab.
3. Drag the **`fincalc`** folder (the one containing index.html) onto the "drag and drop your site folder here" area.
4. Wait ~30 seconds for "Published".
5. Verify: open `https://fincalcyou.netlify.app/robots.txt` and `https://fincalcyou.netlify.app/sitemap.xml` — both should show your real domain. View page source on the homepage and confirm the canonical reads `fincalcyou.netlify.app`.

---

## STEP 2 — Google Search Console (free search traffic starts here)
1. Go to https://search.google.com/search-console and sign in.
2. Click **Add property** → choose **URL prefix** → enter `https://fincalcyou.netlify.app/`.
3. Verify ownership — easiest method: **HTML tag**. Copy the `<meta name="google-site-verification" ...>` tag it gives you, send it to me and I'll paste it into your `<head>`, then you redeploy and click Verify. (Or use any other method it offers.)
4. Once verified: left menu → **Sitemaps** → enter `sitemap.xml` → **Submit**.
5. Left menu → **URL Inspection** → paste your homepage URL → **Request indexing**. Repeat for your top landing pages (UK, USA, Pakistan, Zakat).

## STEP 3 — Bing Webmaster Tools (covers Bing + DuckDuckGo)
1. Go to https://www.bing.com/webmasters and sign in.
2. Click **Import from Google Search Console** (one click, copies everything) — or **Add site manually** and submit `sitemap.xml` the same way.

---

## STEP 4 — Free directory listings (do 2–3 per day)
For each, create a free account and submit. Use this text:

**Name:** fin·calc
**Tagline:** Free finance calculators for 34 countries — no signup, no tracking
**URL:** https://fincalcyou.netlify.app
**Category:** Finance / Productivity
**Description (paste):**
> fin·calc is a free set of finance calculators that knows your country's real central-bank rate. Mortgage/EMI, car loan, SIP, fixed deposit, Zakat, retirement, debt payoff, rent-vs-buy and a live currency converter — 34 countries, 171 named banks. Everything runs in your browser: no signup, no tracking, works offline after first load.

Submit to these (in priority order):
1. AlternativeTo — https://alternativeto.net (add as free alternative to paid finance apps)
2. SaaSHub — https://www.saashub.com
3. Toolify — https://www.toolify.ai
4. Uneed — https://www.uneed.best
5. Fazier — https://fazier.com
6. Startup Stash — https://startupstash.com
7. SaaS Worthy — https://www.saasworthy.com
8. G2 — https://www.g2.com (free product listing)
9. Capterra — https://www.capterra.com (free product listing)

(Full channel list + Reddit/Quora/community tactics are in your `fincalc-free-promotion-playbook.md`.)

---

## STEP 5 — Product Hunt
Everything is prepared in `fincalc-producthunt-launch-pack.md` — every form field, the maker's first comment, the gallery shot list, and launch-day timing. Launch Tue–Thu at 12:01 AM PST.

---

### Why I can't click these for you
The Claude-in-Chrome browser tool that would let me fill these forms is macOS-only right now, and your Windows machine can't install the extension. So Steps 2–4 need your clicks — but the exact fields and copy above make each one a 2-minute job. For the Search Console verification tag, just paste it to me and I'll wire it into your code.
