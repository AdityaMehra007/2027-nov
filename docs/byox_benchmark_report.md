# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-16 17:09:36 UTC  
**Total Run Time:** 17.16 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.012 | 1,697.0 | 2.48 | 5.24 | 5.24 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 13,182.2 | 0.06 | 0.11 | 0.11 |
| **PyDB SELECT WHERE Query** | 200 | 0.026 | 7,596.9 | 0.12 | 0.18 | 0.25 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.010 | 1,022.2 | 1.64 | 3.31 | 3.31 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.032 | 6,323.6 | 0.14 | 0.20 | 0.26 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.180 | 55.5 | 0.79 | 16.40 | 16.40 |
| **PyGit Index Staging (150 files)** | 10 | 0.642 | 15.6 | 64.16 | 64.16 | 64.16 |
| **PyGit Tree Construction & Commit** | 1 | 3.629 | 0.3 | 3628.99 | 3628.99 | 3628.99 |
| **PyShell Built-in Execution (echo)** | 20 | 0.075 | 265.3 | 0.07 | 0.08 | 0.08 |
| **PyShell File Redirection (>>)** | 20 | 0.006 | 3,396.1 | 0.26 | 0.41 | 0.41 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.021 | 9,406.9 | 0.02 | 0.04 | 0.42 |
| **PyTransformer Autoregressive Token Generation** | 15 | 12.388 | 1.2 | 729.15 | 1536.95 | 1536.95 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 111,358.6 | 0.01 | 0.01 | 0.01 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.001 | 3,163.6 | 0.27 | 0.27 | 0.27 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 4,490.4 | 0.22 | 0.22 | 0.22 |
| **PySearch Document Indexing** | 20 | 0.001 | 31,525.8 | 0.03 | 0.04 | 0.04 |
| **PySearch BM25 Ranking Queries** | 150 | 0.007 | 22,149.4 | 0.05 | 0.05 | 0.06 |
| **PyVM Two-Pass Assembly** | 20 | 0.004 | 5,631.1 | 0.17 | 0.20 | 0.20 |
| **PyVM Factorial(10) Execution** | 20 | 0.003 | 5,859.8 | 0.14 | 0.33 | 0.33 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,969.8 | 0.07 | 0.11 | 0.11 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 374,531.8 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 86,505.2 | 0.01 | 0.01 | 0.01 |
