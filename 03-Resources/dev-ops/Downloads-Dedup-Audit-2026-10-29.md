---
title: Downloads dedup audit
created: 2026-10-29
tags: [dev-ops, cleanup, dedup]
status: draft
---

# Downloads dedup audit

**Date:** 2026-10-29  
**Method:** SHA-256 hash of every Downloads file vs whole-vault index (3,905 files).  
**Rule:** move only byte-identical matches to `~/.Trash`; never delete.

## Summary

| | Count |
|---|---|
| Files scanned in Downloads | 220 |
| Byte-identical duplicates in vault | 184 |
| Unique files (keep) | 34 |
| System files excluded | 2 (`.DS_Store`, `.localized`) |

## Duplicates to move to Trash

184 files. Every one has a byte-identical copy somewhere in the vault (`01-Projects/`, `03-Resources/`, `_Inbox/_Conflicts/`, etc.). Moving them to `~/.Trash` is zero-data-loss and fully recoverable.

### Top categories
- LexFlow project artifacts: 60+
- Reference-General docs: 50+
- Hermes-Setup-and-MCP prompts: 20+
- AI-Models-and-Prompts CSVs: 15+
- AVibe-CRM / AVibe-Agency: 10+
- Images / HTML / ZIP bundles: 20+

## Unique files to keep in Downloads

34 files with no identical vault copy. Includes:
- `client_secret_...googleusercontent.com.json` — **sensitive, keep local only, do NOT stage to vault**
- `railway-hobby-audit.md`
- `LexFlow_Session_Pack_2026-10-19.zip`
- `goldoni6-audit*.html` / `goldoni6-audit-bundle.zip`
- `ica-v3-1-scope.zip`
- `Template_SITE-AUDIT_1_ENNEFEX_oct-2026.zip`
- Various aLEXy / avvocato-pagliano HTML snapshots
- Session JSON, agent JSON, and other unique artifacts

## Why vault stager doesn't touch Downloads

The nightly `downloads_stager.py` copies from `~/Downloads` into `_Inbox/` (vault only). It never deletes from Downloads. This cleanup is a separate, explicit task.

## Execution

**Date:** 2026-10-29  
**Result:** moved 184 files to `~/.Trash` with `-dedup-20261029` suffix; 34 unique files kept in Downloads. Zero errors.

## Links

- Parent: [[dev-ops-INDEX]]
- Related: [[DevOps-Platform-Audits]]
