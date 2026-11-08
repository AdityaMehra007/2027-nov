"""RESP2 (REdis Serialization Protocol) Serializer & Streaming Deserializer.

Zero-dependency implementation conforming to Redis RESP2 specifications:
- Simple Strings: +<string>\r\n
- Errors: -<error message>\r\n
- Integers: :<integer>\r\n
- Bulk Strings: $<length>\r\n<data>\r\n (or $-1\r\n for null)
- Arrays: *<count>\r\n<element 1>...<element N> (or *-1\r\n for null)
"""

from typing import Any, Iterable, Optional, Union

_BYTE_PLUS = 43    # ord('+')
_BYTE_MINUS = 45   # ord('-')
_BYTE_COLON = 58   # ord(':')
_BYTE_DOLLAR = 36  # ord('$')
_BYTE_STAR = 42    # ord('*')
_CRLF = b"\r\n"
_COMPACT_THRESHOLD = 65536


class RESPError(Exception):
    """Exception representing a RESP error reply or protocol error."""

    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RESPError):
            return self.message == other.message
        if isinstance(other, Exception):
            return self.args == other.args
        return False

    def __hash__(self) -> int:
        return hash((self.__class__, self.args))

    def __repr__(self) -> str:
        return f"RESPError({self.message!r})"


class SimpleString(str):
    """Marker class to serialize a Python string as a RESP Simple String."""
    pass


def serialize_simple_string(val: str) -> bytes:
    """Serialize a string as a RESP Simple String (+<val>\\r\\n)."""
    return f"+{val}\r\n".encode("utf-8")


def serialize_error(msg: str) -> bytes:
    """Serialize an error message as a RESP Error (-<msg>\\r\\n)."""
    return f"-{msg}\r\n".encode("utf-8")


def serialize_integer(num: int) -> bytes:
    """Serialize an integer as a RESP Integer (:<num>\\r\\n)."""
    return f":{int(num)}\r\n".encode("utf-8")


def serialize_bulk_string(data: Optional[Union[bytes, bytearray, memoryview, str]]) -> bytes:
    """Serialize data as a RESP Bulk String ($<len>\\r\\n<data>\\r\\n or $-1\\r\\n)."""
    if data is None:
        return b"$-1\r\n"
    if isinstance(data, str):
        payload = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray, memoryview)):
        payload = bytes(data)
    else:
        payload = str(data).encode("utf-8")
    return f"${len(payload)}\r\n".encode("utf-8") + payload + b"\r\n"


def serialize_array(items: Optional[Iterable[Any]]) -> bytes:
    """Serialize an iterable of items as a RESP Array (*<count>\\r\\n... or *-1\\r\\n)."""
    if items is None:
        return b"*-1\r\n"
    items_list = list(items)
    parts = [f"*{len(items_list)}\r\n".encode("utf-8")]
    for item in items_list:
        parts.append(serialize_resp(item))
    return b"".join(parts)


def serialize_resp(obj: Any) -> bytes:
    """Serialize any Python object into its canonical RESP2 representation."""
    if obj is None:
        return serialize_bulk_string(None)
    if isinstance(obj, SimpleString):
        return serialize_simple_string(str(obj))
    if isinstance(obj, (RESPError, Exception)):
        msg = obj.args[0] if obj.args else str(obj)
        return serialize_error(msg)
    if isinstance(obj, bool):
        return serialize_integer(1 if obj else 0)
    if isinstance(obj, int):
        return serialize_integer(obj)
    if isinstance(obj, (bytes, bytearray, memoryview)):
        return serialize_bulk_string(bytes(obj))
    if isinstance(obj, str):
        return serialize_bulk_string(obj)
    if isinstance(obj, (list, tuple, set)):
        return serialize_array(list(obj))
    if isinstance(obj, dict):
        flat = []
        for k, v in obj.items():
            flat.append(k)
            flat.append(v)
        return serialize_array(flat)
    return serialize_bulk_string(str(obj))


class RESPParser:
    """Streaming, zero-copy/cursor-based RESP2 protocol deserializer.

    Supports pipelined commands and fragmented TCP byte streams.
    """

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._pos = 0

    def feed(self, chunk: bytes) -> None:
        """Append incoming bytes to the parser buffer."""
        if chunk:
            self._buffer.extend(chunk)

    def reset(self) -> None:
        """Clear parser buffer and reset cursor."""
        self._buffer.clear()
        self._pos = 0

    @property
    def has_pending_data(self) -> bool:
        """Return True if unparsed bytes remain in the buffer."""
        return self._pos < len(self._buffer)

    def _maybe_compact(self) -> None:
        """Compact buffer when consumed data exceeds threshold or everything is consumed."""
        if self._pos >= len(self._buffer):
            self._buffer.clear()
            self._pos = 0
        elif self._pos > _COMPACT_THRESHOLD:
            del self._buffer[:self._pos]
            self._pos = 0

    def get_next_object(self) -> Optional[Any]:
        """Parse and return the next complete RESP object from the buffer.

        Returns None if buffer has insufficient data to form a complete object
        or if the parsed object is null (RESP null bulk string/array).
        """
        if self._pos >= len(self._buffer):
            return None

        success, obj, new_pos = self._parse_object(self._pos)
        if not success:
            return None

        self._pos = new_pos
        self._maybe_compact()
        return obj

    def get_all_objects(self) -> list[Any]:
        """Parse and return all complete RESP objects currently in the buffer."""
        objects = []
        while self._pos < len(self._buffer):
            success, obj, new_pos = self._parse_object(self._pos)
            if not success:
                break
            self._pos = new_pos
            self._maybe_compact()
            objects.append(obj)
        return objects

    def _parse_object(self, pos: int) -> tuple[bool, Any, int]:
        """Attempt to parse one object starting at pos.

        Returns (success: bool, obj: Any, new_pos: int).
        If incomplete, returns (False, None, pos).
        """
        if pos >= len(self._buffer):
            return False, None, pos

        prefix = self._buffer[pos]

        if prefix == _BYTE_PLUS:
            crlf = self._buffer.find(_CRLF, pos + 1)
            if crlf == -1:
                return False, None, pos
            val = self._buffer[pos + 1 : crlf].decode("utf-8", errors="replace")
            return True, val, crlf + 2

        if prefix == _BYTE_MINUS:
            crlf = self._buffer.find(_CRLF, pos + 1)
            if crlf == -1:
                return False, None, pos
            val = self._buffer[pos + 1 : crlf].decode("utf-8", errors="replace")
            return True, RESPError(val), crlf + 2

        if prefix == _BYTE_COLON:
            crlf = self._buffer.find(_CRLF, pos + 1)
            if crlf == -1:
                return False, None, pos
            raw = self._buffer[pos + 1 : crlf]
            try:
                num = int(raw)
            except ValueError:
                raise RESPError(f"Protocol error: invalid integer {bytes(raw)!r}")
            return True, num, crlf + 2

        if prefix == _BYTE_DOLLAR:
            crlf = self._buffer.find(_CRLF, pos + 1)
            if crlf == -1:
                return False, None, pos
            raw_len = self._buffer[pos + 1 : crlf]
            try:
                length = int(raw_len)
            except ValueError:
                raise RESPError(f"Protocol error: invalid bulk string length {bytes(raw_len)!r}")

            if length == -1:
                return True, None, crlf + 2
            if length < -1:
                raise RESPError(f"Protocol error: invalid negative bulk string length {length}")

            data_start = crlf + 2
            data_end = data_start + length
            if len(self._buffer) < data_end + 2:
                return False, None, pos

            if self._buffer[data_end : data_end + 2] != _CRLF:
                raise RESPError(
                    f"Protocol error: expected CRLF after bulk string data, got {bytes(self._buffer[data_end:data_end+2])!r}"
                )

            data = bytes(self._buffer[data_start : data_end])
            return True, data, data_end + 2

        if prefix == _BYTE_STAR:
            crlf = self._buffer.find(_CRLF, pos + 1)
            if crlf == -1:
                return False, None, pos
            raw_count = self._buffer[pos + 1 : crlf]
            try:
                count = int(raw_count)
            except ValueError:
                raise RESPError(f"Protocol error: invalid array length {bytes(raw_count)!r}")

            if count == -1:
                return True, None, crlf + 2
            if count < -1:
                raise RESPError(f"Protocol error: invalid negative array length {count}")
            if count == 0:
                return True, [], crlf + 2

            items = []
            curr = crlf + 2
            for _ in range(count):
                success, item, curr = self._parse_object(curr)
                if not success:
                    return False, None, pos
                items.append(item)
            return True, items, curr

        # Unexpected prefix byte
        prefix_byte = bytes(self._buffer[pos : pos + 1])
        raise RESPError(f"Protocol error: unexpected byte {prefix_byte!r}")
