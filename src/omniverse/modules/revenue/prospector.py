from typing import List, Tuple
from sqlmodel import Session
from omniverse.modules.revenue.models import Lead, LeadStage, GrowthKit
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.pipeline import LeadPipeline

class LocalProspector:
    """Discovers and qualifies local SMBs in high-density commercial clusters."""

    _NEIGHBORHOOD_PATTERNS = {
        "Indiranagar": ["100ft Road", "12th Main", "CMH Road", "HAL 2nd Stage"],
        "Koramangala": ["4th Block", "5th Block", "80ft Road", "Sony World Signal"],
        "Whitefield": ["ITPB Main Road", "ECC Road", "Hope Farm", "Varthur Road"],
        "HSR Layout": ["27th Main", "Sector 1", "Sector 2", "Agara Junction"]
    }

    def __init__(self, session: Session):
        self.session = session
        self.pipeline = LeadPipeline(session)
        self.generator = GrowthKitGenerator()

    def scan_cluster(
        self,
        city: str = "Bengaluru",
        cluster: str = "Indiranagar",
        niche: str = "Specialty Cafe",
        limit: int = 3
    ) -> List[Lead]:
        landmarks = self._NEIGHBORHOOD_PATTERNS.get(cluster, ["Main Road", "Central Plaza", "Commercial Complex"])
        created_leads: List[Lead] = []

        for i in range(min(limit, len(landmarks))):
            biz_name = f"{cluster} {niche} @ {landmarks[i]}"
            lead = self.pipeline.create_lead(
                business_name=biz_name,
                category=niche,
                city=city,
                estimated_value_inr=18000.0 + (i * 2500.0),
                contact_person=f"Store Manager ({cluster})",
                contact_channel="WhatsApp",
                contact_info=f"+91-98800{i:05d}"
            )
            created_leads.append(lead)

        return created_leads

    def prospect_and_generate_kit(
        self,
        business_name: str,
        niche: str,
        city: str = "Bengaluru"
    ) -> Tuple[Lead, GrowthKit]:
        lead = self.pipeline.create_lead(
            business_name=business_name,
            category=niche,
            city=city,
            estimated_value_inr=22000.0,
            contact_channel="WhatsApp"
        )
        kit = self.generator.generate(business_name, niche, city)
        return lead, kit
