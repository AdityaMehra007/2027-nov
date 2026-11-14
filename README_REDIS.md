# PyRedis: Zero-Dependency Redis Clone in Python

A high-performance in-memory key-value database and cache built entirely from scratch using Python 3.13+ standard library (`asyncio`), fully compliant with the Redis Serialization Protocol (RESP2).

Compatible with official tools including `redis-cli`, Python `redis`, and any standard RESP client.

---

## Architecture Overview

```
                      +-----------------------------+
                      |         redis-cli           |
                      |  (or Python redis / SDKs)   |
                      +--------------+--------------+
                                     |  TCP (RESP2)
                                     v
+-------------------------------------------------------------------------+
|                                PyRedis Server                           |
|                                                                         |
|  +--------------------+     +---------------------+     +-------------+ |
|  |     server.py      | --> |     protocol.py     | --> | commands.py | |
|  | (asyncio TCP loop) |     |  (Streaming RESP2)  |     | (Dispatcher)| |
|  +---------+----------+     +---------------------+     +------+------+ |
|            |                                                   |        |
|            v                                                   v        |
|  +--------------------+                             +-----------------+ |
|  |   persistence.py   |                             |    store.py     | |
|  | (AOF Append/Replay)|                             | (In-Memory Core)| |
|  +--------------------+                             +--------+--------+ |
|            |                                                 |          |
|            v                                                 v          |
|     [appendonly.aof]                                [Active TTL Sweeper]|
+-------------------------------------------------------------------------+
```

### Module Responsibilities

1. **`pyredis/protocol.py`**:
   - Streaming, cursor-based RESP2 parser capable of handling fragmented TCP reads and pipelined batches.
   - Serializer supporting Simple Strings (`+`), Errors (`-`), Integers (`:`), Bulk Strings (`$`), and Arrays (`*`).
2. **`pyredis/store.py`**:
   - In-memory data store supporting Strings, Hashes, and Lists with strict type safety (`-WRONGTYPE`).
   - Dual-tier expiration: passive eviction upon access + randomized probabilistic active background sweeper (100ms cycle).
3. **`pyredis/commands.py`**:
   - Case-insensitive command dispatcher validating arity and argument syntax.
   - Mutation tracking for durability logs.
4. **`pyredis/persistence.py`**:
   - Append-Only File (AOF) logger that streams mutating operations to disk.
   - Crash recovery replay restoring full in-memory state on startup.
5. **`pyredis/server.py` & `pyredis/cli.py`**:
   - Async TCP socket server handling concurrent connections and pipelining.
   - CLI flags for `--host`, `--port`, and `--aof-file`.

---

## Quickstart

### 1. Launch the Server

Run using Python's module runner:

```bash
# Start default server on 127.0.0.1:6379 with AOF logging
python -m pyredis.cli

# Or specify custom port and host
python -m pyredis.cli --host 127.0.0.1 --port 6380 --aof-file mydata.aof
```

### 2. Connect via `redis-cli`

```bash
redis-cli -p 6379

127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SET framework "PyRedis"
OK
127.0.0.1:6379> GET framework
"PyRedis"
127.0.0.1:6379> EXPIRE framework 60
(integer) 1
127.0.0.1:6379> TTL framework
(integer) 59
```

### 3. Connect via Python (`redis-py`)

```python
import redis

client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# Strings & TTL
client.set("session:token", "xyz123", ex=300)
print(client.get("session:token"))  # xyz123

# Hashes
client.hset("user:10", mapping={"name": "Alice", "role": "admin"})
print(client.hgetall("user:10"))    # {'name': 'Alice', 'role': 'admin'}

# Lists
client.rpush("queue", "task_1", "task_2")
print(client.lpop("queue"))         # task_1
```

---

## Supported Commands

| Category | Commands |
| :--- | :--- |
| **Server / Connection** | `PING [msg]`, `ECHO msg`, `COMMAND`, `INFO`, `KEYS [pattern]`, `FLUSHDB` |
| **Strings & Numbers** | `SET key val [EX sec] [PX ms] [NX \| XX]`, `GET key`, `DEL key...`, `EXISTS key...`, `INCR key`, `DECR key`, `INCRBY key amt` |
| **Expiration (TTL)** | `EXPIRE key sec`, `PEXPIRE key ms`, `TTL key`, `PTTL key` |
| **Hashes** | `HSET key f v [f v...]`, `HGET key f`, `HGETALL key`, `HDEL key f...`, `HEXISTS key f` |
| **Lists** | `LPUSH key val...`, `RPUSH key val...`, `LPOP key [count]`, `RPOP key [count]`, `LRANGE key start stop`, `LLEN key` |

---

## Running Tests

PyRedis has zero third-party testing requirements. Run the full test suite with standard `unittest`:

```bash
python -m unittest tests/test_protocol.py tests/test_store.py tests/test_store_active_ttl.py tests/test_commands.py tests/test_persistence.py tests/test_server_integration.py
```

All 33 tests verify protocol streaming, binary safety, data structures, dual-tier TTL eviction, AOF persistence recovery, and concurrent TCP connections.
