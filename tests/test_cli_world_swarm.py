import subprocess
import sys
import pytest


def run_cli(*args):
    cmd = [sys.executable, "-m", "omniverse.cli"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result


def test_cli_world_stats():
    res = run_cli("world-stats")
    assert res.returncode == 0
    assert "GLOBAL CLIENT MATRIX" in res.stdout
    assert "METROPOLITAN HUBS DISTRIBUTION" in res.stdout
    assert "SF_BAY_AREA" in res.stdout


def test_cli_world_clients():
    res = run_cli("world-clients", "--hub", "LONDON", "--limit", "2")
    assert res.returncode == 0
    assert "WORLD CLIENT DIRECTORY" in res.stdout
    assert "LONDON" in res.stdout


def test_cli_audit_client():
    res = run_cli("audit-client", "--client", "Apex Neural Compute")
    assert res.returncode == 0
    assert "CLIENT DIAGNOSTIC REPORT: APEX NEURAL COMPUTE" in res.stdout
    assert "Performance Score" in res.stdout
    assert "Est. Monthly Loss" in res.stdout


def test_cli_build_for_client(tmp_path):
    res = run_cli("build-for-client", "--client", "Apex Neural Compute")
    assert res.returncode == 0
    assert "UNIVERSAL CODE FORGE: MANUFACTURING ALL DELIVERABLES" in res.stdout
    assert "GENERATED ARTIFACTS & SHA-256 MANIFEST" in res.stdout
    assert "VERIFIED & PASSED" in res.stdout


def test_cli_run_world_swarm():
    res = run_cli("run-world-swarm", "--hub", "SINGAPORE", "--limit", "1")
    assert res.returncode == 0
    assert "SUPREME SWARM ORCHESTRATOR" in res.stdout
    assert "Active Swarm Fleet: 8 Autonomous Agents Registered." in res.stdout
    assert "Total Clients Serviced : 1" in res.stdout
    assert "RECONCILED" in res.stdout
