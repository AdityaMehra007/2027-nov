"""Tests for duplex WebSocket mesh transport in OmniSwarm."""

import asyncio
import socket
import pytest
from omniverse.swarm.models import MessagePriority, SwarmMessage
from omniverse.swarm.transport import MeshTransport


def _get_free_port() -> int:
    """Allocates an ephemeral free localhost TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _msg(msg_id: str) -> SwarmMessage:
    return SwarmMessage(
        message_id=msg_id,
        sender_node_id="node_sender",
        sender_actor_id="actor_s",
        recipient_node_id="node_receiver",
        recipient_actor_id="actor_r",
        channel="test.transport",
        priority=MessagePriority.HIGH,
        timestamp="2027-11-04T12:00:00Z",
        nonce="nonce123",
        payload={"ping": True, "value": 42},
        signature="sig123",
    )


def test_transport_unconnected_peer_handling():
    async def _runner():
        transport = MeshTransport(local_node_id="node_sender", host="127.0.0.1", port=9999)
        msg = _msg("msg_001")
        # Attempting to send to unconnected peer returns False gracefully
        success = await transport.send_frame("node_unconnected", msg)
        assert success is False

    asyncio.run(_runner())


def test_transport_duplex_communication():
    async def _runner():
        port = _get_free_port()
        received_messages: list[SwarmMessage] = []

        # Server Node (Receiver)
        server_transport = MeshTransport(local_node_id="node_receiver", host="127.0.0.1", port=port)

        async def _on_inbound(msg: SwarmMessage) -> None:
            received_messages.append(msg)

        server_transport.register_inbound_handler(_on_inbound)
        await server_transport.start_server()

        # Client Node (Sender)
        client_transport = MeshTransport(local_node_id="node_sender", host="127.0.0.1", port=_get_free_port())
        connected = await client_transport.connect_to_peer(
            peer_node_id="node_receiver",
            url=f"ws://127.0.0.1:{port}/ws/swarm",
        )
        assert connected is True

        test_message = _msg("msg_wire_001")
        sent = await client_transport.send_frame("node_receiver", test_message)
        assert sent is True

        # Wait for delivery over socket
        for _ in range(20):
            if len(received_messages) > 0:
                break
            await asyncio.sleep(0.02)

        assert len(received_messages) == 1
        rx = received_messages[0]
        assert rx.message_id == "msg_wire_001"
        assert rx.payload == {"ping": True, "value": 42}
        assert rx.priority == MessagePriority.HIGH

        await client_transport.stop()
        await server_transport.stop()

    asyncio.run(_runner())
