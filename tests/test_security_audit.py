import json
import time
import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from sqlmodel.pool import StaticPool

from omniverse.core.security import (
    SecurityGovernor,
    SecurityAuditRecord,
    ActionType,
    ApprovalStatus,
)


@pytest.fixture
def db_session():
    """Provides a fresh in-memory SQLite database session with all tables created."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_in_memory_governor_backward_compatibility():
    """Verifies SecurityGovernor operates normally in pure in-memory mode (session=None)."""
    gov = SecurityGovernor(strict_mode=True)
    assert gov.session is None

    # Check non-gated action is permitted immediately
    assert gov.is_permitted(ActionType.API_EXPENDITURE) is True

    # Check gated action requires approval
    assert gov.is_permitted(ActionType.FINANCIAL_TRANSFER) is False

    # Request approval
    req_id = gov.request_approval(
        ActionType.FINANCIAL_TRANSFER,
        {"amount_usd": 5000.0, "recipient": "SUPPLIER_A"}
    )
    assert req_id is not None
    assert gov.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id) is False

    # Verify pending requests map
    pending = gov.get_pending_requests()
    assert req_id in pending
    assert pending[req_id]["status"] == ApprovalStatus.PENDING

    # Grant approval
    granted = gov.grant_approval(req_id, approver="test_operator")
    assert granted is True
    assert gov.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id) is True

    # Request second approval and reject it
    req_id2 = gov.request_approval(
        ActionType.LIVE_TRADE_ORDER,
        {"symbol": "NIFTY_FUT", "contracts": 5}
    )
    rejected = gov.reject_approval(req_id2)
    assert rejected is True
    assert gov.is_permitted(ActionType.LIVE_TRADE_ORDER, req_id=req_id2) is False

    # Non-existent IDs return False
    assert gov.grant_approval("missing-uuid") is False
    assert gov.reject_approval("missing-uuid") is False

    # Check get_audit_records in in-memory mode
    records = gov.get_audit_records(limit=10)
    assert len(records) == 2
    req_ids = [r["request_id"] for r in records]
    assert req_id in req_ids
    assert req_id2 in req_ids
    # Verify record fields
    for r in records:
        assert "request_id" in r
        assert "action_type" in r
        assert "status" in r
        assert "details_json" in r
        assert "created_at" in r


def test_persistent_governor_request_approval(db_session: Session):
    """Verifies request_approval properly persists SecurityAuditRecord in database."""
    gov = SecurityGovernor(strict_mode=True, session=db_session)

    details = {"amount_usd": 25000.0, "currency": "USD", "memo": "Server expansion"}
    req_id = gov.request_approval(ActionType.FINANCIAL_TRANSFER, details)
    assert req_id is not None

    # Query database directly to confirm audit record persistence
    record = db_session.exec(
        select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
    ).first()

    assert record is not None
    assert record.id is not None
    assert record.request_id == req_id
    assert record.action_type == ActionType.FINANCIAL_TRANSFER.value
    assert json.loads(record.details_json) == details
    assert record.status == ApprovalStatus.PENDING.value
    assert record.approver is None
    assert record.created_at > 0
    assert record.resolved_at is None


def test_persistent_governor_grant_approval(db_session: Session):
    """Verifies grant_approval updates persistent audit record with approver and resolved_at."""
    gov = SecurityGovernor(strict_mode=True, session=db_session)

    req_id = gov.request_approval(
        ActionType.LIVE_TRADE_ORDER,
        {"symbol": "BTC/USD", "amount": 1.5}
    )

    t_before = time.time()
    success = gov.grant_approval(req_id, approver="alice_chief_risk_officer")
    t_after = time.time()

    assert success is True

    # Verify database state
    record = db_session.exec(
        select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
    ).first()

    assert record is not None
    assert record.status == ApprovalStatus.APPROVED.value
    assert record.approver == "alice_chief_risk_officer"
    assert record.resolved_at is not None
    assert t_before <= record.resolved_at <= t_after

    # Default approver fallback
    req_id2 = gov.request_approval(ActionType.OUTBOUND_COMMUNICATION, {"msg": "hello"})
    gov.grant_approval(req_id2)
    record2 = db_session.exec(
        select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id2)
    ).first()
    assert record2.approver == "human_operator"


def test_persistent_governor_reject_approval(db_session: Session):
    """Verifies reject_approval updates persistent audit record status to REJECTED."""
    gov = SecurityGovernor(strict_mode=True, session=db_session)

    req_id = gov.request_approval(
        ActionType.FINANCIAL_TRANSFER,
        {"amount_usd": 1000000.0, "recipient": "UNKNOWN_ENT"}
    )

    t_before = time.time()
    success = gov.reject_approval(req_id)
    t_after = time.time()

    assert success is True

    record = db_session.exec(
        select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
    ).first()

    assert record is not None
    assert record.status == ApprovalStatus.REJECTED.value
    assert record.approver is None
    assert record.resolved_at is not None
    assert t_before <= record.resolved_at <= t_after


def test_persistent_governor_is_permitted(db_session: Session):
    """Verifies is_permitted evaluates correctly across memory and database layers."""
    gov1 = SecurityGovernor(strict_mode=True, session=db_session)

    # 1. Non-gated action is always permitted
    assert gov1.is_permitted(ActionType.API_EXPENDITURE) is True

    # 2. Gated action without request is denied
    assert gov1.is_permitted(ActionType.FINANCIAL_TRANSFER) is False

    # 3. Gated action with pending request is denied
    req_approved = gov1.request_approval(ActionType.FINANCIAL_TRANSFER, {"amount": 500})
    req_rejected = gov1.request_approval(ActionType.LIVE_TRADE_ORDER, {"symbol": "ETH"})
    assert gov1.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_approved) is False
    assert gov1.is_permitted(ActionType.LIVE_TRADE_ORDER, req_id=req_rejected) is False

    # 4. Resolve requests
    gov1.grant_approval(req_approved, approver="risk_engine")
    gov1.reject_approval(req_rejected)

    assert gov1.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_approved) is True
    assert gov1.is_permitted(ActionType.LIVE_TRADE_ORDER, req_id=req_rejected) is False

    # 5. Cross-instance persistence: a new governor sharing the database session
    # must recognize the approved request without having it in in-memory dict!
    gov2 = SecurityGovernor(strict_mode=True, session=db_session)
    assert req_approved not in gov2._approvals  # empty memory cache
    assert gov2.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_approved) is True
    assert gov2.is_permitted(ActionType.LIVE_TRADE_ORDER, req_id=req_rejected) is False


def test_persistent_governor_get_audit_records(db_session: Session):
    """Verifies get_audit_records returns correctly sorted and serialized records."""
    gov = SecurityGovernor(strict_mode=True, session=db_session)

    # Create 3 records with small time intervals
    req1 = gov.request_approval(ActionType.FINANCIAL_TRANSFER, {"id": 1})
    time.sleep(0.01)
    req2 = gov.request_approval(ActionType.LIVE_TRADE_ORDER, {"id": 2})
    time.sleep(0.01)
    req3 = gov.request_approval(ActionType.OUTBOUND_COMMUNICATION, {"id": 3})

    gov.grant_approval(req1, approver="lead_1")
    gov.reject_approval(req2)

    # Limit = 2
    records_limit2 = gov.get_audit_records(limit=2)
    assert len(records_limit2) == 2
    # Verify order is descending by created_at
    assert records_limit2[0]["request_id"] == req3
    assert records_limit2[1]["request_id"] == req2
    assert records_limit2[0]["created_at"] >= records_limit2[1]["created_at"]

    # All records
    all_records = gov.get_audit_records(limit=50)
    assert len(all_records) == 3
    assert all_records[0]["request_id"] == req3
    assert all_records[1]["request_id"] == req2
    assert all_records[2]["request_id"] == req1

    # Verify dictionary shape
    for r in all_records:
        assert isinstance(r["id"], int)
        assert isinstance(r["request_id"], str)
        assert isinstance(r["action_type"], str)
        assert isinstance(r["details_json"], str)
        assert isinstance(r["status"], str)
        assert isinstance(r["created_at"], float)


def test_persistent_governor_edge_cases(db_session: Session):
    """Verifies edge cases: unknown IDs, string action types, None details, HMAC signing."""
    gov = SecurityGovernor(strict_mode=True, session=db_session)

    # Non-existent approval grants/rejections
    assert gov.grant_approval("nonexistent-uuid") is False
    assert gov.reject_approval("nonexistent-uuid") is False

    # String action type and None details
    req_id = gov.request_approval("custom_maintenance_action", None)
    assert req_id is not None
    rec = db_session.exec(
        select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
    ).first()
    assert rec is not None
    assert rec.action_type == "custom_maintenance_action"
    assert rec.details_json == "{}"

    # HMAC signature verification with persistent DB
    secret_key = "sovereign_secret"
    req_hmac = gov.request_approval(ActionType.FINANCIAL_TRANSFER, {"amount": 99000.0})
    sig = gov.generate_signature(req_hmac, secret_key)
    assert len(sig) == 64

    # Verify from another governor instance sharing the session
    gov_remote = SecurityGovernor(strict_mode=True, session=db_session)
    granted = gov_remote.verify_and_grant_signature(req_hmac, sig, secret_key)
    assert granted is True
    assert gov_remote.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_hmac) is True
