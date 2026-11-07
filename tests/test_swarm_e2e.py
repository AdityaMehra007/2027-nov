"""High-density end-to-end stress tests for OmniSwarm virtual actor mesh."""

import asyncio
import socket
import time
import pytest
from omniverse.swarm.actor import SwarmActor
from omniverse.swarm.kernel import SwarmKernel
from omniverse.swarm.models import ActorState, MessagePriority, SwarmMessage


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class WorkerStressActor(SwarmActor):
    """Actor that counts and records messages under high concurrency."""

    def __init__(self, actor_id: str) -> None:
        super().__init__(actor_id=actor_id, mailbox_capacity=5000)
        self.message_count = 0
        self.sum_values = 0

    async def receive(self, message: SwarmMessage) -> None:
        self.message_count += 1
        self.sum_values += message.payload.get("val", 0)


def test_high_density_100_actor_stress():
    """Stress tests 100 concurrent virtual actors with high-frequency concurrent dispatch."""
    async def _runner():
        port = _get_free_port()
        kernel = SwarmKernel(host="127.0.0.1", port=port)
        await kernel.start()

        actor_count = 100
        messages_per_actor = 20
        total_expected_messages = actor_count * messages_per_actor

        actors: list[WorkerStressActor] = []
        for i in range(actor_count):
            actor_id = f"worker_actor_{i:03d}"
            actor = kernel.spawn_actor(WorkerStressActor, actor_id=actor_id)
            actors.append(actor)

        # Dispatch messages concurrently across all 100 actors
        t0 = time.perf_counter()

        async def _dispatch_for_actor(idx: int):
            target_id = f"worker_actor_{idx:03d}"
            for m in range(messages_per_actor):
                await kernel.send(
                    sender_actor_id="load_generator",
                    recipient_node_id=kernel.node_id,
                    recipient_actor_id=target_id,
                    channel="stress.test",
                    payload={"val": 1},
                    priority=MessagePriority.NORMAL,
                )

        tasks = [_dispatch_for_actor(i) for i in range(actor_count)]
        await asyncio.gather(*tasks)

        # Await completion of all mailbox queues
        timeout_seconds = 5.0
        start_wait = time.perf_counter()
        while time.perf_counter() - start_wait < timeout_seconds:
            total_processed = sum(a.message_count for a in actors)
            if total_processed >= total_expected_messages:
                break
            await asyncio.sleep(0.02)

        elapsed = time.perf_counter() - t0
        total_processed = sum(a.message_count for a in actors)
        throughput = total_processed / max(elapsed, 1e-6)

        # Assertions
        assert total_processed == total_expected_messages
        assert kernel.dlq.size() == 0
        for actor in actors:
            assert actor.state == ActorState.ACTIVE
            assert actor.message_count == messages_per_actor
            assert actor.sum_values == messages_per_actor

        assert throughput > 500.0  # Must exceed 500 msg/sec minimum across variable runner loads

        await kernel.shutdown()

    asyncio.run(_runner())
