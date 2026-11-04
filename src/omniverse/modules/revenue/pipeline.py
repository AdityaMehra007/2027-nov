from sqlmodel import Session, select
from typing import List, Dict, Any, Optional
import time
from omniverse.modules.revenue.models import Lead, LeadStage
from omniverse.core.telemetry import global_event_bus

class LeadPipeline:
    """Manages SMB customer prospecting, qualification, and stage advancement."""

    def __init__(self, session: Session):
        self.session = session

    def create_lead(
        self,
        business_name: str,
        category: str,
        city: str = "Bengaluru",
        estimated_value_inr: float = 0.0,
        contact_person: Optional[str] = None,
        contact_channel: str = "WhatsApp",
        contact_info: Optional[str] = None
    ) -> Lead:
        lead = Lead(
            business_name=business_name,
            category=category,
            city=city,
            estimated_value_inr=estimated_value_inr,
            contact_person=contact_person,
            contact_channel=contact_channel,
            contact_info=contact_info,
            status=LeadStage.NEW
        )
        self.session.add(lead)
        self.session.commit()
        self.session.refresh(lead)

        global_event_bus.publish("LEAD_CREATED", {
            "lead_id": lead.id,
            "business_name": lead.business_name,
            "estimated_value_inr": lead.estimated_value_inr
        })
        return lead

    def advance_stage(self, lead_id: int, new_stage: LeadStage, notes: Optional[str] = None) -> Lead:
        lead = self.session.get(Lead, lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        old_stage = lead.status
        lead.status = new_stage
        lead.updated_at = time.time()
        if notes:
            lead.notes = f"{lead.notes or ''}\n[{new_stage.value}]: {notes}".strip()

        self.session.add(lead)
        self.session.commit()
        self.session.refresh(lead)

        global_event_bus.publish("LEAD_STAGE_CHANGED", {
            "lead_id": lead.id,
            "old_stage": old_stage.value,
            "new_stage": new_stage.value
        })
        return lead

    def list_leads(self, status: Optional[LeadStage] = None) -> List[Lead]:
        query = select(Lead)
        if status:
            query = query.where(Lead.status == status)
        return list(self.session.exec(query).all())

    def get_pipeline_summary(self) -> Dict[str, Any]:
        leads = list(self.session.exec(select(Lead)).all())
        total = len(leads)
        won = sum(1 for l in leads if l.status == LeadStage.WON)
        value = sum(l.estimated_value_inr for l in leads)

        by_stage = {stage.value: 0 for stage in LeadStage}
        for l in leads:
            by_stage[l.status.value] += 1

        return {
            "total_leads": total,
            "won_count": won,
            "pipeline_value_inr": value,
            "stages": by_stage
        }
