"""==============================================================================
VERTICAL SAAS HOLDINGS FLEET ("THE VERSE FLEET")
==============================================================================
Multi-tenant provisioning, revenue attribution, and vertical logic engines
for CloudBite, GymVerse, RentShield, and OmniClinicFlow.
==============================================================================
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
import time
import secrets


class SaaSVertical(str, Enum):
    CLOUDBITE = "CLOUDBITE"          # Cloud Kitchens, QSRs, Restaurants
    GYMVERSE = "GYMVERSE"            # Gyms, CrossFits, Wellness Centers
    RENTSHIELD = "RENTSHIELD"        # Zero-Brokerage Leasing, PropTech
    CLINICFLOW = "CLINICFLOW"        # Outpatient Clinics, Diagnostic Labs


class SaaSPlan(str, Enum):
    STARTER = "STARTER"
    GROWTH = "GROWTH"
    ENTERPRISE = "ENTERPRISE"


PLAN_PRICING_USD: Dict[SaaSVertical, Dict[SaaSPlan, float]] = {
    SaaSVertical.CLOUDBITE: {SaaSPlan.STARTER: 49.0, SaaSPlan.GROWTH: 99.0, SaaSPlan.ENTERPRISE: 249.0},
    SaaSVertical.GYMVERSE: {SaaSPlan.STARTER: 69.0, SaaSPlan.GROWTH: 139.0, SaaSPlan.ENTERPRISE: 299.0},
    SaaSVertical.RENTSHIELD: {SaaSPlan.STARTER: 59.0, SaaSPlan.GROWTH: 129.0, SaaSPlan.ENTERPRISE: 349.0},
    SaaSVertical.CLINICFLOW: {SaaSPlan.STARTER: 49.0, SaaSPlan.GROWTH: 119.0, SaaSPlan.ENTERPRISE: 279.0},
}


class SaaSTenant(BaseModel):
    tenant_id: str = Field(default_factory=lambda: f"tnt_{uuid.uuid4().hex[:12]}")
    name: str
    vertical: SaaSVertical
    plan: SaaSPlan = SaaSPlan.GROWTH
    mrr_usd: float = 99.0
    status: str = "ACTIVE"
    custom_domain: Optional[str] = None
    api_key: str = Field(default_factory=lambda: f"omni_live_{secrets.token_urlsafe(16)}")
    created_at: float = Field(default_factory=time.time)


class VerticalSaaSFleetEngine:
    """Manages multi-tenant vertical SaaS provisioning and operational runtimes."""

    def __init__(self):
        self._tenants: Dict[str, SaaSTenant] = {}
        self._seed_default_tenants()

    def _seed_default_tenants(self):
        """Seed representative flagship customers across the 4 verticals."""
        seed_data = [
            ("Bangalore Biryani Box Kitchens", SaaSVertical.CLOUDBITE, SaaSPlan.GROWTH, "biryanibox.cloudbite.io"),
            ("IronCore CrossFit HSR", SaaSVertical.GYMVERSE, SaaSPlan.GROWTH, "ironcore.gymverse.io"),
            ("Prestige Koramangala Estates", SaaSVertical.RENTSHIELD, SaaSPlan.ENTERPRISE, "prestige.rentshield.io"),
            ("Apollo Outpatient Indiranagar", SaaSVertical.CLINICFLOW, SaaSPlan.GROWTH, "apollo.clinicflow.io"),
        ]
        for name, vert, plan, domain in seed_data:
            self.provision_tenant(name=name, vertical=vert, plan=plan, custom_domain=domain)

    def provision_tenant(
        self,
        name: str,
        vertical: SaaSVertical | str,
        plan: SaaSPlan | str = SaaSPlan.GROWTH,
        custom_domain: Optional[str] = None
    ) -> SaaSTenant:
        """Provisions a new tenant with dedicated API keys and pricing."""
        if isinstance(vertical, str):
            vertical = SaaSVertical(vertical.upper())
        if isinstance(plan, str):
            plan = SaaSPlan(plan.upper())
        mrr = PLAN_PRICING_USD.get(vertical, {}).get(plan, 99.0)
        tenant = SaaSTenant(
            name=name,
            vertical=vertical,
            plan=plan,
            mrr_usd=mrr,
            custom_domain=custom_domain or f"{name.lower().replace(' ', '-')}.omniverse.io"
        )
        self._tenants[tenant.tenant_id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Optional[SaaSTenant]:
        return self._tenants.get(tenant_id)

    def list_tenants(self, vertical: Optional[SaaSVertical] = None) -> List[SaaSTenant]:
        tenants = list(self._tenants.values())
        if vertical:
            return [t for t in tenants if t.vertical == vertical]
        return tenants

    def calculate_fleet_summary(self) -> Dict[str, Any]:
        """Calculates total fleet MRR, ARR, and subscriber breakdown."""
        tenants = list(self._tenants.values())
        total_mrr = sum(t.mrr_usd for t in tenants if t.status == "ACTIVE")
        total_arr = total_mrr * 12.0

        by_vertical: Dict[str, Dict[str, Any]] = {}
        for v in SaaSVertical:
            v_tenants = [t for t in tenants if t.vertical == v]
            v_mrr = sum(t.mrr_usd for t in v_tenants if t.status == "ACTIVE")
            by_vertical[v.value] = {
                "active_subscribers": len(v_tenants),
                "mrr_usd": round(v_mrr, 2),
                "arr_usd": round(v_mrr * 12.0, 2)
            }

        return {
            "total_subscribers": len(tenants),
            "total_mrr_usd": round(total_mrr, 2),
            "total_arr_usd": round(total_arr, 2),
            "verticals": by_vertical
        }

    # =========================================================================
    # VERTICAL SPECIFIC RUNTIMES
    # =========================================================================

    @staticmethod
    def cloudbite_calculate_recipe_margin(selling_price: float, ingredient_costs: List[float], labor_overhead: float = 0.0) -> Dict[str, Any]:
        """CloudBite: Computes food cost percentage and gross margin for cloud kitchens."""
        total_cost = sum(ingredient_costs) + labor_overhead
        food_cost_pct = (sum(ingredient_costs) / selling_price * 100.0) if selling_price > 0 else 0.0
        gross_margin_pct = ((selling_price - total_cost) / selling_price * 100.0) if selling_price > 0 else 0.0
        return {
            "selling_price": selling_price,
            "total_food_cost": round(sum(ingredient_costs), 2),
            "total_cost_with_overhead": round(total_cost, 2),
            "food_cost_pct": round(food_cost_pct, 2),
            "gross_margin_pct": round(gross_margin_pct, 2),
            "status": "HEALTHY" if food_cost_pct <= 32.0 else "WARNING_HIGH_COST"
        }

    @staticmethod
    def gymverse_assess_member_retention(checkins_last_30d: int, auto_pay_active: bool) -> Dict[str, Any]:
        """GymVerse: Predicts member retention health and renewal probability."""
        score = min(100.0, checkins_last_30d * 6.5)
        if auto_pay_active:
            score = min(100.0, score + 20.0)
        risk = "LOW" if score >= 75.0 else ("MEDIUM" if score >= 45.0 else "HIGH")
        return {
            "checkins_last_30d": checkins_last_30d,
            "auto_pay_active": auto_pay_active,
            "retention_score": round(score, 1),
            "churn_risk": risk,
            "recommended_action": "Send workout challenge WhatsApp" if risk != "LOW" else "Loyalty reward candidate"
        }

    @staticmethod
    def rentshield_evaluate_tenant_risk(monthly_rent: float, declared_monthly_income: float, credit_score: int) -> Dict[str, Any]:
        """RentShield: Evaluates commercial/residential tenant default risk."""
        rent_to_income = (monthly_rent / declared_monthly_income) if declared_monthly_income > 0 else 1.0
        score = 100.0
        if rent_to_income > 0.40:
            score -= 30.0
        elif rent_to_income > 0.30:
            score -= 15.0
        if credit_score < 650:
            score -= 40.0
        elif credit_score < 720:
            score -= 15.0

        decision = "APPROVED_ZERO_DEPOSIT" if score >= 80.0 else ("REQUIRES_1MO_ESCROW" if score >= 55.0 else "REJECTED_HIGH_RISK")
        return {
            "rent_to_income_ratio": round(rent_to_income, 3),
            "credit_score": credit_score,
            "risk_score": max(0.0, round(score, 1)),
            "decision": decision
        }

    @staticmethod
    def clinicflow_triage_symptom(symptoms: List[str], severity_1_to_10: int) -> Dict[str, Any]:
        """OmniClinicFlow: Preliminary outpatient symptom triage and queue routing."""
        is_emergency = severity_1_to_10 >= 8 or any(s.lower() in ["chest pain", "shortness of breath", "severe bleeding"] for s in symptoms)
        return {
            "symptoms": symptoms,
            "severity": severity_1_to_10,
            "priority": "IMMEDIATE_ER" if is_emergency else ("PRIORITY_DOCTOR" if severity_1_to_10 >= 5 else "STANDARD_CONSULT"),
            "estimated_wait_minutes": 0 if is_emergency else (10 if severity_1_to_10 >= 5 else 25)
        }
