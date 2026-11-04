"""Growth Marketing Agent: Synthesizes high-converting copy, SEO strategies, and email drip funnels."""

from __future__ import annotations

from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.fulfillment.marketing_factory import MarketingFactory
from omniverse.modules.agency.models import JobOrder, ServiceType, OrderStatus


class GrowthMarketingAgent(BaseAgent):
    """Autonomous marketing strategist and asset production agent."""

    def __init__(self, output_root: str = "artifacts/world_builds/marketing"):
        self.factory = MarketingFactory(output_root=output_root)

    @property
    def role_name(self) -> str:
        return "GrowthMarketing"

    @property
    def division(self) -> str:
        return "Fulfillment"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name", "Target Client")
        client_id = payload.get("client_id", "wclient_demo")
        budget = float(payload.get("budget_usd", 8000.0))

        order = JobOrder(
            client_id=client_id,
            service_type=ServiceType.GROWTH_MARKETING,
            brief=f"Growth marketing pack and copy suite for {client_name}",
            budget_usd=budget,
            status=OrderStatus.BUILDING,
        )

        deliverables = self.factory.build_campaign(order)

        global_event_bus.publish("GROWTH_MARKETING_COMPLETED", {
            "client": client_name,
            "artifacts_count": len(deliverables),
        })

        return {
            "status": "SUCCESS",
            "artifacts_count": len(deliverables),
            "deliverables": [d.model_dump() for d in deliverables],
        }
