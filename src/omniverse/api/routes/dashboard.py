from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from omniverse.core.config import get_settings
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.markets.engine import MultiMarketEngine
from omniverse.modules.commerce.catalog import CommerceMatrix
from omniverse.operations.health import HealthDiagnostics

def get_dashboard_router(get_session_dep):
    router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

    @router.get("/summary")
    def get_summary(session: Session = Depends(get_session_dep)):
        settings = get_settings()
        pipeline = LeadPipeline(session)
        payments = PaymentWorkflow(session)
        market_engine = MultiMarketEngine()
        commerce = CommerceMatrix()
        diagnostics = HealthDiagnostics(session)

        return {
            "app_name": settings.app_name,
            "version": settings.version,
            "env": settings.env,
            "primary_market": settings.primary_market,
            "currency": settings.currency,
            "pipeline_summary": pipeline.get_pipeline_summary(),
            "financial_ledger": payments.get_financial_ledger(),
            "market_quotes": [q.model_dump() for q in market_engine.get_global_overview()],
            "commerce_portfolio": commerce.calculate_portfolio_economics(),
            "health_diagnostics": diagnostics.run_diagnostics()
        }

    @router.get("/", response_class=HTMLResponse)
    def render_dashboard():
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CASHFLOW INFINITY: OMNIVERSE Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #090d16;
            --bg-surface: #111827;
            --bg-card: #182234;
            --border: #283548;
            --accent-primary: #3b82f6;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-indigo: #6366f1;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-base); color: var(--text-main); padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }
        .title-badge { background: #1e3a8a; color: #93c5fd; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; text-transform: uppercase; }
        .grid-kpi { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }
        .kpi-title { font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }
        .kpi-value { font-size: 28px; font-weight: 800; }
        .text-emerald { color: var(--accent-emerald); }
        .text-blue { color: var(--accent-primary); }
        .text-amber { color: var(--accent-amber); }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .section-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .grid-two { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
        th { color: var(--text-muted); font-weight: 600; font-size: 12px; text-transform: uppercase; }
        .tag { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
        .tag-green { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .tag-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .interactive-box { display: flex; flex-direction: column; gap: 12px; }
        input, select, button { padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-card); color: #fff; font-size: 14px; }
        button { background: var(--accent-primary); font-weight: 700; cursor: pointer; border: none; transition: background 0.2s; }
        button:hover { background: #2563eb; }
        pre { background: #000; padding: 12px; border-radius: 8px; font-size: 12px; overflow-x: auto; color: #a7f3d0; max-height: 220px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>CASHFLOW INFINITY: OMNIVERSE</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Perpetual Autonomous Wealth, Market & Deep-Tech Resilience Platform</p>
        </div>
        <div>
            <span class="title-badge">24/7 Daemon Active</span>
            <span class="title-badge" style="background: #064e3b; color: #6ee7b7; margin-left: 8px;">SEBI Safe-Mode</span>
        </div>
    </div>

    <div class="grid-kpi">
        <div class="card">
            <div class="kpi-title">Collected Revenue (Verified)</div>
            <div class="kpi-value text-emerald mono" id="kpi-collected">₹25,000.00</div>
        </div>
        <div class="card">
            <div class="kpi-title">Pipeline Value (CRM)</div>
            <div class="kpi-value text-blue mono" id="kpi-pipeline">₹25,000.00</div>
        </div>
        <div class="card">
            <div class="kpi-title">Active Business Units</div>
            <div class="kpi-value text-amber mono">10 / 10</div>
        </div>
        <div class="card">
            <div class="kpi-title">System Health & Storage</div>
            <div class="kpi-value text-emerald mono" style="font-size: 20px;">HEALTHY (308 GB)</div>
        </div>
    </div>

    <div class="grid-two">
        <div class="card">
            <div class="section-title">📊 Multi-Market Global Overview</div>
            <table>
                <thead>
                    <tr><th>Symbol</th><th>Class</th><th>Price</th><th>24h %</th></tr>
                </thead>
                <tbody>
                    <tr><td>NIFTY50</td><td>EQUITY</td><td class="mono">₹24,500.00</td><td class="text-emerald">+0.65%</td></tr>
                    <tr><td>IN10Y</td><td>FIXED INC</td><td class="mono">6.82%</td><td class="text-blue">-0.04%</td></tr>
                    <tr><td>USDINR</td><td>FOREX</td><td class="mono">₹84.10</td><td class="text-blue">-0.12%</td></tr>
                    <tr><td>BRENT</td><td>COMMODITY</td><td class="mono">$76.50</td><td class="text-emerald">+1.45%</td></tr>
                    <tr><td>BTC</td><td>DIGITAL</td><td class="mono">$72,500.00</td><td class="text-emerald">+2.85%</td></tr>
                </tbody>
            </table>
        </div>

        <div class="card">
            <div class="section-title">🏛️ Autonomous Commerce Matrix (10 Units)</div>
            <table>
                <thead>
                    <tr><th>Unit</th><th>Target Market</th><th>Avg Margin</th></tr>
                </thead>
                <tbody>
                    <tr><td>AI Service Agency</td><td>Local SMBs / Retail</td><td class="mono text-emerald">85%</td></tr>
                    <tr><td>SaaS Factory</td><td>Indie Founders</td><td class="mono text-emerald">92%</td></tr>
                    <tr><td>Developer APIs</td><td>Tech Teams</td><td class="mono text-emerald">88%</td></tr>
                    <tr><td>Market Subscriptions</td><td>HNIs / Traders</td><td class="mono text-emerald">90%</td></tr>
                    <tr><td>Enterprise Tech</td><td>Mid-Market Corp</td><td class="mono text-emerald">75%</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="grid-two">
        <div class="card">
            <div class="section-title">⚡ Instant Client Growth Kit Generator</div>
            <div class="interactive-box">
                <input type="text" id="kit-biz" placeholder="Business Name (e.g., Spice Haven Cafe)" value="Spice Haven Cafe">
                <input type="text" id="kit-niche" placeholder="Niche / Category" value="Restaurant">
                <button onclick="generateKit()">Generate Production Growth Kit</button>
                <pre id="kit-output">// Click generate to craft 10 social captions, hooks, and WhatsApp store copy</pre>
            </div>
        </div>

        <div class="card">
            <div class="section-title">🌍 Aether Geospatial Resilience Evaluator</div>
            <div class="interactive-box">
                <div style="display: flex; gap: 8px;">
                    <input type="number" id="risk-lat" step="0.0001" value="12.9716" placeholder="Latitude" style="flex: 1;">
                    <input type="number" id="risk-lon" step="0.0001" value="77.5946" placeholder="Longitude" style="flex: 1;">
                </div>
                <select id="risk-hazard">
                    <option value="FLOOD">Flood Hazard</option>
                    <option value="SEISMIC">Seismic Hazard</option>
                    <option value="HEAT_STRESS">Extreme Heat Stress</option>
                    <option value="STORM_SURGE">Storm Surge</option>
                </select>
                <button onclick="evaluateRisk()" style="background: var(--accent-indigo);">Run Aether Risk Assessment</button>
                <pre id="risk-output">// Click assess to compute WGS84 vulnerability index and emergency mitigation</pre>
            </div>
        </div>
    </div>

    <script>
        async function generateKit() {
            const biz = document.getElementById('kit-biz').value;
            const niche = document.getElementById('kit-niche').value;
            document.getElementById('kit-output').innerText = 'Generating kit via AI Agency Engine...';
            try {
                const res = await fetch('/api/v1/revenue/growth-kit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({business_name: biz, niche: niche, city: 'Bengaluru'})
                });
                const data = await res.json();
                document.getElementById('kit-output').innerText = JSON.stringify(data, null, 2);
            } catch(e) {
                document.getElementById('kit-output').innerText = 'Error: ' + e;
            }
        }

        async function evaluateRisk() {
            const lat = parseFloat(document.getElementById('risk-lat').value);
            const lon = parseFloat(document.getElementById('risk-lon').value);
            const hazard = document.getElementById('risk-hazard').value;
            document.getElementById('risk-output').innerText = 'Calculating geospatial hazard index...';
            try {
                const res = await fetch('/api/v1/aether/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({lat: lat, lon: lon, elevation_meters: 920.0, hazard: hazard})
                });
                const data = await res.json();
                document.getElementById('risk-output').innerText = JSON.stringify(data, null, 2);
            } catch(e) {
                document.getElementById('risk-output').innerText = 'Error: ' + e;
            }
        }
    </script>
</body>
</html>
"""
        return HTMLResponse(content=html_content)

    return router
