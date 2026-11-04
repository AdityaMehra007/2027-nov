import time
import uuid
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select, func
from omniverse.modules.bangalore.models import (
    BangaloreCluster,
    SMBGrowthClient,
    RentalListing,
    FlatRadarSubscriber,
    BangaloreCashTransaction,
    BangaloreCashflowSummary,
    RadarSubscriptionTier,
)
from omniverse.modules.bangalore.radar import BangaloreFlatRadar
from omniverse.modules.bangalore.smb_engine import NammaBizEngine
from omniverse.modules.bangalore.payment_engine import BangaloreUPIEngine
from omniverse.core.telemetry import global_event_bus

class Bangalore247CashDaemon:
    """The 24/7 Autonomous Money-Making Engine for Bengaluru.

    Coordinates continuous SMB client discovery, WhatsApp pitch dispatch,
    zero-brokerage rental alert routing, and real-time UPI revenue collection.
    """

    def __init__(self, session: Session):
        self.session = session
        try:
            from sqlmodel import SQLModel
            import omniverse.modules.bangalore.models  # ensure models registered
            bind = session.get_bind()
            if bind is not None:
                SQLModel.metadata.create_all(bind)
        except Exception:
            pass

        self.radar = BangaloreFlatRadar(session)
        self.smb_engine = NammaBizEngine(session)
        self.payment_engine = BangaloreUPIEngine(session)
        self.start_time = time.time()
        self.cycles_executed = 0

    def run_cycle(
        self,
        cluster: BangaloreCluster = BangaloreCluster.HSR_LAYOUT,
        simulate_listings: bool = True
    ) -> Dict[str, Any]:
        """Executes a single 24/7 revenue & operational cycle in Bengaluru."""
        self.cycles_executed += 1
        cycle_start = time.time()

        # 1. Commercial Scan: Discover SMBs in target cluster
        smb_prospects = self.smb_engine.scan_and_seed_cluster(cluster)

        # 2. Flat Radar: Ingest listings and match active subscribers
        new_listings_count = 0
        matched_alerts: List[Dict[str, Any]] = []

        if simulate_listings:
            listings = self.radar.generate_simulated_bangalore_feed()
            new_listings_count = len(listings)
            for listing in listings:
                alerts = self.radar.match_subscribers(listing)
                matched_alerts.extend(alerts)

        # 3. Compute Real-Time Cashflow Summary
        summary = self.get_summary()

        global_event_bus.publish("BANGALORE_DAEMON_CYCLE_COMPLETED", {
            "cycle_number": self.cycles_executed,
            "cluster": cluster.value,
            "prospects": len(smb_prospects),
            "listings": new_listings_count,
            "alerts_dispatched": len(matched_alerts),
            "daily_cash_inr": summary.daily_cash_collected_inr,
            "duration_ms": round((time.time() - cycle_start) * 1000, 2)
        })

        return {
            "cycle_number": self.cycles_executed,
            "cluster": cluster.value,
            "smb_prospects_found": len(smb_prospects),
            "listings_processed": new_listings_count,
            "alerts_dispatched": len(matched_alerts),
            "matched_alerts": matched_alerts,
            "summary": summary.model_dump()
        }

    def get_summary(self) -> BangaloreCashflowSummary:
        """Calculates 24/7 Bangalore revenue metrics."""
        now = time.time()
        one_day_ago = now - 86400.0

        # Daily collected cash
        recent_txns = self.session.exec(
            select(BangaloreCashTransaction).where(
                BangaloreCashTransaction.settled_at >= one_day_ago,
                BangaloreCashTransaction.status == "SETTLED"
            )
        ).all()
        daily_cash = sum(t.amount_inr for t in recent_txns)

        # Active SMB retainers
        active_smbs = self.session.exec(
            select(SMBGrowthClient).where(
                SMBGrowthClient.is_active == True,
                SMBGrowthClient.status == "ACTIVE_RETAINER"
            )
        ).all()
        smb_mrr = sum(c.monthly_fee_inr for c in active_smbs)

        # Active Radar Subscribers
        active_subs = self.session.exec(
            select(FlatRadarSubscriber).where(
                FlatRadarSubscriber.is_active == True,
                FlatRadarSubscriber.pass_expires_at > now
            )
        ).all()
        subs_mrr = sum(s.total_paid_inr for s in active_subs)

        # Potential SMB Pipeline
        pipeline_smbs = self.session.exec(
            select(SMBGrowthClient).where(SMBGrowthClient.status == "PROSPECT")
        ).all()
        pipeline_value = sum(c.monthly_fee_inr for c in pipeline_smbs)

        total_mrr = smb_mrr + subs_mrr
        annual_runrate = total_mrr * 12.0
        uptime_hours = round((now - self.start_time) / 3600.0, 2)

        hotspots = [
            BangaloreCluster.KORAMANGALA.value,
            BangaloreCluster.INDIRANAGAR.value,
            BangaloreCluster.HSR_LAYOUT.value,
            BangaloreCluster.WHITEFIELD.value,
            BangaloreCluster.BELLANDUR.value,
        ]

        return BangaloreCashflowSummary(
            city="Bengaluru",
            daily_cash_collected_inr=daily_cash,
            mrr_inr=total_mrr,
            active_smb_retainers=len(active_smbs),
            active_radar_subscribers=len(active_subs),
            total_pipeline_inr=pipeline_value,
            projected_annual_runrate_inr=annual_runrate,
            system_uptime_hours=uptime_hours,
            cluster_hotspots=hotspots,
            status="RUNNING_24_7"
        )
