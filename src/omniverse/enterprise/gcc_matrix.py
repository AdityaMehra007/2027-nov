"""Bengaluru Global Capability Center (GCC) intelligence matrix and ranking database."""

from __future__ import annotations

from typing import List, Optional
from omniverse.enterprise.models import Corridor, GCCAccount


class GCCMatrix:
    """Institutional directory of Fortune 500 GCCs operating in Bengaluru corridors."""

    ACCOUNTS: List[GCCAccount] = [
        # Outer Ring Road (Bellandur / Kadubeesanahalli / Marathahalli)
        GCCAccount(
            name="Wells Fargo India",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="BFSI",
            headcount=24000,
            tech_stack=["Java", "Python", "GCP", "Kubernetes", "Kafka"],
            target_titles=["Managing Director, Technology", "VP of Engineering", "Head of Risk & Compliance"],
            readiness_score=88,
            annual_revenue_budget_usd=120_000_000.0,
            key_challenges=["Regulatory reporting compliance latency", "Loan underwriting document processing bottlenecks"],
            location_details="Embassy TechVillage, Outer Ring Road, Bellandur, Bengaluru",
        ),
        GCCAccount(
            name="JPMorgan Chase India",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="BFSI",
            headcount=38000,
            tech_stack=["Python", "C++", "AWS", "Athena", "OpenShift"],
            target_titles=["Head of Digital Assets & Clearing", "Chief Data Officer", "Head of Global Equities Tech"],
            readiness_score=92,
            annual_revenue_budget_usd=180_000_000.0,
            key_challenges=["Cross-border multi-currency settlement clearing speed", "Trade anomaly surveillance false-positives"],
            location_details="Prestige Tech Park, Outer Ring Road, Kadubeesanahalli, Bengaluru",
        ),
        GCCAccount(
            name="Goldman Sachs Services",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="BFSI",
            headcount=9000,
            tech_stack=["SecDb", "Python", "Java", "Slang", "AWS"],
            target_titles=["Partner, Global Engineering", "Head of Asset Management Engineering"],
            readiness_score=95,
            annual_revenue_budget_usd=90_000_000.0,
            key_challenges=["Derivatives portfolio Greeks computation scaling", "Risk margin aggregation at market close"],
            location_details="Helios Business Park, Outer Ring Road, Kadubeesanahalli, Bengaluru",
        ),
        GCCAccount(
            name="Walmart Global Tech India",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="Retail & Supply Chain",
            headcount=12000,
            tech_stack=["Node.js", "Java", "GCP", "Cassandra", "Kafka"],
            target_titles=["VP of Supply Chain Technology", "Director of Merchant Experience"],
            readiness_score=89,
            annual_revenue_budget_usd=110_000_000.0,
            key_challenges=["Warehouse route dispatch under climate hazard disruptions", "Inventory SKU demand forecasting"],
            location_details="Salarpuria Aura, Outer Ring Road, Bellandur, Bengaluru",
        ),
        GCCAccount(
            name="Cisco Systems India",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="Networking & Cloud",
            headcount=14000,
            tech_stack=["Golang", "Python", "Kubernetes", "C", "Docker"],
            target_titles=["VP of Cloud Security", "Director of Edge Network Architecture"],
            readiness_score=86,
            annual_revenue_budget_usd=85_000_000.0,
            key_challenges=["Edge node consensus telemetry monitoring", "Zero-day vulnerability packet inspection"],
            location_details="Cessna Business Park, Outer Ring Road, Kadubeesanahalli, Bengaluru",
        ),
        GCCAccount(
            name="Morgan Stanley Advantage",
            corridor=Corridor.OUTER_RING_ROAD,
            sector="BFSI",
            headcount=8000,
            tech_stack=["Java", "Python", "Angular", "Linux", "Sybase"],
            target_titles=["Executive Director, Institutional Securities Tech", "Head of Enterprise Infrastructure"],
            readiness_score=84,
            annual_revenue_budget_usd=60_000_000.0,
            key_challenges=["Regulatory liquidity stress testing execution cycles", "Post-trade allocation reconciliation"],
            location_details="Prestige Tech Park, Outer Ring Road, Bengaluru",
        ),

        # Manyata Tech Park (Hebbal / Nagavara)
        GCCAccount(
            name="Target in India",
            corridor=Corridor.MANYATA,
            sector="Retail",
            headcount=4500,
            tech_stack=["Java", "Kotlin", "Spinnaker", "GCP"],
            target_titles=["Director of Supply Chain Technology", "Principal Architect"],
            readiness_score=87,
            annual_revenue_budget_usd=40_000_000.0,
            location_details="Manyata Embassy Business Park, Hebbal, Bengaluru",
        ),
        GCCAccount(
            name="Fidelity Investments",
            corridor=Corridor.MANYATA,
            sector="BFSI",
            headcount=11000,
            tech_stack=["Java", "AWS", "Python", "PostgreSQL"],
            target_titles=["Head of Asset Management Technology", "VP of Cloud Engineering"],
            readiness_score=90,
            annual_revenue_budget_usd=75_000_000.0,
            location_details="Manyata Tech Park, Nagavara, Bengaluru",
        ),

        # Whitefield
        GCCAccount(
            name="SAP Labs India",
            corridor=Corridor.WHITEFIELD,
            sector="Enterprise Software",
            headcount=15000,
            tech_stack=["ABAP", "Java", "HANA", "Kubernetes"],
            target_titles=["Managing Director", "Head of Cloud Platform Engineering"],
            readiness_score=91,
            annual_revenue_budget_usd=130_000_000.0,
            location_details="EPIP Zone, Whitefield, Bengaluru",
        ),

        # Electronic City
        GCCAccount(
            name="Bosch Global Software Technologies",
            corridor=Corridor.ELECTRONIC_CITY,
            sector="Automotive & IoT",
            headcount=30000,
            tech_stack=["C/C++", "AUTOSAR", "Python", "AWS IoT"],
            target_titles=["VP of Connected Mobility", "Head of Edge AI Engineering"],
            readiness_score=83,
            annual_revenue_budget_usd=95_000_000.0,
            location_details="Electronic City Phase 1, Bengaluru",
        ),
    ]

    def list_accounts(
        self,
        corridor: Optional[Corridor] = None,
        min_score: Optional[int] = None,
    ) -> List[GCCAccount]:
        """Filters GCC accounts by corridor and minimum AI readiness score."""
        results = self.ACCOUNTS
        if corridor is not None:
            results = [a for a in results if a.corridor == corridor]
        if min_score is not None:
            results = [a for a in results if a.readiness_score >= min_score]
        return results

    def get_account(self, name: str) -> Optional[GCCAccount]:
        """Finds a GCC account by full or partial name."""
        name_lower = name.lower()
        for a in self.ACCOUNTS:
            if name_lower in a.name.lower():
                return a
        return None
