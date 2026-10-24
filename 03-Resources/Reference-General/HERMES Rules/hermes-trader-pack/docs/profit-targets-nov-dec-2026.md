# Profit Targets, Nov-Dec 2026 (planning ranges, not forecasts)

Prepared 2026-10-24. Window: 42 US cash-market sessions (20 in November, 22 in December, excluding Nov 26 and Dec 25; check early closes on Nov 27 and Dec 24).

## Verdict
- 30-50% per day is rejected as an objective. Evidence: in Brazilian futures, 97% of persistent day traders lost money and the best earned about US$310/day with high risk; in Taiwan fewer than 1% reliably earned positive abnormal net returns, and a later study found aggregate net losses. Top-500 traders earned ~38 bps/day after fees only in-sample-ranked, which is a ranking outcome, not an achievable rate.
- Targets below are derived from risk budgets: Net return = risk per trade x number of trades x net expectancy (R). They are caps on what the pilot rules can plausibly produce, not predictions of what the agent will earn. Most outcomes should be expected near zero or negative until a strategy is validated.

## Context on 2026-10-24
Cboe VIX closed 19.45 on Oct 23 (52-week range 13.38-35.30); the S&P 500 closed 7,623.68. Moderately elevated volatility argues for conservative sizing, not higher targets. No verified crypto execution data was retrieved; do not use this document for price levels.

## Scenario math (paper, net of modeled costs)
| Mode | Scenario | Risk/trade % | Trades Nov-Dec | Net expectancy (R) | Net return % |
|---|---|---|---|---|---|
| Intraday | Reject | 0.10 | 40 | -0.10 | -0.40 |
| Intraday | Break-even floor | 0.10 | 40 | +0.00 | +0.00 |
| Intraday | Base (validated) | 0.10 | 40 | +0.10 | +0.40 |
| Intraday | Strong | 0.10 | 80 | +0.20 | +1.60 |
| Swing | Reject | 0.50 | 12 | -0.10 | -0.60 |
| Swing | Break-even floor | 0.50 | 12 | +0.00 | +0.00 |
| Swing | Base (validated) | 0.50 | 12 | +0.15 | +0.90 |
| Swing | Strong | 0.50 | 16 | +0.25 | +2.00 |

Formula check: 40 trades x 0.10% x 0.10R = 0.40%.

## Recommended target ranges (net, after fees/slippage, over Nov-Dec)
| Mode | Floor (must not fail) | Credible target | Stretch (only if validated) | Hard stop |
|---|---|---|---|---|
| Intraday | >= 0% net, zero rule breaches | 0% to +1.0% total (about 0-0.5%/month) | +2% | Daily lock -0.50%; weekly -1.50%; experiment drawdown -3.00% |
| Swing | >= 0% net, zero rule breaches | 0% to +2.0% total | +3% | Per-trade risk 0.50%; weekly -2.0%; drawdown -4.00% |

Per-day expectation for intraday: roughly 0.00-0.03% per session on average. An individual day will mostly be flat or a small loss; do not manage to a daily number.

## Success definitions (priority order)
1. Engineering: zero live orders, zero secret exposure, 100% reconciliation, fail-closed fault tests.
2. Process: every trade traceable to a frozen manifest; trade count driven by qualifying setups only.
3. Statistics: >= 30 sessions and >= 50 naturally qualifying intraday trades (or >= 20 swing trades) before any conclusion; otherwise INCONCLUSIVE.
4. Performance: positive net expectancy with confidence interval reviewed; beats cash and a passive benchmark; max drawdown within locks.

## Rules tied to the targets
- No quota: reaching the target ends new risk for the month's profit-protection review; falling short never raises size.
- Partial profits: staged exit hypothesis (1/3 at +1d, 1/3 at +2d, runner) vs full exit must be compared out of sample; adopt the one with better net expectancy.
- If by Dec 15 the strategy is below break-even with >= 30 trades, stop and archive; do not extend by loosening rules.
- Profit-lock idea (hypothesis): after +0.75% intraday monthly gain, halve per-trade risk for the rest of the month.
- A paper EUR 200 live-scale test is likely unviable: 0.10% of 200 = EUR 0.20 risk per trade, smaller than typical costs/minimums.

## Reconsider targets when
Live-quality data, costs, and at least 100 out-of-sample trades exist. Then re-estimate using the measured expectancy and its uncertainty, not hope.
