from typing import List, Dict, Any
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.models import HazardType
from omniverse.core.database import get_engine
from omniverse.operations.health import HealthDiagnostics

class OmniverseMCPServer:
    """Model Context Protocol (MCP) tool provider exposing Omniverse

    capabilities to Antigravity and external agent harnesses.
    """

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "generate_growth_kit",
                "description": "Generate a localized SMB growth kit (social captions, hooks, WhatsApp store copy, and pitch).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "business_name": {"type": "string"},
                        "niche": {"type": "string"},
                        "city": {"type": "string", "default": "Bengaluru"}
                    },
                    "required": ["business_name", "niche"]
                }
            },
            {
                "name": "get_system_status",
                "description": "Inspect live system diagnostics, database health, disk availability, and memory usage.",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "evaluate_resilience_risk",
                "description": "Evaluate multi-hazard climate and disaster resilience vulnerability index for coordinates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lon": {"type": "number"},
                        "elevation_meters": {"type": "number", "default": 900.0},
                        "hazard": {"type": "string", "enum": ["FLOOD", "SEISMIC", "HEAT_STRESS", "STORM_SURGE"], "default": "FLOOD"}
                    },
                    "required": ["lat", "lon"]
                }
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "generate_growth_kit":
            gen = GrowthKitGenerator()
            kit = gen.generate(
                business_name=arguments["business_name"],
                niche=arguments["niche"],
                city=arguments.get("city", "Bengaluru")
            )
            return kit.model_dump()

        elif tool_name == "get_system_status":
            engine = get_engine()
            with engine.get_session() as session:
                diagnostics = HealthDiagnostics(session)
                return diagnostics.run_diagnostics()

        elif tool_name == "evaluate_resilience_risk":
            hazard_str = arguments.get("hazard", "FLOOD").upper()
            hazard = getattr(HazardType, hazard_str, HazardType.FLOOD)
            risk_engine = AetherRiskEngine()
            assessment = risk_engine.evaluate_location_risk(
                lat=float(arguments["lat"]),
                lon=float(arguments["lon"]),
                elevation_meters=float(arguments.get("elevation_meters", 900.0)),
                hazard_type=hazard
            )
            return assessment.model_dump()

        else:
            raise ValueError(f"Unknown MCP tool: {tool_name}")
