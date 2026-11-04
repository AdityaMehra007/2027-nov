"""World Client Directory: Global multi-hub client registry, sector taxonomy, and prospect ingestion."""

from __future__ import annotations

import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from omniverse.modules.agency.models import (
    Lead,
    LeadStage,
    ProspectArchetype,
)


class GlobalHub(str, Enum):
    SF_BAY_AREA = "SF_BAY_AREA"
    NEW_YORK = "NEW_YORK"
    LONDON = "LONDON"
    BERLIN = "BERLIN"
    SINGAPORE = "SINGAPORE"
    TOKYO = "TOKYO"
    DUBAI = "DUBAI"
    BENGALURU = "BENGALURU"


class IndustrySector(str, Enum):
    SAAS_DEVTOOLS = "SAAS_DEVTOOLS"
    FINTECH_PAYMENTS = "FINTECH_PAYMENTS"
    HEALTHCARE_CLINICAL = "HEALTHCARE_CLINICAL"
    ECOMMERCE_DTC = "ECOMMERCE_DTC"
    CLEANTECH_ENERGY = "CLEANTECH_ENERGY"
    SMB_SERVICES = "SMB_SERVICES"


class WorldClient(BaseModel):
    """Represents an international enterprise, scaleup, or commercial client."""

    client_id: str = Field(default_factory=lambda: f"wclient_{uuid.uuid4().hex[:12]}")
    name: str
    hub: GlobalHub
    sector: IndustrySector
    website: str
    country: str
    tech_stack: List[str] = Field(default_factory=list)
    annual_revenue_usd: float = 1_000_000.0
    declared_needs: List[str] = Field(default_factory=list)
    employee_count: int = 50
    founded_year: int = 2020


class WorldClientDirectory:
    """Master repository and query engine for international commercial clients."""

    SEED_CLIENTS: List[dict] = [
        # San Francisco / Silicon Valley
        {
            "name": "Apex Neural Compute",
            "hub": GlobalHub.SF_BAY_AREA,
            "sector": IndustrySector.SAAS_DEVTOOLS,
            "website": "https://apexcompute.ai",
            "country": "United States",
            "tech_stack": ["Python", "PyTorch", "FastAPI", "Kubernetes", "PostgreSQL"],
            "annual_revenue_usd": 12_500_000.0,
            "declared_needs": ["Automated multi-tenant billing", "Low-latency streaming API", "Developer documentation portal"],
            "employee_count": 85,
            "founded_year": 2023,
        },
        {
            "name": "Soma Clinical Robotics",
            "hub": GlobalHub.SF_BAY_AREA,
            "sector": IndustrySector.HEALTHCARE_CLINICAL,
            "website": "https://somarobotics.health",
            "country": "United States",
            "tech_stack": ["C++", "Python", "ROS2", "React", "HIPAA-Cloud"],
            "annual_revenue_usd": 8_900_000.0,
            "declared_needs": ["Tele-surgery telemetry portal", "24/7 AI surgical nurse concierge", "Real-time audit compliance logs"],
            "employee_count": 45,
            "founded_year": 2022,
        },
        {
            "name": "Mission Solar Grid",
            "hub": GlobalHub.SF_BAY_AREA,
            "sector": IndustrySector.CLEANTECH_ENERGY,
            "website": "https://missionsolargrid.com",
            "country": "United States",
            "tech_stack": ["Python", "Go", "TimescaleDB", "InfluxDB", "Grafana"],
            "annual_revenue_usd": 6_200_000.0,
            "declared_needs": ["Virtual power plant telemetry", "Automated inverter fault alerts", "Commercial battery billing engine"],
            "employee_count": 38,
            "founded_year": 2021,
        },

        # New York
        {
            "name": "Gotham Liquidity Partners",
            "hub": GlobalHub.NEW_YORK,
            "sector": IndustrySector.FINTECH_PAYMENTS,
            "website": "https://gothamliquidity.com",
            "country": "United States",
            "tech_stack": ["Rust", "Python", "FIX Protocol", "Kafka", "ClickHouse"],
            "annual_revenue_usd": 45_000_000.0,
            "declared_needs": ["Sub-millisecond FX triangular arbitrage monitor", "SEC/FINRA compliance reporter", "Institutional treasury dashboard"],
            "employee_count": 120,
            "founded_year": 2019,
        },
        {
            "name": "Manhattan Velvet Apparel",
            "hub": GlobalHub.NEW_YORK,
            "sector": IndustrySector.ECOMMERCE_DTC,
            "website": "https://manhattanvelvet.nyc",
            "country": "United States",
            "tech_stack": ["Shopify Plus", "Next.js", "Klaviyo", "TailwindCSS"],
            "annual_revenue_usd": 4_800_000.0,
            "declared_needs": ["Omni-channel return portal", "Predictive replenishment agent", "High-converting SMS abandonment funnel"],
            "employee_count": 25,
            "founded_year": 2020,
        },
        {
            "name": "Hudson Private Wealth Legal",
            "hub": GlobalHub.NEW_YORK,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://hudsonwealthlaw.com",
            "country": "United States",
            "tech_stack": ["WordPress", "Clio", "DocuSign", "Office365"],
            "annual_revenue_usd": 3_100_000.0,
            "declared_needs": ["Ultra-secure client document vault", "Automated retainer agreement workflow", "24/7 VIP concierge chatbot"],
            "employee_count": 18,
            "founded_year": 2015,
        },

        # London
        {
            "name": "Thames Cross-Border Clearing",
            "hub": GlobalHub.LONDON,
            "sector": IndustrySector.FINTECH_PAYMENTS,
            "website": "https://thamesclearing.co.uk",
            "country": "United Kingdom",
            "tech_stack": ["Go", "Java", "Swift ISO 20022", "PostgreSQL", "Docker"],
            "annual_revenue_usd": 28_000_000.0,
            "declared_needs": ["Multi-currency instant FX netting", "Automated AML screening agent", "Real-time SEPA/Bacs webhook broker"],
            "employee_count": 95,
            "founded_year": 2020,
        },
        {
            "name": "Kensington Aesthetics & Longevity",
            "hub": GlobalHub.LONDON,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://kensingtonlongevity.co.uk",
            "country": "United Kingdom",
            "tech_stack": ["Squarespace", "Phorest", "Stripe", "Instagram"],
            "annual_revenue_usd": 1_850_000.0,
            "declared_needs": ["VIP recurring treatment membership portal", "Zero-friction booking system", "Automated post-care WhatsApp notifications"],
            "employee_count": 14,
            "founded_year": 2018,
        },
        {
            "name": "Shoreditch Synthetics AI",
            "hub": GlobalHub.LONDON,
            "sector": IndustrySector.SAAS_DEVTOOLS,
            "website": "https://shoreditchsynthetics.ai",
            "country": "United Kingdom",
            "tech_stack": ["Python", "FastAPI", "React", "Redis", "AWS"],
            "annual_revenue_usd": 5_400_000.0,
            "declared_needs": ["Self-serve API credit billing system", "High-converting programmatic landing pages", "Automated developer onboarding"],
            "employee_count": 32,
            "founded_year": 2022,
        },

        # Berlin
        {
            "name": "Brandenburg Green Battery",
            "hub": GlobalHub.BERLIN,
            "sector": IndustrySector.CLEANTECH_ENERGY,
            "website": "https://brandenburgbattery.de",
            "country": "Germany",
            "tech_stack": ["C++", "Python", "Rust", "MQTT", "Grafana"],
            "annual_revenue_usd": 18_200_000.0,
            "declared_needs": ["Industrial battery lifecycle forecasting", "Automated EU carbon taxonomy reporting", "B2B warranty claim API"],
            "employee_count": 110,
            "founded_year": 2021,
        },
        {
            "name": "Mitte Cloud Security",
            "hub": GlobalHub.BERLIN,
            "sector": IndustrySector.SAAS_DEVTOOLS,
            "website": "https://mittecloud.io",
            "country": "Germany",
            "tech_stack": ["Go", "Kubernetes", "eBPF", "Terraform", "Vue.js"],
            "annual_revenue_usd": 7_600_000.0,
            "declared_needs": ["Automated zero-trust container scanner", "Self-service SOC-2 compliance exporter", "Enterprise SSO gateway"],
            "employee_count": 48,
            "founded_year": 2020,
        },
        {
            "name": "Kreuzberg Specialty Roast",
            "hub": GlobalHub.BERLIN,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://kreuzbergroast.de",
            "country": "Germany",
            "tech_stack": ["Shopify", "Instagram", "iZettle"],
            "annual_revenue_usd": 920_000.0,
            "declared_needs": ["B2B recurring wholesale coffee portal", "Automated invoice dispatching", "Customer loyalty mobile pass"],
            "employee_count": 12,
            "founded_year": 2017,
        },

        # Singapore
        {
            "name": "Marina Bay Sovereign Wealth Analytics",
            "hub": GlobalHub.SINGAPORE,
            "sector": IndustrySector.FINTECH_PAYMENTS,
            "website": "https://marinabay-analytics.sg",
            "country": "Singapore",
            "tech_stack": ["Python", "Julia", "ClickHouse", "FastAPI", "React"],
            "annual_revenue_usd": 32_000_000.0,
            "declared_needs": ["Cross-asset sovereign risk simulator", "Automated MAS regulatory filing engine", "Portfolio stress-testing engine"],
            "employee_count": 75,
            "founded_year": 2019,
        },
        {
            "name": "Lion City Health Diagnostics",
            "hub": GlobalHub.SINGAPORE,
            "sector": IndustrySector.HEALTHCARE_CLINICAL,
            "website": "https://lioncityhealth.sg",
            "country": "Singapore",
            "tech_stack": ["Next.js", "Python", "FastAPI", "PostgreSQL", "FHIR"],
            "annual_revenue_usd": 6_400_000.0,
            "declared_needs": ["Genomic health report generator", "Direct patient portal with SingPass auth", "Automated medical appointment reminders"],
            "employee_count": 40,
            "founded_year": 2021,
        },
        {
            "name": "Straits Supply Chain Hub",
            "hub": GlobalHub.SINGAPORE,
            "sector": IndustrySector.ECOMMERCE_DTC,
            "website": "https://straitssupply.com.sg",
            "country": "Singapore",
            "tech_stack": ["Node.js", "PostgreSQL", "Redis", "React"],
            "annual_revenue_usd": 14_000_000.0,
            "declared_needs": ["Real-time customs clearance webhook", "Automated multi-carrier freight calculation", "B2B distributor order portal"],
            "employee_count": 65,
            "founded_year": 2020,
        },

        # Tokyo
        {
            "name": "Marunouchi Autonomous Logistics",
            "hub": GlobalHub.TOKYO,
            "sector": IndustrySector.SAAS_DEVTOOLS,
            "website": "https://marunouchi-logistics.jp",
            "country": "Japan",
            "tech_stack": ["Rust", "Python", "ROS2", "Docker", "AWS"],
            "annual_revenue_usd": 22_000_000.0,
            "declared_needs": ["Automated warehouse dispatch engine", "Fleet telematics visualizer", "Sub-second pallet tracking API"],
            "employee_count": 90,
            "founded_year": 2018,
        },
        {
            "name": "Ginza Precision Dental",
            "hub": GlobalHub.TOKYO,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://ginzadental-clinic.jp",
            "country": "Japan",
            "tech_stack": ["HTML5", "PHP", "MySQL", "LinePay"],
            "annual_revenue_usd": 2_400_000.0,
            "declared_needs": ["Line-integrated appointment concierge", "Automated pre-op dental instructions", "English-Japanese bilingual booking flow"],
            "employee_count": 16,
            "founded_year": 2016,
        },
        {
            "name": "Shibuya Streetwear Direct",
            "hub": GlobalHub.TOKYO,
            "sector": IndustrySector.ECOMMERCE_DTC,
            "website": "https://shibuyastreetwear.co.jp",
            "country": "Japan",
            "tech_stack": ["Shopify Plus", "Next.js", "Stripe", "Klaviyo"],
            "annual_revenue_usd": 5_100_000.0,
            "declared_needs": ["High-velocity flash drop countdown system", "Bot protection checkout safeguard", "Global cross-border yen settlement"],
            "employee_count": 28,
            "founded_year": 2021,
        },

        # Dubai
        {
            "name": "DIFC Prime Asset Custody",
            "hub": GlobalHub.DUBAI,
            "sector": IndustrySector.FINTECH_PAYMENTS,
            "website": "https://difccustody.ae",
            "country": "United Arab Emirates",
            "tech_stack": ["Go", "Python", "Hyperledger", "PostgreSQL", "FastAPI"],
            "annual_revenue_usd": 38_000_000.0,
            "declared_needs": ["DFSA-compliant digital asset escrow", "Multi-signature corporate treasury portal", "Instant dirham-dollar-euro settlement"],
            "employee_count": 80,
            "founded_year": 2020,
        },
        {
            "name": "Palm Jumeirah Luxury Estates",
            "hub": GlobalHub.DUBAI,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://palmluxuryestates.ae",
            "country": "United Arab Emirates",
            "tech_stack": ["WordPress", "PropertyFinder API", "Salesforce", "WhatsApp Business"],
            "annual_revenue_usd": 16_500_000.0,
            "declared_needs": ["VIP virtual 3D tour lead capture engine", "Instant WhatsApp brochure dispatcher", "Zero-brokerage direct buyer alert radar"],
            "employee_count": 35,
            "founded_year": 2017,
        },
        {
            "name": "Emirates Solar Power Hub",
            "hub": GlobalHub.DUBAI,
            "sector": IndustrySector.CLEANTECH_ENERGY,
            "website": "https://emiratessolar.ae",
            "country": "United Arab Emirates",
            "tech_stack": ["Python", "SCADA", "TimescaleDB", "React"],
            "annual_revenue_usd": 27_000_000.0,
            "declared_needs": ["Desert dust degradation tracking AI", "Grid feed-in tariff calculator", "Predictive maintenance scheduling agent"],
            "employee_count": 105,
            "founded_year": 2019,
        },

        # Bengaluru
        {
            "name": "Indiranagar Cloud Orchestrator",
            "hub": GlobalHub.BENGALURU,
            "sector": IndustrySector.SAAS_DEVTOOLS,
            "website": "https://cloudorch.in",
            "country": "India",
            "tech_stack": ["Python", "FastAPI", "Go", "Docker", "PostgreSQL"],
            "annual_revenue_usd": 4_200_000.0,
            "declared_needs": ["Automated multi-cloud cost optimizer", "Instant developer environment preview", "Self-service usage billing via Stripe & Razorpay"],
            "employee_count": 42,
            "founded_year": 2022,
        },
        {
            "name": "Koramangala BioDiagnostics",
            "hub": GlobalHub.BENGALURU,
            "sector": IndustrySector.HEALTHCARE_CLINICAL,
            "website": "https://koramangalabio.in",
            "country": "India",
            "tech_stack": ["Python", "Django", "PostgreSQL", "React", "Twilio"],
            "annual_revenue_usd": 2_800_000.0,
            "declared_needs": ["Instant WhatsApp blood test delivery bot", "Home sample collection dispatch scheduler", "Automated NABL accreditation audit logger"],
            "employee_count": 30,
            "founded_year": 2021,
        },
        {
            "name": "HSR Retail Collective",
            "hub": GlobalHub.BENGALURU,
            "sector": IndustrySector.ECOMMERCE_DTC,
            "website": "https://hsrcollective.in",
            "country": "India",
            "tech_stack": ["Shopify", "Razorpay UPI", "Shiprocket", "Node.js"],
            "annual_revenue_usd": 1_650_000.0,
            "declared_needs": ["Instant UPI dynamic QR checkout generator", "RTO fraud reduction engine", "High-retention WhatsApp replenishment campaign"],
            "employee_count": 22,
            "founded_year": 2020,
        },
        {
            "name": "Whitefield Specialty Wellness",
            "hub": GlobalHub.BENGALURU,
            "sector": IndustrySector.SMB_SERVICES,
            "website": "https://whitefieldwellness.in",
            "country": "India",
            "tech_stack": ["WordPress", "Calendly", "Razorpay", "Instagram"],
            "annual_revenue_usd": 850_000.0,
            "declared_needs": ["24/7 WhatsApp AI consultation booking bot", "Membership recurring UPI auto-debit system", "Local Google Business profile ranking engine"],
            "employee_count": 15,
            "founded_year": 2019,
        },
    ]

    def __init__(self):
        self._clients: List[WorldClient] = [
            WorldClient(**data) for data in self.SEED_CLIENTS
        ]

    def get_all_clients(self) -> List[WorldClient]:
        """Returns the full international registry of commercial clients."""
        return list(self._clients)

    def filter_clients(
        self,
        hub: Optional[GlobalHub] = None,
        sector: Optional[IndustrySector] = None,
        min_revenue: Optional[float] = None,
        max_revenue: Optional[float] = None,
    ) -> List[WorldClient]:
        """Filter global clients by geographical hub, industry sector, and revenue thresholds."""
        results = self._clients
        if hub is not None:
            results = [c for c in results if c.hub == hub]
        if sector is not None:
            results = [c for c in results if c.sector == sector]
        if min_revenue is not None:
            results = [c for c in results if c.annual_revenue_usd >= min_revenue]
        if max_revenue is not None:
            results = [c for c in results if c.annual_revenue_usd <= max_revenue]
        return results

    def get_client_by_name(self, name: str) -> Optional[WorldClient]:
        """Lookup a specific client by business name (case-insensitive substring match)."""
        target = name.strip().lower()
        for client in self._clients:
            if target == client.name.lower() or target in client.name.lower():
                return client
        return None

    def to_crm_leads(self, limit: int = 25) -> List[Lead]:
        """Converts world clients into CRM Leads for immediate pipeline integration."""
        leads: List[Lead] = []
        for client in self._clients[:limit]:
            # Map IndustrySector to ProspectArchetype
            if client.sector == IndustrySector.SAAS_DEVTOOLS:
                arch = ProspectArchetype.SAAS_STARTUP
            elif client.sector in (IndustrySector.FINTECH_PAYMENTS, IndustrySector.CLEANTECH_ENERGY):
                arch = ProspectArchetype.ENTERPRISE
            elif client.sector == IndustrySector.ECOMMERCE_DTC:
                arch = ProspectArchetype.ECOMMERCE
            else:
                arch = ProspectArchetype.LOCAL_SMB

            lead = Lead(
                id=f"lead_{client.client_id.replace('wclient_', '')}",
                business_name=client.name,
                archetype=arch,
                website=client.website,
                contact_email=f"founders@{client.website.replace('https://', '').replace('http://', '').strip('/')}",
                estimated_annual_revenue_usd=client.annual_revenue_usd,
                stage=LeadStage.DISCOVERED,
            )
            leads.append(lead)
        return leads
