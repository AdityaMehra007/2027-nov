# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:16:06 UTC  
**Total Run Time:** 15.58 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.021 | 961.9 | 4.40 | 10.27 | 10.27 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.003 | 6,299.8 | 0.14 | 0.19 | 0.19 |
| **PyDB SELECT WHERE Query** | 200 | 0.051 | 3,892.3 | 0.23 | 0.39 | 0.52 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.021 | 485.4 | 3.70 | 6.59 | 6.59 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.076 | 2,625.3 | 0.31 | 0.55 | 0.93 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.111 | 90.2 | 0.91 | 1.22 | 1.22 |
| **PyGit Index Staging (150 files)** | 10 | 0.034 | 294.7 | 3.39 | 3.39 | 3.39 |
| **PyGit Tree Construction & Commit** | 1 | 0.023 | 43.9 | 22.79 | 22.79 | 22.79 |
| **PyShell Built-in Execution (echo)** | 20 | 0.002 | 9,672.6 | 0.03 | 0.04 | 0.04 |
| **PyShell File Redirection (>>)** | 20 | 0.006 | 3,557.4 | 0.26 | 0.38 | 0.38 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.034 | 5,834.0 | 0.04 | 0.06 | 0.41 |
| **PyTransformer Autoregressive Token Generation** | 15 | 14.996 | 1.0 | 1003.85 | 1769.10 | 1769.10 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 48,852.0 | 0.02 | 0.02 | 0.02 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.003 | 640.2 | 0.41 | 0.41 | 0.41 |
| **PyChain Full Chain Verification** | 1 | 0.001 | 2,172.0 | 0.46 | 0.46 | 0.46 |
| **PySearch Document Indexing** | 20 | 0.005 | 4,342.2 | 0.06 | 0.08 | 0.08 |
| **PySearch BM25 Ranking Queries** | 150 | 0.009 | 17,375.4 | 0.06 | 0.09 | 0.10 |
| **PyVM Two-Pass Assembly** | 20 | 0.004 | 5,539.6 | 0.18 | 0.21 | 0.21 |
| **PyVM Factorial(10) Execution** | 20 | 0.011 | 1,792.3 | 0.42 | 1.12 | 1.12 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.006 | 1,652.1 | 0.11 | 0.15 | 0.15 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 170,068.0 | 0.01 | 0.01 | 0.01 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 43,956.0 | 0.02 | 0.02 | 0.02 |
