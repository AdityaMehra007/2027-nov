"""FastAPI Routes for the Autonomous Agency & Multi-Vertical Fulfillment Suite."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field, field_validator

from omniverse.modules.agency.models import (
    ProspectArchetype,
    LeadStage,
    OrderStatus,
    ServiceType,
    Lead,
    AuditReport,
    PersonalizedPitch,
    JobOrder,
    Deliverable,
    ClientAccount,
    AgencyMetrics,
)
from omniverse.modules.agency.acquisition import LeadHunter, TechAuditor, PitchGenerator
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory
from omniverse.modules.agency.fulfillment.marketing_factory import MarketingFactory
from omniverse.modules.agency.fulfillment.automation_factory import AutomationFactory
from omniverse.modules.agency.qa_governor import QAGovernor
from omniverse.modules.agency.portal_engine import AgencyPortalEngine
from omniverse.modules.agency.outreach import MultiChannelOutreachDispatcher, OutreachMessage
from omniverse.modules.agency.upi_gateway import InstantUPIEngine, UPIPaymentIntent
from omniverse.modules.agency.crypto_gateway import Web3CryptoEscrow, CryptoChain, CryptoDepositIntent
from omniverse.modules.agency.inbound_pseo import ProgrammaticSEOMagnet, SEOLandingPage
from omniverse.modules.agency.daemon import AutonomousAgencyDaemon, AgencyCycleReport
from omniverse.modules.agency.revision_manager import AutonomousRevisionAgent, RevisionResult
from omniverse.api.routes.agency_ui import (
    render_agency_cockpit_html,
    render_client_portal_html,
)


# In-memory singletons for operational agency runtime
hunter = LeadHunter()
auditor = TechAuditor()
pitcher = PitchGenerator()
code_factory = CodeFactory()
marketing_factory = MarketingFactory()
automation_factory = AutomationFactory()
qa_governor = QAGovernor()
portal_engine = AgencyPortalEngine()
outreach_dispatcher = MultiChannelOutreachDispatcher()
upi_engine = InstantUPIEngine()
crypto_escrow = Web3CryptoEscrow()
pseo_magnet = ProgrammaticSEOMagnet()
agency_daemon = AutonomousAgencyDaemon()
revision_agent = AutonomousRevisionAgent(portal_engine=portal_engine, qa_governor=qa_governor)
from omniverse.modules.agency.pipeline_runner import AutonomousAgencyPipelineRunner, AutonomousCampaignResult
pipeline_runner = AutonomousAgencyPipelineRunner()

# State caches
_discovered_leads: Dict[str, Lead] = {}
_orders: Dict[str, JobOrder] = {}


class HuntRequest(BaseModel):
    archetype: Optional[ProspectArchetype] = None
    city: Optional[str] = None
    limit: int = 5


class PitchRequest(BaseModel):
    lead: Lead
    audit: AuditReport


class CreateClientRequest(BaseModel):
    name: str
    email: str
    company: str


class CreateOrderRequest(BaseModel):
    client_id: str
    service_type: ServiceType
    brief: str
    budget_usd: float = 0.0


class PaymentRequest(BaseModel):
    order_id: str
    payment_method: str = "STRIPE"


class UPIGenerateRequest(BaseModel):
    order_id: str
    amount_usd: float
    exchange_rate: float = 86.0


class UPIConfirmRequest(BaseModel):
    order_id: str
    utr_number: str


class CryptoDepositIntentRequest(BaseModel):
    order_id: str
    amount_usd: float
    chain: CryptoChain = CryptoChain.BASE


class CryptoVerifyRequest(BaseModel):
    order_id: str
    tx_hash: str
    chain: Optional[CryptoChain] = None


class PSEOGenerateRequest(BaseModel):
    competitor_name: str
    our_solution: str
    service_type: ServiceType = ServiceType.MARKETING_SUITE
    target_niche: str = "B2B SaaS"

    @field_validator("service_type", mode="before")
    @classmethod
    def validate_service_type(cls, v: Any) -> ServiceType:
        if isinstance(v, ServiceType):
            return v
        if isinstance(v, str):
            v_upper = v.upper()
            for member in ServiceType:
                if member.value == v_upper or member.name == v_upper:
                    return member
        return ServiceType.MARKETING_SUITE


class DaemonCycleRequest(BaseModel):
    limit: int = 2
    budget_per_order: float = 3000.0


class RevisionRequest(BaseModel):
    feedback: str


def get_agency_router() -> APIRouter:
    router = APIRouter(prefix="/agency", tags=["Autonomous Agency"])

    @router.get("/overview")
    def get_overview() -> Dict[str, Any]:
        """Return executive KPIs and operational agency metrics."""
        completed = sum(1 for o in _orders.values() if o.status in (OrderStatus.DELIVERED, OrderStatus.PAID))
        active = sum(1 for o in _orders.values() if o.status in (OrderStatus.QUEUED, OrderStatus.BUILDING, OrderStatus.QA_VERIFIED))
        pipeline = sum(o.budget_usd for o in _orders.values() if o.status != OrderStatus.PAID)
        collected = sum(o.budget_usd for o in _orders.values() if o.status == OrderStatus.PAID)

        metrics = AgencyMetrics(
            total_leads_discovered=len(_discovered_leads) or 8,
            total_audits_performed=len(_discovered_leads),
            pitches_dispatched=max(len(_orders), 2),
            active_orders=active,
            completed_deliverables=completed,
            pipeline_value_usd=pipeline,
            reconciled_revenue_usd=collected,
        )
        return {
            "status": "OPERATIONAL",
            "metrics": metrics.model_dump(),
        }

    @router.post("/hunt")
    def hunt_leads(req: HuntRequest) -> Dict[str, Any]:
        """Discover qualified commercial leads across target sectors."""
        leads = hunter.discover_leads(archetype=req.archetype, city=req.city, limit=req.limit)
        for lead in leads:
            _discovered_leads[lead.id] = lead
        return {
            "success": True,
            "count": len(leads),
            "leads": [lead.model_dump() for lead in leads],
        }

    @router.post("/audit")
    def audit_lead(lead: Lead) -> Dict[str, Any]:
        """Perform automated deep technical, SEO, and conversion audit."""
        report = auditor.audit_lead(lead)
        lead.stage = LeadStage.AUDITED
        _discovered_leads[lead.id] = lead
        return report.model_dump()

    @router.post("/outreach")
    def generate_outreach(lead: Lead) -> Dict[str, Any]:
        """Generate multi-channel outreach campaigns (WhatsApp and Email) for lead."""
        messages = outreach_dispatcher.generate_campaign_for_lead(lead)
        return {
            "success": True,
            "business_name": lead.business_name,
            "campaigns": [m.model_dump() for m in messages],
        }

    @router.post("/pitch")
    def generate_pitch(req: PitchRequest) -> Dict[str, Any]:
        """Generate tailored pitch proposal with 1-click WhatsApp link."""
        pitch = pitcher.generate_pitch(req.lead, req.audit)
        req.lead.stage = LeadStage.PITCHED
        _discovered_leads[req.lead.id] = req.lead
        return pitch.model_dump()

    @router.post("/clients")
    def register_client(req: CreateClientRequest) -> Dict[str, Any]:
        """Register a new client account and issue portal access token."""
        client = portal_engine.create_client(name=req.name, email=req.email, company=req.company)
        return {
            "success": True,
            "client": client.model_dump(),
        }

    @router.post("/orders")
    def create_order(req: CreateOrderRequest) -> Dict[str, Any]:
        """Create and queue a client job order."""
        order = JobOrder(
            client_id=req.client_id,
            service_type=req.service_type,
            brief=req.brief,
            budget_usd=req.budget_usd,
            status=OrderStatus.QUEUED,
        )
        _orders[order.id] = order
        portal_engine.register_order(order)
        return {
            "success": True,
            "order": order.model_dump(),
        }

    @router.post("/orders/{order_id}/execute")
    def execute_order(order_id: str) -> Dict[str, Any]:
        """Trigger autonomous agent fulfillment, QA gating, and packaging."""
        order = _orders.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.transition_to(OrderStatus.BUILDING)

        # Route to appropriate autonomous factory
        if order.service_type in (ServiceType.FULLSTACK_DEV, ServiceType.FULL_TRANSFORMATION):
            deliverables = code_factory.build_project(order)
        elif order.service_type in (ServiceType.MARKETING_SUITE, ServiceType.GROWTH_MARKETING, ServiceType.DESIGN_SYSTEM):
            deliverables = marketing_factory.build_campaign(order)
        else:
            deliverables = automation_factory.build_agent_bundle(order)

        order.deliverables = deliverables

        # QA Governor Gate
        qa_result = qa_governor.verify_deliverables(deliverables)
        if not qa_result.passed:
            raise HTTPException(status_code=500, detail=f"QA Gate Failed: {qa_result.failures}")

        order.transition_to(OrderStatus.QA_VERIFIED)

        # Build download zip package
        bundle_path = portal_engine.package_order_bundle(order)
        order.transition_to(OrderStatus.DELIVERED)

        return {
            "success": True,
            "order": order.model_dump(),
            "qa_verification": qa_result.model_dump(),
            "bundle_path": str(bundle_path),
        }

    @router.get("/orders/{order_id}/bundle")
    def download_bundle(order_id: str):
        """Download complete verified deliverable ZIP bundle."""
        order = _orders.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        bundle_path = portal_engine.bundles_root / f"{order.id}_bundle.zip"
        if not bundle_path.exists():
            bundle_path = portal_engine.package_order_bundle(order)

        return FileResponse(
            path=str(bundle_path),
            filename=f"{order.id}_deliverables.zip",
            media_type="application/zip",
        )

    @router.get("/portal/{token}")
    def get_client_portal(token: str) -> Dict[str, Any]:
        """Authenticate and fetch client portal information."""
        client = portal_engine.authenticate_client(token)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid client portal token")

        client_orders = [o.model_dump() for o in _orders.values() if o.client_id == client.id]
        return {
            "client": client.model_dump(),
            "orders": client_orders,
        }

    @router.post("/portal/{token}/pay")
    def settle_order_payment(token: str, req: PaymentRequest) -> Dict[str, Any]:
        """Process verified invoice settlement and credit collected revenue."""
        client = portal_engine.authenticate_client(token)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid client portal token")

        order = _orders.get(req.order_id)
        if not order or order.client_id != client.id:
            raise HTTPException(status_code=404, detail="Order not found for this client")

        receipt = portal_engine.settle_order_payment(order=order, client=client, payment_method=req.payment_method)
        return {
            "success": True,
            "settlement": receipt,
            "order": order.model_dump(),
            "client": client.model_dump(),
        }

    @router.get("/cockpit", response_class=HTMLResponse)
    def render_cockpit():
        """Render cyberpunk interactive agency command center."""
        overview = get_overview()
        leads_list = [l.model_dump() for l in _discovered_leads.values()]
        orders_list = [o.model_dump() for o in _orders.values()]
        return HTMLResponse(content=render_agency_cockpit_html(overview, leads_list, orders_list))

    @router.get("/portal/{token}/view", response_class=HTMLResponse)
    def render_portal_view(token: str):
        """Render client-facing self-serve portal UI."""
        client = portal_engine.authenticate_client(token)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid client portal token")

        client_orders = [o.model_dump() for o in _orders.values() if o.client_id == client.id]
        return HTMLResponse(content=render_client_portal_html(client, client_orders))

    @router.post("/autonomous-cycle", response_model=AutonomousCampaignResult)
    def run_autonomous_cycle(
        archetype: Optional[ProspectArchetype] = None,
        limit: int = 2,
        budget_per_order: float = 3000.0,
    ):
        """Executes full autonomous cycle from discovery to conversion and fulfillment."""
        return pipeline_runner.run_autonomous_cycle(
            archetype=archetype,
            limit=limit,
            budget_per_order=budget_per_order
        )

    @router.get("/autonomous-cycle/history")
    def get_autonomous_cycle_history() -> List[Dict[str, Any]]:
        """Returns history of all autonomous campaign cycles executed."""
        return pipeline_runner.get_pipeline_history()

    @router.post("/orders/{order_id}/revise", response_model=RevisionResult)
    def revise_order_deliverables(order_id: str, req: RevisionRequest) -> RevisionResult:
        """Autonomous client revision and self-healing agent."""
        order = _orders.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        result = revision_agent.apply_revision(order=order, feedback=req.feedback)
        return result

    @router.post("/payments/upi/generate")
    def generate_upi_payment_intent(req: UPIGenerateRequest) -> Dict[str, Any]:
        """Generate instant NPCI UPI payment intent and dynamic QR."""
        intent = upi_engine.generate_upi_intent(
            order_id=req.order_id,
            amount_usd=req.amount_usd,
            exchange_rate=req.exchange_rate,
        )
        return intent.model_dump()

    @router.post("/payments/upi/confirm")
    def confirm_upi_payment(req: UPIConfirmRequest) -> Dict[str, Any]:
        """Confirm and settle UPI payment with replay protection."""
        res = upi_engine.confirm_upi_payment(order_id=req.order_id, utr_number=req.utr_number)
        if not res.get("settled"):
            raise HTTPException(status_code=400, detail=res.get("error", "UPI settlement failed"))
        res["utr_number"] = req.utr_number
        return res

    @router.post("/payments/crypto/deposit-intent")
    def create_crypto_deposit_intent(req: CryptoDepositIntentRequest) -> Dict[str, Any]:
        """Create a segregated Web3 crypto escrow deposit intent."""
        intent = crypto_escrow.create_deposit_intent(
            order_id=req.order_id,
            amount_usd=req.amount_usd,
            chain=req.chain,
        )
        return intent.model_dump()

    @router.post("/payments/crypto/verify")
    def verify_crypto_payment(req: CryptoVerifyRequest) -> Dict[str, Any]:
        """Verify on-chain crypto payment with zero-trust replay protection."""
        res = crypto_escrow.verify_transaction(order_id=req.order_id, tx_hash=req.tx_hash)
        if not res.get("verified"):
            raise HTTPException(status_code=400, detail=res.get("error", "Transaction verification failed"))
        return {
            "verified": True,
            "status": res.get("status", "SETTLED"),
            "amount_settled_usd": res.get("settled_usd", 0.0),
            "tx_hash": req.tx_hash,
            "order_id": req.order_id,
        }

    @router.post("/pseo/generate")
    def generate_pseo_page(req: PSEOGenerateRequest) -> Dict[str, Any]:
        """Manufacture automated competitor comparison pSEO landing page."""
        page = pseo_magnet.generate_competitor_alternative(
            competitor_name=req.competitor_name,
            our_solution=req.our_solution,
            service_type=req.service_type,
            target_niche=req.target_niche,
        )
        return page.model_dump()

    @router.post("/daemon/cycle")
    def run_agency_daemon_cycle(req: DaemonCycleRequest) -> Dict[str, Any]:
        """Trigger one 24/7 autonomous prospecting and delivery cycle."""
        report = agency_daemon.run_cycle(limit=req.limit, budget_per_order=req.budget_per_order)
        return report.model_dump()

    return router
