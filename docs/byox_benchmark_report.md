# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 16:06:42 UTC  
**Total Run Time:** 16.89 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.016 | 1,243.6 | 3.40 | 8.07 | 8.07 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 9,374.3 | 0.09 | 0.16 | 0.16 |
| **PyDB SELECT WHERE Query** | 200 | 0.032 | 6,322.2 | 0.17 | 0.27 | 0.31 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.015 | 683.1 | 2.69 | 4.23 | 4.23 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.054 | 3,699.3 | 0.21 | 0.38 | 0.49 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.078 | 128.6 | 0.83 | 1.46 | 1.46 |
| **PyGit Index Staging (150 files)** | 10 | 0.027 | 372.1 | 2.69 | 2.69 | 2.69 |
| **PyGit Tree Construction & Commit** | 1 | 0.018 | 55.5 | 18.02 | 18.02 | 18.02 |
| **PyShell Built-in Execution (echo)** | 20 | 0.003 | 7,723.2 | 0.04 | 0.08 | 0.08 |
| **PyShell File Redirection (>>)** | 20 | 0.007 | 2,870.7 | 0.32 | 0.42 | 0.42 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.035 | 5,722.8 | 0.04 | 0.06 | 0.70 |
| **PyTransformer Autoregressive Token Generation** | 15 | 16.468 | 0.9 | 939.98 | 2207.49 | 2207.49 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 52,910.1 | 0.02 | 0.02 | 0.02 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.002 | 1,122.6 | 0.89 | 0.89 | 0.89 |
| **PyChain Full Chain Verification** | 1 | 0.001 | 1,548.5 | 0.65 | 0.65 | 0.65 |
| **PySearch Document Indexing** | 20 | 0.001 | 16,123.8 | 0.06 | 0.07 | 0.07 |
| **PySearch BM25 Ranking Queries** | 150 | 0.008 | 17,784.1 | 0.05 | 0.09 | 0.10 |
| **PyVM Two-Pass Assembly** | 20 | 0.006 | 3,114.6 | 0.31 | 0.37 | 0.37 |
| **PyVM Factorial(10) Execution** | 20 | 0.006 | 3,360.2 | 0.32 | 0.46 | 0.46 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.005 | 1,920.2 | 0.07 | 0.13 | 0.13 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 268,817.3 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 63,979.5 | 0.01 | 0.02 | 0.02 |
