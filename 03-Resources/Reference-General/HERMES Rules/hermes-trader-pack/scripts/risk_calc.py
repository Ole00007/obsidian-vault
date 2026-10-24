"""Deterministic sizing and lock checks for Hermes Trader (paper). No network, no orders."""
from decimal import Decimal, ROUND_DOWN

def size_long(equity, risk_pct, entry, stop, fee_per_unit, slip_per_unit, cash, max_notional_pct, liquidity_qty, step):
    d = lambda x: Decimal(str(x))
    equity, entry, stop = d(equity), d(entry), d(stop)
    if stop >= entry:
        return Decimal(0), "SKIP: stop not below entry"
    adverse = (entry - stop) + d(fee_per_unit) + d(slip_per_unit)
    caps = [d(equity) * d(risk_pct) / Decimal(100) / adverse,
            d(cash) / entry,
            equity * d(max_notional_pct) / Decimal(100) / entry,
            d(liquidity_qty)]
    q = min(caps)
    step = d(step)
    q = (q / step).to_integral_value(rounding=ROUND_DOWN) * step
    if q <= 0:
        return Decimal(0), "SKIP: below minimum size"
    return q, "OK"

def locks(session_start_eq, week_start_eq, hwm_adj, eq_now, session_losses_streak, entries_today):
    s = (eq_now - session_start_eq) / session_start_eq * 100
    w = (eq_now - week_start_eq) / week_start_eq * 100
    dd = (eq_now - hwm_adj) / hwm_adj * 100
    out = []
    if s <= -0.5: out.append("DAILY_LOCK")
    if w <= -1.5: out.append("WEEKLY_LOCK")
    if dd <= -3.0: out.append("DRAWDOWN_LOCK")
    if session_losses_streak >= 2: out.append("LOSS_STREAK_LOCK")
    if entries_today >= 3: out.append("MAX_ENTRIES")
    return out

def quote_ok(age_s, max_age_s=5):
    return age_s is not None and 0 <= age_s <= max_age_s
