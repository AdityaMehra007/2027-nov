"""Data models for OmniSwarm peer mesh and actor communications."""

from __future__ import annotations

import datetime
from enum import Enum, IntEnum
from typing import Any
from pydantic import BaseModel, Field


class MessagePriority(IntEnum):
    """Priority levels for actor message queues. Lower integer = higher urgency."""

    EMERGENCY = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class ActorState(str, Enum):
    """Lifecycle states of a Swarm virtual actor."""

    STARTING = "STARTING"
    ACTIVE = "ACTIVE"
    BUSY = "BUSY"
    SUSPENDED = "SUSPENDED"
    FAILED = "FAILED"
    TERMINATED = "TERMINATED"


class SwarmMessage(BaseModel):
    """Deterministic, tamper-proof envelope for inter-actor and inter-node frames."""

    message_id: str = Field(description="Unique UUIDv4 message identifier")
    sender_node_id: str = Field(description="Fingerprint of sending node")
    sender_actor_id: str = Field(description="ID of sending actor")
    recipient_node_id: str = Field(description="Target node fingerprint, or '*' for broadcast")
    recipient_actor_id: str = Field(description="Target actor ID, or '*' for broadcast")
    channel: str = Field(description="Logical topic or routing channel")
    priority: MessagePriority = Field(default=MessagePriority.NORMAL, description="Message priority rank")
    timestamp: str = Field(description="ISO 8601 UTC timestamp")
    nonce: str = Field(description="Random cryptographic nonce for replay protection")
    payload: dict[str, Any] = Field(default_factory=dict, description="Arbitrary message body")
    signature: str = Field(default="", description="Ed25519 hex signature over canonical envelope")


class PeerNode(BaseModel):
    """Descriptor of a remote or local swarm peer node in the mesh."""

    node_id: str = Field(description="Node public fingerprint (node_<hex>)")
    host: str = Field(description="IP address or hostname")
    port: int = Field(description="WebSocket listening port")
    status: str = Field(default="alive", description="SWIM status: alive, suspect, dead")
    incarnation: int = Field(default=0, description="SWIM incarnation counter for refutation")
    last_seen: float = Field(default=0.0, description="Timestamp of last verified contact")

    @property
    def url(self) -> str:
        """Derives the WebSocket endpoint URL for this peer."""
        return f"ws://{self.host}:{self.port}/ws/swarm"
