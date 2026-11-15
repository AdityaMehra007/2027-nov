#!/usr/bin/env python3
"""
B2B REVENUE ENGINE & COMMERCIAL CPQ CALCULATOR — ADITYA MEHRA (@AdityaMehra007)
Provides deterministic ROI modeling, dynamic CPQ pricing tiers, and automated SOW generation.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import math
import sys
from typing import Dict, List, Any, Optional

@dataclass
class ROIResult:
    monthly_revenue_lakhs: float
    lockup_days: int
    hub_nodes: int
    working_capital_unlocked_inr: int
    annual_opex_savings_inr: int
    estimated_payback_days: int
    net_12mo_roi_multiple: float
    verification_hash: str

VERTICAL_SPECS = {
    "TREASURY": {
        "name": "Cashflow Infinity — Autonomous CFO Treasury & ACID Ledger OS",
        "deliverables": [
            "1. Cryptographic SHA-256 Double-Entry Ledger & Automated 3-Way Invoice Reconciler",
            "2. 2,000-Path Monte Carlo Cash Runway (P10/P50/P90) & 95% Value-at-Risk Dashboard",
            "3. Working Capital CCC (DIO+DSO-DPO) Alerting & Early AR Factoring Proration Engine"
        ],
        "default_roi_note": "15–28% Working Capital Unlocked via CCC Compression"
    },
    "SCM": {
        "name": "Nexus-SCM — Multi-Node Dark Store & Supply Chain Digital Twin",
        "deliverables": [
            "1. Multi-Node Hub Telemetry Matrix with EOQ & Safety Stock Reorder Automation",
            "2. Cross-Docking Workflow State Machine targeting -42.0% Dock Cycle-Time Reduction",
            "3. Automated Vendor OTIF SLA Scoring & >99.0% AI Quality Assurance Inspection Gate"
        ],
        "default_roi_note": "-30% Dead Stock / -42% Dock Turnaround"
    },
    "GYMVERSE": {
        "name": "GymVerse-OS — Smart Facility Telemetry & Gemini AI Retention Platform",
        "deliverables": [
            "1. Native Kotlin 2.0 / Jetpack Compose & Web Member Portal with Live Crowd Queue Telemetry",
            "2. Equipment Utilization, Preventive Maintenance & Zero-Downtime Asset Registry",
            "3. Google Gemini AI Personalized Coaching & Member Churn Early-Warning Scorer"
        ],
        "default_roi_note": "+22% Member Retention & Lifetime Value"
    },
    "EVENTOS": {
        "name": "Eventos-Omega & Autonomous 18-Agent B2B Revenue Engine",
        "deliverables": [
            "1. High-Density Event Stall Build & Vendor SLA Command Center (0.00% Downtime Spec)",
            "2. 18-Agent B2B Lead Scoring, Enrichment & Multi-Touch Outbound Cadence Pipeline",
            "3. FastAPI Executive Telemetry Dashboard & Real-Time Incident Escalation Router"
        ],
        "default_roi_note": "3.4x Pipeline Velocity / 0.00% Event Downtime"
    }
}

TIER_PRICING = {
    "PILOT": {
        "label": "Tier A: 14-Day Rapid Production Pilot",
        "fee_inr": 75000,
        "terms": "50% Kickoff / 50% Live Cutover",
        "sla": "14 Business Days to Production"
    },
    "ENTERPRISE": {
        "label": "Tier B: Full Enterprise Architecture Deployment",
        "fee_inr": 185000,
        "terms": "40% Kickoff / 30% Midpoint / 30% Live Cutover",
        "sla": "Full Turnkey Multi-Node Deployment"
    },
    "RETAINER": {
        "label": "Tier C: Dedicated AI-Native Systems Partner",
        "fee_inr": 65000,
        "terms": "Monthly Recurring Retainer",
        "sla": "Continuous Architecture & Optimization"
    }
}

def calculate_roi(monthly_rev_lakhs: float, lockup_days: int, hub_nodes: int) -> ROIResult:
    """Computes deterministic client ROI, working capital release, and payback period."""
    if monthly_rev_lakhs <= 0 or lockup_days <= 0 or hub_nodes <= 0:
        raise ValueError("Inputs must be strictly positive numbers.")

    daily_rev_inr = (monthly_rev_lakhs * 100000.0) / 30.0
    days_saved = round(lockup_days * 0.28)
    capital_unlocked = round(daily_rev_inr * days_saved)
    annual_opex = round((monthly_rev_lakhs * 100000.0 * 12.0) * 0.018 + (hub_nodes * 145000.0))

    investment_inr = TIER_PRICING["ENTERPRISE"]["fee_inr"]
    total_y1_benefit = (capital_unlocked * 0.35) + annual_opex
    multiple = round(max(2.5, total_y1_benefit / investment_inr), 2)
    payback_days = max(5, round((investment_inr / total_y1_benefit) * 365))

    v_str = f"{monthly_rev_lakhs}:{lockup_days}:{hub_nodes}:{capital_unlocked}:{annual_opex}"
    digest = hashlib.sha256(v_str.encode("utf-8")).hexdigest()[:16]

    return ROIResult(
        monthly_revenue_lakhs=monthly_rev_lakhs,
        lockup_days=lockup_days,
        hub_nodes=hub_nodes,
        working_capital_unlocked_inr=capital_unlocked,
        annual_opex_savings_inr=annual_opex,
        estimated_payback_days=payback_days,
        net_12mo_roi_multiple=multiple,
        verification_hash=digest
    )

def generate_sow(client_name: str, vertical_key: str, tier_key: str) -> Dict[str, Any]:
    """Generates an executive Statement of Work (SOW) proposal."""
    v_key = vertical_key.upper()
    t_key = tier_key.upper()

    if v_key not in VERTICAL_SPECS:
        raise KeyError(f"Unknown vertical '{vertical_key}'. Valid: {list(VERTICAL_SPECS.keys())}")
    if t_key not in TIER_PRICING:
        raise KeyError(f"Unknown tier '{tier_key}'. Valid: {list(TIER_PRICING.keys())}")

    vert = VERTICAL_SPECS[v_key]
    tier = TIER_PRICING[t_key]
    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    ref_id = f"SOW-AM-{today_str}-{v_key[:3]}"

    roi = calculate_roi(120.0, 65, 6)

    contract_text = f"""========================================================================
STATEMENT OF WORK (SOW) & TECHNICAL ARCHITECTURE PROPOSAL
Reference ID: {ref_id} | Architect: Aditya Mehra (@AdityaMehra007)
========================================================================
PREPARED FOR : {client_name}
SYSTEM SUITE : {vert['name']}
ENGAGEMENT   : {tier['label']} ({tier['fee_inr']:,} INR — {tier['terms']})

1. QUANTIFIED BUSINESS CASE & TARGET ROI
   • Projected Working Capital Unlocked : ₹{roi.working_capital_unlocked_inr:,}
   • Projected Annual OpEx Savings      : ₹{roi.annual_opex_savings_inr:,} / year
   • Target Architectural SLA           : >99.4% Deterministic QA | <45ms API Latency

2. SCOPE OF DELIVERABLES (14-DAY EXECUTION SPRINT)
   {chr(10).join('   ' + d for d in vert['deliverables'])}

3. MILESTONE SCHEDULE
   • Days 01–03 : Domain Audit, Data Schema Mapping & Deterministic Invariant Spec
   • Days 04–10 : Core Engine Implementation, UI Terminal & Agentic Guardrail Integration
   • Days 11–14 : End-to-End SHA-256 Audit Verification, Team Handover & Live Cutover

4. AUTHORIZATION & NEXT STEPS
   • Portfolio & Live Kernel : https://adityamehra007.github.io/cashflow-infinity-omniverse/
   • GitHub Verification     : https://github.com/AdityaMehra007
========================================================================"""

    return {
        "reference_id": ref_id,
        "client_name": client_name,
        "vertical": vert["name"],
        "tier": tier["label"],
        "investment_inr": tier["fee_inr"],
        "terms": tier["terms"],
        "sla": tier["sla"],
        "deliverables": vert["deliverables"],
        "contract_text": contract_text
    }

if __name__ == "__main__":
    roi = calculate_roi(120.0, 65, 6)
    print(f"[B2B ROI MODEL] Unlocked: ₹{roi.working_capital_unlocked_inr:,} | OpEx Saved: ₹{roi.annual_opex_savings_inr:,} | Multiple: {roi.net_12mo_roi_multiple}x")
    sow = generate_sow("Bengaluru Enterprise Retail Pvt Ltd", "SCM", "ENTERPRISE")
    print(f"[B2B SOW GENERATED] Ref: {sow['reference_id']} | Investment: ₹{sow['investment_inr']:,}")
