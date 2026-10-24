# Hermes Trader Pack v3 (2026-10-24)

Paper-first, analysis-only until owner authorization. Nothing here is installed, validated by a live broker, or financial advice.

## Contents
| Path | Status | Purpose |
|---|---|---|
| profile/SOUL.md | iterated | Trader identity, authority, targets policy |
| profile/memories/MEMORY.md | iterated | Curated starting memory |
| skills/trading-risk-governor/SKILL.md | iterated | Sources, data gate, risk, stops, profit-taking, targets |
| skills/crypto-analytics-trading/SKILL.md | iterated | Crypto research and plans |
| skills/shares-analytics-trading/SKILL.md | iterated | Shares and index research |
| docs/profit-targets-nov-dec-2026.md | NEW | Credible target ranges, intraday and swing |
| docs/platform-selection.md | iterated | Alpaca paper first; IBKR/Kraken later |
| docs/blueprints-and-evidence.md | NEW | Practitioner process and failure evidence |
| prompts/day-trading-test.md | iterated | Intraday paper test |
| prompts/swing-trading-test.md | NEW | Swing paper test |
| prompts/setup-trader.md | iterated | Setup and registration assistance |
| templates/strategy-manifest.md | NEW | Pre-registered test manifest |
| templates/decision-journal.csv | NEW | Decision/fill log columns |
| templates/weekly-review.md | NEW | Review and go/no-go |
| scripts/risk_calc.py + test_risk_calc.py | NEW | Deterministic sizing and lock checks |

## Install order
1. Create a fresh profile (no clone): `hermes profile create trader --no-skills --no-alias`; verify with the installed version.
2. Copy skills/ and profile/ files. 3. Run scripts tests. 4. Paper-only account personally registered by the owner.
Skill frontmatter was kept minimal (quoted descriptions) to avoid YAML upload errors; validate with `agentskills validate` before upload.
