# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:14:54 UTC  
**Total Run Time:** 21.15 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.023 | 885.9 | 3.64 | 8.67 | 8.67 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.004 | 5,431.7 | 0.16 | 0.26 | 0.26 |
| **PyDB SELECT WHERE Query** | 200 | 0.043 | 4,682.8 | 0.17 | 0.31 | 0.64 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.021 | 474.0 | 3.82 | 5.07 | 5.07 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.071 | 2,818.1 | 0.28 | 0.39 | 1.68 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.015 | 668.0 | 0.79 | 1.38 | 1.38 |
| **PyGit Index Staging (150 files)** | 10 | 0.049 | 202.5 | 4.94 | 4.94 | 4.94 |
| **PyGit Tree Construction & Commit** | 1 | 0.177 | 5.6 | 177.43 | 177.43 | 177.43 |
| **PyShell Built-in Execution (echo)** | 20 | 0.005 | 3,702.5 | 0.08 | 0.11 | 0.11 |
| **PyShell File Redirection (>>)** | 20 | 0.008 | 2,494.6 | 0.39 | 0.45 | 0.45 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.040 | 4,975.4 | 0.05 | 0.09 | 0.66 |
| **PyTransformer Autoregressive Token Generation** | 15 | 20.566 | 0.7 | 1344.04 | 2634.01 | 2634.01 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 48,285.8 | 0.02 | 0.02 | 0.02 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.002 | 1,236.0 | 0.31 | 0.31 | 0.31 |
| **PyChain Full Chain Verification** | 1 | 0.001 | 2,133.6 | 0.47 | 0.47 | 0.47 |
| **PySearch Document Indexing** | 20 | 0.001 | 14,804.9 | 0.06 | 0.06 | 0.06 |
| **PySearch BM25 Ranking Queries** | 150 | 0.022 | 6,773.9 | 0.07 | 0.09 | 0.22 |
| **PyVM Two-Pass Assembly** | 20 | 0.012 | 1,665.7 | 0.29 | 0.35 | 0.35 |
| **PyVM Factorial(10) Execution** | 20 | 0.010 | 2,016.6 | 0.48 | 0.56 | 0.56 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.012 | 858.1 | 0.10 | 2.96 | 2.96 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 155,038.7 | 0.01 | 0.01 | 0.01 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 37,119.5 | 0.02 | 0.03 | 0.03 |
