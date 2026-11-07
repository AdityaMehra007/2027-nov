import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app

def test_clearing_reserves_endpoint():
    app = create_app()
    client = TestClient(app)

    res = client.get("/api/v1/clearing/reserves")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OPERATIONAL"
    assert "INR" in data["reserves"]
    assert "USD" in data["reserves"]
    assert data["reserves"]["INR"] > 1000000.0

def test_clearing_rates_and_quote_endpoint():
    app = create_app()
    client = TestClient(app)

    # Rates
    res_rates = client.get("/api/v1/clearing/rates")
    assert res_rates.status_code == 200
    rates_data = res_rates.json()
    assert rates_data["base_currency"] == "INR"
    assert rates_data["rates"]["USD"] >= 80.0

    # Quote (USD to INR)
    res_quote = client.post("/api/v1/clearing/quote", json={
        "source_currency": "USD",
        "target_currency": "INR",
        "source_amount": 1000.0
    })
    assert res_quote.status_code == 200
    quote = res_quote.json()
    assert quote["source_amount"] == 1000.0
    assert quote["target_amount"] >= 80000.0
    assert quote["fee_rate_bps"] == 15
    assert quote["fee_amount"] > 0

def test_clearing_atomic_settlement_execution():
    app = create_app()
    client = TestClient(app)

    res = client.post("/api/v1/clearing/settle", json={
        "sender_id": "ACC-CORP-US-01",
        "recipient_id": "ACC-GCC-BLR-99",
        "source_currency": "USD",
        "target_currency": "INR",
        "source_amount": 5000.0
    })
    assert res.status_code == 200
    tx = res.json()
    assert tx["status"] == "SETTLED"
    assert tx["sender_id"] == "ACC-CORP-US-01"
    assert tx["recipient_id"] == "ACC-GCC-BLR-99"
    assert tx["settlement_hash"].startswith("0x")
    assert tx["target_amount"] >= 400000.0
