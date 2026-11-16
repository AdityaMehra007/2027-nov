"""PyControlPlane Resilience, Telemetry, and Semantic Caching Benchmark."""

from __future__ import annotations
import time
from typing import List
from pycontrolplane.orchestrator import ControlPlaneOrchestrator, ControlPlaneRequest
from pycontrolplane.ai_gateway.router import ModelTier
from pycontrolplane.ai_gateway.semantic_cache import SemanticCache
from pycontrolplane.core.audit import MerkleAuditLedger
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pycontrolplane(num_requests: int = 300) -> List[BenchmarkResult]:
    cp = ControlPlaneOrchestrator(service_name="bench-cp")
    results: List[BenchmarkResult] = []

    # 1. Full Orchestrated Request Lifecycle
    req_latencies: List[float] = []
    t0_req = time.perf_counter()

    for i in range(num_requests):
        req = ControlPlaneRequest(
            tenant_id=f"bench_tenant_{i // 50}",
            actor=f"user_{i}",
            prompt=f"Benchmarking enterprise latency and reliability #{i}",
            preferred_tier=ModelTier.FAST,
            embedding=[0.8, 0.2, 0.1],
        )
        t0 = time.perf_counter()
        res = cp.handle_request(req)
        req_latencies.append((time.perf_counter() - t0) * 1000.0)
        assert res.success is True

    total_req_time = time.perf_counter() - t0_req
    results.append(
        BenchmarkResult.from_latencies(
            name="PyControlPlane End-to-End Invocations",
            latencies_ms=req_latencies,
            duration_sec=total_req_time,
            metadata={"requests": num_requests},
        )
    )

    # 2. Semantic Cache Cosine Lookup Throughput
    cache = SemanticCache(similarity_threshold=0.90)
    for i in range(100):
        cache.set(f"Query {i}", f"Response {i}", embedding=[0.5 + i * 0.001, 0.5, 0.0])

    lookup_latencies: List[float] = []
    t0_lookup = time.perf_counter()

    for _ in range(num_requests):
        t0 = time.perf_counter()
        hit, _, _ = cache.get("Query 50", embedding=[0.55, 0.5, 0.0])
        lookup_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_lookup_time = time.perf_counter() - t0_lookup
    results.append(
        BenchmarkResult.from_latencies(
            name="PyControlPlane Semantic Vector Lookups",
            latencies_ms=lookup_latencies,
            duration_sec=total_lookup_time,
            metadata={"cached_entries": 100, "lookups": num_requests},
        )
    )

    # 3. Merkle Audit Ledger Chaining
    ledger = MerkleAuditLedger()
    audit_latencies: List[float] = []
    t0_audit = time.perf_counter()

    for i in range(num_requests):
        t0 = time.perf_counter()
        ledger.append_record(actor="auditor", action="state_mutation", payload={"block": i})
        audit_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_audit_time = time.perf_counter() - t0_audit
    assert ledger.verify_chain_integrity() is True

    results.append(
        BenchmarkResult.from_latencies(
            name="PyControlPlane Merkle Audit SHA-256 Chaining",
            latencies_ms=audit_latencies,
            duration_sec=total_audit_time,
            metadata={"blocks_chained": num_requests},
        )
    )

    return results
