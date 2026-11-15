"""
Test suite for ATLAS NEXUS Phase III Frontier Missions:
- Model Gateway & Swarm Runtime (Mission 03)
- World Infrastructure & Cislunar Engine (Mission 06)
- Autonomous Workflows & Human-in-the-Loop (Mission 08)
- Evolution, Red-Teaming & Gap Analysis (Mission 10)
- Nexus CLI Interface
"""

import pytest
from src.nexus.engines.ai_gateway import (
    ModelGateway,
    ModelTier,
    SwarmRuntime,
    AgentVote,
    EpisodicMemoryStore,
)
from src.nexus.engines.world import WorldInfrastructureEngine
from src.nexus.engines.autonomy import (
    AutonomousWorkflowEngine,
    WorkflowStatus,
    WorkflowStep,
)
from src.nexus.engines.evolution import (
    EvolutionaryBenchmarker,
    RedTeamChallengeResult,
    SystemMaturityScore,
)
from src.nexus.cli import main as cli_main


# --- 1. Mission 03: AI Model Gateway & Swarm Runtime ---
def test_model_gateway_routing():
    gateway = ModelGateway()
    # Test routing to appropriate tier
    route_fast = gateway.route_task(task_type="FAST", prompt="Short summary")
    assert route_fast.model_id == "gemini-3.8-flash"
    assert route_fast.tier == ModelTier.FAST

    route_reasoning = gateway.route_task(task_type="REASONING", prompt="Complex mathematical proof")
    assert "pro" in route_reasoning.model_id or "thinking" in route_reasoning.model_id
    assert route_reasoning.tier == ModelTier.REASONING

    # Test fallback mechanism
    fallback_res = gateway.execute_with_fallback(failing_primary=True, prompt="Test query")
    assert fallback_res["status"] == "SUCCESS_VIA_FALLBACK"
    assert fallback_res["model_used"] != "primary_broken"


def test_swarm_consensus_voting():
    swarm = SwarmRuntime()
    votes = [
        AgentVote(agent_id="Agent-Architect", vote="APPROVE", confidence=0.98),
        AgentVote(agent_id="Agent-Scientist", vote="APPROVE", confidence=0.95),
        AgentVote(agent_id="Agent-Governor", vote="REJECT", confidence=0.70),
    ]
    consensus = swarm.evaluate_consensus(votes)
    assert consensus.decision == "APPROVE"
    assert consensus.quorum_achieved is True
    assert consensus.approval_ratio > 0.60


def test_episodic_memory_store():
    mem = EpisodicMemoryStore()
    mem.store(key="mem-001", content="Newton developed classical mechanics at Cambridge in 1687", tags=["cambridge", "physics"])
    mem.store(key="mem-002", content="Turing formulated the Universal Turing Machine at Cambridge in 1936", tags=["cambridge", "computation"])

    results = mem.query(tag="physics")
    assert len(results) == 1
    assert "Newton" in results[0]["content"]

    results_all = mem.query(tag="cambridge")
    assert len(results_all) == 2


# --- 2. Mission 06: World Infrastructure & Cislunar Engine ---
def test_smart_energy_grid_balancing():
    world = WorldInfrastructureEngine()
    grid = world.balance_smart_grid(generation_mw=1200.0, load_mw=1000.0, storage_capacity_mwh=500.0)
    assert grid["status"] == "BALANCED"
    assert grid["battery_charging_mw"] == 200.0
    assert grid["curtailment_mw"] == 0.0

    # Overload test
    grid_overload = world.balance_smart_grid(generation_mw=800.0, load_mw=1000.0, storage_capacity_mwh=500.0, current_storage_mwh=300.0)
    assert grid_overload["status"] == "BALANCED_DISCHARGE"
    assert grid_overload["battery_discharge_mw"] == 200.0


def test_cislunar_orbital_transfer():
    world = WorldInfrastructureEngine()
    cislunar = world.calculate_cislunar_transfer(origin="LEO", destination="EML2")
    assert cislunar["delta_v_km_s"] > 3.0
    assert cislunar["trajectory_status"] == "HALO_ORBIT_CONVERGED"


# --- 3. Mission 08: Autonomous Workflows & Human Approval ---
def test_workflow_engine_human_approval_gate():
    engine = AutonomousWorkflowEngine()
    steps = [
        WorkflowStep(name="prepare_manifest", requires_approval=False),
        WorkflowStep(name="wire_financial_settlement", requires_approval=True),
        WorkflowStep(name="deploy_service", requires_approval=False),
    ]
    wf = engine.create_workflow(name="capital_allocation_pipeline", steps=steps)
    
    # Run step 1
    engine.step_forward(wf.workflow_id)
    assert wf.status == WorkflowStatus.RUNNING

    # Step 2 requires human approval
    engine.step_forward(wf.workflow_id)
    assert wf.status == WorkflowStatus.PENDING_APPROVAL

    # Human approves
    engine.approve_step(wf.workflow_id, approver_email="aditya@omniverse.internal")
    assert wf.status == WorkflowStatus.RUNNING

    # Step 2 executes now that it's approved
    engine.step_forward(wf.workflow_id)
    assert wf.status == WorkflowStatus.RUNNING

    # Step 3 completes
    engine.step_forward(wf.workflow_id)
    assert wf.status == WorkflowStatus.COMPLETED


# --- 4. Mission 10: Evolutionary Benchmarking & Red Teaming ---
def test_evolutionary_red_teaming():
    benchmarker = EvolutionaryBenchmarker()
    challenge = benchmarker.generate_red_team_challenge(domain="Cryptographic Ledgers")
    assert isinstance(challenge, RedTeamChallengeResult)
    assert challenge.adversarial_vector in ["DOUBLE_SPEND_RACE", "QUANTUM_SHOR_ATTACK", "SYBIL_PARTITION"]
    assert challenge.mitigated is True


def test_system_maturity_scoring():
    benchmarker = EvolutionaryBenchmarker()
    score = benchmarker.evaluate_maturity()
    assert isinstance(score, SystemMaturityScore)
    assert score.overall_score >= 90.0
    assert len(score.department_scores) == 9
    for dept, s in score.department_scores.items():
        assert s >= 85.0


# --- 5. Nexus CLI Interface ---
def test_nexus_cli_execution(capsys):
    ret = cli_main(["status"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "ATLAS NEXUS" in captured.out
    assert "Departments Active: 9" in captured.out

    ret_caps = cli_main(["capabilities"])
    assert ret_caps == 0
    captured_caps = capsys.readouterr()
    assert "50 Capabilities" in captured_caps.out
