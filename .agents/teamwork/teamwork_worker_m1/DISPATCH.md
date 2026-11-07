# Dispatch Task — Milestone 1 Worker (Swarm Operations & Client Audits)

## Working Directory
`e:\2027 nov\.agents\teamwork\teamwork_worker_m1\`

## Original Request Record
`e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`

## Project Specification
`e:\2027 nov\.agents\teamwork\PROJECT.md`

## Explorer Hand-Off Reports to Read:
- `e:\2027 nov\.agents\teamwork\teamwork_explorer_m1_1\handoff.md` (Client Selection & Hub/Sector Coverage)
- `e:\2027 nov\.agents\teamwork\teamwork_explorer_m1_2\handoff.md` (Swarm Coordination & 8 Agents Telemetry)
- `e:\2027 nov\.agents\teamwork\teamwork_explorer_m1_3\handoff.md` (Audit Execution & Database Persistence)

## Exclusive File Ownership:
- `src/omniverse/core/telemetry.py`
- `src/omniverse/modules/agency/models.py`
- `src/omniverse/core/database.py`
- `src/omniverse/agents/client_diagnostic.py`
- `src/omniverse/agents/swarm_orchestrator.py`

## Mandatory Integrity Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Implementation Tasks:
1. **Telemetry Persistence (`src/omniverse/core/telemetry.py`)**:
   In `EventBus.publish(self, event_name: str, payload: Dict[str, Any])`:
   Append every published event to `artifacts/telemetry/events.jsonl` (ensure parent directory `artifacts/telemetry` exists).
2. **Audit Data Model (`src/omniverse/modules/agency/models.py` & `src/omniverse/core/database.py`)**:
   Define `ClientAuditRecord(SQLModel, table=True)` with fields:
   `id: Optional[int] = Field(default=None, primary_key=True)`, `client_name: str = Field(index=True)`, `hub: str = Field(index=True)`, `sector: str = Field(index=True)`, `performance_score: float`, `seo_score: float`, `conversion_score: float`, `overall_health: float`, `estimated_monthly_loss_usd: float`, `timestamp: float = Field(default_factory=time.time)`.
   Register `ClientAuditRecord` in `src/omniverse/core/database.py` and ensure `init_db()` creates the table.
3. **Audit Execution & DB Persistence (`src/omniverse/agents/client_diagnostic.py`)**:
   In `ClientDiagnosticAgent.execute_task`:
   Extract client metadata (`hub`, `sector`). Persist `ClientAuditRecord` to SQLite via `get_session()` (wrapped with safe try/except).
   Append audit telemetry to `artifacts/telemetry/audit_events.jsonl`.
4. **8-Agent Swarm Orchestrator Coordination (`src/omniverse/agents/swarm_orchestrator.py`)**:
   - In `run_global_cohort()`: explicitly invoke `self.prospector.execute_task(...)` with task type `"DISCOVER_GLOBAL_CLIENTS"`.
   - In `run_pipeline_for_client()`: in Phase 3, explicitly invoke `self.code_forge.execute_task(...)`, `self.agent_engineer.execute_task(...)`, and `self.growth_marketing.execute_task(...)` alongside `self.pipeline.build_everything_for_client(...)` so that all 8 agents actively execute and publish telemetry.
5. **Operate Full-Scale Swarm Across All 8 Global Commercial Hubs**:
   Execute the swarm across all 8 hubs:
   `python -m omniverse.cli run-world-swarm --hub SF_BAY_AREA --limit 3`
   `python -m omniverse.cli run-world-swarm --hub NEW_YORK --limit 3`
   `python -m omniverse.cli run-world-swarm --hub LONDON --limit 3`
   `python -m omniverse.cli run-world-swarm --hub BERLIN --limit 3`
   `python -m omniverse.cli run-world-swarm --hub SINGAPORE --limit 3`
   `python -m omniverse.cli run-world-swarm --hub TOKYO --limit 3`
   `python -m omniverse.cli run-world-swarm --hub DUBAI --limit 3`
   `python -m omniverse.cli run-world-swarm --hub BENGALURU --limit 4`
6. **Execute Comprehensive Client Audits & Verify Persistence**:
   Execute CLI audit commands:
   `python -m omniverse.cli audit-client --client "Apex Neural Compute"`
   `python -m omniverse.cli audit-client --client "Gotham Liquidity Partners"`
   `python -m omniverse.cli audit-client --client "Thames Cross-Border Clearing"`
   `python -m omniverse.cli audit-client --client "Indiranagar Cloud Orchestrator"`
   Verify that rows are recorded in `client_audit_records` in `data/omniverse.db` and telemetry logs in `artifacts/telemetry/audit_events.jsonl` and `artifacts/telemetry/events.jsonl`.
7. **Test Suite Verification**:
   Execute `pytest tests/test_world_clients.py tests/test_world_agents_and_forge.py tests/test_cli_world_swarm.py -v`.
   Ensure all 20 tests pass with zero failures.
8. **Author Deliverables**:
   Author `changes.md` and complete `handoff.md` in your working directory and notify the parent orchestrator via `send_message`.


## 2026-11-07T11:31:15Z
[Message] timestamp=2026-11-07T11:31:15Z sender=975620c1-1b3c-413b-8522-63ef75a9fd83 priority=MESSAGE_PRIORITY_HIGH
You are dispatched as teamwork_worker for Milestone 1: Full-Scale Autonomous Swarm Execution and Client Audits.
Working Directory: e:\2027 nov\.agents\teamwork\teamwork_worker_m1\
Original Request Authority: e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md
Project Specification: e:\2027 nov\.agents\teamwork\PROJECT.md
Your Dispatch Task: e:\2027 nov\.agents\teamwork\teamwork_worker_m1\DISPATCH.md
