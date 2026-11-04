from pathlib import Path
from omniverse.core.directive import MasterDirectiveRegistry

def test_universal_master_directive_file_exists():
    path = Path("UNIVERSAL_MASTER_DIRECTIVE_2027.md")
    assert path.is_file(), "UNIVERSAL_MASTER_DIRECTIVE_2027.md must exist in root"
    content = path.read_text(encoding="utf-8")
    assert "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC" in content
    assert "THE SUPREME UNIVERSAL 2027 DIRECTIVE" in content

    # Verify all 12 services are explicitly detailed in document
    for svc in MasterDirectiveRegistry.get_services():
        assert svc.name in content, f"Service {svc.name} must be documented"

    # Verify all 7 agent personas are explicitly detailed in document
    for persona in MasterDirectiveRegistry.get_personas():
        assert persona.role in content, f"Persona {persona.role} must be documented"
