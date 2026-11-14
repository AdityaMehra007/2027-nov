"""In-memory DataStore for Redis clone with passive & active TTL expiration."""

from __future__ import annotations
import asyncio
from collections import deque
import fnmatch
import math
import random
import time
from typing import Any, Optional


class WrongTypeError(Exception):
    """Raised when an operation is attempted against a key holding the wrong kind of value."""
    pass


class DataStore:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._expires: dict[str, float] = {}
        self._sweep_task: Optional[asyncio.Task] = None
        self._running_sweep = False

    def _is_expired(self, key: str) -> bool:
        """Passive expiration check: evicts key if its expiration timestamp has passed."""
        if key in self._expires:
            if time.time() >= self._expires[key]:
                self._evict(key)
                return True
        return False

    def _evict(self, key: str) -> None:
        """Internal helper to evict a key and its TTL tracking."""
        self._data.pop(key, None)
        self._expires.pop(key, None)

    # -------------------------------------------------------------------------
    # Keys & Server Operations
    # -------------------------------------------------------------------------

    def exists(self, *keys: str) -> int:
        count = 0
        for k in keys:
            if self._is_expired(k):
                continue
            if k in self._data:
                count += 1
        return count

    def delete(self, *keys: str) -> int:
        count = 0
        for k in keys:
            if self._is_expired(k):
                continue
            if k in self._data:
                self._evict(k)
                count += 1
        return count

    def keys(self, pattern: str = "*") -> list[str]:
        # Purge any expired keys encountered
        active_keys = []
        for k in list(self._data.keys()):
            if self._is_expired(k):
                continue
            if fnmatch.fnmatch(k, pattern):
                active_keys.append(k)
        return active_keys

    def flushdb(self) -> None:
        self._data.clear()
        self._expires.clear()

    # -------------------------------------------------------------------------
    # Expiration (TTL)
    # -------------------------------------------------------------------------

    def expire(self, key: str, seconds: float) -> bool:
        if self._is_expired(key) or key not in self._data:
            return False
        self._expires[key] = time.time() + float(seconds)
        return True

    def pexpire(self, key: str, milliseconds: float) -> bool:
        return self.expire(key, milliseconds / 1000.0)

    def ttl(self, key: str) -> int:
        if self._is_expired(key) or key not in self._data:
            return -2
        if key not in self._expires:
            return -1
        rem = self._expires[key] - time.time()
        return max(0, math.ceil(rem))

    def pttl(self, key: str) -> int:
        if self._is_expired(key) or key not in self._data:
            return -2
        if key not in self._expires:
            return -1
        rem = self._expires[key] - time.time()
        return max(0, math.ceil(rem * 1000.0))

    # -------------------------------------------------------------------------
    # String Operations
    # -------------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: str,
        ex_sec: Optional[float] = None,
        px_ms: Optional[float] = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        is_expired = self._is_expired(key)
        exists = (key in self._data) and not is_expired

        if nx and exists:
            return False
        if xx and not exists:
            return False

        self._data[key] = str(value)
        self._expires.pop(key, None)

        if ex_sec is not None:
            self._expires[key] = time.time() + float(ex_sec)
        elif px_ms is not None:
            self._expires[key] = time.time() + (float(px_ms) / 1000.0)

        return True

    def get(self, key: str) -> Optional[str]:
        if self._is_expired(key):
            return None
        val = self._data.get(key)
        if val is None:
            return None
        if not isinstance(val, str):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")
        return val

    def incr_by(self, key: str, amount: int = 1) -> int:
        if self._is_expired(key):
            pass
        val = self._data.get(key)
        if val is None:
            new_val = amount
        else:
            if not isinstance(val, str):
                raise WrongTypeError("Operation against a key holding the wrong kind of value")
            try:
                new_val = int(val) + amount
            except ValueError:
                raise ValueError("value is not an integer or out of range")
        self._data[key] = str(new_val)
        return new_val

    # -------------------------------------------------------------------------
    # Hash Operations
    # -------------------------------------------------------------------------

    def hset(self, key: str, mapping: dict[str, str]) -> int:
        if self._is_expired(key):
            pass
        val = self._data.get(key)
        if val is None:
            val = {}
            self._data[key] = val
        elif not isinstance(val, dict):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        added_count = 0
        for f, v in mapping.items():
            if f not in val:
                added_count += 1
            val[f] = str(v)
        return added_count

    def hget(self, key: str, field: str) -> Optional[str]:
        if self._is_expired(key):
            return None
        val = self._data.get(key)
        if val is None:
            return None
        if not isinstance(val, dict):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")
        return val.get(field)

    def hgetall(self, key: str) -> dict[str, str]:
        if self._is_expired(key):
            return {}
        val = self._data.get(key)
        if val is None:
            return {}
        if not isinstance(val, dict):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")
        return dict(val)

    def hdel(self, key: str, *fields: str) -> int:
        if self._is_expired(key):
            return 0
        val = self._data.get(key)
        if val is None:
            return 0
        if not isinstance(val, dict):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        removed = 0
        for f in fields:
            if f in val:
                del val[f]
                removed += 1
        if not val:
            self._evict(key)
        return removed

    def hexists(self, key: str, field: str) -> bool:
        if self._is_expired(key):
            return False
        val = self._data.get(key)
        if val is None:
            return False
        if not isinstance(val, dict):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")
        return field in val

    # -------------------------------------------------------------------------
    # List Operations
    # -------------------------------------------------------------------------

    def lpush(self, key: str, *values: str) -> int:
        if self._is_expired(key):
            pass
        val = self._data.get(key)
        if val is None:
            val = deque()
            self._data[key] = val
        elif not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        for v in values:
            val.appendleft(str(v))
        return len(val)

    def rpush(self, key: str, *values: str) -> int:
        if self._is_expired(key):
            pass
        val = self._data.get(key)
        if val is None:
            val = deque()
            self._data[key] = val
        elif not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        for v in values:
            val.append(str(v))
        return len(val)

    def lpop(self, key: str, count: int = 1) -> list[str]:
        if self._is_expired(key):
            return []
        val = self._data.get(key)
        if val is None:
            return []
        if not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        popped = []
        for _ in range(min(count, len(val))):
            popped.append(val.popleft())
        if not val:
            self._evict(key)
        return popped

    def rpop(self, key: str, count: int = 1) -> list[str]:
        if self._is_expired(key):
            return []
        val = self._data.get(key)
        if val is None:
            return []
        if not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        popped = []
        for _ in range(min(count, len(val))):
            popped.append(val.pop())
        if not val:
            self._evict(key)
        return popped

    def lrange(self, key: str, start: int, stop: int) -> list[str]:
        if self._is_expired(key):
            return []
        val = self._data.get(key)
        if val is None:
            return []
        if not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")

        items = list(val)
        length = len(items)

        # Normalize negative indices
        if start < 0:
            start = max(0, length + start)
        if stop < 0:
            stop = length + stop

        if start > stop or start >= length:
            return []

        stop = min(stop, length - 1)
        return items[start : stop + 1]

    def llen(self, key: str) -> int:
        if self._is_expired(key):
            return 0
        val = self._data.get(key)
        if val is None:
            return 0
        if not isinstance(val, deque):
            raise WrongTypeError("Operation against a key holding the wrong kind of value")
        return len(val)

    # -------------------------------------------------------------------------
    # Active Expiration Sweeper (Task 3 integration)
    # -------------------------------------------------------------------------

    def purge_expired(self, sample_size: int = 20, threshold: float = 0.25) -> int:
        """Probabilistic active expiration sweep matching Redis internal algorithm.
        Samples up to sample_size expiring keys. If > threshold of sampled keys were expired,
        repeats until ratio drops below threshold (up to 10 iterations).
        """
        now = time.time()
        total_purged = 0
        iterations = 0

        while iterations < 10:
            iterations += 1
            expiring_keys = list(self._expires.keys())
            if not expiring_keys:
                break

            sample = random.sample(expiring_keys, min(len(expiring_keys), sample_size))
            expired_in_sample = 0

            for k in sample:
                exp = self._expires.get(k)
                if exp is not None and now >= exp:
                    self._evict(k)
                    expired_in_sample += 1
                    total_purged += 1

            if len(sample) == 0 or (expired_in_sample / len(sample)) <= threshold:
                break

        return total_purged

    async def _sweep_loop(self, interval_sec: float) -> None:
        try:
            while self._running_sweep:
                self.purge_expired()
                await asyncio.sleep(interval_sec)
        except asyncio.CancelledError:
            pass

    def start_active_expiration(self, interval_sec: float = 0.1) -> asyncio.Task:
        if self._sweep_task and not self._sweep_task.done():
            return self._sweep_task
        self._running_sweep = True
        self._sweep_task = asyncio.create_task(self._sweep_loop(interval_sec))
        return self._sweep_task

    def stop_active_expiration(self) -> None:
        self._running_sweep = False
        if self._sweep_task and not self._sweep_task.done():
            self._sweep_task.cancel()
