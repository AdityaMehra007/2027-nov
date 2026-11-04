# CASHFLOW INFINITY: OMNIVERSE Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete foundation for CASHFLOW INFINITY: OMNIVERSE — an autonomous revenue, market intelligence, agent workforce, and continuous operations platform in Python.

**Architecture:** A modular monolith in `src/omniverse` composed of core configuration and security boundaries, a revenue generation engine (micro-agency growth kit & CRM pipeline), financial & market intelligence schemas with paper trading simulation, agent workforce definitions, 24/7 background operations scheduler/worker, FastAPI command center, and native Antigravity workspace skills.

**Tech Stack:** Python 3.12+, SQLModel, SQLAlchemy, Pydantic v2, Pydantic Settings, FastAPI, Uvicorn, Pytest.

**Spec:** `docs/superpowers/specs/2026-11-04-cashflow-infinity-omniverse-design.md`

## Global Constraints

- Storage: SQLite with WAL mode locally (`data/omniverse.db`), architected for zero-code-change migration to PostgreSQL.
- Safety & Security: Hard-gated `SecurityGovernor` requiring human approval for live outbound communications, live money movement, and expenditure. No API keys hardcoded.
- Financial Accuracy: Strict segregation between unrealized Pipeline Value and confirmed Collected Revenue.
- Quality: Full test coverage with Pytest for all core models, revenue generators, backtester, scheduler, and API endpoints.

---

### Task 1: Project Setup, Core Configuration, Database Engine & Security Boundary

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `src/omniverse/__init__.py`
- Create: `src/omniverse/core/__init__.py`
- Create: `src/omniverse/core/config.py`
- Create: `src/omniverse/core/database.py`
- Create: `src/omniverse/core/security.py`
- Create: `src/omniverse/core/telemetry.py`
- Create: `tests/conftest.py`
- Create: `tests/test_core.py`

**Interfaces:**
- Produces:
  - `omniverse.core.config.OmniverseSettings`: settings singleton with `db_url`, `env`, `safety_budget_daily_usd`.
  - `omniverse.core.database.get_session()`: Generator yielding `sqlmodel.Session`.
  - `omniverse.core.database.init_db()`: Initializes tables.
  - `omniverse.core.security.SecurityGovernor`: `request_approval(action_type, details) -> bool`, `assert_permitted(action_type)`.
  - `omniverse.core.telemetry.EventBus`: `publish(event_name, payload) -> None`, `get_events() -> list[dict]`.

- [ ] **Step 1: Write the failing tests for core configuration, database, security, and telemetry**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `pyproject.toml`, `.gitignore`, `config.py`, `database.py`, `security.py`, `telemetry.py`**
- [ ] **Step 4: Run pytest to verify all tests pass**
- [ ] **Step 5: Commit core subsystem to git**

---

### Task 2: Revenue Engine — Models, Local Business Growth Kit & Offer Generator

**Files:**
- Create: `src/omniverse/modules/__init__.py`
- Create: `src/omniverse/modules/revenue/__init__.py`
- Create: `src/omniverse/modules/revenue/models.py`
- Create: `src/omniverse/modules/revenue/agency.py`
- Create: `tests/test_revenue_agency.py`

**Interfaces:**
- Consumes: `omniverse.core.database.get_session`, `omniverse.core.security.SecurityGovernor`.
- Produces:
  - `omniverse.modules.revenue.models.Lead`: SQLModel for prospective clients with stages (`NEW`, `QUALIFIED`, `CONTACTED`, `PROPOSAL_SENT`, `WON`, `LOST`).
  - `omniverse.modules.revenue.models.Offer`: SQLModel for packaged services and pricing.
  - `omniverse.modules.revenue.models.GrowthKit`: Pydantic model holding 10 social captions, WhatsApp catalog copy, 5 promotional hooks, and outreach pitch script.
  - `omniverse.modules.revenue.agency.GrowthKitGenerator.generate(business_name, niche, city) -> GrowthKit`.

- [ ] **Step 1: Write failing tests for GrowthKitGenerator and Revenue SQLModels**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement `models.py` and `agency.py`**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit revenue agency engine to git**

---

### Task 3: Lead CRM Pipeline, Proposal Generator & Payment Reconciliation

**Files:**
- Create: `src/omniverse/modules/revenue/pipeline.py`
- Create: `src/omniverse/modules/revenue/payments.py`
- Create: `tests/test_revenue_pipeline.py`

**Interfaces:**
- Consumes: `omniverse.modules.revenue.models.Lead`, `omniverse.modules.revenue.models.Invoice`, `omniverse.core.database.get_session`.
- Produces:
  - `omniverse.modules.revenue.pipeline.LeadPipeline`: `create_lead(...) -> Lead`, `advance_stage(lead_id, new_stage) -> Lead`, `get_pipeline_summary() -> dict`.
  - `omniverse.modules.revenue.payments.PaymentWorkflow`: `create_invoice(lead_id, amount_inr) -> Invoice`, `record_payment(invoice_id, reference) -> Invoice`, `get_financial_ledger() -> dict`.

- [ ] **Step 1: Write failing tests for LeadPipeline and PaymentWorkflow**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement `pipeline.py` and `payments.py`**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit lead pipeline and payments to git**

---

### Task 4: Intelligence & Quantitative Systems — Company Research & Paper Trading Engine

**Files:**
- Create: `src/omniverse/modules/intelligence/__init__.py`
- Create: `src/omniverse/modules/intelligence/models.py`
- Create: `src/omniverse/modules/intelligence/research.py`
- Create: `src/omniverse/modules/intelligence/quant_engine.py`
- Create: `tests/test_intelligence.py`

**Interfaces:**
- Consumes: `omniverse.core.database.get_session`, `omniverse.core.security.SecurityGovernor`.
- Produces:
  - `omniverse.modules.intelligence.models.CompanyProfile`: SQLModel for company intelligence.
  - `omniverse.modules.intelligence.models.PaperTrade`: SQLModel for simulated trading positions.
  - `omniverse.modules.intelligence.research.CompanyIntelligenceEngine`: `analyze_company(symbol, industry) -> CompanyProfile`.
  - `omniverse.modules.intelligence.quant_engine.Backtester`: `run_backtest(price_series, strategy_name) -> dict` (calculates CAGR, Sharpe ratio, Max Drawdown).
  - `omniverse.modules.intelligence.quant_engine.PaperTradingEngine`: `execute_order(symbol, direction, quantity, price) -> PaperTrade`.

- [ ] **Step 1: Write failing tests for Company research, Backtester, and PaperTradingEngine**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement `models.py`, `research.py`, and `quant_engine.py`**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit intelligence and quant subsystem to git**

---

### Task 5: Central Agent Workforce Hierarchy & Dispatcher

**Files:**
- Create: `src/omniverse/agents/__init__.py`
- Create: `src/omniverse/agents/base.py`
- Create: `src/omniverse/agents/executive.py`
- Create: `src/omniverse/agents/commercial.py`
- Create: `src/omniverse/agents/quant.py`
- Create: `tests/test_agents.py`

**Interfaces:**
- Consumes: `omniverse.core.security.SecurityGovernor`, `omniverse.core.telemetry.EventBus`.
- Produces:
  - `omniverse.agents.base.BaseAgent`: Abstract protocol with `role`, `division`, `execute_task(task_input) -> dict`.
  - `omniverse.agents.executive.ChiefRevenueArchitect`: Strategic business prioritizer.
  - `omniverse.agents.commercial.SalesDirector`: Lead scoring and proposal director.
  - `omniverse.agents.quant.QuantAnalyst`: Strategy verification and risk checker.
  - `omniverse.agents.base.AgentDispatcher`: Registers and dispatches work across virtual workforce.

- [ ] **Step 1: Write failing tests for Agent hierarchy and Dispatcher**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement `base.py`, `executive.py`, `commercial.py`, and `quant.py`**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit agent workforce to git**

---

### Task 6: 24/7 Operations — Scheduler, Background Worker & Health Watchdog

**Files:**
- Create: `src/omniverse/operations/__init__.py`
- Create: `src/omniverse/operations/health.py`
- Create: `src/omniverse/operations/scheduler.py`
- Create: `src/omniverse/operations/worker.py`
- Create: `tests/test_operations.py`

**Interfaces:**
- Consumes: `omniverse.core.database.get_session`, `omniverse.core.telemetry.EventBus`.
- Produces:
  - `omniverse.operations.health.HealthDiagnostics.run_diagnostics() -> dict`: Checks DB, storage, and memory.
  - `omniverse.operations.scheduler.OmniverseScheduler`: Registers recurring jobs (`hourly_health`, `pipeline_audit`, `daily_reconciliation`) and executes iterations.
  - `omniverse.operations.worker.WorkerDaemon`: Loop executor for autonomous background cycles with cost ceilings and rate limits.

- [ ] **Step 1: Write failing tests for HealthDiagnostics and Scheduler**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement `health.py`, `scheduler.py`, and `worker.py`**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit operations subsystem to git**

---

### Task 7: FastAPI Command Center REST API & Omniverse CLI

**Files:**
- Create: `src/omniverse/api/__init__.py`
- Create: `src/omniverse/api/routes/__init__.py`
- Create: `src/omniverse/api/routes/dashboard.py`
- Create: `src/omniverse/api/routes/revenue.py`
- Create: `src/omniverse/api/routes/intel.py`
- Create: `src/omniverse/api/routes/ops.py`
- Create: `src/omniverse/api/app.py`
- Create: `src/omniverse/cli.py`
- Create: `tests/test_api.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: All core, revenue, intelligence, agent, and operations modules.
- Produces:
  - `omniverse.api.app.create_app() -> FastAPI`: Exposes endpoints under `/api/v1/`.
  - `omniverse.cli.main()`: CLI commands (`status`, `generate-kit`, `leads`, `backtest`, `daemon`).

- [ ] **Step 1: Write failing tests for FastAPI endpoints and CLI commands**
- [ ] **Step 2: Run pytest to verify tests fail**
- [ ] **Step 3: Implement API routes, application factory, and CLI**
- [ ] **Step 4: Run pytest to verify tests pass**
- [ ] **Step 5: Commit API and CLI to git**

---

### Task 8: Antigravity Custom Skills Suite (`.agents/skills/`) & Sidecar Manifests

**Files:**
- Create: `.agents/skills/omniverse-command/SKILL.md`
- Create: `.agents/skills/omniverse-agency/SKILL.md`
- Create: `.agents/skills/omniverse-intel/SKILL.md`
- Create: `.agents/skills/omniverse-ops/SKILL.md`
- Create: `README.md`

**Interfaces:**
- Produces:
  - Markdown Antigravity skill definitions adhering to standard YAML frontmatter for IDE integration.
  - Full instructions for triggering micro-agency deliverables, running quant simulations, and viewing operations dashboard.

- [ ] **Step 1: Create all 4 Antigravity custom skills with YAML frontmatter and action guides**
- [ ] **Step 2: Create comprehensive `README.md` detailing startup instructions, architecture, and verification**
- [ ] **Step 3: Commit skills and documentation to git**

---

### Task 9: Full End-to-End Test Suite & Verification

**Files:**
- Create: `tests/test_e2e.py`

- [ ] **Step 1: Write end-to-end integration test creating a lead, generating a growth kit, advancing through proposal to paid invoice, running a quant backtest, and querying system health**
- [ ] **Step 2: Run full test suite (`pytest -v`) to verify 100% green passing tests**
- [ ] **Step 3: Run CLI status and growth kit generation verification commands**
- [ ] **Step 4: Commit full project verification to git**
