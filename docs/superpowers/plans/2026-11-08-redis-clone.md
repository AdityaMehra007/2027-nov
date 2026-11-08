# Python Redis Clone Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a zero-dependency, RESP2-compliant in-memory Redis clone in Python 3.13 (`asyncio`) supporting strings, lists, hashes, dual-tier TTL expiration, and Append-Only File (AOF) persistence.

**Architecture:** Layered event-driven architecture separating protocol parsing (`protocol.py`), in-memory storage with passive/active TTL sweeps (`store.py`), command validation & dispatch (`commands.py`), AOF persistence logging and replay (`persistence.py`), and concurrent TCP socket handling (`server.py` and `cli.py`).

**Tech Stack:** Python 3.13+, Python Standard Library only (`asyncio`, `socket`, `collections`, `time`, `dataclasses`, `os`, `sys`, `unittest`, `argparse`).

**Spec:** [`docs/superpowers/specs/2026-11-08-redis-clone-design.md`](file:///e:/2027%20nov/docs/superpowers/specs/2026-11-08-redis-clone-design.md)

## Global Constraints

- Python Standard Library ONLY (zero external packages like redis-py, hiredis, or twisted).
- Strict RESP2 line formatting with `\r\n` (CRLF) delimiters.
- Binary-safe bulk strings (handles arbitrary bytes/unicode).
- Pipelined and fragmented TCP packet handling without frame corruption.
- Case-insensitive command names (`get`, `GET`, `Get`).
- All tests must pass using Python's standard `unittest` or `pytest`.

---

### Task 1: RESP2 Protocol Serializer & Streaming Deserializer

**Files:**
- Create: `src/pyredis/__init__.py`
- Create: `src/pyredis/protocol.py`
- Test: `tests/test_protocol.py`

**Interfaces:**
- Produces:
  - `class RESPError(Exception)`
  - `class RESPParser`:
    - `feed(chunk: bytes) -> None`
    - `get_next_object() -> Optional[Any]` (returns parsed object: `str`, `int`, `bytes`, `list`, or `None` if incomplete)
    - `get_all_objects() -> list[Any]`
  - `serialize_simple_string(val: str) -> bytes`
  - `serialize_error(msg: str) -> bytes`
  - `serialize_integer(num: int) -> bytes`
  - `serialize_bulk_string(data: Optional[bytes | str]) -> bytes`
  - `serialize_array(items: Optional[list[Any]]) -> bytes`
  - `serialize_resp(obj: Any) -> bytes`

- [ ] **Step 1: Write the failing tests for RESP serialization and parsing**

Create `tests/test_protocol.py`:
```python
import unittest
from pyredis.protocol import (
    RESPParser,
    serialize_simple_string,
    serialize_error,
    serialize_integer,
    serialize_bulk_string,
    serialize_array,
    serialize_resp,
)

class TestRESPProtocol(unittest.TestCase):
    def test_serialization(self):
        self.assertEqual(serialize_simple_string("OK"), b"+OK\r\n")
        self.assertEqual(serialize_error("ERR unknown"), b"-ERR unknown\r\n")
        self.assertEqual(serialize_integer(42), b":42\r\n")
        self.assertEqual(serialize_bulk_string("hello"), b"$5\r\nhello\r\n")
        self.assertEqual(serialize_bulk_string(b"raw\x00data"), b"$8\r\nraw\x00data\r\n")
        self.assertEqual(serialize_bulk_string(None), b"$-1\r\n")
        self.assertEqual(serialize_array(["GET", "key"]), b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n")
        self.assertEqual(serialize_array(None), b"*-1\r\n")

    def test_parse_simple_types(self):
        parser = RESPParser()
        parser.feed(b"+PONG\r\n:100\r\n-ERR test\r\n")
        self.assertEqual(parser.get_next_object(), "PONG")
        self.assertEqual(parser.get_next_object(), 100)
        self.assertEqual(parser.get_next_object(), Exception("ERR test"))  # or RESPError
        self.assertIsNone(parser.get_next_object())

    def test_parse_bulk_string(self):
        parser = RESPParser()
        parser.feed(b"$5\r\nworld\r\n$-1\r\n")
        self.assertEqual(parser.get_next_object(), b"world")
        self.assertIsNone(parser.get_next_object())  # null bulk string represented as None

    def test_parse_array(self):
        parser = RESPParser()
        parser.feed(b"*2\r\n$4\r\nECHO\r\n$5\r\nhello\r\n")
        self.assertEqual(parser.get_next_object(), [b"ECHO", b"hello"])

    def test_fragmented_stream(self):
        parser = RESPParser()
        # Feed 1 byte at a time
        full_msg = b"*2\r\n$3\r\nSET\r\n$3\r\nfoo\r\n"
        for byte in full_msg[:-1]:
            parser.feed(bytes([byte]))
            self.assertIsNone(parser.get_next_object())
        parser.feed(bytes([full_msg[-1]]))
        self.assertEqual(parser.get_next_object(), [b"SET", b"foo"])

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_protocol.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pyredis'`

- [ ] **Step 3: Implement RESP protocol serializer and parser**

Create `src/pyredis/__init__.py` and `src/pyredis/protocol.py` with cursor-based buffer parsing handling all RESP2 types and fragments.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_protocol.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/__init__.py src/pyredis/protocol.py tests/test_protocol.py
git commit -m "feat(protocol): implement RESP2 streaming parser and serializer"
```

---

### Task 2: In-Memory Storage Engine with Passive Expiration

**Files:**
- Create: `src/pyredis/store.py`
- Test: `tests/test_store.py`

**Interfaces:**
- Produces:
  - `class WrongTypeError(Exception)`
  - `class DataStore`:
    - `get(key: str) -> Optional[str]`
    - `set(key: str, value: str, ex_sec: Optional[float] = None, px_ms: Optional[float] = None, nx: bool = False, xx: bool = False) -> bool`
    - `delete(*keys: str) -> int`
    - `exists(*keys: str) -> int`
    - `incr_by(key: str, amount: int = 1) -> int`
    - `expire(key: str, seconds: float) -> bool`
    - `pexpire(key: str, milliseconds: float) -> bool`
    - `ttl(key: str) -> int` (seconds remaining, -2 if not found, -1 if no TTL)
    - `pttl(key: str) -> int` (milliseconds remaining, -2 if not found, -1 if no TTL)
    - `hset(key: str, mapping: dict[str, str]) -> int`
    - `hget(key: str, field: str) -> Optional[str]`
    - `hgetall(key: str) -> dict[str, str]`
    - `hdel(key: str, *fields: str) -> int`
    - `hexists(key: str, field: str) -> bool`
    - `lpush(key: str, *values: str) -> int`
    - `rpush(key: str, *values: str) -> int`
    - `lpop(key: str, count: int = 1) -> list[str]`
    - `rpop(key: str, count: int = 1) -> list[str]`
    - `lrange(key: str, start: int, stop: int) -> list[str]`
    - `llen(key: str) -> int`
    - `keys(pattern: str = "*") -> list[str]`
    - `flushdb() -> None`

- [ ] **Step 1: Write the failing tests for DataStore**

Create `tests/test_store.py` testing strings, hashes, lists, type verification (`WrongTypeError`), and passive TTL eviction.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_store.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pyredis.store'`

- [ ] **Step 3: Implement `DataStore` with passive TTL**

Create `src/pyredis/store.py` with typed dictionary storage, `collections.deque` for lists, and passive expiration check in `_is_expired(key)`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_store.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/store.py tests/test_store.py
git commit -m "feat(store): implement in-memory datastore with passive TTL and data structures"
```

---

### Task 3: Active TTL Eviction Sweeper

**Files:**
- Modify: `src/pyredis/store.py`
- Test: `tests/test_store_active_ttl.py`

**Interfaces:**
- Produces:
  - `DataStore.purge_expired(sample_size: int = 20, threshold: float = 0.25) -> int`
  - `DataStore.start_active_expiration(interval_sec: float = 0.1) -> asyncio.Task`
  - `DataStore.stop_active_expiration() -> None`

- [ ] **Step 1: Write the failing test for active expiration**

Create `tests/test_store_active_ttl.py` verifying that keys with expired timestamps are sampled, actively purged, and background task works properly.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_store_active_ttl.py`
Expected: FAIL with `AttributeError: 'DataStore' object has no attribute 'purge_expired'`

- [ ] **Step 3: Implement active eviction sweeper**

Add `purge_expired` and async background loop `start_active_expiration()` to `DataStore`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_store_active_ttl.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/store.py tests/test_store_active_ttl.py
git commit -m "feat(store): implement randomized active TTL background eviction sweeper"
```

---

### Task 4: Command Registry & Dispatcher

**Files:**
- Create: `src/pyredis/commands.py`
- Test: `tests/test_commands.py`

**Interfaces:**
- Consumes: `DataStore`, `RESP2 Serialization`
- Produces:
  - `class CommandDispatcher`:
    - `dispatch(raw_args: list[bytes]) -> tuple[bytes, bool]` (returns serialized response bytes and `is_mutation` flag for AOF logging)

- [ ] **Step 1: Write failing tests for command dispatcher**

Create `tests/test_commands.py` testing routing for `PING`, `ECHO`, `INFO`, `COMMAND`, `SET`, `GET`, `DEL`, `EXISTS`, `INCR`, `DECR`, `INCRBY`, `EXPIRE`, `PEXPIRE`, `TTL`, `PTTL`, `HSET`, `HGET`, `HGETALL`, `HDEL`, `HEXISTS`, `LPUSH`, `RPUSH`, `LPOP`, `RPOP`, `LRANGE`, `LLEN`, `KEYS`, `FLUSHDB`, as well as syntax error responses.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_commands.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pyredis.commands'`

- [ ] **Step 3: Implement `CommandDispatcher`**

Create `src/pyredis/commands.py` with command tables, arity validation, uppercase normalization, and exact error responses.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_commands.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/commands.py tests/test_commands.py
git commit -m "feat(commands): implement command dispatcher and RESP argument validation"
```

---

### Task 5: Append-Only File (AOF) Persistence Engine

**Files:**
- Create: `src/pyredis/persistence.py`
- Test: `tests/test_persistence.py`

**Interfaces:**
- Consumes: `DataStore`, `RESPParser`, `serialize_array`
- Produces:
  - `class AOFEngine`:
    - `__init__(filepath: str, store: DataStore, dispatcher: CommandDispatcher)`
    - `append(raw_args: list[bytes]) -> None`
    - `replay() -> int` (returns number of replayed commands on startup)
    - `close() -> None`

- [ ] **Step 1: Write failing test for AOF logging and replay**

Create `tests/test_persistence.py` asserting that mutations write to file, and reading back restores state identically into a fresh `DataStore`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_persistence.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pyredis.persistence'`

- [ ] **Step 3: Implement `AOFEngine`**

Create `src/pyredis/persistence.py` with atomic write, flush semantics, and startup replay through `RESPParser`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_persistence.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/persistence.py tests/test_persistence.py
git commit -m "feat(persistence): implement Append-Only File logger and crash replay"
```

---

### Task 6: Async TCP Socket Server, Connection Lifecycle & CLI

**Files:**
- Create: `src/pyredis/server.py`
- Create: `src/pyredis/cli.py`
- Test: `tests/test_server_integration.py`

**Interfaces:**
- Produces:
  - `class RedisServer`:
    - `start() -> asyncio.Server`
    - `stop() -> None`
  - CLI: `python -m pyredis.cli --host 127.0.0.1 --port 6379 [--aof-file path]`

- [ ] **Step 1: Write failing integration test for live TCP server**

Create `tests/test_server_integration.py` opening real TCP connections with `asyncio.open_connection`, executing commands, pipelining multiple commands, and verifying concurrent client handling.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_server_integration.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pyredis.server'`

- [ ] **Step 3: Implement `RedisServer` and `cli.py`**

Create `src/pyredis/server.py` with client loop, pipelining handling, active TTL sweeper startup, and `src/pyredis/cli.py` entry point.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_server_integration.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/pyredis/server.py src/pyredis/cli.py tests/test_server_integration.py
git commit -m "feat(server): implement high-concurrency asyncio TCP server and CLI"
```

---

### Task 7: Full Test Suite Verification & Quickstart Documentation

**Files:**
- Create: `README_REDIS.md`
- Test: Run complete test suite across all modules

- [ ] **Step 1: Run all unit and integration tests**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`
Expected: All tests pass with zero failures.

- [ ] **Step 2: Create quickstart documentation (`README_REDIS.md`)**

Document how to run the server, connect with standard `redis-cli`, supported commands, and architecture diagrams.

- [ ] **Step 3: Commit**

```bash
git add README_REDIS.md
git commit -m "docs: add redis clone quickstart guide and architecture overview"
```
