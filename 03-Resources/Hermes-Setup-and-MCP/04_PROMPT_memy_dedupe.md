# 04_PROMPT_memy_dedupe

**Source:** `/Users/olesiarasing/Desktop/projects/Products & Services/LEGAL`  
**Reference (read-only):** `/Users/olesiarasing/Projects/lexflow`  
**Archive Exact:** `/Users/olesiarasing/Projects/_archive/legal-dedupe-20261026/`  
**Target Root:** `/Users/olesiarasing/Projects/`

---

## Classification

- **EXACT_DUP**: Same sha256 as a file in REFERENCE -> archive exact (kept relative path)
- **NEAR_DUP**: Same filename/relative path but different hash -> archive review (never overwrite either side; write diff summary)
- **UNIQUE**: No match -> relocate under TARGET_ROOT to the relevant folder (match by topic/ext; mirror the lexflow structure if it fits; else TARGET_ROOT/legal/<topic>/)
- **ACTIVE / SECRET**: Skip, report

---

## Links

[[01-Projects]] → Parent folder hub  
[[04-Archive]] → Related sibling (archive folder)