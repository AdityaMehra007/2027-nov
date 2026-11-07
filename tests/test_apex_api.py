# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Apex Singularity and Hyperscale Multi-Vertical API & UI."""

from fastapi.testclient import TestClient
from omniverse.api.app import create_app


def test_apex_telemetry_api():
    app = create_app()
    client = TestClient(app)

    res = client.get("/api/v1/apex/telemetry")
    assert res.status_code == 200
    data = res.json()

    assert data["system"] == "APEX SINGULARITY & OMNIVERSE HYPERSCALE V5"
    assert data["status"] == "ALL_CROWN_JEWELS_AND_VERTICALS_ONLINE"
    assert "benchmark_latency_ms" in data

    # Verify 8 Crown Jewels
    crown = data["crown_jewels"]
    assert crown["01_bytecode_vm"]["status"] == "VERIFIED"
    assert crown["02_lsm_tree_storage"]["status"] == "VERIFIED"
    assert crown["03_consistent_hash_ring"]["status"] == "VERIFIED"
    assert crown["04_merkle_prover"]["status"] == "VERIFIED"
    assert crown["05_reverse_mode_autograd"]["status"] == "VERIFIED"
    assert crown["06_limit_order_book"]["status"] == "MATCHED"
    assert crown["07_pagerank_rrf"]["status"] == "CONVERGED"
    assert crown["08_circuit_breaker"]["status"] == "HEALTHY"

    # Verify 6 Hyperscale Verticals
    verts = data["hyperscale_verticals"]
    assert "01_ai_foundry" in verts
    assert "02_quant_wealth" in verts
    assert "03_supply_chain_qcomm" in verts
    assert "04_biotech_genomics" in verts
    assert "05_fintech_dpi_ocen" in verts
    assert "06_cleantech_smart_grid" in verts


def test_apex_dashboard_route():
    app = create_app()
    client = TestClient(app)

    res = client.get("/apex")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "Apex Singularity & 6-Vertical Enterprise Fabric" in res.text
    assert "The 8 Crown Jewels of CS" in res.text
    assert "6 Trillion-Dollar Verticals" in res.text
