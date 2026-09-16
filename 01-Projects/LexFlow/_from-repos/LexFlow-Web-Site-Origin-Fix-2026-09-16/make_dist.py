#!/usr/bin/env python3
"""Build a curated dist/ from a site tree: publish only what the site actually serves."""
import pathlib
import shutil
import sys

src = pathlib.Path(sys.argv[1]).resolve()
dist = pathlib.Path(sys.argv[2]).resolve()

ROOT_PAGES = {
    "404.html", "cookie-policy.html", "privacy.html", "terms.html",
    "lexflow-index.html", "lexflow-how-it-works.html", "lexflow-pricing.html",
    "lexflow-practice-areas.html", "lexflow-faq.html", "lexflow-blog.html",
    "lexflow-article-adoption-in-small-firm.html", "lexflow-article-ai-assisted-operations.html",
    "lexflow-article-client-communication.html", "lexflow-article-client-intake.html",
    "lexflow-article-crm-migration.html", "lexflow-article-law-firm-automation.html",
    "lexflow-article-law-firm-workflows.html", "lexflow-article-matter-tracker.html",
    "lexflow-article-security-privacy.html",
    "robots.txt", "sitemap.xml", "llms.txt", "site.webmanifest",
}
DIRS = ["assets", "it", "ru", ".well-known"]

dist.mkdir(parents=True, exist_ok=True)
n = 0
for name in sorted(ROOT_PAGES):
    p = src / name
    if p.is_file():
        shutil.copy2(p, dist / name)
        n += 1
for d in DIRS:
    s = src / d
    if s.is_dir():
        shutil.copytree(s, dist / d, dirs_exist_ok=True)
        n += sum(1 for _ in (dist / d).rglob("*") if _.is_file())

files = [p for p in dist.rglob("*") if p.is_file()]
bad = [str(p.relative_to(dist)) for p in files
       if "(1)" in p.name or p.suffix in {".py", ".csv", ".md", ".pyc"} or "__pycache__" in p.parts
       or p.name == ".DS_Store" or "templates" in p.parts or p.name.startswith("probe") or p.name.startswith("_")]
print(f"dist files: {len(files)}  (copied {n}, then recursion)")
print(f"files that must never be public, still present: {len(bad)}")
for b in bad:
    print("   ", b)