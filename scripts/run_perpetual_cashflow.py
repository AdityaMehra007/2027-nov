"""==============================================================================
24/7 PERPETUAL AUTONOMOUS CASHFLOW ENGINE
==============================================================================
Master perpetual daemon runner that continuously coordinates:
1. Hourly commercial SMB discovery & Growth Kit compilation.
2. Real-time zero-brokerage Flat Radar listing sweeps and VIP alert dispatch.
3. Dual-ledger payment settlement & webhook reconciliation.
4. Quantitative portfolio risk monitoring.
5. Autonomous codebase self-healing and health auditing.
6. Daily executive briefing compilation.
==============================================================================
"""

import sys
import time
import signal
import logging
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.core.database import DatabaseEngine
from omniverse.modules.bangalore.models import BangaloreCluster, RadarSubscriptionTier
from omniverse.modules.bangalore.daemon import Bangalore247CashDaemon
from omniverse.modules.bangalore.radar import BangaloreFlatRadar
from omniverse.modules.bangalore.smb_engine import NammaBizEngine
from omniverse.modules.bangalore.payment_engine import BangaloreUPIEngine
from omniverse.operations.health import HealthDiagnostics
from omniverse.operations.reporter import ExecutiveReporter

# Setup logging
log_dir = Path("data/logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "cashflow_daemon.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OmniDaemon")

running = True

def handle_signal(sig, frame):
    global running
    logger.info("Received termination signal. Gracefully stopping daemon...")
    running = False

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def run_perpetual_daemon(interval_seconds: int = 60, max_cycles: int = 5):
    logger.info("=" * 70)
    logger.info("🚀 LAUNCHING 24/7 PERPETUAL AUTONOMOUS CASHFLOW ENGINE")
    logger.info(f"   Cycle Interval: {interval_seconds}s | Max Test Cycles: {max_cycles}")
    logger.info("=" * 70)

    db = DatabaseEngine()
    db.init_db()

    cycle_count = 0

    with db.get_session() as session:
        daemon = Bangalore247CashDaemon(session)
        smb_engine = NammaBizEngine(session)
        radar = BangaloreFlatRadar(session)
        upi = BangaloreUPIEngine(session)
        health = HealthDiagnostics(session)
        reporter = ExecutiveReporter(session)

        clusters = [
            BangaloreCluster.HSR_LAYOUT,
            BangaloreCluster.KORAMANGALA,
            BangaloreCluster.INDIRANAGAR,
            BangaloreCluster.WHITEFIELD
        ]

        while running and (max_cycles <= 0 or cycle_count < max_cycles):
            cycle_count += 1
            cluster = clusters[(cycle_count - 1) % len(clusters)]
            logger.info(f"\n[DAEMON CYCLE #{cycle_count}] Target Cluster: {cluster.value.upper()}")

            # 1. Run Revenue Cycle
            res = daemon.run_cycle(cluster=cluster, simulate_listings=True)
            logger.info(f"  • Scanned {res['smb_prospects_found']} SMBs | Processed {res['listings_processed']} listings | Alerts: {res['alerts_dispatched']}")

            # 2. Check System Health
            h_stat = health.run_diagnostics()
            logger.info(f"  • System Health: {h_stat['overall_status']} (DB: {h_stat['database_status']}, RAM: {h_stat['memory_usage_mb']}MB)")

            # 3. Ledger Snapshot
            summary = daemon.get_summary()
            logger.info(f"  • Daily Cash: ₹{summary.daily_cash_collected_inr:,.2f} | MRR: ₹{summary.mrr_inr:,.2f} | Run-Rate: ₹{summary.projected_annual_runrate_inr:,.2f}/yr")

            session.commit()

            if max_cycles > 0 and cycle_count >= max_cycles:
                logger.info("Reached maximum requested daemon test cycles.")
                break

            if running:
                logger.info(f"Sleeping {interval_seconds}s until next operational pulse...")
                time.sleep(interval_seconds)

        # Final executive report snapshot
        brief = reporter.generate_daily_briefing()
        brief_file = Path("reports/daily_briefing_latest.md")
        brief_file.parent.mkdir(parents=True, exist_ok=True)
        brief_file.write_text(brief, encoding="utf-8")
        logger.info(f"✅ Master executive briefing compiled: {brief_file}")

    logger.info("=" * 70)
    logger.info("🏁 PERPETUAL DAEMON SHUTDOWN CLEANLY COMPLETED")
    logger.info("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="24/7 Autonomous Cashflow Daemon")
    parser.add_argument("--interval", type=int, default=1, help="Seconds between cycles (default: 1s for tests)")
    parser.add_argument("--cycles", type=int, default=4, help="Number of cycles to run (0 for infinite)")
    args = parser.parse_args()

    run_perpetual_daemon(interval_seconds=args.interval, max_cycles=args.cycles)
