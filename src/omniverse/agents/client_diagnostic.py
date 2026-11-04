"""Client Diagnostic Agent: Audits digital infrastructure, detects bottlenecks, and quantifies revenue loss."""

from __future__ import annotations

from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.world_clients import WorldClientDirectory


class ClientDiagnosticAgent(BaseAgent):
    """Autonomous agent that evaluates technical and commercial bottlenecks for global companies."""

    def __init__(self, directory: WorldClientDirectory = None):
        self.directory = directory or WorldClientDirectory()

    @property
    def role_name(self) -> str:
        return "ClientDiagnostic"

    @property
    def division(self) -> str:
        return "Audit"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name")
        client = None

        if client_name:
            client = self.directory.get_client_by_name(client_name)

        if not client:
            # Fallback to direct client dict in payload if passed
            raw_client = payload.get("client_data")
            if raw_client:
                client_name = raw_client.get("name", "Target Prospect")
                revenue = float(raw_client.get("annual_revenue_usd", 1_000_000.0))
                tech_stack = raw_client.get("tech_stack", ["Python", "React"])
                needs = raw_client.get("declared_needs", ["Modern API", "Client Portal"])
            else:
                return {"status": "ERROR", "message": f"Client '{client_name}' not found."}
        else:
            client_name = client.name
            revenue = client.annual_revenue_usd
            tech_stack = client.tech_stack
            needs = client.declared_needs

        # Calculate heuristic audit scores
        tech_count = len(tech_stack)
        perf_score = min(95.0, max(40.0, 50.0 + (tech_count * 7.5)))
        seo_score = 65.0
        conversion_score = 55.0

        estimated_monthly_loss = round((revenue * 0.08) / 12.0, 2)

        diagnosis = {
            "client_name": client_name,
            "performance_score": perf_score,
            "seo_score": seo_score,
            "conversion_score": conversion_score,
            "overall_health": round((perf_score + seo_score + conversion_score) / 3.0, 1),
            "estimated_monthly_loss_usd": estimated_monthly_loss,
            "primary_bottlenecks": needs,
            "recommended_archetype": "FULL_TRANSFORMATION",
        }

        global_event_bus.publish("CLIENT_DIAGNOSIS_COMPLETED", {
            "client": client_name,
            "health_score": diagnosis["overall_health"],
            "monthly_loss_usd": estimated_monthly_loss,
        })

        return {
            "status": "SUCCESS",
            "diagnosis": diagnosis,
        }
