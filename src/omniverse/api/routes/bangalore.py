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
    CompanyTier,
    TechRole,
    SalaryBenchmark,
    ClusterLivingAnalysis,
    MoneyFlowSimulationResult,
    ProjectArchetype,
)
from omniverse.modules.bangalore.radar import BangaloreFlatRadar
from omniverse.modules.bangalore.smb_engine import NammaBizEngine
from omniverse.modules.bangalore.payment_engine import BangaloreUPIEngine
from omniverse.modules.bangalore.daemon import Bangalore247CashDaemon
from omniverse.modules.bangalore.salary_benchmarking import (
    get_salary_benchmark,
    compare_tiers,
)
from omniverse.modules.bangalore.cost_of_living import (
    analyze_cluster_living,
    get_cluster_col,
)
from omniverse.modules.bangalore.banking import (
    BankCategory,
    BankingCorridor,
    FitoutGrade,
    BangaloreBankOffice,
    GCCCapexOpexModel,
    RBIAuditResult,
    BangaloreBankingEngine,
)
from omniverse.modules.bangalore.money_flow import simulate_capital_flow
from omniverse.modules.bangalore.projects import (
    get_project_archetypes,
    get_project_by_id,
)

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

class ColSimulateRequest(BaseModel):
    cluster: BangaloreCluster = BangaloreCluster.HSR_LAYOUT
    bhk: int = 2
    company_tier: CompanyTier = CompanyTier.TIER_1_GCC
    role: TechRole = TechRole.SDE_2
    experience_years: Optional[float] = None

class MoneyFlowSimulateRequest(BaseModel):
    inflow_amount_inr: float = 100000000.0
    source: str = "GCC_OPEX"

class GCCBlueprintRequest(BaseModel):
    seats: int = 1500
    corridor: BankingCorridor = BankingCorridor.OUTER_RING_ROAD
    fitout_grade: FitoutGrade = FitoutGrade.ULTRA_GRADE_A_FINANCIAL

class RBIAuditRequest(BaseModel):
    bank_name: str
    data_localized: bool = True
    dpdp_consent: bool = True
    cert_in_6hr: bool = True
    npl_clock_sync: bool = True
    vault_cctv_90day: bool = True


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

    # --- Economic & Salary Benchmarking Endpoints ---

    @router.get("/salary-benchmarks", response_model=SalaryBenchmark)
    def get_salary_benchmarks(
        tier: CompanyTier = CompanyTier.TIER_1_GCC,
        role: TechRole = TechRole.SDE_2,
        experience_years: Optional[float] = None,
    ):
        return get_salary_benchmark(tier=tier, role=role, experience_years=experience_years)

    @router.get("/salary-compare", response_model=List[SalaryBenchmark])
    def get_salary_comparison(
        role: TechRole = TechRole.SDE_2,
        experience_years: Optional[float] = None,
    ):
        return compare_tiers(role=role, experience_years=experience_years)

    @router.post("/col-simulate", response_model=ClusterLivingAnalysis)
    def simulate_cost_of_living(req: ColSimulateRequest):
        salary = get_salary_benchmark(
            tier=req.company_tier,
            role=req.role,
            experience_years=req.experience_years
        )
        return analyze_cluster_living(
            cluster=req.cluster,
            bhk=req.bhk,
            salary=salary
        )

    @router.post("/moneyflow-simulate", response_model=MoneyFlowSimulationResult)
    def simulate_moneyflow(req: MoneyFlowSimulateRequest):
        return simulate_capital_flow(
            inflow_amount_inr=req.inflow_amount_inr,
            source=req.source
        )

    @router.get("/projects", response_model=List[ProjectArchetype])
    def list_projects():
        return get_project_archetypes()

    @router.get("/projects/{project_id}", response_model=ProjectArchetype)
    def get_project_detail(project_id: str):
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        return project

    @router.get("/banking/offices", response_model=List[BangaloreBankOffice])
    def get_banking_offices(
        corridor: Optional[BankingCorridor] = None,
        category: Optional[BankCategory] = None,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreBankingEngine(session)
        return engine.get_offices(corridor=corridor, category=category)

    @router.get("/banking/corridors")
    def get_banking_corridors(session: Session = Depends(session_factory)):
        engine = BangaloreBankingEngine(session)
        return engine.get_corridor_intelligence()

    @router.post("/banking/gcc-blueprint", response_model=GCCCapexOpexModel)
    def generate_gcc_blueprint(
        req: GCCBlueprintRequest,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreBankingEngine(session)
        return engine.calculate_gcc_cost_model(
            seats=req.seats,
            corridor=req.corridor,
            fitout_grade=req.fitout_grade
        )

    @router.post("/banking/audit", response_model=RBIAuditResult)
    def audit_banking_compliance(
        req: RBIAuditRequest,
        session: Session = Depends(session_factory)
    ):
        engine = BangaloreBankingEngine(session)
        return engine.audit_rbi_compliance(
            bank_name=req.bank_name,
            data_localized=req.data_localized,
            dpdp_consent=req.dpdp_consent,
            cert_in_6hr=req.cert_in_6hr,
            npl_clock_sync=req.npl_clock_sync,
            vault_cctv_90day=req.vault_cctv_90day
        )

    @router.get("/overview")
    def get_economic_overview():
        return {
            "city": "Bengaluru",
            "currency": "INR",
            "active_tech_clusters": len(BangaloreCluster),
            "tracked_projects": len(get_project_archetypes()),
            "company_tiers_modeled": len(CompanyTier),
            "engineering_roles_modeled": len(TechRole),
            "tax_regime": "Indian New Tax Regime FY 2026-27",
            "status": "OPERATIONAL",
        }

    return router
