from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.core.security import SecurityGovernor, ActionType

class GovernanceOfficer(BaseAgent):
    """Chief Risk & Compliance Officer enforcing safety budgets and regulatory boundaries."""

    @property
    def role_name(self) -> str:
        return "GovernanceOfficer"

    @property
    def division(self) -> str:
        return "Governance & Risk"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        action_name = payload.get("action_type", "financial_transfer")
        governor = SecurityGovernor(strict_mode=True)
        
        action_type = getattr(ActionType, action_name.upper(), ActionType.FINANCIAL_TRANSFER)
        approval_status = governor.check_action(action_type, details=payload)

        global_event_bus.publish("AGENT_TASK_EXECUTED", {
            "agent": self.role_name,
            "task_type": task.task_type
        })

        return {
            "agent": self.role_name,
            "division": self.division,
            "action_evaluated": action_type.value,
            "approval_status": approval_status.value,
            "requires_human_signoff": approval_status.value == "requires_approval",
            "status": "COMPLETED"
        }
