# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-16 16:42:24 UTC  
**Total Run Time:** 16.16 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.012 | 1,707.4 | 2.07 | 4.89 | 4.89 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 10,781.7 | 0.08 | 0.11 | 0.11 |
| **PyDB SELECT WHERE Query** | 200 | 0.033 | 6,061.9 | 0.16 | 0.27 | 0.28 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.011 | 925.7 | 2.17 | 2.87 | 2.87 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.040 | 5,005.9 | 0.17 | 0.26 | 0.34 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.324 | 30.8 | 0.59 | 40.05 | 40.05 |
| **PyGit Index Staging (150 files)** | 10 | 0.911 | 11.0 | 91.14 | 91.14 | 91.14 |
| **PyGit Tree Construction & Commit** | 1 | 0.404 | 2.5 | 403.57 | 403.57 | 403.57 |
| **PyShell Built-in Execution (echo)** | 20 | 0.003 | 6,776.9 | 0.05 | 0.07 | 0.07 |
| **PyShell File Redirection (>>)** | 20 | 0.009 | 2,172.8 | 0.39 | 0.74 | 0.74 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.038 | 5,315.3 | 0.04 | 0.07 | 0.57 |
| **PyTransformer Autoregressive Token Generation** | 15 | 13.818 | 1.1 | 905.24 | 1835.83 | 1835.83 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 51,813.5 | 0.02 | 0.02 | 0.02 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.004 | 510.2 | 0.09 | 0.09 | 0.09 |
| **PyChain Full Chain Verification** | 1 | 0.001 | 2,193.5 | 0.46 | 0.46 | 0.46 |
| **PySearch Document Indexing** | 20 | 0.001 | 18,052.2 | 0.05 | 0.06 | 0.06 |
| **PySearch BM25 Ranking Queries** | 150 | 0.010 | 15,526.2 | 0.06 | 0.07 | 0.08 |
| **PyVM Two-Pass Assembly** | 20 | 0.005 | 3,911.7 | 0.26 | 0.28 | 0.28 |
| **PyVM Factorial(10) Execution** | 20 | 0.006 | 3,351.4 | 0.29 | 0.35 | 0.35 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,933.2 | 0.09 | 0.11 | 0.11 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 253,164.7 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 52,659.3 | 0.01 | 0.03 | 0.03 |
