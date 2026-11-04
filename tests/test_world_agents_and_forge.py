import pytest
from omniverse.agents.base import AgentTask
from omniverse.agents.global_prospector import GlobalProspectorAgent
from omniverse.agents.client_diagnostic import ClientDiagnosticAgent
from omniverse.agents.solution_architect import UniversalSolutionArchitectAgent
from omniverse.agents.code_forge_agent import AutonomousCodeForgeAgent
from omniverse.agents.agent_engineer_agent import AutonomousAgentEngineerAgent
from omniverse.agents.growth_marketing_agent import GrowthMarketingAgent
from omniverse.agents.commercial_closer import CommercialDealCloserAgent
from omniverse.agents.treasury_reconciler import TreasuryReconciliationAgent
from omniverse.agents.swarm_orchestrator import SupremeSwarmOrchestrator

from omniverse.modules.agency.world_clients import (
    GlobalHub,
    IndustrySector,
    WorldClient,
    WorldClientDirectory,
)
from omniverse.modules.agency.fulfillment.forge_pipeline import UniversalForgePipeline


def test_global_prospector_agent():
    agent = GlobalProspectorAgent()
    assert agent.role_name == "GlobalProspector"
    assert agent.division == "Intelligence"

    # Discover task
    task = AgentTask(
        task_type="DISCOVER_GLOBAL_CLIENTS",
        payload={"hub": "SF_BAY_AREA", "limit": 2},
    )
    result = agent.execute_task(task)
    assert result["status"] == "SUCCESS"
    assert result["count"] == 2
    for c in result["clients"]:
        assert c["hub"] == "SF_BAY_AREA"

    # TAM analysis task
    tam_task = AgentTask(task_type="ANALYZE_MARKET_TAM", payload={})
    tam_res = agent.execute_task(tam_task)
    assert tam_res["status"] == "SUCCESS"
    assert tam_res["total_companies_tracked"] >= 24
    assert tam_res["total_annual_revenue_usd"] > 100_000_000.0


def test_client_diagnostic_agent():
    agent = ClientDiagnosticAgent()
    assert agent.role_name == "ClientDiagnostic"
    assert agent.division == "Audit"

    task = AgentTask(
        task_type="AUDIT_CLIENT",
        payload={"client_name": "Apex Neural Compute"},
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    diag = res["diagnosis"]
    assert diag["client_name"] == "Apex Neural Compute"
    assert diag["overall_health"] > 0.0
    assert diag["estimated_monthly_loss_usd"] > 0.0
    assert len(diag["primary_bottlenecks"]) >= 1


def test_universal_solution_architect_agent():
    agent = UniversalSolutionArchitectAgent()
    assert agent.role_name == "SolutionArchitect"
    assert agent.division == "Architecture"

    task = AgentTask(
        task_type="BLUEPRINT_SOLUTION",
        payload={
            "client_name": "Apex Neural Compute",
            "diagnosis": {"primary_bottlenecks": ["Automated multi-tenant billing"]},
        },
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    bp = res["blueprint"]
    assert "Apex Neural Compute" in bp["solution_name"]
    assert len(bp["architecture_modules"]) == 4


def test_autonomous_code_forge_agent(tmp_path):
    agent = AutonomousCodeForgeAgent(output_root=str(tmp_path / "code"))
    assert agent.role_name == "CodeForge"

    task = AgentTask(
        task_type="FORGE_FULLSTACK",
        payload={"client_name": "Apex Neural Compute", "budget_usd": 15000.0},
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    assert res["artifacts_count"] >= 3


def test_autonomous_agent_engineer_agent(tmp_path):
    agent = AutonomousAgentEngineerAgent(output_root=str(tmp_path / "agents"))
    assert agent.role_name == "AgentEngineer"

    task = AgentTask(
        task_type="FORGE_AGENT",
        payload={"client_name": "Apex Neural Compute", "budget_usd": 10000.0},
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    assert res["artifacts_count"] >= 3


def test_growth_marketing_agent(tmp_path):
    agent = GrowthMarketingAgent(output_root=str(tmp_path / "marketing"))
    assert agent.role_name == "GrowthMarketing"

    task = AgentTask(
        task_type="FORGE_CAMPAIGN",
        payload={"client_name": "Apex Neural Compute", "budget_usd": 8000.0},
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    assert res["artifacts_count"] >= 4


def test_commercial_deal_closer_agent():
    agent = CommercialDealCloserAgent()
    assert agent.role_name == "CommercialCloser"

    task = AgentTask(
        task_type="GENERATE_COMMERCIAL_OFFER",
        payload={"client_name": "Apex Neural Compute", "hub": "SF_BAY_AREA", "price_usd": 15000.0},
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    prop = res["proposal"]
    assert prop["client_name"] == "Apex Neural Compute"
    assert "stripe.com" in prop["checkout_payment_url"]
    assert "wa.me" in prop["whatsapp_direct_outreach"]


def test_treasury_reconciliation_agent():
    agent = TreasuryReconciliationAgent()
    assert agent.role_name == "TreasuryReconciler"

    task = AgentTask(
        task_type="RECONCILE_PAYMENT",
        payload={
            "client_name": "Apex Neural Compute",
            "amount_usd": 15000.0,
            "deliverables": [
                {"name": "main.py", "checksum": "a" * 64},
                {"name": "index.html", "checksum": "b" * 64},
            ],
        },
    )
    res = agent.execute_task(task)
    assert res["status"] == "SUCCESS"
    assert res["settled_amount_usd"] == 15000.0
    assert res["verified_deliverables_count"] == 2
    assert res["ledger_status"] == "RECONCILED"


def test_universal_forge_pipeline(tmp_path):
    directory = WorldClientDirectory()
    client = directory.get_client_by_name("Apex Neural Compute")
    assert client is not None

    pipeline = UniversalForgePipeline(root_build_dir=str(tmp_path / "world_builds"))
    package = pipeline.build_everything_for_client(client)

    assert package.client_name == "Apex Neural Compute"
    assert package.total_files >= 10
    assert package.total_bytes > 0
    assert package.qa_passed is True

    # Check that individual expected files were created
    artifact_names = {d.artifact_name for d in package.all_deliverables}
    assert "index.html" in artifact_names
    assert "main.py" in artifact_names
    assert "test_service.py" in artifact_names
    assert "Dockerfile" in artifact_names
    assert "agent_runtime.py" in artifact_names
    assert "mcp_tools.json" in artifact_names
    assert "sales_copy.md" in artifact_names


def test_supreme_swarm_orchestrator(tmp_path):
    directory = WorldClientDirectory()
    orchestrator = SupremeSwarmOrchestrator(
        directory=directory,
        build_root=str(tmp_path / "swarm_builds"),
    )

    fleet = orchestrator.list_fleet()
    assert len(fleet) >= 8
    expected_agents = {
        "GlobalProspector",
        "ClientDiagnostic",
        "SolutionArchitect",
        "CodeForge",
        "AgentEngineer",
        "GrowthMarketing",
        "CommercialCloser",
        "TreasuryReconciler",
    }
    assert expected_agents.issubset(set(fleet.keys()))

    # Run for single client
    client = directory.get_client_by_name("Gotham Liquidity Partners")
    assert client is not None

    result = orchestrator.run_pipeline_for_client(client, contract_value_usd=25000.0)
    assert result["status"] == "SUCCESS"
    assert result["diagnosis"]["overall_health"] > 0
    assert result["blueprint"]["solution_name"]
    assert result["forged_package"]["total_files"] >= 10
    assert result["settlement"]["ledger_status"] == "RECONCILED"
    assert result["duration_sec"] >= 0.0

    # Run global cohort
    cohort_result = orchestrator.run_global_cohort(
        hub=GlobalHub.LONDON,
        limit=2,
        contract_value_usd=18000.0,
    )
    assert cohort_result["status"] == "SUCCESS"
    assert cohort_result["processed_count"] == 2
    assert cohort_result["total_revenue_settled_usd"] == 36000.0
    assert cohort_result["total_artifacts_generated"] >= 20
