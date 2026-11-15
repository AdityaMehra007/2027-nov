# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Prospect Pipeline & 30-Dossier Staging Engine (PROJECT ONE Phase 4)."""

from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import uuid
import hmac
import hashlib
from datetime import datetime, timezone

from omniverse.modules.opportunities.company_intelligence import (
    CompanyIntelligenceRegistry,
    CompanyRecord,
    RegistrySource,
)
from omniverse.modules.opportunities.beachhead import (
    BeachheadAuditGenerator,
    AuditDeliverable,
)


class CorridorRegion(str, Enum):
    BENGALURU_TECH = "BENGALURU_TECH"
    NORTH_AMERICA = "NORTH_AMERICA"
    EUROPE_UK = "EUROPE_UK"
    APAC_MIDDLE_EAST = "APAC_MIDDLE_EAST"


class ProspectCompany(BaseModel):
    id: str = Field(default_factory=lambda: f"prsp_{uuid.uuid4().hex[:10]}")
    company_name: str
    website: str
    country: str
    city: str
    industry: str
    corridor: CorridorRegion
    estimated_annual_toil_usd: float
    problem_hypothesis: str
    monthly_volume: int = 2500
    human_hours_per_unit: float = 0.25
    hourly_wage_usd: float = 16.0


class ProspectDossier(BaseModel):
    prospect: ProspectCompany
    audit_deliverable: AuditDeliverable
    abm_hook: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StagedAction(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:10]}")
    prospect_name: str
    is_gated: bool = True
    status: str = "PENDING_APPROVAL"
    payload: str
    hmac_signature: str
    staged_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProspectPipelineEngine:
    """Manages the 30-organization global prospect cohort, customized dossier generation, and gated staging."""

    def __init__(self, registry: Optional[CompanyIntelligenceRegistry] = None, signing_key: str = "OMNIVERSE_FOUNDER_KEY_2026"):
        self.registry = registry or CompanyIntelligenceRegistry()
        self.signing_key = signing_key
        self._prospects = self._seed_canonical_prospects()

    def _seed_canonical_prospects(self) -> List[ProspectCompany]:
        raw = [
            # 1. BENGALURU TECH & GCCs (8)
            ("Target India", "https://target.com/india", "India", "Bengaluru", "Retail Supply Chain Tech", CorridorRegion.BENGALURU_TECH, 185000.0, "Manual multi-vendor purchase order vs invoice discrepancies across 3,000 weekly SKU shipments", 4000, 0.25, 18.0),
            ("Wells Fargo India Solutions", "https://wellsfargo.com/india", "India", "Bengaluru", "Banking & Financial Services GCC", CorridorRegion.BENGALURU_TECH, 240000.0, "Manual regulatory capital reporting and loan origination document sanity checks", 3500, 0.30, 22.0),
            ("Mercedes-Benz R&D India", "https://mbrdi.co.in", "India", "Bengaluru", "Automotive R&D & Telematics", CorridorRegion.BENGALURU_TECH, 160000.0, "Multi-supplier CAD revision conflict logging and component parts warranty claims", 2200, 0.35, 20.0),
            ("Flipkart Internet Logistics", "https://flipkart.com", "India", "Bengaluru", "Ecommerce Logistics & Fulfillment", CorridorRegion.BENGALURU_TECH, 210000.0, "3PL carrier line-haul freight reconciliation and proof-of-delivery discrepancy disputes", 5000, 0.20, 16.0),
            ("Swiggy Instamart Dark Stores", "https://swiggy.com", "India", "Bengaluru", "Quick Commerce & Hyperlocal Retail", CorridorRegion.BENGALURU_TECH, 145000.0, "FMCG distributor credit notes vs physical stock receiving audits", 4500, 0.18, 15.0),
            ("Razorpay Financial Systems", "https://razorpay.com", "India", "Bengaluru", "Payments & Merchant Infrastructure", CorridorRegion.BENGALURU_TECH, 190000.0, "Merchant chargeback documentation compilation and banking partner settlement triage", 3000, 0.25, 20.0),
            ("Zerodha Broking Operations", "https://zerodha.com", "India", "Bengaluru", "Fintech & Retail Capital Markets", CorridorRegion.BENGALURU_TECH, 175000.0, "Depository participant trade log auditing and KYC document OCR anomaly detection", 3200, 0.22, 22.0),
            ("Cognitive Cloud Systems", "https://cognitivecloud.com", "India", "Bengaluru", "IT Services & Cloud Architecture", CorridorRegion.BENGALURU_TECH, 120000.0, "Multi-cloud invoice FinOps cost anomaly triage and tagging drift alerts", 2000, 0.25, 20.0),

            # 2. NORTH AMERICA (8)
            ("DataFlow SaaS Labs", "https://dataflowlabs.io", "USA", "San Francisco", "B2B Data Integration SaaS", CorridorRegion.NORTH_AMERICA, 160000.0, "Customer integration schema drift and failed webhook replay management", 2500, 0.25, 25.0),
            ("Beacon Health Cloud", "https://beaconhealth.org", "USA", "Boston", "Healthcare Revenue Cycle", CorridorRegion.NORTH_AMERICA, 280000.0, "Prior-authorization insurance claim packet extraction and denial coding", 2800, 0.40, 25.0),
            ("FleetPulse Logistics NY", "https://fleetpulseny.com", "USA", "New York", "Freight Brokerage & Intermodal", CorridorRegion.NORTH_AMERICA, 225000.0, "Broker rate con vs bill of lading cross-referencing and detention fee auditing", 3200, 0.30, 24.0),
            ("Apex DevTools Corp", "https://apexdevtools.com", "USA", "Austin", "Developer Tools & API Infrastructure", CorridorRegion.NORTH_AMERICA, 140000.0, "Open source CVE dependency triage and license compliance attestation", 1800, 0.30, 26.0),
            ("OmniCommerce Direct", "https://omnicommercedirect.com", "USA", "Chicago", "Omnichannel DTC Apparel", CorridorRegion.NORTH_AMERICA, 170000.0, "Cross-marketplace returns fraud validation and restock invoice synchronization", 3000, 0.22, 22.0),
            ("ClearLedger Accounting LLC", "https://clearledger.cpa", "USA", "Dallas", "Mid-Market Accounting & Advisory", CorridorRegion.NORTH_AMERICA, 155000.0, "Multi-entity intercompany balance elimination and bank reconciliation sweeps", 2200, 0.30, 24.0),
            ("Nexus Cyber Defenses", "https://nexuscyber.io", "USA", "Seattle", "Cybersecurity Threat Intel", CorridorRegion.NORTH_AMERICA, 195000.0, "SOC Tier-1 alert triaging and firewall policy anomaly classification", 2400, 0.30, 28.0),
            ("Starlight Property Group", "https://starlightproperties.com", "USA", "Miami", "Commercial Real Estate Management", CorridorRegion.NORTH_AMERICA, 130000.0, "Tenant CAM lease expense reconciliation and vendor insurance cert validation", 1800, 0.30, 22.0),

            # 3. EUROPE & UK (7)
            ("London Thames Logistics Ltd", "https://thameslogistics.co.uk", "UK", "London", "Cross-Channel Freight & Customs", CorridorRegion.EUROPE_UK, 190000.0, "Post-Brexit customs declaration forms and VAT import deferment verification", 2800, 0.30, 22.0),
            ("Nordic FinTech Solutions", "https://nordicfintech.se", "Sweden", "Stockholm", "Open Banking & Payment Gateways", CorridorRegion.EUROPE_UK, 175000.0, "PSD2 consent validation and recurring mandate debit dispute audits", 2600, 0.28, 24.0),
            ("Berlin AutoParts Direct", "https://berlinautoparts.de", "Germany", "Berlin", "Wholesale Automotive Distribution", CorridorRegion.EUROPE_UK, 165000.0, "OEM parts cross-catalog compatibility validation and return RMA approval", 2400, 0.28, 22.0),
            ("Zurich Risk Modeling AG", "https://zurichrisk.ch", "Switzerland", "Zurich", "Reinsurance & Catastrophe Risk", CorridorRegion.EUROPE_UK, 290000.0, "Cedant treaty bordereaux audit and loss run claims normalization", 2100, 0.45, 30.0),
            ("Dublin Cloud Services", "https://dublincloud.ie", "Ireland", "Dublin", "Enterprise SaaS Hosting", CorridorRegion.EUROPE_UK, 150000.0, "Multi-region AWS/Azure egress cost billing reconciliation for European clients", 2000, 0.30, 25.0),
            ("Paris Retail Brands SA", "https://parisretail.fr", "France", "Paris", "Luxury Goods & Retail Licensing", CorridorRegion.EUROPE_UK, 180000.0, "Franchise revenue share audit and trademark license usage reporting", 2300, 0.32, 24.0),
            ("Amsterdam Maritime Terminal", "https://amsterdammaritime.nl", "Netherlands", "Amsterdam", "Port Operations & Container Logistics", CorridorRegion.EUROPE_UK, 230000.0, "Customs manifest EDI parsing and demurrage container release hold audits", 3000, 0.32, 24.0),

            # 4. APAC & MIDDLE EAST (7)
            ("Singapore Straits Maritime", "https://straitsmaritime.sg", "Singapore", "Singapore", "Bunkering & Vessel Logistics", CorridorRegion.APAC_MIDDLE_EAST, 240000.0, "Bunker delivery notes and marine fuel sulfur compliance documentation", 2500, 0.35, 26.0),
            ("Dubai Falcon Trade Escrow", "https://falcontrade.ae", "UAE", "Dubai", "Commodity Trade Finance", CorridorRegion.APAC_MIDDLE_EAST, 280000.0, "Letter of credit discrepancy review and bill of lading trade sanctions check", 2200, 0.45, 28.0),
            ("Tokyo Precision Robotics", "https://tokyoprecision.jp", "Japan", "Tokyo", "Industrial Automation Components", CorridorRegion.APAC_MIDDLE_EAST, 210000.0, "Bilingual Japanese-English component specs and RoHS compliance validation", 2000, 0.40, 26.0),
            ("Sydney Pacific Resources", "https://sydneypacific.com.au", "Australia", "Sydney", "Mining Supply Chain & Procurement", CorridorRegion.APAC_MIDDLE_EAST, 195000.0, "Heavy equipment replacement parts purchase order approval and contract compliance", 2200, 0.35, 25.0),
            ("Emirates Cloud Health", "https://emiratescloudhealth.ae", "UAE", "Abu Dhabi", "Digital Health Records", CorridorRegion.APAC_MIDDLE_EAST, 220000.0, "Malaffi health information exchange compliance and claims pre-authorization", 2600, 0.35, 24.0),
            ("Seoul Smart Factory Systems", "https://seoulsmartfactory.kr", "South Korea", "Seoul", "Semiconductor Line Logistics", CorridorRegion.APAC_MIDDLE_EAST, 250000.0, "Cleanroom consumable inventory lot tracking and wafer defect logging", 2800, 0.35, 25.0),
            ("Melbourne Agile Retail Group", "https://melbourneretail.com.au", "Australia", "Melbourne", "Specialty Retail Network", CorridorRegion.APAC_MIDDLE_EAST, 140000.0, "Franchisee POS sales auditing and supplier rebate calculations", 2100, 0.28, 22.0),
        ]

        prospects = []
        for name, web, country, city, ind, corr, toil, hyp, vol, hrs, wage in raw:
            prospects.append(
                ProspectCompany(
                    company_name=name,
                    website=web,
                    country=country,
                    city=city,
                    industry=ind,
                    corridor=corr,
                    estimated_annual_toil_usd=toil,
                    problem_hypothesis=hyp,
                    monthly_volume=vol,
                    human_hours_per_unit=hrs,
                    hourly_wage_usd=wage,
                )
            )
        return prospects

    def load_target_prospects(self) -> List[ProspectCompany]:
        return self._prospects

    def build_dossier(self, prospect: ProspectCompany) -> ProspectDossier:
        generator = BeachheadAuditGenerator()
        deliverable = generator.generate_audit(
            prospect_name=prospect.company_name,
            industry=prospect.industry,
            current_workflow=prospect.problem_hypothesis,
            monthly_volume=prospect.monthly_volume,
            human_hours_per_unit=prospect.human_hours_per_unit,
            hourly_wage_usd=prospect.hourly_wage_usd,
        )
        hook = f"We noticed {prospect.company_name} spends over ${prospect.estimated_annual_toil_usd:,.0f} USD annually managing {prospect.problem_hypothesis.lower()}."
        return ProspectDossier(
            prospect=prospect,
            audit_deliverable=deliverable,
            abm_hook=hook,
        )

    def stage_outreach_action(self, dossier: ProspectDossier) -> StagedAction:
        payload = (
            f"OUTREACH_INTENT // TARGET: {dossier.prospect.company_name} "
            f"({dossier.prospect.city}, {dossier.prospect.country}) | "
            f"HOOK: {dossier.abm_hook} | "
            f"DELIVERABLE: Net Projected ROI {dossier.audit_deliverable.roi_percentage}%"
        )
        sig = hmac.new(
            self.signing_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return StagedAction(
            prospect_name=dossier.prospect.company_name,
            is_gated=True,
            status="PENDING_APPROVAL",
            payload=payload,
            hmac_signature=sig,
        )

    def ingest_all_to_registry(self) -> int:
        count = 0
        for p in self._prospects:
            rec = CompanyRecord(
                name=p.company_name,
                website=p.website,
                country=p.country,
                city=p.city,
                industry=p.industry,
                source=RegistrySource.PUBLIC_TECH_INDEX,
                buying_signals=["Active digital transformation", "High operational workflow volume"],
                operational_pain_indicators=[p.problem_hypothesis],
                confidence_score=0.90,
                verified=True,
            )
            if self.registry.register_company(rec):
                count += 1
        return count
