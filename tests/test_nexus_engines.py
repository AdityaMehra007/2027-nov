"""
Test suite for ATLAS NEXUS Mission Engines:
- Intelligence & Knowledge Fabric (Mission 02)
- Software Factory (Mission 05)
- Simulation & Digital Twin (Mission 04)
- Enterprise Governance & Compute (Mission 09)
"""

import pytest
from starlette.testclient import TestClient

from src.nexus.api import app
from src.nexus.engines.intelligence import NexusKnowledgeGraph, ClaimVerifier, ResearchIntelligence
from src.nexus.engines.software_factory import SoftwareFactory, CodeValidationResult
from src.nexus.engines.simulation import DigitalTwin, ScenarioSimulator
from src.nexus.engines.enterprise import TenantManager, ComputeGovernor, UserRole


# --- 1. Intelligence & Knowledge Fabric Tests ---
def test_knowledge_graph_triplets_and_traversal():
    kg = NexusKnowledgeGraph()
    kg.add_triplet("Cambridge", "birthplace_of", "Cavendish_Laboratory")
    kg.add_triplet("Cavendish_Laboratory", "discovered", "Electron")
    kg.add_triplet("Cavendish_Laboratory", "discovered", "Neutron")

    neighbors = kg.get_outgoing("Cavendish_Laboratory")
    assert len(neighbors) == 2
    targets = [rel[1] for rel in neighbors]
    assert "Electron" in targets
    assert "Neutron" in targets

    path = kg.find_path("Cambridge", "Electron")
    assert path == ["Cambridge", "Cavendish_Laboratory", "Electron"]


def test_claim_verifier():
    verifier = ClaimVerifier()
    res = verifier.verify_claim(
        claim="Cambridge was home to the Cavendish Laboratory where the electron was discovered in 1897",
        grounding_sources=["Cavendish History", "Thomson Nobel 1906"]
    )
    assert res.is_verified is True
    assert res.confidence >= 0.95
    assert len(res.evidence_hash) == 64  # SHA-256


def test_research_intelligence_synthesis():
    intel = ResearchIntelligence()
    summary = intel.synthesize_domain("Quantum Computing & Surface Codes")
    assert "Quantum Computing & Surface Codes" in summary.domain
    assert len(summary.key_findings) >= 3
    assert len(summary.suggested_directions) >= 2


# --- 2. Software Factory Tests ---
def test_software_factory_scaffolding():
    factory = SoftwareFactory()
    project = factory.scaffold_project(name="OmniPay", project_type="saas_service")
    assert project.name == "OmniPay"
    assert "main.py" in project.files
    assert "test_main.py" in project.files
    assert "README.md" in project.files
    assert len(project.files) >= 4


def test_software_factory_code_validation():
    factory = SoftwareFactory()
    valid_code = "def add(a: int, b: int) -> int:\n    return a + b\n"
    res = factory.validate_code(valid_code)
    assert res.is_valid is True
    assert res.ast_node_count > 0

    invalid_code = "def broken(\n  return 42"
    res_bad = factory.validate_code(invalid_code)
    assert res_bad.is_valid is False
    assert "SyntaxError" in res_bad.error_message


# --- 3. Simulation & Digital Twin Tests ---
def test_digital_twin_telemetry_and_drift():
    twin = DigitalTwin(system_id="TURBINE-001", nominal_state={"temperature": 300.0, "rpm": 3600.0})
    # Nominal reading
    drift = twin.record_telemetry({"temperature": 302.0, "rpm": 3605.0})
    assert drift < 0.05
    assert twin.is_healthy is True

    # Critical anomaly reading
    drift_critical = twin.record_telemetry({"temperature": 450.0, "rpm": 5200.0})
    assert drift_critical > 0.3
    assert twin.is_healthy is False


def test_numerical_scenario_simulator():
    sim = ScenarioSimulator()
    # Simple harmonic oscillator: dx/dt = v, dv/dt = -x
    def derivs(t, state):
        x, v = state
        return [v, -x]

    trajectory = sim.rk4_integrate(derivs, initial_state=[1.0, 0.0], t_span=(0.0, 1.0), steps=20)
    assert len(trajectory) == 21
    # At t=0, x=1.0. At t=pi/2 ~ 1.57 x=0, at t=1.0 x ~ cos(1.0) ~ 0.54
    final_x = trajectory[-1][1][0]
    assert 0.50 <= final_x <= 0.60


# --- 4. Enterprise Governance & Compute Tests ---
def test_tenant_manager_and_rbac():
    tm = TenantManager()
    tenant = tm.create_tenant("ApexCorp", admin_email="aditya@apexcorp.internal")
    assert tenant.tenant_id.startswith("TEN-")

    # Add user
    user = tm.add_user(tenant.tenant_id, "researcher_1@apexcorp.internal", UserRole.RESEARCHER)
    assert user.role == UserRole.RESEARCHER

    # Check permission
    assert tm.has_permission(user.user_id, "execute_research") is True
    assert tm.has_permission(user.user_id, "manage_billing") is False


def test_compute_governor_budgeting():
    gov = ComputeGovernor(global_token_quota=10000)
    # First spend
    assert gov.consume(tokens=2000, compute_seconds=1.5) is True
    assert gov.remaining_tokens == 8000

    # Overspend
    assert gov.consume(tokens=9000, compute_seconds=5.0) is False
    assert gov.remaining_tokens == 8000


# --- 5. Visual Cockpit Tests ---
def test_visual_cockpit_html_endpoint():
    client = TestClient(app)
    res = client.get("/ui")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "ATLAS NEXUS" in res.text
    assert "Universal Orchestrator" in res.text
