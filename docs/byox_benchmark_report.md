# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:13:11 UTC  
**Total Run Time:** 14.78 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.015 | 1,363.3 | 2.44 | 6.74 | 6.74 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 9,011.9 | 0.10 | 0.12 | 0.12 |
| **PyDB SELECT WHERE Query** | 200 | 0.036 | 5,484.9 | 0.17 | 0.27 | 0.34 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.012 | 835.3 | 2.17 | 3.95 | 3.95 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.048 | 4,210.6 | 0.21 | 0.34 | 0.51 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.086 | 116.4 | 1.02 | 1.37 | 1.37 |
| **PyGit Index Staging (150 files)** | 10 | 0.048 | 207.5 | 4.82 | 4.82 | 4.82 |
| **PyGit Tree Construction & Commit** | 1 | 0.111 | 9.0 | 111.09 | 111.09 | 111.09 |
| **PyShell Built-in Execution (echo)** | 20 | 0.003 | 7,580.4 | 0.03 | 0.04 | 0.04 |
| **PyShell File Redirection (>>)** | 20 | 0.007 | 3,033.5 | 0.31 | 0.45 | 0.45 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.034 | 5,971.9 | 0.04 | 0.07 | 0.42 |
| **PyTransformer Autoregressive Token Generation** | 15 | 14.307 | 1.1 | 979.18 | 1768.77 | 1768.77 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 92,506.9 | 0.01 | 0.01 | 0.01 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.001 | 2,628.1 | 0.09 | 0.09 | 0.09 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 4,113.5 | 0.24 | 0.24 | 0.24 |
| **PySearch Document Indexing** | 20 | 0.000 | 46,008.7 | 0.02 | 0.03 | 0.03 |
| **PySearch BM25 Ranking Queries** | 150 | 0.004 | 36,281.8 | 0.03 | 0.04 | 0.05 |
| **PyVM Two-Pass Assembly** | 20 | 0.005 | 4,236.8 | 0.27 | 0.30 | 0.30 |
| **PyVM Factorial(10) Execution** | 20 | 0.003 | 6,413.1 | 0.15 | 0.17 | 0.17 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,879.0 | 0.07 | 0.10 | 0.10 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 363,636.5 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 83,752.1 | 0.01 | 0.01 | 0.01 |
