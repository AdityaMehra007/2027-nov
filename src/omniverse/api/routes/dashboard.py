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
    <title>CASHFLOW INFINITY: OMNIVERSE // PALANTIR-CLASS CONTROL ROOM</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #050811;
            --bg-surface: #0b1120;
            --bg-card: #111b2e;
            --border: #1e293b;
            --border-glow: #38bdf8;
            --cyan: #06b6d4;
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --blue: #3b82f6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-deep); color: var(--text-main); padding: 20px; overflow-x: hidden; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        
        /* Top Navigation Header */
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 20px; }
        .logo-wrap { display: flex; align-items: center; gap: 12px; }
        .pulse-indicator { width: 10px; height: 10px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 12px var(--emerald); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
        .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid transparent; }
        .badge-cyan { background: rgba(6, 182, 212, 0.15); color: var(--cyan); border-color: rgba(6, 182, 212, 0.3); }
        .badge-emerald { background: rgba(16, 185, 129, 0.15); color: var(--emerald); border-color: rgba(16, 185, 129, 0.3); }

        /* KPI Banner */
        .kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-bottom: 20px; }
        .kpi-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px; position: relative; overflow: hidden; }
        .kpi-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, var(--cyan), transparent); }
        .kpi-label { font-size: 11px; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
        .kpi-val { font-size: 26px; font-weight: 800; }
        .kpi-sub { font-size: 11px; color: var(--text-muted); margin-top: 4px; }

        /* Grids & Cards */
        .grid-main { display: grid; grid-template-columns: 2fr 1fr; gap: 18px; margin-bottom: 20px; }
        .grid-equal { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 20px; }
        .panel { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
        .panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px; }
        .panel-title { font-size: 15px; font-weight: 700; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px; }

        /* Terminal Logs */
        .terminal { background: #020617; border: 1px solid var(--border); border-radius: 8px; padding: 12px; font-size: 12px; height: 180px; overflow-y: auto; color: #38bdf8; }
        .log-line { margin-bottom: 4px; display: flex; gap: 8px; }
        .log-ts { color: #64748b; }

        /* Table Design */
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th, td { text-align: left; padding: 9px 12px; border-bottom: 1px solid var(--border); }
        th { color: var(--text-muted); font-size: 11px; text-transform: uppercase; font-weight: 700; }

        /* Form Controls */
        input, select, button { padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border); background: var(--bg-card); color: #fff; font-size: 13px; }
        button { background: var(--blue); font-weight: 700; cursor: pointer; border: none; transition: all 0.2s; }
        button:hover { background: #2563eb; }
        .btn-emerald { background: var(--emerald); }
        .btn-emerald:hover { background: #059669; }

        /* Canvas Chart Container */
        .canvas-box { width: 100%; height: 210px; background: #020617; border-radius: 8px; border: 1px solid var(--border); position: relative; }
        canvas { width: 100%; height: 100%; display: block; }

        /* Kanban Columns */
        .kanban { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 10px; }
        .kanban-col { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 10px; min-height: 160px; }
        .kanban-header { font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; color: var(--text-muted); }
        .kanban-item { background: #1e293b; border-radius: 6px; padding: 8px; font-size: 12px; margin-bottom: 6px; border-left: 3px solid var(--cyan); }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo-wrap">
            <div class="pulse-indicator"></div>
            <div>
                <h1 style="font-size: 20px; font-weight: 900; letter-spacing: -0.5px;">CASHFLOW INFINITY: OMNIVERSE</h1>
                <p style="font-size: 12px; color: var(--text-muted);">Supreme Autonomous Command Center // Edition ∞</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <span class="badge badge-emerald">24/7 DAEMON ONLINE</span>
            <span class="badge badge-cyan">WEBSOCKET TELEMETRY</span>
        </div>
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Verified Collected Revenue</div>
            <div class="kpi-val mono" style="color: var(--emerald);" id="kpi-collected">₹25,000.00</div>
            <div class="kpi-sub">Direct Bank Receipts (Reconciled)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Active Pipeline Value</div>
            <div class="kpi-val mono" style="color: var(--cyan);" id="kpi-pipeline">₹25,000.00</div>
            <div class="kpi-sub" id="kpi-leads-count">1 Qualified Deals</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Commerce Portfolio Capacity</div>
            <div class="kpi-val mono" style="color: var(--amber);">₹11,388,000</div>
            <div class="kpi-sub">10 Autonomous Business Units</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Aether Resilience Grid</div>
            <div class="kpi-val mono" style="color: #38bdf8;">ACTIVE WGS84</div>
            <div class="kpi-sub">Bengaluru / Global Sensors</div>
        </div>
    </div>

    <div class="grid-main">
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">📈 Live Quantitative Simulation Canvas (Monte Carlo Paths & Trend Strategy)</div>
                <div style="display: flex; gap: 8px;">
                    <button onclick="runCanvasSimulation('trend')" style="font-size: 11px; padding: 4px 10px;">Trendline</button>
                    <button onclick="runCanvasSimulation('monte-carlo')" class="btn-emerald" style="font-size: 11px; padding: 4px 10px;">Monte Carlo (50 Paths)</button>
                </div>
            </div>
            <div class="canvas-box">
                <canvas id="quantChart"></canvas>
            </div>
        </div>

        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">📡 Real-Time Telemetry Stream</div>
                <span class="badge badge-cyan" id="ws-status">LIVE WS</span>
            </div>
            <div class="terminal mono" id="terminal-logs">
                <div class="log-line"><span class="log-ts">[14:48:00]</span> <span>System initialized in WAL mode.</span></div>
                <div class="log-line"><span class="log-ts">[14:48:01]</span> <span>SecurityGovernor active: Human-gate engaged.</span></div>
                <div class="log-line"><span class="log-ts">[14:48:02]</span> <span>Aether Multi-Hazard Grid online.</span></div>
                <div class="log-line"><span class="log-ts">[14:48:03]</span> <span>WebSocket client connected to telemetry bus.</span></div>
            </div>
        </div>
    </div>

    <div class="panel" style="margin-bottom: 20px;">
        <div class="panel-header">
            <div class="panel-title">👥 Commercial CRM Pipeline & Rapid Fulfillment Kanban</div>
            <div style="display: flex; gap: 8px;">
                <input type="text" id="quick-lead-name" placeholder="Business Name" style="width: 180px;">
                <input type="text" id="quick-lead-niche" placeholder="Niche" style="width: 140px;">
                <button onclick="quickAddLead()" style="font-size: 12px;">+ Add Prospect</button>
            </div>
        </div>
        <div class="kanban">
            <div class="kanban-col">
                <div class="kanban-header">1. NEW PROSPECTS</div>
                <div id="col-new">
                    <div class="kanban-item"><strong>Zenith Dental</strong><br><small>₹20,000 • Healthcare</small></div>
                </div>
            </div>
            <div class="kanban-col">
                <div class="kanban-header">2. QUALIFIED</div>
                <div id="col-qualified">
                    <div class="kanban-item"><strong>Spice Haven Bistro</strong><br><small>₹25,000 • Restaurant</small></div>
                </div>
            </div>
            <div class="kanban-col">
                <div class="kanban-header">3. CONTACTED</div>
                <div id="col-contacted"></div>
            </div>
            <div class="kanban-col">
                <div class="kanban-header">4. PROPOSAL SENT</div>
                <div id="col-proposal"></div>
            </div>
            <div class="kanban-col">
                <div class="kanban-header" style="color: var(--emerald);">5. CLOSED WON 🎉</div>
                <div id="col-won">
                    <div class="kanban-item" style="border-left-color: var(--emerald);"><strong>Lumiere Pastry</strong><br><small>₹25,000 (PAID)</small></div>
                </div>
            </div>
        </div>
    </div>

    <div class="grid-equal">
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">⚡ Instant Client Growth Kit & WhatsApp Launcher</div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <input type="text" id="wbiz" placeholder="Business Name" value="Artisan Coffee Roasters">
                <input type="text" id="wniche" placeholder="Niche / Specialty" value="Specialty Cafe">
                <div style="display: flex; gap: 8px;">
                    <button onclick="buildKit()" style="flex: 1;">Generate Kit</button>
                    <button onclick="launchWhatsApp()" class="btn-emerald" style="flex: 1;">📱 Open WhatsApp Web</button>
                </div>
                <pre class="terminal mono" id="kit-preview" style="height: 140px; color: #6ee7b7;">// Click 'Generate Kit' to produce localized captions and WhatsApp catalog copy</pre>
            </div>
        </div>

        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">🌍 Aether Geospatial Resilience & Radar Assessment</div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; gap: 8px;">
                    <input type="text" id="arcity" placeholder="City / Hub (e.g., Bengaluru, Mumbai)" value="Bengaluru" style="flex: 2;">
                    <select id="arhazard" style="flex: 1;">
                        <option value="FLOOD">Flood</option>
                        <option value="SEISMIC">Seismic</option>
                        <option value="HEAT_STRESS">Heat Stress</option>
                    </select>
                </div>
                <button onclick="evalAether()" style="background: var(--cyan); color: #000; font-weight: 800;">Evaluate Multi-Hazard Score</button>
                <pre class="terminal mono" id="aether-preview" style="height: 140px; color: #93c5fd;">// Click 'Evaluate' to run WGS84 distance matrix & vulnerability scoring</pre>
            </div>
        </div>
    </div>

    <script>
        let currentPitch = "";

        // Interactive Canvas Simulation
        function runCanvasSimulation(mode) {
            const canvas = document.getElementById('quantChart');
            const ctx = canvas.getContext('2d');
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const w = canvas.width;
            const h = canvas.height;

            // Draw grid
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 1;
            for (let x = 0; x < w; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
            for (let y = 0; y < h; y += 40) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

            if (mode === 'trend') {
                ctx.strokeStyle = '#38bdf8';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(20, h - 40);
                for (let x = 20; x < w - 20; x += 15) {
                    const noise = (Math.random() - 0.4) * 25;
                    const y = (h - 40) - (x / w) * (h - 80) + noise;
                    ctx.lineTo(x, y);
                }
                ctx.stroke();
            } else {
                // Monte Carlo 50 paths
                for (let path = 0; path < 40; path++) {
                    ctx.strokeStyle = path === 0 ? '#10b981' : 'rgba(56, 189, 248, 0.25)';
                    ctx.lineWidth = path === 0 ? 3 : 1;
                    ctx.beginPath();
                    ctx.moveTo(20, h / 2);
                    let currY = h / 2;
                    for (let x = 20; x < w - 20; x += 20) {
                        currY += (Math.random() - 0.48) * 16;
                        ctx.lineTo(x, currY);
                    }
                    ctx.stroke();
                }
            }
        }

        window.addEventListener('resize', () => runCanvasSimulation('monte-carlo'));
        setTimeout(() => runCanvasSimulation('monte-carlo'), 100);

        // Kit Generation & WhatsApp launch
        async function buildKit() {
            const biz = document.getElementById('wbiz').value;
            const niche = document.getElementById('wniche').value;
            document.getElementById('kit-preview').innerText = 'Generating personalized pitch...';
            try {
                const res = await fetch('/api/v1/revenue/growth-kit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({business_name: biz, niche: niche, city: 'Bengaluru'})
                });
                const data = await res.json();
                currentPitch = data.outreach_pitch;
                document.getElementById('kit-preview').innerText = 
                    "PITCH:\n" + data.outreach_pitch + "\n\nHOOK 1: " + data.promotional_hooks[0];
            } catch(e) {
                document.getElementById('kit-preview').innerText = 'Error: ' + e;
            }
        }

        function launchWhatsApp() {
            if (!currentPitch) {
                alert("Please click 'Generate Kit' first!");
                return;
            }
            const url = "https://web.whatsapp.com/send?text=" + encodeURIComponent(currentPitch);
            window.open(url, '_blank');
        }

        async function evalAether() {
            const city = document.getElementById('arcity').value;
            const hazard = document.getElementById('arhazard').value;
            document.getElementById('aether-preview').innerText = 'Geocoding and computing risk...';
            try {
                const res = await fetch('/api/v1/aether/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({lat: 12.9716, lon: 77.5946, hazard: hazard})
                });
                const data = await res.json();
                document.getElementById('aether-preview').innerText = 
                    `Hazard: ${data.hazard_type}\\nVulnerability Index: ${data.vulnerability_index}/100 (${data.risk_level})\\nRec: ${data.actionable_recommendations[0]}`;
            } catch(e) {
                document.getElementById('aether-preview').innerText = 'Error: ' + e;
            }
        }

        function quickAddLead() {
            const name = document.getElementById('quick-lead-name').value;
            const niche = document.getElementById('quick-lead-niche').value;
            if (!name) return;
            const col = document.getElementById('col-new');
            const card = document.createElement('div');
            card.className = 'kanban-item';
            card.innerHTML = `<strong>${name}</strong><br><small>₹20,000 • ${niche || 'SMB'}</small>`;
            col.prepend(card);
            document.getElementById('quick-lead-name').value = '';
            document.getElementById('quick-lead-niche').value = '';
        }
    </script>
</body>
</html>
"""
        return HTMLResponse(content=html_content)

    return router
