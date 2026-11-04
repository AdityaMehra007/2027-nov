"""Master SwarmKernel orchestrator unifying actors, gossip, transport, and security."""

from __future__ import annotations

import datetime
import logging
import secrets
import uuid
from typing import Any, TypeVar
from omniverse.core.security import ActionType, ApprovalStatus, SecurityGovernor
from omniverse.core.telemetry import EventBus, global_event_bus
from omniverse.swarm.actor import ActorSupervisor, SwarmActor
from omniverse.swarm.crypto import SwarmCrypto
from omniverse.swarm.gossip import SWIMGossip
from omniverse.swarm.mailbox import DeadLetterQueue
from omniverse.swarm.models import MessagePriority, PeerNode, SwarmMessage
from omniverse.swarm.transport import MeshTransport

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=SwarmActor)


class SwarmKernel:
    """Master node kernel for OmniSwarm.

    Coordinates cryptographic identity, actor lifecycle, SWIM membership,
    WebSocket transport, and air-gapped security governance.
    """

    def __init__(
        self,
        node_id: str | None = None,
        host: str = "127.0.0.1",
        port: int = 9091,
        governor: SecurityGovernor | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.governor = governor or SecurityGovernor()
        self.event_bus = event_bus or global_event_bus

        # Generate Ed25519 identity keypair
        self._private_key, self._public_key = SwarmCrypto.generate_keypair()
        self.node_id = node_id or SwarmCrypto.derive_node_id(self._public_key)

        # Core subsystems
        self.dlq = DeadLetterQueue()
        self.supervisor = ActorSupervisor(dead_letter_queue=self.dlq)
        self.local_node = PeerNode(
            node_id=self.node_id,
            host=self.host,
            port=self.port,
            status="alive",
            incarnation=0,
        )
        self.gossip = SWIMGossip(local_node=self.local_node)
        self.transport = MeshTransport(
            local_node_id=self.node_id,
            host=self.host,
            port=self.port,
        )

    def spawn_actor(self, actor_cls: type[T], actor_id: str, **kwargs: Any) -> T:
        """Spawns an actor under the supervised actor kernel."""
        actor = self.supervisor.spawn(actor_cls, actor_id=actor_id, **kwargs)
        self.event_bus.publish(
            "SWARM_ACTOR_SPAWNED",
            {"actor_id": actor_id, "node_id": self.node_id},
        )
        return actor

    def add_peer_node(self, peer: PeerNode) -> None:
        """Registers a remote peer in the gossip membership registry."""
        self.gossip.add_peer(peer)
        self.event_bus.publish(
            "SWARM_PEER_ADDED",
            {"peer_node_id": peer.node_id, "host": peer.host, "port": peer.port},
        )

    async def start(self) -> None:
        """Boots the transport server and all supervised virtual actors."""
        self.transport.register_inbound_handler(self._handle_inbound_frame)
        await self.transport.start_server()
        await self.supervisor.start_all()
        self.event_bus.publish(
            "SWARM_KERNEL_STARTED",
            {"node_id": self.node_id, "port": self.port},
        )
        logger.info("SwarmKernel %s booted on port %d", self.node_id, self.port)

    async def shutdown(self) -> None:
        """Performs graceful shutdown of all actors and transport connections."""
        await self.supervisor.stop_all()
        await self.transport.stop()
        self.event_bus.publish(
            "SWARM_KERNEL_STOPPED",
            {"node_id": self.node_id},
        )
        logger.info("SwarmKernel %s stopped.", self.node_id)

    async def send(
        self,
        sender_actor_id: str,
        recipient_node_id: str,
        recipient_actor_id: str,
        channel: str,
        payload: dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> str:
        """Signs and routes a message to a local actor or remote peer node."""
        # 1. Security Governor Interception for privileged actions
        action_type_str = payload.get("action_type")
        if action_type_str:
            try:
                action_type = ActionType(action_type_str)
                status = self.governor.check_action(action_type, payload)
                if status == ApprovalStatus.REQUIRES_APPROVAL:
                    req_id = self.governor.request_approval(action_type, payload)
                    raise PermissionError(
                        f"Air-gapped SecurityGovernor requires human approval for action "
                        f"'{action_type.value}'. Request ID: {req_id}"
                    )
            except ValueError:
                pass  # Unrecognized action types pass through standard actor validation

        # 2. Build envelope
        msg_id = f"msg_{uuid.uuid4()}"
        timestamp_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        nonce = secrets.token_hex(8)

        envelope_dict: dict[str, Any] = {
            "message_id": msg_id,
            "sender_node_id": self.node_id,
            "sender_actor_id": sender_actor_id,
            "recipient_node_id": recipient_node_id,
            "recipient_actor_id": recipient_actor_id,
            "channel": channel,
            "priority": int(priority),
            "timestamp": timestamp_str,
            "nonce": nonce,
            "payload": payload,
        }

        # 3. Cryptographic Signature
        signature = SwarmCrypto.sign_message(self._private_key, envelope_dict)
        envelope_dict["signature"] = signature

        message = SwarmMessage(**envelope_dict)

        # 4. Routing
        if recipient_node_id in (self.node_id, "*"):
            await self._dispatch_local(message)

        if recipient_node_id != self.node_id:
            await self.transport.send_frame(recipient_node_id, message)

        self.event_bus.publish(
            "SWARM_MESSAGE_SENT",
            {
                "message_id": msg_id,
                "sender_actor_id": sender_actor_id,
                "recipient_node_id": recipient_node_id,
                "recipient_actor_id": recipient_actor_id,
                "priority": int(priority),
            },
        )
        return msg_id

    async def _dispatch_local(self, message: SwarmMessage) -> None:
        """Delivers a message to local actor mailboxes."""
        if message.recipient_actor_id == "*":
            for actor in self.supervisor._actors.values():
                await actor.mailbox.push(message)
        else:
            actor = self.supervisor.get_actor(message.recipient_actor_id)
            if actor:
                await actor.mailbox.push(message)
            else:
                self.dlq.quarantine(
                    message,
                    reason=f"Recipient actor '{message.recipient_actor_id}' not found on node.",
                )

    async def _handle_inbound_frame(self, message: SwarmMessage) -> None:
        """Callback processing an incoming frame from transport."""
        self.event_bus.publish(
            "SWARM_MESSAGE_RECEIVED",
            {
                "message_id": message.message_id,
                "sender_node_id": message.sender_node_id,
                "recipient_actor_id": message.recipient_actor_id,
            },
        )
        if message.recipient_node_id in (self.node_id, "*"):
            await self._dispatch_local(message)
