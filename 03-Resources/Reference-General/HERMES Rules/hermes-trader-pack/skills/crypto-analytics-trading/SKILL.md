---
name: crypto-analytics-trading
description: "Research cryptocurrencies, screen spot markets, assess on-chain evidence and build reproducible conditional trading plans. Use for crypto analysis, portfolio reviews, backtesting and authorized paper tests. Requires trading-risk-governor before actionable plans."
metadata:
  version: "3.0"
  reviewed: "2026-10-24"
---

# Crypto Analytics and Trading

## When to Use
Crypto research and conditional spot plans. Default to analysis; paper execution only with explicit authorization.

## Dependency
Read trading-risk-governor first. Without it, output non-actionable research only. This skill cannot authorize live orders, signing, approvals, transfers, leverage or limit changes.

## Instructions
1. Establish asset, venue, quote currency, timeframe, mode (intraday or swing) and as-of time.
2. Resolve provider ID, chain, exact contract and native/wrapped/bridged status; a ticker alone is not identity.
3. Verify regional availability, fees, minimums, precision and order types in the account.
4. Keep executable venue data separate from aggregated and wallet-label data; apply the governor data gate.
5. Check liquidity, spread, depth, unlocks, emissions, security events and protocol economics; do not equate fees, revenue, incentives and TVL.
6. Treat wallet labels and exchange-flow tags as fallible; a transfer is not proof of buying or selling.
7. Compute a small justified indicator set with tested code on closed candles.
8. Separate observed facts, calculations, interpretation and scenarios; include the strongest counter-case, invalidation and expiry.
9. Apply governor sizing, stops, exits, locks and anti-overtrading rules unchanged.
10. Record the decision before the outcome. Backtests: chronological, costs, benchmarks, untouched test data, failed variants kept.
11. Abstain when data, costs, liquidity or evidence are inadequate.

## Pilot Universe
BTC and ETH spot pairs actually supported by the account only (verify exact EEA-available quote assets). No new listings, memecoins, DeFi signing, perpetuals, lending or staking.

## Output
Timestamp, instrument, feed and data quality; sourced observations; thesis and counter-case; plan or NO TRADE; stop, cost, quantity eligibility and exit plan; governor result; next review trigger. No invented targets, probabilities or backtests.

## Examples
"Analyze ETH for three months": dated research and scenarios, not an intraday order. "Smart money bought": verify the claim; labels alone never authorize an order.
