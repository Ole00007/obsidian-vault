# Prompt - Set Up an Isolated Hermes Trader
Help me set up a paper-first Trader. Prefer Nous Portal after verifying available models; invent no model IDs; copy no credentials.

Do not: submit identity attestations or accept agreements for me; register an account as an AI; ask for passwords, recovery codes, API secrets or ID documents in chat; fund or transfer; enable live trading, withdrawals, leverage or derivatives; clone a profile holding personal credentials.

Ask only what is needed: jurisdiction, operating system/Hermes install, existing vs new Alpaca paper account.
1 Inspect without changing (Hermes version, profile names, credential-inheritance risks); show planned changes.
2 Create fresh profile (verify syntax for the installed version): hermes profile create trader --no-skills --no-alias ; hermes profile show trader. No --clone flags. Place SOUL.md, memories/MEMORY.md and three skills; scripts/ beside them.
3 Secure runtime: isolated OS/container, restricted mounts, no personal browser profiles, paper-execution service with host/account allowlists, no money-movement capability, no YOLO mode, fail-closed unattended settings.
4 Guide registration (Alpaca paper) on the official site; pause for email, MFA, agreements; never claim an account exists before I confirm and a non-secret check passes. No live upgrade.
5 Connect secrets only through local protected entry; report masked IDs; verify paper endpoint, account ID, instrument and data entitlement.
6 Validate: agentskills validate on each skill directory; run scripts tests; fault demos; log redaction; Перекрёстный тест. Syntax validation is not security or profitability evidence.
7 Request explicit paper authorization listing account, endpoint, balance, universe, test ID, limits, duration, stop/revoke procedure.
Deliver file paths/versions, verified vs missing capabilities, masked checks, test results, launch, stop/revoke and rollback steps. Keep token use low; use code for repetitive checks.
