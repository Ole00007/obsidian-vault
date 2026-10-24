---
name: shares-analytics-trading
description: "Analyze listed shares and index exposure using verified prices, filings, fundamentals, valuation, catalysts and reproducible technical evidence. Use for equity research, screening, backtesting and authorized paper tests. Requires trading-risk-governor."
metadata:
  version: "3.0"
  reviewed: "2026-10-24"
---

# Shares and Index Analytics

## When to Use
Listed-company research, index/ETF analysis, earnings reviews, theses, conditional trade plans and paper-strategy evaluation (intraday or swing).

## Dependency
Read trading-risk-governor first; otherwise research only. No live orders or permission changes.

## Instructions
1. Establish horizon, exchange, base currency, objective and as-of time.
2. Resolve issuer, ticker, exchange, share class, currency and identifier; distinguish shares, ADRs, ETFs, indexes, CFDs, derivatives, tokenized assets.
3. An index level is not tradable; name the implementation instrument and check tracking, cost, liquidity and legal access. For EU retail accounts check product eligibility and disclosure documents (PRIIPs/KID); do not assume US ETFs are available.
4. Use governor sources; verify claims in filings, not snippets. Record quote delay, feed coverage (single-venue vs consolidated), session and corporate actions.
5. Use real exchange calendars and daylight-saving rules; never hardcode time conversions.
6. Separate reported results, adjusted figures, guidance, consensus and own calculations.
7. Assess business quality, margins, cash conversion, leverage, dilution; valuation with explicit assumptions and sensitivities.
8. Technical and relative-strength measures from suitable data; correlated indicators are not independent evidence.
9. Verify catalysts; confirmed date vs vendor estimate. Keep long-term theses apart from short-term signals.
10. Write thesis, counter-case, invalidation and expiry before any plan; apply governor sizing, stops, exits and locks.
11. Backtests need point-in-time fundamentals, constituents, corporate actions and realistic fills (no same-close fill from a close-based signal).
12. Keep dated thesis revisions, rejected candidates and failed variants.

## Pilot Universe
One liquid, legally eligible cash share or unleveraged index ETF. No options, futures, leveraged/inverse ETFs, CFDs, shorts, penny stocks, earnings-event trades or extended hours.

## Output
Identity, timestamp, session, feed and quality; evidence; valuation and technicals where relevant; thesis, counter-case, catalyst, invalidation, expiry; plan or NO TRADE; costs and governor result.

## Examples
"Trade the S&P 500": choose an eligible instrument; never order an index level. "Buy before earnings": verify the date; reject under pilot policy.
