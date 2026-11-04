from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus

class SalesDirector(BaseAgent):
    """Directs lead prospecting, high-conversion proposals, and customer closing."""

    @property
    def role_name(self) -> str:
        return "SalesDirector"

    @property
    def division(self) -> str:
        return "Commercial"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        biz_name = payload.get("business_name", "Target Prospect")
        est_val = payload.get("estimated_value_inr", 15000.0)

        strategy = (
            f"Offer sample demo first for {biz_name}. Deliver sample WhatsApp copy and 2 captions. "
            f"Close on upfront retainers of ₹{est_val:,.0f}."
        )

        global_event_bus.publish("AGENT_TASK_EXECUTED", {
            "agent": self.role_name,
            "task_type": task.task_type
        })

        return {
            "agent": self.role_name,
            "division": self.division,
            "pitch_strategy": strategy,
            "closing_cta": "Can I send over the sample kit for you to review? No obligation at all.",
            "status": "COMPLETED"
        }
