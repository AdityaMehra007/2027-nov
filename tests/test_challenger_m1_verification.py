"""Milestone 1 Empirical Challenger Verification & Stress Harness.

Empirically challenges:
1. 8-Agent Swarm Orchestration under SupremeSwarmOrchestrator.
2. GlobalHub (8/8) and IndustrySector (6/6) cohort processing.
3. Telemetry events.jsonl and audit_events.jsonl schema, timestamp, and payload integrity.
4. Edge cases: limit=0, limit=-1, limit=1000, unknown client, zero contract value.
5. Multithreaded concurrent event publishing stress test.
6. CLI execution of run-world-swarm, audit-client, world-stats, and world-clients.
"""

import json
import subprocess
import sys
import threading
import time
from pathlib import Path
import pytest

from omniverse.agents.swarm_orchestrator import SupremeSwarmOrchestrator
from omniverse.agents.client_diagnostic import ClientDiagnosticAgent
from omniverse.agents.base import AgentTask
from omniverse.modules.agency.world_clients import (
    GlobalHub,
    IndustrySector,
    WorldClientDirectory,
)
from omniverse.core.telemetry import global_event_bus, EventBus
from omniverse.core.database import get_session
from omniverse.modules.agency.models import ClientAuditRecord
from sqlmodel import select


def test_swarm_orchestrator_fleet_registration():
    """Verify SupremeSwarmOrchestrator registers exactly 8 autonomous agents across functional divisions."""
    orchestrator = SupremeSwarmOrchestrator()
    fleet = orchestrator.list_fleet()

    expected_agents = {
        "GlobalProspector": "Intelligence",
        "ClientDiagnostic": "Audit",
        "SolutionArchitect": "Architecture",
        "CodeForge": "Fulfillment",
        "AgentEngineer": "Fulfillment",
        "GrowthMarketing": "Fulfillment",
        "CommercialCloser": "Commercial",
        "TreasuryReconciler": "Finance",
    }

    assert len(fleet) == 8, f"Expected 8 registered agents, got {len(fleet)}: {fleet}"
    for name, div in expected_agents.items():
        assert name in fleet, f"Agent {name} missing from fleet: {fleet}"
        assert fleet[name] == div, f"Agent {name} division mismatch: expected {div}, got {fleet[name]}"


def test_swarm_orchestrator_single_client_cycle():
    """Verify single client pipeline execution runs all 6 phases and produces valid artifacts."""
    orchestrator = SupremeSwarmOrchestrator()
    directory = WorldClientDirectory()
    client = directory.get_client_by_name("Apex Neural Compute")
    assert client is not None, "Client Apex Neural Compute not found"

    res = orchestrator.run_pipeline_for_client(client, contract_value_usd=20000.0, reconcile=True)

    assert res["status"] == "SUCCESS"
    assert "diagnosis" in res
    assert res["diagnosis"]["overall_health"] > 0
    assert "blueprint" in res
    assert len(res["blueprint"]["architecture_modules"]) >= 4
    assert "forged_package" in res
    assert res["forged_package"]["total_files"] >= 10
    assert res["forged_package"]["qa_passed"] is True
    assert "commercial_proposal" in res
    assert res["commercial_proposal"]["quoted_contract_usd"] == 20000.0
    assert "settlement" in res
    assert res["settlement"]["ledger_status"] == "RECONCILED"
    assert res["settlement"]["settled_amount_usd"] == 20000.0
    assert res["duration_sec"] > 0


@pytest.mark.parametrize("hub", list(GlobalHub))
def test_all_8_global_hubs_cohort_execution(hub):
    """Verify swarm execution successfully processes cohorts across all 8 global hubs."""
    orchestrator = SupremeSwarmOrchestrator()
    cohort = orchestrator.run_global_cohort(hub=hub, limit=1, contract_value_usd=12000.0)

    assert cohort["status"] == "SUCCESS"
    assert cohort["processed_count"] == 1
    assert cohort["hub_filter"] == hub.value
    assert cohort["total_revenue_settled_usd"] == 12000.0
    assert cohort["total_artifacts_generated"] >= 10
    assert len(cohort["cohort_results"]) == 1
    result = cohort["cohort_results"][0]
    assert result["client"]["hub"] == hub.value or result["client"]["hub"] == hub


@pytest.mark.parametrize("sector", list(IndustrySector))
def test_all_6_industry_sectors_cohort_execution(sector):
    """Verify swarm execution successfully processes cohorts across all 6 industry sectors."""
    orchestrator = SupremeSwarmOrchestrator()
    cohort = orchestrator.run_global_cohort(sector=sector, limit=1, contract_value_usd=10000.0)

    assert cohort["status"] == "SUCCESS"
    assert cohort["processed_count"] == 1
    assert cohort["sector_filter"] == sector.value
    assert cohort["total_revenue_settled_usd"] == 10000.0
    assert len(cohort["cohort_results"]) == 1
    result = cohort["cohort_results"][0]
    assert result["client"]["sector"] == sector.value or result["client"]["sector"] == sector


def test_telemetry_events_jsonl_schema_and_timestamps():
    """Verify artifacts/telemetry/events.jsonl has valid JSON on every line, valid timestamps, and expected schemas."""
    events_path = Path("artifacts/telemetry/events.jsonl")
    assert events_path.exists(), "artifacts/telemetry/events.jsonl does not exist"

    with open(events_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "artifacts/telemetry/events.jsonl is empty"

    now = time.time()
    observed_event_names = set()

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except Exception as e:
            pytest.fail(f"Line {i+1} is invalid JSON: {e}\nContent: {line}")

        assert "timestamp" in data, f"Line {i+1} missing 'timestamp': {data}"
        assert "event_name" in data, f"Line {i+1} missing 'event_name': {data}"
        assert "payload" in data, f"Line {i+1} missing 'payload': {data}"

        ts = data["timestamp"]
        assert isinstance(ts, (int, float)), f"Timestamp not numeric on line {i+1}: {ts}"
        # Assert timestamp is reasonable Unix epoch timestamp in 2026/2027 era
        assert 1.7e9 <= ts <= now + 3600, f"Timestamp out of reasonable bounds on line {i+1}: {ts}"

        event_name = data["event_name"]
        observed_event_names.add(event_name)
        payload = data["payload"]
        assert isinstance(payload, dict), f"Payload is not dict on line {i+1}: {payload}"

        # Schema assertions per swarm event
        if event_name == "GLOBAL_PROSPECTS_DISCOVERED":
            assert "count" in payload
            assert "hub" in payload
            assert "sector" in payload
        elif event_name == "CLIENT_DIAGNOSIS_COMPLETED":
            assert "client" in payload
            assert "health_score" in payload
            assert "monthly_loss_usd" in payload
        elif event_name == "SOLUTION_BLUEPRINT_CREATED":
            assert "client" in payload
            assert "solution_name" in payload
        elif event_name == "CODE_FORGE_COMPLETED":
            assert "client" in payload
            assert "artifacts_count" in payload
        elif event_name == "AGENT_ENGINEERING_COMPLETED":
            assert "client" in payload
            assert "artifacts_count" in payload
        elif event_name == "GROWTH_MARKETING_COMPLETED":
            assert "client" in payload
            assert "artifacts_count" in payload
        elif event_name == "COMMERCIAL_PROPOSAL_DISPATCHED":
            assert "client" in payload
            assert "quoted_usd" in payload
        elif event_name == "TREASURY_SETTLEMENT_RECORDED":
            assert "client" in payload
            assert "amount_usd" in payload
            assert "tx_id" in payload
            assert "status" in payload
        elif event_name == "SWARM_BUILD_CYCLE_COMPLETED":
            assert "client" in payload
            assert "hub" in payload
            assert "total_artifacts" in payload
            assert "total_bytes" in payload
            assert "duration_sec" in payload

    # Verify all 9 primary swarm events were observed
    required_events = {
        "GLOBAL_PROSPECTS_DISCOVERED",
        "CLIENT_DIAGNOSIS_COMPLETED",
        "SOLUTION_BLUEPRINT_CREATED",
        "CODE_FORGE_COMPLETED",
        "AGENT_ENGINEERING_COMPLETED",
        "GROWTH_MARKETING_COMPLETED",
        "COMMERCIAL_PROPOSAL_DISPATCHED",
        "TREASURY_SETTLEMENT_RECORDED",
        "SWARM_BUILD_CYCLE_COMPLETED",
    }
    missing = required_events - observed_event_names
    assert not missing, f"Missing required telemetry events: {missing}"


def test_audit_events_jsonl_content():
    """Verify artifacts/telemetry/audit_events.jsonl has valid JSON and spans all 8 hubs and 25 clients."""
    audit_path = Path("artifacts/telemetry/audit_events.jsonl")
    assert audit_path.exists(), "artifacts/telemetry/audit_events.jsonl does not exist"

    with open(audit_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 25, f"Expected at least 25 audit events, found {len(lines)}"

    hubs = set()
    clients = set()
    for line in lines:
        entry = json.loads(line)
        assert entry["event_name"] == "CLIENT_DIAGNOSIS_COMPLETED"
        assert entry["health_score"] > 0
        assert entry["monthly_loss_usd"] >= 0.0
        hubs.add(entry["hub"])
        clients.add(entry["client_name"])

    expected_hubs = {h.value for h in GlobalHub}
    assert expected_hubs.issubset(hubs), f"Missing global hubs in audit_events: {expected_hubs - hubs}"
    dir_clients = {c.name for c in WorldClientDirectory().get_all_clients()}
    missing = dir_clients - clients
    assert not missing, f"Missing directory clients from audit_events: {missing}"


def test_sqlite_client_audit_records_integrity():
    """Verify SQLite database data/omniverse.db stores client_audit_records across all 8 hubs and 25 clients."""
    with get_session() as session:
        records = session.exec(select(ClientAuditRecord)).all()
        assert len(records) >= 25, f"Expected >= 25 records, found {len(records)}"

        hubs = {r.hub for r in records}
        clients = {r.client_name for r in records}
        sectors = {r.sector for r in records}

        expected_hubs = {h.value for h in GlobalHub}
        assert expected_hubs.issubset(hubs), f"Missing global hubs in SQLite: {expected_hubs - hubs}"
        dir_clients = {c.name for c in WorldClientDirectory().get_all_clients()}
        missing = dir_clients - clients
        assert not missing, f"Missing directory clients from SQLite: {missing}"
        assert len(sectors) >= 6, f"Expected at least 6 sectors, found {len(sectors)}"

        for r in records:
            assert r.overall_health > 0
            assert r.estimated_monthly_loss_usd >= 0.0
            assert r.performance_score > 0
            assert r.seo_score > 0
            assert r.conversion_score > 0


def test_stress_edge_case_limit_zero():
    """Verify cohort processing with limit=0 does not crash and processes 0 clients cleanly."""
    orchestrator = SupremeSwarmOrchestrator()
    cohort = orchestrator.run_global_cohort(limit=0)
    assert cohort["status"] == "SUCCESS"
    assert cohort["processed_count"] == 0
    assert cohort["total_revenue_settled_usd"] == 0.0
    assert cohort["total_artifacts_generated"] == 0
    assert len(cohort["cohort_results"]) == 0


def test_stress_edge_case_limit_overflow():
    """Verify cohort processing with limit exceeding total clients (e.g. 1000) caps at total catalog size without crashing."""
    orchestrator = SupremeSwarmOrchestrator()
    cohort = orchestrator.run_global_cohort(hub=GlobalHub.SF_BAY_AREA, limit=1000)
    assert cohort["status"] == "SUCCESS"
    # SF_BAY_AREA has 3 clients
    assert cohort["processed_count"] == 3
    assert len(cohort["cohort_results"]) == 3


def test_stress_edge_case_negative_limit():
    """Verify behavior when negative limit is passed."""
    orchestrator = SupremeSwarmOrchestrator()
    cohort = orchestrator.run_global_cohort(limit=-1)
    assert cohort["status"] == "SUCCESS"
    # Python slicing [: -1] gives all except last client (24 out of 25)
    assert cohort["processed_count"] == 24


def test_stress_edge_case_unknown_client_diagnostic():
    """Verify ClientDiagnosticAgent handles unknown client gracefully with status ERROR."""
    agent = ClientDiagnosticAgent()
    res = agent.execute_task(AgentTask(task_type="AUDIT_CLIENT", payload={"client_name": "NonExistentCompanyXYZ_999"}))
    assert res["status"] == "ERROR"
    assert "not found" in res["message"].lower()


def test_stress_edge_case_zero_contract_value():
    """Verify single client pipeline runs when contract value is $0.0."""
    orchestrator = SupremeSwarmOrchestrator()
    directory = WorldClientDirectory()
    client = directory.get_client_by_name("Apex Neural Compute")
    res = orchestrator.run_pipeline_for_client(client, contract_value_usd=0.0, reconcile=True)
    assert res["status"] == "SUCCESS"
    assert res["commercial_proposal"]["quoted_contract_usd"] == 0.0
    assert res["settlement"]["settled_amount_usd"] == 0.0


def test_stress_concurrent_event_bus_publishing():
    """Stress test concurrent thread safety of EventBus publishing: verify valid JSON and in-memory retention."""
    test_log = Path("artifacts/telemetry/test_stress_events.jsonl")
    if test_log.exists():
        test_log.unlink()

    bus = EventBus(log_path=str(test_log))
    thread_count = 10
    events_per_thread = 50

    def worker(tid):
        for j in range(events_per_thread):
            bus.publish(
                "STRESS_TEST_EVENT",
                {"thread_id": tid, "index": j, "data": "A" * 100},
            )

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # In-memory must retain 100% of events
    assert len(bus._events) == thread_count * events_per_thread

    # On disk: verify every line that was written is 100% valid JSON with no corrupted interleaving
    with open(test_log, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 480, f"Excessive dropped writes under contention: {len(lines)}"
    for line in lines:
        parsed = json.loads(line)
        assert parsed["event_name"] == "STRESS_TEST_EVENT"
        assert parsed["payload"]["data"] == "A" * 100

    # Cleanup test file
    test_log.unlink()


def test_cli_run_world_swarm_subprocess():
    """Verify CLI command run-world-swarm executes cleanly in subprocess and returns exit code 0."""
    cmd = [sys.executable, "-m", "omniverse.cli", "run-world-swarm", "--hub", "SF_BAY_AREA", "--limit", "1"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"CLI run-world-swarm failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
    assert "SUPREME SWARM ORCHESTRATOR" in proc.stdout
    assert "Total Clients Serviced : 1" in proc.stdout


def test_cli_audit_client_subprocess():
    """Verify CLI command audit-client executes cleanly in subprocess."""
    cmd = [sys.executable, "-m", "omniverse.cli", "audit-client", "--client", "Apex Neural Compute"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"CLI audit-client failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
    assert "CLIENT DIAGNOSTIC REPORT: APEX NEURAL COMPUTE" in proc.stdout
    assert "Overall Health" in proc.stdout


def test_cli_world_stats_subprocess():
    """Verify CLI command world-stats executes cleanly in subprocess."""
    cmd = [sys.executable, "-m", "omniverse.cli", "world-stats"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"CLI world-stats failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
    assert "GLOBAL CLIENT MATRIX — TOTAL ADDRESSABLE MARKET" in proc.stdout
    assert "Total Companies Tracked : 25" in proc.stdout


def test_cli_world_clients_subprocess():
    """Verify CLI command world-clients executes cleanly in subprocess."""
    cmd = [sys.executable, "-m", "omniverse.cli", "world-clients", "--hub", "BERLIN", "--limit", "2"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"CLI world-clients failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
    assert "Total Discovered: 2 companies" in proc.stdout
