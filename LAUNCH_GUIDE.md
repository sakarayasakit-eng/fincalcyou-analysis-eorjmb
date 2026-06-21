# fin·calc Complete Launch Guide
## From ZIP file to earning money — step by step

**Your situation:** You have the ZIP file on your Android phone. You want to launch a website and start earning. This guide covers every single step, in plain language, with real costs and honest timelines.

**Total cost to launch:** $10–12 (domain only)
**Time to go live:** 30 minutes
**Time to first earnings:** 4–8 weeks (after AdSense approval)

---

## PHASE 1: GET A DOMAIN NAME (Day 1 — 15 minutes)

### What is a domain name?
It's your website address. Like `google.com` or `bankrate.com`. You need to buy one.

### What name to choose
For a finance calculator, good options:
- `fincalc.app` — clean, descriptive, global
- `calcloan.com` — clear
- `moneycalcs.com` — approachable
- `loancalculator.app` — direct SEO value

**Avoid:** EMI in the name (India-centric). Pick something global.
**Tip:** Check availability before deciding.

### Where to buy — RECOMMENDED: Porkbun
Go to **porkbun.com** on your phone browser.

**Why Porkbun:**
- .com costs ~$11/year — same price every year, no first-year trap
- Free WHOIS privacy (protects your personal info)
- No hidden fees, no upsells
- Trusted by millions of developers

**Alternatives if Porkbun unavailable:**
- **Namecheap.com** — similar pricing, slightly more upsells
- **Cloudflare.com/products/registrar** — cheapest at $10.46/yr but requires Cloudflare nameservers

**DO NOT use:** GoDaddy (stripped consumer protections Feb 2026), Google Domains (sold to Squarespace, overpriced)

### Steps on Porkbun:
1. Open porkbun.com on your phone
2. Type your desired name in the search box
3. If .com is available and affordable — buy it
4. Create a free account (use any email)
5. Enter payment (debit/credit card or PayPal)
6. Complete purchase. You now own the domain for 1 year.
7. **Do not buy hosting from Porkbun** — you don't need it (hosting is free on Netlify)

**Cost: $10–12/year**

---

## PHASE 2: DEPLOY THE WEBSITE FREE (Day 1 — 10 minutes)

### Why Netlify (free hosting)
Netlify is a professional hosting service used by millions of developers. Their free plan is completely free — no credit card, no time limit, no catch. You can drag and drop your project folder and it's live in seconds.

fin·calc is a static HTML file — perfect for Netlify's free tier.

### What Netlify free plan gives you:
- Unlimited bandwidth for a static site like fin·calc
- Free HTTPS (SSL certificate) — required for AdSense
- Global CDN — loads fast in every country
- Custom domain support (so `fincalc.app` instead of `xyz.netlify.app`)
- Instant redeploy when you upload a new version

### Steps to deploy:

**Step 1: Create a Netlify account**
1. Open **netlify.com** on your phone
2. Click "Sign up"
3. Sign up with your email (or Google account)
4. Confirm your email

**Step 2: Deploy your site**
1. Log into Netlify dashboard
2. Click **"Add new site"**
3. Select **"Deploy manually"** (not GitHub — you don't have code on GitHub)
4. You'll see a box that says "Drag and drop your site folder here"
5. Extract your `fincalc_v19.zip` file on your phone (use your file manager, hold-press the zip → Extract)
6. Upload the entire `fincalc` folder to Netlify

**On Android, how to upload:**
- After extracting, go back to Netlify in your browser
- Click "browse to upload" instead of drag-drop
- Select the extracted `fincalc` folder
- Wait ~30 seconds
- Your site is now live at a URL like `random-name-12345.netlify.app`

**Step 3: Connect your custom domain**
1. In Netlify dashboard, go to your site → "Domain settings"
2. Click "Add custom domain"
3. Type your domain (e.g., `fincalc.app`)
4. Netlify will give you nameserver addresses (like `dns1.p07.nsone.net`)
5. Go back to Porkbun → your domain → "Authoritative Nameservers"
6. Replace Porkbun's nameservers with Netlify's nameservers
7. Save. DNS propagates in 5–60 minutes.

**Step 4: Enable HTTPS**
1. In Netlify → Site settings → Domain management
2. Scroll to "HTTPS"
3. Click "Verify DNS configuration"
4. Click "Provision certificate"
5. Free SSL certificate activated. Your site now loads as `https://` — required for AdSense.

**Your site is now live. Anyone in the world can visit it.**

---

## PHASE 3: ESSENTIAL PAGES BEFORE ADSENSE (Day 1–2)

### What you MUST have before applying for AdSense:
AdSense reviewers check for these. Missing any = rejection.

fin·calc already has `privacy.html`. You need to add or update:

**1. Privacy Policy** (`privacy.html`) — ✅ Already exists in your ZIP
Update it to include:
- Your domain name (replace `example.com` everywhere in the file)
- A line about Google AdSense: *"This site uses Google AdSense to show advertisements. Google uses cookies to show relevant ads based on your browsing. To opt out: https://www.google.com/settings/ads"*

**2. About page** (create `about.html`)
Simple paragraph about the site. Example:
> "fin·calc is a free finance calculator covering 34 countries. Built to give everyone access to accurate loan, investment, and savings calculations with real bank rate data — no signup, no tracking, no cost."

**3. Contact page** (create `contact.html` or just add email to footer)
Just an email address. Use any public email. Even Gmail is fine.

**4. Terms of Service** (create `terms.html`) — optional but helps
One page saying: calculations are for reference only, not financial advice.

### Update your domain in the HTML:
Open `index.html` in any text editor (Notepad, Codepen, any app that can edit text files). Search for `example.com` and replace with your actual domain. Same for `sitemap.xml` and all pages in `/pages/`.

**How to edit on Android:**
- Use a free app called **"QuickEdit Text Editor"** or **"Acode"** from Play Store
- Open any HTML file from your phone storage
- Find/replace `example.com` with your domain
- Save

---

## PHASE 4: APPLY FOR GOOGLE ADSENSE (Day 3–4)

### Before applying, checklist:
- [ ] Website is live at your custom domain (not netlify.app subdomain)
- [ ] HTTPS is working (padlock icon in browser)
- [ ] Privacy policy page exists
- [ ] About page exists
- [ ] Contact info visible
- [ ] Site loads on mobile without errors
- [ ] Content is original (fin·calc is — all calculator text is original)

### Steps to apply:

1. Go to **adsense.google.com** on your phone
2. Click "Get started"
3. Enter your website URL
4. Enter your Gmail address
5. Choose your country (your real country — this affects payment method)
6. Accept Terms of Service
7. Google will ask you to add a code snippet to your `<head>` section
   - Copy the code snippet
   - Open `index.html` in Acode/QuickEdit
   - Paste the snippet just before `</head>`
   - Save and redeploy to Netlify
8. Click "I've placed the code"
9. Google reviews your site: **typically 1–14 days** (sometimes 3–4 weeks for new domains)

### What can cause rejection (avoid these):
- Site not live yet / still on netlify.app subdomain
- Privacy policy missing or copied word-for-word without customization
- No About page
- Calculator works but has zero text content (fin·calc has the FAQ section now — good)
- Site loads but has JS errors visible to Google's crawler

### After approval:
1. Go to AdSense → Ads → Ad units
2. Create ad units matching the 3 ad slot positions already in fin·calc:
   - `adSlotTop` — use "Display ad" 728×90 or responsive
   - `adSlotEmiMid` — use "Display ad" responsive
   - `adSlotFooter` — use "Display ad" responsive
3. Open `index.html`, find the 3 `<!-- AD SLOT -->` comment blocks
4. Inside each `.ad-slot` div, paste the AdSense code (uncomment + fill your `pub-XXXXXXXX` and `data-ad-slot` values)
5. Redeploy to Netlify

**Your site is now earning money.**

---

## PHASE 5: FIRST 30 DAYS — GETTING TRAFFIC

### The honest truth
A website with no traffic earns nothing. You need visitors. Here's how to get them without paying for ads:

### Free traffic sources (ranked by effort vs. payoff)

**1. Google Search Console (Day 1 — free, takes 5 minutes)**
- Go to **search.google.com/search-console**
- Add your domain
- Submit your sitemap: enter `https://yourdomain.com/sitemap.xml`
- This tells Google your site exists and to start indexing it
- **Do this on Day 1** — the clock starts when you submit

**2. Share in relevant WhatsApp / Telegram groups (Day 1 — instant traffic)**
If you're in any finance, business, or professional groups:
> "I made a free loan/EMI calculator that works for 34 countries — here's the link: [your domain]. No signup, no ads yet, just tell me if it works for your country."
- This gets you first real users AND their feedback
- Pakistan / India / Gulf finance groups especially

**3. Answer questions on Reddit / Quora (Week 1–2)**
People ask "How do I calculate my home loan EMI?" / "What's my monthly mortgage payment?" / "Is my bank rate competitive?" constantly on:
- reddit.com/r/personalfinance
- reddit.com/r/india (for INR users)
- reddit.com/r/pakistan
- Quora finance sections

Give a real helpful answer. Mention the calculator as a tool. Don't spam — one good answer per week is enough.

**4. Post on social media (Week 1)**
LinkedIn especially — finance professionals are there.
> "Built a free calculator covering 34 countries with real bank rate data. What makes it different: it tells you if your offered loan rate is competitive vs market. [link]"

**5. Submit to product hunt, tool directories (Week 2)**
- producthunt.com — "launch" your product (free)
- alternativeto.net — add as alternative to Bankrate, Groww, NerdWallet
- toolsforhuman.com, theresanaiforthat.com — many tool directories accept submissions

---

## PHASE 6: LONG-TERM GROWTH (Month 2–12)

### What generates sustainable organic traffic

**Write one article per week** (most important single thing you can do)

The landing pages we built (US mortgage, UK mortgage, Canada, Australia) are ~500 words each. That's thin for AdSense dwell time and Google ranking. Target: 1,200–1,500 words per page.

Topics that work well for fin·calc:
- "How to calculate your home loan EMI in Pakistan (with real SBP rates)"
- "Is my home loan rate too high? How to find out"
- "Mortgage calculator Canada: semi-annual compounding explained"
- "UAE car loan: 5-year vs 7-year — which is cheaper?"
- "Zakat calculation 2026: complete guide with nisab threshold"
- "Debt avalanche vs snowball — which saves more money?"

**Each article should:**
1. Answer a real question in the first paragraph (AEO best practice)
2. Include the calculator embedded or linked prominently
3. Have a specific country or topic focus (not "global EMI calculator")
4. Link to 2–3 related calculators on the site

### Content calendar example (8 weeks)
| Week | Article | Target keyword |
|------|---------|----------------|
| 1 | Pakistan home loan rates 2026 | "home loan calculator Pakistan" |
| 2 | Canada mortgage semi-annual compounding | "mortgage calculator Canada" |
| 3 | UAE car loan rules | "car loan calculator UAE" |
| 4 | India vs Pakistan EMI comparison | "EMI calculator India Pakistan" |
| 5 | Zakat 2026 guide | "zakat calculator 2026" |
| 6 | Debt avalanche method | "which loan to pay first" |
| 7 | Australia home loan offset account | "home loan calculator Australia" |
| 8 | Financial Health Check guide | "financial health score" |

---

## FULL COST BREAKDOWN

| Item | Cost | When |
|------|------|------|
| Domain name (.com) | $11/year (~₹920/yr) | Day 1 |
| Netlify hosting | **FREE** | Always free |
| SSL certificate | **FREE** (via Netlify) | Always free |
| Google AdSense | **FREE** | After approval |
| Ezoic (upgrade) | **FREE** (takes 30% of ad revenue) | After 10k sessions |
| Mediavine Journey | **FREE** (takes 30% of ad revenue) | After 1k sessions |

**Total hard cost: $11/year = less than $1/month**

---

## REALISTIC EARNING TIMELINE

| Month | Expected traffic | Earning (AdSense) |
|-------|-----------------|-------------------|
| 1 | 0–500 sessions | $0–3 |
| 2 | 500–2,000 sessions | $3–15 |
| 3 | 2,000–5,000 sessions | $15–40 |
| 6 | 5,000–20,000 sessions | $40–200 |
| 12 | 20,000–50,000+ sessions | $200–800+ |

**With Ezoic (upgrade after ~3 months):** 2-3× these numbers.
**With affiliate buttons added:** 3-5× these numbers.

---

## UPGRADE PATH (simple version)

```
Day 1:      Buy domain ($11) + Deploy to Netlify (free)
Day 2-3:    Add pages, submit to Search Console
Day 4:      Apply for AdSense
Week 2:     AdSense approved → add ad codes → earning starts
Month 3:    Switch from AdSense to Ezoic (at 5-10k sessions)
Month 6:    Add "compare rates" affiliate button
Month 12:   Apply for Mediavine (at 50k sessions)
Year 2:     Apply for Raptive / hire freelancer for content
```

---

## TOP 5 MISTAKES TO AVOID

1. **Applying for AdSense before the site has proper pages.** You need About, Privacy Policy, Contact, real content. Don't rush the application.

2. **Using your Netlify subdomain instead of custom domain.** AdSense will often reject `.netlify.app` domains. Use your bought domain.

3. **Clicking your own ads.** Google bans publishers who do this. Even clicking once to "test" is a violation. Open the site in incognito/private browsing to see how it looks — never click the ad.

4. **Buying traffic.** "Social traffic" packages from Fiverr ($5 for 10,000 visitors) — Google filters this out AND it can get your AdSense account banned. Only organic or your own social sharing.

5. **Changing nothing for months.** Google rewards sites that update regularly. Add one page or article per week minimum. The sitemap already links to 11 landing pages — just keep going.

---

## QUICK START CHECKLIST (cut this out)

**Today:**
- [ ] Buy domain from Porkbun ($11)
- [ ] Create free Netlify account
- [ ] Extract ZIP → upload `fincalc` folder to Netlify
- [ ] Connect custom domain to Netlify
- [ ] Open `index.html` → replace all `example.com` with your domain → redeploy

**Tomorrow:**
- [ ] Submit site to Google Search Console
- [ ] Update privacy.html with your domain + AdSense mention
- [ ] Create simple about.html
- [ ] Add contact email to footer
- [ ] Share link in 2-3 WhatsApp/Telegram groups you're in

**This week:**
- [ ] Apply for Google AdSense
- [ ] Write first real article for one landing page
- [ ] Answer 2-3 questions on Quora/Reddit about loan calculations

**After AdSense approval:**
- [ ] Create 3 ad units in AdSense dashboard
- [ ] Paste ad codes into index.html ad slot divs
- [ ] Redeploy
- [ ] Watch your first cents arrive 🎉
EOF
echo "Guide ready"