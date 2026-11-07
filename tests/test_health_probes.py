from fastapi.testclient import TestClient
from omniverse.api.app import create_app


def test_healthz_and_readyz_probes():
    app = create_app()
    client = TestClient(app)

    # 1. Test /healthz
    h_res = client.get("/healthz")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"

    # 2. Test /readyz
    r_res = client.get("/readyz")
    assert r_res.status_code == 200
    assert r_res.json()["status"] == "ready"
    assert r_res.json()["database"] == "connected"
