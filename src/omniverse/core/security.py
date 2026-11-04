import uuid
import hmac
import hashlib
import time
from enum import Enum
from typing import Dict, Any, Optional, Tuple

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

class SecurityGovernor:
    """Hard-gated security governor enforcing human-in-the-loop approvals,

    air-gapped HMAC-SHA256 cryptographic signatures, and financial safety limits.
    """

    CAPITAL_THRESHOLD_USD: float = 10000.0

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self._approvals: Dict[str, Dict[str, Any]] = {}

    def check_action(self, action_type: ActionType, details: Optional[Dict[str, Any]] = None) -> ApprovalStatus:
        """Determines whether an action is permitted immediately or requires human consent."""
        if not self.strict_mode:
            return ApprovalStatus.APPROVED
            
        # Hard gates: Any capital movement, live trading, or outbound sending requires explicit approval
        if action_type in (ActionType.FINANCIAL_TRANSFER, ActionType.LIVE_TRADE_ORDER, ActionType.OUTBOUND_COMMUNICATION):
            return ApprovalStatus.REQUIRES_APPROVAL
            
        return ApprovalStatus.APPROVED

    def request_approval(self, action_type: ActionType, details: Optional[Dict[str, Any]] = None) -> str:
        """Registers a pending approval request and returns a tracking request ID."""
        req_id = str(uuid.uuid4())
        created_at = time.time()
        self._approvals[req_id] = {
            "action_type": action_type,
            "details": details or {},
            "status": ApprovalStatus.PENDING,
            "created_at": created_at
        }
        return req_id

    def get_pending_requests(self) -> Dict[str, Dict[str, Any]]:
        """Returns all pending approval requests."""
        return {
            k: v for k, v in self._approvals.items()
            if v.get("status") == ApprovalStatus.PENDING
        }

    def generate_signature(self, req_id: str, secret_key: str) -> str:
        """Computes a deterministic cryptographic HMAC-SHA256 signature for a pending request."""
        req_info = self._approvals.get(req_id, {})
        action_type = req_info.get("action_type", "")
        created_at = req_info.get("created_at", 0.0)
        canonical = f"{req_id}:{action_type}:{created_at}".encode("utf-8")
        return hmac.new(secret_key.encode("utf-8"), canonical, hashlib.sha256).hexdigest()

    def verify_and_grant_signature(self, req_id: str, signature: str, secret_key: str) -> bool:
        """Verifies an HMAC-SHA256 cryptographic signature and grants approval if valid."""
        if req_id not in self._approvals:
            return False
        if self._approvals[req_id]["status"] != ApprovalStatus.PENDING:
            return False

        expected_sig = self.generate_signature(req_id, secret_key)
        if not hmac.compare_digest(expected_sig, signature):
            return False

        self._approvals[req_id]["status"] = ApprovalStatus.APPROVED
        self._approvals[req_id]["approved_at"] = time.time()
        return True

    def grant_approval(self, req_id: str) -> bool:
        """Grants human approval for a specific request ID."""
        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.APPROVED
            self._approvals[req_id]["approved_at"] = time.time()
            return True
        return False

    def reject_approval(self, req_id: str) -> bool:
        """Rejects a specific request ID."""
        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.REJECTED
            self._approvals[req_id]["rejected_at"] = time.time()
            return True
        return False

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
            return self._approvals[req_id]["status"] == ApprovalStatus.APPROVED
        return False
