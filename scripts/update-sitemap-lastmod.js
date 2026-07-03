// Stamps each sitemap.xml entry with a <lastmod> date pulled from git history,
// so Google's crawler can tell which pages actually changed since its last visit.
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const REPO_ROOT = path.join(__dirname, "..");
const SITEMAP_PATH = path.join(REPO_ROOT, "sitemap.xml");
const HOST = "https://fincalcyou.netlify.app";

function localPathForUrl(url) {
  const rel = url.replace(HOST, "").replace(/^\//, "");
  return rel === "" ? "index.html" : rel;
}

function lastCommitDate(relPath) {
  const filePath = path.join(REPO_ROOT, relPath);
  if (!fs.existsSync(filePath)) return null;
  try {
    const out = execSync(`git log -1 --format=%cd --date=short -- "${relPath}"`, {
      cwd: REPO_ROOT,
    })
      .toString()
      .trim();
    return out || null;
  } catch {
    return null;
  }
}

let xml = fs.readFileSync(SITEMAP_PATH, "utf8");
const today = new Date().toISOString().slice(0, 10);

xml = xml.replace(/<url>(.*?)<\/url>/gs, (block, inner) => {
  const locMatch = inner.match(/<loc>(.*?)<\/loc>/);
  if (!locMatch) return block;
  const url = locMatch[1];
  const relPath = localPathForUrl(url);
  const date = lastCommitDate(relPath) || today;

  let newInner = inner.replace(/<lastmod>.*?<\/lastmod>/, "");
  newInner = newInner.replace(/<\/loc>/, `</loc><lastmod>${date}</lastmod>`);
  return `<url>${newInner}</url>`;
});

fs.writeFileSync(SITEMAP_PATH, xml);
console.log("sitemap.xml lastmod dates updated.");
