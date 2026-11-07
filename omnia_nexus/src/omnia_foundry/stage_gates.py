"""
PROJECT OMNIA NEXUS: Venture Studio Stage-Gate Engine
Implements the 5-point rigorous stage-gate governance framework:
1. Customer Need Gate
2. Technical Feasibility Gate
3. Capital Class Allocation Gate (A/B/C/D)
4. Safety & Security Gate
5. Kill / Pivot Decision Gate
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional
import time

class CapitalClass(str, Enum):
    CLASS_A = "Class A (Software / Zero Marginal Cost)"
    CLASS_B = "Class B (Moderate Compute / Cloud Infrastructure)"
    CLASS_C = "Class C (Hardware Prototype / Field Pilots)"
    CLASS_D = "Class D (Heavy Physical Infrastructure / Frontier CapEx)"

class GateStatus(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WAIVED = "waived"

@dataclass
class StageGateEvaluation:
    studio_id: str
    studio_name: str
    evaluator: str
    customer_gate: GateStatus = GateStatus.PENDING
    customer_evidence_ids: List[str] = field(default_factory=list)
    feasibility_gate: GateStatus = GateStatus.PENDING
    feasibility_proof: Optional[str] = None
    capital_class: CapitalClass = CapitalClass.CLASS_A
    capital_approved: bool = False
    safety_gate: GateStatus = GateStatus.PENDING
    safety_controls: List[str] = field(default_factory=list)
    kill_criteria: str = "3 months without customer traction or failing feasibility gate"
    kill_decision: bool = False
    evaluated_at: float = field(default_factory=time.time)

    def is_cleared_for_advancement(self) -> bool:
        if self.kill_decision:
            return False
        return (
            self.customer_gate == GateStatus.PASSED and
            self.feasibility_gate == GateStatus.PASSED and
            self.capital_approved and
            self.safety_gate == GateStatus.PASSED
        )

    def summary(self) -> dict[str, Any]:
        return {
            "studio_id": self.studio_id,
            "studio_name": self.studio_name,
            "status": "APPROVED" if self.is_cleared_for_advancement() else "BLOCKED",
            "gates": {
                "customer": self.customer_gate.value,
                "feasibility": self.feasibility_gate.value,
                "capital": self.capital_class.value,
                "capital_approved": self.capital_approved,
                "safety": self.safety_gate.value,
            },
            "kill_decision": self.kill_decision,
            "evaluated_at": self.evaluated_at
        }
