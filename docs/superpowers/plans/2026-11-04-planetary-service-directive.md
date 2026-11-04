# Universal Planetary Service Ecosystem & Master Directive 2027 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify the Universal Planetary Service Ecosystem architecture, author the comprehensive Master Operational Directive (`UNIVERSAL_MASTER_DIRECTIVE_2027.md`), integrate programmatic directive validation and CLI commands in `src/omniverse`, and verify with automated unit tests.

**Architecture:** A dual-core operational model connecting 12 planetary services (6 Core Alpha commercial services, 6 Core Beta resilience services) with a 7-division autonomous agent workforce, protected by cryptographic Human-in-the-Loop gates. The directive is available both as a standalone portable markdown prompt and through the `omniverse` CLI.

**Tech Stack:** Python 3.11+, Click/Typer/CLI, Pydantic/dataclasses, Pytest, Markdown.

**Spec:** `docs/superpowers/specs/2026-11-04-planetary-service-directive-design.md`

## Global Constraints

- Absolute evidence over assertions: 100% green pytest verification before claiming task completion.
- No live capital movement, trade placement, or live message broadcast without explicit human confirmation (`HITL_TOKEN`).
- Strict dual-ledger accounting: distinguish pipeline value from settled deposits.
- Full backwards compatibility with existing 205 passing unit tests.

---

### Task 1: Core Directive Implementation & Schema Validator

**Files:**
- Create: `src/omniverse/core/directive.py`
- Test: `tests/test_directive.py`

**Interfaces:**
- Produces:
  - `GlobalService(id: str, name: str, core: str, description: str, cli_command: str)`
  - `AgentPersona(role: str, division: str, mandate: str, bound: str)`
  - `MasterDirectiveRegistry`:
    - `get_services() -> list[GlobalService]`
    - `get_personas() -> list[AgentPersona]`
    - `get_service(service_id: str) -> GlobalService | None`
    - `validate_integrity() -> dict[str, Any]`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_directive.py
import pytest
from omniverse.core.directive import MasterDirectiveRegistry, GlobalService, AgentPersona

def test_registry_services_count():
    services = MasterDirectiveRegistry.get_services()
    assert len(services) == 12
    alpha_services = [s for s in services if s.core == "ALPHA"]
    beta_services = [s for s in services if s.core == "BETA"]
    assert len(alpha_services) == 6
    assert len(beta_services) == 6

def test_registry_personas_count():
    personas = MasterDirectiveRegistry.get_personas()
    assert len(personas) == 7
    roles = {p.role for p in personas}
    assert "Supreme Chief Architect" in roles
    assert "Aether Resilience Commander" in roles

def test_registry_integrity_check():
    health = MasterDirectiveRegistry.validate_integrity()
    assert health["valid"] is True
    assert health["total_services"] == 12
    assert health["total_personas"] == 7
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_directive.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'omniverse.core.directive'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/omniverse/core/directive.py
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class GlobalService:
    id: str
    name: str
    core: str
    description: str
    cli_command: str

@dataclass(frozen=True)
class AgentPersona:
    role: str
    division: str
    mandate: str
    bound: str

SERVICES: list[GlobalService] = [
    GlobalService("SVC-ALPHA-01", "Local SMB Autonomous Growth Kits", "ALPHA", "Automated audits, local SEO, and WhatsApp growth kits", "omniverse generate-kit"),
    GlobalService("SVC-ALPHA-02", "10-Unit Commerce Matrix", "ALPHA", "Multi-provider payment routing (Stripe/UPI/Web3/SEPA) with dual-ledger accounting", "omniverse commerce status"),
    GlobalService("SVC-ALPHA-03", "Autonomous Micro-SaaS Factory", "ALPHA", "Declarative vertical SaaS scaffolding, testing, and containerization", "omniverse saas build"),
    GlobalService("SVC-ALPHA-04", "Deterministic B2B Prospecting", "ALPHA", "Public registry scraping and decision-maker lead verification", "omniverse scan-prospects"),
    GlobalService("SVC-ALPHA-05", "Quantitative Risk & Portfolio Lab", "ALPHA", "Backtesting, Monte Carlo simulation, and VaR risk boundary checks", "omniverse backtest"),
    GlobalService("SVC-ALPHA-06", "Real-Time Market Volatility Radar", "ALPHA", "Cross-asset volatility tracking and paper trading execution", "omniverse market-radar"),
    GlobalService("SVC-BETA-07", "Aether Geospatial Multi-Hazard Radar", "BETA", "Planetary WGS84 hazard scoring for flood, seismic, cyclone, heat", "omniverse aether-risk"),
    GlobalService("SVC-BETA-08", "Satellite SAR & Telemetry Processing", "BETA", "Cloud-penetrating Earth observation analysis and disaster boundaries", "omniverse sar-process"),
    GlobalService("SVC-BETA-09", "Emergency Relief & Shelter Logistics", "BETA", "Linear-programming relief supply routing and shelter allocations", "omniverse aether-logistics"),
    GlobalService("SVC-BETA-10", "Critical Infrastructure Vulnerability", "BETA", "Single-point-of-failure modeling for power, water, and telecom", "omniverse infra-vuln"),
    GlobalService("SVC-BETA-11", "BFT Swarm Mesh Consensus", "BETA", "Byzantine fault tolerant P2P gossip mesh and actor consensus", "omniverse swarm status"),
    GlobalService("SVC-BETA-12", "Continuous Self-Healing Autonomic Ops", "BETA", "24/7 background worker daemons with automated circuit breakers", "omniverse ops heal"),
]

PERSONAS: list[AgentPersona] = [
    AgentPersona("Supreme Chief Architect", "Command", "Master governance and platform orchestration", "Human-in-the-loop ratification required for live production change"),
    AgentPersona("Commercial Agency Director", "Core Alpha", "Client acquisition, outreach funnels, revenue generation", "Cannot issue client invoices without settlement ledger confirmation"),
    AgentPersona("Quantitative & Financial Governor", "Core Alpha", "Algorithmic intelligence and risk envelope enforcement", "Maximum drawdown capped at 20.0%; cannot execute real orders without HITL_TOKEN"),
    AgentPersona("Aether Resilience Commander", "Core Beta", "Geospatial hazard modeling and relief distribution", "Open data outputs must adhere to verified scientific standard"),
    AgentPersona("Swarm Mesh Operator", "Core Beta", "P2P actor network monitoring and gossip transport", "Isolates malfunctioning swarm nodes automatically"),
    AgentPersona("Security & Cryptographic Arbiter", "Governance", "Air-gapped security, zero-trust tokens, audit trails", "Inviolable veto power over unauthenticated actions"),
    AgentPersona("Open-Source Standards Fellow", "Governance", "Test integrity, documentation quality, licensing compliance", "100% green test suite gatekeeper"),
]

class MasterDirectiveRegistry:
    @staticmethod
    def get_services() -> list[GlobalService]:
        return SERVICES

    @staticmethod
    def get_personas() -> list[AgentPersona]:
        return PERSONAS

    @staticmethod
    def get_service(service_id: str) -> GlobalService | None:
        for s in SERVICES:
            if s.id == service_id:
                return s
        return None

    @staticmethod
    def validate_integrity() -> dict[str, Any]:
        services = MasterDirectiveRegistry.get_services()
        personas = MasterDirectiveRegistry.get_personas()
        alpha = [s for s in services if s.core == "ALPHA"]
        beta = [s for s in services if s.core == "BETA"]
        valid = (len(services) == 12) and (len(alpha) == 6) and (len(beta) == 6) and (len(personas) == 7)
        return {
            "valid": valid,
            "total_services": len(services),
            "alpha_services": len(alpha),
            "beta_services": len(beta),
            "total_personas": len(personas),
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_directive.py -v`  
Expected: PASS (3 tests passed)

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/core/directive.py tests/test_directive.py
git commit -m "feat(directive): add master directive registry and schema validator"
```

---

### Task 2: CLI Integration for Master Directive

**Files:**
- Modify: `src/omniverse/cli.py`
- Test: `tests/test_directive_cli.py`

**Interfaces:**
- Consumes: `MasterDirectiveRegistry` from `src/omniverse/core/directive.py`
- Produces: `omniverse directive [--summary] [--json]` CLI command

- [ ] **Step 1: Write the failing test**

```python
# tests/test_directive_cli.py
from typer.testing import CliRunner
from omniverse.cli import app

runner = CliRunner()

def test_cli_directive_summary():
    result = runner.invoke(app, ["directive", "--summary"])
    assert result.exit_code == 0
    assert "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC" in result.output
    assert "12 Planetary Services" in result.output
    assert "7 Executive Agent Roles" in result.output

def test_cli_directive_json():
    result = runner.invoke(app, ["directive", "--json"])
    assert result.exit_code == 0
    assert '"valid": true' in result.output.lower() or '"valid":true' in result.output.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_directive_cli.py -v`  
Expected: FAIL with `Error: No such command 'directive'`

- [ ] **Step 3: Implement CLI command in `src/omniverse/cli.py`**

Add the `directive` command to `src/omniverse/cli.py`:

```python
import json
from omniverse.core.directive import MasterDirectiveRegistry

@app.command("directive")
def directive_cmd(
    summary: bool = typer.Option(True, "--summary", "-s", help="Show directive summary"),
    as_json: bool = typer.Option(False, "--json", "-j", help="Output directive status as JSON"),
):
    """Inspect and validate the Universal Master Directive and 12-Service Taxonomy."""
    integrity = MasterDirectiveRegistry.validate_integrity()
    if as_json:
        typer.echo(json.dumps(integrity, indent=2))
        return

    typer.secho("================================================================================", fg=typer.colors.CYAN)
    typer.secho("   CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC — MASTER DIRECTIVE   ", fg=typer.colors.BRIGHT_GREEN, bold=True)
    typer.secho("================================================================================", fg=typer.colors.CYAN)
    typer.echo(f"Operational Horizon: 2027 Edition | Planetary Grid Active")
    typer.echo(f"Integrity Status   : {'VALID (100% HEALTHY)' if integrity['valid'] else 'INVALID'}")
    typer.echo(f"Service Taxonomy   : 12 Planetary Services (Core Alpha: {integrity['alpha_services']} | Core Beta: {integrity['beta_services']})")
    typer.echo(f"Executive Workforce: 7 Executive Agent Roles Active\n")

    typer.secho("[CORE ALPHA: COMMERCIAL ENGINE]", fg=typer.colors.YELLOW, bold=True)
    for svc in MasterDirectiveRegistry.get_services():
        if svc.core == "ALPHA":
            typer.echo(f"  * {svc.id}: {svc.name} -> `{svc.cli_command}`")

    typer.secho("\n[CORE BETA: AETHER RESILIENCE FABRIC]", fg=typer.colors.BLUE, bold=True)
    for svc in MasterDirectiveRegistry.get_services():
        if svc.core == "BETA":
            typer.echo(f"  * {svc.id}: {svc.name} -> `{svc.cli_command}`")

    typer.secho("\n[EXECUTIVE AGENT ROLES]", fg=typer.colors.MAGENTA, bold=True)
    for p in MasterDirectiveRegistry.get_personas():
        typer.echo(f"  * {p.role} ({p.division}): {p.mandate}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_directive_cli.py -v`  
Expected: PASS (2 tests passed)

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/cli.py tests/test_directive_cli.py
git commit -m "feat(cli): add directive CLI command with summary and JSON formatting"
```

---

### Task 3: Author the Monumental Master Directive Document (`UNIVERSAL_MASTER_DIRECTIVE_2027.md`)

**Files:**
- Create: `UNIVERSAL_MASTER_DIRECTIVE_2027.md`
- Test: `tests/test_directive_docs.py`

**Interfaces:**
- Produces: Complete master operational prompt markdown document.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_directive_docs.py
from pathlib import Path
from omniverse.core.directive import MasterDirectiveRegistry

def test_universal_master_directive_file_exists():
    path = Path("UNIVERSAL_MASTER_DIRECTIVE_2027.md")
    assert path.is_file(), "UNIVERSAL_MASTER_DIRECTIVE_2027.md must exist in root"
    content = path.read_text(encoding="utf-8")
    assert "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC" in content
    assert "THE SUPREME UNIVERSAL 2027 DIRECTIVE" in content

    # Verify all 12 services are explicitly detailed in document
    for svc in MasterDirectiveRegistry.get_services():
        assert svc.name in content, f"Service {svc.name} must be documented"

    # Verify all 7 agent personas are explicitly detailed in document
    for persona in MasterDirectiveRegistry.get_personas():
        assert persona.role in content, f"Persona {persona.role} must be documented"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_directive_docs.py -v`  
Expected: FAIL (`AssertionError: UNIVERSAL_MASTER_DIRECTIVE_2027.md must exist in root`)

- [ ] **Step 3: Author `UNIVERSAL_MASTER_DIRECTIVE_2027.md`**

Write the definitive, supreme master prompt document containing:
- Complete ASCII Header & Planetary Mission Declaration.
- The Inviolable Operational Constitution (epistemological guardrails, HITL security, dual-ledger accounting).
- Full specifications for all 12 Global Services.
- Full cognitive instructions and bounds for all 7 Agent Roles.
- Universal Agent Harness Instructions (copy-paste blocks for Antigravity, Claude, Codex, headless runners).
- Complete CLI recipes and emergency runbooks.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_directive_docs.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add UNIVERSAL_MASTER_DIRECTIVE_2027.md tests/test_directive_docs.py
git commit -m "docs(directive): create UNIVERSAL_MASTER_DIRECTIVE_2027 monumental master prompt"
```

---

### Task 4: Synchronize `PROMPT_NO1_2027.md` and Documentation

**Files:**
- Modify: `PROMPT_NO1_2027.md`
- Test: `tests/test_prompt_sync.py`

**Interfaces:**
- Consumes: `UNIVERSAL_MASTER_DIRECTIVE_2027.md`
- Produces: Updated `PROMPT_NO1_2027.md` with direct reference and quick invocation tokens.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_prompt_sync.py
from pathlib import Path

def test_prompt_no1_sync():
    path = Path("PROMPT_NO1_2027.md")
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "UNIVERSAL_MASTER_DIRECTIVE_2027.md" in content
    assert "12-Unit Planetary Service Matrix" in content or "12 Planetary Services" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_prompt_sync.py -v`  
Expected: FAIL

- [ ] **Step 3: Update `PROMPT_NO1_2027.md`**

Integrate the reference to `UNIVERSAL_MASTER_DIRECTIVE_2027.md` and the 12 Planetary Services taxonomy.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_prompt_sync.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add PROMPT_NO1_2027.md tests/test_prompt_sync.py
git commit -m "docs(prompt): sync PROMPT_NO1_2027 with universal master directive"
```

---

### Task 5: Full Regression Testing & System Health Validation

**Files:**
- All tests in `tests/`

- [ ] **Step 1: Run complete test suite**

Run: `pytest -v`  
Expected: All 210+ tests pass with 0 failures and 0 regressions.

- [ ] **Step 2: Verify CLI status and directive commands**

Run: `python -m omniverse.cli status`  
Run: `python -m omniverse.cli directive --summary`  
Run: `python -m omniverse.cli directive --json`  
Expected: Clean exit code 0 and valid JSON/terminal outputs.
