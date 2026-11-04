from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Callable, Generator, List, Dict, Any, Optional
from pydantic import BaseModel
from sqlmodel import Session, select
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
from omniverse.modules.bangalore.daemon import Bangalore247CashDaemon

class ScanClusterRequest(BaseModel):
    cluster: BangaloreCluster = BangaloreCluster.HSR_LAYOUT

class EvaluateListingRequest(BaseModel):
    raw_text: str

class RadarCheckoutRequest(BaseModel):
    name: str
    phone_whatsapp: str
    tier: RadarSubscriptionTier = RadarSubscriptionTier.PRO_RELOCATOR
    target_clusters: str = "HSR Layout,Koramangala,Indiranagar"
    preferred_bhk: int = 2
    max_budget_inr: float = 35000.0

class SettleRadarRequest(BaseModel):
    transaction_id: str
    name: str
    phone_whatsapp: str
    tier: RadarSubscriptionTier = RadarSubscriptionTier.PRO_RELOCATOR
    amount_inr: float = 499.0
    gateway_ref: Optional[str] = None

class SettleSMBRequest(BaseModel):
    client_id: int
    amount_inr: float
    gateway_ref: Optional[str] = None

def get_bangalore_router(session_factory: Callable[[], Generator[Session, None, None]]) -> APIRouter:
    router = APIRouter(prefix="/bangalore", tags=["Bangalore 24/7 Cashflow Engine"])

    @router.get("/status", response_model=BangaloreCashflowSummary)
    def get_bangalore_status(session: Session = Depends(session_factory)):
        daemon = Bangalore247CashDaemon(session)
        return daemon.get_summary()

    @router.get("/prospects", response_model=List[SMBGrowthClient])
    def get_prospects(
        cluster: Optional[BangaloreCluster] = None,
        session: Session = Depends(session_factory)
    ):
        query = select(SMBGrowthClient)
        if cluster:
            query = query.where(SMBGrowthClient.cluster == cluster)
        return session.exec(query).all()

    @router.post("/prospects/scan")
    def scan_prospects(
        req: ScanClusterRequest,
        session: Session = Depends(session_factory)
    ):
        engine = NammaBizEngine(session)
        clients = engine.scan_and_seed_cluster(req.cluster)
        kits = [engine.generate_growth_kit(c) for c in clients]
        return {
            "cluster": req.cluster.value,
            "count": len(clients),
            "prospects": kits
        }

    @router.get("/flat-radar/listings", response_model=List[RentalListing])
    def get_listings(
        zero_brokerage_only: bool = True,
        cluster: Optional[BangaloreCluster] = None,
        session: Session = Depends(session_factory)
    ):
        query = select(RentalListing)
        if zero_brokerage_only:
            query = query.where(RentalListing.is_zero_brokerage == True)
        if cluster:
            query = query.where(RentalListing.cluster == cluster)
        return session.exec(query.order_by(RentalListing.verified_at.desc())).all()

    @router.post("/flat-radar/evaluate")
    def evaluate_listing(
        req: EvaluateListingRequest,
        session: Session = Depends(session_factory)
    ):
        radar = BangaloreFlatRadar(session)
        is_zero_brokerage, confidence = radar.evaluate_listing_content(req.raw_text)
        return {
            "is_zero_brokerage": is_zero_brokerage,
            "broker_confidence": confidence,
            "verdict": "VERIFIED_DIRECT_OWNER" if is_zero_brokerage else "PROBABLE_BROKER_SPAM"
        }

    @router.post("/checkout/radar")
    def checkout_radar(
        req: RadarCheckoutRequest,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreUPIEngine(session)
        return engine.checkout_radar_subscription(
            name=req.name,
            phone_whatsapp=req.phone_whatsapp,
            tier=req.tier,
            target_clusters=req.target_clusters,
            preferred_bhk=req.preferred_bhk,
            max_budget_inr=req.max_budget_inr
        )

    @router.post("/settle/radar")
    def settle_radar(
        req: SettleRadarRequest,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreUPIEngine(session)
        txn, sub = engine.settle_radar_payment(
            transaction_id=req.transaction_id,
            name=req.name,
            phone_whatsapp=req.phone_whatsapp,
            tier=req.tier,
            amount_inr=req.amount_inr,
            gateway_ref=req.gateway_ref
        )
        receipt = engine.generate_cryptographic_receipt(txn)
        return {
            "status": "SETTLED",
            "transaction_id": txn.transaction_id,
            "amount_inr": txn.amount_inr,
            "vip_access_key": sub.vip_access_key,
            "pass_expires_at": sub.pass_expires_at,
            "hmac_receipt": receipt
        }

    @router.post("/settle/smb")
    def settle_smb(
        req: SettleSMBRequest,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreUPIEngine(session)
        try:
            txn, client = engine.settle_smb_retainer(
                client_id=req.client_id,
                amount_inr=req.amount_inr,
                gateway_ref=req.gateway_ref
            )
            receipt = engine.generate_cryptographic_receipt(txn)
            return {
                "status": "SETTLED",
                "transaction_id": txn.transaction_id,
                "amount_inr": txn.amount_inr,
                "client_name": client.business_name,
                "hmac_receipt": receipt
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.post("/daemon/cycle")
    def execute_daemon_cycle(
        cluster: BangaloreCluster = BangaloreCluster.HSR_LAYOUT,
        session: Session = Depends(session_factory)
    ):
        daemon = Bangalore247CashDaemon(session)
        result = daemon.run_cycle(cluster=cluster, simulate_listings=True)
        return result

    return router
