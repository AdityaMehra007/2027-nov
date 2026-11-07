from fastapi import APIRouter, Query
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
from omniverse.modules.saas_factory.scaffolder import SaaSFactoryScaffolder
from omniverse.modules.saas.fleet import (
    VerticalSaaSFleetEngine,
    SaaSVertical,
    SaaSPlan,
    SaaSTenant,
)

# Global engine instance for fleet state
_fleet_engine = VerticalSaaSFleetEngine()


class ScaffoldRequest(BaseModel):
    name: str
    target_dir: str = "./generated_saas"
    include_auth: bool = True
    pricing_model: str = "freemium"


class ProvisionTenantRequest(BaseModel):
    name: str
    vertical: SaaSVertical
    plan: SaaSPlan = SaaSPlan.GROWTH
    custom_domain: Optional[str] = None


class CloudBiteMarginRequest(BaseModel):
    selling_price: float
    ingredient_costs: List[float]
    labor_overhead: float = 0.0


class GymVerseRetentionRequest(BaseModel):
    checkins_last_30d: int
    auto_pay_active: bool = True


class RentShieldRiskRequest(BaseModel):
    monthly_rent: float
    declared_monthly_income: float
    credit_score: int


class ClinicFlowTriageRequest(BaseModel):
    symptoms: List[str]
    severity_1_to_10: int


def get_saas_router():
    router = APIRouter(prefix="/saas", tags=["SaaS Fleet & Factory"])

    # 1. Existing Scaffolder Route (Backward Compatible)
    @router.post("/scaffold")
    def scaffold_saas(req: ScaffoldRequest):
        scaffolder = SaaSFactoryScaffolder()
        return scaffolder.scaffold_project(
            app_name=req.name,
            target_dir=Path(req.target_dir),
            include_auth=req.include_auth,
            pricing_model=req.pricing_model
        )

    # 2. Fleet Summary & MRR Overview
    @router.get("/fleet/summary")
    def get_fleet_summary():
        return _fleet_engine.calculate_fleet_summary()

    # 3. List & Provision Tenants
    @router.get("/fleet/tenants", response_model=List[SaaSTenant])
    def list_fleet_tenants(vertical: Optional[SaaSVertical] = None):
        return _fleet_engine.list_tenants(vertical=vertical)

    @router.post("/fleet/provision", response_model=SaaSTenant)
    def provision_fleet_tenant(req: ProvisionTenantRequest):
        return _fleet_engine.provision_tenant(
            name=req.name,
            vertical=req.vertical,
            plan=req.plan,
            custom_domain=req.custom_domain
        )

    # 4. Vertical Micro-Service Logic
    @router.post("/fleet/cloudbite/margin")
    def compute_cloudbite_margin(req: CloudBiteMarginRequest):
        return _fleet_engine.cloudbite_calculate_recipe_margin(
            selling_price=req.selling_price,
            ingredient_costs=req.ingredient_costs,
            labor_overhead=req.labor_overhead
        )

    @router.post("/fleet/gymverse/retention")
    def evaluate_gymverse_retention(req: GymVerseRetentionRequest):
        return _fleet_engine.gymverse_assess_member_retention(
            checkins_last_30d=req.checkins_last_30d,
            auto_pay_active=req.auto_pay_active
        )

    @router.post("/fleet/rentshield/risk")
    def evaluate_rentshield_risk(req: RentShieldRiskRequest):
        return _fleet_engine.rentshield_evaluate_tenant_risk(
            monthly_rent=req.monthly_rent,
            declared_monthly_income=req.declared_monthly_income,
            credit_score=req.credit_score
        )

    @router.post("/fleet/clinicflow/triage")
    def evaluate_clinicflow_triage(req: ClinicFlowTriageRequest):
        return _fleet_engine.clinicflow_triage_symptom(
            symptoms=req.symptoms,
            severity_1_to_10=req.severity_1_to_10
        )

    return router
