# BYOX 10-Engine Multi-System Benchmark Report

**Generated:** 2026-11-15 20:34:11 UTC  
**Total Run Time:** 14.09 seconds  
**Engines Evaluated:** 10 Systems (22 Benchmarks)

| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **PyRedis Concurrent SET** | 20 | 0.014 | 1,457.3 | 2.47 | 5.61 | 5.61 |
| **PyRedis Pipelined GET (50-op batch)** | 0 | 0.000 | 0.0 | 0.00 | 0.00 | 0.00 |
| **PyDB Row Insertion** | 20 | 0.002 | 10,227.6 | 0.08 | 0.10 | 0.10 |
| **PyDB SELECT WHERE Query** | 200 | 0.021 | 9,317.4 | 0.09 | 0.19 | 0.27 |
| **PyWeb HTTP/1.1 JSON Request** | 10 | 0.009 | 1,057.3 | 1.68 | 2.74 | 2.74 |
| **PyWeb WebSocket Frame Roundtrip** | 200 | 0.042 | 4,737.8 | 0.17 | 0.34 | 0.44 |
| **PyGit Object Hashing & zlib Compression** | 10 | 0.227 | 44.0 | 1.01 | 53.46 | 53.46 |
| **PyGit Index Staging (150 files)** | 10 | 0.153 | 65.4 | 15.29 | 15.29 | 15.29 |
| **PyGit Tree Construction & Commit** | 1 | 0.266 | 3.8 | 265.82 | 265.82 | 265.82 |
| **PyShell Built-in Execution (echo)** | 20 | 0.029 | 679.3 | 0.06 | 0.11 | 0.11 |
| **PyShell File Redirection (>>)** | 20 | 0.007 | 2,794.0 | 0.34 | 0.44 | 0.44 |
| **PyTransformer Autograd Graph Backprop** | 200 | 0.028 | 7,101.5 | 0.03 | 0.09 | 0.48 |
| **PyTransformer Autoregressive Token Generation** | 15 | 13.149 | 1.1 | 821.54 | 1593.07 | 1593.07 |
| **PyChain Transaction Ingestion** | 10 | 0.000 | 48,661.8 | 0.02 | 0.02 | 0.02 |
| **PyChain Block Mining (Diff=1)** | 2 | 0.001 | 1,903.0 | 0.18 | 0.18 | 0.18 |
| **PyChain Full Chain Verification** | 1 | 0.000 | 4,413.1 | 0.23 | 0.23 | 0.23 |
| **PySearch Document Indexing** | 20 | 0.000 | 51,440.3 | 0.02 | 0.02 | 0.02 |
| **PySearch BM25 Ranking Queries** | 150 | 0.007 | 21,091.7 | 0.04 | 0.07 | 0.09 |
| **PyVM Two-Pass Assembly** | 20 | 0.003 | 8,072.3 | 0.10 | 0.17 | 0.17 |
| **PyVM Factorial(10) Execution** | 20 | 0.006 | 3,333.2 | 0.28 | 0.46 | 0.46 |
| **PyControlPlane End-to-End Invocations** | 10 | 0.006 | 1,760.9 | 0.10 | 0.14 | 0.14 |
| **PyControlPlane Semantic Vector Lookups** | 10 | 0.000 | 233,100.2 | 0.00 | 0.00 | 0.00 |
| **PyControlPlane Merkle Audit SHA-256 Chaining** | 10 | 0.000 | 42,844.9 | 0.02 | 0.03 | 0.03 |
