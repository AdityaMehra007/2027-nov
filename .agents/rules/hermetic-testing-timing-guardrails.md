---
description: Flake prevention for integration test timing assertions under variable runner loads
globs: "tests/**"
---

# Hermetic Testing Timing & Benchmark Guardrails

1. **Headroom for Multi-Engine Integration Assertions**:
   - Never use tight micro-benchmark thresholds (< 500ms - 1000ms) inside standard regression test suites.
   - Shared CPU cores, Windows background indexing, and GitHub Actions virtual runners introduce 2x–5x latency jitter.
   - For integration monolith suites (e.g., 12-engine or 32-engine pipelines), allow reasonable timing ceilings (e.g., `< 5000.0 ms`) to verify termination without flaking.

2. **Dedicated Benchmark Separation**:
   - Isolate strict latency SLAs into dedicated benchmark runs (`pytest -m benchmark`) or performance telemetry scripts (`scripts/benchmarks/`), rather than blocking primary unit test gates.
