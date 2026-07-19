// Submits every URL in sitemap.xml to IndexNow (Bing, Yandex, Seznam, Naver).
// Google does not support IndexNow; this does not affect Google indexing.
const fs = require("fs");
const path = require("path");
const https = require("https");

const SITEMAP_PATH = path.join(__dirname, "..", "sitemap.xml");
const HOST = "fincalcyou.com";
const KEY = "7094e86a5ce8fe76b528041a968212c9";
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

const xml = fs.readFileSync(SITEMAP_PATH, "utf8");
const urlList = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map((m) => m[1]);

if (urlList.length === 0) {
  console.error("No URLs found in sitemap.xml");
  process.exit(1);
}

// Safety: only submit URLs that belong to the verified domain. Guards against a
// stale/wrong host in the sitemap leaking foreign URLs into an IndexNow submission
// (IndexNow rejects/ignores a payload whose URLs don't match `host`, and submitting
// URLs you don't own can get the key throttled).
const VERIFIED_DOMAIN = HOST; // fincalcyou.com — set to your actual verified domain
const submitUrls = urlList.filter((url) => {
  try {
    const hostname = new URL(url).hostname;
    return hostname === VERIFIED_DOMAIN || hostname === `www.${VERIFIED_DOMAIN}`;
  } catch (e) {
    return false; // skip malformed URLs
  }
});

if (submitUrls.length === 0) {
  console.error(`No valid URLs found for the verified domain (${VERIFIED_DOMAIN})`);
  process.exit(1);
}
if (submitUrls.length !== urlList.length) {
  console.warn(
    `Skipped ${urlList.length - submitUrls.length} URL(s) not on ${VERIFIED_DOMAIN}`
  );
}

const payload = JSON.stringify({
  host: HOST,
  key: KEY,
  keyLocation: KEY_LOCATION,
  urlList: submitUrls,
});

const req = https.request(
  "https://api.indexnow.org/indexnow",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Content-Length": Buffer.byteLength(payload),
    },
  },
  (res) => {
    let body = "";
    res.on("data", (chunk) => (body += chunk));
    res.on("end", () => {
      console.log(`IndexNow response: ${res.statusCode}`);
      if (body) console.log(body);
      if (res.statusCode >= 200 && res.statusCode < 300) {
        console.log(`Submitted ${submitUrls.length} URLs.`);
      } else {
        process.exitCode = 1;
      }
    });
  }
);

req.on("error", (err) => {
  console.error("IndexNow submission failed:", err.message);
  process.exit(1);
});

req.write(payload);
req.end();
