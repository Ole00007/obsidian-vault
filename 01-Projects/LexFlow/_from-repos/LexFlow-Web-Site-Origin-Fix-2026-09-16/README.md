# LexFlow Web-Site Origin Fix — evidence pack (2026-09-16)

Raw evidence behind [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]]. Nothing here
touched the live repo — all runs were made in scratch copies.

| File | What it is |
|---|---|
| `PLAN.md` | copy of the plan note as delivered |
| `audit_origin.py` | audits a site tree: placeholder origin per field, self-referential canonical, missing/duplicate canonicals |
| `audit-before.txt` | committed tree: 54 canonicals / 51 og:url / 48 JSON-LD on the placeholder; 9 real pages with the wrong canonical |
| `audit-after.txt` | after env-driven `ORIGIN` only → **not sufficient**: 24 / 21 / 48 still on the placeholder |
| `audit-after3.txt` | after the full fix (self-stamp + origin rotation) → 0 / 0 / 0, only the 6 probe strays remain |
| `build-lang-sites-ORIGIN.patch` | 134-line patch to `templates/build-lang-sites.py` implementing P0.1–P0.3 |
| `build-out3.txt` | clean build log: 48 sitemap URLs, 28 files rotated, drift guard PASS |
| `snap.py` / `diffsnap.py` | before/after per-page snapshot + diff of canonical/og:url/JSON-LD |
| `deploy_hygiene.py` / `hygiene.txt` | what a repo-root deploy would publish: 53 non-content files, 4 tracked duplicates, 15 `templates/` HTML copies |
| `make_dist.py` | curated `dist/` whitelist → 88 files, 0 forbidden files |

Reproduce:

```
python3 audit_origin.py "<site root>"            # defect inventory, before/after
python3 deploy_hygiene.py "<site root>"          # publish-set pollution
python3 make_dist.py "<site root>" dist          # curated deploy output
cd "<site root>" && ORIGIN=https://<host> python3 templates/build-lang-sites.py   # after P0 patch
```

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]], [[LexFlow-Web-Site-Build-2026-09-07]]