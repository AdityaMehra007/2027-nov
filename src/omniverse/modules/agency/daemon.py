"""Autonomous Agency Daemon: 24/7 background continuous execution loop."""

from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from omniverse.modules.agency.models import (
    Lead,
    AuditReport,
    PersonalizedPitch,
    JobOrder,
    ServiceType,
    OrderStatus,
    Deliverable,
)
from omniverse.modules.agency.acquisition import LeadHunter, TechAuditor, PitchGenerator
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory
from omniverse.modules.agency.fulfillment.marketing_factory import MarketingFactory
from omniverse.modules.agency.fulfillment.automation_factory import AutomationFactory
from omniverse.modules.agency.qa_governor import QAGovernor


class AgencyCycleReport(BaseModel):
    cycle_id: str = Field(default_factory=lambda: f"cycle_{uuid.uuid4().hex[:8]}")
    cycle_number: int
    leads_hunted: int = 0
    audits_performed: int = 0
    pitches_generated: int = 0
    deliverables_completed: int = 0
    pipeline_value_generated_usd: float = 0.0
    duration_sec: float = 0.0
    timestamp: float = Field(default_factory=time.time)
    details: Dict[str, Any] = Field(default_factory=dict)


class AutonomousAgencyDaemon:
    """Continuous 24/7 execution engine for prospecting, audits, pitches, and delivery."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.cycle_count = 0
        self.hunter = LeadHunter()
        self.auditor = TechAuditor()
        self.pitcher = PitchGenerator()
        self.code_factory = CodeFactory()
        self.marketing_factory = MarketingFactory()
        self.automation_factory = AutomationFactory()
        self.qa_gov = QAGovernor()
        self.history: List[AgencyCycleReport] = []

    def run_cycle(self, limit: int = 2, budget_per_order: float = 3000.0) -> AgencyCycleReport:
        start_time = time.time()
        self.cycle_count += 1

        leads = self.hunter.discover_leads(limit=limit)
        audits: List[AuditReport] = []
        pitches: List[PersonalizedPitch] = []
        total_deliverables = 0

        for idx, lead in enumerate(leads):
            audit = self.auditor.audit_lead(lead)
            audits.append(audit)

            pitch = self.pitcher.generate_pitch(lead, audit)
            pitches.append(pitch)

            # Alternate factory fulfillment for each discovered lead
            if idx % 3 == 0:
                service = ServiceType.FULLSTACK_DEV
                order = JobOrder(
                    client_id=lead.id,
                    service_type=service,
                    brief=f"Turnkey high-converting landing page & backend for {lead.business_name}",
                    budget_usd=budget_per_order,
                )
                deliverables = self.code_factory.build_project(order)
            elif idx % 3 == 1:
                service = ServiceType.MARKETING_SUITE
                order = JobOrder(
                    client_id=lead.id,
                    service_type=service,
                    brief=f"Complete marketing copywriting and ad sequence for {lead.business_name}",
                    budget_usd=budget_per_order,
                )
                deliverables = self.marketing_factory.build_campaign(order)
            else:
                service = ServiceType.AI_AUTOMATION
                order = JobOrder(
                    client_id=lead.id,
                    service_type=service,
                    brief=f"AI agent and autonomous workflow automation for {lead.business_name}",
                    budget_usd=budget_per_order,
                )
                deliverables = self.automation_factory.build_agent_bundle(order)

            # Pre-flight QA verify deliverables
            qa_res = self.qa_gov.verify_deliverables(deliverables)
            for d in deliverables:
                d.qa_passed = qa_res.passed

            total_deliverables += len(deliverables)

        pipeline_val = limit * budget_per_order
        duration = time.time() - start_time

        report = AgencyCycleReport(
            cycle_number=self.cycle_count,
            leads_hunted=len(leads),
            audits_performed=len(audits),
            pitches_generated=len(pitches),
            deliverables_completed=total_deliverables,
            pipeline_value_generated_usd=pipeline_val,
            duration_sec=duration,
            details={
                "leads": [lead.business_name for lead in leads],
                "avg_health_score": sum(a.overall_health_score for a in audits) / len(audits) if audits else 0.0,
            },
        )
        self.history.append(report)
        return report

    def get_aggregate_summary(self) -> Dict[str, Any]:
        total_leads = sum(r.leads_hunted for r in self.history)
        total_pipeline = sum(r.pipeline_value_generated_usd for r in self.history)
        total_deliv = sum(r.deliverables_completed for r in self.history)

        return {
            "total_cycles_executed": len(self.history),
            "total_leads_processed": total_leads,
            "pipeline_value_usd": total_pipeline,
            "total_deliverables_created": total_deliv,
            "last_run_timestamp": self.history[-1].timestamp if self.history else None,
        }
