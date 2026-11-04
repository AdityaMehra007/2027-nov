"""Tests for SWIM epidemic gossip membership protocol in OmniSwarm."""

import time
import pytest
from omniverse.swarm.gossip import SWIMGossip
from omniverse.swarm.models import PeerNode


def _make_peer(node_id: str, host: str = "127.0.0.1", port: int = 9091) -> PeerNode:
    return PeerNode(
        node_id=node_id,
        host=host,
        port=port,
        status="alive",
        incarnation=0,
        last_seen=time.time(),
    )


def test_gossip_peer_registration_and_active_list():
    local = _make_peer("node_local", port=9000)
    gossip = SWIMGossip(local_node=local, ping_period=1.0)

    p1 = _make_peer("node_B", port=9001)
    p2 = _make_peer("node_C", port=9002)

    gossip.add_peer(p1)
    gossip.add_peer(p2)

    active = gossip.get_active_peers()
    assert len(active) == 2
    assert {p.node_id for p in active} == {"node_B", "node_C"}


def test_gossip_tick_generates_direct_ping():
    local = _make_peer("node_local")
    gossip = SWIMGossip(local_node=local)
    gossip.add_peer(_make_peer("node_target"))

    actions = gossip.tick()
    assert len(actions) == 1
    action_type, target_id, data = actions[0]
    assert action_type == "PING"
    assert target_id == "node_target"
    assert data["sender_id"] == "node_local"


def test_gossip_ack_refreshes_last_seen():
    local = _make_peer("node_local")
    gossip = SWIMGossip(local_node=local)
    peer = _make_peer("node_target")
    old_time = time.time() - 10.0
    peer.last_seen = old_time
    gossip.add_peer(peer)

    gossip.process_ack("node_target")
    updated = gossip.get_peer("node_target")
    assert updated is not None
    assert updated.last_seen > old_time
    assert updated.status == "alive"


def test_gossip_suspect_and_alive_refutation():
    local = _make_peer("node_local")
    gossip = SWIMGossip(local_node=local, suspect_timeout=0.2)
    peer = _make_peer("node_target")
    gossip.add_peer(peer)

    # Mark suspect with incarnation 0
    gossip.mark_suspect("node_target")
    assert gossip.get_peer("node_target").status == "suspect"

    # Alive refutation with higher incarnation (1)
    refutation_peer = _make_peer("node_target")
    refutation_peer.incarnation = 1
    gossip.process_alive(refutation_peer)

    assert gossip.get_peer("node_target").status == "alive"
    assert gossip.get_peer("node_target").incarnation == 1


def test_gossip_dead_transition_after_timeout():
    local = _make_peer("node_local")
    gossip = SWIMGossip(local_node=local, suspect_timeout=0.05)
    peer = _make_peer("node_target")
    gossip.add_peer(peer)

    gossip.mark_suspect("node_target")
    assert gossip.get_peer("node_target").status == "suspect"

    # Wait for suspect timeout
    time.sleep(0.08)
    gossip.evaluate_suspects()

    assert gossip.get_peer("node_target").status == "dead"
    # Dead node is not in active peers list
    assert len(gossip.get_active_peers()) == 0
