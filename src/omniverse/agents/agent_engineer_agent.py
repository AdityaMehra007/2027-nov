"""Autonomous Agent Engineer Agent: Builds custom conversational AI agents and MCP tool schemas."""

from __future__ import annotations

from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.fulfillment.automation_factory import AutomationFactory
from omniverse.modules.agency.models import JobOrder, ServiceType, OrderStatus


class AutonomousAgentEngineerAgent(BaseAgent):
    """Autonomous AI engineer that generates custom AI agents, MCP schemas, and bots for clients."""

    def __init__(self, output_root: str = "artifacts/world_builds/agents"):
        self.factory = AutomationFactory(output_root=output_root)

    @property
    def role_name(self) -> str:
        return "AgentEngineer"

    @property
    def division(self) -> str:
        return "Fulfillment"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name", "Target Client")
        client_id = payload.get("client_id", "wclient_demo")
        budget = float(payload.get("budget_usd", 10000.0))

        order = JobOrder(
            client_id=client_id,
            service_type=ServiceType.AGENT_AUTOMATION,
            brief=f"Bespoke AI agent runtime and MCP schema for {client_name}",
            budget_usd=budget,
            status=OrderStatus.BUILDING,
        )

        deliverables = self.factory.build_agent_bundle(order)

        global_event_bus.publish("AGENT_ENGINEERING_COMPLETED", {
            "client": client_name,
            "artifacts_count": len(deliverables),
        })

        return {
            "status": "SUCCESS",
            "artifacts_count": len(deliverables),
            "deliverables": [d.model_dump() for d in deliverables],
        }
