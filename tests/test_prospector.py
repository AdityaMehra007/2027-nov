import pytest
from sqlmodel import Session
from omniverse.modules.revenue.prospector import LocalProspector
from omniverse.modules.revenue.models import LeadStage

def test_local_prospector_scan(test_db: Session):
    prospector = LocalProspector(session=test_db)
    leads = prospector.scan_cluster(
        city="Bengaluru",
        cluster="Indiranagar",
        niche="Specialty Cafe",
        limit=3
    )
    
    assert len(leads) == 3
    for lead in leads:
        assert lead.id is not None
        assert "Indiranagar" in lead.business_name
        assert lead.status == LeadStage.NEW
        assert lead.estimated_value_inr >= 15000.0

def test_prospector_auto_kit_generation(test_db: Session):
    prospector = LocalProspector(session=test_db)
    lead, kit = prospector.prospect_and_generate_kit(
        business_name="Artisan Sourdough Bakery",
        niche="Bakery",
        city="Bengaluru"
    )
    
    assert lead.id is not None
    assert kit.business_name == "Artisan Sourdough Bakery"
    assert len(kit.social_captions) == 10
