import pytest
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.config import OmniverseSettings, get_settings
from omniverse.core.database import DatabaseEngine

EXPECTED_SECURITY_HEADERS = {
    "x-frame-options": "DENY",
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "content-security-policy": (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' ws: wss:; "
        "script-src 'self' 'unsafe-inline';"
    ),
}


@pytest.fixture
def db_engine(tmp_path):
    db_file = tmp_path / "sec_headers_test.db"
    engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    engine.init_db()
    return engine


@pytest.fixture
def client(db_engine):
    app = create_app(db_engine=db_engine)
    with TestClient(app) as test_client:
        yield test_client


def assert_security_headers_present(response):
    """Helper to verify presence and exact values of all required security headers."""
    for header, expected_val in EXPECTED_SECURITY_HEADERS.items():
        actual_val = response.headers.get(header)
        assert actual_val is not None, f"Missing security header: {header}"
        assert actual_val == expected_val, (
            f"Header {header} mismatch: expected '{expected_val}', got '{actual_val}'"
        )


@pytest.mark.parametrize("endpoint", [
    "/",
    "/api/v1/dashboard/summary",
    "/api/v1/revenue/leads",
])
def test_security_headers_on_standard_endpoints(client: TestClient, endpoint: str):
    """Verify all security headers are present on GET /, /dashboard/summary, and /revenue/leads."""
    response = client.get(endpoint)
    assert response.status_code == 200
    assert_security_headers_present(response)


def test_security_headers_on_redirect(client: TestClient):
    """Verify security headers are attached even on HTTP redirect responses."""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code in (301, 302, 307)
    assert_security_headers_present(response)


def test_security_headers_on_not_found(client: TestClient):
    """Verify security headers are attached on 404 Not Found error responses."""
    response = client.get("/api/v1/non-existent-route")
    assert response.status_code == 404
    assert_security_headers_present(response)


def test_security_headers_on_post_request(client: TestClient):
    """Verify security headers are attached on POST mutation endpoints."""
    response = client.post(
        "/api/v1/revenue/leads",
        json={
            "business_name": "Apex Security Test Corp",
            "category": "Enterprise Cyber",
            "city": "Bengaluru",
            "estimated_value_inr": 150000.0,
        },
    )
    assert response.status_code == 200
    assert_security_headers_present(response)


def test_openapi_docs_accessible_in_development(db_engine):
    """Verify that when env != 'production' (development), /docs, /redoc, and /openapi.json return 200 OK."""
    dev_settings = OmniverseSettings(env="development")
    app = create_app(db_engine=db_engine, settings=dev_settings)
    with TestClient(app) as dev_client:
        docs_res = dev_client.get("/docs")
        assert docs_res.status_code == 200
        assert_security_headers_present(docs_res)

        redoc_res = dev_client.get("/redoc")
        assert redoc_res.status_code == 200
        assert_security_headers_present(redoc_res)

        openapi_res = dev_client.get("/openapi.json")
        assert openapi_res.status_code == 200
        assert_security_headers_present(openapi_res)

        root_res = dev_client.get("/")
        assert root_res.status_code == 200
        assert root_res.json()["docs"] == "/docs"


def test_openapi_docs_accessible_in_staging(db_engine):
    """Verify that when env is 'staging', /docs returns 200 OK."""
    staging_settings = OmniverseSettings(env="staging")
    app = create_app(db_engine=db_engine, settings=staging_settings)
    with TestClient(app) as staging_client:
        docs_res = staging_client.get("/docs")
        assert docs_res.status_code == 200


@pytest.mark.parametrize("prod_env_val", ["production", "Production", "PRODUCTION"])
def test_openapi_docs_gated_in_production(db_engine, prod_env_val):
    """Verify that when env == 'production' (case-insensitive), docs endpoints return 404 Not Found."""
    prod_settings = OmniverseSettings(env=prod_env_val)
    app = create_app(db_engine=db_engine, settings=prod_settings)
    with TestClient(app) as prod_client:
        # /docs returns 404
        docs_res = prod_client.get("/docs")
        assert docs_res.status_code == 404
        assert_security_headers_present(docs_res)

        # /redoc returns 404
        redoc_res = prod_client.get("/redoc")
        assert redoc_res.status_code == 404
        assert_security_headers_present(redoc_res)

        # /openapi.json returns 404
        openapi_res = prod_client.get("/openapi.json")
        assert openapi_res.status_code == 404
        assert_security_headers_present(openapi_res)

        # Root endpoint shows docs=None in production
        root_res = prod_client.get("/")
        assert root_res.status_code == 200
        assert root_res.json()["docs"] is None


def test_production_env_via_monkeypatch(monkeypatch, db_engine):
    """Verify create_app inspects get_settings().env dynamically via environment variable."""
    monkeypatch.setenv("ENV", "production")
    get_settings.cache_clear()
    try:
        app = create_app(db_engine=db_engine)
        with TestClient(app) as prod_client:
            assert prod_client.get("/docs").status_code == 404
            assert prod_client.get("/redoc").status_code == 404
            assert prod_client.get("/openapi.json").status_code == 404
    finally:
        get_settings.cache_clear()


def test_trusted_host_middleware_allows_valid_and_blocks_untrusted(db_engine):
    """Verify TrustedHostMiddleware blocks spoofed Host headers when restricted."""
    restricted_settings = OmniverseSettings(
        env="development",
        allowed_hosts=["127.0.0.1", "localhost", "testserver", "trusted.omniverse.io"],
    )
    app = create_app(db_engine=db_engine, settings=restricted_settings)
    with TestClient(app) as restricted_client:
        # Valid host succeeds
        res_valid = restricted_client.get("/", headers={"host": "trusted.omniverse.io"})
        assert res_valid.status_code == 200
        assert_security_headers_present(res_valid)

        # Testserver default succeeds
        res_testserver = restricted_client.get("/", headers={"host": "testserver"})
        assert res_testserver.status_code == 200

        # Untrusted host is rejected with 400 Bad Request
        res_evil = restricted_client.get("/", headers={"host": "evil-attacker.com"})
        assert res_evil.status_code == 400
        # Even rejected requests have security headers
        assert_security_headers_present(res_evil)


def test_production_env_with_whitespace_via_monkeypatch(monkeypatch, db_engine):
    """Verify create_app correctly gates docs when ENV has surrounding whitespace."""
    monkeypatch.setenv("ENV", "  production  ")
    get_settings.cache_clear()
    try:
        app = create_app(db_engine=db_engine)
        with TestClient(app) as prod_client:
            assert prod_client.get("/docs").status_code == 404
            assert prod_client.get("/docs/").status_code == 404
            assert prod_client.get("/redoc").status_code == 404
            assert prod_client.get("/redoc/").status_code == 404
            assert prod_client.get("/openapi.json").status_code == 404
    finally:
        get_settings.cache_clear()


def test_allowed_hosts_env_var_comma_separated(monkeypatch, db_engine):
    """Verify ALLOWED_HOSTS parses comma-separated strings without SettingsError."""
    monkeypatch.setenv("ALLOWED_HOSTS", "localhost, 127.0.0.1, custom.omniverse.io")
    get_settings.cache_clear()
    try:
        settings = get_settings()
        assert "custom.omniverse.io" in settings.allowed_hosts
        assert "localhost" in settings.allowed_hosts
        assert "127.0.0.1" in settings.allowed_hosts

        app = create_app(db_engine=db_engine, settings=settings)
        with TestClient(app) as client:
            res_valid = client.get("/", headers={"host": "custom.omniverse.io"})
            assert res_valid.status_code == 200
            assert_security_headers_present(res_valid)

            res_blocked = client.get("/", headers={"host": "untrusted.attacker.com"})
            assert res_blocked.status_code == 400
            assert_security_headers_present(res_blocked)
    finally:
        get_settings.cache_clear()


def test_allowed_hosts_env_var_json_format(monkeypatch, db_engine):
    """Verify ALLOWED_HOSTS parses JSON array format from environment variable."""
    monkeypatch.setenv("ALLOWED_HOSTS", '["localhost", "json.omniverse.io"]')
    get_settings.cache_clear()
    try:
        settings = get_settings()
        assert "json.omniverse.io" in settings.allowed_hosts
        assert "localhost" in settings.allowed_hosts

        app = create_app(db_engine=db_engine, settings=settings)
        with TestClient(app) as client:
            res_valid = client.get("/", headers={"host": "json.omniverse.io"})
            assert res_valid.status_code == 200
            assert_security_headers_present(res_valid)
    finally:
        get_settings.cache_clear()


def test_allowed_hosts_string_input_in_settings(db_engine):
    """Verify raw string passed to allowed_hosts is safely handled and testserver is appended."""
    settings = OmniverseSettings(allowed_hosts="direct.host.com")
    assert settings.allowed_hosts == ["direct.host.com"]
    app = create_app(db_engine=db_engine, settings=settings)
    with TestClient(app) as client:
        # testserver automatically injected
        assert client.get("/", headers={"host": "testserver"}).status_code == 200
        assert client.get("/", headers={"host": "direct.host.com"}).status_code == 200
        assert client.get("/", headers={"host": "rogue.com"}).status_code == 400


def test_security_headers_on_method_not_allowed(client: TestClient):
    """Verify security headers are attached on 405 Method Not Allowed responses."""
    response = client.post("/")
    assert response.status_code == 405
    assert_security_headers_present(response)


def test_security_headers_on_http_exception_500(db_engine):
    """Verify security headers are attached on 500 HTTPException error responses."""
    from fastapi import HTTPException

    app = create_app(db_engine=db_engine)

    @app.get("/trigger-500")
    def trigger_500():
        raise HTTPException(status_code=500, detail="Database connection failed")

    with TestClient(app) as err_client:
        response = err_client.get("/trigger-500")
        assert response.status_code == 500
        assert_security_headers_present(response)

