import pytest
from omniverse.modules.intelligence.derivatives import DerivativesEngine, OptionGreeks, TriangularArbitrageOpportunity

def test_black_scholes_at_the_money_call():
    engine = DerivativesEngine()
    greeks = engine.calculate_black_scholes_greeks(
        spot=100.0,
        strike=100.0,
        time_to_maturity_years=1.0,
        risk_free_rate=0.05,
        volatility=0.20
    )

    assert isinstance(greeks, OptionGreeks)
    # Typical ATM call with 5% rate and 20% vol is around $10.45
    assert 9.0 <= greeks.call_price <= 12.0
    # Put price via put-call parity: C - P = S - K * exp(-rT) -> ~5.57
    assert 4.5 <= greeks.put_price <= 7.0
    # ATM Delta is ~0.63
    assert 0.50 <= greeks.delta_call <= 0.75
    # Put Delta is call Delta - 1
    assert -0.50 <= greeks.delta_put <= -0.25
    assert greeks.gamma > 0.0
    assert greeks.vega > 0.0

def test_triangular_arbitrage_detection():
    engine = DerivativesEngine()
    # Synthetic arbitrage scenario:
    # USD/INR = 80.0, EUR/USD = 1.10, EUR/INR = 92.0 (synthetic cross is 88.0, 92.0 offers mispricing)
    rates = {
        "USD_INR": 80.0,
        "EUR_USD": 1.10,
        "EUR_INR": 92.0
    }
    arb = engine.detect_triangular_arbitrage(rates=rates, initial_capital=100000.0)

    assert isinstance(arb, TriangularArbitrageOpportunity)
    assert arb.profit_pct > 0.0
    assert arb.end_amount > arb.start_amount
    assert arb.arbitrage_detected is True
