# 🤖 Reddit Community Launch Kits

---

## 1. Post for `r/LocalLLaMA`
**Title:** `I built an open-source MCP tool server (JSON-RPC 2.0 stdio) for local agents and Claude Desktop – OMEGA-MCP`

**Body:**
Hey r/LocalLLaMA,

With Model Context Protocol (MCP) quickly becoming the open standard for tool calling, I wanted a fast, zero-bloat Python package that exposes production-grade domain tools rather than toy calculator functions.

I packaged and published **OMEGA-MCP**:
* **Repo:** https://github.com/AdityaMehra007/cashflow-infinity-omniverse
* **Install:** `pip install omega-mcp`
* **Protocol:** Pure JSON-RPC 2.0 over `stdio`. Works seamlessly with Claude Desktop, Cursor, and local agent harnesses.

Included tools out-of-the-box:
* `bengaluru_startup_radar`: Queries venture intelligence on 1,000+ tech companies and active hiring.
* `generate_growth_kit`: Builds B2B copy, cold outreach, and conversion hooks for any niche.
* `evaluate_resilience_risk`: Geospatial risk index scoring.
* `double_entry_ledger_clearing`: Deterministic transactional accounting with mathematical zero-leak verification.

CLI test:
```bash
omega-mcp call bengaluru_startup_radar -a "{'query':'Sarvam'}"
```

Feedback and PRs welcome!

---

## 2. Post for `r/Python`
**Title:** `[Project] omega-mcp: Lightweight Model Context Protocol (MCP) CLI & Server with Click and Pydantic`

**Body:**
Hi everyone,

I wanted to share a project I built implementing Anthropic's Model Context Protocol (MCP) in pure Python 3.10+:

**Features:**
- Clean decorator-based tool registration (`@register_tool`)
- Automatic JSON-RPC 2.0 stdio multiplexing
- Click CLI interface with built-in test runner (`omega-mcp call <tool_name> -a <args>`)
- 100% test coverage with Pytest and strict PyPI packaging (`twine check` approved)

GitHub: https://github.com/AdityaMehra007/cashflow-infinity-omniverse
Package: `pip install omega-mcp`

Looking forward to your thoughts on the architecture!
