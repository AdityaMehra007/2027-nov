# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:14:09 UTC  
**Total Run Time:** 18.89 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.024 | 832.7 | 3.77 | 9.29 | 9.29 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.003 | 6,413.1 | 0.14 | 0.17 | 0.17 |
| **PyDB SELECT WHERE Query** | 200 | 0.061 | 3,264.4 | 0.28 | 0.38 | 1.52 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.027 | 371.5 | 3.01 | 5.66 | 5.66 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.076 | 2,612.7 | 0.30 | 0.48 | 1.84 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.020 | 492.1 | 0.92 | 1.12 | 1.12 |
| **PyGit Index Staging (150 files)** | 10 | 0.108 | 92.6 | 10.80 | 10.80 | 10.80 |
| **PyGit Tree Construction & Commit** | 1 | 0.027 | 37.5 | 26.70 | 26.70 | 26.70 |
| **PyShell Built-in Execution (echo)** | 20 | 0.009 | 2,334.1 | 0.08 | 1.76 | 1.76 |
| **PyShell File Redirection (>>)** | 20 | 0.010 | 1,966.8 | 0.41 | 0.92 | 0.92 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.050 | 3,966.4 | 0.04 | 0.10 | 0.79 |
| **PyTransformer Autoregressive Token Generation** | 15 | 18.355 | 0.8 | 1333.82 | 2150.76 | 2150.76 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 77,760.5 | 0.01 | 0.01 | 0.01 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.003 | 793.1 | 0.63 | 0.63 | 0.63 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 3,456.6 | 0.29 | 0.29 | 0.29 |
| **PySearch Document Indexing** | 20 | 0.001 | 24,102.2 | 0.04 | 0.05 | 0.05 |
| **PySearch BM25 Ranking Queries** | 150 | 0.009 | 16,091.7 | 0.06 | 0.07 | 0.09 |
| **PyVM Two-Pass Assembly** | 20 | 0.006 | 3,564.4 | 0.28 | 0.30 | 0.30 |
| **PyVM Factorial(10) Execution** | 20 | 0.007 | 2,833.5 | 0.35 | 0.47 | 0.47 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,827.0 | 0.09 | 0.12 | 0.12 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 235,849.0 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 42,535.1 | 0.01 | 0.04 | 0.04 |
