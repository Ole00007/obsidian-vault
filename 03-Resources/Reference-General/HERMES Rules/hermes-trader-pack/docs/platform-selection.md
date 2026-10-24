# Trader Platform Selection (2026-10-24)
Recommendation conditional on eligibility, terms, costs and owner approval. No account has been created.

## Sequence
1 Alpaca paper-only, no deposit (open to anyone globally per Alpaca docs; this does not prove live eligibility). 2 One asset class and one instrument first. 3 Later, human-owned live account only after review: IBKR for cash shares/eligible ETFs, Kraken spot for crypto, each subject to Italy/EEA checks.

| Platform | Role | Limitation |
|---|---|---|
| Alpaca paper | API and agent workflow test | Simulation omits market impact, latency slippage, queue position, fees; free IEX feed covers roughly 2.5% of US volume vs paid consolidated SIP |
| Interactive Brokers | Later shares/ETFs via API | Permissions, data fees, cash-account settlement, EU PRIIPs product eligibility (US ETFs may be rejected for retail) |
| Kraken Pro | Later eligible spot crypto | Dynamic fee tiers (check live schedule; base tier 0.40% maker / 0.80% taker as seen on the fee page), EEA restrictions incl. delisted stablecoins, no assumed spot subaccounts |

Sources: docs.alpaca.markets trading-api; alpaca.markets/learn/fetch-historical-data; interactivebrokers.ie API page; interactivebrokers.com campus (cash accounts); kraken.com/features/fee-schedule; kraken.com/legal/eea-terms; support.kraken.com stablecoin-offerings-for-eea-clients.

## Small-account economics
EUR 200 x 0.10% = EUR 0.20 planned risk per intraday trade; costs and minimum order sizes will likely make compliant trades impossible. Stay paper-only if so. Never trade to earn fee tiers.

## Separate account meaning
The verified human owns it; the agent is an authorized client. Need dedicated credentials, no withdrawal/transfer/margin/derivative permissions, no auto top-up, no access to strategic holdings. A second API key on the same account is not balance isolation.

## Registration boundary
Assistant may explain, verify official domains, guide setup, verify non-secret configuration. Owner must supply accurate identity, pass KYC/MFA, accept agreements, approve funding and any live permission. Never bypass restrictions with VPN or false data.
