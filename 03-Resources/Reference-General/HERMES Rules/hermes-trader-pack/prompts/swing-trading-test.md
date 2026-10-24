# Prompt - Swing Paper Test (Hermes Trader)
Read SOUL.md, trading-risk-governor, the relevant asset skill, docs/profit-targets-nov-dec-2026.md.

Objective: evaluate a multi-day, closed-bar strategy on one eligible instrument (cash share, unleveraged ETF, or BTC/ETH spot). Target range for Nov-Dec: 0 to +2.0% net (stretch +3% only if validated); floor = no loss and zero rule breaches. Risk 0.50% per trade, <= 2 concurrent positions, aggregate open risk <= 1.0%, weekly lock -2.0%, drawdown lock -4.0%. No earnings-event trades, no leverage, no averaging down. No quota; <= 16 trades.

Steps: preflight as in day-trading-test; freeze manifest including holding period, gap and weekend/overnight risk, event calendar, trailing/partial-exit plan; evaluate once per closed daily bar using deterministic code; document thesis, counter-case, invalidation, expiry; apply governor sizing; record each decision; weekly review with templates/weekly-review.md; cross-test the code and tests (Перекрёстный тест).
Stop rule: if net result is below break-even after >= 20 trades or by Dec 15 with a drawdown lock hit, mark REJECTED/INCONCLUSIVE and archive; never loosen rules to continue.
Report like the day-trading prompt plus gap losses versus planned stop losses.
