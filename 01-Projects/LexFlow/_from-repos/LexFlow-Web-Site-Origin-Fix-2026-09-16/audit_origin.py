#!/usr/bin/env python3
"""Audit the LexFlow web-site tree for origin/canonical/AEO defects.

Usage: python3 audit_origin.py <site-root> [placeholder-origin]
Prints a precise inventory: which pages carry the placeholder origin in each
field, which pages have a canonical that does not point at themselves, which
have duplicate canonicals, and which pages have no canonical at all.
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
PLACEHOLDER = sys.argv[2] if len(sys.argv) > 2 else "lexflow.example.com"

pages = sorted(list(root.glob("*.html")) + list(root.glob("it/*.html")) + list(root.glob("ru/*.html")))

CANON = re.compile(r'<link rel="canonical" href="([^"]*)"')
OGURL = re.compile(r'<meta property="og:url" content="([^"]*)"')
JDURL = re.compile(r'"url":\s*"([^"]*)"')

ph_canon, ph_og, ph_jd, no_canon, multi_canon, selfmiss = [], [], [], [], [], []

for p in pages:
    t = p.read_text(encoding="utf-8", errors="replace")
    rel = str(p.relative_to(root))
    canons = CANON.findall(t)
    og = OGURL.findall(t)
    jd = JDURL.findall(t)

    if not canons:
        no_canon.append(rel)
    if len(canons) > 1:
        multi_canon.append((rel, len(canons)))
    if any(PLACEHOLDER in u for u in canons):
        ph_canon.append(rel)
    if any(PLACEHOLDER in u for u in og):
        ph_og.append(rel)
    if any(PLACEHOLDER in u for u in jd):
        ph_jd.append(rel)

    # does the single canonical point at this page's own URL? (path comparison only)
    if canons:
        path = "/" + rel
        cpath = canons[0].split("//", 1)[-1]
        cpath = cpath.split("/", 1)[1] if "/" in cpath else ""
        if cpath.rstrip("/") != path.lstrip("/"):
            selfmiss.append((rel, canons[0]))

print(f"pages scanned: {len(pages)}")
print(f"pages with an inline JSON-LD url field: {sum(1 for p in pages if JDURL.search(p.read_text(encoding='utf-8', errors='replace')))}")
print()
print(f"PLACEHOLDER {PLACEHOLDER} STILL PRESENT")
print(f"  in canonical   : {len(ph_canon)}")
print(f"  in og:url      : {len(ph_og)}")
print(f"  in JSON-LD url : {len(ph_jd)}")
print(f"  in any field   : {len(set(ph_canon) | set(ph_og) | set(ph_jd))}")
print()
print(f"PAGES WITH NO CANONICAL AT ALL ({len(no_canon)}):")
for r in no_canon:
    print("   ", r)
print()
print(f"PAGES WITH MULTIPLE CANONICAL TAGS ({len(multi_canon)}):")
for r, n in multi_canon:
    print(f"    {r}  ({n})")
print()
print(f"CANONICAL DOES NOT MATCH OWN PATH ({len(selfmiss)}):")
for r, c in selfmiss:
    print(f"    {r}  ->  {c}")