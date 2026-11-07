# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Interactive Multi-Tenant Vertical SaaS Fleet UI Template.

Provides real-time interactive dashboards and algorithmic simulators for:
- CloudBite: Food cost accounting & kitchen recipe margins
- GymVerse: Member retention risk & churn prediction
- RentShield: Tenant lease default underwriting
- ClinicFlow: Outpatient symptom triage queue priority
"""

def render_saas_portal_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMNIVERSE // Vertical SaaS Fleet Command</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;800&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #030712;
            --surface: #0b1329;
            --surface-border: #1e293b;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .navbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 32px;
            background: rgba(11, 19, 41, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--surface-border);
            position: sticky;
            top: 0;
            z-index: 50;
        }}
        .brand {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 2px;
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .brand-badge {{
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.4);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
        }}
        .nav-links {{
            display: flex;
            gap: 8px;
        }}
        .nav-link {{
            color: var(--text-muted);
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .nav-link:hover, .nav-link.active {{
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--surface-border);
        }}
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px 24px;
            width: 100%;
            flex: 1;
        }}
        .hero {{
            margin-bottom: 32px;
        }}
        .hero h1 {{
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #fff 40%, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .hero p {{
            color: var(--text-muted);
            font-size: 15px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 12px;
            padding: 20px;
        }}
        .kpi-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 8px;
        }}
        .kpi-val {{
            font-size: 26px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-main);
        }}
        .tabs {{
            display: flex;
            gap: 12px;
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}
        .tab-btn {{
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.03);
        }}
        .tab-btn.active {{
            background: rgba(6, 182, 212, 0.1);
            color: var(--accent-cyan);
            border-color: rgba(6, 182, 212, 0.3);
        }}
        .panel {{
            display: none;
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 14px;
            padding: 28px;
        }}
        .panel.active {{
            display: block;
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .form-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .form-group label {{
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .form-control {{
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid var(--surface-border);
            border-radius: 8px;
            padding: 12px 14px;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .form-control:focus {{
            border-color: var(--accent-cyan);
        }}
        .btn {{
            background: var(--accent-cyan);
            color: #030712;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn:hover {{
            box-shadow: 0 0 16px rgba(6, 182, 212, 0.4);
            transform: translateY(-1px);
        }}
        .result-box {{
            background: rgba(3, 7, 18, 0.9);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
        }}
        .badge-success {{ background: rgba(16, 185, 129, 0.2); color: var(--accent-green); border: 1px solid rgba(16, 185, 129, 0.4); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.4); }}
        .badge-danger {{ background: rgba(244, 63, 94, 0.2); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.4); }}
        .tenant-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
            font-size: 13px;
        }}
        .tenant-table th, .tenant-table td {{
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--surface-border);
        }}
        .tenant-table th {{
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="brand">
            <span>OMNIVERSE</span>
            <span class="brand-badge">VERSE FLEET</span>
        </div>
        <nav class="nav-links">
            <a href="/cockpit" class="nav-link">🚀 Cockpit</a>
            <a href="/saas" class="nav-link active">🏢 SaaS Fleet</a>
            <a href="/aether-map" class="nav-link">🛰️ Aether Radar</a>
            <a href="/portal" class="nav-link">💼 Client Portal</a>
            <a href="/docs" class="nav-link">📖 API Docs</a>
        </nav>
    </header>

    <main class="main-container">
        <div class="hero">
            <h1>Vertical SaaS Holdings Fleet</h1>
            <p>Multi-tenant autonomous operating systems powering high-margin vertical business workflows.</p>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Active Fleet Tenants</div>
                <div class="kpi-val" id="kpi-tenants">4</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Combined MRR</div>
                <div class="kpi-val" id="kpi-mrr" style="color: var(--accent-green);">$706.00</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Projected Fleet ARR</div>
                <div class="kpi-val" id="kpi-arr" style="color: var(--accent-cyan);">$8,472.00</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Fleet Gross Margin</div>
                <div class="kpi-val" style="color: var(--accent-purple);">91.4%</div>
            </div>
        </div>

        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('cloudbite')">🍳 CloudBite (Kitchens)</button>
            <button class="tab-btn" onclick="switchTab('gymverse')">🏋️ GymVerse (Fitness)</button>
            <button class="tab-btn" onclick="switchTab('rentshield')">🛡️ RentShield (Real Estate)</button>
            <button class="tab-btn" onclick="switchTab('clinicflow')">🩺 ClinicFlow (Healthcare)</button>
            <button class="tab-btn" onclick="switchTab('tenants')">📋 Registered Tenants</button>
        </div>

        <!-- CLOUDBITE -->
        <div id="panel-cloudbite" class="panel active">
            <h2 style="margin-bottom: 8px;">CloudBite: Food Cost & Margin Calculator</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">Algorithmic recipe margin optimization and ingredient waste prevention.</p>
            <div class="form-grid">
                <div class="form-group">
                    <label>Menu Item Selling Price ($)</label>
                    <input type="number" id="cb-price" class="form-control" value="24.00" step="0.5">
                </div>
                <div class="form-group">
                    <label>Ingredient Costs ($ Comma-separated)</label>
                    <input type="text" id="cb-ingredients" class="form-control" value="3.50, 1.75, 1.20">
                </div>
                <div class="form-group">
                    <label>Labor & Packaging Overhead ($)</label>
                    <input type="number" id="cb-overhead" class="form-control" value="2.00" step="0.5">
                </div>
            </div>
            <button class="btn" onclick="calculateCloudBite()">Calculate Recipe Economics</button>
            <div id="cb-result" class="result-box" style="display: none;"></div>
        </div>

        <!-- GYMVERSE -->
        <div id="panel-gymverse" class="panel">
            <h2 style="margin-bottom: 8px;">GymVerse: Member Retention & Churn Predictor</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">Predict member renewal probabilities and automate WhatsApp retention hooks.</p>
            <div class="form-grid">
                <div class="form-group">
                    <label>Check-ins in Last 30 Days</label>
                    <input type="number" id="gv-checkins" class="form-control" value="12" min="0" max="60">
                </div>
                <div class="form-group">
                    <label>Auto-Pay Active?</label>
                    <select id="gv-autopay" class="form-control">
                        <option value="true" selected>Yes - Active Auto-Pay</option>
                        <option value="false">No - Manual Renewal</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="calculateGymVerse()">Assess Member Retention</button>
            <div id="gv-result" class="result-box" style="display: none;"></div>
        </div>

        <!-- RENTSHIELD -->
        <div id="panel-rentshield" class="panel">
            <h2 style="margin-bottom: 8px;">RentShield: Tenant Default Underwriting</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">Underwrite lease applications with automated debt-to-income and credit algorithms.</p>
            <div class="form-grid">
                <div class="form-group">
                    <label>Monthly Rent ($)</label>
                    <input type="number" id="rs-rent" class="form-control" value="2500" step="100">
                </div>
                <div class="form-group">
                    <label>Declared Monthly Income ($)</label>
                    <input type="number" id="rs-income" class="form-control" value="8500" step="250">
                </div>
                <div class="form-group">
                    <label>Credit Score (300-850)</label>
                    <input type="number" id="rs-credit" class="form-control" value="740" min="300" max="850">
                </div>
            </div>
            <button class="btn" onclick="calculateRentShield()">Underwrite Lease</button>
            <div id="rs-result" class="result-box" style="display: none;"></div>
        </div>

        <!-- CLINICFLOW -->
        <div id="panel-clinicflow" class="panel">
            <h2 style="margin-bottom: 8px;">ClinicFlow: Outpatient Triage & Priority Queue</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">Algorithmic patient symptom classification and clinical priority assignment.</p>
            <div class="form-grid">
                <div class="form-group">
                    <label>Reported Symptoms</label>
                    <input type="text" id="cf-symptoms" class="form-control" value="High fever, shortness of breath, sudden fatigue">
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" id="cf-age" class="form-control" value="45" min="1" max="120">
                </div>
                <div class="form-group">
                    <label>Pre-existing Conditions?</label>
                    <select id="cf-preexisting" class="form-control">
                        <option value="true" selected>Yes (Asthma/Hypertension/Diabetes)</option>
                        <option value="false">None</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="calculateClinicFlow()">Triage Patient</button>
            <div id="cf-result" class="result-box" style="display: none;"></div>
        </div>

        <!-- REGISTERED TENANTS -->
        <div id="panel-tenants" class="panel">
            <h2 style="margin-bottom: 8px;">Registered Fleet Tenants</h2>
            <p style="color: var(--text-muted); margin-bottom: 16px;">Live multi-tenant instances running across the 4 SaaS verticals.</p>
            <table class="tenant-table">
                <thead>
                    <tr>
                        <th>Vertical</th>
                        <th>Tenant Name</th>
                        <th>Plan Tier</th>
                        <th>MRR (USD)</th>
                        <th>Subdomain</th>
                    </tr>
                </thead>
                <tbody id="tenant-rows">
                    <tr>
                        <td><span class="badge badge-success">CLOUDBITE</span></td>
                        <td>Bangalore Biryani Box Kitchens</td>
                        <td>GROWTH</td>
                        <td>$99.00</td>
                        <td><code>biryanibox.cloudbite.io</code></td>
                    </tr>
                    <tr>
                        <td><span class="badge badge-success">GYMVERSE</span></td>
                        <td>IronCore CrossFit HSR</td>
                        <td>GROWTH</td>
                        <td>$139.00</td>
                        <td><code>ironcore.gymverse.io</code></td>
                    </tr>
                    <tr>
                        <td><span class="badge badge-success">RENTSHIELD</span></td>
                        <td>Prestige Koramangala Estates</td>
                        <td>ENTERPRISE</td>
                        <td>$349.00</td>
                        <td><code>prestige.rentshield.io</code></td>
                    </tr>
                    <tr>
                        <td><span class="badge badge-success">CLINICFLOW</span></td>
                        <td>Apollo Outpatient Indiranagar</td>
                        <td>GROWTH</td>
                        <td>$119.00</td>
                        <td><code>apollo.clinicflow.io</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>

    <script>
        function switchTab(vertical) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            event.target.classList.add('active');
            const panel = document.getElementById(`panel-${{vertical}}`);
            if (panel) panel.classList.add('active');
        }}

        async function calculateCloudBite() {{
            const price = parseFloat(document.getElementById('cb-price').value) || 20.0;
            const ing_raw = document.getElementById('cb-ingredients').value;
            const ingredients = ing_raw.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));
            const overhead = parseFloat(document.getElementById('cb-overhead').value) || 0.0;

            const res = await fetch('/api/v1/saas/calculator/cloudbite', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ selling_price: price, ingredient_costs: ingredients, labor_overhead: overhead }})
            }});
            const data = await res.json();
            const box = document.getElementById('cb-result');
            box.style.display = 'block';
            box.innerHTML = `
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: var(--accent-cyan);">Calculated Cloud Kitchen Unit Economics</div>
                <div>Food Cost Percentage: <strong>${{data.food_cost_pct}}%</strong></div>
                <div>Total Cost per Serving: <strong>$${{data.total_cost_with_overhead}}</strong></div>
                <div>Gross Profit Margin: <strong>${{data.gross_margin_pct}}%</strong></div>
                <div style="margin-top: 10px;">Status: <span class="badge ${{data.status === 'HEALTHY' ? 'badge-success' : 'badge-warning'}}">${{data.status}}</span></div>
            `;
        }}

        async function calculateGymVerse() {{
            const checkins = parseInt(document.getElementById('gv-checkins').value) || 0;
            const autopay = document.getElementById('gv-autopay').value === 'true';

            const res = await fetch('/api/v1/saas/calculator/gymverse', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ checkins_last_30d: checkins, auto_pay_active: autopay }})
            }});
            const data = await res.json();
            const box = document.getElementById('gv-result');
            box.style.display = 'block';
            box.innerHTML = `
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: var(--accent-cyan);">Gym Member Retention Telemetry</div>
                <div>Retention Health Score: <strong>${{data.retention_score}} / 100</strong></div>
                <div>Churn Risk Classification: <span class="badge ${{data.churn_risk === 'LOW' ? 'badge-success' : (data.churn_risk === 'MEDIUM' ? 'badge-warning' : 'badge-danger')}}">${{data.churn_risk}} RISK</span></div>
                <div style="margin-top: 8px; color: var(--accent-cyan);">Autonomous Retention Trigger: <em>${{data.recommended_action}}</em></div>
            `;
        }}

        async function calculateRentShield() {{
            const rent = parseFloat(document.getElementById('rs-rent').value) || 2000;
            const income = parseFloat(document.getElementById('rs-income').value) || 6000;
            const credit = parseInt(document.getElementById('rs-credit').value) || 700;

            const res = await fetch('/api/v1/saas/calculator/rentshield', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ monthly_rent: rent, declared_monthly_income: income, credit_score: credit }})
            }});
            const data = await res.json();
            const box = document.getElementById('rs-result');
            box.style.display = 'block';
            box.innerHTML = `
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: var(--accent-cyan);">RentShield Underwriting Scorecard</div>
                <div>Underwriting Score: <strong>${{data.underwriting_score}} / 100</strong></div>
                <div>Rent-to-Income Ratio: <strong>${{(data.rent_to_income_ratio * 100).toFixed(1)}}%</strong></div>
                <div>Decision: <span class="badge ${{data.risk_tier === 'APPROVED_LOW_RISK' ? 'badge-success' : 'badge-danger'}}">${{data.risk_tier}}</span></div>
                <div style="margin-top: 8px;">Recommended Security Deposit: <strong>${{data.recommended_deposit_months}} Months</strong></div>
            `;
        }}

        async function calculateClinicFlow() {{
            const symptoms = document.getElementById('cf-symptoms').value;
            const age = parseInt(document.getElementById('cf-age').value) || 30;
            const preexisting = document.getElementById('cf-preexisting').value === 'true';

            const res = await fetch('/api/v1/saas/calculator/clinicflow', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ symptoms: symptoms, age: age, has_preexisting_conditions: preexisting }})
            }});
            const data = await res.json();
            const box = document.getElementById('cf-result');
            box.style.display = 'block';
            box.innerHTML = `
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: var(--accent-cyan);">ClinicFlow Triage Assessment</div>
                <div>Severity Score: <strong>${{data.severity_score}} / 100</strong></div>
                <div>Triage Priority Queue: <span class="badge ${{data.priority === 'PRIORITY_1_EMERGENCY' ? 'badge-danger' : (data.priority === 'PRIORITY_2_URGENT' ? 'badge-warning' : 'badge-success')}}">${{data.priority}}</span></div>
                <div>Assigned Clinical Department: <strong>${{data.department}}</strong></div>
                <div>Estimated Doctor Wait Time: <strong>${{data.estimated_wait_minutes}} Minutes</strong></div>
            `;
        }}
    </script>
</body>
</html>
"""
