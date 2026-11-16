# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-16 17:10:26 UTC  
**Total Run Time:** 13.93 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 500 | 0.131 | 3,824.9 | 2.62 | 3.18 | 3.31 |
| **PyRedis Pipelined GET (50-op batch)** | 10 | 0.016 | 616.7 | 1.51 | 1.58 | 1.58 |
| **PyDB Row Insertion** | 500 | 0.062 | 8,091.9 | 0.10 | 0.17 | 0.20 |
| **PyDB SELECT WHERE Query** | 200 | 0.431 | 463.8 | 2.24 | 3.10 | 4.49 |
| **PyWeb HTTP/1.1 JSON Request** | 300 | 0.235 | 1,278.7 | 1.58 | 1.96 | 2.21 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.031 | 6,537.1 | 0.15 | 0.17 | 0.21 |
| **PyGit Object Hashing & zlib Compression** | 100 | 0.071 | 1,412.7 | 0.63 | 0.74 | 0.84 |
| **PyGit Index Staging (150 files)** | 100 | 1.118 | 89.5 | 11.18 | 11.18 | 11.18 |
| **PyGit Tree Construction & Commit** | 1 | 0.077 | 13.0 | 77.18 | 77.18 | 77.18 |
| **PyShell Built-in Execution (echo)** | 300 | 0.011 | 26,027.7 | 0.03 | 0.05 | 0.07 |
| **PyShell File Redirection (>>)** | 300 | 0.070 | 4,266.6 | 0.23 | 0.30 | 0.37 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.021 | 9,545.4 | 0.03 | 0.04 | 0.32 |
| **PyTransformer Autoregressive Token Generation** | 15 | 10.630 | 1.4 | 535.82 | 1459.04 | 1459.04 |
| **PyChain Transaction Ingestion** | 100 | 0.008 | 12,570.2 | 0.04 | 0.06 | 0.08 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.027 | 74.7 | 0.19 | 0.19 | 0.19 |
| **PyChain Full Chain Verification** | 1 | 0.003 | 333.4 | 3.00 | 3.00 | 3.00 |
| **PySearch Document Indexing** | 300 | 0.014 | 21,299.6 | 0.04 | 0.05 | 0.06 |
| **PySearch BM25 Ranking Queries** | 150 | 0.046 | 3,227.2 | 0.34 | 0.44 | 0.51 |
| **PyVM Two-Pass Assembly** | 300 | 0.061 | 4,912.0 | 0.18 | 0.32 | 0.37 |
| **PyVM Factorial(10) Execution** | 300 | 0.050 | 6,035.5 | 0.11 | 0.30 | 0.48 |
| **PyControlPlane End-to-End Invocations** | 150 | 0.012 | 12,713.0 | 0.04 | 0.06 | 0.07 |
| **PyControlPlane Semantic Vector Lookups** | 150 | 0.000 | 510,725.2 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 150 | 0.002 | 90,203.9 | 0.01 | 0.02 | 0.02 |
