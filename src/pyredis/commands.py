"""Command registry and dispatcher for Redis clone."""

from __future__ import annotations
import os
import sys
import time
from typing import Any, Callable, Optional, Sequence
from pyredis.protocol import (
    serialize_array,
    serialize_bulk_string,
    serialize_error,
    serialize_integer,
    serialize_resp,
    serialize_simple_string,
)
from pyredis.store import DataStore, WrongTypeError

SERVER_START_TIME = time.time()


class CommandDispatcher:
    def __init__(self, store: DataStore) -> None:
        self.store = store
        self._handlers: dict[str, Callable[[list[str]], tuple[bytes, bool]]] = {
            # Connection & Server
            "PING": self._handle_ping,
            "ECHO": self._handle_echo,
            "COMMAND": self._handle_command,
            "INFO": self._handle_info,
            "KEYS": self._handle_keys,
            "FLUSHDB": self._handle_flushdb,
            # Strings & Numeric
            "SET": self._handle_set,
            "GET": self._handle_get,
            "DEL": self._handle_del,
            "EXISTS": self._handle_exists,
            "INCR": self._handle_incr,
            "DECR": self._handle_decr,
            "INCRBY": self._handle_incrby,
            # Expiration
            "EXPIRE": self._handle_expire,
            "PEXPIRE": self._handle_pexpire,
            "TTL": self._handle_ttl,
            "PTTL": self._handle_pttl,
            # Hashes
            "HSET": self._handle_hset,
            "HGET": self._handle_hget,
            "HGETALL": self._handle_hgetall,
            "HDEL": self._handle_hdel,
            "HEXISTS": self._handle_hexists,
            # Lists
            "LPUSH": self._handle_lpush,
            "RPUSH": self._handle_rpush,
            "LPOP": self._handle_lpop,
            "RPOP": self._handle_rpop,
            "LRANGE": self._handle_lrange,
            "LLEN": self._handle_llen,
        }

    def dispatch(self, raw_args: Sequence[bytes | str]) -> tuple[bytes, bool]:
        """Dispatches raw command arguments to the appropriate handler.
        Returns: (resp_bytes, is_mutation)
        """
        if not raw_args:
            return serialize_error("ERR empty command"), False

        # Convert bytes to string (decoded leniently with surrogateescape for binary safety)
        decoded_args: list[str] = []
        for a in raw_args:
            if isinstance(a, bytes):
                decoded_args.append(a.decode("utf-8", errors="surrogateescape"))
            else:
                decoded_args.append(str(a))

        cmd_name = decoded_args[0].upper()
        args = decoded_args[1:]

        handler = self._handlers.get(cmd_name)
        if not handler:
            return serialize_error(f"ERR unknown command '{cmd_name}'"), False

        try:
            return handler(args)
        except WrongTypeError as e:
            return serialize_error(f"WRONGTYPE {str(e)}"), False
        except ValueError as e:
            msg = str(e)
            if not msg.startswith("ERR "):
                msg = f"ERR {msg}"
            return serialize_error(msg), False
        except Exception as e:
            return serialize_error(f"ERR {str(e)}"), False

    # -------------------------------------------------------------------------
    # Connection Handlers
    # -------------------------------------------------------------------------

    def _handle_ping(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) == 0:
            return serialize_simple_string("PONG"), False
        elif len(args) == 1:
            return serialize_bulk_string(args[0]), False
        return serialize_error("ERR wrong number of arguments for 'ping' command"), False

    def _handle_echo(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'echo' command"), False
        return serialize_bulk_string(args[0]), False

    def _handle_command(self, args: list[str]) -> tuple[bytes, bool]:
        # Empty array for redis-cli compatibility
        return serialize_array([]), False

    def _handle_info(self, args: list[str]) -> tuple[bytes, bool]:
        uptime = int(time.time() - SERVER_START_TIME)
        info_str = (
            f"# Server\r\n"
            f"redis_version:7.0.0-pyredis\r\n"
            f"os:{sys.platform}\r\n"
            f"uptime_in_seconds:{uptime}\r\n"
            f"connected_clients:1\r\n"
            f"# Keyspace\r\n"
            f"db0:keys={len(self.store._data)},expires={len(self.store._expires)}\r\n"
        )
        return serialize_bulk_string(info_str), False

    def _handle_keys(self, args: list[str]) -> tuple[bytes, bool]:
        pattern = args[0] if args else "*"
        matched = self.store.keys(pattern)
        return serialize_array(matched), False

    def _handle_flushdb(self, args: list[str]) -> tuple[bytes, bool]:
        self.store.flushdb()
        return serialize_simple_string("OK"), True

    # -------------------------------------------------------------------------
    # String Handlers
    # -------------------------------------------------------------------------

    def _handle_set(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 2:
            return serialize_error("ERR wrong number of arguments for 'set' command"), False

        key = args[0]
        value = args[1]
        ex_sec: Optional[float] = None
        px_ms: Optional[float] = None
        nx = False
        xx = False

        idx = 2
        while idx < len(args):
            opt = args[idx].upper()
            if opt == "EX" and idx + 1 < len(args):
                try:
                    ex_sec = float(args[idx + 1])
                except ValueError:
                    return serialize_error("ERR value is not an integer or out of range"), False
                idx += 2
            elif opt == "PX" and idx + 1 < len(args):
                try:
                    px_ms = float(args[idx + 1])
                except ValueError:
                    return serialize_error("ERR value is not an integer or out of range"), False
                idx += 2
            elif opt == "NX":
                nx = True
                idx += 1
            elif opt == "XX":
                xx = True
                idx += 1
            else:
                return serialize_error("ERR syntax error"), False

        ok = self.store.set(key, value, ex_sec=ex_sec, px_ms=px_ms, nx=nx, xx=xx)
        if ok:
            return serialize_simple_string("OK"), True
        return serialize_bulk_string(None), False

    def _handle_get(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'get' command"), False
        val = self.store.get(args[0])
        return serialize_bulk_string(val), False

    def _handle_del(self, args: list[str]) -> tuple[bytes, bool]:
        if not args:
            return serialize_error("ERR wrong number of arguments for 'del' command"), False
        count = self.store.delete(*args)
        return serialize_integer(count), count > 0

    def _handle_exists(self, args: list[str]) -> tuple[bytes, bool]:
        if not args:
            return serialize_error("ERR wrong number of arguments for 'exists' command"), False
        count = self.store.exists(*args)
        return serialize_integer(count), False

    def _handle_incr(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'incr' command"), False
        new_val = self.store.incr_by(args[0], 1)
        return serialize_integer(new_val), True

    def _handle_decr(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'decr' command"), False
        new_val = self.store.incr_by(args[0], -1)
        return serialize_integer(new_val), True

    def _handle_incrby(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 2:
            return serialize_error("ERR wrong number of arguments for 'incrby' command"), False
        try:
            amt = int(args[1])
        except ValueError:
            return serialize_error("ERR value is not an integer or out of range"), False
        new_val = self.store.incr_by(args[0], amt)
        return serialize_integer(new_val), True

    # -------------------------------------------------------------------------
    # Expiration Handlers
    # -------------------------------------------------------------------------

    def _handle_expire(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 2:
            return serialize_error("ERR wrong number of arguments for 'expire' command"), False
        try:
            sec = float(args[1])
        except ValueError:
            return serialize_error("ERR value is not an integer or out of range"), False
        ok = self.store.expire(args[0], sec)
        return serialize_integer(1 if ok else 0), ok

    def _handle_pexpire(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 2:
            return serialize_error("ERR wrong number of arguments for 'pexpire' command"), False
        try:
            ms = float(args[1])
        except ValueError:
            return serialize_error("ERR value is not an integer or out of range"), False
        ok = self.store.pexpire(args[0], ms)
        return serialize_integer(1 if ok else 0), ok

    def _handle_ttl(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'ttl' command"), False
        rem = self.store.ttl(args[0])
        return serialize_integer(rem), False

    def _handle_pttl(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'pttl' command"), False
        rem = self.store.pttl(args[0])
        return serialize_integer(rem), False

    # -------------------------------------------------------------------------
    # Hash Handlers
    # -------------------------------------------------------------------------

    def _handle_hset(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 3 or (len(args) - 1) % 2 != 0:
            return serialize_error("ERR wrong number of arguments for 'hset' command"), False
        key = args[0]
        mapping: dict[str, str] = {}
        for i in range(1, len(args), 2):
            mapping[args[i]] = args[i + 1]
        added = self.store.hset(key, mapping)
        return serialize_integer(added), True

    def _handle_hget(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 2:
            return serialize_error("ERR wrong number of arguments for 'hget' command"), False
        val = self.store.hget(args[0], args[1])
        return serialize_bulk_string(val), False

    def _handle_hgetall(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'hgetall' command"), False
        mapping = self.store.hgetall(args[0])
        flat_list = []
        for k, v in mapping.items():
            flat_list.append(k)
            flat_list.append(v)
        return serialize_array(flat_list), False

    def _handle_hdel(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 2:
            return serialize_error("ERR wrong number of arguments for 'hdel' command"), False
        count = self.store.hdel(args[0], *args[1:])
        return serialize_integer(count), count > 0

    def _handle_hexists(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 2:
            return serialize_error("ERR wrong number of arguments for 'hexists' command"), False
        exists = self.store.hexists(args[0], args[1])
        return serialize_integer(1 if exists else 0), False

    # -------------------------------------------------------------------------
    # List Handlers
    # -------------------------------------------------------------------------

    def _handle_lpush(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 2:
            return serialize_error("ERR wrong number of arguments for 'lpush' command"), False
        length = self.store.lpush(args[0], *args[1:])
        return serialize_integer(length), True

    def _handle_rpush(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 2:
            return serialize_error("ERR wrong number of arguments for 'rpush' command"), False
        length = self.store.rpush(args[0], *args[1:])
        return serialize_integer(length), True

    def _handle_lpop(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 1 or len(args) > 2:
            return serialize_error("ERR wrong number of arguments for 'lpop' command"), False
        count = int(args[1]) if len(args) == 2 else 1
        popped = self.store.lpop(args[0], count)
        if len(args) == 1:
            val = popped[0] if popped else None
            return serialize_bulk_string(val), bool(popped)
        return serialize_array(popped), bool(popped)

    def _handle_rpop(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) < 1 or len(args) > 2:
            return serialize_error("ERR wrong number of arguments for 'rpop' command"), False
        count = int(args[1]) if len(args) == 2 else 1
        popped = self.store.rpop(args[0], count)
        if len(args) == 1:
            val = popped[0] if popped else None
            return serialize_bulk_string(val), bool(popped)
        return serialize_array(popped), bool(popped)

    def _handle_lrange(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 3:
            return serialize_error("ERR wrong number of arguments for 'lrange' command"), False
        try:
            start = int(args[1])
            stop = int(args[2])
        except ValueError:
            return serialize_error("ERR value is not an integer or out of range"), False
        items = self.store.lrange(args[0], start, stop)
        return serialize_array(items), False

    def _handle_llen(self, args: list[str]) -> tuple[bytes, bool]:
        if len(args) != 1:
            return serialize_error("ERR wrong number of arguments for 'llen' command"), False
        length = self.store.llen(args[0])
        return serialize_integer(length), False
