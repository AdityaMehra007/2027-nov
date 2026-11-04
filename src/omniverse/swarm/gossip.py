"""SWIM-inspired epidemic gossip protocol for decentralized OmniSwarm membership."""

from __future__ import annotations

import random
import time
from typing import Any
from omniverse.swarm.models import PeerNode


class SWIMGossip:
    """Manages decentralized peer discovery, health probes, and suspicion state machines."""

    def __init__(
        self,
        local_node: PeerNode,
        ping_period: float = 1.0,
        ping_timeout: float = 0.5,
        suspect_timeout: float = 5.0,
        indirect_peers_k: int = 3,
    ) -> None:
        self.local_node = local_node
        self.ping_period = ping_period
        self.ping_timeout = ping_timeout
        self.suspect_timeout = suspect_timeout
        self.indirect_peers_k = indirect_peers_k

        self._peers: dict[str, PeerNode] = {local_node.node_id: local_node}
        self._suspect_timestamps: dict[str, float] = {}
        self._peer_order: list[str] = []
        self._probe_index: int = 0

    def add_peer(self, peer: PeerNode) -> None:
        """Registers or updates a peer node."""
        self._peers[peer.node_id] = peer
        if peer.node_id not in self._peer_order and peer.node_id != self.local_node.node_id:
            self._peer_order.append(peer.node_id)

    def get_peer(self, node_id: str) -> PeerNode | None:
        """Returns peer node metadata by ID."""
        return self._peers.get(node_id)

    def get_active_peers(self) -> list[PeerNode]:
        """Returns all peers currently marked alive or suspect (excluding local node)."""
        return [
            peer
            for peer in self._peers.values()
            if peer.node_id != self.local_node.node_id and peer.status in ("alive", "suspect")
        ]

    def mark_suspect(self, target_node_id: str) -> None:
        """Transitions a node to suspect status and begins grace timer."""
        peer = self._peers.get(target_node_id)
        if peer and peer.status != "dead":
            peer.status = "suspect"
            self._suspect_timestamps[target_node_id] = time.time()

    def process_ack(self, sender_node_id: str) -> None:
        """Handles an incoming probe ACK, refreshing freshness and restoring alive state."""
        peer = self._peers.get(sender_node_id)
        if peer:
            peer.last_seen = time.time()
            peer.status = "alive"
            self._suspect_timestamps.pop(sender_node_id, None)

    def process_alive(self, target_node: PeerNode) -> None:
        """Processes an ALIVE refutation or update with incarnation comparison."""
        existing = self._peers.get(target_node.node_id)
        if not existing:
            self.add_peer(target_node)
            return

        if target_node.incarnation >= existing.incarnation:
            existing.status = "alive"
            existing.incarnation = target_node.incarnation
            existing.last_seen = time.time()
            self._suspect_timestamps.pop(target_node.node_id, None)

    def evaluate_suspects(self) -> list[str]:
        """Checks for suspect nodes that have breached grace timeout, transitioning to dead."""
        now = time.time()
        evicted: list[str] = []
        for node_id, suspect_start in list(self._suspect_timestamps.items()):
            if now - suspect_start >= self.suspect_timeout:
                peer = self._peers.get(node_id)
                if peer:
                    peer.status = "dead"
                self._suspect_timestamps.pop(node_id, None)
                evicted.append(node_id)
        return evicted

    def tick(self) -> list[tuple[str, str, dict[str, Any]]]:
        """Executes one round of SWIM failure detection, returning probe actions."""
        self.evaluate_suspects()

        candidates = [
            nid for nid in self._peer_order
            if self._peers.get(nid) and self._peers[nid].status in ("alive", "suspect")
        ]
        if not candidates:
            return []

        # Rotate probe target
        if self._probe_index >= len(candidates):
            self._probe_index = 0
            random.shuffle(self._peer_order)
            candidates = [
                nid for nid in self._peer_order
                if self._peers.get(nid) and self._peers[nid].status in ("alive", "suspect")
            ]
            if not candidates:
                return []

        target_id = candidates[self._probe_index % len(candidates)]
        self._probe_index += 1

        probe_action = (
            "PING",
            target_id,
            {
                "sender_id": self.local_node.node_id,
                "incarnation": self.local_node.incarnation,
                "timestamp": time.time(),
            },
        )
        return [probe_action]
