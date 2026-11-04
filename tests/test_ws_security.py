import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.api.routes.ws import ALLOWED_ORIGINS


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "ws_sec_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    return TestClient(app)


def test_websocket_valid_origin(client):
    """Test valid origin connects successfully and receives INITIAL_STATE."""
    with client.websocket_connect(
        "/api/v1/ws/telemetry",
        headers={"origin": "http://127.0.0.1:8888"}
    ) as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"
        assert "financial_ledger" in data
        assert "pipeline_summary" in data


def test_websocket_no_origin_header(client):
    """Test absence of origin header (CLI/native scripts) connects successfully."""
    with client.websocket_connect("/api/v1/ws/telemetry") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"
        assert "financial_ledger" in data
        assert "pipeline_summary" in data


def test_websocket_forbidden_origin(client):
    """Test forbidden origin triggers close with code 1008 (Policy Violation)."""
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            "/api/v1/ws/telemetry",
            headers={"origin": "http://evil-attacker.com"}
        ):
            pass
    assert exc_info.value.code == 1008


@pytest.mark.parametrize("origin", list(ALLOWED_ORIGINS))
def test_all_allowed_origins_permitted(client, origin):
    """Test all origins defined in ALLOWED_ORIGINS are accepted."""
    with client.websocket_connect(
        "/api/v1/ws/telemetry",
        headers={"origin": origin}
    ) as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"


def test_websocket_forbidden_capitalized_origin_header(client):
    """Test forbidden origin with capitalized 'Origin' header is rejected."""
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            "/api/v1/ws/telemetry",
            headers={"Origin": "https://attacker-domain.xyz"}
        ):
            pass
    assert exc_info.value.code == 1008


def test_websocket_valid_capitalized_origin(client):
    """Test valid origin using capitalized 'Origin' header connects successfully."""
    with client.websocket_connect(
        "/api/v1/ws/telemetry",
        headers={"Origin": "http://localhost:8888"}
    ) as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"


def test_websocket_valid_origin_with_surrounding_whitespace(client):
    """Test valid origin with leading/trailing whitespace connects successfully."""
    with client.websocket_connect(
        "/api/v1/ws/telemetry",
        headers={"origin": "  http://127.0.0.1:8888  "}
    ) as websocket:
        data = websocket.receive_json()
        assert data["type"] == "INITIAL_STATE"


@pytest.mark.parametrize("malicious_origin", [
    "null",
    "http://localhost:8888.evil.com",
    "http://127.0.0.1:8888.attacker.org",
    "https://localhost:8888",
    "http://localhost:8888/",
    "http://localhost:8888:80",
    "http://localhost:9999",
    "",
    "   ",
])
def test_websocket_rejects_edge_case_and_malformed_origins(client, malicious_origin):
    """Test that null, subdomains, scheme mismatches, and trailing slashes are strictly rejected."""
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            "/api/v1/ws/telemetry",
            headers={"origin": malicious_origin}
        ):
            pass
    assert exc_info.value.code == 1008


def test_websocket_bidirectional_ping_poll_communication(client):
    """Test valid origin connection can exchange ping/pong and poll/snapshot payloads."""
    with client.websocket_connect(
        "/api/v1/ws/telemetry",
        headers={"origin": "http://127.0.0.1:8888"}
    ) as websocket:
        initial = websocket.receive_json()
        assert initial["type"] == "INITIAL_STATE"

        websocket.send_text("ping")
        pong = websocket.receive_json()
        assert pong == {"type": "PONG"}

        websocket.send_text("poll")
        snapshot = websocket.receive_json()
        assert snapshot["type"] == "SNAPSHOT"
        assert "financial_ledger" in snapshot
        assert "pipeline_summary" in snapshot

