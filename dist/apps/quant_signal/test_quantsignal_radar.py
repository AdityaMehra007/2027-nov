import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

spec = importlib.util.spec_from_file_location("local_app_main", Path(__file__).parent / "main.py")
app_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_main)
app = app_main.app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ONLINE"

def test_landing():
    res = client.get("/")
    assert res.status_code == 200
    assert "QuantSignal Radar" in res.text

def test_checkout():
    res = client.post("/api/v1/billing/checkout")
    assert res.status_code == 200
    assert "checkout_url" in res.json()
