from typing import Any, Tuple

def bencode(obj: Any) -> bytes:
    """Encodes a Python object into canonical Bencoding format."""
    if isinstance(obj, int):
        return f"i{obj}e".encode("ascii")
    elif isinstance(obj, bytes):
        return f"{len(obj)}:".encode("ascii") + obj
    elif isinstance(obj, str):
        b = obj.encode("utf-8")
        return f"{len(b)}:".encode("ascii") + b
    elif isinstance(obj, (list, tuple)):
        return b"l" + b"".join(bencode(x) for x in obj) + b"e"
    elif isinstance(obj, dict):
        # Keys must be bytes or strings, sorted in lexicographical byte order
        def get_byte_key(k):
            return k if isinstance(k, bytes) else str(k).encode("utf-8")

        sorted_items = sorted(obj.items(), key=lambda item: get_byte_key(item[0]))
        out = [b"d"]
        for k, v in sorted_items:
            out.append(bencode(k))
            out.append(bencode(v))
        out.append(b"e")
        return b"".join(out)
    else:
        raise TypeError(f"Object of type {type(obj)} is not bencode serializable")

def bdecode(data: bytes, offset: int = 0) -> Tuple[Any, int]:
    """Decodes bencoded bytes into a Python object and returns (obj, consumed_bytes)."""
    if offset >= len(data):
        raise ValueError("Unexpected EOF in bdecode")

    indicator = data[offset:offset+1]

    if indicator == b"i":
        # Integer: i<digits>e
        end = data.find(b"e", offset + 1)
        if end == -1:
            raise ValueError("Unterminated integer in bdecode")
        val = int(data[offset+1:end].decode("ascii"))
        return val, (end + 1 - offset)

    elif indicator.isdigit():
        # Byte string: <length>:<bytes>
        colon = data.find(b":", offset)
        if colon == -1:
            raise ValueError("Unterminated string length in bdecode")
        length = int(data[offset:colon].decode("ascii"))
        str_start = colon + 1
        str_end = str_start + length
        if str_end > len(data):
            raise ValueError("String length extends beyond buffer in bdecode")
        return data[str_start:str_end], (str_end - offset)

    elif indicator == b"l":
        # List: l<items>e
        items = []
        cur = offset + 1
        while cur < len(data) and data[cur:cur+1] != b"e":
            val, consumed = bdecode(data, cur)
            items.append(val)
            cur += consumed
        if cur >= len(data) or data[cur:cur+1] != b"e":
            raise ValueError("Unterminated list in bdecode")
        return items, (cur + 1 - offset)

    elif indicator == b"d":
        # Dictionary: d<key><val>e
        res = {}
        cur = offset + 1
        while cur < len(data) and data[cur:cur+1] != b"e":
            k, c_k = bdecode(data, cur)
            cur += c_k
            v, c_v = bdecode(data, cur)
            cur += c_v
            res[k] = v
        if cur >= len(data) or data[cur:cur+1] != b"e":
            raise ValueError("Unterminated dictionary in bdecode")
        return res, (cur + 1 - offset)

    else:
        raise ValueError(f"Unknown bencode indicator: {indicator}")
