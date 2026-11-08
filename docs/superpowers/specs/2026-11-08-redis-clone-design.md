# Redis Clone Design Specification

**Date:** 2026-11-08  
**System:** High-Performance In-Memory Key-Value Store (Redis Clone)  
**Language & Runtime:** Python 3.13+ (`asyncio`, Python Standard Library only, zero third-party dependencies)  
**Status:** Approved for Implementation Planning

---

## 1. Executive Summary & Goals

The goal of this project is to build an in-memory key-value database and cache from scratch, fully compatible with the official Redis Serialization Protocol (RESP2) and capable of interfacing seamlessly with official client utilities such as `redis-cli`, `redis-py`, and modern HTTP/microservice frameworks.

### Key Goals
1. **Zero External Dependencies:** Built entirely with Python's standard library (`asyncio`, `socket`, `collections`, `time`, `dataclasses`, `os`, `sys`).
2. **RESP2 Wire Compliance:** Exact parsing and serialization of Simple Strings, Errors, Integers, Bulk Strings (including Null Bulk Strings), and Arrays.
3. **Pipelining & Streaming Support:** Robust handling of fragmented TCP streams and pipelined commands across concurrent client connections.
4. **Rich Data Structure Support:** Strings, numeric counters, Hash maps, and double-ended Lists.
5. **Exact Expiration (TTL) Semantics:** Dual-tier expiration combining passive eviction upon access with an active randomized background sweeper.
6. **Append-Only File (AOF) Persistence:** Transactional log appending for state mutations with automated replay on server boot.

---

## 2. System Architecture & Component Boundaries

The system is decomposed into cleanly decoupled modules under `src/pyredis/`:

```
src/pyredis/
├── __init__.py
├── protocol.py       # RESP2 serialization, streaming deserialization & framing
├── store.py          # Core in-memory data store, data types, and TTL eviction logic
├── commands.py       # Command dispatch table, argument validation, and handler implementations
├── persistence.py   # Append-Only File (AOF) logger and startup replay parser
├── server.py         # Asyncio TCP socket server, connection management & client loop
└── cli.py            # Entry point with argparse (--port, --host, --aof, etc.)
```

### Module Responsibilities

| Module | Purpose | Interface / Boundaries |
| :--- | :--- | :--- |
| `protocol.py` | Converts byte streams to Python primitives and vice-versa. | `RESPParser.feed(chunk) -> list[Any]`, `serialize_resp(obj) -> bytes` |
| `store.py` | Holds key-value data, metadata, and performs passive/active expiration sweeps. | `DataStore.get()`, `set()`, `expire()`, `purge_expired()` |
| `commands.py` | Routes parsed command arrays to execution functions and enforces type safety. | `CommandDispatcher.dispatch(cmd_args, client_context)` |
| `persistence.py` | Appends mutating commands to disk and replays them on cold boot. | `AOFEngine.append(cmd_bytes)`, `AOFEngine.replay(datastore)` |
| `server.py` | Listens for client sockets, coordinates event loops, and delegates command handling. | `RedisServer.start()`, `RedisServer.stop()` |
| `cli.py` | Provides the executable CLI interface for starting the server. | `python -m pyredis.cli --port 6379` |

---

## 3. Protocol Specification (RESP2)

All RESP communication consists of typed prefixes terminated by `\r\n` (CRLF):

1. **Simple Strings (`+`):** `+OK\r\n`, `+PONG\r\n`
2. **Errors (`-`):** `-ERR unknown command\r\n`, `-WRONGTYPE Operation against a key holding the wrong kind of value\r\n`
3. **Integers (`:`):** `:1\r\n`, `:0\r\n`, `:-1\r\n`
4. **Bulk Strings (`$`):**
   - Content: `$5\r\nhello\r\n`
   - Empty string: `$0\r\n\r\n`
   - Null value (key does not exist): `$-1\r\n`
5. **Arrays (`*`):**
   - Multi-element: `*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n`
   - Null array: `*-1\r\n`
   - Empty array: `*0\r\n`

### Streaming Framing Algorithm
TCP does not guarantee packet boundaries. The `RESPParser` maintains an internal `bytearray` buffer:
- When bytes arrive via `reader.read(4096)`, they are appended to the buffer.
- The parser advances a reading cursor.
- If CRLF is missing, or if a Bulk String length indicates more bytes are pending than available in the buffer, the parser pauses without consuming, preserving state until the next chunk arrives.
- Pipelined requests (e.g., 5 commands sent in one TCP packet) are yielded sequentially in a single pass.

---

## 4. In-Memory Storage & Data Types

The storage engine (`DataStore`) manages key-value bindings and their optional expiration timestamps.

### Internal Data Structures
- `_data: dict[str, Any]`:
  - **Strings:** Stored as `str`.
  - **Hashes:** Stored as `dict[str, str]`.
  - **Lists:** Stored as `collections.deque[str]`.
- `_expires: dict[str, float]`:
  - Maps `key` -> UNIX epoch timestamp in seconds (`time.time()`).

### Supported Commands

#### General / Connection
- `PING [message]`: Returns `PONG` or bulk string echo.
- `ECHO message`: Returns the provided message.
- `COMMAND`: Returns empty/basic command documentation array for `redis-cli` handshake.
- `INFO [section]`: Returns server metadata (uptime, connected clients, total keys).
- `KEYS pattern`: Returns all keys matching glob pattern (default `*`).
- `FLUSHDB`: Purges all keys and expiration tracking.

#### String & Key Operations
- `SET key value [EX seconds] [PX milliseconds] [NX | XX]`:
  - `EX`: Set expiration in seconds.
  - `PX`: Set expiration in milliseconds.
  - `NX`: Only set if key does not exist.
  - `XX`: Only set if key already exists.
  - Returns `+OK\r\n` on success, `$-1\r\n` if condition fails.
- `GET key`: Returns Bulk String value or `$-1\r\n` if expired/missing.
- `DEL key [key ...]`: Deletes specified keys. Returns Integer count of keys removed.
- `EXISTS key [key ...]`: Returns Integer count of existing keys.
- `INCR key` / `DECR key`: Atomically increments/decrements integer string.
- `INCRBY key increment`: Atomically increments by integer value.

#### Expiration Operations
- `EXPIRE key seconds`: Sets TTL in seconds. Returns `1` if key exists, `0` otherwise.
- `PEXPIRE key milliseconds`: Sets TTL in milliseconds.
- `TTL key`: Returns remaining seconds (`-2` if key doesn't exist, `-1` if key exists without TTL).
- `PTTL key`: Returns remaining milliseconds (`-2` if doesn't exist, `-1` if no TTL).

#### Hash Operations
- `HSET key field value [field value ...]`: Sets field(s) on a hash. Returns count of new fields added.
- `HGET key field`: Returns Bulk String of field or `$-1\r\n`.
- `HGETALL key`: Returns Array of `[field1, value1, field2, value2, ...]`.
- `HDEL key field [field ...]`: Removes field(s) from a hash. Returns count of removed fields.
- `HEXISTS key field`: Returns `1` if field exists, `0` otherwise.

#### List Operations
- `LPUSH key value [value ...]`: Prepends values to list. Returns new list length.
- `RPUSH key value [value ...]`: Appends values to list. Returns new list length.
- `LPOP key [count]`: Pops elements from head of list.
- `RPOP key [count]`: Pops elements from tail of list.
- `LRANGE key start stop`: Returns Array of elements from slice.
- `LLEN key`: Returns Integer length of list.

---

## 5. Expiration (TTL) Lifecycle Specification

1. **Passive Eviction (On Read/Write):**
   - Whenever any command (`GET`, `HGET`, `EXISTS`, etc.) looks up a key, `_is_expired(key)` is checked.
   - If `time.time() >= _expires[key]`:
     - Delete `_data[key]` and `_expires[key]`.
     - Key is treated as non-existent.
2. **Active Eviction (Periodic Sweeper):**
   - Background task scheduled every `100ms` via `asyncio.create_task()`.
   - Algorithm:
     1. Sample up to 20 keys with active expirations.
     2. Evict any key whose timestamp is in the past.
     3. If more than 25% of sampled keys were expired, repeat sampling immediately (capped at 10 iterations to prevent blocking).

---

## 6. Persistence Specification (Append-Only File - AOF)

### Log Structure
- Standard RESP array format. For example, a command `SET foo bar` is serialized as:
  `*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n`
- Write Mode: Flushed to disk synchronously on mutation or batched per event loop tick.

### Cold Start Replay
1. Check if `appendonly.aof` exists on startup.
2. If present, stream byte chunks into `RESPParser`.
3. Dispatch each deserialized command directly into `DataStore` (without writing back to AOF).
4. Once replay reaches EOF, start the TCP listener.

---

## 7. Testing & Verification Strategy

1. **Unit Test Suite (`tests/test_resp.py`):**
   - Parsing each data type.
   - Fragmented chunk testing (1 byte at a time feeding).
   - Pipelined frames in single buffer.
   - Serialization accuracy.
2. **Storage & TTL Test Suite (`tests/test_store.py`):**
   - Strings, Hashes, Lists behavior and boundary tests.
   - Type error checking (`-WRONGTYPE`).
   - Passive expiration with simulated clocks.
   - Active background eviction verification.
3. **AOF Persistence Test Suite (`tests/test_persistence.py`):**
   - Mutation recording and file integrity.
   - Crash recovery / replay verification.
4. **Integration Test Suite (`tests/test_server.py`):**
   - Real TCP socket connections using `asyncio.open_connection`.
   - Concurrency tests (multiple parallel client connections).
   - Pipelining commands over live sockets.
   - Full command parity check.
