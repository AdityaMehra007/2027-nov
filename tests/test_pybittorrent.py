import hashlib
import pytest
from src.pybittorrent.bencode import bencode, bdecode
from src.pybittorrent.metainfo import Torrent
from src.pybittorrent.peer import PeerHandshake, PeerMessage, MessageType

def test_bencode_and_bdecode_integers():
    assert bencode(42) == b"i42e"
    assert bencode(-17) == b"i-17e"
    assert bencode(0) == b"i0e"

    val, consumed = bdecode(b"i42e")
    assert val == 42
    assert consumed == 4

    val, _ = bdecode(b"i-17e")
    assert val == -17

def test_bencode_and_bdecode_strings():
    assert bencode(b"spam") == b"4:spam"
    assert bencode("hello") == b"5:hello"
    assert bencode(b"") == b"0:"

    val, consumed = bdecode(b"4:spam")
    assert val == b"spam"
    assert consumed == 6

def test_bencode_and_bdecode_lists():
    data = [b"spam", 42, [b"inner"]]
    encoded = bencode(data)
    assert encoded == b"l4:spami42el5:inneree"

    val, _ = bdecode(encoded)
    assert val == data

def test_bencode_and_bdecode_dictionaries():
    data = {b"cow": b"moo", b"spam": 42}
    encoded = bencode(data)
    assert encoded == b"d3:cow3:moo4:spami42ee"

    val, _ = bdecode(encoded)
    assert val == data

def test_torrent_metainfo_and_info_hash():
    dummy_piece = hashlib.sha1(b"piece0").digest()
    torrent_dict = {
        b"announce": b"http://tracker.example.com/announce",
        b"info": {
            b"name": b"sample.iso",
            b"length": 1048576,
            b"piece length": 262144,
            b"pieces": dummy_piece
        }
    }
    raw_bytes = bencode(torrent_dict)
    torrent = Torrent.from_bytes(raw_bytes)

    assert torrent.announce == "http://tracker.example.com/announce"
    assert torrent.name == "sample.iso"
    assert torrent.length == 1048576
    assert torrent.piece_length == 262144
    assert len(torrent.pieces) == 1
    assert torrent.pieces[0] == dummy_piece

    # Verify info_hash is the SHA-1 of the bencoded info dictionary
    expected_hash = hashlib.sha1(bencode(torrent_dict[b"info"])).digest()
    assert torrent.info_hash == expected_hash

def test_peer_handshake():
    info_hash = b"\x01" * 20
    peer_id = b"-OMNIV-0000000000001"

    packet = PeerHandshake.build(info_hash=info_hash, peer_id=peer_id)
    assert len(packet) == 68

    parsed = PeerHandshake.parse(packet)
    assert parsed.protocol == b"BitTorrent protocol"
    assert parsed.info_hash == info_hash
    assert parsed.peer_id == peer_id

def test_peer_wire_messages():
    # Keepalive (len 0)
    msg_keep = PeerMessage.build_keepalive()
    assert msg_keep == b"\x00\x00\x00\x00"

    # Choke & Unchoke
    msg_choke = PeerMessage.build(MessageType.CHOKE)
    assert msg_choke == b"\x00\x00\x00\x01\x00"

    msg_unchoke = PeerMessage.build(MessageType.UNCHOKE)
    parsed = PeerMessage.parse(msg_unchoke)
    assert parsed.msg_type == MessageType.UNCHOKE

    # Have message
    msg_have = PeerMessage.build_have(piece_index=42)
    parsed_have = PeerMessage.parse(msg_have)
    assert parsed_have.msg_type == MessageType.HAVE
    assert parsed_have.payload == (42).to_bytes(4, byteorder="big")

    # Request message
    msg_req = PeerMessage.build_request(index=1, begin=0, length=16384)
    parsed_req = PeerMessage.parse(msg_req)
    assert parsed_req.msg_type == MessageType.REQUEST
    assert len(parsed_req.payload) == 12
