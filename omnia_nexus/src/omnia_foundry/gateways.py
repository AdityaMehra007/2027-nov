"""
PROJECT OMNIA NEXUS: Consequential Action Gateway & Unit Economics Telemetry
Enforces cryptographically signed approval tokens before high-risk execution,
and tracks compute costs and execution latencies across all 24 Venture Studios.
"""
from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict

class ConsequentialActionError(PermissionError):
    """Raised when an action requires approval but has not been signed."""
    pass

@dataclass
class ConsequentialActionGateway:
    signed_approvals: Dict[str, dict[str, Any]] = field(default_factory=dict)

    def register_approval(self, action_id: str, approver: str, reason: str) -> str:
        token = hashlib.sha256(f"{action_id}:{approver}:{time.time()}".encode("utf-8")).hexdigest()
        self.signed_approvals[action_id] = {
            "token": token,
            "approver": approver,
            "reason": reason,
            "timestamp": time.time()
        }
        return token

    def verify_and_execute(self, action_id: str, is_restricted: bool, token: str | None = None) -> bool:
        if not is_restricted:
            return True # Safe actions proceed
        if not token or action_id not in self.signed_approvals:
            raise ConsequentialActionError(f"Action '{action_id}' is restricted and requires verified approval.")
        approval = self.signed_approvals[action_id]
        if approval["token"] != token:
            raise ConsequentialActionError("Invalid approval token presented.")
        return True

@dataclass
class TelemetryCollector:
    metrics: list[dict[str, Any]] = field(default_factory=list)

    def record_operation(self, studio_id: str, operation: str, duration_ms: float, compute_units: float = 1.0):
        cost_usd = compute_units * 0.00002 # Model pricing rate
        entry = {
            "studio_id": studio_id,
            "operation": operation,
            "duration_ms": duration_ms,
            "compute_units": compute_units,
            "cost_usd": cost_usd,
            "timestamp": time.time()
        }
        self.metrics.append(entry)

    def studio_cost_breakdown(self) -> dict[str, float]:
        costs: dict[str, float] = {}
        for m in self.metrics:
            sid = m["studio_id"]
            costs[sid] = costs.get(sid, 0.0) + m["cost_usd"]
        return {k: round(v, 6) for k, v in costs.items()}
