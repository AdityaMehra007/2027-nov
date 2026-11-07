"""Public-Facing Multi-Tenant Customer & Client Self-Service Portal."""

from typing import Dict, Any, Optional


def render_public_customer_portal_html(stats: Optional[Dict[str, Any]] = None) -> str:
    """Render the public-facing customer portal HTML."""
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
                    <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest">Self-Service Autonomous Enterprise Portal</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-950/60 border border-emerald-500/40 text-emerald-300">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>
                    GATEWAYS LIVE // 24/7 RECONCILIATION
                </span>
                <a href="#packages" class="px-4 py-2 rounded-lg bg-cyan-500 text-black font-extrabold text-xs uppercase tracking-wider hover:bg-cyan-400 transition">
                    View Solutions
                </a>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <main class="max-w-7xl mx-auto px-6 py-12">
        <div class="text-center max-w-3xl mx-auto mb-16">
            <div class="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-950/80 border border-cyan-800/80 text-cyan-300 mb-4">
                ENTERPRISE COMMERCIAL ENGINE 2027
            </div>
            <h2 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-6">
                Turnkey Software, AI Agency & <span class="text-cyan-400">Autonomous Cashflow</span>
            </h2>
            <p class="text-gray-400 text-lg leading-relaxed">
                Instant technical diagnostics, zero-egress VPC compliance, and micro-SaaS deployments. Enter your company details below for an instant mathematical growth audit.
            </p>
        </div>

        <!-- Live Platform Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div class="p-6 rounded-2xl bg-gray-900/40 border border-gray-800/80">
                <div class="text-xs uppercase font-mono font-bold text-gray-400">Active Monitored Businesses</div>
                <div class="text-4xl font-mono font-extrabold text-cyan-400 mt-2">{total_leads}</div>
                <div class="text-xs text-gray-500 mt-1">Across Bangalore Commercial Hubs</div>
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

        <!-- Interactive Growth Kit Generator Form -->
        <section class="max-w-2xl mx-auto p-8 rounded-2xl bg-gray-900/60 border border-cyan-800/40 glow-cyan mb-20">
            <h3 class="text-xl font-bold text-white mb-2 flex items-center">
                <span class="mr-2">⚡</span> Instant AI Growth & Technical Audit
            </h3>
            <p class="text-xs text-gray-400 mb-6">Enter your business information to generate your tailored 15-point growth dossier.</p>

            <form id="auditForm" onsubmit="generateInstantAudit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Business Name</label>
                    <input type="text" id="bizName" required placeholder="e.g. Acme Tech Solutions" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Industry / Niche</label>
                        <select id="bizNiche" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                            <option value="Specialty Cafe">Specialty Cafe / F&B</option>
                            <option value="Gym & Fitness">Gym & Fitness</option>
                            <option value="SaaS & Cloud">SaaS & Cloud</option>
                            <option value="Commercial Leasing">Commercial Leasing</option>
                            <option value="Healthcare Clinic">Healthcare Clinic</option>
                            <option value="Enterprise IT">Enterprise IT</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs uppercase font-mono font-bold text-gray-400 mb-1">Location</label>
                        <input type="text" id="bizCity" value="Bengaluru" class="w-full px-4 py-2.5 rounded-lg bg-gray-950 border border-gray-800 text-white text-sm focus:border-cyan-500 focus:outline-none">
                    </div>
                </div>
                <button type="submit" id="auditBtn" class="w-full py-3 rounded-lg bg-gradient-to-r from-cyan-500 to-emerald-500 text-black font-extrabold text-sm uppercase tracking-wider hover:opacity-90 transition">
                    Generate Diagnostic Dossier &rarr;
                </button>
            </form>

            <div id="auditResult" class="hidden mt-6 p-4 rounded-xl bg-gray-950/80 border border-cyan-800/60 font-mono text-xs text-gray-300"></div>
        </section>

        <!-- Service Tier Packages -->
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
        async function generateInstantAudit(e) {{
            e.preventDefault();
            const btn = document.getElementById('auditBtn');
            const resultBox = document.getElementById('auditResult');
            btn.innerText = "Analyzing System Topology...";
            btn.disabled = true;

            try {{
                const res = await fetch('/api/v1/revenue/growth-kit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        business_name: document.getElementById('bizName').value,
                        niche: document.getElementById('bizNiche').value,
                        city: document.getElementById('bizCity').value
                    }})
                }});
                const data = await res.json();
                resultBox.classList.remove('hidden');
                resultBox.innerHTML = `
                    <div class="font-bold text-cyan-400 mb-2">✅ Diagnostic Report Compiled: ${{data.business_name}}</div>
                    <div class="text-gray-400">Category: ${{data.niche}} | Cluster: ${{data.city}}</div>
                    <div class="text-amber-400 mt-2">Recommended Action: ${{data.recommended_offer}}</div>
                    <div class="text-emerald-400 mt-1">Est. Conversion Uplift: +${{data.estimated_roi_pct || 35}}%</div>
                    <div class="mt-4 pt-2 border-t border-gray-800 text-[11px] text-gray-500">Full diagnostic package queued for immediate fulfillment.</div>
                `;
            }} catch (err) {{
                alert("Failed to compile diagnostic audit: " + err);
            }} finally {{
                btn.innerText = "Generate Diagnostic Dossier →";
                btn.disabled = false;
            }}
        }}

        async function purchasePackage(amount, pkgName) {{
            const name = prompt("Enter your company name to generate invoice:", "Acme Global");
            if (!name) return;

            try {{
                // Create lead first
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

                // Create invoice
                const invRes = await fetch('/api/v1/revenue/invoices', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        lead_id: lead.id,
                        amount_inr: amount
                    }})
                }});
                const invoice = await invRes.json();

                alert(`✅ Invoice #${{invoice.id}} Created!\\nAmount: ₹${{amount.toLocaleString()}}\\nStatus: ${{invoice.status}}\\nUUID: ${{invoice.uuid}}\\n\\nTo settle instantly, send webhook payload or pay via UPI/Stripe.`);
            }} catch (err) {{
                alert("Failed to initiate checkout: " + err);
            }}
        }}
    </script>
</body>
</html>"""
    return html
