# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""PROJECT GODMODE / ATLAS: Career OS Interactive Dashboard Template."""

from omniverse.modules.career.engine import CareerOSEngine


def render_career_os_html() -> str:
    engine = CareerOSEngine()
    profile = engine.get_profile()
    opps = engine.list_opportunities()
    demo_opp = opps[0] if opps else None

    # Pre-render opportunity card
    opp_cards_html = ""
    for o in opps:
        opp_cards_html += f"""
        <div class="opp-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 700; color: #fff;">{o.role_title}</h3>
                    <div style="font-size: 13px; color: var(--accent-cyan);">{o.company}</div>
                </div>
                <span class="badge badge-status">{o.status.value}</span>
            </div>
            <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">📍 {o.location} | 💰 {o.salary_range}</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 14px; line-height: 1.4;"><em>"{o.notes}"</em></div>
            <div class="opp-actions">
                <button class="btn btn-sm" onclick="runAnalysis('{o.id}')">⚡ Analyze JD</button>
                <button class="btn btn-sm btn-outline" onclick="runTailor('{o.id}')">📄 Tailor Resume</button>
                <button class="btn btn-sm btn-outline" onclick="runInterviewPack('{o.id}')">🎯 Prep STAR</button>
            </div>
        </div>
        """

    ach_html = ""
    for a in profile.achievements:
        ach_html += f"""
        <div class="ach-card">
            <div style="font-weight: 700; color: var(--accent-green); margin-bottom: 4px;">✓ {a.title}</div>
            <div style="font-size: 13px; color: #e2e8f0; margin-bottom: 6px;">Impact: <strong>{a.impact_metric}</strong></div>
            <div style="font-size: 11px; color: var(--text-muted);">Skills: {', '.join(a.skills_used)}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATLAS // GODMODE Career OS</title>
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
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }}
        .navbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 32px;
            background: rgba(11, 19, 41, 0.9);
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
        .nav-links {{ display: flex; gap: 8px; }}
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
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px 24px;
        }}
        .hero {{ margin-bottom: 28px; }}
        .hero h1 {{
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #fff 40%, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .hero p {{ color: var(--text-muted); font-size: 15px; }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        @media (max-width: 900px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        .card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 14px;
            padding: 24px;
        }}
        .card h2 {{
            font-size: 18px;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .opp-card {{
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 14px;
            transition: all 0.2s;
        }}
        .opp-card:hover {{
            border-color: rgba(6, 182, 212, 0.4);
            transform: translateY(-2px);
        }}
        .ach-card {{
            background: rgba(3, 7, 18, 0.7);
            border: 1px solid var(--surface-border);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}
        .badge-status {{ background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border: 1px solid rgba(6, 182, 212, 0.4); }}
        .badge-match {{ background: rgba(16, 185, 129, 0.2); color: var(--accent-green); border: 1px solid rgba(16, 185, 129, 0.4); }}
        .btn {{
            background: var(--accent-cyan);
            color: #030712;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            border: none;
            border-radius: 6px;
            padding: 8px 14px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn:hover {{
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
        }}
        .btn-outline {{
            background: transparent;
            color: var(--text-main);
            border: 1px solid var(--surface-border);
        }}
        .btn-outline:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--accent-cyan);
        }}
        .opp-actions {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .result-panel {{
            background: rgba(3, 7, 18, 0.9);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            padding: 20px;
            margin-top: 16px;
            font-size: 13px;
            line-height: 1.5;
            display: none;
        }}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="brand">
            <span>ATLAS</span>
            <span class="brand-badge">CAREER OS // GODMODE</span>
        </div>
        <nav class="nav-links">
            <a href="/cockpit" class="nav-link">🚀 Cockpit</a>
            <a href="/career" class="nav-link active">💼 Career OS</a>
            <a href="/saas" class="nav-link">🏢 SaaS Fleet</a>
            <a href="/apex" class="nav-link">⚡ Apex Singularity</a>
            <a href="/docs" class="nav-link">📖 API Docs</a>
        </nav>
    </header>

    <main class="container">
        <div class="hero">
            <h1>GODMODE Career OS & Intelligence Platform</h1>
            <p>Turn career objectives into structured, evidence-backed pipelines with 100% factual accuracy and human approval gates.</p>
        </div>

        <div class="grid-2">
            <!-- LEFT: PROFILE & ACHIEVEMENTS -->
            <div>
                <div class="card" style="margin-bottom: 24px;">
                    <h2>
                        <span>Candidate Profile</span>
                        <span class="badge badge-match">VERIFIED</span>
                    </h2>
                    <div style="font-size: 18px; font-weight: 700; margin-bottom: 4px;">{profile.full_name}</div>
                    <div style="font-size: 13px; color: var(--accent-cyan); margin-bottom: 12px;">{profile.headline}</div>
                    <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">{profile.summary}</div>
                    <div style="font-size: 12px; margin-bottom: 12px;">
                        <strong>Target Minimum Compensation:</strong> <span style="color: var(--accent-green); font-family: 'JetBrains Mono';">${profile.target_compensation_min_usd:,.0f} USD</span>
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                        {' '.join(f'<span class="badge" style="background: rgba(255,255,255,0.05);">{s}</span>' for s in profile.skills[:8])}
                    </div>
                </div>

                <div class="card">
                    <h2>
                        <span>Verified Achievement Evidence</span>
                        <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-green);">{len(profile.achievements)} VERIFIED</span>
                    </h2>
                    {ach_html}
                </div>
            </div>

            <!-- RIGHT: OPPORTUNITIES & WORKFLOW DOCK -->
            <div>
                <div class="card" style="margin-bottom: 24px;">
                    <h2>
                        <span>Opportunity Pipeline</span>
                        <span class="badge badge-status">{len(opps)} ACTIVE</span>
                    </h2>
                    {opp_cards_html}
                </div>

                <!-- LIVE EXECUTION RESULT DOCK -->
                <div class="card">
                    <h2>
                        <span>Intelligence & Execution Dock</span>
                        <span id="dock-status" class="badge badge-status">READY</span>
                    </h2>
                    <div id="dock-content" style="color: var(--text-muted); font-size: 13px;">
                        Click <strong>Analyze JD</strong>, <strong>Tailor Resume</strong>, or <strong>Prep STAR</strong> on any opportunity above to run real-time deterministic workflows.
                    </div>
                    <div id="dock-box" class="result-panel"></div>
                </div>
            </div>
        </div>
    </main>

    <script>
        async function runAnalysis(oppId) {{
            const box = document.getElementById('dock-box');
            const status = document.getElementById('dock-status');
            status.innerText = "ANALYZING...";
            box.style.display = 'block';
            box.innerHTML = "<em>Parsing job description and computing match matrix...</em>";

            try {{
                const res = await fetch(`/api/v1/career/opportunities/${{oppId}}/analyze`, {{ method: 'POST' }});
                const data = await res.json();
                status.innerText = "MATCH " + data.match_score_pct + "%";
                box.innerHTML = `
                    <div style="font-weight: 700; color: var(--accent-green); font-size: 16px; margin-bottom: 8px;">Job Description Match Analysis: ${{data.match_score_pct}}%</div>
                    <div style="margin-bottom: 8px;"><strong>Matched Competencies:</strong> ${{data.matched_skills.join(', ')}}</div>
                    <div style="margin-bottom: 8px; color: var(--accent-amber);"><strong>Identified Growth Edges:</strong> ${{data.skill_gaps.join(', ')}}</div>
                    <div style="margin-top: 12px; font-weight: 700;">Suggested Interview Angles:</div>
                    <ul style="padding-left: 20px; margin-top: 6px;">
                        ${{data.suggested_interview_questions.map(q => `<li style="margin-bottom: 4px;">${{q}}</li>`).join('')}}
                    </ul>
                `;
            }} catch (err) {{
                box.innerHTML = `<span style="color: var(--accent-rose);">Error: ${{err.message}}</span>`;
            }}
        }}

        async function runTailor(oppId) {{
            const box = document.getElementById('dock-box');
            const status = document.getElementById('dock-status');
            status.innerText = "TAILORING...";
            box.style.display = 'block';
            box.innerHTML = "<em>Mapping verified achievements to job requirements with 0 hallucination...</em>";

            try {{
                const res = await fetch(`/api/v1/career/opportunities/${{oppId}}/tailor-resume`, {{ method: 'POST' }});
                const data = await res.json();
                status.innerText = "TAILORED FACTUAL";
                box.innerHTML = `
                    <div style="font-weight: 700; color: var(--accent-cyan); font-size: 16px; margin-bottom: 8px;">Factually Grounded Tailored Resume (${{data.company}})</div>
                    <div style="font-style: italic; color: #cbd5e1; margin-bottom: 12px;">"${{data.tailored_summary}}"</div>
                    <div style="font-weight: 700; margin-bottom: 6px;">Requirement-Mapped Evidence:</div>
                    ${{data.aligned_bullets.map(b => `
                        <div style="background: rgba(255,255,255,0.03); padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid var(--accent-green);">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Requirement: ${{b.requirement}}</div>
                            <div style="margin-top: 2px;">• ${{b.bullet_point}}</div>
                        </div>
                    `).join('')}}
                `;
            }} catch (err) {{
                box.innerHTML = `<span style="color: var(--accent-rose);">Error: ${{err.message}}</span>`;
            }}
        }}

        async function runInterviewPack(oppId) {{
            const box = document.getElementById('dock-box');
            const status = document.getElementById('dock-status');
            status.innerText = "GENERATING STAR...";
            box.style.display = 'block';
            box.innerHTML = "<em>Assembling STAR response frameworks from verified candidate achievements...</em>";

            try {{
                const res = await fetch(`/api/v1/career/opportunities/${{oppId}}/interview-pack`, {{ method: 'POST' }});
                const data = await res.json();
                status.innerText = "STAR PACK READY";
                box.innerHTML = `
                    <div style="font-weight: 700; color: var(--accent-purple); font-size: 16px; margin-bottom: 8px;">STAR Interview Preparation Framework (${{data.role_title}})</div>
                    ${{data.behavioral_star_frameworks.map(s => `
                        <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                            <div style="font-weight: 700; color: var(--accent-cyan); margin-bottom: 6px;">❓ ${{s.question}}</div>
                            <div style="font-size: 12px; margin-bottom: 4px;"><strong>S (Situation):</strong> ${{s.situation}}</div>
                            <div style="font-size: 12px; margin-bottom: 4px;"><strong>T (Task):</strong> ${{s.task}}</div>
                            <div style="font-size: 12px; margin-bottom: 4px;"><strong>A (Action):</strong> ${{s.action}}</div>
                            <div style="font-size: 12px; color: var(--accent-green);"><strong>R (Result):</strong> ${{s.result}}</div>
                        </div>
                    `).join('')}}
                    <div style="font-weight: 700; margin-top: 12px;">Reverse-Interview Questions to Ask Leadership:</div>
                    <ul style="padding-left: 20px; margin-top: 6px;">
                        ${{data.company_reverse_interview_questions.map(q => `<li style="margin-bottom: 4px;">${{q}}</li>`).join('')}}
                    </ul>
                `;
            }} catch (err) {{
                box.innerHTML = `<span style="color: var(--accent-rose);">Error: ${{err.message}}</span>`;
            }}
        }}
    </script>
</body>
</html>
"""
