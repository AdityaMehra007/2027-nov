"""RFC 6455 WebSocket Handshake and Framing Engine."""

from __future__ import annotations
import base64
from dataclasses import dataclass
import hashlib
import struct
from typing import Optional

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xA


@dataclass
class WebSocketFrame:
    fin: bool
    opcode: int
    payload: bytes


def compute_accept_key(sec_websocket_key: str) -> str:
    concat = (sec_websocket_key.strip() + WS_GUID).encode("utf-8")
    digest = hashlib.sha1(concat).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_websocket_frame(payload: str | bytes, opcode: int = OPCODE_TEXT, mask: bool = False) -> bytes:
    if isinstance(payload, str):
        data = payload.encode("utf-8")
    else:
        data = payload

    length = len(data)
    first_byte = 0x80 | (opcode & 0x0F)  # FIN = 1
    out = bytearray([first_byte])

    mask_bit = 0x80 if mask else 0x00
    if length <= 125:
        out.append(mask_bit | length)
    elif length <= 65535:
        out.append(mask_bit | 126)
        out.extend(struct.pack(">H", length))
    else:
        out.append(mask_bit | 127)
        out.extend(struct.pack(">Q", length))

    if mask:
        import os
        mask_key = os.urandom(4)
        out.extend(mask_key)
        masked_data = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data))
        out.extend(masked_data)
    else:
        out.extend(data)

    return bytes(out)


def parse_websocket_frame(data: bytes) -> Optional[WebSocketFrame]:
    if len(data) < 2:
        return None

    first_byte = data[0]
    fin = bool(first_byte & 0x80)
    opcode = first_byte & 0x0F

    second_byte = data[1]
    is_masked = bool(second_byte & 0x80)
    payload_len = second_byte & 0x7F

    offset = 2
    if payload_len == 126:
        if len(data) < offset + 2:
            return None
        payload_len = struct.unpack(">H", data[offset : offset + 2])[0]
        offset += 2
    elif payload_len == 127:
        if len(data) < offset + 8:
            return None
        payload_len = struct.unpack(">Q", data[offset : offset + 8])[0]
        offset += 8

    mask_key = b""
    if is_masked:
        if len(data) < offset + 4:
            return None
        mask_key = data[offset : offset + 4]
        offset += 4

    if len(data) < offset + payload_len:
        return None

    raw_payload = data[offset : offset + payload_len]
    if is_masked:
        unmasked = bytes(b ^ mask_key[i % 4] for i, b in enumerate(raw_payload))
    else:
        unmasked = raw_payload

    return WebSocketFrame(fin=fin, opcode=opcode, payload=unmasked)
