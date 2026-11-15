"""Public-Facing Multi-Tenant Customer & Client Self-Service Portal."""

from typing import Dict, Any, Optional


def render_public_customer_portal_html(stats: Optional[Dict[str, Any]] = None) -> str:
    """Render the public-facing customer portal HTML with Beachhead Intake and Delivery Tracker."""
    stats = stats or {}
    total_leads = stats.get("total_leads", 101)
    pipeline_val = stats.get("pipeline_value_inr", 1955500.0)
    reconciled_val = stats.get("reconciled_revenue_inr", 631125.0)

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMNIVERSE // Client Portal & Autonomous Growth Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #070a12; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .cyber-border {{ border: 1px solid rgba(6, 182, 212, 0.25); }}
        .glow-cyan {{ box-shadow: 0 0 25px -5px rgba(6, 182, 212, 0.25); }}
        .glow-emerald {{ box-shadow: 0 0 25px -5px rgba(16, 185, 129, 0.25); }}
    </style>
</head>
<body class="text-gray-100 min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-950/20 via-[#070a12] to-[#070a12]">
    <!-- Header -->
    <header class="border-b border-gray-800/80 backdrop-blur-md sticky top-0 z-50 bg-[#070a12]/80">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <span class="text-2xl">🌌</span>
                <div>
                    <h1 class="text-lg font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-emerald-400">
                        CASHFLOW INFINITY: OMNIVERSE
                    </h1>
                    <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest">Autonomous Customer Intake & Operations Portal</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <a href="#audit-section" class="px-3 py-1.5 rounded-lg bg-gray-900 border border-cyan-800 text-cyan-300 font-mono text-xs hover:border-cyan-400 transition">
                    Audit Intake
                </a>
                <a href="#tracker-section" class="px-3 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-gray-300 font-mono text-xs hover:border-emerald-400 hover:text-emerald-300 transition">
                    Job Tracker
                </a>
                <a href="#packages" class="px-4 py-2 rounded-lg bg-cyan-500 text-black font-extrabold text-xs uppercase tracking-wider hover:bg-cyan-400 transition">
                    Solutions & Pricing
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-6 py-12">
        <!-- Hero Section -->
        <div class="text-center max-w-3xl mx-auto mb-16">
            <div class="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-950/80 border border-cyan-800/80 text-cyan-300 mb-4">
                AUTONOMOUS B2B REVENUE INTELLIGENCE
            </div>
            <h2 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-6">
                Turnkey Software, AI Agency & <span class="text-cyan-400">Autonomous Cashflow</span>
            </h2>
            <p class="text-gray-400 text-lg leading-relaxed">
                Self-service workflow auditing, quantified Cost of Inaction (COI) calculations, zero-egress VPC compliance, and micro-SaaS deployments.
            </p>
        </div>

        <!-- Live Platform Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div class="p-6 rounded-2xl bg-gray-900/40 border border-gray-800/80">
                <div class="text-xs uppercase font-mono font-bold text-gray-400">Active Monitored Businesses</div>
                <div class="text-4xl font-mono font-extrabold text-cyan-400 mt-2">{total_leads}</div>
                <div class="text-xs text-gray-500 mt-1">Across Global Commercial Hubs</div>
            </div>
            <div class="p-6 rounded-2xl bg-gray-900/40 border border-gray-800/80">
                <div class="text-xs uppercase font-mono font-bold text-gray-400">Total Pipeline Value</div>
                <div class="text-4xl font-mono font-extrabold text-amber-400 mt-2 font-mono">₹{pipeline_val:,.2f}</div>
                <div class="text-xs text-gray-500 mt-1">Verified Audit Assessments</div>
            </div>
            <div class="p-6 rounded-2xl bg-gray-900/40 border border-gray-800/80">
                <div class="text-xs uppercase font-mono font-bold text-gray-400">Reconciled Settled Cash</div>
                <div class="text-4xl font-mono font-extrabold text-emerald-400 mt-2 font-mono">₹{reconciled_val:,.2f}</div>
                <div class="text-xs text-gray-500 mt-1">100% Reconciled Bank Receipts</div>
            </div>
        </div>

        <!-- Section 1: Self-Service Beachhead Workflow Audit & ROI Calculator -->
        <section id="audit-section" class="max-w-4xl mx-auto p-8 rounded-2xl bg-gray-900/70 border border-cyan-800/50 glow-cyan mb-20">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h3 class="text-2xl font-extrabold text-white flex items-center">
                        <span class="mr-2">⚡</span> Beachhead Workflow Audit: Operational Bottleneck & Quantified ROI Engine
                    </h3>
                    <p class="text-xs text-gray-400 mt-1">
                        Instant AI Growth & Diagnostic Engine. Input your operational parameters to calculate annual Cost of Inaction (COI) and generate a customized Markdown deliverable.
                    </p>
                </div>
                <span class="px-2.5 py-1 rounded bg-cyan-950 border border-cyan-700/60 text-cyan-300 font-mono text-[10px] uppercase font-bold">
                    Zero-Touch Instant Engine
                </span>
            </div>

            <form id="beachheadAuditForm" onsubmit="generateBeachheadAudit(event)" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Company / Organization Name</label>
                        <input type="text" id="auditCompany" required value="Apex Freight & Logistics" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Industry / Sector</label>
                        <select id="auditIndustry" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                            <option value="Logistics & Supply Chain">Logistics & Freight Forwarding</option>
                            <option value="B2B SaaS & IT Services">B2B SaaS & IT Services</option>
                            <option value="Fintech & WealthTech">Fintech & Payments</option>
                            <option value="Healthcare & Diagnostics">Healthcare & Clinics</option>
                            <option value="DTC Commerce & Retail">DTC Commerce & Retail</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Current Operational Workflow / Bottleneck</label>
                    <input type="text" id="auditWorkflow" required value="Manual invoice matching & freight bill reconciliation against ERP" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Monthly Volume</label>
                        <input type="number" id="auditVolume" required value="2500" min="50" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Hours / Unit</label>
                        <input type="number" step="0.05" id="auditHours" required value="0.25" min="0.01" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Hourly Wage ($)</label>
                        <input type="number" step="1" id="auditWage" required value="18" min="5" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Pilot Tier ($/mo)</label>
                        <select id="auditPilotFee" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                            <option value="49">$49 Rapid</option>
                            <option value="99" selected>$99 Production</option>
                            <option value="499">$499 Enterprise</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="generateAuditBtn" class="w-full py-3.5 rounded-lg bg-gradient-to-r from-cyan-500 to-emerald-500 text-black font-extrabold text-sm uppercase tracking-wider hover:opacity-95 transition">
                    Generate Quantified Audit & Download Report &rarr;
                </button>
            </form>

            <!-- Instant Audit Results Box -->
            <div id="beachheadResultBox" class="hidden mt-8 pt-6 border-t border-gray-800">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div class="p-4 rounded-xl bg-gray-950 border border-gray-800">
                        <div class="text-[10px] uppercase font-mono text-gray-500 font-bold">Annual Cost of Inaction (COI)</div>
                        <div id="resCoi" class="text-2xl font-extrabold font-mono text-rose-400 mt-1">$0.00</div>
                    </div>
                    <div class="p-4 rounded-xl bg-gray-950 border border-gray-800">
                        <div class="text-[10px] uppercase font-mono text-gray-500 font-bold">Projected Monthly Savings</div>
                        <div id="resSavings" class="text-2xl font-extrabold font-mono text-emerald-400 mt-1">$0.00</div>
                    </div>
                    <div class="p-4 rounded-xl bg-gray-950 border border-gray-800">
                        <div class="text-[10px] uppercase font-mono text-gray-500 font-bold">Projected ROI %</div>
                        <div id="resRoi" class="text-2xl font-extrabold font-mono text-cyan-400 mt-1">0%</div>
                    </div>
                    <div class="p-4 rounded-xl bg-gray-950 border border-gray-800">
                        <div class="text-[10px] uppercase font-mono text-gray-500 font-bold">Labor Hours Saved / Mo</div>
                        <div id="resHours" class="text-2xl font-extrabold font-mono text-amber-400 mt-1">0 hrs</div>
                    </div>
                </div>

                <div class="p-5 rounded-xl bg-gray-950/80 border border-cyan-800/60 font-mono text-xs text-gray-300">
                    <div class="flex items-center justify-between mb-3 pb-2 border-b border-gray-800">
                        <span class="font-bold text-cyan-400">📄 Executive Deliverable Summary</span>
                        <button onclick="downloadReportMarkdown()" class="px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-black font-extrabold text-[11px] uppercase tracking-wider transition">
                            Download Audit Report (.md) ⬇
                        </button>
                    </div>
                    <div id="reportSummaryText" class="whitespace-pre-wrap text-gray-300 leading-relaxed font-sans text-xs"></div>
                </div>
            </div>
        </section>

        <!-- Section 2: Job Delivery Status Tracker & Deliverables Ingress -->
        <section id="tracker-section" class="max-w-4xl mx-auto p-8 rounded-2xl bg-gray-900/60 border border-gray-800 glow-emerald mb-20">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h3 class="text-2xl font-extrabold text-white flex items-center">
                        <span class="mr-2">📦</span> Job Delivery Status Tracker
                    </h3>
                    <p class="text-xs text-gray-400 mt-1">
                        Track live progress of commissioned audits, software implementations, and download completed artifacts.
                    </p>
                </div>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-950/80 border border-emerald-500/40 text-emerald-400">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 mr-2"></span>
                    TRACKER READY
                </span>
            </div>

            <div class="flex flex-col md:flex-row gap-3 mb-8">
                <input type="text" id="trackerInput" placeholder="Enter Invoice UUID or Order ID (e.g. DEMO-PILOT-2026)" value="DEMO-PILOT-2026" class="flex-1 px-4 py-3 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm font-mono focus:border-emerald-500 focus:outline-none">
                <button onclick="checkJobTrackingStatus()" class="px-6 py-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold text-sm uppercase tracking-wider transition">
                    Query Job Status &rarr;
                </button>
            </div>

            <div id="trackerOutput" class="p-6 rounded-xl bg-gray-950 border border-gray-800 space-y-6">
                <div class="flex flex-col md:flex-row md:items-center justify-between border-b border-gray-800 pb-4">
                    <div>
                        <div class="text-xs uppercase font-mono text-gray-500">Tracking Reference</div>
                        <div id="trackRef" class="text-base font-mono font-bold text-white mt-0.5">DEMO-PILOT-2026</div>
                    </div>
                    <div class="mt-2 md:mt-0">
                        <div class="text-xs uppercase font-mono text-gray-500">Current Phase</div>
                        <div id="trackStatus" class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-emerald-950 border border-emerald-700/60 text-emerald-300">
                            COMPLETED // READY FOR DOWNLOAD
                        </div>
                    </div>
                </div>

                <!-- Multi-stage progress indicators -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
                    <div class="p-3 rounded-lg bg-gray-900 border border-emerald-500/40">
                        <div class="flex items-center text-emerald-400 font-bold text-xs">
                            <span class="mr-1.5">✓</span> Stage 1: Intake
                        </div>
                        <div class="text-[10px] text-gray-400 mt-1">Workflow mapped</div>
                    </div>
                    <div class="p-3 rounded-lg bg-gray-900 border border-emerald-500/40">
                        <div class="flex items-center text-emerald-400 font-bold text-xs">
                            <span class="mr-1.5">✓</span> Stage 2: Profiling
                        </div>
                        <div class="text-[10px] text-gray-400 mt-1">COI quantified</div>
                    </div>
                    <div class="p-3 rounded-lg bg-gray-900 border border-emerald-500/40">
                        <div class="flex items-center text-emerald-400 font-bold text-xs">
                            <span class="mr-1.5">✓</span> Stage 3: Architecture
                        </div>
                        <div class="text-[10px] text-gray-400 mt-1">Blueprint compiled</div>
                    </div>
                    <div class="p-3 rounded-lg bg-gray-900 border border-emerald-500/40">
                        <div class="flex items-center text-emerald-400 font-bold text-xs">
                            <span class="mr-1.5">✓</span> Stage 4: Delivered
                        </div>
                        <div class="text-[10px] text-gray-400 mt-1">Artifacts signed</div>
                    </div>
                </div>

                <!-- Available Deliverables -->
                <div>
                    <div class="text-xs font-mono uppercase font-bold text-gray-400 mb-3">Client Deliverable Assets</div>
                    <div class="space-y-2">
                        <div class="p-3 rounded-lg bg-gray-900/60 border border-gray-800 flex items-center justify-between">
                            <div>
                                <div class="text-xs font-bold text-white">Operational Workflow Audit & ROI Dossier (.md)</div>
                                <div class="text-[10px] text-gray-500 font-mono">audit_report_apex.md • 14.2 KB</div>
                            </div>
                            <button onclick="downloadDeliverableMock('audit_report_apex.md')" class="px-3 py-1.5 rounded bg-gray-800 hover:bg-emerald-500 hover:text-black text-xs font-mono transition">
                                Download ⬇
                            </button>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-900/60 border border-gray-800 flex items-center justify-between">
                            <div>
                                <div class="text-xs font-bold text-white">Automated Pipeline Specification & Integration Map (.json)</div>
                                <div class="text-[10px] text-gray-500 font-mono">pipeline_architecture.json • 8.5 KB</div>
                            </div>
                            <button onclick="downloadDeliverableMock('pipeline_architecture.json')" class="px-3 py-1.5 rounded bg-gray-800 hover:bg-emerald-500 hover:text-black text-xs font-mono transition">
                                Download ⬇
                            </button>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-900/60 border border-gray-800 flex items-center justify-between">
                            <div>
                                <div class="text-xs font-bold text-white">Zero-Egress Security & SLA Assurance Certificate (.md)</div>
                                <div class="text-[10px] text-gray-500 font-mono">security_sla_guarantee.md • 5.1 KB</div>
                            </div>
                            <button onclick="downloadDeliverableMock('security_sla_guarantee.md')" class="px-3 py-1.5 rounded bg-gray-800 hover:bg-emerald-500 hover:text-black text-xs font-mono transition">
                                Download ⬇
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Service Tier Packages & Instant Checkout -->
        <section id="packages" class="mb-20">
            <div class="text-center mb-12">
                <h3 class="text-3xl font-extrabold text-white">Commercial Retainers & Software Deployments</h3>
                <p class="text-gray-400 text-sm mt-2">Instant online activation via Credit Card, Stripe, or UPI AutoPay.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Package 1 -->
                <div class="p-8 rounded-2xl bg-gray-900/50 border border-gray-800 flex flex-col justify-between">
                    <div>
                        <div class="text-xs font-mono font-bold uppercase text-cyan-400 mb-2">Tier 1: Growth Kit</div>
                        <h4 class="text-2xl font-extrabold text-white">Comprehensive Audit</h4>
                        <div class="text-3xl font-mono font-extrabold text-white my-4">₹15,000 <span class="text-xs text-gray-500 font-normal">/ one-time</span></div>
                        <ul class="text-xs text-gray-400 space-y-2.5 my-6">
                            <li>✓ Full Technical & SEO Vulnerability Audit</li>
                            <li>✓ WhatsApp & UPI Gateway Configuration</li>
                            <li>✓ 15-Point Actionable Local Market Dossier</li>
                            <li>✓ Competitor Conversion Benchmark</li>
                        </ul>
                    </div>
                    <button onclick="purchasePackage(15000, 'GROWTH_KIT')" class="w-full py-2.5 rounded-lg bg-gray-800 hover:bg-cyan-500 hover:text-black font-bold text-xs uppercase transition">
                        Select Package
                    </button>
                </div>

                <!-- Package 2 (Featured) -->
                <div class="p-8 rounded-2xl bg-gray-900/80 border-2 border-cyan-500/80 relative glow-cyan flex flex-col justify-between">
                    <span class="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full text-[10px] font-mono font-extrabold bg-cyan-500 text-black uppercase tracking-wider">
                        Most Popular
                    </span>
                    <div>
                        <div class="text-xs font-mono font-bold uppercase text-cyan-400 mb-2">Tier 2: Micro-SaaS</div>
                        <h4 class="text-2xl font-extrabold text-white">Fullstack App Scaffolding</h4>
                        <div class="text-3xl font-mono font-extrabold text-white my-4">₹50,000 <span class="text-xs text-gray-500 font-normal">/ turnkey</span></div>
                        <ul class="text-xs text-gray-300 space-y-2.5 my-6">
                            <li>✓ Dedicated FastAPI & SQLite Stack</li>
                            <li>✓ Stripe & Razorpay Webhook Ingress</li>
                            <li>✓ Turnkey Dockerfile & Deployment Config</li>
                            <li>✓ 100% Automated Pytest Verification</li>
                        </ul>
                    </div>
                    <button onclick="purchasePackage(50000, 'MICRO_SAAS')" class="w-full py-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold text-xs uppercase tracking-wider transition">
                        Deploy Now &rarr;
                    </button>
                </div>

                <!-- Package 3 -->
                <div class="p-8 rounded-2xl bg-gray-900/50 border border-gray-800 flex flex-col justify-between">
                    <div>
                        <div class="text-xs font-mono font-bold uppercase text-emerald-400 mb-2">Tier 3: Enterprise GCC</div>
                        <h4 class="text-2xl font-extrabold text-white">Managed SLA Retainer</h4>
                        <div class="text-3xl font-mono font-extrabold text-white my-4">₹1,50,000 <span class="text-xs text-gray-500 font-normal">/ month</span></div>
                        <ul class="text-xs text-gray-400 space-y-2.5 my-6">
                            <li>✓ Zero-Egress VPC Security Blueprints</li>
                            <li>✓ Air-Gapped Signature Governor (HMAC)</li>
                            <li>✓ 24/7 Automated Health Watchdog</li>
                            <li>✓ 99.9% Uptime Guarantee with SLA Penalties</li>
                        </ul>
                    </div>
                    <button onclick="purchasePackage(150000, 'ENTERPRISE_RETAINER')" class="w-full py-2.5 rounded-lg bg-gray-800 hover:bg-emerald-500 hover:text-black font-bold text-xs uppercase transition">
                        Contact Sales
                    </button>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800/60 py-8 text-center text-xs text-gray-600 font-mono">
        CASHFLOW INFINITY: OMNIVERSE &copy; 2027. ALL RIGHTS RESERVED. APACHE 2.0 LICENSED.
    </footer>

    <script>
        let currentGeneratedReport = "";
        let currentCompanyName = "Company";

        async function generateBeachheadAudit(e) {{
            e.preventDefault();
            const btn = document.getElementById('generateAuditBtn');
            const resBox = document.getElementById('beachheadResultBox');
            btn.innerText = "Analyzing Bottlenecks & Synthesizing Deliverable...";
            btn.disabled = true;

            const company = document.getElementById('auditCompany').value;
            const industry = document.getElementById('auditIndustry').value;
            const workflow = document.getElementById('auditWorkflow').value;
            const volume = parseInt(document.getElementById('auditVolume').value) || 2000;
            const hours = parseFloat(document.getElementById('auditHours').value) || 0.25;
            const wage = parseFloat(document.getElementById('auditWage').value) || 18.0;
            const fee = parseFloat(document.getElementById('auditPilotFee').value) || 99.0;

            currentCompanyName = company;

            try {{
                const res = await fetch('/api/v1/opportunities/beachhead/generate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        prospect_name: company,
                        industry: industry,
                        current_workflow: workflow,
                        monthly_volume: volume,
                        human_hours_per_unit: hours,
                        hourly_wage_usd: wage,
                        proposed_monthly_fee_usd: fee
                    }})
                }});

                const data = await res.json();
                currentGeneratedReport = data.markdown_report || "";

                document.getElementById('resCoi').innerText = "$" + data.annual_cost_of_inaction_usd.toLocaleString();
                document.getElementById('resSavings').innerText = "$" + data.projected_monthly_savings_usd.toLocaleString();
                document.getElementById('resRoi').innerText = data.roi_percentage.toLocaleString() + "%";
                document.getElementById('resHours').innerText = Math.round(volume * hours * 0.70) + " hrs";

                // Format first 500 chars for preview
                document.getElementById('reportSummaryText').innerText = currentGeneratedReport.substring(0, 900) + "\\n\\n[...Full quantified implementation roadmap generated in downloadable report...]";
                resBox.classList.remove('hidden');
                resBox.scrollIntoView({{ behavior: 'smooth' }});
            }} catch (err) {{
                alert("Audit compilation error: " + err);
            }} finally {{
                btn.innerText = "Generate Quantified Audit & Download Report →";
                btn.disabled = false;
            }}
        }}

        function downloadReportMarkdown() {{
            if (!currentGeneratedReport) return;
            const blob = new Blob([currentGeneratedReport], {{ type: 'text/markdown' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `operational_audit_${{currentCompanyName.toLowerCase().replace(/[^a-z0-9]/g, '_')}}.md`;
            a.click();
            URL.revokeObjectURL(url);
        }}

        async function checkJobTrackingStatus() {{
            const ref = document.getElementById('trackerInput').value.trim();
            if (!ref) return;

            try {{
                const res = await fetch(`/api/v1/portal/tracking/${{encodeURIComponent(ref)}}`);
                const data = await res.json();
                document.getElementById('trackRef').innerText = data.tracking_id + " (" + data.client_name + ")";
                document.getElementById('trackStatus').innerText = data.status + " // " + data.current_stage;
            }} catch (err) {{
                alert("Failed to query tracking status: " + err);
            }}
        }}

        function downloadDeliverableMock(filename) {{
            const content = `# CASHFLOW INFINITY: DELIVERABLE ARTIFACT\\n\\n**File:** ${{filename}}\\n**Status:** VERIFIED & SIGNED\\n**License:** Apache 2.0\\n`;
            const blob = new Blob([content], {{ type: 'text/plain' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }}

        async function purchasePackage(amount, pkgName) {{
            const name = prompt("Enter your company name to generate invoice:", "Acme Global");
            if (!name) return;

            try {{
                const leadRes = await fetch('/api/v1/revenue/leads', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        business_name: name,
                        category: pkgName,
                        city: "Bengaluru",
                        estimated_value_inr: amount
                    }})
                }});
                const lead = await leadRes.json();

                const invRes = await fetch('/api/v1/revenue/invoices', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        lead_id: lead.id,
                        amount_inr: amount
                    }})
                }});
                const invoice = await invRes.json();

                alert(`✅ Invoice #${{invoice.id}} Created!\\nAmount: ₹${{amount.toLocaleString()}}\\nStatus: ${{invoice.status}}\\nUUID: ${{invoice.uuid}}\\n\\nTracking ID: ${{invoice.uuid}}\\nTo settle instantly, pay via UPI QR or Stripe card in test mode.`);
            }} catch (err) {{
                alert("Failed to initiate checkout: " + err);
            }}
        }}
    </script>
</body>
</html>"""
    return html
