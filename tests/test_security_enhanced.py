import pytest
import hmac
import hashlib
import time
from omniverse.core.security import SecurityGovernor, ActionType, ApprovalStatus


def test_cryptographic_signing_and_verification():
    governor = SecurityGovernor(strict_mode=True)
    secret_key = "sovereign_founder_master_hmac_secret"

    # Request an approval for high-capital transfer
    req_id = governor.request_approval(
        action_type=ActionType.FINANCIAL_TRANSFER,
        details={"recipient": "CLOUD_CLUSTER_PROVIDER", "amount_usd": 15000.0}
    )
    assert req_id is not None
    assert governor.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id) is False

    # Check pending list
    pending = governor.get_pending_requests()
    assert req_id in pending
    assert pending[req_id]["status"] == ApprovalStatus.PENDING

    # Sign request with cryptographic HMAC-SHA256
    sig = governor.generate_signature(req_id, secret_key)
    assert len(sig) == 64

    # Grant approval with valid signature
    success = governor.verify_and_grant_signature(req_id, sig, secret_key)
    assert success is True
    assert governor.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id) is True

    # Ensure it's no longer pending
    pending_after = governor.get_pending_requests()
    assert req_id not in pending_after


def test_tampered_signature_rejection():
    governor = SecurityGovernor(strict_mode=True)
    secret_key = "sovereign_founder_master_hmac_secret"

    req_id = governor.request_approval(
        action_type=ActionType.LIVE_TRADE_ORDER,
        details={"symbol": "NIFTY_FUT", "contracts": 10}
    )

    # Bad secret key
    sig_wrong_secret = governor.generate_signature(req_id, "wrong_secret_key")
    assert governor.verify_and_grant_signature(req_id, sig_wrong_secret, secret_key) is False
    assert governor.is_permitted(ActionType.LIVE_TRADE_ORDER, req_id=req_id) is False

    # Tampered signature string
    assert governor.verify_and_grant_signature(req_id, "tampered_hex_deadbeef" * 2, secret_key) is False


def test_intercept_action_thresholds():
    governor = SecurityGovernor(strict_mode=True)

    # Low API expenditure under threshold is allowed
    allowed, req_id = governor.intercept_action(
        ActionType.API_EXPENDITURE,
        details={"cost_usd": 0.50},
        amount_usd=0.50
    )
    assert allowed is True
    assert req_id is None

    # Capital transfer above $10,000 is intercepted into air-gap
    allowed_big, req_id_big = governor.intercept_action(
        ActionType.FINANCIAL_TRANSFER,
        details={"cost_usd": 25000.0},
        amount_usd=25000.0
    )
    assert allowed_big is False
    assert req_id_big is not None
    assert governor.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id_big) is False
