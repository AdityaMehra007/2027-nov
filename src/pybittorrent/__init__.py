"""
pybittorrent: Zero-dependency BitTorrent Protocol & Bencoding Engine
Built for CASHFLOW INFINITY / ATLAS NEXUS reference architectures.
"""

from .bencode import bencode, bdecode
from .metainfo import Torrent
from .peer import PeerHandshake, PeerMessage, MessageType

__all__ = [
    "bencode",
    "bdecode",
    "Torrent",
    "PeerHandshake",
    "PeerMessage",
    "MessageType",
]
