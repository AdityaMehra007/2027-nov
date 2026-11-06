from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ONLINE"

def test_landing():
    res = client.get("/")
    assert res.status_code == 200
    assert "OmniSpecialtyCafeFlow" in res.text

def test_checkout():
    res = client.post("/api/v1/billing/checkout")
    assert res.status_code == 200
    assert "checkout_url" in res.json()
