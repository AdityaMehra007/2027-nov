"""
ATLAS NEXUS: FastAPI REST Gateway
Exposes institutional command intake, capability discovery, orchestration execution, and telemetry.
"""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.nexus.command import NexusCommandCenter, ProjectDirective
from src.nexus.departments import (
    CapabilityDescriptor,
    CapabilityRegistry,
    get_all_capabilities,
    get_capability_by_id,
)
from src.nexus.orchestrator import (
    ExecutionManifest,
    OrchestratorTelemetry,
    UniversalOrchestrator,
)

app = FastAPI(
    title="ATLAS NEXUS: The Civilization-Scale Intelligence & Creation Engine",
    description="Unified REST interface for 50 institutional capabilities across 9 departments.",
    version="1.0.0",
)

command_center = NexusCommandCenter()
orchestrator = UniversalOrchestrator()


class IntakeRequest(BaseModel):
    raw_input: str
    user_id: Optional[str] = "aditya"
    priority: Optional[str] = "NORMAL"


class ExecuteRequest(BaseModel):
    raw_input: str
    user_id: Optional[str] = "aditya"
    priority: Optional[str] = "NORMAL"


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {
        "status": "HEALTHY",
        "system": "ATLAS_NEXUS",
        "version": "1.0.0",
        "environment": "Google Antigravity",
    }


@app.post("/api/v1/nexus/intake")
def intake(req: IntakeRequest) -> Dict[str, Any]:
    try:
        directive = command_center.parse_intake(
            raw_input=req.raw_input,
            user_id=req.user_id or "aditya",
            priority=req.priority or "NORMAL",
        )
        return {
            "directive_id": directive.directive_id,
            "raw_input": directive.raw_input,
            "user_id": directive.user_id,
            "intent": directive.intent,
            "target_departments": [d.name for d in directive.target_departments],
            "requested_capabilities": directive.requested_capabilities,
            "priority": directive.priority,
            "timestamp_hlc": directive.timestamp_hlc,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/nexus/capabilities")
def list_capabilities() -> List[Dict[str, Any]]:
    caps = command_center.list_capabilities()
    return [
        {
            "id": c.id,
            "name": c.name,
            "department": c.department.name,
            "department_label": c.department.value,
            "description": c.description,
            "engine_target": c.engine_target,
        }
        for c in caps
    ]


@app.get("/api/v1/nexus/capabilities/{cap_id}")
def get_capability(cap_id: int) -> Dict[str, Any]:
    cap = command_center.get_capability(cap_id)
    if not cap:
        raise HTTPException(status_code=404, detail=f"Capability {cap_id} not found")
    return {
        "id": cap.id,
        "name": cap.name,
        "department": cap.department.name,
        "department_label": cap.department.value,
        "description": cap.description,
        "engine_target": cap.engine_target,
    }


@app.post("/api/v1/nexus/execute")
def execute(req: ExecuteRequest) -> Dict[str, Any]:
    try:
        directive = command_center.parse_intake(
            raw_input=req.raw_input,
            user_id=req.user_id or "aditya",
            priority=req.priority or "NORMAL",
        )
        manifest = orchestrator.dispatch(directive)
        return {
            "directive_id": manifest.directive_id,
            "status": manifest.status,
            "executed_departments": [d.name for d in manifest.executed_departments],
            "executed_capabilities": manifest.executed_capabilities,
            "results": manifest.results,
            "audit_trail": manifest.audit_trail,
            "hlc_timestamp": manifest.hlc_timestamp,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/nexus/telemetry")
def get_telemetry() -> Dict[str, Any]:
    telemetry = orchestrator.get_telemetry()
    return {
        "active_agents": telemetry.active_agents,
        "hlc_timestamp": telemetry.hlc_timestamp,
        "total_executions": telemetry.total_executions,
        "departments_ready": telemetry.departments_ready,
        "capabilities_indexed": telemetry.capabilities_indexed,
    }
