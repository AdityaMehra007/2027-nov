# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Customer Category Taxonomy & Revenue Model Catalogue (PROJECT ONE)."""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class CustomerCategory:
    name: str
    tier: str  # INDIVIDUAL, MICRO, SMB, MID_MARKET, ENTERPRISE, SPECIALIZED
    avg_budget_monthly_usd: float
    core_pain_points: List[str]
    description: str = ""
    willingness_to_pay_score: float = 7.0
    willingness_to_pay_score: float = 7.0


class CustomerTaxonomy:
    """Canonical registry of 60+ customer categories across commerce, tech, and services."""

    def __init__(self):
        self._categories: Dict[str, CustomerCategory] = {}
        self._init_taxonomy()

    def _init_taxonomy(self):
        # 60+ comprehensive customer categories
        raw_data = [
            ("Individuals", "INDIVIDUAL", 29.0, ["Time-consuming repetitive tasks", "Personal budgeting", "Job application tracking"]),
            ("Small businesses", "SMB", 250.0, ["Cash flow tracking", "Invoice chasing", "Customer lead capture", "Vendor coordination"]),
            ("Marketing agencies", "SMB", 500.0, ["Client reporting overhead", "Ad spend tracking", "Content calendar bottlenecks", "Lead attribution"]),
            ("SaaS businesses", "MID_MARKET", 1200.0, ["High cloud inference costs", "Churn prediction", "Feature flag management", "Customer onboarding drop-off"]),
            ("Large enterprises", "ENTERPRISE", 5000.0, ["Multi-ERP reconciliation", "Sox compliance auditing", "Vendor OTIF delays", "Siloed legacy data"]),
            ("Logistics companies", "SMB", 800.0, ["Manual freight bill verification", "Route optimization", "Fleet maintenance scheduling", "Carrier SLA disputes"]),
            ("Accounting firms", "SMB", 600.0, ["Tax season receipt parsing", "Bank statement reconciliation", "Client document collection", "Timesheet audits"]),
            ("Law firms", "MID_MARKET", 1500.0, ["Contract clause extraction", "E-discovery document scanning", "Billing realization tracking", "Client conflict checks"]),
            ("Medical practices", "SMB", 750.0, ["Patient intake form transcription", "Insurance pre-authorization", "Appointment no-show reduction", "Telehealth scheduling"]),
            ("Dental clinics", "SMB", 400.0, ["Patient recall automation", "Insurance claim processing", "Supply ordering inventory", "Review generation"]),
            ("Real estate brokerages", "SMB", 500.0, ["Lead qualification speed", "Listing syndication errors", "Commission split calculations", "Client follow-ups"]),
            ("Property management", "SMB", 650.0, ["Tenant maintenance requests", "Rent collection reminders", "Vendor dispatching", "Lease renewal tracking"]),
            ("E-commerce brands", "SMB", 800.0, ["Return fraud detection", "Cart abandonment recovery", "Multi-warehouse stock sync", "Ad creative exhaustion"]),
            ("Dropshipping operators", "MICRO", 150.0, ["Supplier order forwarding", "Tracking number sync", "Customer service inquiries", "Margin erosion"]),
            ("Independent restaurants", "SMB", 200.0, ["Menu pricing vs food cost inflation", "Labor shift scheduling", "Online delivery reconciliation", "Food waste tracking"]),
            ("Ghost kitchens", "SMB", 350.0, ["Multi-platform tablet chaos", "Ingredient inventory depletion", "Order prep pacing", "Review management"]),
            ("Coffee shops & Cafes", "MICRO", 100.0, ["Barista scheduling", "Inventory shrinkage", "Loyalty program engagement", "Peak hour queue times"]),
            ("Fitness centers & Gyms", "SMB", 300.0, ["Member churn after trial", "Personal trainer payout tracking", "Equipment repair tickets", "Recurring billing failures"]),
            ("Yoga & Pilates studios", "MICRO", 150.0, ["Class capacity management", "Instructor sub scheduling", "Late cancellation fees", "Membership renewals"]),
            ("Co-working spaces", "SMB", 600.0, ["Hot desk occupancy tracking", "Conference room billing", "Visitor badge printing", "High-speed Wi-Fi tiering"]),
            ("Construction contractors", "SMB", 900.0, ["Subcontractor lien waivers", "Change order cost tracking", "Material delivery delays", "Daily site job logs"]),
            ("Plumbing services", "SMB", 350.0, ["Emergency dispatch routing", "Parts inventory on trucks", "Invoice generation in field", "Review collection"]),
            ("HVAC contractors", "SMB", 450.0, ["Seasonal tune-up reminders", "Warranty claim filing", "Technician job time tracking", "Equipment financing"]),
            ("Electrical contractors", "SMB", 400.0, ["Permit status tracking", "Copper wire price fluctuations", "Job site safety sign-offs", "Progress billing"]),
            ("Auto repair shops", "SMB", 350.0, ["Parts sourcing delays", "Mechanic flat-rate hours", "Customer estimate approvals", "Fleet commercial billing"]),
            ("Car dealerships", "MID_MARKET", 1500.0, ["Vehicle inventory floor plan costs", "Test drive lead follow-up", "Trade-in valuation consistency", "F&I compliance"]),
            ("Veterinary clinics", "SMB", 500.0, ["Prescription refill reminders", "Pet vaccine records tracking", "Emergency triage scheduling", "Specialist lab sync"]),
            ("Architecture firms", "SMB", 700.0, ["BIM file versioning", "Project milestone billing", "Consultant fee allocations", "Design review markups"]),
            ("Interior designers", "MICRO", 250.0, ["Client sample tracking", "Custom furniture lead times", "Deposit vs balance collection", "Vendor trade discounts"]),
            ("Civil engineering firms", "MID_MARKET", 1200.0, ["Environmental compliance filings", "CAD drawing review bottlenecks", "Sub-consultant cost control", "Field inspection logs"]),
            ("Freight brokers", "SMB", 900.0, ["Load board rate haggling", "Driver check calls", "Lumper receipt reconciliation", "Factoring company approvals"]),
            ("Warehouse operators", "MID_MARKET", 1400.0, ["Cross-docking scheduling", "Forklift telematics monitoring", "Space utilization efficiency", "Pick-and-pack error rates"]),
            ("Last-mile courier fleets", "SMB", 600.0, ["Fuel surcharge calculations", "Proof-of-delivery photo archival", "Driver payout deductions", "Route re-sequencing"]),
            ("Commercial cleaning companies", "SMB", 300.0, ["Janitor shift attendance", "Cleaning chemical replenishment", "Client inspection scorecards", "Subcontractor 1099 tracking"]),
            ("Landscaping contractors", "SMB", 350.0, ["Weather-induced rescheduling", "Mower maintenance logs", "HOA contract compliance", "Commercial snow removal dispatch"]),
            ("Pest control services", "SMB", 250.0, ["Chemical application reporting", "Quarterly renewal contracts", "Field technician GPS logs", "Customer prep checklists"]),
            ("Security guard firms", "SMB", 500.0, ["Guard post verification NFC", "Incident report generation", "Overtime hour controls", "Client billing reconciliation"]),
            ("Staffing & Recruitment agencies", "SMB", 700.0, ["Resume parsing & screening", "Candidate interview scheduling", "Client job order fill rates", "Timesheet approval chasing"]),
            ("Executive search boutiques", "MICRO", 400.0, ["C-suite candidate confidentiality", "Client retainers vs placement fees", "Background check coordination", "Talent mapping"]),
            ("Management consultancies", "MID_MARKET", 1800.0, ["Consultant billable utilization", "Deliverable QA formatting", "Client expense pass-throughs", "Knowledge base indexing"]),
            ("PR & Communications agencies", "SMB", 600.0, ["Media list clipping verification", "Pitch response tracking", "Client monthly retainer reporting", "Crisis response timing"]),
            ("Web development studios", "SMB", 500.0, ["Scope creep management", "Client feedback on staging sites", "Server maintenance contracts", "Milestone payment delays"]),
            ("Mobile app studios", "SMB", 750.0, ["App Store rejection debugging", "Crash log triage", "Cross-platform QA matrix", "SDK version compatibility"]),
            ("Cybersecurity MSPs", "MID_MARKET", 1600.0, ["Alert fatigue in SOC", "Patching compliance reporting", "Incident post-mortem timelines", "Multi-tenant firewall audits"]),
            ("Cloud hosting providers", "MID_MARKET", 2000.0, ["Bandwidth overage billing", "Hardware node failure alerts", "DDoS mitigation telemetry", "Customer support SLA"]),
            ("EdTech startups", "SMB", 600.0, ["Student churn after lesson 3", "Tutor commission payouts", "Video stream buffering logs", "Quiz performance analytics"]),
            ("Tutoring centers", "MICRO", 200.0, ["Parent student progress reports", "Tutor hourly payroll", "Diagnostic test evaluations", "Seasonal summer drop"]),
            ("Language academies", "SMB", 300.0, ["Placement test scoring", "Native instructor visa tracking", "Small group lesson scheduling", "Certificates of completion"]),
            ("Charities & Non-profits", "SMB", 250.0, ["Donor gift matching tracking", "Grant application deadline tracking", "Volunteer hour logging", "Annual IRS 990 audit prep"]),
            ("Faith-based organizations", "MICRO", 150.0, ["Congregation tithing records", "Event room reservations", "Weekly bulletin creation", "Mission trip expense tracking"]),
            ("Alumni associations", "SMB", 300.0, ["Graduation cohort address updates", "Endowment contribution campaigns", "Reunion ticket sales", "Mentorship pairing"]),
            ("Event planners & Venues", "SMB", 500.0, ["Catering dietary requirement tracking", "Vendor load-in schedules", "Client payment deposit schedules", "Floorplan approvals"]),
            ("Wedding coordinators", "MICRO", 250.0, ["Bride & groom timeline sync", "Florist arrival confirmations", "RSVP headcount mismatches", "Day-of vendor coordination"]),
            ("Commercial photography studios", "MICRO", 200.0, ["RAW photo batch export & culling", "Client proofing galleries", "Model release form archives", "Studio equipment rentals"]),
            ("Video production houses", "SMB", 600.0, ["Footage proxy generation", "Client timestamped review notes", "Music licensing tracking", "Freelance editor rates"]),
            ("Podcast networks", "MICRO", 250.0, ["Sponsor dynamic ad insertion", "Episode transcription accuracy", "Guest pre-interview prep sheets", "Distribution feed sync"]),
            ("Book publishers", "MID_MARKET", 1100.0, ["Author royalty calculation splits", "ISBN & metadata feeds", "Typesetting error proofs", "Inventory return reserves"]),
            ("Game developers", "SMB", 800.0, ["Player telemetry ingestion", "In-app purchase store verification", "Liveops event scheduling", "Multiplayer matchmaking ping"]),
            ("Agritech & Farms", "SMB", 450.0, ["Soil moisture sensor telemetry", "Fertilizer purchase hedging", "Produce harvest labor tracking", "Cold storage temp compliance"]),
            ("Aquaculture & Fisheries", "SMB", 500.0, ["Water oxygenation logs", "Feed conversion ratio tracking", "Hatchery mortality rates", "Export tariff documentation"]),
            ("Solar installation companies", "SMB", 700.0, ["Utility interconnection paperwork", "Roof design CAD turnaround", "Customer financing approvals", "Crew safety audit logs"]),
            ("Biotech research labs", "MID_MARKET", 2500.0, ["FDA clinical trial data audit", "Reagent temperature monitoring", "Lab equipment calibration records", "Grant spending compliance"]),
            ("Specialty manufacturers", "MID_MARKET", 1500.0, ["CNC machine downtime logging", "BOM cost tracking", "Raw material lead times", "Quality reject rate analysis"]),
        ]

        for name, tier, budget, pains in raw_data:
            self._categories[name] = CustomerCategory(
                name=name,
                tier=tier,
                avg_budget_monthly_usd=budget,
                core_pain_points=pains,
                description=f"Standardized profile for {name} ({tier}) with primary pains in {', '.join(pains[:2])}."
            )

    def list_categories(self) -> List[CustomerCategory]:
        return list(self._categories.values())

    def get_category(self, name: str) -> Optional[CustomerCategory]:
        return self._categories.get(name)


@dataclass
class RevenueModel:
    name: str
    typical_monthly_usd: float
    gross_margin_pct: float
    clients_needed_for_10_usd_day: int
    clients_needed_for_100_usd_day: int
    description: str = ""


class RevenueModelCatalogue:
    """Catalogue of 50+ proven monetization models with daily revenue targets."""

    def __init__(self):
        self._models: Dict[str, RevenueModel] = {}
        self._init_models()

    def _init_models(self):
        # 50 monetization models
        raw_models = [
            ("SaaS subscriptions", 99.0, 85.0),
            ("Productized services", 299.0, 75.0),
            ("AI automation implementation", 1500.0, 80.0),
            ("Document processing", 199.0, 90.0),
            ("Software QA", 250.0, 85.0),
            ("Usage-based API metering", 49.0, 90.0),
            ("White-label agency reselling", 499.0, 70.0),
            ("Retainer advisory audits", 750.0, 85.0),
            ("Managed security monitoring", 399.0, 80.0),
            ("Compliance verification reports", 299.0, 85.0),
            ("Data pipeline orchestration", 450.0, 80.0),
            ("Database tuning and backup", 199.0, 85.0),
            ("Reverse-engineered data extraction", 500.0, 75.0),
            ("Automated invoice matching", 149.0, 90.0),
            ("Customer onboarding flows", 299.0, 80.0),
            ("Lead enrichment subscriptions", 129.0, 85.0),
            ("E-commerce cart recovery bots", 199.0, 85.0),
            ("Custom webhook infrastructure", 99.0, 90.0),
            ("Ad spend arbitrage monitoring", 350.0, 75.0),
            ("Competitor intelligence feeds", 149.0, 85.0),
            ("Regulatory filing assistants", 400.0, 80.0),
            ("Vendor SLA auditing tools", 250.0, 85.0),
            ("Cloud cost optimization agents", 300.0, 80.0),
            ("Micro-ERP for vertical niches", 199.0, 85.0),
            ("Contract clause extraction APIs", 299.0, 85.0),
            ("Staffing resume screeners", 179.0, 85.0),
            ("Property maintenance bots", 149.0, 85.0),
            ("Customer feedback sentiment triage", 99.0, 90.0),
            ("Incident post-mortem automation", 199.0, 85.0),
            ("Multi-channel social syndication", 79.0, 90.0),
            ("Dark store inventory rebalancer", 450.0, 80.0),
            ("Telematics fuel audit service", 299.0, 80.0),
            ("Emergency dispatch routing SaaS", 399.0, 80.0),
            ("B2B payment reconciliation engine", 249.0, 85.0),
            ("Automated SEO content cluster engine", 199.0, 85.0),
            ("Lead qualification SMS bot", 149.0, 85.0),
            ("Review booster & reputation manager", 99.0, 90.0),
            ("Warranty claim parsing system", 299.0, 80.0),
            ("Subcontractor lien waiver tracker", 199.0, 85.0),
            ("Medical intake transcription API", 349.0, 85.0),
            ("Event vendor timeline coordination", 149.0, 85.0),
            ("Patent prior art searching tool", 499.0, 80.0),
            ("B2B cold outbound personalization", 199.0, 80.0),
            ("Dynamic pricing engine for rentals", 299.0, 80.0),
            ("Supply chain stress testing sim", 600.0, 80.0),
            ("AI video prompt generator", 49.0, 90.0),
            ("Audio transcription with diarization", 89.0, 85.0),
            ("Algorithmic backtesting sandbox", 199.0, 85.0),
            ("Executive KPI daily digest builder", 99.0, 90.0),
            ("Automated churn save flow manager", 149.0, 85.0),
        ]

        target_10_usd_day = 300.0   # $10/day = ~$300/mo
        target_100_usd_day = 3000.0 # $100/day = ~$3000/mo

        for name, monthly, margin in raw_models:
            clients_10 = max(1, math.ceil(target_10_usd_day / monthly))
            clients_100 = max(clients_10, math.ceil(target_100_usd_day / monthly))
            self._models[name] = RevenueModel(
                name=name,
                typical_monthly_usd=monthly,
                gross_margin_pct=margin,
                clients_needed_for_10_usd_day=clients_10,
                clients_needed_for_100_usd_day=clients_100,
                description=f"Model {name} at ${monthly}/mo with {margin}% gross margin."
            )

    def list_models(self) -> List[RevenueModel]:
        return list(self._models.values())

    def get_model(self, name: str) -> Optional[RevenueModel]:
        return self._models.get(name)
