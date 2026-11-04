"""Executive Account-Based Marketing (ABM) Campaign and Brief Generator."""

from typing import Optional, List, Dict, Any
from omniverse.enterprise.models import (
    Corridor,
    GCCAccount,
    OutreachTouch,
    OutreachSequence,
    TeardownReport,
)
from omniverse.enterprise.gcc_matrix import GCCMatrix
from omniverse.enterprise.proof_engine import ProofEngine


class ABMCampaign:
    """Orchestrates 4-touch high-ticket ABM cadences and executive one-pagers for Bangalore GCCs."""

    def __init__(
        self,
        matrix: Optional[GCCMatrix] = None,
        proof_engine: Optional[ProofEngine] = None
    ):
        self.matrix = matrix or GCCMatrix()
        self.proof_engine = proof_engine or ProofEngine(self.matrix)

    def generate_cadence(
        self,
        company_name: str,
        executive_title: Optional[str] = None
    ) -> OutreachSequence:
        """Create a bespoke 4-touch outreach cadence for a Bangalore GCC leader."""
        account = self.matrix.get_account(company_name)
        if not account:
            account = GCCAccount(
                name=company_name,
                corridor=Corridor.OUTER_RING_ROAD,
                sector="Enterprise Technology",
                headcount=5000,
                tech_stack=["AWS", "Kubernetes", "Kafka", "Python"],
                target_titles=["VP of Engineering"],
                readiness_score=85
            )

        title = executive_title or (account.target_titles[0] if account.target_titles else "VP of Engineering")
        teardown = self.proof_engine.generate_teardown(account.name)

        hook = (
            f"Noticing {account.name}'s engineering scaling across Bengaluru's {account.corridor.value.replace('_', ' ')} "
            f"and the operational load on your {', '.join(account.tech_stack[:2])} platforms."
        )

        touches = [
            OutreachTouch(
                touch_number=1,
                channel="LinkedIn InMail / Executive Email",
                subject=f"{account.name} tech roadmap: Autonomous multi-agent pipeline for Bengaluru team",
                body=(
                    f"Hi {title},\n\n"
                    f"I've been following {account.name}'s engineering expansion at {account.location_details}. "
                    f"Given your architecture running on {', '.join(account.tech_stack[:3])}, your senior platform leads are likely "
                    f"absorbing significant toil on {teardown.target_workflow}.\n\n"
                    f"We recently designed an autonomous multi-agent swarm that eliminates manual triage by running self-verifying "
                    f"worker agents directly in-cluster. We put together a short architectural teardown tailored specifically to {account.name}.\n\n"
                    f"Open to reviewing a 3-minute video breakdown of how this deploys inside your VPC?\n\n"
                    f"Best regards,\nManaging Partner, CASHFLOW INFINITY Enterprise"
                ),
                delay_days=0
            ),
            OutreachTouch(
                touch_number=2,
                channel="Private Loom Video & Architecture Drop",
                subject=f"Private architectural teardown & workflow diagram: {account.name}",
                body=(
                    f"Hi {title},\n\n"
                    f"Sharing the private 3-minute video breakdown and architectural sequence diagram we modeled for {account.name}:\n\n"
                    f"🔗 [Private Architecture Teardown & Demo Video: 3 Min]\n\n"
                    f"Key Takeaways for your {account.corridor.value.replace('_', ' ')} leadership team:\n"
                    f"• Target Workflow: {teardown.target_workflow}\n"
                    f"• Quantified Annual ROI: ₹{teardown.quantified_annual_roi_inr/10000000:.2f} Crores ($"
                    f"{teardown.quantified_annual_roi_inr/83000000:.2f}M USD) in engineering bandwidth recaptured\n"
                    f"• Zero code refactoring: Operates as an event-driven sidecar in your existing {account.tech_stack[0]} setup.\n\n"
                    f"Would love to know if this maps to your current Q1/Q2 platform engineering OKRs."
                ),
                delay_days=3
            ),
            OutreachTouch(
                touch_number=3,
                channel="Enterprise VPC & Security De-Risk Brief",
                subject=f"Security Architecture: Zero-egress private VPC deployment for {account.name}",
                body=(
                    f"Hi {title},\n\n"
                    f"When speaking with GCC tech heads in Bengaluru, the first hurdle is always security and data sovereignty. "
                    f"To make evaluation effortless for your CISO and InfoSec audit committees:\n\n"
                    f"1. 100% Private VPC / Air-Gapped Deployment: No customer telemetry or tokens ever leave your cloud perimeter.\n"
                    f"2. Customer-Managed Keys (CMEK): All agent memory and audit trails are encrypted with your hardware security keys.\n"
                    f"3. Full Compliance: Built to satisfy RBI localization guidelines, DPDP 2023, and SOC2 Type II controls.\n\n"
                    f"We bundle our complete InfoSec Architecture Pack into our pilot agreement so procurement approval takes days instead of quarters."
                ),
                delay_days=7
            ),
            OutreachTouch(
                touch_number=4,
                channel="Executive Briefing / Bengaluru Meeting Invite",
                subject=f"Coffee in Bengaluru / 20-min architectural briefing next week?",
                body=(
                    f"Hi {title},\n\n"
                    f"I will be near {account.location_details} next Thursday meeting with GCC technology leaders along the Outer Ring Road.\n\n"
                    f"I would be glad to host you for a 20-minute executive coffee or run a live sandbox walkthrough for your principal architects. "
                    f"We structure this as a low-friction 6-week scoped pilot with full technical SLAs.\n\n"
                    f"Do you have 20 minutes next Tuesday or Thursday?\n\n"
                    f"Best regards,\nCASHFLOW INFINITY Enterprise Practice"
                ),
                delay_days=12
            )
        ]

        return OutreachSequence(
            company=account.name,
            executive_title=title,
            touches=touches,
            personalized_hook=hook
        )

    def generate_one_pager(self, company_name: str) -> str:
        """Emits an institutional-grade 1-page executive brief in clean Markdown."""
        account = self.matrix.get_account(company_name)
        if not account:
            account = GCCAccount(
                name=company_name,
                corridor=Corridor.OUTER_RING_ROAD,
                sector="Enterprise Technology",
                headcount=5000,
                tech_stack=["AWS", "Kubernetes", "Kafka", "Python"],
                target_titles=["VP of Engineering"],
                readiness_score=85
            )

        teardown = self.proof_engine.generate_teardown(account.name)

        return f"""# Executive Brief: Autonomous Multi-Agent Process Engine
### Tailored Architectural Dossier for {account.name} | Bengaluru Tech Corridor

---

## 1. Enterprise Profile
- **Organization**: {account.name}
- **Bengaluru Footprint**: {account.headcount:,} Engineers & Technology Specialists
- **Corridor**: {account.corridor.value.replace('_', ' ')} ({account.location_details})
- **Primary Technology Stack**: {', '.join(account.tech_stack)}
- **Automation Readiness Index**: {account.readiness_score}/100

## 2. The Operational Problem
- **Bottleneck**: {teardown.target_workflow}
- **Current Enterprise Cost Baseline**: ~₹{teardown.baseline_cost_inr/10000000:.2f} Crores/Year in manual engineering triage
- **Quantified Annual ROI**: **₹{teardown.quantified_annual_roi_inr/10000000:.2f} Crores** ($ {teardown.quantified_annual_roi_inr/83000000:.2f}M USD)

## 3. Autonomous Solution Architecture
{teardown.agent_architecture_summary}

### Workflow Sequence
{teardown.architecture_diagram}

## 4. Enterprise Security & Sovereignty Guarantees
- **Zero Data Egress**: Private VPC deployment inside AWS ap-south-1 (Mumbai) / Azure India Central.
- **Data Sovereignty**: Complete compliance with India DPDP Act 2023 & RBI circular on data localization.
- **Access Control**: Strict RBAC, immutable tamper-evident audit logs, and human-in-the-loop escalation queues.

## 5. Commercial Engagement Model: 6-Week Scoped Pilot
- **Scope**: Single critical workflow automated in private sandbox.
- **Target SLA**: Minimum 70% latency reduction verified under enterprise load.
- **Pilot Investment**: ₹35,00,000 INR (Fixed price, milestone-gated).
- **Conversion Trigger**: Unlocks 12-month Enterprise Master Services Agreement & VPC Retainer.

---
*Confidential Document | Prepared by CASHFLOW INFINITY Enterprise Practice*
"""
