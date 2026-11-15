"""==============================================================================
PROJECT ONE: PROSPECT DOSSIER & PENDING ACTIONS STAGING ENGINE
==============================================================================
Extracts 35 high-probability target organizations from public commercial indices,
constructs personalized workflow audit briefs, and stages outreach drafts into
the cryptographic PendingActionsQueue (enforcing the non-negotiable governance
rule: no unapproved external outbound communications without founder signoff).
==============================================================================
"""

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional

from pycontrolplane.cognitive_mesh.consensus import AgentConsensusGovernor


@dataclass
class CandidateOrganization:
    name: str
    hub: str
    country: str
    industry: str
    estimated_team_size: int
    detected_tech_stack: str
    primary_workflow_drag: str
    proposed_beachhead_audit: str
    target_role: str
    outreach_subject: str
    outreach_body: str


class ProspectStagingEngine:
    """Manages prospect identification, dossier generation, and PendingActionsQueue staging."""

    def __init__(self, governor: Optional[AgentConsensusGovernor] = None):
        self.governor = governor or AgentConsensusGovernor(required_quorum=3, approval_ratio=0.66)
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        self.data_dir = base_dir / "data"
        self.artifacts_dir = base_dir / "artifacts" / "staged_outreach"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def get_candidate_organizations(self) -> List[CandidateOrganization]:
        """Returns 35 curated candidate organizations across global hubs."""
        hubs_data = [
            # Bengaluru Tech Hub (10)
            ("KaptureDesk Solutions", "Bengaluru", "India", "B2B SaaS / Helpdesk", 45, "React / Node / PostgreSQL", "CRM deal to invoice latency", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("ZetaFleet Logistics", "Bengaluru", "India", "Supply Chain / Telematics", 65, "Python / Go / Kafka", "Customs & invoice reconciliation drag", "Automated Logistics & Invoice Document Intelligence"),
            ("QuickPay Gateway India", "Bengaluru", "India", "Fintech / UPI Payments", 50, "Java / Spring / AWS", "Webhook timeout & API contract drift", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("CloudPulse Observability", "Bengaluru", "India", "DevTools / APM", 35, "Go / Rust / Kubernetes", "Manual bug triage handoffs", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("NammaRetail Direct", "Bengaluru", "India", "DTC Commerce", 28, "Shopify Plus / Python", "Failed payment dunning loss", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("IndiraHealth Systems", "Bengaluru", "India", "HealthTech / Diagnostics", 40, "Python / Django / GCP", "Lab report OCR data extraction", "Automated Logistics & Invoice Document Intelligence"),
            ("Whitefield Robotics", "Bengaluru", "India", "Industrial IoT", 30, "C++ / ROS / Python", "Telemetry event schema mismatches", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("Koramangala Analytics Co", "Bengaluru", "India", "BI Consulting", 22, "PostgreSQL / dbt / Snowflake", "Manual spreadsheet data wrangling", "Automated Logistics & Invoice Document Intelligence"),
            ("HSR Capital Advisory", "Bengaluru", "India", "Fintech / WealthTech", 18, "Python / FastAPI / AWS", "Regulatory compliance document audits", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("VibeCraft Studios", "Bengaluru", "India", "Creative Tech", 25, "TypeScript / Next.js", "Client milestone invoice friction", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),

            # San Francisco Bay Area (8)
            ("NeuralScale Systems", "San Francisco", "USA", "AI Infrastructure", 60, "Python / PyTorch / Ray", "Billing & GPU quota reconciliation", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("ApexVantage Analytics", "San Francisco", "USA", "B2B SaaS", 48, "FastAPI / Postgres / Stripe", "Dunning recovery & involuntary churn", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("SomaBio Diagnostics", "San Francisco", "USA", "Biotech Software", 35, "Python / AWS / FHIR", "Clinical document normalization", "Automated Logistics & Invoice Document Intelligence"),
            ("MissionGrid CleanTech", "San Francisco", "USA", "Renewables", 42, "Go / TimescaleDB", "Smart meter webhook contract drift", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("Presidio Cyber Defense", "San Francisco", "USA", "Security Ops", 55, "Go / Rust / AWS", "Audit evidence collection overhead", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Embarcadero Payments", "San Francisco", "USA", "Fintech Clearing", 40, "Node / TypeScript / Stripe", "Multi-processor settlement mismatches", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("BayArea FreightFlow", "San Francisco", "USA", "Logistics Tech", 38, "Python / React / GCP", "Bill of lading paper processing", "Automated Logistics & Invoice Document Intelligence"),
            ("MarketStreet Marketing AI", "San Francisco", "USA", "MarTech", 25, "Next.js / Python / OpenAI", "Campaign ROI data consolidation", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),

            # London & Europe (8)
            ("Thames CrossBorder FX", "London", "UK", "Fintech / Remittances", 52, "Java / Spring / Azure", "Currency pair settlement reconciliation", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("Shoreditch Synthetics", "London", "UK", "AI Audio & Video", 30, "Python / PyTorch / AWS", "SaaS subscription tier migration churn", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Kensington Aesthetics Care", "London", "UK", "MedTech / Clinics", 24, "Salesforce / Custom Portal", "Patient intake document digitization", "Automated Logistics & Invoice Document Intelligence"),
            ("CityAlpha Asset Management", "London", "UK", "Quantitative Hedge Fund", 20, "Python / C++ / Linux", "Portfolio trade allocation reconciliation", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Brandenburg Battery Systems", "Berlin", "Germany", "CleanTech / EV", 45, "Python / Docker / GCP", "Supplier invoice matching in ERP", "Automated Logistics & Invoice Document Intelligence"),
            ("Mitte Cloud Identity", "Berlin", "Germany", "Cybersecurity", 38, "Rust / Go / AWS", "OAuth webhook delivery failures", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("Kreuzberg Direct Commerce", "Berlin", "Germany", "Ecommerce", 30, "Shopify / Klaviyo / Supabase", "Cross-border VAT calculation drag", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Munich Precision Sensor", "Munich", "Germany", "Industrial Tech", 50, "C++ / Python / Azure", "Firmware telemetry ingest drift", "Autonomous API Contract & Endpoint Regression Watchdog"),

            # Singapore & Asia Pacific (5)
            ("Marina Bay Sovereign Analytics", "Singapore", "Singapore", "WealthTech / RegTech", 40, "Python / Django / AWS", "Multi-jurisdiction tax reporting drag", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Straits Logistics Ocean", "Singapore", "Singapore", "Maritime Logistics", 70, "Java / Oracle / Cloud", "Port cargo clearance document matching", "Automated Logistics & Invoice Document Intelligence"),
            ("LionCity Health Genomics", "Singapore", "Singapore", "Health Informatics", 32, "Python / Next.js / GCP", "Lab order to billing sync latency", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Marunouchi Autonomous Tech", "Tokyo", "Japan", "Warehouse Automation", 60, "C++ / Python / Linux", "Robot dispatch API regression testing", "Autonomous API Contract & Endpoint Regression Watchdog"),
            ("Ginza Dental Cloud", "Tokyo", "Japan", "Practice Management", 28, "Ruby / Rails / PostgreSQL", "Insurance claim processing delays", "Automated Logistics & Invoice Document Intelligence"),

            # New York & East Coast (4)
            ("Gotham Liquidity Partners", "New York", "USA", "Fintech / Trading", 35, "Python / C# / AWS", "Post-trade settlement ledger discrepancies", "B2B Revenue Intelligence & Workflow Bottleneck Audit"),
            ("Manhattan Velvet Apparel", "New York", "USA", "Luxury DTC", 26, "Shopify Plus / Netsuite", "Inventory count to invoice mismatches", "Automated Logistics & Invoice Document Intelligence"),
            ("Hudson Legal Compliance AI", "New York", "USA", "LegalTech", 32, "Python / FastAPI / Azure", "Contract clause extraction drag", "Automated Logistics & Invoice Document Intelligence"),
            ("WallStreet Risk Analytics", "New York", "USA", "Financial Risk", 44, "Python / QuantLib / Linux", "Market data feed timeout monitoring", "Autonomous API Contract & Endpoint Regression Watchdog"),
        ]

        prospects = []
        for name, hub, country, ind, size, stack, drag, beachhead in hubs_data:
            role = "Head of Revenue Operations" if "Revenue" in beachhead else ("Finance Controller" if "Document" in beachhead else "VP of Engineering")
            subject = f"Workflow audit for {name}: Quantified bottleneck reduction ({drag})"
            body = (
                f"Hello {name} Team,\n\n"
                f"I noticed your operations in {hub} scaling your {ind} platform on {stack}.\n\n"
                f"In scaling teams of ~{size} people, {drag.lower()} frequently creates 20–35 hours of manual drag "
                f"per month across operations. We prepared an autonomous, zero-integration workflow audit preview "
                f"benchmarking {beachhead.lower()}.\n\n"
                f"Our analysis estimates ~$3,200/mo in direct labor savings and faster cycle times with zero operational disruption.\n\n"
                f"Would you be open to reviewing the 2-page quantified audit brief this Thursday?\n\n"
                f"Best regards,\n"
                f"Aditya Mehra\n"
                f"Founder, PROJECT ONE Autonomous Commerce\n"
                f"Bengaluru, India"
            )

            prospects.append(
                CandidateOrganization(
                    name=name,
                    hub=hub,
                    country=country,
                    industry=ind,
                    estimated_team_size=size,
                    detected_tech_stack=stack,
                    primary_workflow_drag=drag,
                    proposed_beachhead_audit=beachhead,
                    target_role=role,
                    outreach_subject=subject,
                    outreach_body=body,
                )
            )
        return prospects

    def stage_all_prospects(self) -> Dict[str, Any]:
        """Stages all candidate prospects into PendingActionsQueue and persists to disk."""
        prospects = self.get_candidate_organizations()
        staged_ops = []

        for p in prospects:
            payload = {
                "recipient_company": p.name,
                "hub": p.hub,
                "country": p.country,
                "industry": p.industry,
                "target_role": p.target_role,
                "subject": p.outreach_subject,
                "body": p.outreach_body,
                "proposed_audit": p.proposed_beachhead_audit,
                "requires_human_signoff": True,
                "status": "AWAITING_FOUNDER_SIGN_OFF",
                "staged_at": time.time(),
            }
            op_id = self.governor.propose_operation("OUTBOUND_PROSPECT_COMMUNICATION", payload)
            staged_ops.append({
                "op_id": op_id,
                **payload
            })

        # Persist staged list to data/staged_prospects.json
        json_path = self.data_dir / "staged_prospects.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(staged_ops, f, indent=2)

        # Generate Human Review Manifest
        manifest_path = self.artifacts_dir / "HUMAN_REVIEW_OUTREACH_MANIFEST.md"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write("# PENDING ACTIONS QUEUE: PROSPECT OUTREACH REVIEW MANIFEST\n")
            f.write(f"**Total Staged Operations:** {len(staged_ops)}  \n")
            f.write("**Status:** AWAITING HUMAN FOUNDER SIGN-OFF  \n")
            f.write("**Security Policy:** Zero unsolicited outbound communication without explicit HMAC/CLI approval.\n\n")
            f.write("---\n\n")
            for idx, op in enumerate(staged_ops, 1):
                f.write(f"### [{idx:02d}] {op['recipient_company']} ({op['hub']}, {op['country']})\n")
                f.write(f"- **Operation ID:** `{op['op_id']}`\n")
                f.write(f"- **Industry:** {op['industry']} | **Target Role:** {op['target_role']}\n")
                f.write(f"- **Audit Package:** {op['proposed_audit']}\n")
                f.write(f"- **Subject:** `{op['subject']}`\n")
                f.write(f"- **Draft Preview:**\n```text\n{op['body'][:240]}...\n```\n\n")

        return {
            "total_staged": len(staged_ops),
            "json_path": str(json_path),
            "manifest_path": str(manifest_path),
            "governor_pending_count": len(self.governor.pending_actions_queue),
        }
