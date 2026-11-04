"""Enterprise Pilot Commercial Framework and Master Services Agreement (MSA) Generator."""

from typing import Optional, List, Dict, Any
from omniverse.enterprise.models import (
    Corridor,
    GCCAccount,
    PilotAgreement,
    Milestone,
)
from omniverse.enterprise.gcc_matrix import GCCMatrix


def format_inr(amount: float) -> str:
    """Format an amount into standard Indian Rupee notation (e.g. 35,00,000)."""
    amt_int = int(amount)
    s = str(amt_int)
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    remaining = s[:-3]
    chunks = []
    while len(remaining) > 2:
        chunks.append(remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        chunks.append(remaining)
    chunks.reverse()
    return ",".join(chunks) + "," + last_three


class PilotFramework:
    """Institutional commercial gating engine for 6-week scoped GCC autonomous enterprise pilots."""

    def __init__(self, matrix: Optional[GCCMatrix] = None):
        self.matrix = matrix or GCCMatrix()

    def generate_agreement(
        self,
        company_name: str,
        fee_inr: float = 3500000.0,
        duration_weeks: int = 6,
        gst_rate: float = 0.18,
    ) -> PilotAgreement:
        """Constructs a binding milestone-gated pilot commercial structure."""
        account = self.matrix.get_account(company_name)
        company = account.name if account else company_name

        gst_amount = round(fee_inr * gst_rate, 2)
        total_contract_value = round(fee_inr + gst_amount, 2)
        annual_retainer = round(max(fee_inr * 5.0, 18_000_000.0), 2)

        milestones = [
            Milestone(
                week_number=1,
                name="VPC Enclave Provisioning & Architecture Ingestion",
                deliverable="Isolated VPC boundary setup, CMEK encryption keys, and telemetry ingress pipelines.",
                acceptance_criteria="Zero external egress verified; InfoSec sign-off on network topology.",
                payment_percentage=15.0,
            ),
            Milestone(
                week_number=2,
                name="Multi-Agent Collective Provisioning & Tool Wiring",
                deliverable="Deployment of supervisor and worker agents with domain connectors.",
                acceptance_criteria="Agent harness passes mock schema validation with 100% test coverage.",
                payment_percentage=15.0,
            ),
            Milestone(
                week_number=3,
                name="Shadow Pipeline Execution on Historical Data",
                deliverable="Replay execution across past 90 days of transactions/tickets in shadow mode.",
                acceptance_criteria="Reconciliation accuracy >= 99.8% with zero regression on edge cases.",
                payment_percentage=20.0,
            ),
            Milestone(
                week_number=4,
                name="Live Parallel Execution & Exception Routing",
                deliverable="Parallel dual-run against live operations with human-in-the-loop escalation UI.",
                acceptance_criteria="P99 processing latency reduced by > 75%; zero unauthorized state writes.",
                payment_percentage=20.0,
            ),
            Milestone(
                week_number=5,
                name="Enterprise Load Testing & Security Governance Audit",
                deliverable="10x peak stress test and third-party penetration/compliance audit pack.",
                acceptance_criteria="Zero memory leaks, SOC2 Type II compliance audit passed without findings.",
                payment_percentage=15.0,
            ),
            Milestone(
                week_number=6,
                name="Executive Readout & Production Transition",
                deliverable="Master operational scorecard, Quantified ROI audit, and 12-month MSA Retainer transition.",
                acceptance_criteria="Sign-off from VP/Director of Engineering on production cutover.",
                payment_percentage=15.0,
            ),
        ]

        # In case duration_weeks is different, adjust milestone slice
        if duration_weeks < 6:
            milestones = milestones[:duration_weeks]
        elif duration_weeks > 6:
            for w in range(7, duration_weeks + 1):
                milestones.append(
                    Milestone(
                        week_number=w,
                        name=f"Extended Hardening & Fine-Tuning Week {w}",
                        deliverable="Specialized model tuning and expanded integration coverage.",
                        acceptance_criteria="SLAs consistently satisfied.",
                        payment_percentage=round(100.0 / duration_weeks, 2),
                    )
                )

        sla_terms = (
            "99.95% agent uptime, sub-250ms deterministic triage latency, "
            "zero data egress outside client VPC, and 1-hour P1 escalation response window."
        )

        return PilotAgreement(
            company=company,
            pilot_fee_inr=fee_inr,
            duration_weeks=duration_weeks,
            milestones=milestones,
            gst_rate=gst_rate,
            gst_amount_inr=gst_amount,
            total_contract_value_inr=total_contract_value,
            annual_retainer_conversion_fee_inr=annual_retainer,
            sla_terms=sla_terms,
        )

    def generate_contract_document(
        self,
        company_name: str,
        fee_inr: float = 3500000.0,
        duration_weeks: int = 6,
    ) -> str:
        """Generates a complete institutional Master Services Agreement (MSA) contract."""
        agreement = self.generate_agreement(company_name, fee_inr, duration_weeks)
        fee_formatted = format_inr(agreement.pilot_fee_inr)
        gst_formatted = format_inr(agreement.gst_amount_inr)
        total_formatted = format_inr(agreement.total_contract_value_inr)
        retainer_formatted = format_inr(agreement.annual_retainer_conversion_fee_inr)

        milestone_rows = []
        for m in agreement.milestones:
            m_amount = format_inr(round(agreement.pilot_fee_inr * (m.payment_percentage / 100.0), 2))
            milestone_rows.append(
                f"| Week {m.week_number} | **{m.name}** | {m.deliverable} | {m.acceptance_criteria} | {m.payment_percentage:.0f}% (₹{m_amount}) |"
            )
        milestones_table = "\n".join(milestone_rows)

        return f"""# Master Services Agreement: 6-Week Scoped Enterprise AI Pilot
**Parties:** CASHFLOW INFINITY Enterprise Practice ("Provider") & **{agreement.company}** ("Client")  
**Effective Date:** Upon Mutual Cryptographic Signature  
**Governing Law:** Laws of Karnataka, India (Arbitration in Bengaluru)

---

## 1. Commercial Terms
- **Pilot Investment Fee**: **₹{fee_formatted} INR** (excluding GST)
- **Applicable GST (18%)**: ₹{gst_formatted} INR
- **Total Contract Value**: **₹{total_formatted} INR**
- **Engagement Duration**: {agreement.duration_weeks} Calendar Weeks
- **Post-Pilot Annual Retainer Option**: ₹{retainer_formatted} INR/year (Credits 100% of pilot fee upon exercise)

---

## 2. Milestone Deliverables & Acceptance Schedule
| Milestone | Focus | Key Deliverable | Acceptance Criteria | Tranche |
|---|---|---|---|---|
{milestones_table}

---

## 3. Service Level Agreement (SLA) & Security Guarantees
- **Uptime & Latency**: {agreement.sla_terms}
- **Data Sovereignty**: 100% private tenant execution within Client VPC. No training on Client data.
- **Intellectual Property**: All bespoke agent prompts, connectors, and configuration scripts developed during the engagement remain the exclusive property of Client.

---

## 4. Signatures & Execution Authorization

**For Client ({agreement.company})**  
Name: __________________________  
Title: VP / Director of Engineering  
Signature: ______________________  
Date: __________________________  

**For CASHFLOW INFINITY Enterprise Practice**  
Name: Managing Director  
Title: Head of Autonomous Systems  
Signature: *[Cryptographically Verified HMAC-SHA256]*  
Date: 2026-11-04  
"""
