#!/usr/bin/env python3
"""Inventory what a naive `deploy the repo root` would publish that should not be public."""
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
tracked = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True).stdout.split()
untracked = [l[3:] for l in subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True).stdout.splitlines() if l.startswith("??")]

KEEP_TOP = {"assets/", "it/", "ru/", ".well-known/"}
KEEP_ROOT_FILES = {
    "404.html", "cookie-policy.html", "llms.txt", "privacy.html", "robots.txt",
    "site.webmanifest", "sitemap.xml", "terms.html",
    "lexflow-index.html", "lexflow-how-it-works.html", "lexflow-pricing.html",
    "lexflow-practice-areas.html", "lexflow-faq.html", "lexflow-blog.html",
    "lexflow-article-adoption-in-small-firm.html", "lexflow-article-ai-assisted-operations.html",
    "lexflow-article-client-communication.html", "lexflow-article-client-intake.html",
    "lexflow-article-crm-migration.html", "lexflow-article-law-firm-automation.html",
    "lexflow-article-law-firm-workflows.html", "lexflow-article-matter-tracker.html",
    "lexflow-article-security-privacy.html",
}

def should_not_publish(p):
    if any(p.startswith(k) for k in KEEP_TOP):
        return False
    if "/" in p:  # anything not under a keep-top dir
        return True
    return p not in KEEP_ROOT_FILES

bad = sorted(p for p in tracked if should_not_publish(p))
print(f"TRACKED files: {len(tracked)}   UNTRACKED: {len(untracked)}")
print(f"\nTRACKED files a root-deploy would serve but must NOT be public ({len(bad)}):")
for p in bad:
    print("   ", p)
print(f"\nUNTRACKED files a working-dir deploy would serve ({len(untracked)}):")
for p in untracked:
    print("   ", p)

dupes = [p for p in tracked if "(1)" in p]
print(f"\nDUPLICATE-CONTENT pages (filename contains '(1)') : {len(dupes)}")
for p in dupes:
    print("   ", p)
pre = [p for p in tracked if p.startswith("templates/") and p.endswith(".html")]
print(f"\ntemplates/ HTML copies (crawlable duplicates of live pages): {len(pre)}")
for p in pre:
    print("   ", p)