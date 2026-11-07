# Project: CASHFLOW INFINITY: OMNIVERSE

## Architecture
CASHFLOW INFINITY: OMNIVERSE is a planetary-scale autonomous agency and venture platform orchestrated by `SupremeSwarmOrchestrator` (`src/omniverse/agents/swarm_orchestrator.py`), coordinating 8 specialized agents across 6 core operational divisions:
1. **Intelligence**: `GlobalProspectorAgent` (`src/omniverse/agents/global_prospector.py`) — Discovers international market opportunities, calculates total addressable market (TAM), and filters accounts by commercial hub and sector.
2. **Audit**: `ClientDiagnosticAgent` (`src/omniverse/agents/client_diagnostic.py`) — Executes deep technical, SEO, and conversion diagnostics, generating health scores (0-100) and quantifying monthly revenue leakage.
3. **Architecture**: `UniversalSolutionArchitectAgent` (`src/omniverse/agents/solution_architect.py`) — Transforms diagnostic gaps into comprehensive technical solution blueprints and deliverable scopes.
4. **Fulfillment**:
   - `AutonomousCodeForgeAgent` (`src/omniverse/agents/code_forge_agent.py`) — Generates fullstack software applications (`index.html`, `main.py`, `README.md`, `test_service.py`, `Dockerfile`).
   - `AutonomousAgentEngineerAgent` (`src/omniverse/agents/agent_engineer_agent.py`) — Synthesizes autonomous AI agents (`agent_runtime.py`, `webhook_bot.py`) and Model Context Protocol schemas (`mcp_tools.json`).
   - `GrowthMarketingAgent` (`src/omniverse/agents/growth_marketing_agent.py`) — Produces direct-response marketing suites (`sales_copy.md`, `ad_pack.json`, `email_drip_sequence.md`, `schema_org.json`).
   - Coordinated via `UniversalForgePipeline` (`src/omniverse/modules/agency/fulfillment/forge_pipeline.py`) and verified by `QAGovernor` (`src/omniverse/modules/agency/qa_governor.py`).
5. **Commercial**: `CommercialDealCloserAgent` (`src/omniverse/agents/commercial_closer.py`) — Formulates executive proposals with integrated payment gateways (Stripe, Razorpay, RTGS, Web3).
6. **Finance**: `TreasuryReconciliationAgent` (`src/omniverse/agents/treasury_reconciler.py`) — Validates SHA-256 deliverable checksum tokens and settles transactions atomically in `GlobalClearingHouse`.

### World Client Directory
- Located in `src/omniverse/modules/agency/world_clients.py`.
- 8 Global Commercial Hubs: `SF_BAY_AREA`, `NEW_YORK`, `LONDON`, `BERLIN`, `SINGAPORE`, `TOKYO`, `DUBAI`, `BENGALURU`.
- 6 Industry Sectors: `SAAS_DEVTOOLS`, `FINTECH_PAYMENTS`, `HEALTHCARE_CLINICAL`, `ECOMMERCE_DTC`, `CLEANTECH_ENERGY`, `SMB_SERVICES`.
- Catalog: 25 verified international commercial enterprises tracking $315,370,000 USD in aggregate annual revenue.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | 8-Agent Swarm Orchestration | SupremeSwarmOrchestrator manages all 8 agents across 5 pipeline phases | M1 | survey_miner_1_rep (VERIFIED) |
| 2 | World Client Hub Coverage | Execution across all 8 global commercial hubs (SF, NYC, LON, BER, SGP, TYO, DXB, BLR) | M1 | survey_miner_1_rep (VERIFIED) |
| 3 | World Client Sector Coverage | Swarm processing across all 6 industry verticals | M1 | survey_miner_1_rep (VERIFIED) |
| 4 | Client Diagnostic Audits | Deterministic health scoring (0-100) and monthly revenue loss quantification | M1 | survey_miner_1_rep (VERIFIED) |
| 5 | Audit Telemetry Persistence | Event bus telemetry (`CLIENT_DIAGNOSIS_COMPLETED`) and SQLite persistence | M1 | survey_miner_1_rep (VERIFIED) |
| 6 | Fullstack Software Generation | Universal Build Forge compiles HTML5/Tailwind, FastAPI backend, Dockerfile, unit tests | M2 | survey_miner_2_rep (VERIFIED) |
| 7 | Autonomous AI Agent Synthesis | Compilation of `agent_runtime.py` and `webhook_bot.py` | M2 | survey_miner_2_rep (VERIFIED) |
| 8 | MCP Tool Schema Compilation | Model Context Protocol v1.0 declarations in `mcp_tools.json` | M2 | survey_miner_2_rep (VERIFIED) |
| 9 | Marketing Suite Generation | Direct-response sales copy, ad pack, email drip, Schema.org JSON-LD | M2 | survey_miner_2_rep (VERIFIED) |
| 10 | On-Disk Build Asset Validation | Artifact tree generation under `artifacts/world_builds/<slug>/` with SHA-256 manifests | M2 | survey_miner_2_rep (VERIFIED) |
| 11 | Build Packaging & ZIP Bundling | Compilation into `artifacts/bundles/<order_id>_bundle.zip` with manifest | M2 | survey_miner_2_rep (VERIFIED) |
| 12 | Database Fulfillment Persistence | Job order and deliverable tracking in SQLite ledger | M2 | survey_miner_2_rep (VERIFIED) |
| 13 | Autonomous Revision Manager | Implementation of `revision_manager.py` to resolve missing dependency in tests | M3 | worker_m2_m3 (VERIFIED) |
| 14 | Automated Test Suite Health | 100% clean test suite run across all unit/integration tests without fatal errors | M3 | worker_m2_m3 (VERIFIED) |
| 15 | CLI `world-clients` Command | Filtering and discovery of world clients by hub, sector, and limits | M4 | worker_m2_m3 (VERIFIED) |
| 16 | CLI `audit-client` Command | Execution of client diagnostic gap analysis from terminal | M4 | worker_m2_m3 (VERIFIED) |
| 17 | CLI `build-for-client` Command | Compilation and verification of full 12-artifact package from terminal | M4 | worker_m2_m3 (VERIFIED) |
| 18 | CLI `run-world-swarm` Command | End-to-end swarm execution and treasury settlement across cohorts | M4 | worker_m2_m3 (VERIFIED) |
| 19 | CLI `world-stats` Command | Platform-wide operational statistics and TAM breakdown | M4 | worker_m2_m3 (VERIFIED) |
| 20 | Telemetry & Database Verification | End-to-end verification of database records and telemetry logs | M4 | worker_m2_m3 (VERIFIED) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Swarm Operations & Client Audits | Coordinate 8 autonomous agents across all 8 commercial hubs & 6 sectors; execute and persist audits | none | DONE |
| M2 | Universal Build Forge Fulfillment | Compile software, AI agents, MCP schemas, and marketing suites across hubs; validate on disk and DB | M1 | DONE |
| M3 | Revisions Manager & Test Health | Implement `revision_manager.py` per architecture spec; verify 100% test suite execution | none | DONE |
| M4 | CLI Verification & Operational Telemetry | Verify all 5 platform CLI commands and validate end-to-end telemetry and database persistence | M1, M2, M3 | DONE |

## Interface Contracts
### SupremeSwarmOrchestrator ↔ AgentDispatcher ↔ BaseAgent
- `AgentTask(task_id: str, task_type: str, client_name: str, payload: dict)`
- `BaseAgent.execute_task(task: AgentTask) -> dict` returning status, telemetry, artifacts, and metrics.
- `global_event_bus.publish(event_type: str, data: dict)`

### UniversalForgePipeline ↔ Factories ↔ QAGovernor
- `UniversalForgePipeline.build_all_for_client(client: WorldClient, budget: float) -> ForgedPackage`
- `CodeFactory.generate_application(client_name: str, tech_stack: list[str]) -> list[Deliverable]`
- `AutomationFactory.generate_agent(client_name: str) -> list[Deliverable]`
- `AutomationFactory.generate_mcp_schema(client_name: str) -> Deliverable`
- `MarketingFactory.generate_growth_kit(client_name: str, sector: str) -> list[Deliverable]`
- `QAGovernor.verify_deliverables(deliverables: list[Deliverable]) -> dict` enforcing zero secret leaks, valid AST/JSON/HTML, and minimum byte size.

### CLI ↔ Omniverse Core
- `python -m omniverse.cli <command> [flags]` returning 0 on success, formatting stdout/stderr, and recording database rows.

## Code Layout
- `src/omniverse/agents/` — Autonomous agents and SupremeSwarmOrchestrator
- `src/omniverse/modules/agency/` — World Client Directory, acquisition, models, portal engine, QA governor, revision manager
- `src/omniverse/modules/agency/fulfillment/` — Universal Forge Pipeline, CodeFactory, AutomationFactory, MarketingFactory
- `src/omniverse/core/` — Database (`database.py`), Config (`config.py`), Telemetry (`telemetry.py`), Security (`security.py`)
- `src/omniverse/cli.py` — Platform CLI entrypoints
- `tests/` — Automated test suite
- `artifacts/world_builds/` — Compiled deliverable trees and SHA-256 manifests
- `artifacts/bundles/` — Client ZIP delivery archives
- `artifacts/telemetry/` — On-disk event journals (`events.jsonl`, `audit_events.jsonl`)
- `data/` — SQLite persistent databases (`omniverse.db`, `cashflow_omniverse.db`)
