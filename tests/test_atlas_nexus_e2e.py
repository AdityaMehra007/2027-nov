"""
End-to-End Civilization-Scale Verification Suite for ATLAS NEXUS
Verifies complete user journeys, multi-department orchestration, and quality gates.
"""

import pytest
from src.nexus.client import NexusClient
from src.nexus.departments import DepartmentEnum

def test_e2e_university_research_journey():
    client = NexusClient()
    manifest = client.execute("Which is the number one university in the world and research paper citations")
    assert manifest.status == "SUCCESS"
    assert DepartmentEnum.DEPT_A in manifest.executed_departments
    dept_a_res = manifest.results["DEPT_A"]
    assert dept_a_res["verification_confidence"] >= 0.99
    assert len(dept_a_res["source_citations"]) > 0

def test_e2e_software_factory_creation_journey():
    client = NexusClient()
    manifest = client.execute("Build and deploy a full stack saas application with automated tests")
    assert manifest.status == "SUCCESS"
    assert DepartmentEnum.DEPT_G in manifest.executed_departments
    dept_g_res = manifest.results["DEPT_G"]
    assert dept_g_res["code_quality_score"] == 100
    assert len(dept_g_res["scaffolded_artifacts"]) >= 3

def test_e2e_deep_tech_quantum_and_financial_journey():
    client = NexusClient()
    manifest = client.execute("Simulate quantum surface codes, plasma fusion energy and financial ledger balance")
    assert manifest.status == "SUCCESS"
    assert DepartmentEnum.DEPT_B in manifest.executed_departments
    assert DepartmentEnum.DEPT_D in manifest.executed_departments
    
    dept_b_res = manifest.results["DEPT_B"]
    assert dept_b_res["quantum_surface_code_fidelity"] >= 0.999
    
    dept_d_res = manifest.results["DEPT_D"]
    assert dept_d_res["financial_ledger_status"] == "BALANCED_AUDITED"

def test_e2e_omniverse_civilization_scale_directive():
    client = NexusClient()
    # Exact prompt phrase from Aditya in ChatGPT
    manifest = client.execute(
        "Make the level very high make the level very up and make it everything so I can create everything omniverse civilization scale"
    )
    assert manifest.status == "SUCCESS"
    assert len(manifest.executed_departments) == 9
    assert len(manifest.executed_capabilities) == 50
    assert len(manifest.audit_trail) == 9
    
    # Verify strict monotonicity of HLC timestamps in audit trail
    timestamps = [step["hlc_timestamp"] for step in manifest.audit_trail]
    for i in range(1, len(timestamps)):
        assert timestamps[i] > timestamps[i - 1], f"HLC non-monotonic: {timestamps[i]} <= {timestamps[i-1]}"

def test_all_50_capabilities_integrity():
    client = NexusClient()
    caps = client.get_capabilities()
    assert len(caps) == 50
    for c in caps:
        assert c.id >= 1 and c.id <= 50
        assert len(c.name.strip()) > 0
        assert len(c.description.strip()) > 0
        assert c.department in DepartmentEnum
