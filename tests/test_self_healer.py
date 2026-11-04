import pytest
from pathlib import Path
from omniverse.modules.evolution.self_healer import SelfHealingEngine, CodeHealthAudit, OptimizationProposal

def test_codebase_health_audit():
    healer = SelfHealingEngine(root_dir=Path("./src/omniverse"))
    audit = healer.audit_codebase_health()

    assert isinstance(audit, CodeHealthAudit)
    assert audit.files_analyzed >= 20
    assert audit.total_lines > 2000
    assert audit.functions_count > 50
    assert audit.classes_count > 20
    assert audit.type_annotated_pct > 70.0
    assert audit.health_grade in ["A", "A+"]

def test_generate_optimization_proposals():
    healer = SelfHealingEngine()
    proposals = healer.generate_optimization_proposals()

    assert len(proposals) >= 3
    assert all(isinstance(p, OptimizationProposal) for p in proposals)
    assert all(p.safety_governor_approved is True for p in proposals)
    assert any("LRU" in p.optimization_type for p in proposals)
