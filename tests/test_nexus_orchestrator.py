import pytest
from src.nexus.command import NexusCommandCenter, ProjectDirective
from src.nexus.departments import DepartmentEnum
from src.nexus.orchestrator import UniversalOrchestrator, ExecutionManifest, OrchestratorTelemetry

def test_orchestrator_initialization():
    orchestrator = UniversalOrchestrator()
    telemetry = orchestrator.get_telemetry()
    assert isinstance(telemetry, OrchestratorTelemetry)
    assert telemetry.departments_ready == 9
    assert telemetry.capabilities_indexed == 50
    assert telemetry.total_executions == 0

def test_orchestrator_dispatch_single_department():
    command_center = NexusCommandCenter()
    directive = command_center.parse_intake(
        raw_input="Validate financial ledger and limit order book risk metrics",
        user_id="aditya"
    )
    orchestrator = UniversalOrchestrator()
    manifest = orchestrator.dispatch(directive)
    
    assert isinstance(manifest, ExecutionManifest)
    assert manifest.directive_id == directive.directive_id
    assert manifest.status == "SUCCESS"
    assert DepartmentEnum.DEPT_D in manifest.executed_departments
    assert len(manifest.audit_trail) > 0
    assert "ledger" in str(manifest.results).lower() or "financial" in str(manifest.results).lower()

def test_orchestrator_dispatch_civilization_scale_omniverse():
    command_center = NexusCommandCenter()
    directive = command_center.parse_intake(
        raw_input="Make the level very high make it everything so I can create everything omniverse civilization scale",
        user_id="aditya"
    )
    orchestrator = UniversalOrchestrator()
    manifest = orchestrator.dispatch(directive)
    
    assert manifest.status == "SUCCESS"
    assert len(manifest.executed_departments) == 9
    assert len(manifest.executed_capabilities) == 50
    
    # Verify telemetry incremented
    telemetry = orchestrator.get_telemetry()
    assert telemetry.total_executions == 1
    assert len(manifest.audit_trail) == 9
