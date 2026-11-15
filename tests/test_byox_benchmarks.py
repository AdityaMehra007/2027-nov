# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Unit tests for the BYOX Unified 10-Engine Benchmark Suite & Workbench."""

import pytest

from byox.workbench import BYOXWorkbench
from byox.benchmarks.bench_chain import benchmark_pychain
from byox.benchmarks.bench_search import benchmark_pysearch
from byox.benchmarks.bench_vm import benchmark_pyvm
from byox.benchmarks.bench_controlplane import benchmark_pycontrolplane
from byox.benchmarks.runner import run_all_benchmarks


def test_byox_workbench_diagnostics():
    wb = BYOXWorkbench()
    diag = wb.run_system_diagnostics()
    assert diag["all_systems_go"] is True
    assert diag["systems_count"] == 10
    assert diag["probe_duration_ms"] < 200.0  # Sub-200ms sanity check


def test_byox_chain_benchmark():
    results = benchmark_pychain(num_txs=20, difficulty=1)
    assert len(results) == 3
    assert any("Transaction Ingestion" in r.name for r in results)
    assert any("Block Mining" in r.name for r in results)
    assert any("Chain Verification" in r.name for r in results)


def test_byox_search_benchmark():
    results = benchmark_pysearch(num_docs=50, num_queries=20)
    assert len(results) == 2
    assert results[0].total_ops == 50
    assert results[1].total_ops == 20


def test_byox_vm_benchmark():
    results = benchmark_pyvm(num_runs=50)
    assert len(results) == 2
    assert results[1].metadata["computed_factorial"] == 3628800


def test_byox_controlplane_benchmark():
    results = benchmark_pycontrolplane(num_requests=30)
    assert len(results) == 3
    assert any("End-to-End" in r.name for r in results)
    assert any("Vector Lookups" in r.name for r in results)
    assert any("Merkle Audit" in r.name for r in results)


def test_byox_runner_smoke():
    data = run_all_benchmarks(
        redis_reqs=20,
        web_reqs=10,
        db_rows=20,
        git_files=10,
        shell_cmds=20,
        chain_txs=10,
        search_docs=20,
        vm_runs=20,
        cp_reqs=10,
    )
    assert data["total_benchmarks"] >= 20
    assert len(data["results"]) >= 20
    assert data["wall_time_sec"] > 0.0
