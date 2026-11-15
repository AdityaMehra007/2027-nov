import struct
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional

class MessageType(IntEnum):
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8

@dataclass
class PeerHandshake:
    protocol: bytes
    info_hash: bytes
    peer_id: bytes

    @classmethod
    def build(cls, info_hash: bytes, peer_id: bytes) -> bytes:
        pstr = b"BitTorrent protocol"
        pstrlen = len(pstr)
        reserved = b"\x00" * 8
        if len(info_hash) != 20:
            raise ValueError("info_hash must be exactly 20 bytes")
        if len(peer_id) != 20:
            raise ValueError("peer_id must be exactly 20 bytes")
        return struct.pack(f">B{pstrlen}s8s20s20s", pstrlen, pstr, reserved, info_hash, peer_id)

    @classmethod
    def parse(cls, data: bytes) -> "PeerHandshake":
        if len(data) < 68:
            raise ValueError("Handshake buffer must be at least 68 bytes")
        pstrlen = data[0]
        pstr = data[1:1+pstrlen]
        if pstr != b"BitTorrent protocol":
            raise ValueError(f"Invalid BitTorrent protocol header: {pstr}")
        # Reserved: bytes 1+pstrlen to 9+pstrlen
        info_hash = data[9+pstrlen:29+pstrlen]
        peer_id = data[29+pstrlen:49+pstrlen]
        return cls(protocol=pstr, info_hash=info_hash, peer_id=peer_id)

@dataclass
class PeerMessage:
    msg_type: Optional[MessageType]
    payload: bytes = b""

    @classmethod
    def build_keepalive(cls) -> bytes:
        return struct.pack(">I", 0)

    @classmethod
    def build(cls, msg_type: MessageType, payload: bytes = b"") -> bytes:
        length = 1 + len(payload)
        return struct.pack(f">IB{len(payload)}s", length, int(msg_type), payload)

    @classmethod
    def build_have(cls, piece_index: int) -> bytes:
        return cls.build(MessageType.HAVE, struct.pack(">I", piece_index))

    @classmethod
    def build_request(cls, index: int, begin: int, length: int) -> bytes:
        payload = struct.pack(">III", index, begin, length)
        return cls.build(MessageType.REQUEST, payload)

    @classmethod
    def parse(cls, data: bytes) -> "PeerMessage":
        if len(data) < 4:
            raise ValueError("Message buffer too short for length prefix")
        length = struct.unpack(">I", data[:4])[0]
        if length == 0:
            return cls(msg_type=None, payload=b"")

        msg_id = data[4]
        payload = data[5:4+length]
        return cls(msg_type=MessageType(msg_id), payload=payload)
