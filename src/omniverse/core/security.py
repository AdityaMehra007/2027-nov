import uuid
import hmac
import hashlib
import json
import time
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List
from sqlmodel import SQLModel, Field, Session, select

class ActionType(str, Enum):
    OUTBOUND_COMMUNICATION = "outbound_communication"
    FINANCIAL_TRANSFER = "financial_transfer"
    API_EXPENDITURE = "api_expenditure"
    LIVE_TRADE_ORDER = "live_trade_order"
    DATABASE_MIGRATION = "database_migration"

class ApprovalStatus(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    REQUIRES_APPROVAL = "requires_approval"

class SecurityAuditRecord(SQLModel, table=True):
    __tablename__ = "security_audit_records"
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: str = Field(index=True, unique=True)
    action_type: str
    details_json: str = Field(default="{}")
    status: str = Field(default="pending")
    approver: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    resolved_at: Optional[float] = None

class SecurityGovernor:
    """Hard-gated security governor enforcing human-in-the-loop approvals,
    air-gapped HMAC-SHA256 cryptographic signatures, persistent audit trails, and financial safety limits.
    """

    CAPITAL_THRESHOLD_USD: float = 10000.0

    def __init__(self, strict_mode: bool = True, session: Optional[Session] = None):
        self.strict_mode = strict_mode
        self.session = session
        self._approvals: Dict[str, Dict[str, Any]] = {}

    def check_action(self, action_type: ActionType, details: Optional[Dict[str, Any]] = None) -> ApprovalStatus:
        """Determines whether an action is permitted immediately or requires human consent."""
        if not self.strict_mode:
            return ApprovalStatus.APPROVED
            
        # Hard gates: Any capital movement, live trading, or outbound sending requires explicit approval
        if action_type in (ActionType.FINANCIAL_TRANSFER, ActionType.LIVE_TRADE_ORDER, ActionType.OUTBOUND_COMMUNICATION):
            return ApprovalStatus.REQUIRES_APPROVAL
            
        return ApprovalStatus.APPROVED

    def request_approval(self, action_type: ActionType | str, details: Optional[Dict[str, Any]] = None) -> str:
        """Registers a pending approval request and returns a tracking request ID."""
        req_id = str(uuid.uuid4())
        created_at = time.time()
        act_str = action_type.value if hasattr(action_type, "value") else str(action_type)
        details_map = details or {}
        details_json_str = json.dumps(details_map)

        self._approvals[req_id] = {
            "id": None,
            "request_id": req_id,
            "action_type": action_type,
            "details": details_map,
            "details_json": details_json_str,
            "status": ApprovalStatus.PENDING,
            "created_at": created_at,
            "approver": None,
            "resolved_at": None,
        }

        if self.session is not None:
            audit_record = SecurityAuditRecord(
                request_id=req_id,
                action_type=act_str,
                details_json=details_json_str,
                status=ApprovalStatus.PENDING.value,
                created_at=created_at,
            )
            self.session.add(audit_record)
            self.session.commit()
            if audit_record.id is not None:
                self._approvals[req_id]["id"] = audit_record.id

        return req_id

    def get_pending_requests(self) -> Dict[str, Dict[str, Any]]:
        """Returns all pending approval requests."""
        pending = {
            k: v for k, v in self._approvals.items()
            if v.get("status") == ApprovalStatus.PENDING
        }
        if self.session is not None:
            statement = select(SecurityAuditRecord).where(
                SecurityAuditRecord.status == ApprovalStatus.PENDING.value
            )
            records = self.session.exec(statement).all()
            for rec in records:
                if rec.request_id not in pending:
                    try:
                        details_map = json.loads(rec.details_json)
                    except Exception:
                        details_map = {}
                    pending[rec.request_id] = {
                        "id": rec.id,
                        "request_id": rec.request_id,
                        "action_type": rec.action_type,
                        "details": details_map,
                        "details_json": rec.details_json,
                        "status": ApprovalStatus.PENDING,
                        "created_at": rec.created_at,
                        "approver": rec.approver,
                        "resolved_at": rec.resolved_at,
                    }
        return pending

    def generate_signature(self, req_id: str, secret_key: str) -> str:
        """Computes a deterministic cryptographic HMAC-SHA256 signature for a pending request."""
        req_info = self._approvals.get(req_id)
        if not req_info and self.session is not None:
            record = self.session.exec(
                select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
            ).first()
            if record:
                try:
                    act_enum = ActionType(record.action_type)
                except Exception:
                    act_enum = record.action_type
                req_info = {
                    "action_type": act_enum,
                    "created_at": record.created_at,
                }
        if not req_info:
            req_info = {}
        action_type = req_info.get("action_type", "")
        created_at = req_info.get("created_at", 0.0)
        canonical = f"{req_id}:{action_type}:{created_at}".encode("utf-8")
        return hmac.new(secret_key.encode("utf-8"), canonical, hashlib.sha256).hexdigest()

    def verify_and_grant_signature(self, req_id: str, signature: str, secret_key: str) -> bool:
        """Verifies an HMAC-SHA256 cryptographic signature and grants approval if valid."""
        is_pending = False
        if req_id in self._approvals and self._approvals[req_id]["status"] == ApprovalStatus.PENDING:
            is_pending = True
        elif self.session is not None:
            record = self.session.exec(
                select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
            ).first()
            if record and record.status == ApprovalStatus.PENDING.value:
                is_pending = True

        if not is_pending:
            return False

        expected_sig = self.generate_signature(req_id, secret_key)
        if not hmac.compare_digest(expected_sig, signature):
            return False

        return self.grant_approval(req_id, approver="hmac_signature")

    def grant_approval(self, req_id: str, approver: str = "human_operator") -> bool:
        """Grants human approval for a specific request ID."""
        now = time.time()
        found = False

        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.APPROVED
            self._approvals[req_id]["approved_at"] = now
            self._approvals[req_id]["resolved_at"] = now
            self._approvals[req_id]["approver"] = approver
            found = True

        if self.session is not None:
            statement = select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
            record = self.session.exec(statement).first()
            if record is not None:
                record.status = ApprovalStatus.APPROVED.value
                record.approver = approver
                record.resolved_at = now
                self.session.add(record)
                self.session.commit()
                found = True

        return found

    def reject_approval(self, req_id: str) -> bool:
        """Rejects a specific request ID."""
        now = time.time()
        found = False

        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.REJECTED
            self._approvals[req_id]["rejected_at"] = now
            self._approvals[req_id]["resolved_at"] = now
            found = True

        if self.session is not None:
            statement = select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
            record = self.session.exec(statement).first()
            if record is not None:
                record.status = ApprovalStatus.REJECTED.value
                record.resolved_at = now
                self.session.add(record)
                self.session.commit()
                found = True

        return found

    def get_audit_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves audit trail records from database or in-memory cache."""
        if self.session is not None:
            statement = (
                select(SecurityAuditRecord)
                .order_by(SecurityAuditRecord.created_at.desc())
                .limit(limit)
            )
            records = self.session.exec(statement).all()
            return [
                r.model_dump() if hasattr(r, "model_dump") else r.dict()
                for r in records
            ]

        results: List[Dict[str, Any]] = []
        sorted_approvals = sorted(
            self._approvals.values(),
            key=lambda x: x.get("created_at", 0.0),
            reverse=True,
        )
        for data in sorted_approvals[:limit]:
            status_val = data.get("status")
            if hasattr(status_val, "value"):
                status_val = status_val.value
            act_type = data.get("action_type")
            if hasattr(act_type, "value"):
                act_type = act_type.value
            results.append({
                "id": data.get("id"),
                "request_id": data.get("request_id"),
                "action_type": str(act_type) if act_type is not None else "",
                "details_json": data.get("details_json", json.dumps(data.get("details", {}))),
                "status": str(status_val) if status_val is not None else "",
                "approver": data.get("approver"),
                "created_at": data.get("created_at", 0.0),
                "resolved_at": data.get("resolved_at"),
            })
        return results

    def intercept_action(
        self,
        action_type: ActionType,
        details: Optional[Dict[str, Any]] = None,
        amount_usd: float = 0.0
    ) -> Tuple[bool, Optional[str]]:
        """Evaluates whether an action can execute immediately or must be intercepted into air-gap."""
        if not self.strict_mode:
            return True, None

        if amount_usd > self.CAPITAL_THRESHOLD_USD or action_type in (
            ActionType.FINANCIAL_TRANSFER,
            ActionType.LIVE_TRADE_ORDER,
            ActionType.OUTBOUND_COMMUNICATION
        ):
            req_id = self.request_approval(action_type, details)
            return False, req_id

        return True, None

    def is_permitted(self, action_type: ActionType, req_id: Optional[str] = None) -> bool:
        """Verifies if an action is allowed to execute."""
        status = self.check_action(action_type)
        if status == ApprovalStatus.APPROVED:
            return True
        if req_id and req_id in self._approvals:
            if self._approvals[req_id]["status"] == ApprovalStatus.APPROVED:
                return True
        if req_id and self.session is not None:
            statement = select(SecurityAuditRecord).where(SecurityAuditRecord.request_id == req_id)
            record = self.session.exec(statement).first()
            if record is not None and record.status == ApprovalStatus.APPROVED.value:
                return True
        return False
