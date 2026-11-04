"""Tests for master SwarmKernel orchestration, security gating, and telemetry."""

import asyncio
import socket
import pytest
from omniverse.core.security import ActionType, ApprovalStatus, SecurityGovernor
from omniverse.core.telemetry import EventBus
from omniverse.swarm.actor import SwarmActor
from omniverse.swarm.kernel import SwarmKernel
from omniverse.swarm.models import MessagePriority, SwarmMessage


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class MockTraderActor(SwarmActor):
    def __init__(self, actor_id: str) -> None:
        super().__init__(actor_id)
        self.trades: list[dict] = []

    async def receive(self, message: SwarmMessage) -> None:
        self.trades.append(message.payload)


def test_kernel_init_and_actor_spawning():
    event_bus = EventBus()
    kernel = SwarmKernel(host="127.0.0.1", port=9091, event_bus=event_bus)

    assert kernel.node_id.startswith("node_")
    actor = kernel.spawn_actor(MockTraderActor, actor_id="trader_alpha")
    assert actor.actor_id == "trader_alpha"

    events = event_bus.get_events()
    assert any(e["event_name"] == "SWARM_ACTOR_SPAWNED" for e in events)


def test_kernel_local_dispatch():
    async def _runner():
        event_bus = EventBus()
        kernel = SwarmKernel(host="127.0.0.1", port=_get_free_port(), event_bus=event_bus)
        actor = kernel.spawn_actor(MockTraderActor, actor_id="trader_local")

        await kernel.start()

        msg_id = await kernel.send(
            sender_actor_id="operator",
            recipient_node_id=kernel.node_id,
            recipient_actor_id="trader_local",
            channel="trading.orders",
            payload={"symbol": "BTC/USD", "amount": 1.5},
            priority=MessagePriority.HIGH,
        )

        assert isinstance(msg_id, str)
        await asyncio.sleep(0.05)

        assert len(actor.trades) == 1
        assert actor.trades[0]["symbol"] == "BTC/USD"

        events = event_bus.get_events()
        assert any(e["event_name"] == "SWARM_MESSAGE_SENT" for e in events)

        await kernel.shutdown()

    asyncio.run(_runner())


def test_kernel_security_governor_gating():
    async def _runner():
        governor = SecurityGovernor(strict_mode=True)
        kernel = SwarmKernel(host="127.0.0.1", port=_get_free_port(), governor=governor)
        kernel.spawn_actor(MockTraderActor, actor_id="privileged_agent")
        await kernel.start()

        # Sending an unapproved financial transfer action must be gated by the governor
        with pytest.raises(PermissionError) as exc_info:
            await kernel.send(
                sender_actor_id="agent_x",
                recipient_node_id=kernel.node_id,
                recipient_actor_id="privileged_agent",
                channel="finance.transfers",
                payload={
                    "action_type": ActionType.FINANCIAL_TRANSFER.value,
                    "amount_usd": 25000.0,
                },
            )

        assert "Air-gapped SecurityGovernor requires human approval" in str(exc_info.value)
        await kernel.shutdown()

    asyncio.run(_runner())


def test_kernel_remote_peer_routing():
    async def _runner():
        port_a = _get_free_port()
        port_b = _get_free_port()

        kernel_a = SwarmKernel(host="127.0.0.1", port=port_a)
        kernel_b = SwarmKernel(host="127.0.0.1", port=port_b)

        target_actor = kernel_b.spawn_actor(MockTraderActor, actor_id="remote_agent_b")

        await kernel_a.start()
        await kernel_b.start()

        # Register peer B with A
        kernel_a.add_peer_node(kernel_b.local_node)
        await kernel_a.transport.connect_to_peer(
            kernel_b.node_id,
            f"ws://127.0.0.1:{port_b}/ws/swarm",
        )

        # Send from A to B
        await kernel_a.send(
            sender_actor_id="agent_a",
            recipient_node_id=kernel_b.node_id,
            recipient_actor_id="remote_agent_b",
            channel="tasks.remote",
            payload={"task": "BUILD_SCAFFOLD", "spec_id": 101},
        )

        for _ in range(25):
            if len(target_actor.trades) > 0:
                break
            await asyncio.sleep(0.02)

        assert len(target_actor.trades) == 1
        assert target_actor.trades[0]["spec_id"] == 101

        await kernel_a.shutdown()
        await kernel_b.shutdown()

    asyncio.run(_runner())
