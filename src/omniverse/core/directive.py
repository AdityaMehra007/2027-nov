from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class GlobalService:
    id: str
    name: str
    core: str
    description: str
    cli_command: str

@dataclass(frozen=True)
class AgentPersona:
    role: str
    division: str
    mandate: str
    bound: str

SERVICES: list[GlobalService] = [
    GlobalService("SVC-ALPHA-01", "Local SMB Autonomous Growth Kits", "ALPHA", "Automated audits, local SEO, and WhatsApp growth kits", "omniverse generate-kit"),
    GlobalService("SVC-ALPHA-02", "10-Unit Commerce Matrix", "ALPHA", "Multi-provider payment routing (Stripe/UPI/Web3/SEPA) with dual-ledger accounting", "omniverse commerce status"),
    GlobalService("SVC-ALPHA-03", "Autonomous Micro-SaaS Factory", "ALPHA", "Declarative vertical SaaS scaffolding, testing, and containerization", "omniverse saas build"),
    GlobalService("SVC-ALPHA-04", "Deterministic B2B Prospecting", "ALPHA", "Public registry scraping and decision-maker lead verification", "omniverse scan-prospects"),
    GlobalService("SVC-ALPHA-05", "Quantitative Risk & Portfolio Lab", "ALPHA", "Backtesting, Monte Carlo simulation, and VaR risk boundary checks", "omniverse backtest"),
    GlobalService("SVC-ALPHA-06", "Real-Time Market Volatility Radar", "ALPHA", "Cross-asset volatility tracking and paper trading execution", "omniverse market-radar"),
    GlobalService("SVC-BETA-07", "Aether Geospatial Multi-Hazard Radar", "BETA", "Planetary WGS84 hazard scoring for flood, seismic, cyclone, heat", "omniverse aether-risk"),
    GlobalService("SVC-BETA-08", "Satellite SAR & Telemetry Processing", "BETA", "Cloud-penetrating Earth observation analysis and disaster boundaries", "omniverse sar-process"),
    GlobalService("SVC-BETA-09", "Emergency Relief & Shelter Logistics", "BETA", "Linear-programming relief supply routing and shelter allocations", "omniverse aether-logistics"),
    GlobalService("SVC-BETA-10", "Critical Infrastructure Vulnerability", "BETA", "Single-point-of-failure modeling for power, water, and telecom", "omniverse infra-vuln"),
    GlobalService("SVC-BETA-11", "BFT Swarm Mesh Consensus", "BETA", "Byzantine fault tolerant P2P gossip mesh and actor consensus", "omniverse swarm status"),
    GlobalService("SVC-BETA-12", "Continuous Self-Healing Autonomic Ops", "BETA", "24/7 background worker daemons with automated circuit breakers", "omniverse ops heal"),
]

PERSONAS: list[AgentPersona] = [
    AgentPersona("Supreme Chief Architect", "Command", "Master governance and platform orchestration", "Human-in-the-loop ratification required for live production change"),
    AgentPersona("Commercial Agency Director", "Core Alpha", "Client acquisition, outreach funnels, revenue generation", "Cannot issue client invoices without settlement ledger confirmation"),
    AgentPersona("Quantitative & Financial Governor", "Core Alpha", "Algorithmic intelligence and risk envelope enforcement", "Maximum drawdown capped at 20.0%; cannot execute real orders without HITL_TOKEN"),
    AgentPersona("Aether Resilience Commander", "Core Beta", "Geospatial hazard modeling and relief distribution", "Open data outputs must adhere to verified scientific standard"),
    AgentPersona("Swarm Mesh Operator", "Core Beta", "P2P actor network monitoring and gossip transport", "Isolates malfunctioning swarm nodes automatically"),
    AgentPersona("Security & Cryptographic Arbiter", "Governance", "Air-gapped security, zero-trust tokens, audit trails", "Inviolable veto power over unauthenticated actions"),
    AgentPersona("Open-Source Standards Fellow", "Governance", "Test integrity, documentation quality, licensing compliance", "100% green test suite gatekeeper"),
]

class MasterDirectiveRegistry:
    @staticmethod
    def get_services() -> list[GlobalService]:
        return SERVICES

    @staticmethod
    def get_personas() -> list[AgentPersona]:
        return PERSONAS

    @staticmethod
    def get_service(service_id: str) -> GlobalService | None:
        for s in SERVICES:
            if s.id == service_id:
                return s
        return None

    @staticmethod
    def validate_integrity() -> dict[str, Any]:
        services = MasterDirectiveRegistry.get_services()
        personas = MasterDirectiveRegistry.get_personas()
        alpha = [s for s in services if s.core == "ALPHA"]
        beta = [s for s in services if s.core == "BETA"]
        valid = (len(services) == 12) and (len(alpha) == 6) and (len(beta) == 6) and (len(personas) == 7)
        return {
            "valid": valid,
            "total_services": len(services),
            "alpha_services": len(alpha),
            "beta_services": len(beta),
            "total_personas": len(personas),
        }
