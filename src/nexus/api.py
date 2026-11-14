"""
ATLAS NEXUS: FastAPI REST Gateway
Exposes institutional command intake, capability discovery, orchestration execution, and telemetry.
"""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
def visual_cockpit() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATLAS NEXUS: Command Cockpit</title>
    <style>
        :root {
            --bg: #090d16;
            --surface: #111827;
            --border: #1f293d;
            --primary: #38bdf8;
            --accent: #818cf8;
            --success: #34d399;
            --text: #f3f4f6;
            --text-muted: #9ca3af;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            background: var(--bg);
            color: var(--text);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        header {
            padding: 20px 40px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { margin: 0; font-size: 20px; font-weight: 700; color: var(--primary); letter-spacing: 1px; }
        .badge {
            background: rgba(56, 189, 248, 0.15);
            color: var(--primary);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        main { padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; box-sizing: border-box; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        .card-val { font-size: 32px; font-weight: 700; color: var(--text); margin-top: 8px; }
        .card-lbl { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .command-bar {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 40px;
        }
        .command-input {
            width: 100%;
            padding: 16px;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
            font-size: 15px;
            box-sizing: border-box;
            outline: none;
            margin-bottom: 12px;
        }
        .command-btn {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: #000;
            font-weight: 700;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .departments-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .dept-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
        }
        .dept-title { font-size: 15px; font-weight: 600; color: var(--primary); margin-bottom: 6px; }
        .dept-desc { font-size: 13px; color: var(--text-muted); line-height: 1.4; }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>ATLAS NEXUS</h1>
            <small style="color: var(--text-muted)">The Civilization-Scale Intelligence & Creation Engine</small>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <span class="badge">Google Antigravity</span>
            <span class="badge" style="background: rgba(52, 211, 153, 0.15); color: var(--success); border-color: var(--success);">Universal Orchestrator Online</span>
        </div>
    </header>
    <main>
        <div class="metrics">
            <div class="card">
                <div class="card-lbl">Departments Active</div>
                <div class="card-val" style="color: var(--primary)">9</div>
            </div>
            <div class="card">
                <div class="card-lbl">Indexed Capabilities</div>
                <div class="card-val" style="color: var(--accent)">50</div>
            </div>
            <div class="card">
                <div class="card-lbl">Deep-Tech Engines</div>
                <div class="card-val" style="color: var(--success)">32</div>
            </div>
            <div class="card">
                <div class="card-lbl">Audit Ledger HLC</div>
                <div class="card-val" style="font-size: 20px; font-family: monospace;">MONOTONIC</div>
            </div>
        </div>

        <div class="command-bar">
            <h3 style="margin-top: 0; margin-bottom: 12px;">Universal Nexus Command Intake</h3>
            <input type="text" class="command-input" placeholder="Type a directive, e.g. 'Build a quantum error correction simulation' or 'Omniverse civilization scale'...">
            <button class="command-btn" onclick="alert('Directive dispatched across Universal Orchestrator.')">Execute Directive</button>
        </div>

        <h3 style="margin-bottom: 16px;">Institutional Departments</h3>
        <div class="departments-grid">
            <div class="dept-card">
                <div class="dept-title">Dept A: Universal Intelligence</div>
                <div class="dept-desc">Knowledge Graph, Research Synthesis, Claim Verification (Caps 01–05).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept B: Science & Frontier Tech</div>
                <div class="dept-desc">Quantum Surface Codes, Plasma MHD, Robotics, Materials (Caps 06–15).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept C: Computational & Engineering</div>
                <div class="dept-desc">Digital Twins, Simulation Engines, Micro-Autograd, Bytecode VM (Caps 16–20).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept D: Business & Economics</div>
                <div class="dept-desc">TigerBeetle Double-Entry, L3 Limit Order Book, VCG Mechanism (Caps 21–25).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept E: Knowledge & Education</div>
                <div class="dept-desc">Career OS, Socratic Tutoring, Multiplayer CRDT Workspace (Caps 26–30).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept F: World & Infrastructure</div>
                <div class="dept-desc">CR3BP Orbital Mechanics, Smart City Urban Grid, Geospatial SAR (Caps 31–35).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept G: Creation & Execution</div>
                <div class="dept-desc">Universal Software Factory, Product Foundry, App Generation (Caps 36–40).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept H: Control & Governance</div>
                <div class="dept-desc">Post-Quantum LWE, Tenant RBAC, Compute Governor, Audit Ledger (Caps 41–45).</div>
            </div>
            <div class="dept-card">
                <div class="dept-title">Dept I: Advanced Intelligence</div>
                <div class="dept-desc">DPLL Automated Theorem Prover, Symbolic AI Physicist (Caps 46–50).</div>
            </div>
        </div>
    </main>
</body>
</html>"""


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
