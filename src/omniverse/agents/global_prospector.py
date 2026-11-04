"""Global Prospector Agent: Discovers, enriches, and structures international client rosters."""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.world_clients import (
    GlobalHub,
    IndustrySector,
    WorldClient,
    WorldClientDirectory,
)


class GlobalProspectorAgent(BaseAgent):
    """Autonomous agent that monitors global hubs and builds rich prospective client profiles."""

    def __init__(self, directory: Optional[WorldClientDirectory] = None):
        self.directory = directory or WorldClientDirectory()

    @property
    def role_name(self) -> str:
        return "GlobalProspector"

    @property
    def division(self) -> str:
        return "Intelligence"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        task_type = task.task_type
        payload = task.payload

        if task_type == "DISCOVER_GLOBAL_CLIENTS":
            hub_str = payload.get("hub")
            sector_str = payload.get("sector")
            min_rev = payload.get("min_revenue")
            limit = payload.get("limit", 10)

            hub = GlobalHub(hub_str) if hub_str else None
            sector = IndustrySector(sector_str) if sector_str else None

            clients = self.directory.filter_clients(
                hub=hub,
                sector=sector,
                min_revenue=min_rev,
            )[:limit]

            global_event_bus.publish("GLOBAL_PROSPECTS_DISCOVERED", {
                "count": len(clients),
                "hub": hub_str or "ALL",
                "sector": sector_str or "ALL",
            })

            return {
                "status": "SUCCESS",
                "count": len(clients),
                "clients": [c.model_dump() for c in clients],
            }

        elif task_type == "ANALYZE_MARKET_TAM":
            all_clients = self.directory.get_all_clients()
            total_rev = sum(c.annual_revenue_usd for c in all_clients)
            hubs_count = {}
            sectors_count = {}
            for c in all_clients:
                hubs_count[c.hub.value] = hubs_count.get(c.hub.value, 0) + 1
                sectors_count[c.sector.value] = sectors_count.get(c.sector.value, 0) + 1

            return {
                "status": "SUCCESS",
                "total_companies_tracked": len(all_clients),
                "total_annual_revenue_usd": total_rev,
                "hubs_distribution": hubs_count,
                "sectors_distribution": sectors_count,
            }

        else:
            return {
                "status": "ERROR",
                "message": f"Unsupported task_type: {task_type}",
            }
