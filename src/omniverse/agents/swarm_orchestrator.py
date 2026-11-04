"""Supreme Swarm Orchestrator: Multi-agent coordination matrix executing end-to-end global builds."""

from __future__ import annotations

import time
from typing import Dict, Any, List, Optional
from omniverse.agents.base import AgentTask, AgentDispatcher
from omniverse.agents.global_prospector import GlobalProspectorAgent
from omniverse.agents.client_diagnostic import ClientDiagnosticAgent
from omniverse.agents.solution_architect import UniversalSolutionArchitectAgent
from omniverse.agents.code_forge_agent import AutonomousCodeForgeAgent
from omniverse.agents.agent_engineer_agent import AutonomousAgentEngineerAgent
from omniverse.agents.growth_marketing_agent import GrowthMarketingAgent
from omniverse.agents.commercial_closer import CommercialDealCloserAgent
from omniverse.agents.treasury_reconciler import TreasuryReconciliationAgent

from omniverse.modules.agency.world_clients import (
    GlobalHub,
    IndustrySector,
    WorldClient,
    WorldClientDirectory,
)
from omniverse.modules.agency.fulfillment.forge_pipeline import UniversalForgePipeline, ForgedPackage
from omniverse.core.telemetry import global_event_bus


class SupremeSwarmOrchestrator:
    """Master conductor of the 8-agent autonomous workforce and Universal Forge."""

    def __init__(
        self,
        directory: Optional[WorldClientDirectory] = None,
        build_root: str = "artifacts/world_builds",
    ):
        self.directory = directory or WorldClientDirectory()
        self.pipeline = UniversalForgePipeline(root_build_dir=build_root)
        self.dispatcher = AgentDispatcher()

        # Initialize and register the 8 specialized agents
        self.prospector = GlobalProspectorAgent(self.directory)
        self.diagnostic = ClientDiagnosticAgent(self.directory)
        self.architect = UniversalSolutionArchitectAgent()
        self.code_forge = AutonomousCodeForgeAgent(output_root=f"{build_root}/code")
        self.agent_engineer = AutonomousAgentEngineerAgent(output_root=f"{build_root}/agents")
        self.growth_marketing = GrowthMarketingAgent(output_root=f"{build_root}/marketing")
        self.closer = CommercialDealCloserAgent()
        self.treasury = TreasuryReconciliationAgent()

        self.dispatcher.register(self.prospector)
        self.dispatcher.register(self.diagnostic)
        self.dispatcher.register(self.architect)
        self.dispatcher.register(self.code_forge)
        self.dispatcher.register(self.agent_engineer)
        self.dispatcher.register(self.growth_marketing)
        self.dispatcher.register(self.closer)
        self.dispatcher.register(self.treasury)

    def list_fleet(self) -> Dict[str, str]:
        """Returns the registered fleet and their functional divisions."""
        return self.dispatcher.list_agents()

    def run_pipeline_for_client(
        self,
        client: WorldClient,
        contract_value_usd: float = 15000.0,
        reconcile: bool = True,
    ) -> Dict[str, Any]:
        """Executes full 6-phase autonomous cycle for a given world client."""
        start_time = time.time()
        client_name = client.name

        # Phase 1: Client Diagnostic
        diag_res = self.diagnostic.execute_task(AgentTask(
            task_type="AUDIT_CLIENT",
            payload={"client_name": client_name},
        ))
        diagnosis = diag_res.get("diagnosis", {})

        # Phase 2: Solution Architecture Blueprint
        arch_res = self.architect.execute_task(AgentTask(
            task_type="BLUEPRINT_SOLUTION",
            payload={"client_name": client_name, "diagnosis": diagnosis},
        ))
        blueprint = arch_res.get("blueprint", {})

        # Phase 3: Universal Code, Agent & Marketing Forge
        forged_package: ForgedPackage = self.pipeline.build_everything_for_client(
            client=client,
            budget_usd=contract_value_usd,
        )

        # Phase 4: Commercial Proposal & One-Click Payment Formulation
        closer_res = self.closer.execute_task(AgentTask(
            task_type="GENERATE_COMMERCIAL_OFFER",
            payload={
                "client_name": client_name,
                "hub": client.hub.value,
                "price_usd": contract_value_usd,
                "demo_url": f"https://demo.omniverse.io/client/{client.client_id}",
            },
        ))
        proposal = closer_res.get("proposal", {})

        # Phase 5: Treasury Reconciliation (if auto-reconcile enabled)
        settlement_info = None
        if reconcile:
            settle_res = self.treasury.execute_task(AgentTask(
                task_type="RECONCILE_PAYMENT",
                payload={
                    "client_name": client_name,
                    "amount_usd": contract_value_usd,
                    "deliverables": [d.model_dump() for d in forged_package.all_deliverables],
                },
            ))
            settlement_info = settle_res

        duration = time.time() - start_time

        global_event_bus.publish("SWARM_BUILD_CYCLE_COMPLETED", {
            "client": client_name,
            "hub": client.hub.value,
            "total_artifacts": forged_package.total_files,
            "total_bytes": forged_package.total_bytes,
            "duration_sec": duration,
        })

        return {
            "status": "SUCCESS",
            "client": client.model_dump(),
            "diagnosis": diagnosis,
            "blueprint": blueprint,
            "forged_package": forged_package.model_dump(),
            "commercial_proposal": proposal,
            "settlement": settlement_info,
            "duration_sec": round(duration, 3),
        }

    def run_global_cohort(
        self,
        hub: Optional[GlobalHub] = None,
        sector: Optional[IndustrySector] = None,
        limit: int = 3,
        contract_value_usd: float = 15000.0,
    ) -> Dict[str, Any]:
        """Runs the entire autonomous swarm across an international cohort."""
        cohort = self.directory.filter_clients(hub=hub, sector=sector)[:limit]
        results = []
        total_revenue_settled = 0.0
        total_artifacts_generated = 0

        for client in cohort:
            res = self.run_pipeline_for_client(
                client=client,
                contract_value_usd=contract_value_usd,
                reconcile=True,
            )
            results.append(res)
            total_revenue_settled += contract_value_usd
            total_artifacts_generated += res["forged_package"]["total_files"]

        return {
            "status": "SUCCESS",
            "processed_count": len(results),
            "hub_filter": hub.value if hub else "ALL",
            "sector_filter": sector.value if sector else "ALL",
            "total_revenue_settled_usd": total_revenue_settled,
            "total_artifacts_generated": total_artifacts_generated,
            "cohort_results": results,
        }
