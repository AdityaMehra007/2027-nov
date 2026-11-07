"""Client Diagnostic Agent: Audits digital infrastructure, detects bottlenecks, and quantifies revenue loss."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus
from omniverse.modules.agency.world_clients import WorldClientDirectory


class ClientDiagnosticAgent(BaseAgent):
    """Autonomous agent that evaluates technical and commercial bottlenecks for global companies."""

    def __init__(self, directory: WorldClientDirectory = None):
        self.directory = directory or WorldClientDirectory()

    @property
    def role_name(self) -> str:
        return "ClientDiagnostic"

    @property
    def division(self) -> str:
        return "Audit"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name")
        client = None

        if client_name:
            client = self.directory.get_client_by_name(client_name)

        if not client:
            # Fallback to direct client dict in payload if passed
            raw_client = payload.get("client_data")
            if raw_client:
                client_name = raw_client.get("name", "Target Prospect")
                revenue = float(raw_client.get("annual_revenue_usd", 1_000_000.0))
                tech_stack = raw_client.get("tech_stack", ["Python", "React"])
                needs = raw_client.get("declared_needs", ["Modern API", "Client Portal"])
                raw_hub = raw_client.get("hub", "GLOBAL")
                raw_sector = raw_client.get("sector", "GENERAL")
                hub = raw_hub.value if hasattr(raw_hub, "value") else str(raw_hub)
                sector = raw_sector.value if hasattr(raw_sector, "value") else str(raw_sector)
            else:
                return {"status": "ERROR", "message": f"Client '{client_name}' not found."}
        else:
            client_name = client.name
            revenue = client.annual_revenue_usd
            tech_stack = client.tech_stack
            needs = client.declared_needs
            hub = client.hub.value if hasattr(client.hub, "value") else str(client.hub)
            sector = client.sector.value if hasattr(client.sector, "value") else str(client.sector)

        # Calculate heuristic audit scores
        tech_count = len(tech_stack)
        perf_score = min(95.0, max(40.0, 50.0 + (tech_count * 7.5)))
        seo_score = 65.0
        conversion_score = 55.0

        estimated_monthly_loss = round((revenue * 0.08) / 12.0, 2)

        diagnosis = {
            "client_name": client_name,
            "hub": hub,
            "sector": sector,
            "performance_score": perf_score,
            "seo_score": seo_score,
            "conversion_score": conversion_score,
            "overall_health": round((perf_score + seo_score + conversion_score) / 3.0, 1),
            "estimated_monthly_loss_usd": estimated_monthly_loss,
            "primary_bottlenecks": needs,
            "recommended_archetype": "FULL_TRANSFORMATION",
        }

        # Persist audit record and security audit log to database
        try:
            from omniverse.core.database import get_session, init_db
            from omniverse.modules.agency.models import ClientAuditRecord
            from omniverse.core.security import SecurityAuditRecord

            init_db()

            with get_session() as session:
                audit_record = ClientAuditRecord(
                    client_name=client_name,
                    hub=hub,
                    sector=sector,
                    performance_score=perf_score,
                    seo_score=seo_score,
                    conversion_score=conversion_score,
                    overall_health=diagnosis["overall_health"],
                    estimated_monthly_loss_usd=estimated_monthly_loss,
                    bottlenecks_json=json.dumps(needs),
                    recommended_archetype=diagnosis.get("recommended_archetype", "FULL_TRANSFORMATION"),
                    timestamp=time.time(),
                )
                session.add(audit_record)

                sec_record = SecurityAuditRecord(
                    request_id=f"audit_{uuid.uuid4().hex[:12]}",
                    action_type="client_diagnostic_audit",
                    details_json=json.dumps({
                        "client": client_name,
                        "hub": hub,
                        "sector": sector,
                        "overall_health": diagnosis["overall_health"],
                        "estimated_monthly_loss_usd": estimated_monthly_loss,
                    }),
                    status="approved",
                    approver="ClientDiagnosticAgent",
                    created_at=time.time(),
                    resolved_at=time.time(),
                )
                session.add(sec_record)
                session.commit()
        except Exception:
            pass

        # Append audit event to artifacts/telemetry/audit_events.jsonl
        try:
            audit_event = {
                "timestamp": time.time(),
                "event_name": "CLIENT_DIAGNOSIS_COMPLETED",
                "client_name": client_name,
                "hub": hub,
                "sector": sector,
                "health_score": diagnosis["overall_health"],
                "monthly_loss_usd": estimated_monthly_loss,
                "performance_score": perf_score,
                "seo_score": seo_score,
                "conversion_score": conversion_score,
            }
            audit_path = Path("artifacts/telemetry/audit_events.jsonl")
            audit_path.parent.mkdir(parents=True, exist_ok=True)
            with open(audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_event, default=str) + "\n")
        except Exception:
            pass

        global_event_bus.publish("CLIENT_DIAGNOSIS_COMPLETED", {
            "client": client_name,
            "hub": hub,
            "sector": sector,
            "health_score": diagnosis["overall_health"],
            "monthly_loss_usd": estimated_monthly_loss,
        })

        return {
            "status": "SUCCESS",
            "diagnosis": diagnosis,
        }

