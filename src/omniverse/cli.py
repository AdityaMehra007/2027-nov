import argparse
import sys
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from omniverse.core.database import get_engine, init_db
from omniverse.core.config import get_settings
from omniverse.operations.health import HealthDiagnostics
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow

def main():
    parser = argparse.ArgumentParser(description="CASHFLOW INFINITY: OMNIVERSE Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: status
    subparsers.add_parser("status", help="Display system status, health, and financials")

    # Command: generate-kit
    kit_parser = subparsers.add_parser("generate-kit", help="Generate local business growth kit")
    kit_parser.add_argument("--business", required=True, help="Business name")
    kit_parser.add_argument("--niche", required=True, help="Industry / Niche")
    kit_parser.add_argument("--city", default="Bengaluru", help="Target city")

    # Command: leads
    subparsers.add_parser("leads", help="List all CRM leads")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Start FastAPI Command Center")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host address")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number")

    args = parser.parse_args()

    init_db()
    engine = get_engine()

    if args.command == "status":
        with engine.get_session() as session:
            diagnostics = HealthDiagnostics(session)
            health = diagnostics.run_diagnostics()
            pipeline = LeadPipeline(session)
            pipe_summary = pipeline.get_pipeline_summary()
            payments = PaymentWorkflow(session)
            ledger = payments.get_financial_ledger()

            print("==================================================")
            print("  CASHFLOW INFINITY: OMNIVERSE STATUS")
            print("==================================================")
            print(f"Overall Status   : {health['overall_status']}")
            print(f"Database Status  : {health['database_status']}")
            print(f"Disk Available   : {health['disk_available_gb']} GB")
            print(f"Memory Usage     : {health['memory_usage_mb']} MB")
            print("--------------------------------------------------")
            print(f"Total Leads      : {pipe_summary['total_leads']}")
            print(f"Pipeline Value   : ₹{pipe_summary['pipeline_value_inr']:,.2f}")
            print(f"Collected Revenue: ₹{ledger['collected_revenue_inr']:,.2f}")
            print(f"Outstanding Recv : ₹{ledger['outstanding_receivables_inr']:,.2f}")
            print("==================================================")

    elif args.command == "generate-kit":
        generator = GrowthKitGenerator()
        kit = generator.generate(
            business_name=args.business,
            niche=args.niche,
            city=args.city
        )
        print("\n=== LOCAL BUSINESS GROWTH KIT ===")
        print(f"Business: {kit.business_name} | Niche: {kit.niche} | City: {kit.city}\n")
        print("--- OUTREACH PITCH ---")
        print(kit.outreach_pitch)
        print("\n--- SOCIAL CAPTIONS (Sample) ---")
        for i, cap in enumerate(kit.social_captions[:3], 1):
            print(f"{i}. {cap}")
        print(f"... and {len(kit.social_captions) - 3} more captions.")
        print("\n--- PROMOTIONAL HOOKS ---")
        for i, hook in enumerate(kit.promotional_hooks, 1):
            print(f"{i}. {hook}")

    elif args.command == "leads":
        with engine.get_session() as session:
            pipeline = LeadPipeline(session)
            leads = pipeline.list_leads()
            if not leads:
                print("No leads recorded yet. Generate kits and add prospects!")
            else:
                for l in leads:
                    print(f"[{l.id}] {l.business_name} ({l.category}) - {l.status.value} - ₹{l.estimated_value_inr:,.0f}")

    elif args.command == "serve":
        import uvicorn
        from omniverse.api.app import create_app
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
