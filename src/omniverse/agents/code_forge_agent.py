"""Autonomous Code Forge Agent: Compiles production web services, databases, and APIs."""

from __future__ import annotations

from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory
from omniverse.modules.agency.models import JobOrder, ServiceType, OrderStatus


class AutonomousCodeForgeAgent(BaseAgent):
    """Autonomous engineering agent that manufactures fullstack codebases."""

    def __init__(self, output_root: str = "artifacts/world_builds/code"):
        self.factory = CodeFactory(output_root=output_root)

    @property
    def role_name(self) -> str:
        return "CodeForge"

    @property
    def division(self) -> str:
        return "Fulfillment"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name", "Target Client")
        client_id = payload.get("client_id", "wclient_demo")
        budget = float(payload.get("budget_usd", 15000.0))

        order = JobOrder(
            client_id=client_id,
            service_type=ServiceType.FULLSTACK_DEV,
            brief=f"Fullstack production code build for {client_name}",
            budget_usd=budget,
            status=OrderStatus.BUILDING,
        )

        deliverables = self.factory.build_project(order)

        global_event_bus.publish("CODE_FORGE_COMPLETED", {
            "client": client_name,
            "artifacts_count": len(deliverables),
        })

        return {
            "status": "SUCCESS",
            "artifacts_count": len(deliverables),
            "deliverables": [d.model_dump() for d in deliverables],
        }
