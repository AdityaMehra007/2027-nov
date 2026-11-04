"""6-Week Scoped Enterprise Pilot Framework and Retainer Agreement Engine."""

from typing import Optional, List, Dict, Any
from omniverse.enterprise.models import (
    Milestone,
    PilotAgreement,
    GCCAccount,
    Corridor,
)
from omniverse.enterprise.gcc_matrix import GCCMatrix
from omniverse.enterprise.proof_engine import ProofEngine


class PilotFramework:
    """Structures, calculates, and generates enterprise 6-week paid pilots and annual retainer conversions."""

    def __init__(
        self,
        matrix: Optional[GCCMatrix] = None,
        proof_engine: Optional[ProofEngine] = None
    ):
        self.matrix = matrix or GCCMatrix()
        self.proof_engine = proof_engine or ProofEngine(self.matrix)

    def generate_agreement(
        self,
        company_name: str,
        fee_inr: float = 3_500_000.0,
        duration_weeks: int = 6
    ) -> PilotAgreement:
        """Create a mathematically precise, milestone-gated pilot agreement."""
        account = self.matrix.get_account(company_name)
        company = account.name if account else company_name
        teardown = self.proof_engine.generate_teardown(company)

        gst_rate = 0.18
        gst_amount = fee_inr * gst_rate
        total_contract_value = fee_inr + gst_amount

        # Retainer calculation: 4.5x - 6x pilot value or based on quantified ROI
        annual_retainer = max(15_000_000.0, min(30_000_000.0, teardown.quantified_annual_roi_inr * 0.45))

        milestones = [
            Milestone(
                week_number=1,
                name="VPC Peering & InfoSec Environment Provisioning",
                deliverable="Isolated cloud sandbox in client VPC with zero-egress IAM roles",
                acceptance_criteria="Successful network ping within VPC perimeter with CMEK keys verified",
                payment_percentage=0.15
            ),
            Milestone(
                week_number=2,
                name="Schema Ingestion & Baseline Benchmarking",
                deliverable="Telemetry schema validation adapter and current-state latency baseline report",
                acceptance_criteria="Deterministic parsing of 5,000 sample workflow events without error",
                payment_percentage=0.15
            ),
            Milestone(
                week_number=3,
                name="Autonomous Agent Swarm Orchestration",
                deliverable="Deploy Ingestion, Verification, Worker, and Audit agents in sandbox",
                acceptance_criteria="End-to-end execution of synthetic workflow tasks with self-reflection",
                payment_percentage=0.20
            ),
            Milestone(
                week_number=4,
                name="Stress Testing & Error Self-Correction",
                deliverable="Chaos test report under peak enterprise transaction load",
                acceptance_criteria="99.5% autonomous error self-correction without operator intervention",
                payment_percentage=0.20
            ),
            Milestone(
                week_number=5,
                name="Production Shadowing & Human-in-the-Loop Trial",
                deliverable="Real-time parallel execution against live production events in shadow mode",
                acceptance_criteria="Zero impact on production throughput; 100% agreement with enterprise leads",
                payment_percentage=0.15
            ),
            Milestone(
                week_number=6,
                name="Executive Readout & SLA Retainer Conversion",
                deliverable="Executive ROI signoff report demonstrating >= 70% latency reduction",
                acceptance_criteria="Formal technical signoff by VP/Director of Engineering for annual transition",
                payment_percentage=0.15
            ),
        ]

        sla_terms = (
            "1. Pilot SLA Target: >= 70% reduction in workflow latency.\n"
            "2. Zero-Downtime Guarantee: Operates strictly as a non-disruptive shadow sidecar.\n"
            "3. Data Sovereignty SLA: 100% data remains inside sovereign Indian borders.\n"
            "4. Conversion Trigger: Upon verified achievement of Week 6 acceptance criteria, "
            "Client executes the 12-Month Annual Retainer Agreement."
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
            sla_terms=sla_terms
        )

    def generate_contract_document(
        self,
        company_name: str,
        fee_inr: float = 3_500_000.0
    ) -> str:
        """Outputs a formal Master Services Agreement (MSA) and Statement of Work (SOW)."""
        agreement = self.generate_agreement(company_name, fee_inr)
        account = self.matrix.get_account(company_name)
        corridor_str = account.corridor.value.replace('_', ' ') if account else "Bengaluru"

        milestone_rows = "\n".join(
            f"| Week {m.week_number} | **{m.name}** | {m.deliverable} | {m.acceptance_criteria} | ₹{agreement.pilot_fee_inr * m.payment_percentage:,.0f} ({m.payment_percentage*100:.0f}%) |"
            for m in agreement.milestones
        )

        return f"""# Master Services Agreement: 6-Week Scoped Enterprise AI Pilot
### Statement of Work (SOW) & Commercial Terms
**Client Organization**: {agreement.company} ({corridor_str})  
**Provider**: CASHFLOW INFINITY Enterprise Practice  
**Jurisdiction**: Bengaluru, Karnataka, India  

---

## 1. Commercial Summary
- **Scoped Pilot Fee**: ₹{agreement.pilot_fee_inr:,.0f} INR (Thirty-Five Lakh Rupees)
- **Applicable GST (18%)**: ₹{agreement.gst_amount_inr:,.0f} INR (Six Lakh Thirty Thousand Rupees)
- **Total Invoiced Contract Value**: **₹{agreement.total_contract_value_inr:,.0f} INR**
- **Follow-on Annual Platform Retainer**: ₹{agreement.annual_retainer_conversion_fee_inr:,.0f} INR/Year

---

## 2. Milestone Execution Schedule & Acceptance Gate

| Milestone | Phase | Deliverable | Acceptance Criteria | Milestone Fee |
| :--- | :--- | :--- | :--- | :--- |
{milestone_rows}

---

## 3. Service Level Agreement (SLA) & Warranty
{agreement.sla_terms}

---

## 4. Annual Retainer Conversion Clause
Upon formal acceptance and delivery of the Week 6 Milestone readout demonstrating achieving target operational efficiency, Client agrees to transition the pilot deployment into the **Annual Enterprise VPC Retainer & Support Agreement** at the negotiated rate of **₹{agreement.annual_retainer_conversion_fee_inr:,.0f} INR/Year**, payable quarterly in advance.

---
**Agreed & Accepted:**

For **{agreement.company}**:  
Signature: __________________________  
Name: _______________________________  
Title: VP / Director of Engineering  
Date: _______________________________  

For **CASHFLOW INFINITY**:  
Signature: __________________________  
Name: Managing Partner, Enterprise  
Date: _______________________________  
"""
