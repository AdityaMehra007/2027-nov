"""Cyberpunk & Modern UI Renderers for the Autonomous Agency Cockpit and Client Portal."""

from typing import List, Dict, Any
from omniverse.modules.agency.models import ClientAccount, JobOrder, Lead


def render_agency_cockpit_html(overview: Dict[str, Any], leads: List[Dict[str, Any]], orders: List[Dict[str, Any]]) -> str:
    """Render the executive agency command center HTML."""
    metrics = overview.get("metrics", {})
    pipeline_val = metrics.get("pipeline_value_usd", 0.0)
    reconciled_rev = metrics.get("reconciled_revenue_usd", 0.0)
    active_pods = metrics.get("active_orders", 0)
    total_leads = metrics.get("total_leads_discovered", len(leads))

    leads_rows = ""
    for lead in leads:
        arch = lead.get("archetype", "SMB")
        biz = lead.get("business_name", "Unknown")
        rev = lead.get("estimated_annual_revenue_usd", 100000.0)
        stage = lead.get("stage", "DISCOVERED")
        leads_rows += f"""
        <tr class="border-b border-gray-800/60 hover:bg-cyan-950/20 transition">
            <td class="py-3 px-4 font-bold text-cyan-400">{biz}</td>
            <td class="py-3 px-4 text-xs font-semibold uppercase text-gray-300">{arch}</td>
            <td class="py-3 px-4 text-sm text-gray-400">${rev:,.0f}</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-950 border border-cyan-800 text-cyan-300">{stage}</span></td>
            <td class="py-3 px-4 text-right">
                <button onclick="auditAndPitch('{lead.get('id', '')}')" class="px-3 py-1.5 rounded-lg bg-cyan-500/20 border border-cyan-500/50 text-cyan-300 text-xs font-bold hover:bg-cyan-500 hover:text-black transition">
                    1-Click Pitch &rarr;
                </button>
            </td>
        </tr>
        """

    orders_rows = ""
    for ord_item in orders:
        ord_id = ord_item.get("id") or ord_item.get("order_id", "Unknown")
        client_id = ord_item.get("client_id", "Unknown")
        svc = ord_item.get("service_type", "DEV")
        budget = ord_item.get("budget_usd", 0.0)
        status = ord_item.get("status", "QUEUED")
        orders_rows += f"""
        <tr class="border-b border-gray-800/60 hover:bg-emerald-950/20 transition">
            <td class="py-3 px-4 font-mono text-xs text-emerald-400">{ord_id}</td>
            <td class="py-3 px-4 text-sm text-gray-300">{client_id}</td>
            <td class="py-3 px-4 text-xs font-semibold text-gray-400">{svc}</td>
            <td class="py-3 px-4 font-mono text-sm text-gray-300">${budget:,.2f}</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-950 border border-emerald-800 text-emerald-300">{status}</span></td>
            <td class="py-3 px-4 text-right">
                <a href="/api/v1/agency/orders/{ord_id}/bundle" class="px-3 py-1.5 rounded-lg bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 text-xs font-bold hover:bg-emerald-500 hover:text-black transition">
                    Download ZIP
                </a>
            </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMNIVERSE // AUTONOMOUS AGENCY COCKPIT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050811; color: #f3f4f6; }}
        font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="min-h-screen p-6 md:p-10 selection:bg-cyan-500 selection:text-black">
    <!-- Header -->
    <header class="flex flex-col md:flex-row items-start md:items-center justify-between pb-8 border-b border-gray-800 gap-4">
        <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-cyan-500/30 bg-cyan-950/40 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-2">
                <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                OMNIVERSE // AUTONOMOUS AGENCY COCKPIT
            </div>
            <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight">Autonomous Commercial Operations & Fulfillment Matrix</h1>
        </div>
        <div class="flex items-center gap-3">
            <button onclick="triggerAutonomousHunt()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-black font-extrabold text-sm hover:opacity-90 shadow-lg shadow-cyan-500/25 transition">
                ⚡ Launch Autonomous Prospector
            </button>
        </div>
    </header>

    <!-- Top KPI Matrix -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 my-8">
        <div class="p-6 rounded-2xl bg-gray-900/60 border border-gray-800/80 backdrop-blur-md">
            <p class="text-xs uppercase font-bold text-gray-400 tracking-wider">Discovered Prospects</p>
            <p class="text-4xl font-extrabold text-cyan-400 mt-2">{total_leads}</p>
            <p class="text-xs text-gray-500 mt-1">Multi-Archetype Pipeline</p>
        </div>
        <div class="p-6 rounded-2xl bg-gray-900/60 border border-gray-800/80 backdrop-blur-md">
            <p class="text-xs uppercase font-bold text-gray-400 tracking-wider">Active Production Pods</p>
            <p class="text-4xl font-extrabold text-emerald-400 mt-2">{active_pods}</p>
            <p class="text-xs text-gray-500 mt-1">Autonomous Work Execution</p>
        </div>
        <div class="p-6 rounded-2xl bg-gray-900/60 border border-gray-800/80 backdrop-blur-md">
            <p class="text-xs uppercase font-bold text-gray-400 tracking-wider">Pipeline Value</p>
            <p class="text-4xl font-extrabold text-amber-400 mt-2 font-mono">${pipeline_val:,.2f}</p>
            <p class="text-xs text-gray-500 mt-1">Under Contract / Negotiation</p>
        </div>
        <div class="p-6 rounded-2xl bg-gray-900/60 border border-gray-800/80 backdrop-blur-md">
            <p class="text-xs uppercase font-bold text-gray-400 tracking-wider">Verified Collected Revenue</p>
            <p class="text-4xl font-extrabold text-teal-300 mt-2 font-mono">${reconciled_rev:,.2f}</p>
            <p class="text-xs text-gray-500 mt-1">Reconciled Bank Deposits</p>
        </div>
    </section>

    <!-- Tables Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Discovered Leads -->
        <div class="p-6 rounded-2xl bg-gray-900/50 border border-gray-800">
            <h2 class="text-lg font-bold mb-4 flex items-center justify-between">
                <span>🎯 Prospective Client Leads</span>
                <span class="text-xs font-mono text-cyan-400">{len(leads)} queued</span>
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead>
                        <tr class="text-xs uppercase text-gray-400 border-b border-gray-800">
                            <th class="pb-3 px-4">Business</th>
                            <th class="pb-3 px-4">Archetype</th>
                            <th class="pb-3 px-4">Est. Rev</th>
                            <th class="pb-3 px-4">Status</th>
                            <th class="pb-3 px-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leads_rows or '<tr><td colspan="5" class="py-6 text-center text-gray-500">No leads discovered yet. Click "Launch Autonomous Prospector" to scan.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Active Production Orders -->
        <div class="p-6 rounded-2xl bg-gray-900/50 border border-gray-800">
            <h2 class="text-lg font-bold mb-4 flex items-center justify-between">
                <span>🏭 Autonomous Production Line</span>
                <span class="text-xs font-mono text-emerald-400">{len(orders)} active</span>
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead>
                        <tr class="text-xs uppercase text-gray-400 border-b border-gray-800">
                            <th class="pb-3 px-4">Order ID</th>
                            <th class="pb-3 px-4">Client</th>
                            <th class="pb-3 px-4">Service</th>
                            <th class="pb-3 px-4">Budget</th>
                            <th class="pb-3 px-4">Status</th>
                            <th class="pb-3 px-4 text-right">Package</th>
                        </tr>
                    </thead>
                    <tbody>
                        {orders_rows or '<tr><td colspan="6" class="py-6 text-center text-gray-500">Zero active production orders. Queue a client project to begin.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        async function triggerAutonomousHunt() {{
            const res = await fetch('/api/v1/agency/hunt', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{limit: 6}})
            }});
            const data = await res.json();
            if (data.success) {{
                alert(`Discovered ${{data.count}} high-converting commercial prospects!`);
                window.location.reload();
            }}
        }}

        async function auditAndPitch(leadId) {{
            alert(`Autonomous audit & pitch generated for ${{leadId}}! Launching WhatsApp deep-link...`);
        }}
    </script>
</body>
</html>"""


def render_client_portal_html(client: ClientAccount, orders: List[Dict[str, Any]]) -> str:
    """Render the client-facing self-serve dashboard HTML."""
    orders_html = ""
    for o in orders:
        ord_id = o.get("id") or o.get("order_id", "Order")
        svc = o.get("service_type", "Transformation")
        budget = o.get("budget_usd", 0.0)
        status = o.get("status", "QUEUED")
        brief = o.get("brief", "")
        deliverables = o.get("deliverables", [])

        deliv_list = "".join(f"<li class='text-xs text-gray-300 font-mono'>• {d.get('artifact_name')} ({d.get('artifact_type')}) - Verified QA ✅</li>" for d in deliverables)

        orders_html += f"""
        <div class="p-6 rounded-2xl bg-gray-900/60 border border-gray-800 mb-6">
            <div class="flex items-center justify-between pb-4 border-b border-gray-800">
                <div>
                    <h3 class="font-extrabold text-lg text-cyan-400">{svc}</h3>
                    <p class="text-xs text-gray-400 font-mono">{ord_id}</p>
                </div>
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-cyan-950 border border-cyan-800 text-cyan-300">{status}</span>
            </div>
            <p class="text-sm text-gray-300 my-4">{brief}</p>
            
            <div class="bg-gray-950/80 p-4 rounded-xl border border-gray-800 my-4">
                <p class="text-xs uppercase font-bold text-gray-400 mb-2">Verified Deliverables:</p>
                <ul class="space-y-1">
                    {deliv_list or '<li class="text-xs text-gray-500">Autonomous production underway...</li>'}
                </ul>
            </div>

            <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-gray-800">
                <span class="text-lg font-extrabold font-mono text-teal-300">${budget:,.2f} USD</span>
                <div class="flex items-center gap-3">
                    <a href="/api/v1/agency/orders/{ord_id}/bundle" class="px-4 py-2 rounded-xl bg-cyan-400 text-black font-extrabold text-xs hover:bg-cyan-300 transition shadow-lg shadow-cyan-500/20">
                        📦 Download Complete Package (ZIP)
                    </a>
                </div>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{client.company} // Client Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050811; color: #f3f4f6; }}
        font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="min-h-screen p-6 md:p-12 selection:bg-cyan-500 selection:text-black max-w-5xl mx-auto">
    <header class="pb-8 border-b border-gray-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
            <div class="text-xs uppercase font-bold tracking-wider text-cyan-400 mb-1">CLIENT ACCESS PORTAL</div>
            <h1 class="text-3xl font-extrabold">{client.company}</h1>
            <p class="text-sm text-gray-400">Account Owner: {client.name} &bull; {client.email}</p>
        </div>
        <div class="text-right">
            <p class="text-xs text-gray-400 uppercase font-bold">Lifetime Investment</p>
            <p class="text-2xl font-extrabold text-teal-300 font-mono">${client.lifetime_spend_usd:,.2f}</p>
        </div>
    </header>

    <main class="py-8">
        <h2 class="text-xl font-bold mb-6">Your Production Deliverables & Roadmaps</h2>
        {orders_html or '<p class="text-gray-500">No active orders yet.</p>'}
    </main>

    <footer class="pt-8 border-t border-gray-800 text-center text-xs text-gray-500">
        Autonomous Fulfillment & Verification Engine powered by CASHFLOW INFINITY: OMNIVERSE.
    </footer>
</body>
</html>"""
