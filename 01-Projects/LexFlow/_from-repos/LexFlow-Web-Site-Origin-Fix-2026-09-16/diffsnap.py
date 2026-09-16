#!/usr/bin/env python3
"""Diff two snap.py outputs: pages still carrying the placeholder, and fields that changed."""
import json
import sys
from collections import Counter

before = json.load(open(sys.argv[1]))
after = json.load(open(sys.argv[2]))
placeholder = sys.argv[3] if len(sys.argv) > 3 else "lexflow.example.com"
fields = ["canonical", "og:url", "jsonld_url"]

print("== PAGES STILL CONTAINING", placeholder, "AFTER REBUILD ==")
tot = Counter()
for i, f in enumerate(fields):
    n = sum(1 for v in after.values() if v[i] and placeholder in v[i])
    tot[f] = n
    print(f"  {f}: {n}")
print("  any field:", sum(1 for v in after.values() if any(x and placeholder in x for x in v)))

print("\n== FIELDS THAT CHANGED DURING REBUILD ==")
changed = 0
for p, v in sorted(after.items()):
    b = before.get(p)
    if b and b != v:
        changed += 1
        print(" ", p)
        for f, x, y in zip(fields, b, v):
            if x != y:
                print(f"      {f}: {x}  ->  {y}")
print("changed pages:", changed)