#!/usr/bin/env python3
"""Example 01: Autonomous Revenue Agency & Prospecting Workflow.

Demonstrates scanning local commercial clusters, generating branded growth kits,
and producing one-click WhatsApp client outreach links.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pathlib import Path
from omniverse.core.database import DatabaseEngine
from omniverse.modules.revenue.prospector import LocalProspector
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.exporter import GrowthKitExporter

def main():
    print("================================================================")
    print("  01. AUTONOMOUS LOCAL AGENCY & GROWTH KIT GENERATOR")
    print("================================================================")

    # 1. Initialize temporary in-memory database
    db_engine = DatabaseEngine("sqlite:///:memory:")
    db_engine.init_db()

    with db_engine.get_session() as session:
        # 2. Discover high-density SMB prospects in Indiranagar tech corridor
        print("\n🔍 Step 1: Scanning Indiranagar cluster for prospective clients...")
        prospector = LocalProspector(session)
        leads = prospector.scan_cluster(cluster="Indiranagar", niche="Specialty Cafe", limit=2)
        for lead in leads:
            print(f" • Found: {lead.business_name} | Est. Value: ₹{lead.estimated_value_inr:,.0f} | Contact: {lead.contact_info}")

        # 3. Generate tailored growth kit for the first lead
        lead = leads[0]
        print(f"\n🚀 Step 2: Generating AI Growth Kit for '{lead.business_name}'...")
        generator = GrowthKitGenerator()
        kit = generator.generate(
            business_name=lead.business_name,
            niche=lead.category,
            city="Bengaluru"
        )

        print("\n--- OUTREACH HOOK ---")
        print(kit.outreach_pitch)

        print("\n--- SOCIAL CAMPAIGN (First 2 Days) ---")
        for i, caption in enumerate(kit.social_captions[:2], 1):
            print(f" Day {i}: {caption}")

        # 4. Generate one-click WhatsApp link and export proposal
        exporter = GrowthKitExporter()
        wa_link = exporter.generate_whatsapp_click_url("919876543210", kit.outreach_pitch)
        print("\n--- ONE-CLICK WHATSAPP OUTREACH URL ---")
        print(wa_link)

        out_path = Path("./reports/proposals/example_demo_proposal.md")
        saved_file = exporter.export_markdown(kit, out_path)
        print(f"\n✅ Proposal exported to: {saved_file}")
        print("================================================================")

if __name__ == "__main__":
    main()
