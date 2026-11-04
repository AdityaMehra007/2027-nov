# Autonomous Agency & Multi-Vertical Fulfillment Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete, autonomous AI client acquisition and multi-vertical fulfillment operating engine for CASHFLOW INFINITY: OMNIVERSE.

**Architecture:** A unified modular engine extending OMNIVERSE with an acquisition pipeline (leads, audits, instant demo pitches), multi-agent fulfillment factory (code, marketing, automation), automated QA governor, client portal packager, and FastAPI/CLI control surfaces.

**Tech Stack:** Python 3.11+, Pydantic v2, FastAPI, WebSockets, Pytest, Jinja2/HTML5/Tailwind/CSS, SQLite/PostgreSQL.

**Spec:** `docs/superpowers/specs/2026-11-04-autonomous-agency-fulfillment-design.md`

## Global Constraints
- Must integrate cleanly with OMNIVERSE core (`SecurityGovernor`, `Clearinghouse`, `LLMArbitrator`).
- Must maintain 100% test pass rate across all new and existing tests (116+ baseline).
- Strictly enforce distinction between speculative `Pipeline Value` and verified `Collected Revenue`.
- Strict pre-delivery QA validation for all autonomous deliverables.

---

### Task 1: Agency Data Models & Lifecycle State Machine
**Files:**
- Create: `src/omniverse/modules/agency/__init__.py`
- Create: `src/omniverse/modules/agency/models.py`
- Test: `tests/test_agency_models.py`

**Interfaces:**
- Produces: `Lead`, `AuditReport`, `PersonalizedPitch`, `JobOrder`, `Deliverable`, `ClientAccount`, `AgencyMetrics`, and associated enums (`ProspectArchetype`, `OrderStatus`, `ServiceType`).

- [ ] **Step 1: Write tests for Agency models, validation, and state serialization**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement models.py with Pydantic v2 and status transition rules**
- [ ] **Step 4: Run pytest to verify all model tests pass**
- [ ] **Step 5: Git commit task 1**

---

### Task 2: Lead Acquisition, Tech Auditor, & Pitch Generator
**Files:**
- Create: `src/omniverse/modules/agency/acquisition.py`
- Test: `tests/test_agency_acquisition.py`

**Interfaces:**
- Consumes: Models from `models.py`
- Produces: `LeadHunter` (scrapes/discovers leads across archetypes), `TechAuditor` (simulates/evaluates SEO, performance, and conversion leaks), `PitchGenerator` (builds tailored proposals with estimated revenue uplift).

- [ ] **Step 1: Write tests for LeadHunter, TechAuditor, and PitchGenerator**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement acquisition.py with deterministic audit scoring and pitch templating**
- [ ] **Step 4: Run pytest to verify all acquisition tests pass**
- [ ] **Step 5: Git commit task 2**

---

### Task 3: Autonomous Fulfillment Factory (Code, Marketing, Automation)
**Files:**
- Create: `src/omniverse/modules/agency/fulfillment/__init__.py`
- Create: `src/omniverse/modules/agency/fulfillment/code_factory.py`
- Create: `src/omniverse/modules/agency/fulfillment/marketing_factory.py`
- Create: `src/omniverse/modules/agency/fulfillment/automation_factory.py`
- Test: `tests/test_agency_fulfillment.py`

**Interfaces:**
- Consumes: `JobOrder`, `ServiceType`, `Deliverable`
- Produces: `CodeFactory.build_project()`, `MarketingFactory.build_campaign()`, `AutomationFactory.build_agent_bundle()`.

- [ ] **Step 1: Write tests for CodeFactory, MarketingFactory, AutomationFactory**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement CodeFactory (landing pages, full-stack scaffold, APIs)**
- [ ] **Step 4: Implement MarketingFactory (copywriting, SEO topic clusters, ad packs)**
- [ ] **Step 5: Implement AutomationFactory (AI agent scripts, MCP tools, bot webhooks)**
- [ ] **Step 6: Run pytest to verify all fulfillment factory tests pass**
- [ ] **Step 7: Git commit task 3**

---

### Task 4: QA & Verification Governor
**Files:**
- Create: `src/omniverse/modules/agency/qa_governor.py`
- Test: `tests/test_agency_qa_governor.py`

**Interfaces:**
- Consumes: `Deliverable`, `JobOrder`
- Produces: `QAGovernor.verify_deliverables()` returning quality score, syntax status, and pass/fail decision.

- [ ] **Step 1: Write tests for QAGovernor (syntax check, security scan, content validation)**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement QAGovernor with deterministic AST syntax checks, secret scanning, and quality metrics**
- [ ] **Step 4: Run pytest to verify QA governor tests pass**
- [ ] **Step 5: Git commit task 4**

---

### Task 5: Client Portal Engine & Settlement Packager
**Files:**
- Create: `src/omniverse/modules/agency/portal_engine.py`
- Test: `tests/test_agency_portal.py`

**Interfaces:**
- Consumes: `ClientAccount`, `JobOrder`, `Clearinghouse`
- Produces: `AgencyPortalEngine`: client token auth, ZIP/tar deliverable bundle generator, invoice creation, and verified payment clearing into OMNIVERSE financial ledger.

- [ ] **Step 1: Write tests for token generation, bundle creation, and invoice reconciliation**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement portal_engine.py with ZIP packaging and clearinghouse integration**
- [ ] **Step 4: Run pytest to verify portal engine tests pass**
- [ ] **Step 5: Git commit task 5**

---

### Task 6: FastAPI Agency Routes & Real-time WebSockets
**Files:**
- Create: `src/omniverse/api/routes/agency.py`
- Modify: `src/omniverse/api/app.py`
- Test: `tests/test_agency_api.py`

**Interfaces:**
- Exposes: REST API endpoints (`/api/v1/agency/...`) and live WebSocket telemetry.

- [ ] **Step 1: Write tests for FastAPI agency routes (hunt, audit, pitch, order execution, client portal)**
- [ ] **Step 2: Run pytest to verify test failure**
- [ ] **Step 3: Implement routes/agency.py and wire into api/app.py**
- [ ] **Step 4: Run pytest to verify agency API tests pass**
- [ ] **Step 5: Git commit task 6**

---

### Task 7: Interactive Agency Cockpit & Client Portal Web Interface
**Files:**
- Create: `src/omniverse/api/templates/agency_cockpit.html`
- Create: `src/omniverse/api/templates/client_portal.html`
- Modify: `src/omniverse/api/routes/agency.py` to serve dynamic views

- [ ] **Step 1: Build responsive cyberpunk/modern HTML5/Tailwind/CSS Agency Cockpit**
- [ ] **Step 2: Build sleek Self-Serve Client Portal with live order progress bar & deliverable download**
- [ ] **Step 3: Add routes in agency.py to serve interactive HTML dashboards**
- [ ] **Step 4: Test endpoint response status and HTML rendering**
- [ ] **Step 5: Git commit task 7**

---

### Task 8: CLI Commands & Autonomous Orchestration
**Files:**
- Modify: `src/omniverse/cli.py`
- Test: `tests/test_agency_cli.py`

- [ ] **Step 1: Write CLI command tests (`agency-hunt`, `agency-audit`, `agency-fulfill`, `agency-status`)**
- [ ] **Step 2: Implement CLI commands in cli.py with formatted tables and color highlights**
- [ ] **Step 3: Run pytest to verify CLI tests pass**
- [ ] **Step 4: Git commit task 8**

---

### Task 9: Full Regression, End-to-End Simulation, and Verification
**Files:**
- Run: `pytest -v` across the entire codebase
- Verify: Zero regressions, 100% green tests
- Run: End-to-end CLI demonstration (`python -m omniverse.cli agency-hunt`, `agency-status`)
- Update: `README.md` and `MASTER_DIRECTIVE.md` documentation
- Git commit final verification
