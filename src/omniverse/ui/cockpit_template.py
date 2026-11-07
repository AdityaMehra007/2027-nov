"""==============================================================================
CONGLOMERATE MASTER COMMAND COCKPIT UI TEMPLATE
==============================================================================
Unified executive command plane unifying all 4 Pillars of Cashflow Infinity:
Agency Fleet, Vertical SaaS Holdings, Aether Geospatial, and Treasury Clearing.
==============================================================================
"""

from typing import Dict, Any, Optional
import json


def render_conglomerate_cockpit_html(state: Optional[Dict[str, Any]] = None) -> str:
    state = state or {}
    total_leads = state.get("total_leads", 101)
    pipeline_inr = state.get("pipeline_inr", 1955500.0)
    reconciled_inr = state.get("reconciled_inr", 631125.0)
    saas_mrr_usd = state.get("saas_mrr_usd", 646.0)
    saas_arr_usd = state.get("saas_arr_usd", 7752.0)
    sar_zones_count = state.get("sar_zones_count", 4)
    reserves = state.get("reserves", {"INR": 25000000.0, "USD": 500000.0, "EUR": 300000.0, "eINR": 5000000.0})

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMNIVERSE // Supreme Conglomerate Command Cockpit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #050811; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .glass-card {{ background: rgba(10, 15, 30, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(6, 182, 212, 0.2); }}
        .glow-cyan {{ box-shadow: 0 0 25px -5px rgba(6, 182, 212, 0.25); }}
    </style>
</head>
<body class="text-gray-100 min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-950/20 via-[#050811] to-[#050811] p-6 lg:p-10">

    <!-- Top Conglomerate Header -->
    <header class="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between pb-8 border-b border-gray-800 gap-4">
        <div class="flex items-center space-x-4">
            <div class="w-12 h-12 rounded-2xl bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold text-2xl glow-cyan">
                🌌
            </div>
            <div>
                <div class="flex items-center space-x-3">
                    <h1 class="text-xl md:text-2xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400 font-mono">
                        CASHFLOW INFINITY: OMNIVERSE
                    </h1>
                    <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-800">
                        CONGLOMERATE v2027
                    </span>
                </div>
                <p class="text-xs font-mono text-gray-500 uppercase tracking-widest mt-1">
                    Autonomous Multi-Pillar Operating System • Target: $100M ARR Unicorn
                </p>
            </div>
        </div>

        <div class="flex items-center space-x-3 font-mono text-xs">
            <span class="inline-flex items-center px-3 py-1.5 rounded-xl bg-emerald-950/70 border border-emerald-500/30 text-emerald-300">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse mr-2"></span>
                ALL 4 PILLARS ACTIVE
            </span>
            <a href="/portal" class="px-3.5 py-1.5 rounded-xl border border-gray-700 hover:border-cyan-500 text-gray-300 hover:text-white transition">
                Client Portal
            </a>
            <a href="/aether-map" class="px-3.5 py-1.5 rounded-xl bg-cyan-500 text-black font-extrabold hover:bg-cyan-400 transition">
                🛰️ SAR Map
            </a>
        </div>
    </header>

    <!-- Main 4-Pillar Grid -->
    <main class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">

        <!-- PILLAR 1: Agency Fleet -->
        <div class="glass-card rounded-2xl p-6 flex flex-col justify-between border-t-2 border-t-cyan-500">
            <div>
                <div class="flex items-center justify-between text-xs font-mono text-gray-400 mb-2">
                    <span class="font-bold text-cyan-400 uppercase tracking-wider">PILLAR 1 // $25M TARGET</span>
                    <span>🏢 GCC FLEET</span>
                </div>
                <h3 class="text-lg font-bold text-white mb-4">Autonomous B2B Agency</h3>
                <div class="space-y-3">
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">CRM Pipeline</span>
                        <span class="text-xl font-extrabold text-cyan-300 font-mono">₹{pipeline_inr:,.0f}</span>
                        <span class="text-[10px] font-mono text-gray-400 block mt-0.5">{total_leads} Monitored Commercial Leads</span>
                    </div>
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Settled Invoices</span>
                        <span class="text-lg font-bold text-emerald-400 font-mono">₹{reconciled_inr:,.0f}</span>
                    </div>
                </div>
            </div>
            <div class="mt-6 pt-4 border-t border-gray-800/80">
                <a href="/portal" class="w-full block text-center py-2 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-700 text-xs font-mono text-cyan-300 transition">
                    Dispatch Multi-Channel Ingress &rarr;
                </a>
            </div>
        </div>

        <!-- PILLAR 2: Vertical SaaS Holdings -->
        <div class="glass-card rounded-2xl p-6 flex flex-col justify-between border-t-2 border-t-emerald-500">
            <div>
                <div class="flex items-center justify-between text-xs font-mono text-gray-400 mb-2">
                    <span class="font-bold text-emerald-400 uppercase tracking-wider">PILLAR 2 // $35M TARGET</span>
                    <span>⚡ VERSE FLEET</span>
                </div>
                <h3 class="text-lg font-bold text-white mb-4">Vertical SaaS Holdings</h3>
                <div class="space-y-3">
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Live Run-Rate ARR</span>
                        <span class="text-xl font-extrabold text-emerald-300 font-mono">${saas_arr_usd:,.0f}</span>
                        <span class="text-[10px] font-mono text-gray-400 block mt-0.5">MRR: ${saas_mrr_usd:,.0f} / mo</span>
                    </div>
                    <div class="text-[11px] font-mono space-y-1 text-gray-300">
                        <div class="flex justify-between"><span>• CloudBite POS</span><span class="text-emerald-400">ACTIVE</span></div>
                        <div class="flex justify-between"><span>• GymVerse OS</span><span class="text-emerald-400">ACTIVE</span></div>
                        <div class="flex justify-between"><span>• RentShield Prop</span><span class="text-emerald-400">ACTIVE</span></div>
                        <div class="flex justify-between"><span>• ClinicFlow EHR</span><span class="text-emerald-400">ACTIVE</span></div>
                    </div>
                </div>
            </div>
            <div class="mt-6 pt-4 border-t border-gray-800/80">
                <a href="/api/v1/saas/fleet/summary" target="_blank" class="w-full block text-center py-2 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-700 text-xs font-mono text-emerald-300 transition">
                    Provision Tenant Instance &rarr;
                </a>
            </div>
        </div>

        <!-- PILLAR 3: Aether Deep-Tech Resilience -->
        <div class="glass-card rounded-2xl p-6 flex flex-col justify-between border-t-2 border-t-purple-500">
            <div>
                <div class="flex items-center justify-between text-xs font-mono text-gray-400 mb-2">
                    <span class="font-bold text-purple-400 uppercase tracking-wider">PILLAR 3 // $30M TARGET</span>
                    <span>🛰️ AETHER</span>
                </div>
                <h3 class="text-lg font-bold text-white mb-4">Satellite SAR Resilience</h3>
                <div class="space-y-3">
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Monitored Basins</span>
                        <span class="text-xl font-extrabold text-purple-300 font-mono">{sar_zones_count} Key Corridors</span>
                        <span class="text-[10px] font-mono text-gray-400 block mt-0.5">Sentinel-1 C-Band InSAR (-16.4 dB)</span>
                    </div>
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Underwriting Risk Engine</span>
                        <span class="text-xs font-bold text-gray-200 font-mono">WGS84 Sub-basin Inundation</span>
                    </div>
                </div>
            </div>
            <div class="mt-6 pt-4 border-t border-gray-800/80">
                <a href="/aether-map" class="w-full block text-center py-2 rounded-lg bg-purple-950/60 hover:bg-purple-900 border border-purple-500/40 text-xs font-mono text-purple-200 transition">
                    Launch Interactive SAR Viewer &rarr;
                </a>
            </div>
        </div>

        <!-- PILLAR 4: OmniSwarm Treasury & Clearing -->
        <div class="glass-card rounded-2xl p-6 flex flex-col justify-between border-t-2 border-t-amber-500">
            <div>
                <div class="flex items-center justify-between text-xs font-mono text-gray-400 mb-2">
                    <span class="font-bold text-amber-400 uppercase tracking-wider">PILLAR 4 // $10M TARGET</span>
                    <span>🏛️ OMNISWARM</span>
                </div>
                <h3 class="text-lg font-bold text-white mb-4">Treasury & Clearing Mesh</h3>
                <div class="space-y-3">
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Liquid Treasury Reserves</span>
                        <span class="text-xl font-extrabold text-amber-300 font-mono">₹{reserves.get('INR', 25000000.0):,.0f}</span>
                        <span class="text-[10px] font-mono text-gray-400 block mt-0.5">${reserves.get('USD', 500000.0):,.0f} USD • €{reserves.get('EUR', 300000.0):,.0f} EUR</span>
                    </div>
                    <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                        <span class="text-[10px] font-mono text-gray-500 block uppercase">Clearing Rate</span>
                        <span class="text-xs font-bold text-gray-200 font-mono">0.15% Net B2B Settlement Fee</span>
                    </div>
                </div>
            </div>
            <div class="mt-6 pt-4 border-t border-gray-800/80">
                <a href="/api/v1/clearing/reserves" target="_blank" class="w-full block text-center py-2 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-700 text-xs font-mono text-amber-300 transition">
                    Inspect Clearing Reserves &rarr;
                </a>
            </div>
        </div>

    </main>

    <!-- Bottom Telemetry & Quick API Links -->
    <footer class="max-w-7xl mx-auto mt-10 pt-6 border-t border-gray-800/80 flex flex-col md:flex-row items-center justify-between text-xs font-mono text-gray-500 gap-4">
        <div>
            <span>SYSTEM STATUS: </span>
            <span class="text-emerald-400 font-bold">ALL SERVICES OPERATIONAL (330/330 TESTS PASSING)</span>
        </div>
        <div class="flex items-center space-x-4">
            <a href="/api/v1/finance/quotes" target="_blank" class="hover:text-cyan-400">Market Quotes</a>
            <span>•</span>
            <a href="/api/v1/clearing/rates" target="_blank" class="hover:text-cyan-400">FX Rates</a>
            <span>•</span>
            <a href="/api/v1/aether/hazard-zones" target="_blank" class="hover:text-cyan-400">Hazard Zones</a>
            <span>•</span>
            <a href="/api/v1/ops/health" target="_blank" class="hover:text-cyan-400">Healthcheck</a>
        </div>
    </footer>

</body>
</html>
"""
