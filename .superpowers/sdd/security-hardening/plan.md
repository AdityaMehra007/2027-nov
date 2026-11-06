# Implementation Plan: Institutional Security Hardening
**Target Plan**: Security Best Practices Remediation (SEC-001 through SEC-006)  
**Spec Reference**: `security_best_practices_report.md`  

## Global Constraints
- Zero regressions in existing 116 passing tests (`pytest -q`).
- Non-breaking backwards compatibility for all existing API routes and CLI handlers.
- Preserves all Apache 2.0 headers, docstrings, and type hints.

---

### Task 1: WebSocket Origin Validation & CSWSH Protection (SEC-001)
- **Target File**: `src/omniverse/api/routes/ws.py`
- **Actions**:
  1. Inspect `websocket.headers.get("origin")` on incoming WebSocket connection.
  2. Validate against allowed origin set (`http://127.0.0.1:8888`, `http://localhost:8888`, `http://localhost:3000`). If absent (non-browser tools like CLI or local scripts), permit connection.
  3. If origin is non-empty and not in allowed origins, reject connection with WebSocket close code `1008` (Policy Violation).
- **Test File**: `tests/test_ws_security.py`
- **Verification**: `pytest tests/test_ws_security.py` passes.

---

### Task 2: ASGI Security Response Headers & Gated OpenAPI Docs (SEC-002, SEC-003, SEC-006)
- **Target File**: `src/omniverse/api/app.py`
- **Actions**:
  1. Add HTTP middleware injecting `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy`.
  2. Configure `docs_url`, `redoc_url`, and `openapi_url` conditionally: enabled when `settings.env != "production"`, disabled when `settings.env == "production"`.
  3. Mount `TrustedHostMiddleware` with `allowed_hosts=["127.0.0.1", "localhost", "testserver", "*"]` (configurable via settings).
- **Test File**: `tests/test_security_headers.py`
- **Verification**: `pytest tests/test_security_headers.py` passes.

---

### Task 3: Security Governor Persistent Audit Trail (SEC-004)
- **Target File**: `src/omniverse/core/security.py`, `src/omniverse/modules/revenue/models.py`
- **Actions**:
  1. Define `SecurityAuditEntry` in SQLModel storing `req_id`, `action_type`, `details_json`, `status`, `created_at`, `resolved_at`.
  2. Enhance `SecurityGovernor` with optional database session binding to persist every request and approval decision.
  3. Maintain backward-compatible fallback for in-memory operation when run outside a database context.
- **Test File**: `tests/test_security_audit.py`
- **Verification**: `pytest tests/test_security_audit.py` passes.

---

### Task 4: Public UUID4 Identifiers for Invoices & Leads (SEC-005)
- **Target File**: `src/omniverse/modules/revenue/models.py`, `src/omniverse/api/routes/revenue.py`
- **Actions**:
  1. Add `uuid: str = Field(default_factory=...)` to `Lead` and `Invoice` models.
  2. Support fetching leads and invoices by either integer `id` or string `uuid`.
- **Test File**: `tests/test_uuid_lookup.py`
- **Verification**: `pytest tests/test_uuid_lookup.py` passes.
