# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""1-Click Template Automation Store & Viral Growth Flywheel Engine.

Provides a catalog of 10+ pre-seeded flagship AI automations for solo founders,
developers, and enterprise teams, complete with 1-click installation and viral embed badges.
"""

from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AutomationTemplate(BaseModel):
    """An executable 1-click automation blueprint."""
    id: str
    name: str
    category: str  # finance, sales, engineering, operations, agency
    description: str
    target_audience: str
    install_count: int = 0
    estimated_monthly_roi_usd: float
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    viral_badge_html: str = ""
    one_click_install_url: str = ""
    created_at: float = Field(default_factory=time.time)


class TemplateStoreEngine:
    """Manages the catalog of 1-click templates and provisions them to active tenants."""

    def __init__(self):
        self._templates: Dict[str, AutomationTemplate] = {}
        self._tenant_installations: Dict[str, List[str]] = {}  # tenant_id -> list of template_ids
        self._seed_flagship_catalog()

    def _seed_flagship_catalog(self) -> None:
        """Seeds the 10 core flagship 1-click automations."""
        catalog = [
            AutomationTemplate(
                id="tpl_invoice_ocr",
                name="Auto-Extract Invoices & Receipt OCR to Double-Entry Ledger",
                category="finance",
                description="Ingests vendor PDFs, extracts line items via OCR, matches POs, and posts balanced credits/debits directly to ledger.",
                target_audience="Founders, Finance Teams, Accountants",
                install_count=482,
                estimated_monthly_roi_usd=1200.0,
                workflow_config={
                    "trigger": "webhook:invoice_received",
                    "actions": ["ocr_extract", "validate_tax_id", "reconcile_ledger"],
                    "retry_policy": {"max_retries": 3, "backoff": "exponential"}
                }
            ),
            AutomationTemplate(
                id="tpl_whatsapp_sales",
                name="24/7 Autonomous WhatsApp Sales & Customer Support Agent",
                category="sales",
                description="Conversational AI agent that qualifies inbound WhatsApp leads, delivers product catalogs, and collects instant payments.",
                target_audience="E-Commerce, SMBs, Direct-to-Consumer Brands",
                install_count=934,
                estimated_monthly_roi_usd=3500.0,
                workflow_config={
                    "trigger": "whatsapp:message_inbound",
                    "actions": ["intent_classification", "catalog_lookup", "upi_payment_link"],
                    "channels": ["WHATSAPP", "SMS"]
                }
            ),
            AutomationTemplate(
                id="tpl_competitor_radar",
                name="Daily Competitor Intelligence & Real-Time Ranking Drop Alert",
                category="operations",
                description="Monitors competitor pricing, product updates, and search rankings. Alerts executive Slack/Discord on shifts.",
                target_audience="Product Managers, Growth Marketers, CMOs",
                install_count=319,
                estimated_monthly_roi_usd=1800.0,
                workflow_config={
                    "trigger": "cron:daily_0600_utc",
                    "actions": ["scrape_competitor_pricing", "compare_features", "dispatch_alert"]
                }
            ),
            AutomationTemplate(
                id="tpl_github_pr_auditor",
                name="Autonomous GitHub PR Code Reviewer & OWASP Vulnerability Scanner",
                category="engineering",
                description="Reviews every pull request for architecture drift, leaked secrets, SQL injection, and zero-placeholder violations.",
                target_audience="Engineering Leads, DevOps, Open-Source Maintainers",
                install_count=712,
                estimated_monthly_roi_usd=2400.0,
                workflow_config={
                    "trigger": "github:pull_request_opened",
                    "actions": ["ast_lint", "secret_scan", "post_pr_review_comment"]
                }
            ),
            AutomationTemplate(
                id="tpl_instant_upi_web3",
                name="Multi-Rail Instant UPI QR & Solana/Base Crypto Escrow Collector",
                category="finance",
                description="Universal instant checkout engine generating dynamic UPI QR codes in India and smart escrow vaults on Solana and Base.",
                target_audience="SaaS Startups, Global Agencies, Freelancers",
                install_count=640,
                estimated_monthly_roi_usd=4000.0,
                workflow_config={
                    "rails": ["UPI_INTENT_2_0", "SOLANA_USDC", "BASE_USDC"],
                    "actions": ["generate_qr", "listen_webhook", "settle_double_entry"]
                }
            ),
            AutomationTemplate(
                id="tpl_bangalore_gcc_switch",
                name="Bangalore GCC ISO 20022 Enterprise Banking Interconnect",
                category="finance",
                description="Interbank settlement engine executing pain.001 and pacs.008 corporate XML wire transfers with RBI statutory filings.",
                target_audience="Fortune 500 GCCs, Corporate Treasuries",
                install_count=128,
                estimated_monthly_roi_usd=8500.0,
                workflow_config={
                    "standard": "ISO_20022",
                    "actions": ["parse_pain_001", "hitl_multisig_eval", "dispatch_pacs_008"]
                }
            ),
            AutomationTemplate(
                id="tpl_churn_preventer",
                name="SaaS Churn Watch, Failed Payment Recovery & Save Offer Sequence",
                category="sales",
                description="Detects subscription usage decline, automated dunning email sequences, and presents custom exit save offers.",
                target_audience="SaaS Founders, Subscription Businesses",
                install_count=521,
                estimated_monthly_roi_usd=2900.0,
                workflow_config={
                    "trigger": "billing:invoice_payment_failed",
                    "actions": ["smart_retry", "dunning_email", "save_offer_modal"]
                }
            ),
            AutomationTemplate(
                id="tpl_pseo_magnet_gen",
                name="Programmatic SEO Competitor Comparison Landing Hub Manufacturer",
                category="agency",
                description="Generates 50+ high-intent '[Competitor] Alternative' landing pages with Schema.org JSON-LD and booking CTAs.",
                target_audience="Growth Agencies, SEO Specialists, B2B SaaS",
                install_count=815,
                estimated_monthly_roi_usd=4500.0,
                workflow_config={
                    "trigger": "manual_or_api",
                    "actions": ["generate_markdown", "render_html", "build_sitemap_xml"]
                }
            ),
            AutomationTemplate(
                id="tpl_aether_disaster_risk",
                name="Geospatial Climate Hazard & Critical Infrastructure Resilience Scorer",
                category="operations",
                description="Evaluates real-time geospatial hazard vectors (flood, seismic, storm surge) across global enterprise facilities.",
                target_audience="Enterprise Risk Officers, Data Centers, Insurers",
                install_count=94,
                estimated_monthly_roi_usd=12000.0,
                workflow_config={
                    "grid": "WGS84",
                    "hazards": ["FLOOD", "SEISMIC", "STORM_SURGE"],
                    "actions": ["evaluate_spatial_risk", "route_relief_corridors"]
                }
            ),
            AutomationTemplate(
                id="tpl_client_growth_kit",
                name="Hyper-Local SMB Client Acquisition & 10-Day Omnichannel Kit Factory",
                category="agency",
                description="Scans local commercial clusters, produces bespoke promotional proposals, and exports 1-click WhatsApp outreach links.",
                target_audience="Solo Consultants, Micro-Agencies",
                install_count=1104,
                estimated_monthly_roi_usd=3200.0,
                workflow_config={
                    "trigger": "agency:cluster_scan",
                    "actions": ["audit_tech_presence", "formulate_kit", "export_bundle"]
                }
            ),
        ]

        for t in catalog:
            t.viral_badge_html = self.generate_viral_badge(t.id)
            t.one_click_install_url = f"/api/v1/saas/templates/{t.id}/install"
            self._templates[t.id] = t

    def list_templates(self, category: Optional[str] = None) -> List[AutomationTemplate]:
        """List templates optionally filtered by category."""
        templates = list(self._templates.values())
        if category:
            cat_lower = category.lower()
            templates = [t for t in templates if t.category.lower() == cat_lower]
        return templates

    def get_template(self, template_id: str) -> Optional[AutomationTemplate]:
        """Fetch a specific template by ID."""
        return self._templates.get(template_id)

    def install_template(self, template_id: str, tenant_id: str) -> Dict[str, Any]:
        """Install an automation template into a tenant's workspace."""
        template = self._templates.get(template_id)
        if not template:
            raise KeyError(f"Template {template_id} not found in catalog.")

        template.install_count += 1

        if tenant_id not in self._tenant_installations:
            self._tenant_installations[tenant_id] = []
        if template_id not in self._tenant_installations[tenant_id]:
            self._tenant_installations[tenant_id].append(template_id)

        installation_id = f"inst_{uuid.uuid4().hex[:10]}"

        return {
            "success": True,
            "installation_id": installation_id,
            "tenant_id": tenant_id,
            "template": template.model_dump(),
            "installed_at": time.time(),
            "status": "PROVISIONED_AND_ACTIVE",
        }

    def generate_viral_badge(self, template_id: str, brand_name: str = "CASHFLOW INFINITY: OMNIVERSE") -> str:
        """Generate embeddable viral HTML badge carrying one-click clone capability."""
        return (
            f'<div class="omni-viral-badge" style="display:inline-flex;align-items:center;gap:8px;'
            f'background:#0a101f;border:1px solid #06b6d4;border-radius:9999px;padding:6px 14px;'
            f'font-family:sans-serif;font-size:12px;color:#f3f4f6;">'
            f'<span style="color:#10b981;font-weight:bold;">⚡ Powered by {brand_name}</span>'
            f'<span style="color:#64748b;">|</span>'
            f'<a href="/saas/templates/{template_id}?ref=viral_badge" style="color:#38bdf8;text-decoration:none;font-weight:600;">'
            f'Clone this in 1 Click →</a>'
            f'</div>'
        )
