---
tags:
  - vault-hygiene
  - trash-purge
project: vault-hygiene
home: 05-Daily/agent-reports
---

# Trash Purge Check — 2026-11-04

Rule: delete item if >= 7 days old AND every file has a verified twin (filename match + SHA-256 match).
Newer items: keep, list purge date. Items with any unverified file: "needs Ole".

---

## Oldest-to-newest order (older than 7 days)

| Trash item | File | Twin path | Hash match | Action |
|---|---|---|---|---|
| 2026-10-10-lexflow-dedupe/ | roadmap-_Conflicts-2026-09-03-16nodes.json | — | no | needs Ole |
| 2026-10-10-lexflow-dedupe/ | roadmap-vault-_from-repos-2026-09-03-21nodes.json | — | no | needs Ole |
| _Deleted-Dupes-20261010_222526/ | AVIbe & Alessia Content Agent Skills Stack (2).md | 01-Projects/AVibe-CRM/AVIbe & Alessia Content Agent Skills Stack.md | yes | delete |
| _Deleted-Dupes-20261010_222526/ | Agent-Priority-Providermodel-Architectureparameter (1).csv | 03-Resources/AI-Models-and-Prompts/Agent-Priority-Providermodel-Architectureparameter.csv | yes | delete |
| _Deleted-Dupes-20261010_222526/ | Hermes_LexFlow_Gantt_Master_Prompt (1).md | Hermes_LexFlow_Gantt_Master_Prompt.md | yes | delete |
| _Deleted-Dupes-20261010_222526/ | avibe-humanizer (1).md | 01-Projects/AVibe-CRM/avibe-humanizer.md | yes | delete |
| _Deleted-Dupes-20261010_222526/ | avibe-viral-wide-catch-ru (1).md | 01-Projects/AVibe-CRM/avibe-viral-wide-catch-ru.md | yes | delete |
| _Deleted-Dupes-20261012_222723/ | AVIbe & Alessia Content Agent Skills Stack (2).md | 01-Projects/AVibe-CRM/AVIbe & Alessia Content Agent Skills Stack.md | yes | delete |
| _Deleted-Dupes-20261012_222723/ | Agent-Priority-Providermodel-Architectureparameter (1).csv | 03-Resources/AI-Models-and-Prompts/Agent-Priority-Providermodel-Architectureparameter.csv | yes | delete |
| _Deleted-Dupes-20261012_222723/ | CANDIDATE-full-stack-rules-v0.2 (2).md | 03-Resources/Reference-General/CANDIDATE-full-stack-rules-v0.2.md | yes | delete |
| _Deleted-Dupes-20261012_222723/ | Hermes_LexFlow_Gantt_Master_Prompt.md | Hermes_LexFlow_Gantt_Master_Prompt.md | yes | delete |
| _Deleted-Dupes-20261012_222723/ | avibe-humanizer (1).md | 01-Projects/AVibe-CRM/avibe-humanizer.md | yes | delete |
| _Deleted-Dupes-20261012_222723/ | avibe-viral-wide-catch-ru (1).md | 01-Projects/AVibe-CRM/avibe-viral-wide-catch-ru.md | yes | delete |
| _Deleted-Dupes-20261013_224610/ | CANDIDATE-full-stack-rules-v0.2 (2).md | 03-Resources/Reference-General/CANDIDATE-full-stack-rules-v0.2.md | yes | delete |
| _Deleted-Dupes-20261014_223559/ | Liguria_Hospitality_Investment_Model_RU_IT_EN (1) (1).xlsx | 03-Resources/AI-Models-and-Prompts/Liguria_Hospitality_Investment_Model_RU_IT_EN.xlsx | no | needs Ole |
| _Deleted-Dupes-20261016_225444/ | *(empty folder — _Conflicts only)* | — | — | delete |
| _Deleted-Dupes-20261021_143634/ | *(empty folder — _Conflicts only)* | — | — | delete |
| _Deleted-Dupes-20261022_222728/ | Agent-Priority-Providermodel-Architectureparameter (1).csv | 03-Resources/AI-Models-and-Prompts/Agent-Priority-Providermodel-Architectureparameter.csv | yes | delete |
| _Deleted-Dupes-20261022_222728/ | Hermes_LexFlow_Gantt_Master_Prompt.md | Hermes_LexFlow_Gantt_Master_Prompt.md | yes | delete |
| _Deleted-Dupes-20261022_222728/ | avibe-viral-wide-catch-ru (1).md | 01-Projects/AVibe-CRM/avibe-viral-wide-catch-ru.md | yes | delete |
| _Deleted-Dupes-20261023_222539/ | AVIbe & Alessia Content Agent Skills Stack (2).md | 01-Projects/AVibe-CRM/AVIbe & Alessia Content Agent Skills Stack.md | yes | delete |
| _Deleted-Dupes-20261023_222539/ | Agent-Priority-Providermodel-Architectureparameter (1).csv | 03-Resources/AI-Models-and-Prompts/Agent-Priority-Providermodel-Architectureparameter.csv | yes | delete |
| _Deleted-Dupes-20261023_222539/ | CANDIDATE-full-stack-rules-v0.2 (2).md | 03-Resources/Reference-General/CANDIDATE-full-stack-rules-v0.2.md | yes | delete |
| _Deleted-Dupes-20261023_222539/ | Hermes_LexFlow_Gantt_Master_Prompt.md | Hermes_LexFlow_Gantt_Master_Prompt.md | yes | delete |
| _Deleted-Dupes-20261023_222539/ | Liguria_Hospitality_Investment_Model_RU_IT_EN (1) (1).xlsx | 03-Resources/AI-Models-and-Prompts/Liguria_Hospitality_Investment_Model_RU_IT_EN.xlsx | no | needs Ole |
| _Deleted-Dupes-20261023_222539/ | avibe-humanizer (1).md | 01-Projects/AVibe-CRM/avibe-humanizer.md | yes | delete |
| _Deleted-Dupes-20261023_222539/ | avibe-viral-wide-catch-ru (1).md | 01-Projects/AVibe-CRM/avibe-viral-wide-catch-ru.md | yes | delete |
| _Deleted-Dupes-20261025_222502/ | *(empty folder — _Conflicts only)* | — | — | delete |
| _Deleted-Dupes-20261026_225417/ | Gap-Fix-Risk (1).csv | 01-Projects/LexFlow/Gap-Fix-Risk.csv | yes | delete |
| _Deleted-Dupes-20261027_222541/ | Gap-Fix-Risk (1).csv | 01-Projects/LexFlow/Gap-Fix-Risk.csv | yes | delete |

## Newer than 7 days (keep)

| Trash item | Purge date | Reason |
|---|---|---|
| _Deleted-Dupes-20261031_222530/ | 2026-11-07 | 7 days from 2026-10-31 |
| _Deleted-Dupes-20261103_222632/ | 2026-11-10 | 7 days from 2026-11-03 |

## Size audit

| State | Items | Total |
|---|---|---|
| Before | 14 folders | 22,060 KB (~22 MB) |
| After | 5 folders | 472 KB |

## Deleted (post-check)

9 items deleted (~21.6 MB freed):
- _Deleted-Dupes-20261010_222526/
- _Deleted-Dupes-20261012_222723/
- _Deleted-Dupes-20261013_224610/
- _Deleted-Dupes-20261016_225444/
- _Deleted-Dupes-20261021_143634/
- _Deleted-Dupes-20261022_222728/
- _Deleted-Dupes-20261025_222502/
- _Deleted-Dupes-20261026_225417/
- _Deleted-Dupes-20261027_222541/

3 items kept (needs Ole):
- 2026-10-10-lexflow-dedupe/ (2 JSON files, no twins anywhere)
- _Deleted-Dupes-20261014_223559/ (xlsx hash mismatch)
- _Deleted-Dupes-20261023_222539/ (contains xlsx hash mismatch)

2 items kept (too new):
- _Deleted-Dupes-20261031_222530/ → purge 2026-11-07
- _Deleted-Dupes-20261103_222632/ → purge 2026-11-10

## Decisions applied (2026-11-04, Ole-approved)

1. **2026-10-10-lexflow-dedupe/** — archived to `~/Obsidian/04-Archive/` (filenames kept):
   `roadmap-_Conflicts-2026-09-03-16nodes.json` and `roadmap-vault-_from-repos-2026-09-03-21nodes.json`.
   Vault, project, and script references to the old `_Trash` path updated to `04-Archive`.

2. **_Deleted-Dupes-20261014_223559/** — xlsx differs from twin (`Liguria_Hospitality_Investment_Model_RU_IT_EN.xlsx`) by sheet names (trash copy has `00_Summary, 01_Assumptions, ...`; twin has `Assumptions, Licences, Liguria_TAM, ...`). Archived to `~/Obsidian/04-Archive/Trash-Dupes-20261014_Liguria_Hospitality_Investment_Model_RU_IT_EN.xlsx`.

3. **_Deleted-Dupes-20261023_222539/** — same xlsx content difference as above. Archived to `~/Obsidian/04-Archive/Trash-Dupes-20261023_Liguria_Hospitality_Investment_Model_RU_IT_EN.xlsx`.

## Links

- [[05-Daily/2026-11-04]]
- [[03-Resources/Reference-General/CANDIDATE-full-stack-rules-v0.2]]
