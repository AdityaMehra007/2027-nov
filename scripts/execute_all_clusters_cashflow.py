"""==============================================================================
ALL-CLUSTER REVENUE RUNNER & GROWTH KIT EXPORTER
==============================================================================
Executes 24/7 revenue cycles across all Bangalore commercial clusters:
- HSR Layout
- Koramangala
- Indiranagar
- Whitefield
Settles UPI transactions, matches radar alerts, and exports client growth kits.
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.core.database import DatabaseEngine
from omniverse.modules.bangalore.models import (
    BangaloreCluster,
    RadarSubscriptionTier,
    SMBTier,
)
from omniverse.modules.bangalore.daemon import Bangalore247CashDaemon
from omniverse.modules.bangalore.radar import BangaloreFlatRadar
from omniverse.modules.bangalore.smb_engine import NammaBizEngine
from omniverse.modules.bangalore.payment_engine import BangaloreUPIEngine

def run_all_clusters():
    print("=" * 70)
    print("  🚀 CASHFLOW INFINITY: ALL-CLUSTER WEALTH RUNNER")
    print("=" * 70)

    db = DatabaseEngine()
    db.init_db()

    export_dir = Path("data/growth_kits")
    export_dir.mkdir(parents=True, exist_ok=True)

    with db.get_session() as session:
        daemon = Bangalore247CashDaemon(session)
        smb_engine = NammaBizEngine(session)
        radar = BangaloreFlatRadar(session)
        upi = BangaloreUPIEngine(session)

        clusters = [
            BangaloreCluster.HSR_LAYOUT,
            BangaloreCluster.KORAMANGALA,
            BangaloreCluster.INDIRANAGAR,
            BangaloreCluster.WHITEFIELD,
        ]

        total_prospects = 0
        total_settled_inr = 0.0

        for cluster in clusters:
            print(f"\n[CLUSTER SCAN] >>> {cluster.value.upper()}")
            # Run daemon cycle
            res = daemon.run_cycle(cluster=cluster, simulate_listings=True)
            print(f"  • Cycle #{res['cycle_number']} executed")
            print(f"  • Prospects Discovered: {res['smb_prospects_found']}")
            print(f"  • Listings Processed  : {res['listings_processed']}")
            print(f"  • VIP Alerts Sent     : {res['alerts_dispatched']}")

            # Seed and get clients
            clients = smb_engine.scan_and_seed_cluster(cluster)
            total_prospects += len(clients)

            for client in clients:
                kit = smb_engine.generate_growth_kit(client)
                kit_file = export_dir / f"{cluster.value}_{client.id}_growth_kit.md"
                md_content = f"""# SMB Growth Kit: {client.business_name}
**Cluster**: {client.cluster.value.title()}  
**Tier**: {client.tier.value}  
**Monthly Retainer**: ₹{client.monthly_fee_inr:,.0f}/month  
**WhatsApp Outreach Link**: [Launch Chat]({client.pitch_url})  

## Conversion Hooks
"""
                for hook in kit.get("social_hooks", []):
                    md_content += f"- {hook}\n"
                
                md_content += "\n## Audit Observations\n"
                for audit in kit.get("audit_items", []):
                    md_content += f"- {audit}\n"

                kit_file.write_text(md_content, encoding="utf-8")

                # Settle first client in each cluster as an active paying client
                if client == clients[0]:
                    settled, _ = upi.settle_smb_retainer(client.id, client.monthly_fee_inr)
                    if settled:
                        total_settled_inr += client.monthly_fee_inr
                        print(f"  💰 Retainer Settled: ₹{client.monthly_fee_inr:,.0f} from {client.business_name}")

            # Settle a simulated Flat Radar VIP pass in each cluster
            order = upi.checkout_radar_subscription(
                name=f"Tech Founder ({cluster.value.title()})",
                phone_whatsapp=f"+91-987654321{clusters.index(cluster)}",
                tier=RadarSubscriptionTier.PRO_RELOCATOR,
                target_clusters=cluster.value
            )
            upi.settle_radar_payment(
                transaction_id=order["transaction_id"],
                name=order["subscriber_name"],
                phone_whatsapp=order["phone_whatsapp"],
                tier=RadarSubscriptionTier.PRO_RELOCATOR,
                amount_inr=order["amount_inr"],
                target_clusters=cluster.value
            )
            total_settled_inr += order["amount_inr"]
            print(f"  ⚡ Settled VIP Pass: ₹{order['amount_inr']:,.2f} for {order['transaction_id']}")

        session.commit()

        # Telemetry summary
        summary = daemon.get_summary()
        print("\n" + "=" * 70)
        print("  📊 GLOBAL WEALTH RUNNER SUMMARY")
        print("=" * 70)
        print(f"  Daily Cash Collected: ₹{summary.daily_cash_collected_inr:,.2f}")
        print(f"  Monthly Recurring   : ₹{summary.mrr_inr:,.2f}")
        print(f"  Annual Projected RR : ₹{summary.projected_annual_runrate_inr:,.2f} / yr")
        print(f"  Active SMB Retainers: {summary.active_smb_retainers}")
        print(f"  Active VIP Hunters  : {summary.active_radar_subscribers}")
        print(f"  Total Pipeline Value: ₹{summary.total_pipeline_inr:,.2f}")
        print(f"  Total Kits Exported : {total_prospects} kits in {export_dir}")
        print("=" * 70)

if __name__ == "__main__":
    run_all_clusters()
