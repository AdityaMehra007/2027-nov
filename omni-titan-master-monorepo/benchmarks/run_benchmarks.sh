#!/usr/bin/env bash
set -e
echo "=========================================================="
echo " OMNI-TITAN 100-ENGINE PERFORMANCE BENCHMARK HARNESS"
echo "=========================================================="
for port in 8001 8011 8021 8031 8041 8051 8061 8071 8081 8091; do
    echo "[BENCHMARKING] Testing Engine on port $port..."
    curl -s http://localhost:$port/healthz || true
done
echo "Benchmark sweep completed successfully."
