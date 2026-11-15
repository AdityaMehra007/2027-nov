# Build-Your-Own-X: Canonical Systems Suite from Scratch

Inspired by [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x), this repository contains six canonical, high-performance computing systems built entirely from scratch in Python 3.13 standard library with **zero external dependencies**.

Every system features complete test coverage, documented architecture, and CLI interfaces.

---

## The 6 Flagship Systems

| # | System | Package | Core Technologies & Protocols | Tests | Documentation |
|---|---|---|---|:---:|---|
| **0** | **PyRedis** | `src/pyredis/` | RESP2 Protocol Streaming, Dual-tier TTL (Passive + Active Sweeper), AOF Persistence, Asyncio TCP Server | 33 | [`README_REDIS.md`](./README_REDIS.md) |
| **1** | **PyGit** | `src/pygit/` | Canonical Object Store (`blob`, `tree`, `commit`, SHA-1, zlib), DIRC v2 Binary Index, Porcelain CLI (`add`, `commit`, `status`, `log`, `branch`, `checkout`, `diff`) | 11 | [`README_PYGIT.md`](./README_PYGIT.md) |
| **2** | **PyDB** | `src/pydb/` | 4KB Paged Disk Storage, Buffer Pool Pager, SQL Lexer & Recursive-Descent Parser, Binary Row Serializer, WHERE Filtering, REPL | 5 | [`README_PYDB.md`](./README_PYDB.md) |
| **3** | **PyShell** | `src/pyshell/` | Quote Tokenizer, Command Pipelines (`\|`), File Redirection (`>`, `>>`, `<`, `2>&1`), Shell Builtins (`cd`, `pwd`, `echo`, `export`, `history`, `type`, `which`) | 4 | [`README_PYSHELL.md`](./README_PYSHELL.md) |
| **4** | **PyWeb** | `src/pyweb/` | Async HTTP/1.1 Streaming Parser, RFC 6455 WebSocket Handshake & Masked Frame Engine, Route Decorators, JSON/HTML Utilities | 6 | [`README_PYWEB.md`](./README_PYWEB.md) |
| **5** | **PyTransformer** | `src/pytransformer/` | Scalar Autograd Computational Graph (`Value.backward()`), Multi-Head Causal Self-Attention, Positional Embeddings, Autoregressive Generator | 4 | [`README_PYTRANSFORMER.md`](./README_PYTRANSFORMER.md) |

---

## Unified Test Suite (63/63 Passing)

Run the full suite across all 6 systems in one command:

```bash
python -m unittest tests/test_protocol.py tests/test_store.py tests/test_store_active_ttl.py tests/test_commands.py tests/test_persistence.py tests/test_server_integration.py tests/test_pygit_objects.py tests/test_pygit_index.py tests/test_pygit_repo.py tests/test_pygit_status_diff.py tests/test_pygit_e2e.py tests/test_pydb_storage.py tests/test_pydb_engine.py tests/test_pyshell.py tests/test_pyweb.py tests/test_pyweb_integration.py tests/test_pytransformer.py
```

```
...............................................................
----------------------------------------------------------------------
Ran 63 tests in 7.699s

OK
```
