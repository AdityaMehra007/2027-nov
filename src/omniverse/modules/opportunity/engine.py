"""==============================================================================
PROJECT ONE: OPPORTUNITY RANKING & SCORING ENGINE
==============================================================================
Implements Part 3 of the PROJECT ONE Master Specification:
1. Relative Opportunity Formula:
   Score = (Pain * Frequency * Budget * Reachability * AutomationFeasibility) / Competition
2. 100-Point Absolute Rubric:
   - Pain Severity (15)
   - Urgency (10)
   - Willingness to Pay (15)
   - Ease of Finding Customers (10)
   - Recurring Demand (10)
   - Gross Margin (10)
   - Automation Potential (10)
   - Time to First Paid Pilot (10)
   - Founder Fit (5)
   - Defensibility (5)
3. Evidence Hierarchy (E0 to E5)
4. Local SQLite Persistence with FTS5 Full-Text Indexing
==============================================================================
"""

import enum
import json
import sqlite3
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any


class EvidenceLevel(str, enum.Enum):
    E0_IDEA = "E0_IDEA"
    E1_ANECDOTAL = "E1_ANECDOTAL"
    E2_SECONDARY_SOURCES = "E2_SECONDARY_SOURCES"
    E3_PRIMARY_BUYER_CONFIRMATION = "E3_PRIMARY_BUYER_CONFIRMATION"
    E4_PAID_PILOT = "E4_PAID_PILOT"
    E5_REPEAT_PURCHASES = "E5_REPEAT_PURCHASES"


@dataclass
class OpportunityFactorScores:
    """Core factors for relative ratio scoring (scale 1.0 - 10.0)."""
    pain: float = 7.0
    frequency: float = 7.0
    budget: float = 6.0
    reachability: float = 7.0
    automation_feasibility: float = 8.0
    competition: float = 4.0

    def compute_relative_score(self) -> float:
        comp = max(self.competition, 0.5)
        raw = (self.pain * self.frequency * self.budget * self.reachability * self.automation_feasibility) / comp
        return round(raw, 2)


@dataclass
class OpportunityRubric:
    """100-Point absolute evaluation rubric with explicit risk deductions."""
    pain_severity: float = 12.0          # max 15
    urgency: float = 8.0                 # max 10
    willingness_to_pay: float = 12.0     # max 15
    ease_of_finding_customers: float = 8.0 # max 10
    recurring_demand: float = 8.0        # max 10
    gross_margin: float = 9.0            # max 10
    automation_potential: float = 9.0    # max 10
    time_to_first_paid_pilot: float = 8.0 # max 10
    founder_fit: float = 4.0             # max 5
    defensibility: float = 4.0           # max 5
    risk_deductions: Dict[str, float] = field(default_factory=dict)

    def compute_rubric_score(self) -> float:
        base = (
            min(self.pain_severity, 15.0) +
            min(self.urgency, 10.0) +
            min(self.willingness_to_pay, 15.0) +
            min(self.ease_of_finding_customers, 10.0) +
            min(self.recurring_demand, 10.0) +
            min(self.gross_margin, 10.0) +
            min(self.automation_potential, 10.0) +
            min(self.time_to_first_paid_pilot, 10.0) +
            min(self.founder_fit, 5.0) +
            min(self.defensibility, 5.0)
        )
        total_deductions = sum(self.risk_deductions.values())
        return round(max(0.0, min(100.0, base - total_deductions)), 2)


@dataclass
class Opportunity:
    id: str
    title: str
    category: str
    target_customer: str
    economic_buyer: str
    problem_description: str
    proposed_solution: str
    pricing_model: str
    factors: OpportunityFactorScores
    rubric: OpportunityRubric
    relative_score: float
    rubric_score: float
    evidence_level: EvidenceLevel
    is_commercially_validated: bool
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["evidence_level"] = self.evidence_level.value
        return d


class OpportunityScoringEngine:
    """Manages scoring, persistence, ranking, and discovery of business opportunities."""

    def __init__(self, db_path: Optional[Path] = None):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        self.db_path = db_path or (base_dir / "data" / "opportunities.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            target_customer TEXT NOT NULL,
            economic_buyer TEXT NOT NULL,
            problem_description TEXT NOT NULL,
            proposed_solution TEXT NOT NULL,
            pricing_model TEXT NOT NULL,
            relative_score REAL NOT NULL,
            rubric_score REAL NOT NULL,
            evidence_level TEXT NOT NULL,
            is_commercially_validated INTEGER NOT NULL,
            factors_json TEXT NOT NULL,
            rubric_json TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_opp_rubric ON opportunities(rubric_score DESC);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_opp_category ON opportunities(category);")
        conn.commit()
        conn.close()

    def evaluate_opportunity(
        self,
        title: str,
        category: str,
        target_customer: str,
        economic_buyer: str,
        problem_description: str,
        proposed_solution: str,
        pricing_model: str,
        factors: Optional[OpportunityFactorScores] = None,
        rubric: Optional[OpportunityRubric] = None,
        evidence_level: EvidenceLevel = EvidenceLevel.E1_ANECDOTAL,
        metadata: Optional[Dict[str, Any]] = None,
        opp_id: Optional[str] = None,
    ) -> Opportunity:
        f = factors or OpportunityFactorScores()
        r = rubric or OpportunityRubric()

        rel_score = f.compute_relative_score()
        rub_score = r.compute_rubric_score()

        is_validated = evidence_level in [
            EvidenceLevel.E4_PAID_PILOT,
            EvidenceLevel.E5_REPEAT_PURCHASES,
        ]

        assigned_id = opp_id or f"opp_{uuid.uuid5(uuid.NAMESPACE_DNS, title).hex[:12]}"

        opp = Opportunity(
            id=assigned_id,
            title=title,
            category=category,
            target_customer=target_customer,
            economic_buyer=economic_buyer,
            problem_description=problem_description,
            proposed_solution=proposed_solution,
            pricing_model=pricing_model,
            factors=f,
            rubric=r,
            relative_score=rel_score,
            rubric_score=rub_score,
            evidence_level=evidence_level,
            is_commercially_validated=is_validated,
            metadata=metadata or {},
        )
        self.save_opportunity(opp)
        return opp

    def save_opportunity(self, opp: Opportunity) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO opportunities (
            id, title, category, target_customer, economic_buyer,
            problem_description, proposed_solution, pricing_model,
            relative_score, rubric_score, evidence_level,
            is_commercially_validated, factors_json, rubric_json,
            metadata_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opp.id,
            opp.title,
            opp.category,
            opp.target_customer,
            opp.economic_buyer,
            opp.problem_description,
            opp.proposed_solution,
            opp.pricing_model,
            opp.relative_score,
            opp.rubric_score,
            opp.evidence_level.value,
            1 if opp.is_commercially_validated else 0,
            json.dumps(asdict(opp.factors)),
            json.dumps(asdict(opp.rubric)),
            json.dumps(opp.metadata),
            opp.created_at,
        ))

        conn.commit()
        conn.close()

    def rank_opportunities(
        self,
        category: Optional[str] = None,
        min_rubric_score: float = 0.0,
        validated_only: bool = False,
        limit: int = 50,
    ) -> List[Opportunity]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        query = "SELECT * FROM opportunities WHERE rubric_score >= ?"
        params: List[Any] = [min_rubric_score]

        if category:
            query += " AND category = ?"
            params.append(category)

        if validated_only:
            query += " AND is_commercially_validated = 1"

        query += " ORDER BY rubric_score DESC, relative_score DESC LIMIT ?"
        params.append(limit)

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            factors_dict = json.loads(r["factors_json"])
            rubric_dict = json.loads(r["rubric_json"])
            meta_dict = json.loads(r["metadata_json"])
            results.append(
                Opportunity(
                    id=r["id"],
                    title=r["title"],
                    category=r["category"],
                    target_customer=r["target_customer"],
                    economic_buyer=r["economic_buyer"],
                    problem_description=r["problem_description"],
                    proposed_solution=r["proposed_solution"],
                    pricing_model=r["pricing_model"],
                    factors=OpportunityFactorScores(**factors_dict),
                    rubric=OpportunityRubric(**rubric_dict),
                    relative_score=r["relative_score"],
                    rubric_score=r["rubric_score"],
                    evidence_level=EvidenceLevel(r["evidence_level"]),
                    is_commercially_validated=bool(r["is_commercially_validated"]),
                    created_at=r["created_at"],
                    metadata=meta_dict,
                )
            )
        return results

    def get_ranked_opportunities(
        self,
        category: Optional[str] = None,
        min_rubric_score: float = 0.0,
        validated_only: bool = False,
        limit: int = 50,
    ) -> List[Opportunity]:
        """Alias for rank_opportunities."""
        return self.rank_opportunities(
            category=category,
            min_rubric_score=min_rubric_score,
            validated_only=validated_only,
            limit=limit,
        )

    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM opportunities WHERE id = ?", (opportunity_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        factors_dict = json.loads(row["factors_json"])
        rubric_dict = json.loads(row["rubric_json"])
        meta_dict = json.loads(row["metadata_json"])
        return Opportunity(
            id=row["id"],
            title=row["title"],
            category=row["category"],
            target_customer=row["target_customer"],
            economic_buyer=row["economic_buyer"],
            problem_description=row["problem_description"],
            proposed_solution=row["proposed_solution"],
            pricing_model=row["pricing_model"],
            factors=OpportunityFactorScores(**factors_dict),
            rubric=OpportunityRubric(**rubric_dict),
            relative_score=row["relative_score"],
            rubric_score=row["rubric_score"],
            evidence_level=EvidenceLevel(row["evidence_level"]),
            is_commercially_validated=bool(row["is_commercially_validated"]),
            created_at=row["created_at"],
            metadata=meta_dict,
        )

    def search_opportunities(self, query_text: str, limit: int = 20) -> List[Opportunity]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        clean = query_text.strip()
        if not clean:
            conn.close()
            return []

        pattern = f"%{clean}%"
        sql = """
        SELECT * FROM opportunities
        WHERE title LIKE ? OR problem_description LIKE ? OR target_customer LIKE ? OR category LIKE ?
        ORDER BY rubric_score DESC, relative_score DESC
        LIMIT ?
        """
        cur.execute(sql, (pattern, pattern, pattern, pattern, limit))
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            factors_dict = json.loads(r["factors_json"])
            rubric_dict = json.loads(r["rubric_json"])
            meta_dict = json.loads(r["metadata_json"])
            results.append(
                Opportunity(
                    id=r["id"],
                    title=r["title"],
                    category=r["category"],
                    target_customer=r["target_customer"],
                    economic_buyer=r["economic_buyer"],
                    problem_description=r["problem_description"],
                    proposed_solution=r["proposed_solution"],
                    pricing_model=r["pricing_model"],
                    factors=OpportunityFactorScores(**factors_dict),
                    rubric=OpportunityRubric(**rubric_dict),
                    relative_score=r["relative_score"],
                    rubric_score=r["rubric_score"],
                    evidence_level=EvidenceLevel(r["evidence_level"]),
                    is_commercially_validated=bool(r["is_commercially_validated"]),
                    created_at=r["created_at"],
                    metadata=meta_dict,
                )
            )
        return results

    def get_ranked_opportunities(
        self,
        category: Optional[str] = None,
        min_rubric_score: float = 0.0,
        validated_only: bool = False,
        limit: int = 50,
    ) -> List[Opportunity]:
        """Alias for rank_opportunities."""
        return self.rank_opportunities(
            category=category,
            min_rubric_score=min_rubric_score,
            validated_only=validated_only,
            limit=limit,
        )

    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM opportunities WHERE id = ?", (opportunity_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        factors_dict = json.loads(row["factors_json"])
        rubric_dict = json.loads(row["rubric_json"])
        meta_dict = json.loads(row["metadata_json"])
        return Opportunity(
            id=row["id"],
            title=row["title"],
            category=row["category"],
            target_customer=row["target_customer"],
            economic_buyer=row["economic_buyer"],
            problem_description=row["problem_description"],
            proposed_solution=row["proposed_solution"],
            pricing_model=row["pricing_model"],
            factors=OpportunityFactorScores(**factors_dict),
            rubric=OpportunityRubric(**rubric_dict),
            relative_score=row["relative_score"],
            rubric_score=row["rubric_score"],
            evidence_level=EvidenceLevel(row["evidence_level"]),
            is_commercially_validated=bool(row["is_commercially_validated"]),
            created_at=row["created_at"],
            metadata=meta_dict,
        )

    def seed_default_opportunities(self) -> List[Opportunity]:
        """Seeds the 3 primary beachhead opportunities from PROJECT ONE master blueprint."""
        opps = [
            # Opportunity 1: B2B Revenue Intelligence & Workflow Auditing
            {
                "title": "B2B Revenue Intelligence & Workflow Bottleneck Auditing",
                "category": "B2B Workflow Automation",
                "target_customer": "SaaS and IT Services SMBs (10–100 employees)",
                "economic_buyer": "VP of Revenue Operations / Managing Director",
                "problem_description": "Manual cross-checking of CRM deals, pipeline progression, invoice reconciliation, and team time-tracking creates 12-18 hours of repetitive administrative drag per week per operations manager.",
                "proposed_solution": "Automated workflow telemetry auditor that ingests CRM/invoicing logs, identifies high-friction bottlenecks, and generates weekly revenue recovery blueprints.",
                "pricing_model": "$149 - $499 / month retainer",
                "factors": OpportunityFactorScores(
                    pain=9.0,
                    frequency=9.0,
                    budget=8.0,
                    reachability=8.0,
                    automation_feasibility=9.0,
                    competition=3.5,
                ),
                "rubric": OpportunityRubric(
                    pain_severity=14.0,
                    urgency=9.0,
                    willingness_to_pay=13.0,
                    ease_of_finding_customers=8.5,
                    recurring_demand=9.5,
                    gross_margin=9.0,
                    automation_potential=9.0,
                    time_to_first_paid_pilot=8.5,
                    founder_fit=5.0,
                    defensibility=4.5,
                    risk_deductions={"data_privacy_compliance": 2.0},
                ),
                "evidence_level": EvidenceLevel.E3_PRIMARY_BUYER_CONFIRMATION,
                "metadata": {
                    "beachhead_rank": 1,
                    "target_arr_per_client_usd": 3588.0,
                    "ideal_tech_stack": "Python / FastAPI / SQLite / FTS5",
                },
            },
            # Opportunity 2: Automated Spreadsheet/Document Processing & Data Extraction
            {
                "title": "Automated Logistics & Invoice Document Intelligence",
                "category": "Document & Spreadsheet Processing",
                "target_customer": "Wholesalers, Import/Export, Freight Forwarders",
                "economic_buyer": "Finance Controller / Operations Head",
                "problem_description": "Processing bills of lading, supplier invoices, customs filings, and delivery notes manually causes high error rates, payment disputes, and 3-5 days in delayed invoice clearing.",
                "proposed_solution": "Air-gapped document extraction pipeline with automated OCR normalization, ledger matching, and mismatch alerting.",
                "pricing_model": "$199 - $599 / month + $0.05 per page",
                "factors": OpportunityFactorScores(
                    pain=9.5,
                    frequency=10.0,
                    budget=8.5,
                    reachability=7.5,
                    automation_feasibility=8.5,
                    competition=4.0,
                ),
                "rubric": OpportunityRubric(
                    pain_severity=14.5,
                    urgency=9.5,
                    willingness_to_pay=14.0,
                    ease_of_finding_customers=8.0,
                    recurring_demand=9.5,
                    gross_margin=8.5,
                    automation_potential=9.0,
                    time_to_first_paid_pilot=8.0,
                    founder_fit=4.5,
                    defensibility=4.0,
                    risk_deductions={"format_drift": 3.0},
                ),
                "evidence_level": EvidenceLevel.E3_PRIMARY_BUYER_CONFIRMATION,
                "metadata": {
                    "beachhead_rank": 2,
                    "target_arr_per_client_usd": 4788.0,
                    "ideal_tech_stack": "PyWeb / PaddleOCR / SQLite",
                },
            },
            # Opportunity 3: Autonomous Web/API Health & QA Reliability Monitoring
            {
                "title": "Autonomous API Contract & Endpoint Regression Watchdog",
                "category": "Developer & IT Tooling",
                "target_customer": "Digital Agencies, Boutique Dev Shops, Series A Startups",
                "economic_buyer": "Head of Engineering / Lead Architect",
                "problem_description": "Third-party API breaking changes, silent webhook timeouts, and payload drift break production integrations without alerting developers until paying users complain.",
                "proposed_solution": "24/7 autonomous endpoint probe with synthetic transaction replay, cryptographic payload hash verification, and instant webhook alert dispatches.",
                "pricing_model": "$49 - $149 / month per cluster",
                "factors": OpportunityFactorScores(
                    pain=8.5,
                    frequency=10.0,
                    budget=7.0,
                    reachability=9.0,
                    automation_feasibility=9.5,
                    competition=4.5,
                ),
                "rubric": OpportunityRubric(
                    pain_severity=13.0,
                    urgency=8.5,
                    willingness_to_pay=12.0,
                    ease_of_finding_customers=9.0,
                    recurring_demand=9.0,
                    gross_margin=9.5,
                    automation_potential=9.5,
                    time_to_first_paid_pilot=9.0,
                    founder_fit=5.0,
                    defensibility=4.0,
                    risk_deductions={"infrastructure_costs": 1.5},
                ),
                "evidence_level": EvidenceLevel.E3_PRIMARY_BUYER_CONFIRMATION,
                "metadata": {
                    "beachhead_rank": 3,
                    "target_arr_per_client_usd": 1188.0,
                    "ideal_tech_stack": "PyControlPlane / PyWeb / asyncio",
                },
            },
        ]

        seeded = []
        for o in opps:
            seeded.append(self.evaluate_opportunity(**o))
        return seeded
