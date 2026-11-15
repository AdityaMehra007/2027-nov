import hashlib
from dataclasses import dataclass
from typing import List, Optional
from .bencode import bencode, bdecode

@dataclass
class Torrent:
    announce: str
    name: str
    length: int
    piece_length: int
    pieces: List[bytes]
    info_hash: bytes
    raw_dict: Optional[dict] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> "Torrent":
        decoded, _ = bdecode(data)
        if not isinstance(decoded, dict):
            raise ValueError("Torrent payload must be a bencoded dictionary")

        announce_raw = decoded.get(b"announce", b"")
        announce = announce_raw.decode("utf-8") if isinstance(announce_raw, bytes) else str(announce_raw)

        info = decoded.get(b"info")
        if not isinstance(info, dict):
            raise ValueError("Missing 'info' dictionary in torrent file")

        # Info hash is the SHA-1 of the raw bencoded 'info' dictionary
        info_hash = hashlib.sha1(bencode(info)).digest()

        name_raw = info.get(b"name", b"")
        name = name_raw.decode("utf-8") if isinstance(name_raw, bytes) else str(name_raw)

        length = info.get(b"length", 0)
        piece_length = info.get(b"piece length", 0)

        pieces_blob = info.get(b"pieces", b"")
        pieces = [pieces_blob[i:i+20] for i in range(0, len(pieces_blob), 20)]

        return cls(
            announce=announce,
            name=name,
            length=length,
            piece_length=piece_length,
            pieces=pieces,
            info_hash=info_hash,
            raw_dict=decoded
        )

    def to_bytes(self) -> bytes:
        if self.raw_dict:
            return bencode(self.raw_dict)

        info = {
            b"name": self.name.encode("utf-8"),
            b"length": self.length,
            b"piece length": self.piece_length,
            b"pieces": b"".join(self.pieces)
        }
        root = {
            b"announce": self.announce.encode("utf-8"),
            b"info": info
        }
        return bencode(root)
