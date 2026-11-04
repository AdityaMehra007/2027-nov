import uuid
from enum import Enum
from typing import Dict, Any, Optional

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
    """Hard-gated security governor enforcing human-in-the-loop approvals

    and financial safety limits.
    """

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
        self._approvals[req_id] = {
            "action_type": action_type,
            "details": details or {},
            "status": ApprovalStatus.PENDING
        }
        return req_id

    def grant_approval(self, req_id: str) -> bool:
        """Grants human approval for a specific request ID."""
        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.APPROVED
            return True
        return False

    def reject_approval(self, req_id: str) -> bool:
        """Rejects a specific request ID."""
        if req_id in self._approvals:
            self._approvals[req_id]["status"] = ApprovalStatus.REJECTED
            return True
        return False

    def is_permitted(self, action_type: ActionType, req_id: Optional[str] = None) -> bool:
        """Verifies if an action is allowed to execute."""
        status = self.check_action(action_type)
        if status == ApprovalStatus.APPROVED:
            return True
        if req_id and req_id in self._approvals:
            return self._approvals[req_id]["status"] == ApprovalStatus.APPROVED
        return False
