from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus

class QuantAnalyst(BaseAgent):
    """Evaluates quantitative models, risk envelopes, and statistical significance."""

    @property
    def role_name(self) -> str:
        return "QuantAnalyst"

    @property
    def division(self) -> str:
        return "Financial Intelligence"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        max_dd = payload.get("max_drawdown_pct", 0.0)
        sharpe = payload.get("sharpe_ratio", 0.0)

        # Risk parameters: Max drawdown must be under 20% and Sharpe > 1.0
        if max_dd <= 20.0 and sharpe >= 1.0:
            verdict = "APPROVED"
            notes = "Strategy satisfies institutional risk tolerances."
        else:
            verdict = "REJECTED"
            notes = f"Risk limits breached: MaxDD={max_dd}%, Sharpe={sharpe}"

        global_event_bus.publish("AGENT_TASK_EXECUTED", {
            "agent": self.role_name,
            "task_type": task.task_type
        })

        return {
            "agent": self.role_name,
            "division": self.division,
            "risk_verdict": verdict,
            "notes": notes,
            "status": "COMPLETED"
        }
