from typing import List, Dict, Any
from omniverse.modules.commerce.models import BusinessUnitID, BusinessUnitSpec

class CommerceMatrix:
    """Manages specifications, unit economics, and operational configurations

    for all 10 autonomous business units.
    """

    def __init__(self):
        self._units: Dict[BusinessUnitID, BusinessUnitSpec] = {
            BusinessUnitID.AI_SERVICE_AGENCY: BusinessUnitSpec(
                unit_id=BusinessUnitID.AI_SERVICE_AGENCY,
                title="AI Growth & Social Agency",
                target_customer="Local SMBs, Cafes, Retailers, Clinics",
                core_offering="Local Business Growth Kits, WhatsApp catalogues, 10-post social campaigns",
                monetization_model="Monthly Retainers & One-Off Setup",
                typical_contract_value_inr=20000.0,
                gross_margin_pct=85.0,
                delivery_lead_time_days=1
            ),
            BusinessUnitID.SAAS_FACTORY: BusinessUnitSpec(
                unit_id=BusinessUnitID.SAAS_FACTORY,
                title="Micro-SaaS Software Factory",
                target_customer="Indie Hackers, Solo Founders, Startups",
                core_offering="Pre-scaffolded, authenticated niche B2B tools",
                monetization_model="Recurring MRR Subscriptions",
                typical_contract_value_inr=4000.0,
                gross_margin_pct=92.0,
                delivery_lead_time_days=3
            ),
            BusinessUnitID.DATA_INTELLIGENCE_SERVICES: BusinessUnitSpec(
                unit_id=BusinessUnitID.DATA_INTELLIGENCE_SERVICES,
                title="Data & Research Intelligence",
                target_customer="Investors, Market Researchers, Hedge Funds",
                core_offering="B2B company dossiers, competitive profiling, market share tracking",
                monetization_model="Per-Dossier & Enterprise Feeds",
                typical_contract_value_inr=75000.0,
                gross_margin_pct=80.0,
                delivery_lead_time_days=2
            ),
            BusinessUnitID.DEVELOPER_API_BUSINESS: BusinessUnitSpec(
                unit_id=BusinessUnitID.DEVELOPER_API_BUSINESS,
                title="Developer Tooling & Cloud APIs",
                target_customer="Software Engineers & Tech Teams",
                core_offering="Geospatial calculations, resilience APIs, MCP connectors",
                monetization_model="Usage-Based Metering ($/request)",
                typical_contract_value_inr=15000.0,
                gross_margin_pct=88.0,
                delivery_lead_time_days=0
            ),
            BusinessUnitID.DIGITAL_PRODUCT_BUSINESS: BusinessUnitSpec(
                unit_id=BusinessUnitID.DIGITAL_PRODUCT_BUSINESS,
                title="Digital Products & Frameworks",
                target_customer="Creators, Consultants, Professionals",
                core_offering="Antigravity agent templates, quantitative model notebooks, playbooks",
                monetization_model="Direct Downloads & License Fees",
                typical_contract_value_inr=5000.0,
                gross_margin_pct=95.0,
                delivery_lead_time_days=0
            ),
            BusinessUnitID.MARKET_INTELLIGENCE_SUBSCRIPTIONS: BusinessUnitSpec(
                unit_id=BusinessUnitID.MARKET_INTELLIGENCE_SUBSCRIPTIONS,
                title="Financial & Market Subscriptions",
                target_customer="HNIs, Family Offices, Active Traders",
                core_offering="Macro regime alerts, backtested quant signals, yield curves",
                monetization_model="Quarterly & Annual Subscriptions",
                typical_contract_value_inr=60000.0,
                gross_margin_pct=90.0,
                delivery_lead_time_days=0
            ),
            BusinessUnitID.ENTERPRISE_TECHNOLOGY: BusinessUnitSpec(
                unit_id=BusinessUnitID.ENTERPRISE_TECHNOLOGY,
                title="Enterprise Infrastructure Deployment",
                target_customer="Mid-Market Corporates & Institutions",
                core_offering="On-premise agent workflow deployment, private MCP clusters",
                monetization_model="Enterprise Annual Contracts",
                typical_contract_value_inr=500000.0,
                gross_margin_pct=75.0,
                delivery_lead_time_days=14
            ),
            BusinessUnitID.MARKETPLACE: BusinessUnitSpec(
                unit_id=BusinessUnitID.MARKETPLACE,
                title="Agent & Skill Marketplace",
                target_customer="Third-Party Tool Builders & Buyers",
                core_offering="Verified custom skills, prompts, and domain integrations",
                monetization_model="15-20% Transaction Take-Rate",
                typical_contract_value_inr=2500.0,
                gross_margin_pct=90.0,
                delivery_lead_time_days=0
            ),
            BusinessUnitID.CONSULTANCY_AND_IMPLEMENTATION: BusinessUnitSpec(
                unit_id=BusinessUnitID.CONSULTANCY_AND_IMPLEMENTATION,
                title="Strategic Advisory & Implementation",
                target_customer="Founders, Executives, Organizations",
                core_offering="Bespoke AI transformation, quantitative architecture consulting",
                monetization_model="Hourly / Project Retainers",
                typical_contract_value_inr=150000.0,
                gross_margin_pct=70.0,
                delivery_lead_time_days=7
            ),
            BusinessUnitID.PARTNERSHIP_AND_REFERRAL: BusinessUnitSpec(
                unit_id=BusinessUnitID.PARTNERSHIP_AND_REFERRAL,
                title="Affiliate & Co-Marketing Network",
                target_customer="SaaS vendors, Hosting Providers, Brokers",
                core_offering="Integrated recommendations, API partnership referrals",
                monetization_model="Recurring Affiliate Commissions",
                typical_contract_value_inr=10000.0,
                gross_margin_pct=98.0,
                delivery_lead_time_days=0
            ),
        }

    def list_all_units(self) -> List[BusinessUnitSpec]:
        return list(self._units.values())

    def get_unit(self, unit_id: BusinessUnitID) -> BusinessUnitSpec:
        return self._units[unit_id]

    def calculate_portfolio_economics(self) -> Dict[str, Any]:
        units = list(self._units.values())
        avg_margin = sum(u.gross_margin_pct for u in units) / len(units)
        total_capacity = sum(u.typical_contract_value_inr * 12 for u in units)

        return {
            "total_business_units": len(units),
            "average_gross_margin_pct": round(avg_margin, 2),
            "projected_annual_capacity_inr": total_capacity,
            "high_margin_units_count": sum(1 for u in units if u.gross_margin_pct >= 85.0)
        }
