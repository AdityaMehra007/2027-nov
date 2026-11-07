from __future__ import annotations
from dataclasses import dataclass
from .models import ActionClass

class PolicyDenied(PermissionError):
    """Raised when an action does not satisfy the local policy."""

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    requires_approval: bool

class PolicyEngine:
    """Default-deny policy for the local prototype.

    This is an application-level control, not a hardened security boundary.
    """
    def evaluate(self, action_class: str, approved: bool = False) -> PolicyDecision:
        try:
            klass = ActionClass(action_class)
        except ValueError:
            return PolicyDecision(False, "Unknown action class: default deny", False)

        if klass == ActionClass.RESTRICTED:
            return PolicyDecision(False, "Restricted actions are not executable by this prototype", True)
        if klass == ActionClass.APPROVAL_REQUIRED and not approved:
            return PolicyDecision(False, "Explicit approval is required", True)
        return PolicyDecision(True, "Allowed within local prototype policy", False)

    def enforce(self, action_class: str, approved: bool = False) -> None:
        decision = self.evaluate(action_class, approved)
        if not decision.allowed:
            raise PolicyDenied(decision.reason)
