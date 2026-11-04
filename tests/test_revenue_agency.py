import pytest
from pathlib import Path
from sqlmodel import Session, select
from omniverse.modules.revenue.models import Lead, LeadStage, Offer, GrowthKit
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.exporter import GrowthKitExporter

def test_growth_kit_generation():
    generator = GrowthKitGenerator()
    kit = generator.generate(
        business_name="Spice Garden Bistro",
        niche="Restaurant / Fine Dining",
        city="Bengaluru"
    )
    
    assert isinstance(kit, GrowthKit)
    assert kit.business_name == "Spice Garden Bistro"
    assert len(kit.social_captions) == 10
    assert len(kit.promotional_hooks) == 5
    assert len(kit.whatsapp_catalog_copy) > 0
    assert "Spice Garden Bistro" in kit.outreach_pitch

def test_growth_kit_exporter(tmp_path):
    generator = GrowthKitGenerator()
    kit = generator.generate("Zenith Dental Clinic", "Dental Healthcare", "Bengaluru")
    
    exporter = GrowthKitExporter()
    out_file = tmp_path / "zenith_proposal.md"
    written_path = exporter.export_markdown(kit, out_file)
    
    assert written_path.exists()
    content = written_path.read_text(encoding="utf-8")
    assert "Zenith Dental Clinic" in content
    assert "WhatsApp" in content
    
    wa_url = exporter.generate_whatsapp_click_url("919876543210", kit.outreach_pitch)
    assert wa_url.startswith("https://wa.me/919876543210?text=")

def test_lead_and_offer_models(test_db: Session):
    lead = Lead(
        business_name="FitPulse Gym",
        category="Fitness & Wellness",
        city="Bengaluru",
        contact_person="Rohan Mehta",
        contact_channel="WhatsApp",
        status=LeadStage.NEW,
        estimated_value_inr=25000.0
    )
    test_db.add(lead)
    test_db.commit()
    test_db.refresh(lead)
    
    assert lead.id is not None
    assert lead.status == LeadStage.NEW
    
    offer = Offer(
        title="Local Business Growth Kit",
        niche="Retail & Hospitality",
        price_inr=15000.0,
        deliverables_summary="10 captions, WhatsApp catalog, 5 promotional hooks, pitch deck"
    )
    test_db.add(offer)
    test_db.commit()
    test_db.refresh(offer)
    
    assert offer.id is not None
    assert offer.price_inr == 15000.0
