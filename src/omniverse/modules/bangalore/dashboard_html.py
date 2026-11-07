"""
BENGALURU BANKING & GCC EXECUTIVE DASHBOARD HTML RENDERER
Cashflow Infinity: Omniverse Platform
"""

def render_banking_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BENGALURU BANKING NEXUS // PALANTIR-CLASS GCC COMMAND</title>
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
            --purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-deep); color: var(--text-main); padding: 24px; min-height: 100vh; }
        .mono { font-family: 'JetBrains Mono', monospace; }

        /* Header */
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 24px; }
        .logo-wrap { display: flex; align-items: center; gap: 14px; }
        .pulse-indicator { width: 12px; height: 12px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 14px var(--emerald); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
        .title { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
        .subtitle { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
        .badge { padding: 5px 12px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .badge-cyan { background: rgba(6, 182, 212, 0.15); color: var(--cyan); border: 1px solid rgba(6, 182, 212, 0.3); }
        .badge-emerald { background: rgba(16, 185, 129, 0.15); color: var(--emerald); border: 1px solid rgba(16, 185, 129, 0.3); }

        /* KPI Banner */
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .kpi-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; position: relative; }
        .kpi-card:hover { border-color: var(--border-glow); }
        .kpi-label { font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; }
        .kpi-val { font-size: 24px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
        .kpi-sub { font-size: 11px; color: var(--cyan); margin-top: 6px; }

        /* Navigation Tabs */
        .tabs { display: flex; gap: 8px; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 24px; overflow-x: auto; }
        .tab-btn { background: transparent; border: 1px solid var(--border); color: var(--text-muted); padding: 9px 18px; border-radius: 8px; font-weight: 600; font-size: 13px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
        .tab-btn:hover { color: var(--text-main); border-color: var(--cyan); }
        .tab-btn.active { background: rgba(6, 182, 212, 0.15); color: var(--cyan); border-color: var(--cyan); }

        /* Tab Panes */
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Cards & Grid */
        .facility-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }
        .facility-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: transform 0.2s; }
        .facility-card:hover { transform: translateY(-2px); border-color: rgba(56, 189, 248, 0.4); }
        .facility-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
        .facility-name { font-size: 16px; font-weight: 700; color: #fff; }
        .facility-corridor { font-size: 11px; color: var(--cyan); font-weight: 600; margin-top: 3px; }
        .facility-detail { font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
        .tag-pill { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; margin-right: 6px; margin-top: 8px; background: rgba(255,255,255,0.05); border: 1px solid var(--border); }

        /* Interactive Simulator */
        .sim-container { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        @media (max-width: 900px) { .sim-container { grid-template-columns: 1fr; } }
        .panel { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
        .form-group { margin-bottom: 18px; }
        .form-label { display: block; font-size: 12px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; }
        .form-control { width: 100%; padding: 10px 14px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: #fff; font-size: 14px; }
        .form-control:focus { outline: none; border-color: var(--cyan); }
        .range-wrap { display: flex; align-items: center; gap: 14px; }
        .range-slider { flex: 1; accent-color: var(--cyan); cursor: pointer; }
        .range-val { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 16px; color: var(--cyan); min-width: 60px; text-align: right; }

        .stat-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 13px; }
        .stat-row:last-child { border-bottom: none; }
        .stat-highlight { font-weight: 800; font-size: 18px; color: var(--emerald); font-family: 'JetBrains Mono', monospace; }

        /* Checkbox list */
        .check-item { display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 10px; cursor: pointer; }
        .check-item input { accent-color: var(--emerald); width: 18px; height: 18px; }
        .check-title { font-size: 13px; font-weight: 600; color: #fff; }
        .check-desc { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

        /* Score Meter */
        .score-box { text-align: center; padding: 24px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 20px; }
        .score-circle { font-size: 48px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--emerald); }
        .score-status { font-size: 14px; font-weight: 700; margin-top: 6px; }

        /* Table */
        .data-table { width: 100%; border-collapse: collapse; margin-top: 14px; }
        .data-table th, .data-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }
        .data-table th { background: rgba(255,255,255,0.02); color: var(--text-muted); font-size: 11px; text-transform: uppercase; font-weight: 600; }
        .data-table tr:hover { background: rgba(255,255,255,0.02); }
    </style>
</head>
<body>

    <header class="header">
        <div class="logo-wrap">
            <div class="pulse-indicator"></div>
            <div>
                <h1 class="title">BENGALURU BANKING OPERATIONS & GCC COMMAND NEXUS</h1>
                <p class="subtitle mono">CASHFLOW INFINITY // DUAL-CORE FINANCIAL INTELLIGENCE FABRIC</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <span class="badge badge-cyan">2027 ACTIVE HORIZON</span>
            <span class="badge badge-emerald">RBI / DPDP / CERT-In COMPLIANT</span>
        </div>
    </header>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Monitored Facilities</div>
            <div class="kpi-val" id="kpi-facilities">10</div>
            <div class="kpi-sub">Tier-1 GCCs, PSU HQs & Tech Parks</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Tracked GCC Capacity</div>
            <div class="kpi-val" id="kpi-seats">64,500</div>
            <div class="kpi-sub">Operational Banking Technology Seats</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Prime Banking Corridors</div>
            <div class="kpi-val">6 Zones</div>
            <div class="kpi-sub">ORR, Whitefield, CBD, Manyata, E-City, HSR</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">RBI Data Residency</div>
            <div class="kpi-val" style="color: var(--emerald);">100%</div>
            <div class="kpi-sub">AWS Mumbai & Azure Pune Localized</div>
        </div>
    </div>

    <nav class="tabs">
        <button class="tab-btn active" onclick="switchTab('facilities')">Verified Campuses & HQs</button>
        <button class="tab-btn" onclick="switchTab('simulator')">GCC Capex / Opex Simulator</button>
        <button class="tab-btn" onclick="switchTab('compliance')">RBI & DPDP Audit Studio</button>
        <button class="tab-btn" onclick="switchTab('branches')">Smart Branch Network</button>
        <button class="tab-btn" onclick="switchTab('talent')">Tech Talent & Compensation</button>
    </nav>

    <!-- TAB 1: Facilities Explorer -->
    <section id="tab-facilities" class="tab-content active">
        <div style="margin-bottom: 18px; display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 13px; color: var(--text-muted); font-weight: 600;">FILTER CORRIDOR:</span>
            <button class="tab-btn active" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('ALL', this)">ALL</button>
            <button class="tab-btn" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('OUTER_RING_ROAD', this)">Outer Ring Road</button>
            <button class="tab-btn" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('CBD_MG_ROAD', this)">CBD (MG/JC Rd)</button>
            <button class="tab-btn" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('WHITEFIELD', this)">Whitefield</button>
            <button class="tab-btn" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('NORTH_MANYATA', this)">North Manyata</button>
            <button class="tab-btn" style="padding: 6px 12px; font-size: 12px;" onclick="filterCorridor('KORAMANGALA_HSR', this)">Fintech Valley</button>
        </div>
        <div class="facility-grid" id="facility-container"></div>
    </section>

    <!-- TAB 2: GCC Sizer -->
    <section id="tab-simulator" class="tab-content">
        <div class="sim-container">
            <div class="panel">
                <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; color: var(--cyan);">FACILITY SIZING PARAMETERS</h2>
                <div class="form-group">
                    <label class="form-label">Operational Headcount (Seats)</label>
                    <div class="range-wrap">
                        <input type="range" class="range-slider" min="500" max="10000" step="250" value="2500" id="sim-seats" oninput="calculateBlueprint()">
                        <span class="range-val" id="seats-display">2,500</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Bengaluru Corridor</label>
                    <select class="form-control" id="sim-corridor" onchange="calculateBlueprint()">
                        <option value="OUTER_RING_ROAD" selected>Outer Ring Road (Bellandur/ETV/Ecoworld) - ₹125/sq ft</option>
                        <option value="WHITEFIELD">Whitefield (ITPL/Shantiniketan) - ₹85/sq ft</option>
                        <option value="CBD_MG_ROAD">CBD (MG Rd/JC Rd/Richmond Rd) - ₹170/sq ft</option>
                        <option value="NORTH_MANYATA">North Bengaluru (Manyata/Hebbal) - ₹95/sq ft</option>
                        <option value="ELECTRONIC_CITY">Electronic City (Phase 1/2) - ₹60/sq ft</option>
                        <option value="KORAMANGALA_HSR">Fintech Corridor (HSR/Koramangala) - ₹135/sq ft</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Fitout & Security Tier</label>
                    <select class="form-control" id="sim-grade" onchange="calculateBlueprint()">
                        <option value="ULTRA_GRADE_A_FINANCIAL" selected>Ultra Grade-A (Zero-Trust, Faraday, Class-A Vault) - ₹4,200/sq ft</option>
                        <option value="STANDARD_GRADE_A">Standard Grade-A (Commercial Bank GCC Tech) - ₹3,300/sq ft</option>
                        <option value="VALUE_COMMERCIAL">Value Commercial (Back-Office & Operations) - ₹2,400/sq ft</option>
                    </select>
                </div>
            </div>

            <div class="panel">
                <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; color: var(--emerald);">FINANCIAL MODEL BREAKDOWN</h2>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Super Built-Up Area</span>
                    <span class="mono" id="out-sqft">225,000 sq ft</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Civil & Acoustic Fitout</span>
                    <span class="mono" id="out-civil">₹94.50 Cr</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Electrical, N+2 UPS & 72h DG</span>
                    <span class="mono" id="out-elec">₹31.50 Cr</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Zero-Trust IT, Cisco/Arista & SOC</span>
                    <span class="mono" id="out-it">₹43.50 Cr</span>
                </div>
                <div class="stat-row" style="background: rgba(16, 185, 129, 0.08); padding: 12px; border-radius: 8px; margin: 12px 0;">
                    <span style="font-weight: 700;">TOTAL INITIAL CAPEX</span>
                    <span class="stat-highlight" id="out-capex">₹172.00 Cr (~$20.72M)</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Annual Lease Rent</span>
                    <span class="mono" id="out-rent">₹33.75 Cr / yr</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Annual CAM & Operations</span>
                    <span class="mono" id="out-cam">₹4.72 Cr / yr</span>
                </div>
                <div class="stat-row">
                    <span style="color: var(--text-muted);">Talent Payroll (Blended ₹18.5L/seat)</span>
                    <span class="mono" id="out-payroll">₹462.50 Cr / yr</span>
                </div>
                <div class="stat-row" style="background: rgba(6, 182, 212, 0.08); padding: 12px; border-radius: 8px; margin-top: 12px;">
                    <span style="font-weight: 700;">TOTAL ANNUAL OPEX</span>
                    <span class="stat-highlight" style="color: var(--cyan);" id="out-opex">₹526.48 Cr (~$63.43M)</span>
                </div>
            </div>
        </div>
    </section>

    <!-- TAB 3: Compliance Studio -->
    <section id="tab-compliance" class="tab-content">
        <div class="sim-container">
            <div class="panel">
                <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; color: var(--cyan);">REGULATORY AUDIT CONTROLS</h2>
                <div class="check-item" onclick="toggleCheck('c1')">
                    <input type="checkbox" id="c1" checked onchange="runAudit()">
                    <div>
                        <div class="check-title">RBI Payment Data Localization</div>
                        <div class="check-desc">Primary transaction stores locked to domestic cloud regions (AWS Mumbai / Azure Pune).</div>
                    </div>
                </div>
                <div class="check-item" onclick="toggleCheck('c2')">
                    <input type="checkbox" id="c2" checked onchange="runAudit()">
                    <div>
                        <div class="check-title">DPDP Act 2023 Consent Manager & DPO</div>
                        <div class="check-desc">Registered Data Protection Officer with 72-hour grievance redressal protocol.</div>
                    </div>
                </div>
                <div class="check-item" onclick="toggleCheck('c3')">
                    <input type="checkbox" id="c3" checked onchange="runAudit()">
                    <div>
                        <div class="check-title">CERT-In 6-Hour Escalation SLA</div>
                        <div class="check-desc">Automated SOC triggers dispatching security incidents within 6 hours to CERT-In.</div>
                    </div>
                </div>
                <div class="check-item" onclick="toggleCheck('c4')">
                    <input type="checkbox" id="c4" checked onchange="runAudit()">
                    <div>
                        <div class="check-title">NPL NTP Clock Synchronization</div>
                        <div class="check-desc">All switches and servers synced directly to National Physical Laboratory servers.</div>
                    </div>
                </div>
                <div class="check-item" onclick="toggleCheck('c5')">
                    <input type="checkbox" id="c5" checked onchange="runAudit()">
                    <div>
                        <div class="check-title">RBI Class-A Vault & 90-Day CCTV Retention</div>
                        <div class="check-desc">Reinforced 18-inch concrete vaults and RAID-6 CCTV storage for currency chests.</div>
                    </div>
                </div>
            </div>

            <div class="panel">
                <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; color: var(--emerald);">COMPLIANCE VERDICT</h2>
                <div class="score-box">
                    <div class="score-circle" id="audit-score">100</div>
                    <div class="score-status" id="audit-status" style="color: var(--emerald);">REGULATORY SATISFACTION LEVEL: 100%</div>
                </div>
                <div id="remediation-box" style="display: none;">
                    <div style="font-size: 12px; font-weight: 700; color: var(--rose); margin-bottom: 8px;">MANDATORY REMEDIATION ACTION ITEMS:</div>
                    <ul id="remediation-list" style="padding-left: 20px; font-size: 12px; color: var(--text-muted); line-height: 1.6;"></ul>
                </div>
            </div>
        </div>
    </section>

    <!-- TAB 4: Branch Network -->
    <section id="tab-branches" class="tab-content">
        <div class="panel">
            <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 16px; color: var(--cyan);">BENGALURU HIGH-YIELD SMART BRANCH & WEALTH NETWORK</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Locality</th>
                        <th>Corridor</th>
                        <th>Archetype</th>
                        <th>Area (Carpet)</th>
                        <th>Capex</th>
                        <th>Monthly Opex</th>
                        <th>Target Clientele</th>
                        <th>Specialized Infrastructure</th>
                    </tr>
                </thead>
                <tbody id="branch-table-body">
                    <tr>
                        <td style="font-weight: 700;">Indiranagar (100 Feet Rd)</td>
                        <td>CBD / East</td>
                        <td><span class="tag-pill" style="color: var(--cyan);">TECH WEALTH LOUNGE</span></td>
                        <td class="mono">3,500 sq ft</td>
                        <td class="mono">₹2.20 Cr</td>
                        <td class="mono">₹7.50 L</td>
                        <td>Startup Founders, VCs, Tech Executives</td>
                        <td>ESOP Monetization, Video-KYC, Dual CDMs</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">Sarjapur / Bellandur</td>
                        <td>Outer Ring Road</td>
                        <td><span class="tag-pill" style="color: var(--cyan);">TECH WEALTH LOUNGE</span></td>
                        <td class="mono">4,200 sq ft</td>
                        <td class="mono">₹2.60 Cr</td>
                        <td class="mono">₹8.20 L</td>
                        <td>GCC Tech VPs, Senior Lead Architects</td>
                        <td>8 PM Extended Desk, Biometric Lockers</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">MG Road / Trinity Circle</td>
                        <td>CBD Core</td>
                        <td><span class="tag-pill" style="color: var(--amber);">FLAGSHIP DIGITAL HUB</span></td>
                        <td class="mono">7,500 sq ft</td>
                        <td class="mono">₹4.80 Cr</td>
                        <td class="mono">₹14.00 L</td>
                        <td>Corporate HNI, NRI Desks, Institutional</td>
                        <td>Class-A Vault, Swift Desk, Boardroom</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">Peenya Industrial Phase 1</td>
                        <td>North-West Hub</td>
                        <td><span class="tag-pill" style="color: var(--emerald);">COMMERCIAL SME</span></td>
                        <td class="mono">5,000 sq ft</td>
                        <td class="mono">₹2.90 Cr</td>
                        <td class="mono">₹6.80 L</td>
                        <td>MSME Machine Works, Defense Vendors</td>
                        <td>Working Capital Desk, Heavy Cash Drop Bay</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- TAB 5: Talent Benchmarking -->
    <section id="tab-talent" class="tab-content">
        <div class="panel">
            <h2 style="font-size: 16px; font-weight: 700; margin-bottom: 16px; color: var(--cyan);">BENGALURU GCC & INVESTMENT BANKING COMPENSATION MATRIX</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Role Title</th>
                        <th>Experience</th>
                        <th>Fixed Base (₹ INR)</th>
                        <th>Target Bonus</th>
                        <th>Annual RSUs (USD)</th>
                        <th>Feeder Institutions</th>
                        <th>Retention Playbook</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-weight: 700;">Software Development Engineer I</td>
                        <td class="mono">0-2 Years</td>
                        <td class="mono">₹14L – ₹22L</td>
                        <td class="mono">15%</td>
                        <td class="mono">$6,000</td>
                        <td>IIIT-B, RVCE, BMSCE, PES, NITK</td>
                        <td>Fast-track internal mobility, tuition grants</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">Senior Quant / Algo Trading Engineer</td>
                        <td class="mono">3-6 Years</td>
                        <td class="mono">₹28L – ₹45L</td>
                        <td class="mono">30%</td>
                        <td class="mono">$20,000</td>
                        <td>IISc Bangalore, IIT Madras, IIT Dharwad</td>
                        <td>Profit-share pool, patent royalties</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">VP, Core Banking & Distributed Tech</td>
                        <td class="mono">10-15 Years</td>
                        <td class="mono">₹65L – ₹95L</td>
                        <td class="mono">40%</td>
                        <td class="mono">$50,000</td>
                        <td>Tier-1 Alumni, Global Laterals</td>
                        <td>3-Year vesting cliffs, executive healthcare</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 700;">Managing Director & GCC Country Head</td>
                        <td class="mono">18-25 Years</td>
                        <td class="mono">₹1.4Cr – ₹2.2Cr</td>
                        <td class="mono">60%</td>
                        <td class="mono">$150,000</td>
                        <td>Global Executive Search / C-Suite</td>
                        <td>Direct equity carry, LTIP discretionary pool</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <script>
        const facilitiesData = [
            {
                name: "Goldman Sachs Bengaluru",
                corridor: "OUTER_RING_ROAD",
                campus: "Helios Business Park / Embassy GolfLinks",
                address: "Kadubeesanahalli, ORR",
                seats: 8500,
                sqft: 1100000,
                rent: 135,
                cam: 18,
                power: "72h DG Autonomy (Dual Grid)",
                transit: "Metro Phase 2A (Kadubeesanahalli)",
                tech: "Proprietary SecDB / Slang / Java Cloud Microservices"
            },
            {
                name: "JPMorgan Chase Global Service Center",
                corridor: "OUTER_RING_ROAD",
                campus: "Embassy TechVillage (ETV)",
                address: "Devarabeesanahalli, ORR",
                seats: 14000,
                sqft: 1700000,
                rent: 128,
                cam: 17.5,
                power: "72h DG Autonomy (Dual Grid)",
                transit: "Metro Phase 2A (Bellandur)",
                tech: "Athena / Cloud Native Distributed Ledgers"
            },
            {
                name: "Morgan Stanley Advantage Services",
                corridor: "OUTER_RING_ROAD",
                campus: "RMZ Ecoworld (Campus 30)",
                address: "Bellandur, ORR",
                seats: 5500,
                sqft: 680000,
                rent: 130,
                cam: 18,
                power: "72h DG Autonomy (Dual Grid)",
                transit: "Metro Phase 2A (Ecoworld)",
                tech: "C++ Low-Latency Trading / Global Clearing"
            },
            {
                name: "Standard Chartered Global Business Services",
                corridor: "OUTER_RING_ROAD",
                campus: "RMZ Ecoworld (Building 4A)",
                address: "Sarjapur-Marathahalli Ring Road",
                seats: 9000,
                sqft: 1020000,
                rent: 125,
                cam: 17,
                power: "72h DG Autonomy (Dual Grid)",
                transit: "Metro Phase 2A (Bellandur)",
                tech: "eBBS / Finacle Omnichannel Middleware"
            },
            {
                name: "Canara Bank Global Head Office",
                corridor: "CBD_MG_ROAD",
                campus: "Canara Bank Head Office Tower",
                address: "112, J.C. Road, Town Hall Circle",
                seats: 4500,
                sqft: 480000,
                rent: 175,
                cam: 22,
                power: "48h DG Autonomy (Municipal Grid)",
                transit: "Green Line Metro (KR Market / Chickpet)",
                tech: "TCS BaNCS Enterprise Core Banking"
            },
            {
                name: "State Bank of India (Local Head Office)",
                corridor: "CBD_MG_ROAD",
                campus: "SBI LHO Complex",
                address: "65, St. Mark's Road, Shanthala Nagar",
                seats: 3800,
                sqft: 420000,
                rent: 185,
                cam: 24,
                power: "48h DG Autonomy (Dual Feed)",
                transit: "Purple Line Metro (MG Road)",
                tech: "TCS BaNCS / SBI YONO Microservices Stack"
            },
            {
                name: "HDFC Bank (Karnataka Zonal Head Office)",
                corridor: "CBD_MG_ROAD",
                campus: "HDFC Bank House",
                address: "8/24, Richmond Road",
                seats: 2200,
                sqft: 250000,
                rent: 165,
                cam: 20,
                power: "48h DG Autonomy (Dual Feed)",
                transit: "Purple Line Metro (Trinity / MG Road)",
                tech: "Finacle 11.x Core Enterprise"
            },
            {
                name: "HSBC Technology & Services India",
                corridor: "WHITEFIELD",
                campus: "Prestige Shantiniketan",
                address: "ITPL Main Road, Whitefield",
                seats: 8000,
                sqft: 950000,
                rent: 85,
                cam: 14,
                power: "72h DG Autonomy (Dedicated Substation)",
                transit: "Purple Line Metro (Hoodi / Pattandur)",
                tech: "Universal Banking Platform / Digital Core"
            },
            {
                name: "Barclays Global Service Centre",
                corridor: "NORTH_MANYATA",
                campus: "Manyata Embassy Business Park",
                address: "Nagawara, Outer Ring Road, Hebbal",
                seats: 6000,
                sqft: 750000,
                rent: 92,
                cam: 15,
                power: "72h DG Autonomy (66kV Substation)",
                transit: "Blue Line Airport Metro (Nagawara)",
                tech: "Barclays Cloud Engine / Open Banking APIs"
            },
            {
                name: "Razorpay Technologies (Fintech Hub)",
                corridor: "KORAMANGALA_HSR",
                campus: "The Grove by SJR",
                address: "1st Block, Koramangala",
                seats: 3000,
                sqft: 300000,
                rent: 140,
                cam: 16,
                power: "48h DG Autonomy",
                transit: "Yellow Line (Silk Board / Jayadeva)",
                tech: "Custom UPI Switch & Neo-banking APIs"
            }
        ];

        function renderFacilities(list) {
            const container = document.getElementById('facility-container');
            container.innerHTML = '';
            list.forEach(f => {
                const card = document.createElement('div');
                card.className = 'facility-card';
                card.innerHTML = `
                    <div class="facility-header">
                        <div>
                            <div class="facility-name">${f.name}</div>
                            <div class="facility-corridor">${f.corridor.replace('_', ' ')} // ${f.campus}</div>
                        </div>
                    </div>
                    <div class="facility-detail">📍 ${f.address}</div>
                    <div class="facility-detail">👥 Capacity: <strong class="mono" style="color: #fff;">${f.seats.toLocaleString()} seats</strong> (${f.sqft.toLocaleString()} sq ft)</div>
                    <div class="facility-detail">🏢 Lease: <span class="mono">₹${f.rent}/sq ft</span> + <span class="mono">₹${f.cam}/sq ft CAM</span></div>
                    <div class="facility-detail">⚡ ${f.power}</div>
                    <div class="facility-detail">🚇 ${f.transit}</div>
                    <div style="margin-top: 10px;">
                        <span class="tag-pill" style="color: var(--cyan);">${f.tech.split('/')[0]}</span>
                        <span class="tag-pill" style="color: var(--emerald);">RBI LOCALIZED</span>
                        <span class="tag-pill" style="color: var(--purple);">DPDP READY</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterCorridor(corridor, btn) {
            document.querySelectorAll('#tab-facilities .tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (corridor === 'ALL') {
                renderFacilities(facilitiesData);
            } else {
                renderFacilities(facilitiesData.filter(f => f.corridor === corridor));
            }
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
        }

        function calculateBlueprint() {
            const seats = parseInt(document.getElementById('sim-seats').value);
            document.getElementById('seats-display').innerText = seats.toLocaleString();

            const corridor = document.getElementById('sim-corridor').value;
            const grade = document.getElementById('sim-grade').value;

            const sqft = seats * 90;
            const rentMap = {
                OUTER_RING_ROAD: [125, 17.5],
                WHITEFIELD: [85, 14],
                CBD_MG_ROAD: [170, 22],
                NORTH_MANYATA: [95, 15],
                ELECTRONIC_CITY: [60, 12],
                KORAMANGALA_HSR: [135, 16.5]
            };
            const [rent, cam] = rentMap[corridor] || [120, 16];

            const fitoutMap = {
                ULTRA_GRADE_A_FINANCIAL: 4200,
                STANDARD_GRADE_A: 3300,
                VALUE_COMMERCIAL: 2400
            };
            const fitoutPsf = fitoutMap[grade];

            const civilCr = (sqft * fitoutPsf) / 10000000;
            const elecCr = (sqft * 1400) / 10000000;
            const itCr = (seats * 120000 + sqft * 600) / 10000000;
            const capexCr = civilCr + elecCr + itCr + 2.5;
            const capexUsd = (capexCr * 10) / 83;

            const rentCr = (sqft * rent * 12) / 10000000;
            const camCr = (sqft * cam * 12) / 10000000;
            const utilCr = (seats * 45000) / 10000000;
            const bwCr = (seats * 25000) / 10000000;
            const payrollCr = (seats * 1850000) / 10000000;
            const secCr = (seats * 32000) / 10000000;
            const opexCr = rentCr + camCr + utilCr + bwCr + payrollCr + secCr;
            const opexUsd = (opexCr * 10) / 83;

            document.getElementById('out-sqft').innerText = sqft.toLocaleString() + ' sq ft';
            document.getElementById('out-civil').innerText = '₹' + civilCr.toFixed(2) + ' Cr';
            document.getElementById('out-elec').innerText = '₹' + elecCr.toFixed(2) + ' Cr';
            document.getElementById('out-it').innerText = '₹' + itCr.toFixed(2) + ' Cr';
            document.getElementById('out-capex').innerText = '₹' + capexCr.toFixed(2) + ' Cr (~$' + capexUsd.toFixed(2) + 'M)';

            document.getElementById('out-rent').innerText = '₹' + rentCr.toFixed(2) + ' Cr / yr';
            document.getElementById('out-cam').innerText = '₹' + camCr.toFixed(2) + ' Cr / yr';
            document.getElementById('out-payroll').innerText = '₹' + payrollCr.toFixed(2) + ' Cr / yr';
            document.getElementById('out-opex').innerText = '₹' + opexCr.toFixed(2) + ' Cr (~$' + opexUsd.toFixed(2) + 'M)';
        }

        function toggleCheck(id) {
            const el = document.getElementById(id);
            if (event.target !== el) {
                el.checked = !el.checked;
                runAudit();
            }
        }

        function runAudit() {
            let score = 100;
            const remediations = [];

            if (!document.getElementById('c1').checked) {
                score -= 35;
                remediations.push("Partition databases: relocate all transaction ledgers to AWS Mumbai (ap-south-1) / Azure Pune. Restrict overseas nodes to 24h ephemeral cache.");
            }
            if (!document.getElementById('c2').checked) {
                score -= 20;
                remediations.push("Deploy DPDP 2023 Consent Manager layer and formally designate Bengaluru-based Data Protection Officer.");
            }
            if (!document.getElementById('c3').checked) {
                score -= 20;
                remediations.push("Implement automated SIEM alert escalation to CERT-In (incident@cert-in.org.in) adhering strictly to the statutory 6-hour window.");
            }
            if (!document.getElementById('c4').checked) {
                score -= 15;
                remediations.push("Synchronize all core switches, firewalls, and server NTPs with National Physical Laboratory (time1.nplindia.org).");
            }
            if (!document.getElementById('c5').checked) {
                score -= 10;
                remediations.push("Upgrade NAS storage to preserve continuous, uncompressed 90-day CCTV recordings across strongroom perimeters.");
            }

            document.getElementById('audit-score').innerText = score;
            const statusEl = document.getElementById('audit-status');
            const remBox = document.getElementById('remediation-box');
            const remList = document.getElementById('remediation-list');

            if (score >= 95) {
                statusEl.innerText = "REGULATORY STATUS: FULLY COMPLIANT";
                statusEl.style.color = "var(--emerald)";
                document.getElementById('audit-score').style.color = "var(--emerald)";
                remBox.style.display = "none";
            } else if (score >= 70) {
                statusEl.innerText = "REGULATORY STATUS: PARTIAL REMEDIATION REQUIRED";
                statusEl.style.color = "var(--amber)";
                document.getElementById('audit-score').style.color = "var(--amber)";
                remBox.style.display = "block";
            } else {
                statusEl.innerText = "REGULATORY STATUS: NON-COMPLIANT (PENAL RISK)";
                statusEl.style.color = "var(--rose)";
                document.getElementById('audit-score').style.color = "var(--rose)";
                remBox.style.display = "block";
            }

            remList.innerHTML = '';
            remediations.forEach(r => {
                const li = document.createElement('li');
                li.innerText = r;
                remList.appendChild(li);
            });
        }

        // Initial setup
        renderFacilities(facilitiesData);
        calculateBlueprint();
    </script>
</body>
</html>
"""
