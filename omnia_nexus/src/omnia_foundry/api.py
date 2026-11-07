"""
PROJECT OMNIA NEXUS: Supreme Control Plane API & Executive Dashboard
FastAPI REST interface and real-time operational dashboard for OMNIA Foundry.
"""
from __future__ import annotations
import csv
import json
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from .models import TASK_STATES, identifier
from .store import Store
from .audit import verify

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REGISTRY_DIR = BASE_DIR / "registry"
RESEARCH_DIR = BASE_DIR / "research"
PLANNING_DIR = BASE_DIR / "planning"
DB_PATH = BASE_DIR / "data" / "omnia_foundry.db"

app = FastAPI(
    title="PROJECT OMNIA NEXUS — Master API",
    description="Operational command plane, cryptographic audit ledger, and venture studio intelligence registry.",
    version="1.0.0"
)

# Request / Response Schemas
class TaskStatusUpdate(BaseModel):
    status: str = Field(..., description="Target status: not_started, in_progress, blocked, completed, cancelled")
    actor: str = Field(default="master_orchestrator", description="Actor initiating status update")

class ApprovalRequestPayload(BaseModel):
    action: str
    details: str
    requested_by: str = "founder"

class ApprovalDecisionPayload(BaseModel):
    approved_by: str = "founder"
    reason: str
    approve: bool = True

def get_store() -> Store:
    return Store(DB_PATH)

@app.get("/api/v1/health", tags=["System"])
def get_health():
    store = get_store()
    events = store.audit_events()
    is_valid = verify(events)
    return {
        "status": "online",
        "system": "PROJECT OMNIA NEXUS",
        "timestamp": time.time(),
        "database": str(DB_PATH.name),
        "audit_chain_valid": is_valid,
        "audit_event_count": len(events)
    }

@app.get("/api/v1/report", tags=["Intelligence"])
def get_report():
    store = get_store()
    return {
        "programmes": store.rows("programmes"),
        "tasks": store.rows("tasks"),
        "experiments": store.rows("experiments"),
        "evidence": store.rows("evidence"),
        "approvals": store.rows("approvals")
    }

@app.get("/api/v1/studios", tags=["Venture Studios"])
def get_studios():
    studios_csv = REGISTRY_DIR / "VENTURE_STUDIOS.csv"
    if not studios_csv.exists():
        raise HTTPException(status_code=404, detail="VENTURE_STUDIOS.csv not found")
    with open(studios_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get("/api/v1/ecosystem", tags=["Ecosystem Intelligence"])
def get_ecosystem(category: Optional[str] = None):
    eco_csv = REGISTRY_DIR / "ECOSYSTEM_RESEARCH_SEED.csv"
    if not eco_csv.exists():
        raise HTTPException(status_code=404, detail="ECOSYSTEM_RESEARCH_SEED.csv not found")
    with open(eco_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        items = list(reader)
        if category:
            items = [item for item in items if item.get("Domain", "").lower() == category.lower()]
        return items

@app.get("/api/v1/research", tags=["Frontier R&D"])
def get_research():
    res_csv = RESEARCH_DIR / "FRONTIER_RESEARCH_AGENDA.csv"
    if not res_csv.exists():
        raise HTTPException(status_code=404, detail="FRONTIER_RESEARCH_AGENDA.csv not found")
    with open(res_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get("/api/v1/tasks", tags=["Execution Backlog"])
def get_tasks(status: Optional[str] = None, priority: Optional[str] = None):
    store = get_store()
    tasks = store.rows("tasks")
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]
    return tasks

@app.put("/api/v1/tasks/{task_id}/status", tags=["Execution Backlog"])
def update_task_status(task_id: str, payload: TaskStatusUpdate):
    store = get_store()
    try:
        store.set_task_status(task_id, payload.status, actor=payload.actor)
        return {"task_id": task_id, "status": payload.status, "updated_by": payload.actor}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/audit/verify", tags=["Cryptographic Audit"])
def verify_audit():
    store = get_store()
    events = store.audit_events()
    is_valid = verify(events)
    return {
        "valid": is_valid,
        "event_count": len(events),
        "genesis_hash": events[0]["previous_hash"] if events else "GENESIS",
        "latest_hash": events[-1]["event_hash"] if events else None
    }

@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard():
    store = get_store()
    programmes = store.rows("programmes")
    tasks = store.rows("tasks")
    events = store.audit_events()
    is_valid = verify(events)

    p0_count = sum(1 for t in tasks if t.get("priority") == "P0")
    completed_count = sum(1 for t in tasks if t.get("status") == "completed")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PROJECT OMNIA NEXUS — Supreme Command Console</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ background-color: #0b0f19; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }}
    .glow {{ box-shadow: 0 0 20px rgba(56, 189, 248, 0.15); }}
    .cyber-card {{ background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(55, 65, 81, 0.6); }}
  </style>
</head>
<body class="p-6 max-w-7xl mx-auto">
  <!-- Header -->
  <header class="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-gray-800 gap-4">
    <div>
      <div class="flex items-center gap-3">
        <span class="inline-block w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
        <h1 class="text-2xl font-bold tracking-tight text-white">PROJECT OMNIA NEXUS</h1>
        <span class="px-2.5 py-0.5 rounded text-xs font-semibold bg-cyan-900/50 text-cyan-300 border border-cyan-700/50">FOUNDRY CORE v1.0</span>
      </div>
      <p class="text-sm text-gray-400 mt-1">Civilisation-Scale Frontier Technology, Intelligence & Venture-Building Operating Platform</p>
    </div>
    <div class="flex items-center gap-3">
      <div class="px-3 py-1.5 rounded-lg cyber-card flex items-center gap-2">
        <span class="text-xs text-gray-400">LEDGER:</span>
        <span class="text-xs font-mono font-bold {'text-emerald-400' if is_valid else 'text-red-400'}">
          {'CRYPTOGRAPHICALLY SECURED (' + str(len(events)) + ' HASHES)' if is_valid else 'TAMPERED'}
        </span>
      </div>
      <a href="/docs" target="_blank" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-xs font-semibold text-white transition">API Swagger Docs</a>
    </div>
  </header>

  <!-- Metric Badges -->
  <section class="grid grid-cols-2 md:grid-cols-4 gap-4 my-6">
    <div class="cyber-card p-4 rounded-xl glow">
      <span class="text-xs text-cyan-400 font-semibold tracking-wider uppercase">Venture Studios</span>
      <div class="text-3xl font-bold text-white mt-1">{len(programmes)}</div>
      <span class="text-xs text-gray-400">24 Frontier Disciplines</span>
    </div>
    <div class="cyber-card p-4 rounded-xl glow">
      <span class="text-xs text-amber-400 font-semibold tracking-wider uppercase">Backlog Tasks</span>
      <div class="text-3xl font-bold text-white mt-1">{len(tasks)}</div>
      <span class="text-xs text-gray-400">{p0_count} Critical P0 Tasks</span>
    </div>
    <div class="cyber-card p-4 rounded-xl glow">
      <span class="text-xs text-emerald-400 font-semibold tracking-wider uppercase">Completed Milestones</span>
      <div class="text-3xl font-bold text-white mt-1">{completed_count}</div>
      <span class="text-xs text-gray-400">Evidence verified</span>
    </div>
    <div class="cyber-card p-4 rounded-xl glow">
      <span class="text-xs text-purple-400 font-semibold tracking-wider uppercase">Audit Events</span>
      <div class="text-3xl font-bold text-white mt-1">{len(events)}</div>
      <span class="text-xs text-gray-400">SHA-256 Chained</span>
    </div>
  </section>

  <!-- Main Grid -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Venture Studios Column -->
    <div class="cyber-card rounded-xl p-5 lg:col-span-1">
      <h2 class="text-base font-bold text-white mb-3 flex items-center justify-between">
        <span>24 Venture Studios</span>
        <span class="text-xs font-normal text-cyan-400">Active</span>
      </h2>
      <div class="space-y-2.5 max-h-[550px] overflow-y-auto pr-1">
        {"".join([f'''
        <div class="p-3 rounded-lg bg-gray-900/60 border border-gray-800/80 hover:border-gray-700 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-mono text-cyan-400">{p['programme_id']}</span>
            <span class="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-gray-800 text-gray-300">{p['stage']}</span>
          </div>
          <div class="text-sm font-semibold text-white mt-1">{p['name']}</div>
          <div class="text-xs text-gray-400 mt-0.5 line-clamp-1">{p['domain']}</div>
        </div>
        ''' for p in programmes[:12]])}
      </div>
    </div>

    <!-- Master Execution Backlog Column -->
    <div class="cyber-card rounded-xl p-5 lg:col-span-2">
      <h2 class="text-base font-bold text-white mb-3 flex items-center justify-between">
        <span>Master Execution Backlog (Top Milestones)</span>
        <span class="text-xs font-normal text-amber-400">P0 / P1 Prioritized</span>
      </h2>
      <div class="space-y-2 max-h-[550px] overflow-y-auto pr-1">
        {"".join([f'''
        <div class="p-3 rounded-lg bg-gray-900/60 border border-gray-800/80 flex items-start justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-xs font-mono font-bold text-amber-400">{t['task_id']}</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-950/60 text-amber-300 border border-amber-800/50">{t['priority']}</span>
              <span class="text-[10px] text-gray-400">Owner: {t['owner']}</span>
            </div>
            <div class="text-sm font-medium text-gray-200">{t['title']}</div>
            <div class="text-xs text-gray-400">DoD: {t['acceptance']}</div>
          </div>
          <span class="text-xs font-mono px-2 py-1 rounded {'bg-emerald-950 text-emerald-300 border border-emerald-800' if t['status'] == 'completed' else 'bg-gray-800 text-gray-300'}">
            {t['status']}
          </span>
        </div>
        ''' for t in tasks[:15]])}
      </div>
    </div>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html)
