"""
CASHFLOW INFINITY: OMNIVERSE & PROJECT OMNIA NEXUS
Unified Master API Route for Civilisation-Scale Venture Studios, Backlog & Audit Ledger.
"""
from __future__ import annotations
import csv
import json
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Locate OMNIA NEXUS directories
REPO_ROOT = Path(__file__).resolve().parents[4]
NEXUS_DIR = REPO_ROOT / "omnia_nexus"
REGISTRY_DIR = NEXUS_DIR / "registry"
RESEARCH_DIR = NEXUS_DIR / "research"
PLANNING_DIR = NEXUS_DIR / "planning"
DB_PATH = NEXUS_DIR / "data" / "omnia_foundry.db"

# Lazy store loader to ensure zero import conflicts
def get_foundry_store():
    import sys
    src_path = str(NEXUS_DIR / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from omnia_foundry.store import Store
    return Store(DB_PATH)

def verify_audit_chain(events):
    import sys
    src_path = str(NEXUS_DIR / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from omnia_foundry.audit import verify
    return verify(events)

class TaskStatusUpdate(BaseModel):
    status: str = Field(..., description="Target status: not_started, in_progress, blocked, completed, cancelled")
    actor: str = Field(default="master_orchestrator", description="Actor initiating status update")

def get_omnia_router() -> APIRouter:
    router = APIRouter(prefix="/omnia", tags=["Project Omnia Nexus"])

    @router.get("/health")
    def omnia_health():
        store = get_foundry_store()
        events = store.audit_events()
        is_valid = verify_audit_chain(events)
        return {
            "status": "online",
            "system": "PROJECT OMNIA NEXUS",
            "timestamp": time.time(),
            "database": str(DB_PATH.name),
            "audit_chain_valid": is_valid,
            "audit_event_count": len(events)
        }

    @router.get("/report")
    def omnia_report():
        store = get_foundry_store()
        return {
            "programmes": store.rows("programmes"),
            "tasks": store.rows("tasks"),
            "experiments": store.rows("experiments"),
            "evidence": store.rows("evidence"),
            "approvals": store.rows("approvals")
        }

    @router.get("/studios")
    def omnia_studios():
        studios_csv = REGISTRY_DIR / "VENTURE_STUDIOS.csv"
        if not studios_csv.exists():
            raise HTTPException(status_code=404, detail="VENTURE_STUDIOS.csv not found")
        with open(studios_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    @router.get("/ecosystem")
    def omnia_ecosystem(domain: Optional[str] = None):
        eco_csv = REGISTRY_DIR / "ECOSYSTEM_RESEARCH_SEED.csv"
        if not eco_csv.exists():
            raise HTTPException(status_code=404, detail="ECOSYSTEM_RESEARCH_SEED.csv not found")
        with open(eco_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            items = list(reader)
            if domain:
                items = [item for item in items if item.get("Domain", "").lower() == domain.lower()]
            return items

    @router.get("/research")
    def omnia_research():
        res_csv = RESEARCH_DIR / "FRONTIER_RESEARCH_AGENDA.csv"
        if not res_csv.exists():
            raise HTTPException(status_code=404, detail="FRONTIER_RESEARCH_AGENDA.csv not found")
        with open(res_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    @router.get("/tasks")
    def omnia_tasks(status: Optional[str] = None, priority: Optional[str] = None):
        store = get_foundry_store()
        tasks = store.rows("tasks")
        if status:
            tasks = [t for t in tasks if t.get("status") == status]
        if priority:
            tasks = [t for t in tasks if t.get("priority") == priority]
        return tasks

    @router.put("/tasks/{task_id}/status")
    def omnia_update_task(task_id: str, payload: TaskStatusUpdate):
        store = get_foundry_store()
        try:
            store.set_task_status(task_id, payload.status, actor=payload.actor)
            return {"task_id": task_id, "status": payload.status, "updated_by": payload.actor}
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/audit/verify")
    def omnia_audit_verify():
        store = get_foundry_store()
        events = store.audit_events()
        is_valid = verify_audit_chain(events)
        return {
            "valid": is_valid,
            "event_count": len(events),
            "genesis_hash": events[0]["previous_hash"] if events else "GENESIS",
            "latest_hash": events[-1]["event_hash"] if events else None
        }

    return router
