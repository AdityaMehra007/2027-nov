import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

def test_websocket_telemetry(tmp_path):
    db_file = tmp_path / "ws_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()
    
    app = create_app(db_engine=db_engine)
    client = TestClient(app)
    
    with client.websocket_connect("/api/v1/ws/telemetry") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"
        assert "financial_ledger" in data
        assert "pipeline_summary" in data
