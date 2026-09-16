#!/usr/bin/env python3
"""Snapshot canonical + og:url for every page in a site tree (for before/after diff)."""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "_snap.json")
snap = {}
for p in sorted(list(root.glob("*.html")) + list(root.glob("it/*.html")) + list(root.glob("ru/*.html"))):
    t = p.read_text(encoding="utf-8", errors="replace")
    c = re.search(r'<link rel="canonical" href="([^"]*)"', t)
    o = re.search(r'<meta property="og:url" content="([^"]*)"', t)
    j = re.search(r'"url":\s*"([^"]*)"', t)
    snap[str(p)] = [c.group(1) if c else None, o.group(1) if o else None, j.group(1) if j else None]
out.write_text(json.dumps(snap, indent=1))
print("pages:", len(snap))