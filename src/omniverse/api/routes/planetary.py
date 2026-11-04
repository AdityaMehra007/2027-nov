from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from omniverse.modules.planetary_mesh import GlobalPlanetaryMesh, TelemetryPacket
from omniverse.modules.aether.telemetry_ingestion import SatelliteTelemetryHub
from omniverse.modules.settlement import GlobalClearingHouse, CurrencyCode
from omniverse.modules.research_lab import AutonomousResearchLab

class ConsensusRequest(BaseModel):
    proposal_id: str = "PROP-RISK-001"
    proposed_value: float = 85.5

class SettlementRequest(BaseModel):
    source_currency: str = "INR"
    target_currency: str = "USD"
    amount: float = 50000.0

class ResearchSynthesizeRequest(BaseModel):
    domain: str = "autonomous-planetary-resilience"
    baseline_metric: str = "Mean-Time-To-Consensus"
    proposed_mechanism: str = "Federated Byzantine Fault-Tolerant Edge Graphs"

def get_planetary_router() -> APIRouter:
    router = APIRouter(prefix="/planetary", tags=["Planetary Mesh & Settlement"])
    mesh = GlobalPlanetaryMesh()
    telemetry_hub = SatelliteTelemetryHub()
    clearing_house = GlobalClearingHouse()
    research_lab = AutonomousResearchLab()

    @router.get("/mesh/nodes")
    def list_mesh_nodes():
        nodes = mesh.list_nodes()
        return {
            "status": "ONLINE",
            "total_nodes": len(nodes),
            "nodes": [n.model_dump() for n in nodes]
        }

    @router.post("/mesh/consensus")
    def trigger_mesh_consensus(req: ConsensusRequest):
        res = mesh.reach_federated_consensus(
            proposal_id=req.proposal_id,
            proposed_value=req.proposed_value
        )
        return res

    @router.get("/satellite/telemetry")
    def get_satellite_telemetry():
        passes = telemetry_hub.simulate_satellite_passes()
        alert = telemetry_hub.generate_composite_hazard_alert(passes)
        return {
            "passes_recorded": len(passes),
            "passes": [p.model_dump() for p in passes],
            "composite_hazard_alert": alert
        }

    @router.post("/settlement/execute")
    def execute_settlement(req: SettlementRequest):
        src_curr = getattr(CurrencyCode, req.source_currency.upper(), CurrencyCode.INR)
        tgt_curr = getattr(CurrencyCode, req.target_currency.upper(), CurrencyCode.USD)
        tx = clearing_house.execute_atomic_settlement(
            sender_id="CLIENT-API-001",
            recipient_id="OMNIVERSE-TREASURY",
            source_currency=src_curr,
            target_currency=tgt_curr,
            source_amount=req.amount
        )
        return {
            "settlement": tx.model_dump(),
            "reserve_liquidity": clearing_house.get_liquidity_reserves()
        }

    @router.post("/research/synthesize")
    def synthesize_research(req: ResearchSynthesizeRequest):
        hyp = research_lab.formulate_hypothesis(
            domain=req.domain,
            baseline_metric=req.baseline_metric,
            proposed_mechanism=req.proposed_mechanism
        )
        paper = research_lab.generate_research_paper(
            hypothesis=hyp,
            title="Federated Autonomous Computational Fabrics for Planetary Resilience"
        )
        return {
            "hypothesis": hyp.model_dump(),
            "paper_draft": {
                "title": paper.title,
                "authors": paper.authors,
                "domain": paper.domain,
                "abstract": paper.abstract,
                "output_file": str(paper.output_file)
            }
        }

    return router
