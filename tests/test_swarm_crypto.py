"""Tests for OmniSwarm cryptographic identity and wire envelope models."""

import pytest
from omniverse.swarm.crypto import SwarmCrypto
from omniverse.swarm.models import ActorState, MessagePriority, PeerNode, SwarmMessage


def test_keypair_generation_and_address_derivation():
    private_key, public_key = SwarmCrypto.generate_keypair()
    assert private_key is not None
    assert public_key is not None

    node_id = SwarmCrypto.derive_node_id(public_key)
    assert node_id.startswith("node_")
    assert len(node_id) == len("node_") + 16

    # Determinism: same public key gives same node_id
    node_id_2 = SwarmCrypto.derive_node_id(public_key)
    assert node_id == node_id_2


def test_signature_creation_and_valid_verification():
    private_key, public_key = SwarmCrypto.generate_keypair()
    node_id = SwarmCrypto.derive_node_id(public_key)

    envelope = {
        "message_id": "msg_001",
        "sender_node_id": node_id,
        "sender_actor_id": "agent_alpha",
        "recipient_node_id": "*",
        "recipient_actor_id": "*",
        "channel": "system.gossip",
        "priority": int(MessagePriority.HIGH),
        "timestamp": "2027-11-04T12:00:00Z",
        "nonce": "abcdef0123456789",
        "payload": {"action": "PING", "incarnation": 1},
    }

    sig = SwarmCrypto.sign_message(private_key, envelope)
    assert isinstance(sig, str)
    assert len(sig) == 128  # 64 bytes hex encoded

    # Verification passes
    assert SwarmCrypto.verify_signature(public_key, envelope, sig) is True


def test_tampered_payload_rejected():
    private_key, public_key = SwarmCrypto.generate_keypair()
    node_id = SwarmCrypto.derive_node_id(public_key)

    envelope = {
        "message_id": "msg_002",
        "sender_node_id": node_id,
        "sender_actor_id": "agent_alpha",
        "recipient_node_id": "node_other",
        "recipient_actor_id": "agent_beta",
        "channel": "task.bidding",
        "priority": int(MessagePriority.NORMAL),
        "timestamp": "2027-11-04T12:00:00Z",
        "nonce": "1122334455667788",
        "payload": {"bid_amount": 100.0},
    }

    sig = SwarmCrypto.sign_message(private_key, envelope)

    # Tamper with payload
    tampered_envelope = dict(envelope)
    tampered_envelope["payload"] = {"bid_amount": 999999.0}

    assert SwarmCrypto.verify_signature(public_key, tampered_envelope, sig) is False


def test_swarm_message_pydantic_validation():
    msg = SwarmMessage(
        message_id="msg_003",
        sender_node_id="node_1234567812345678",
        sender_actor_id="agent_1",
        recipient_node_id="node_8765432187654321",
        recipient_actor_id="agent_2",
        channel="actor.direct",
        priority=MessagePriority.EMERGENCY,
        timestamp="2027-11-04T12:00:00Z",
        nonce="aabbccddeeff0011",
        payload={"status": "OK"},
        signature="deadbeef",
    )
    assert msg.priority == MessagePriority.EMERGENCY
    assert msg.payload["status"] == "OK"


def test_peer_node_model():
    peer = PeerNode(
        node_id="node_1234567812345678",
        host="127.0.0.1",
        port=9091,
        status="alive",
        incarnation=1,
    )
    assert peer.status == "alive"
    assert peer.incarnation == 1
    assert peer.url == "ws://127.0.0.1:9091/ws/swarm"
