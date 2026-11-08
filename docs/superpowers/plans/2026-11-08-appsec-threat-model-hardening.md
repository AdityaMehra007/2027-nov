# CASHFLOW INFINITY: OMNIVERSE AppSec Threat Model Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remediate and harden the top 4 critical/high vulnerabilities identified in the official AppSec Threat Model (`docs/cashflow-infinity-omniverse-threat-model.md`): unauthenticated gross clearing settlements (TM-001), unauthenticated RTGS invoice reconciliations (TM-002), SaaS scaffolder filesystem path traversal (TM-003), and production mock webhook secrets leakage (TM-004).

**Architecture:** Implement perimeter defenses directly into FastAPI route boundaries and core domain adapters. Introduce strict path normalization to jail directory generation, enforce HMAC-SHA256 signature verification on RTGS settlement webhooks, integrate the air-gapped `SecurityGovernor` into high-value clearing settlements, and enforce fail-closed cryptographic key validation in production environments.

**Tech Stack:** Python 3.13, FastAPI, SQLModel / SQLite, Cryptography (HMAC-SHA256, Ed25519), Pytest.

**Spec:** `docs/cashflow-infinity-omniverse-threat-model.md`

## Global Constraints

- Python versions supported: Python 3.10+ (active: Python 3.13).
- Test suite integrity: All 84 existing tests across `tests/` must remain passing without regressions.
- No network requests during tests: All cryptographic and settlement tests must execute hermetically and offline.
- Backward compatibility: Development mode continues to support local testing workflows while production mode fails closed.
- Coding standards: PEP 8 compliant, fully type-annotated, standard library `hmac`, `hashlib`, and `pathlib.Path` usage.

---

### Task 1: Harden SaaS Scaffolder against Path Traversal (TM-003)

**Files:**
- Modify: `src/omniverse/modules/saas_factory/scaffolder.py`
- Modify: `src/omniverse/api/routes/saas.py`
- Modify: `tests/test_saas_factory.py`

**Interfaces:**
- Consumes: `ScaffoldRequest` from `src/omniverse/api/routes/saas.py`.
- Produces: Sanitized `target_dir` guaranteed to resolve within an allowed sandbox directory. Raises `ValueError` / `HTTPException(status_code=400)` on path traversal attempts (`..`, absolute paths outside sandbox).

- [ ] **Step 1: Write the failing test for path traversal rejection**

In `tests/test_saas_factory.py`:
```python
def test_saas_factory_path_traversal_rejected(tmp_path):
    scaffolder = SaaSFactoryScaffolder(sandbox_root=tmp_path / "sandbox")
    with pytest.raises(ValueError, match="Path traversal detected"):
        scaffolder.scaffold_project(
            app_name="Malicious App",
            target_dir=tmp_path / "outside",
            include_auth=True,
            pricing_model="freemium"
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_saas_factory.py -v`
Expected: FAIL with `ValueError: Path traversal detected` not raised.

- [ ] **Step 3: Implement path jail and validation in SaaSFactoryScaffolder and route**

In `src/omniverse/modules/saas_factory/scaffolder.py`:
Add `sandbox_root: Optional[Path] = None` to `__init__`. In `scaffold_project`, resolve `target_path = Path(target_dir).resolve()`. If `self.sandbox_root` is set, verify `target_path.is_relative_to(self.sandbox_root.resolve())`. Also reject paths containing `..`.
In `src/omniverse/api/routes/saas.py`: Catch `ValueError` and raise `HTTPException(status_code=400, detail=str(e))`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_saas_factory.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/saas_factory/scaffolder.py src/omniverse/api/routes/saas.py tests/test_saas_factory.py
git commit -m "fix(security): jail saas scaffolder to prevent path traversal (TM-003)"
```

---

### Task 2: Fail-Closed Production Secrets Guardrail for Webhooks (TM-004)

**Files:**
- Modify: `src/omniverse/modules/revenue/gateways.py`
- Modify: `src/omniverse/api/routes/webhooks.py`
- Test: `tests/test_webhooks_api.py`

**Interfaces:**
- Consumes: `OmniverseSettings.env` from `src/omniverse/core/config.py`.
- Produces: `is_mock_key` detector that raises `RuntimeError` or `HTTPException(status_code=500)` when mock secrets (`whsec_mock`, `rzp_sec_mock`) are used in `production` environment.

- [ ] **Step 1: Write the failing test**

In `tests/test_webhooks_api.py`:
```python
def test_production_mock_secret_rejection():
    adapter = StripeGatewayAdapter(webhook_secret="whsec_mock")
    with pytest.raises(RuntimeError, match="Insecure default mock webhook secret in production"):
        adapter.verify_webhook(b"{}", "t=123,v1=abc", env="production")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_webhooks_api.py -k test_production_mock_secret_rejection -v`
Expected: FAIL with `RuntimeError` not raised.

- [ ] **Step 3: Implement production secret enforcement**

In `src/omniverse/modules/revenue/gateways.py`:
In `StripeGatewayAdapter.verify_webhook` and `RazorpayGatewayAdapter.verify_webhook_signature`, accept optional `env: Optional[str] = None`. If `env == "production"` and the secret equals `"whsec_mock"` or `"rzp_sec_mock"`, raise `RuntimeError("Insecure default mock webhook secret in production")`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_webhooks_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/revenue/gateways.py src/omniverse/api/routes/webhooks.py tests/test_webhooks_api.py
git commit -m "fix(security): enforce fail-closed check on default webhook mock secrets in production (TM-004)"
```

---

### Task 3: Enforce Cryptographic HMAC Verification on RTGS Webhooks (TM-002)

**Files:**
- Modify: `src/omniverse/modules/revenue/gateways.py`
- Modify: `src/omniverse/api/routes/webhooks.py`
- Test: `tests/test_webhooks_api.py`

**Interfaces:**
- Consumes: Inbound HTTP Header `X-RTGS-Signature` or canonical HMAC-SHA256 signature payload.
- Produces: Cryptographic signature verification over `invoice_id:sender_id:source_amount`. Returns HTTP 401 if signature is absent or invalid.

- [ ] **Step 1: Write the failing test**

In `tests/test_webhooks_api.py`:
```python
def test_rtgs_unauthenticated_request_rejected(client):
    test_client, _ = client
    resp = test_client.post(
        "/api/v1/webhooks/rtgs",
        json={"invoice_id": 999, "sender_id": "ROGUE", "source_amount": 1000.0}
    )
    assert resp.status_code == 401
    assert "Missing or invalid RTGS signature" in resp.json()["detail"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_webhooks_api.py -k test_rtgs_unauthenticated_request_rejected -v`
Expected: FAIL with status code 400 or 200 instead of 401.

- [ ] **Step 3: Implement RTGS HMAC signature verification**

In `src/omniverse/modules/revenue/gateways.py`:
Add `verify_rtgs_signature(payload_str: str, signature: str, secret: str) -> bool` to `RTGSGatewayAdapter`.
In `src/omniverse/api/routes/webhooks.py`:
Add `rtgs_signature: Optional[str] = Header(None, alias="x-rtgs-signature")` to `rtgs_settlement`.
Validate signature against canonical payload string `f"{payload.invoice_id}:{payload.sender_id}:{payload.source_amount}"`. Raise `HTTPException(status_code=401, detail="Missing or invalid RTGS signature")` if invalid.

- [ ] **Step 4: Update test suite with valid and invalid signatures**

Update existing `test_rtgs_settlement_webhook_flow` to include valid `X-RTGS-Signature` header, and verify all tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/revenue/gateways.py src/omniverse/api/routes/webhooks.py tests/test_webhooks_api.py
git commit -m "feat(security): require cryptographic HMAC-SHA256 signature for RTGS settlement ingress (TM-002)"
```

---

### Task 4: Enforce SecurityGovernor Checks on High-Value Clearing Settlements (TM-001)

**Files:**
- Modify: `src/omniverse/api/routes/clearing.py`
- Test: `tests/test_clearing_api.py`

**Interfaces:**
- Consumes: `SecurityGovernor` from `src/omniverse/core/security.py`, `approval_req_id: Optional[str]` and `signature: Optional[str]` in `SettlementExecuteRequest`.
- Produces: Interception for settlements exceeding `CAPITAL_THRESHOLD_USD` ($10,000 USD). If unapproved, returns HTTP 403 with `approval_required` and `request_id`. If valid approved `approval_req_id` is supplied, proceeds with atomic settlement.

- [ ] **Step 1: Write the failing test**

In `tests/test_clearing_api.py`:
```python
def test_clearing_high_value_settlement_governor_interception():
    app = create_app()
    client = TestClient(app)

    # High value transaction exceeding $10,000 USD threshold
    res = client.post("/api/v1/clearing/settle", json={
        "sender_id": "ACC-CORP-US-01",
        "recipient_id": "ACC-GCC-BLR-99",
        "source_currency": "USD",
        "target_currency": "INR",
        "source_amount": 25000.0  # > $10,000 USD
    })
    assert res.status_code == 403
    data = res.json()
    assert "SecurityGovernor approval required" in data["detail"]
    assert "request_id" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_clearing_api.py -k test_clearing_high_value_settlement_governor_interception -v`
Expected: FAIL with status code 200 instead of 403.

- [ ] **Step 3: Implement SecurityGovernor integration in clearing router**

In `src/omniverse/api/routes/clearing.py`:
Add `approval_req_id: Optional[str] = None` to `SettlementExecuteRequest`.
Initialize `_governor = SecurityGovernor(strict_mode=True)`.
In `execute_settlement`, if `req.source_amount > _governor.CAPITAL_THRESHOLD_USD`:
Check `_governor.is_permitted(ActionType.FINANCIAL_TRANSFER, req.approval_req_id)`.
If not permitted, register approval request via `req_id = _governor.request_approval(ActionType.FINANCIAL_TRANSFER, details=req.model_dump())` and raise `HTTPException(status_code=403, detail={"error": "SecurityGovernor approval required for high-value transfer", "request_id": req_id})`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_clearing_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/api/routes/clearing.py tests/test_clearing_api.py
git commit -m "feat(security): intercept high-value clearing settlements with air-gapped SecurityGovernor (TM-001)"
```
