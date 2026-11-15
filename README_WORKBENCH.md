# BYOX Studio & Interactive Visual Workbench

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Zero Runtime Dependencies](https://img.shields.io/badge/dependencies-0%20(Standard%20Library%20Only)-success.svg)]()
[![Test Suite Passing](https://img.shields.io/badge/tests-72%2F72%20passing-brightgreen.svg)]()

> **The Definitive Built-From-Scratch Systems Engineering Studio.**
> An integrated, real-time visual workbench and multi-engine benchmark harness powering 6 canonical systems built entirely from first principles using **100% Python 3.13 Standard Library**—zero external runtime packages, frameworks, or wrappers.

---

## 1. Architectural Architecture

```mermaid
flowchart TD
    subgraph Browser["Modern Web Browser Client"]
        UI["BYOX Studio UI (Dark Glassmorphism)"]
        WSTerm["WebSocket xterm Terminal"]
        WSLLM["WebSocket LLM Token Streamer"]
        REST["REST API Client (Fetch)"]
    end

    subgraph Server["PyWeb Async Core (RFC 6455 & HTTP/1.1)"]
        Router["Route Dispatcher (/api/* & /ws/*)"]
        PagingBuffer["HTTP Body Pager & Streaming Parser"]
    end

    subgraph Engines["Canonical Built-From-Scratch Engines"]
        Redis["PyRedis\n(RESP2, In-Memory KV, TTL Sweeper, AOF)"]
        DB["PyDB\n(Paged 4KB B-Tree, SQL Lexer/Parser, Disk Pager)"]
        Git["PyGit\n(Content-Addressed Store, DIRC v2 Index, Merkle Tree)"]
        Shell["PyShell\n(Pipeline Parser, I/O Redirection, Builtins)"]
        Transformer["PyTransformer\n(Scalar Autograd DAG, Multi-Head Attention)"]
        Bench["BYOX Benchmark Harness\n(Microsecond Telemetry & Percentiles)"]
    end

    UI --> REST
    WSTerm -->|ws://host:port/ws/shell| Router
    WSLLM -->|ws://host:port/ws/llm| Router
    REST -->|http://host:port/api/*| Router

    Router --> Redis
    Router --> DB
    Router --> Git
    Router --> Shell
    Router --> Transformer
    Router --> Bench
```

---

## 2. Integrated Systems Portfolio

All engines were constructed without third-party frameworks:

| System | Canonical Equivalent | Architecture & Core Capabilities | Spec Compliance |
| :--- | :--- | :--- | :--- |
| **PyRedis** | Redis 7.x | Streaming byte RESP2 parser, thread-safe in-memory store (Strings, Lists, Hashes), active (100ms) & passive TTL expiration sweep, Append-Only File (AOF) persistence & reconstruction. | RESP2 Protocol |
| **PyGit** | Git Core | Content-addressed SHA-1 zlib object store (`Blob`, `Tree`, `Commit`), binary DIRC v2 index parser/writer, branch reference manager, working tree status checker, unified diff generator. | Git Object & Index v2 |
| **PyDB** | SQLite 3 | Paged 4KB binary disk pager with dirty-page writeback, binary row serializer (`INTEGER`, `REAL`, `TEXT`), recursive-descent SQL parser (`CREATE`, `INSERT`, `SELECT`, `WHERE`), full table scan evaluator. | ANSI SQL-92 Subset |
| **PyShell** | Bash / Zsh | Lexical tokenizer supporting single/double quote escaping, pipeline parser (`\|`), file redirection (`>`, `>>`, `<`, `2>`, `2>&1`), built-in command dispatcher (`cd`, `pwd`, `echo`, `export`, `history`). | POSIX Shell Subset |
| **PyWeb** | ASGI / Uvicorn | Asynchronous HTTP/1.1 streaming parser, request/response models, query parameter extractor, RFC 6455 WebSocket engine with XOR frame masking/unmasking and ping/pong control. | RFC 2616 / RFC 6455 |
| **PyTransformer** | nanoGPT / LLaMA | Scalar autograd computational graph engine (`Value.backward()`), causal multi-head self-attention, feed-forward layers, positional embeddings, character tokenizer, autoregressive generation. | Transformer Architecture |

---

## 3. Interactive Studio Tabs

The Visual Workbench UI (`src/byox/workbench/static/index.html`) provides a responsive, dark glassmorphism dashboard organized into 7 specialized workspaces:

### Tab 1: System Overview & Telemetry
- **Live Status Badges**: Operational status across all 6 engines, process uptime, memory allocations, and socket bindings.
- **Engine Metrics**: Real-time display of active Redis keys, DB page counts, Git branch & HEAD SHA, shell command counts, and transformer embedding dimensions.

### Tab 2: PyRedis Keyspace & Command Console
- **Interactive Command REPL**: Send raw Redis commands (`SET`, `GET`, `HSET`, `HGETALL`, `RPUSH`, `LRANGE`, `TTL`, `EXPIRE`) directly to the backend dispatcher.
- **Visual Keyspace Table**: Live view of all active keys, types, TTL countdowns, and stored values with automatic refresh.

### Tab 3: PyDB SQL Studio & Buffer Pager
- **SQL Query Editor**: Execute ANSI SQL queries against the 4KB paged binary database on disk.
- **Data Grid View**: Tabular presentation of returned columns and rows with execution time in milliseconds.
- **Disk Buffer Telemetry**: Real-time page count, total storage size, and pager buffer allocation statistics.

### Tab 4: PyGit Visual Commit Graph & Diff Viewer
- **Commit History Graph**: Visual timeline of commits showing SHA-1 hashes, author information, and commit messages.
- **Branch Selector & Working Tree Status**: Live inspection of staged files, modified unstaged files, and untracked artifacts.

### Tab 5: PyShell Interactive Terminal Emulator
- **WebSocket Pseudo-Terminal**: Full-duplex interactive terminal connected via `/ws/shell`.
- **Pipeline & Redirection**: Run shell commands, inspect environmental variables, change directories, and test input/output pipelines with ANSI color codes.

### Tab 6: PyTransformer Token Generator Playground
- **Autoregressive Inference**: Stream tokens character-by-character over `/ws/llm` in real time.
- **Model Hyperparameters**: Display of vocabulary size, embedding dimensions (32-d), attention heads (4), and context window size (24 tokens).

### Tab 7: Multi-Engine Benchmark Dashboard
- **Comparative Latency Gauges**: Interactive cards displaying operations per second, mean latency, p50, p95, and p99 percentiles across all engines.
- **Stress Testing Data**: Visualization of throughput under simulated concurrent workload.

---

## 4. Benchmark Performance & Stress Metrics

All benchmarks run natively without external instrumentation (`python -m byox.benchmarks.runner`):

| Engine Benchmark | Total Ops | Throughput | Mean Latency | p50 Latency | p95 Latency | p99 Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PyRedis Concurrent SET/GET** | 500 reqs | **4,340 ops/sec** | 2.19 ms | 1.86 ms | 3.99 ms | 5.86 ms |
| **PyDB 4KB Paged Bulk Insert** | 500 rows | **8,535 rows/sec** | 0.11 ms | 0.10 ms | 0.20 ms | 0.38 ms |
| **PyDB Filtered SELECT Scan** | 100 queries | **343 qps** | 2.87 ms | 2.76 ms | 4.09 ms | 4.88 ms |
| **PyWeb Concurrent HTTP/1.1** | 300 reqs | **4,195 req/sec** | 1.15 ms | 0.98 ms | 2.50 ms | 3.91 ms |
| **PyWeb WebSocket Ping-Pong** | 200 frames | **4,584 fps** | 0.21 ms | 0.20 ms | 0.31 ms | 0.44 ms |
| **PyGit Object Hashing (SHA-1/zlib)** | 100 objects | **3,088 ops/sec** | 0.31 ms | 0.29 ms | 0.50 ms | 0.81 ms |
| **PyGit DIRC v2 Tree Construction** | 100 entries | **2,476 ops/sec** | 0.39 ms | 0.37 ms | 0.62 ms | 0.99 ms |
| **PyShell Builtin Execution** | 300 cmds | **14,038 ops/sec** | 0.07 ms | 0.05 ms | 0.14 ms | 0.26 ms |
| **PyTransformer Autograd Graph** | 200 steps | **3,548 steps/sec** | 0.07 ms | 0.06 ms | 0.12 ms | 0.21 ms |
| **PyTransformer Forward Attention** | 20 passes | **232 passes/sec** | 4.28 ms | 4.19 ms | 5.48 ms | 5.92 ms |

---

## 5. REST & WebSocket API Reference

The workbench exposes a clean REST and WebSocket interface:

| Endpoint | Protocol | Method | Description |
| :--- | :--- | :--- | :--- |
| `/` | HTTP/1.1 | `GET` | Serves the single-page application dashboard |
| `/api/status` | HTTP/1.1 | `GET` | Returns uptime, operational status, and engine statistics |
| `/api/redis/command` | HTTP/1.1 | `POST` | Executes a raw Redis command line (`{"command": "..."}`) |
| `/api/redis/keys` | HTTP/1.1 | `GET` | Lists all active keys, types, TTLs, and value previews |
| `/api/db/query` | HTTP/1.1 | `POST` | Executes an SQL query string (`{"sql": "..."}`) |
| `/api/git/graph` | HTTP/1.1 | `GET` | Returns commit history, branches, and staged/modified status |
| `/api/benchmarks` | HTTP/1.1 | `GET` | Returns the latest multi-engine benchmark results and percentiles |
| `/ws/shell` | RFC 6455 WS | Upgrade | Bidirectional interactive terminal session |
| `/ws/llm` | RFC 6455 WS | Upgrade | Streaming token generation (`{"prompt": "...", "tokens": 10}`) |

---

## 6. Quick Start & Launcher

### Launch the Visual Workbench

```bash
# Launch with default settings (127.0.0.1:9000)
python launch_workbench.py

# Launch and automatically open your default browser
python launch_workbench.py --open-browser

# Custom port and database location
python launch_workbench.py --port 8080 --db data/custom.db
```

Once running, navigate to:
```
http://127.0.0.1:9000/
```

### Run Multi-Engine Benchmarks

```bash
# Run the complete multi-engine benchmark suite
python -m byox.benchmarks.runner
```
Benchmark outputs are saved automatically to:
- `data/byox_benchmark_results.json`
- `docs/byox_benchmark_report.md`

### Run Verification Test Suite

```bash
# Run the complete test suite (72 tests passing)
python -m unittest discover tests/ -p "test_*.py"

# Or using pytest
python -m pytest tests/test_byox_benchmarks.py tests/test_byox_workbench.py
```

---

## 7. Standards & Verification

- **Pure Standard Library**: Validated with zero external packages in runtime dependencies.
- **TDD Compliance**: Strict red-green-refactor methodology across all engines.
- **Platform Agnostic**: Fully tested and verified on Windows, Linux, and macOS.
