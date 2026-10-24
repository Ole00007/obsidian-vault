from decimal import Decimal
from risk_calc import size_long, locks, quote_ok

def test_size_risk_bound():
    q, s = size_long(10000, 0.10, 100, 99, 0.01, 0.01, 10000, 20, 1000, 1)
    assert s == "OK" and q == Decimal(9)  # 10 / 1.02 = 9.8 -> 9; notional cap allows 20

def test_skip_when_too_small():
    q, s = size_long(200, 0.10, 100, 99, 0.05, 0.05, 200, 20, 1000, 1)
    assert q == 0 and s.startswith("SKIP")

def test_bad_stop():
    assert size_long(1000, 0.1, 100, 101, 0, 0, 1000, 20, 10, 1)[0] == 0

def test_locks():
    assert "DAILY_LOCK" in locks(1000, 1000, 1000, 994, 0, 0)
    assert locks(1000, 1000, 1000, 1000, 0, 0) == []
    assert "LOSS_STREAK_LOCK" in locks(1000, 1000, 1000, 1000, 2, 0)

def test_quote():
    assert quote_ok(3) and not quote_ok(9) and not quote_ok(None)
