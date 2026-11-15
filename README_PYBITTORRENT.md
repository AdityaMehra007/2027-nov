# `src/pybittorrent` - Zero-Dependency BitTorrent Protocol & Bencoding Engine

A pure Python 3.13 standard library implementation of the BitTorrent Peer-to-Peer specification (BEP 0003), including canonical Bencoding serialization/deserialization, metainfo `.torrent` file parsing, info-hash calculation, 68-byte peer handshakes, and wire message framing.

---

## Architecture & Primitives

```
                  Raw .torrent Binary File
                            |
                            v
               [ Canonical Bencoding Parser ]
               - Integer Encoding: `i<digits>e`
               - Byte String Encoding: `<len>:<data>`
               - List Encoding: `l<items>e`
               - Dictionary Encoding: `d<key><val>e` (byte-sorted)
                            |
                            v
               [ Metainfo Torrent Structure ]
               - 20-byte SHA-1 Piece Digest Validation
               - Info Dictionary Canonical SHA-1 Info-Hash
                            |
                            v
             [ Peer Wire Protocol (BEP 0003) ]
             - 68-byte Handshake Frame:
               `[19] + "BitTorrent protocol" + [8-byte reserved] + [info_hash] + [peer_id]`
             - Wire Framing: `[4-byte len] + [1-byte id] + [payload]`
             - Messages: KEEP-ALIVE, CHOKE, UNCHOKE, INTERESTED, HAVE, REQUEST, PIECE
```

---

## Quickstart Usage

```python
from src.pybittorrent.bencode import bencode, bdecode
from src.pybittorrent.metainfo import Torrent
from src.pybittorrent.peer import PeerHandshake, PeerMessage, MessageType

# Bencoding
encoded = bencode({"name": "ubuntu.iso", "size": 1048576})
decoded, _ = bdecode(encoded)

# Handshake
packet = PeerHandshake.build(info_hash=b"\x01"*20, peer_id=b"-OMNIV-0000000000001")
parsed_handshake = PeerHandshake.parse(packet)

# Peer Wire
msg_unchoke = PeerMessage.build(MessageType.UNCHOKE)
msg_req = PeerMessage.build_request(index=0, begin=0, length=16384)
```

---

## Test Suite

```bash
python -m pytest tests/test_pybittorrent.py -v
```
All 7 test specifications pass with 100% fidelity.
