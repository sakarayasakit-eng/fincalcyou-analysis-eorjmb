# fin·calc v21 — Netlify launch steps

## What you have ready (✓)

- ✓ Main app: `index.html` (fully functional)
- ✓ Privacy policy: `privacy.html` (with AdSense notice)
- ✓ About page: `about.html` (explains fin·calc)
- ✓ Contact page: `contact.html` (email contact)
- ✓ Landing pages: 11 pages in `/pages/` folder (USA, UK, Canada, Australia mortgages + SIP, Zakat, etc.)
- ✓ Security headers: `netlify.toml` (configured)
- ✓ Sitemap: `sitemap.xml` (for SEO)
- ✓ Robots: `robots.txt` (allows all crawlers)
- ✓ llms.txt: for AI crawlers (ChatGPT, Claude, Perplexity)

**Everything is ready to deploy. No further changes needed before launch.**

---

## Step 1: Buy a domain (15 minutes)

1. Go to **porkbun.com** on your phone or computer
2. Search for a domain name:
   - `fincalc.app` (if available — clean, global)
   - `loancalculator.app`
   - `moneycalcs.com`
   - Pick whatever feels right
3. If available and under $15/year, buy it
4. Create a free account or log in
5. Complete payment (card or PayPal both work)
6. You now own the domain for 1 year

**Cost: ~$11 USD**

---

## Step 2: Create Netlify account (5 minutes)

1. Go to **netlify.com**
2. Click "Sign up"
3. Sign up with your email (or GitHub / Google account if you prefer)
4. Verify your email

---

## Step 3: Deploy to Netlify (10 minutes)

### Option A: Drag and drop (easiest)

1. Log into Netlify
2. Go to your dashboard
3. You'll see a box that says "Drag and drop your site folder here"
4. On your computer, open your file manager and navigate to the `fincalc` folder
5. Drag the entire `fincalc` folder onto Netlify
6. Wait ~30 seconds
7. Netlify assigns you a temporary URL like `random-name-12345.netlify.app`
8. Your site is live (but on a temporary URL)

### Option B: Git-based (if you know GitHub)

1. Push your `fincalc` folder to GitHub
2. Connect your GitHub account to Netlify
3. Select the repo
4. Netlify auto-deploys on every push

**For this guide, Option A is easiest.**

---

## Step 4: Connect your custom domain (5 minutes)

1. In Netlify, go to your site dashboard
2. Click "Domain settings" (or "Site settings" → "Domain management")
3. Click "Add custom domain"
4. Type your domain (e.g., `fincalc.app`)
5. Netlify will ask to verify you own the domain
6. Netlify gives you 4 nameserver addresses (they look like `dns1.p07.nsone.net`)
7. Go back to Porkbun
8. Log in, find your domain
9. Go to "Authoritative Nameservers" (or similar)
10. Replace Porkbun's default nameservers with the 4 Netlify ones
11. Save

**DNS propagation takes 5 minutes to 24 hours. Usually 15-30 minutes.**

After propagation, your site lives at `https://fincalc.app` (or whatever you bought).

---

## Step 5: Enable HTTPS (automatic)

Netlify automatically creates a free SSL certificate when you connect your domain. Your site will load as `https://...` with a green padlock. Nothing to do here.

---

## Step 6: Submit to Google Search Console (10 minutes)

This is critical. Do this on the same day you launch.

1. Go to **search.google.com/search-console**
2. Click "URL prefix" property
3. Enter your domain: `https://fincalc.app`
4. Google will ask you to verify ownership
5. Netlify verification is easiest: add a DNS record
   - Netlify shows you a TXT record to add
   - Go back to Porkbun, add the TXT record
   - Google verifies
6. Once verified, Google shows you:
   - Coverage (pages indexed)
   - Errors (broken links, crawl issues)
   - Sitemaps (submit `sitemap.xml`)
7. Upload your sitemap: click "Sitemaps" → add `https://fincalc.app/sitemap.xml`

---

## Step 7: Apply for Google AdSense (5 minutes to apply)

1. Go to **adsense.google.com**
2. Click "Get started"
3. Enter your website URL
4. Enter your email
5. Choose your country
6. Accept Terms of Service
7. Google will email you a verification code
8. Paste it into a meta tag in your `index.html` (Netlify will walk you through this)
9. Click "I've placed the code"
10. Google reviews your site: **1–14 days** (sometimes longer for new domains)

**What Google checks:**
- Is the site live and accessible? ✓
- Does it have a privacy policy? ✓
- Does it have an about/contact page? ✓
- Is the content original? ✓
- Are there ads-friendly content policies violations? ✓ (none)

Your site should pass easily.

---

## After AdSense approval (5 minutes)

1. Go to AdSense → Ads → Ad units
2. Create 3 display ad units (for the 3 slots in your HTML)
3. Copy each ad code
4. Open `index.html` in a text editor
5. Find the 3 empty `<div>` tags with comments `<!-- AD SLOT -->`
6. Paste your ad codes there
7. Upload updated HTML to Netlify
8. Ads appear on your site

---

## The timeline

| Day | Action | Time |
|-----|--------|------|
| 1 | Buy domain + deploy to Netlify | 30 min |
| 1 | Connect domain | 5 min (wait for DNS propagation) |
| 1 | Submit to Search Console | 10 min |
| 1 | Apply for AdSense | 5 min |
| 2–14 | Wait for AdSense approval | — |
| 14+ | Add ad codes to your HTML | 5 min |

**Total hands-on time: ~1 hour. Real-world time: 2–14 days (for AdSense approval).**

---

## After launch (optional, but recommended)

1. **Share the link** in 2–3 WhatsApp groups or finance forums you're in
2. **Answer 3 finance questions on Quora or Reddit per week,** mention fin·calc when relevant
3. **Check Google Search Console daily** for the first week (see if Google crawls your site, how many impressions you get)
4. **Watch AdSense revenue** (after approval) — even $1 in the first week is meaningful signal

---

## Troubleshooting

**Domain not working after connecting?**
- DNS takes 5 min to 24 hours. Wait 30 min, then restart your browser / clear cache. If still broken after 24h, check that Porkbun nameservers actually got updated.

**AdSense rejects the site?**
- Common reasons: too little original content (add the landing page articles), or policy violation (fin·calc has none). Re-apply after making changes.

**Site loads but calculators broken?**
- Check browser console (F12 → Console tab). If you see errors, contact support@fincalc.app with a screenshot.

---

## You're ready to launch

Everything is prepared. No further development needed before going live. Deploy today and let the site prove itself with real users.

Good luck. 🚀
