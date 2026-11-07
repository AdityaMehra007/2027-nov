import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app

def test_finance_greeks_endpoint():
    app = create_app()
    client = TestClient(app)

    res = client.post("/api/v1/finance/greeks", json={
        "spot": 100.0,
        "strike": 100.0,
        "time_to_maturity_years": 1.0,
        "risk_free_rate": 0.05,
        "volatility": 0.20
    })
    assert res.status_code == 200
    greeks = res.json()
    assert greeks["call_price"] > 0
    assert greeks["put_price"] > 0
    assert 0.0 <= greeks["delta_call"] <= 1.0
    assert -1.0 <= greeks["delta_put"] <= 0.0
    assert greeks["gamma"] > 0
    assert greeks["vega"] > 0

def test_finance_arbitrage_and_quotes_endpoint():
    app = create_app()
    client = TestClient(app)

    # Quotes
    res_q = client.get("/api/v1/finance/quotes")
    assert res_q.status_code == 200
    quotes = res_q.json()
    assert len(quotes) >= 5
    assert any(q["symbol"] == "NIFTY50" for q in quotes)

    # Arbitrage Scan
    res_arb = client.post("/api/v1/finance/arbitrage", json={
        "initial_capital": 50000.0,
        "rates": {
            "USD_INR": 84.15,
            "EUR_USD": 1.085,
            "EUR_INR": 91.50
        }
    })
    assert res_arb.status_code == 200
    arb = res_arb.json()
    assert "profit_pct" in arb
    assert arb["start_amount"] == 50000.0
    assert len(arb["pair_path"]) == 4

def test_finance_macro_regime_endpoint():
    app = create_app()
    client = TestClient(app)

    res = client.post("/api/v1/finance/macro", json={
        "inflation_cpi_pct": 4.5,
        "repo_rate_pct": 6.5,
        "gdp_growth_pct": 7.0
    })
    assert res.status_code == 200
    macro = res.json()
    assert macro["regime"] == "EXPANSION"
    assert "strategic_asset_allocation" in macro
    assert macro["strategic_asset_allocation"]["Equities"] > 0.40
