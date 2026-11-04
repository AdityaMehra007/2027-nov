import argparse
import sys
import json
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.core.database import get_engine, init_db
from omniverse.core.config import get_settings
from omniverse.operations.health import HealthDiagnostics
from omniverse.operations.reporter import ExecutiveReportGenerator
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.exporter import GrowthKitExporter
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.geocoder import AetherGeocoder
from omniverse.modules.aether.models import HazardType
from omniverse.modules.intelligence.quant_engine import Backtester
from omniverse.modules.saas_factory.scaffolder import SaaSFactoryScaffolder

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
    kit_parser.add_argument("--export", action="store_true", help="Export to markdown proposal file")

    # Command: leads
    subparsers.add_parser("leads", help="List all CRM leads")

    # Command: aether-risk
    risk_parser = subparsers.add_parser("aether-risk", help="Assess Aether geospatial resilience and climate hazard")
    risk_parser.add_argument("--city", default=None, help="City to geocode")
    risk_parser.add_argument("--lat", type=float, default=12.9716, help="Latitude")
    risk_parser.add_argument("--lon", type=float, default=77.5946, help="Longitude")
    risk_parser.add_argument("--elevation", type=float, default=920.0, help="Elevation in meters")
    risk_parser.add_argument("--hazard", default="FLOOD", help="Hazard type (FLOOD, SEISMIC, HEAT_STRESS)")

    # Command: scaffold-saas
    saas_parser = subparsers.add_parser("scaffold-saas", help="Scaffold a micro-SaaS application")
    saas_parser.add_argument("--name", required=True, help="Application name")
    saas_parser.add_argument("--dir", default="./generated_saas", help="Output directory")

    # Command: backtest
    bt_parser = subparsers.add_parser("backtest", help="Run quantitative multi-strategy backtest")
    bt_parser.add_argument("--strategy", default="trend", choices=["trend", "sma", "monte-carlo"])

    # Command: daily-brief
    subparsers.add_parser("daily-brief", help="Generate executive daily briefing report")

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

        exporter = GrowthKitExporter()
        wa_url = exporter.generate_whatsapp_click_url("919999999999", kit.outreach_pitch)
        print("\n--- ONE-CLICK WHATSAPP LAUNCH URL ---")
        print(wa_url)

        if args.export:
            slug = args.business.lower().replace(" ", "_")
            out_file = Path(f"./reports/proposals/{slug}_proposal.md")
            saved_path = exporter.export_markdown(kit, out_file)
            print(f"\n✅ Exported branded client proposal deck to: {saved_path}")

    elif args.command == "aether-risk":
        lat = args.lat
        lon = args.lon
        elev = args.elevation

        if args.city:
            geocoder = AetherGeocoder()
            loc = geocoder.geocode(args.city)
            lat = loc["lat"]
            lon = loc["lon"]
            elev = loc["elevation_meters"]
            print(f"📍 Geocoded '{args.city}' -> {loc['display_name']} ({lat}, {lon})")

        hazard_enum = getattr(HazardType, args.hazard.upper(), HazardType.FLOOD)
        engine_risk = AetherRiskEngine()
        assessment = engine_risk.evaluate_location_risk(
            lat=lat,
            lon=lon,
            elevation_meters=elev,
            hazard_type=hazard_enum
        )
        print("\n==================================================")
        print("  AETHER RESILIENCE FABRIC — RISK ASSESSMENT")
        print("==================================================")
        print(f"Coordinates    : ({assessment.latitude}, {assessment.longitude})")
        print(f"Hazard Analyzed: {assessment.hazard_type.value}")
        print(f"Risk Level     : {assessment.risk_level.value}")
        print(f"Vulnerability  : {assessment.vulnerability_index} / 100")
        print("--------------------------------------------------")
        print("Recommendations:")
        for r in assessment.actionable_recommendations:
            print(f" • {r}")
        print("==================================================")

    elif args.command == "scaffold-saas":
        scaffolder = SaaSFactoryScaffolder()
        res = scaffolder.scaffold_project(args.name, Path(args.dir))
        print(f"✅ Successfully scaffolded micro-SaaS '{args.name}' in {res['target_dir']}")

    elif args.command == "backtest":
        backtester = Backtester()
        sample_prices = [100.0, 102.5, 101.8, 106.0, 110.2, 108.5, 115.0, 122.4, 124.0, 128.5]
        if args.strategy == "trend":
            res = backtester.run_trend_following_backtest(sample_prices)
            print("\n=== TREND FOLLOWING BACKTEST ===")
            print(f"Total Return % : {res['total_return_pct']}%")
            print(f"Sharpe Ratio   : {res['sharpe_ratio']}")
            print(f"Max Drawdown % : {res['max_drawdown_pct']}%")
        elif args.strategy == "sma":
            res = backtester.run_moving_average_crossover(sample_prices, fast_period=2, slow_period=4)
            print("\n=== SMA CROSSOVER BACKTEST ===")
            print(f"Total Return % : {res['total_return_pct']}%")
            print(f"Trades Count   : {res['trades_count']}")
            print(f"Win Rate %     : {res['win_rate_pct']}%")
        elif args.strategy == "monte-carlo":
            res = backtester.run_monte_carlo_var(sample_prices, num_simulations=500, horizon_days=30)
            print("\n=== MONTE CARLO VALUE-AT-RISK (VaR) ===")
            print(f"VaR 95% (10d)  : {res['var_95_pct']}%")
            print(f"VaR 99% (10d)  : {res['var_99_pct']}%")
            print(f"Expected CVaR  : {res['expected_shortfall_cvar_pct']}%")

    elif args.command == "daily-brief":
        with engine.get_session() as session:
            reporter = ExecutiveReportGenerator(session)
            brief_file = reporter.generate_daily_brief()
            print(f"\n✅ Executive Daily Briefing compiled and saved to: {brief_file}")
            print("==================================================")
            print(brief_file.read_text(encoding="utf-8")[:500] + "...\n[Full briefing in file]")
            print("==================================================")

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
