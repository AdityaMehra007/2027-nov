import pytest
from omniverse.core.directive import MasterDirectiveRegistry, GlobalService, AgentPersona

def test_registry_services_count():
    services = MasterDirectiveRegistry.get_services()
    assert len(services) == 12
    alpha_services = [s for s in services if s.core == "ALPHA"]
    beta_services = [s for s in services if s.core == "BETA"]
    assert len(alpha_services) == 6
    assert len(beta_services) == 6

def test_registry_personas_count():
    personas = MasterDirectiveRegistry.get_personas()
    assert len(personas) == 7
    roles = {p.role for p in personas}
    assert "Supreme Chief Architect" in roles
    assert "Aether Resilience Commander" in roles

def test_registry_integrity_check():
    health = MasterDirectiveRegistry.validate_integrity()
    assert health["valid"] is True
    assert health["total_services"] == 12
    assert health["total_personas"] == 7

def test_registry_get_service():
    svc = MasterDirectiveRegistry.get_service("SVC-ALPHA-01")
    assert svc is not None
    assert svc.name == "Local SMB Autonomous Growth Kits"
    assert svc.core == "ALPHA"
    assert MasterDirectiveRegistry.get_service("NON-EXISTENT") is None
