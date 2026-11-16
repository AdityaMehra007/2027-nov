# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-16 17:11:45 UTC  
**Total Run Time:** 13.55 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.026 | 764.8 | 4.54 | 11.91 | 11.91 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.006 | 3,342.8 | 0.16 | 1.19 | 1.19 |
| **PyDB SELECT WHERE Query** | 200 | 0.051 | 3,960.3 | 0.26 | 0.33 | 0.41 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.016 | 621.4 | 2.91 | 4.69 | 4.69 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.057 | 3,482.8 | 0.27 | 0.36 | 0.48 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.010 | 996.4 | 0.84 | 1.60 | 1.60 |
| **PyGit Index Staging (150 files)** | 10 | 0.026 | 386.6 | 2.59 | 2.59 | 2.59 |
| **PyGit Tree Construction & Commit** | 1 | 0.016 | 62.8 | 15.91 | 15.91 | 15.91 |
| **PyShell Built-in Execution (echo)** | 20 | 0.001 | 38,066.2 | 0.02 | 0.03 | 0.03 |
| **PyShell File Redirection (>>)** | 20 | 0.006 | 3,160.8 | 0.31 | 0.45 | 0.45 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.032 | 6,218.1 | 0.04 | 0.06 | 0.47 |
| **PyTransformer Autoregressive Token Generation** | 15 | 13.238 | 1.1 | 864.44 | 1558.17 | 1558.17 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 110,132.2 | 0.01 | 0.01 | 0.01 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.000 | 4,511.6 | 0.07 | 0.07 | 0.07 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 4,411.1 | 0.23 | 0.23 | 0.23 |
| **PySearch Document Indexing** | 20 | 0.000 | 48,007.7 | 0.02 | 0.03 | 0.03 |
| **PySearch BM25 Ranking Queries** | 150 | 0.005 | 30,410.5 | 0.03 | 0.05 | 0.07 |
| **PyVM Two-Pass Assembly** | 20 | 0.002 | 9,454.9 | 0.10 | 0.11 | 0.11 |
| **PyVM Factorial(10) Execution** | 20 | 0.002 | 8,355.6 | 0.12 | 0.12 | 0.12 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,935.8 | 0.06 | 0.11 | 0.11 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 367,647.0 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 87,489.1 | 0.01 | 0.01 | 0.01 |
