# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:04:19 UTC  
**Total Run Time:** 15.73 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.018 | 1,136.3 | 2.22 | 5.09 | 5.09 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 8,498.3 | 0.10 | 0.14 | 0.14 |
| **PyDB SELECT WHERE Query** | 200 | 0.036 | 5,607.9 | 0.17 | 0.28 | 0.35 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.017 | 601.1 | 2.88 | 5.73 | 5.73 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.058 | 3,456.2 | 0.25 | 0.38 | 0.50 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.172 | 58.0 | 0.85 | 0.99 | 0.99 |
| **PyGit Index Staging (150 files)** | 10 | 0.030 | 333.2 | 3.00 | 3.00 | 3.00 |
| **PyGit Tree Construction & Commit** | 1 | 0.018 | 54.6 | 18.31 | 18.31 | 18.31 |
| **PyShell Built-in Execution (echo)** | 20 | 0.003 | 7,282.0 | 0.06 | 0.08 | 0.08 |
| **PyShell File Redirection (>>)** | 20 | 0.008 | 2,575.2 | 0.38 | 0.49 | 0.49 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.036 | 5,528.7 | 0.04 | 0.07 | 0.53 |
| **PyTransformer Autoregressive Token Generation** | 15 | 15.135 | 1.0 | 1025.14 | 1992.86 | 1992.86 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 43,630.0 | 0.02 | 0.03 | 0.03 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.003 | 740.0 | 0.12 | 0.12 | 0.12 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 2,895.2 | 0.34 | 0.34 | 0.34 |
| **PySearch Document Indexing** | 20 | 0.001 | 18,345.3 | 0.05 | 0.06 | 0.06 |
| **PySearch BM25 Ranking Queries** | 150 | 0.009 | 16,792.2 | 0.05 | 0.09 | 0.15 |
| **PyVM Two-Pass Assembly** | 20 | 0.005 | 3,971.7 | 0.25 | 0.30 | 0.30 |
| **PyVM Factorial(10) Execution** | 20 | 0.006 | 3,169.9 | 0.30 | 0.48 | 0.48 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,919.0 | 0.06 | 0.11 | 0.11 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 366,300.3 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 86,355.8 | 0.01 | 0.01 | 0.01 |
