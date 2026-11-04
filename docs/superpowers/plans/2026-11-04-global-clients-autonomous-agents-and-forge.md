# Global Client Matrix & Autonomous Build-Everything Agent Fleet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a global client directory spanning 8 hubs and 6 industry sectors, an 8-agent autonomous swarm coordinated by a Supreme Swarm Orchestrator, and a Universal Build Forge that autonomously generates full-stack code, AI agent bundles, marketing suites, and commercial payment checkout integrations.

**Architecture:** Decoupled agent architecture extending `BaseAgent` and `BaseModel`, backed by SQLite/SQLModel persistence, unified through `SupremeSwarmOrchestrator` and `UniversalForgePipeline`, and exposed via `omniverse.cli` commands.

**Tech Stack:** Python 3.13, FastAPI, SQLModel, Pydantic v2, Pytest, Uvicorn, Docker, Hashlib SHA-256.

**Spec:** [docs/superpowers/specs/2026-11-04-global-clients-autonomous-agents-and-forge-design.md](file:///e:/2027%20nov/docs/superpowers/specs/2026-11-04-global-clients-autonomous-agents-and-forge-design.md)

## Global Constraints

- Python 3.11+ compatible (currently running Python 3.13).
- Must adhere strictly to Air-Gapped Security doctrine: live monetary movements require verified tokens or simulated modes.
- Strict test verification: 100% green test execution with no unhandled exceptions.
- Deliverable integrity: Every generated deliverable must include an accurate SHA-256 hash and byte size.

---

### Task 1: Global Client Directory & Multi-Hub Taxonomy

**Files:**
- Create: `src/omniverse/modules/agency/world_clients.py`
- Test: `tests/test_world_clients.py`

**Interfaces:**
- Consumes: `ProspectArchetype`, `Lead`, `LeadStage` from `omniverse.modules.agency.models`
- Produces: `GlobalHub`, `IndustrySector`, `WorldClient`, `WorldClientDirectory`

- [ ] **Step 1: Write test for WorldClientDirectory**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement WorldClientDirectory with 8 global hubs and 6 sectors**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**

---

### Task 2: Specialized Autonomous Agent Fleet

**Files:**
- Create:
  - `src/omniverse/agents/global_prospector.py`
  - `src/omniverse/agents/client_diagnostic.py`
  - `src/omniverse/agents/solution_architect.py`
  - `src/omniverse/agents/code_forge_agent.py`
  - `src/omniverse/agents/agent_engineer_agent.py`
  - `src/omniverse/agents/growth_marketing_agent.py`
  - `src/omniverse/agents/commercial_closer.py`
  - `src/omniverse/agents/treasury_reconciler.py`
  - `src/omniverse/agents/swarm_orchestrator.py`
- Modify: `src/omniverse/agents/__init__.py`
- Test: `tests/test_world_agents_and_forge.py`

**Interfaces:**
- Consumes: `BaseAgent`, `AgentTask`, `AgentDispatcher` from `omniverse.agents.base`
- Produces: 8 specialized agent classes and `SupremeSwarmOrchestrator`

- [ ] **Step 1: Write tests for the autonomous agent fleet**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement all 8 agent roles and SupremeSwarmOrchestrator**
- [ ] **Step 4: Update `src/omniverse/agents/__init__.py`**
- [ ] **Step 5: Run tests to verify all agent executions pass**
- [ ] **Step 6: Commit**

---

### Task 3: Universal Build Forge Pipeline

**Files:**
- Create: `src/omniverse/modules/agency/fulfillment/forge_pipeline.py`
- Modify: `src/omniverse/modules/agency/fulfillment/__init__.py`
- Test: `tests/test_world_agents_and_forge.py`

**Interfaces:**
- Consumes: `CodeFactory`, `AutomationFactory`, `MarketingFactory` from `omniverse.modules.agency.fulfillment`
- Produces: `UniversalForgePipeline` with unified multi-artifact bundle compilation and QA reporting.

- [ ] **Step 1: Write tests for UniversalForgePipeline**
- [ ] **Step 2: Implement UniversalForgePipeline**
- [ ] **Step 3: Run tests to verify generated artifacts compile cleanly**
- [ ] **Step 4: Commit**

---

### Task 4: CLI Master Command Integration

**Files:**
- Modify: `src/omniverse/cli.py`
- Test: `tests/test_cli_world_swarm.py`

**Interfaces:**
- Produces commands: `world-clients`, `audit-client`, `build-for-client`, `run-world-swarm`, `world-stats`

- [ ] **Step 1: Add argument parsers and command handlers in `cli.py`**
- [ ] **Step 2: Write test verifying CLI commands execute with code 0**
- [ ] **Step 3: Run pytest on CLI tests**
- [ ] **Step 4: Commit**

---

### Task 5: End-to-End Autonomous Execution & Verification

**Files:**
- Run full pytest suite across entire repository
- Execute CLI demo commands generating real client solutions
- Record generated deliverables and verified revenue

- [ ] **Step 1: Execute full test suite `pytest -v`**
- [ ] **Step 2: Run sample world swarm execution via CLI**
- [ ] **Step 3: Verify output artifacts and ledger reconciliation**
- [ ] **Step 4: Final verification and audit signoff**
