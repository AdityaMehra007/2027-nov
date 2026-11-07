# Dispatch Task — Build Forge Fulfillment & Test Health Worker (Milestones 2, 3, 4)

## Working Directory
`e:\2027 nov\.agents\teamwork\teamwork_worker_m2_m3\`

## Original Request Record
`e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`

## Project Specification
`e:\2027 nov\.agents\teamwork\PROJECT.md`

## Exclusive File Ownership:
- `src/omniverse/modules/agency/revision_manager.py`

## Mandatory Integrity Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Tasks:
1. **Implement `src/omniverse/modules/agency/revision_manager.py`**:
   - Implement `RevisionResult(BaseModel)` with:
     - `order_id: str`
     - `files_updated: list[str]`
     - `summary: str`
     - `qa_verified: bool`
     - `zip_bundle_path: str`
   - Implement `AutonomousRevisionAgent`:
     - `__init__(self, portal_engine: Optional[AgencyPortalEngine] = None, qa_governor: Optional[QAGovernor] = None)`
     - `apply_revision(self, order: JobOrder, feedback: str) -> RevisionResult`:
       - Parses feedback instructions.
       - Iterates through `order.deliverables`, finds relevant files (e.g. `index.html` for UI/pricing/dark mode, `sales_copy.md` for copy/guarantee/urgency, `main.py` for API endpoints).
       - Modifies file content on disk with appropriate enhancements matching the feedback.
       - Re-runs QA validation on modified deliverables via `QAGovernor.verify_deliverable(d)` and sets `d.qa_passed = True`.
       - Re-packages bundle via `portal_engine.package_order_bundle(order)`.
       - Returns a valid `RevisionResult`.
2. **Verify `tests/test_agency_revisions.py`**:
   - Run `pytest tests/test_agency_revisions.py -v` and verify it passes 100%.
3. **Execute Universal Build Forge Across Commercial Hubs**:
   - Execute `build-for-client` across commercial hubs:
     `python -m omniverse.cli build-for-client --client "Apex Neural Compute"` (SF_BAY_AREA)
     `python -m omniverse.cli build-for-client --client "Gotham Liquidity Partners"` (NEW_YORK)
     `python -m omniverse.cli build-for-client --client "Thames Cross-Border Clearing"` (LONDON)
     `python -m omniverse.cli build-for-client --client "Brandenburg Green Battery"` (BERLIN)
     `python -m omniverse.cli build-for-client --client "Marina Bay Sovereign Wealth Analytics"` (SINGAPORE)
     `python -m omniverse.cli build-for-client --client "Marunouchi Autonomous Logistics"` (TOKYO)
     `python -m omniverse.cli build-for-client --client "DIFC Prime Asset Custody"` (DUBAI)
     `python -m omniverse.cli build-for-client --client "Indiranagar Cloud Orchestrator"` (BENGALURU)
   - Verify that disk artifact trees under `artifacts/world_builds/<slug>/` contain all 12 deliverables (fullstack software, AI agents, MCP schemas, marketing suites) with valid `build_manifest.json` and SHA-256 tokens.
4. **Execute and Verify Platform CLI Commands**:
   - Run `python -m omniverse.cli world-stats`
   - Run `python -m omniverse.cli world-clients --hub SF_BAY_AREA`
   - Run `python -m omniverse.cli audit-client --client "Apex Neural Compute"`
   - Run `python -m omniverse.cli run-world-swarm --limit 1`
5. **Verify Automated Test Suites**:
   - Run `pytest tests/test_agency_revisions.py tests/test_world_clients.py tests/test_world_agents_and_forge.py tests/test_cli_world_swarm.py tests/test_challenger_m1_verification.py -v`
   - Run `pytest --collect-only -q` to confirm zero collection errors across the entire repository.
6. **Author Deliverables**:
   Author `changes.md` and complete `handoff.md` in your working directory and notify parent orchestrator via `send_message`.


## 2026-11-07T12:00:06Z
[Message] timestamp=2026-11-07T12:00:06Z sender=975620c1-1b3c-413b-8522-63ef75a9fd83 priority=MESSAGE_PRIORITY_HIGH content=You are dispatched as teamwork_worker for Milestones 2, 3, and 4: Universal Build Forge Client Fulfillment, Revisions Manager Implementation, and Platform CLI / Automated Test Suite Health.

Working Directory: e:\2027 nov\.agents\teamwork\teamwork_worker_m2_m3\
Original Request Authority: e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md
Project Specification: e:\2027 nov\.agents\teamwork\PROJECT.md
Your Dispatch Task: e:\2027 nov\.agents\teamwork\teamwork_worker_m2_m3\DISPATCH.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE OWNERSHIP:
- src/omniverse/modules/agency/revision_manager.py

TASKS:
1. Implement `src/omniverse/modules/agency/revision_manager.py` with `AutonomousRevisionAgent` and `RevisionResult` according to `tests/test_agency_revisions.py`.
2. Verify `pytest tests/test_agency_revisions.py -v` passes 100%.
3. Execute Universal Build Forge pipeline across commercial hubs via CLI:
   `python -m omniverse.cli build-for-client --client "Apex Neural Compute"`
   `python -m omniverse.cli build-for-client --client "Gotham Liquidity Partners"`
   `python -m omniverse.cli build-for-client --client "Thames Cross-Border Clearing"`
   `python -m omniverse.cli build-for-client --client "Brandenburg Green Battery"`
   `python -m omniverse.cli build-for-client --client "Marina Bay Sovereign Wealth Analytics"`
   `python -m omniverse.cli build-for-client --client "Marunouchi Autonomous Logistics"`
   `python -m omniverse.cli build-for-client --client "DIFC Prime Asset Custody"`
   `python -m omniverse.cli build-for-client --client "Indiranagar Cloud Orchestrator"`
   Verify that compiled build assets (12 deliverables: fullstack software, AI agents, MCP schemas, marketing suites) and artifact trees are generated and validated on disk and in database records.
4. Execute and verify platform CLI commands:
   `python -m omniverse.cli world-stats`
   `python -m omniverse.cli world-clients --hub SF_BAY_AREA`
   `python -m omniverse.cli audit-client --client "Apex Neural Compute"`
   `python -m omniverse.cli run-world-swarm --limit 1`
5. Verify automated test suite:
   `pytest tests/test_agency_revisions.py tests/test_world_clients.py tests/test_world_agents_and_forge.py tests/test_cli_world_swarm.py tests/test_challenger_m1_verification.py -v`
   `pytest --collect-only -q`
6. Document changes in `changes.md` and `handoff.md` and notify parent orchestrator via `send_message`.
