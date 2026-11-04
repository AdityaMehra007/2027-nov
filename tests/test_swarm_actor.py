"""Tests for OmniSwarm virtual actors and supervisor auto-healing."""

import asyncio
import pytest
from omniverse.swarm.actor import ActorSupervisor, RestartPolicy, SwarmActor
from omniverse.swarm.mailbox import DeadLetterQueue
from omniverse.swarm.models import ActorState, MessagePriority, SwarmMessage


class CounterActor(SwarmActor):
    """Simple test actor that tallies received values."""

    def __init__(self, actor_id: str) -> None:
        super().__init__(actor_id)
        self.total = 0
        self.received_messages: list[str] = []

    async def receive(self, message: SwarmMessage) -> None:
        self.received_messages.append(message.message_id)
        self.total += message.payload.get("amount", 0)


class CrashingActor(SwarmActor):
    """Actor that crashes on specific triggers."""

    def __init__(self, actor_id: str) -> None:
        super().__init__(actor_id)
        self.processed = 0

    async def receive(self, message: SwarmMessage) -> None:
        if message.payload.get("crash"):
            raise ValueError("Intentional simulated crash")
        self.processed += 1


def _msg(msg_id: str, payload: dict) -> SwarmMessage:
    return SwarmMessage(
        message_id=msg_id,
        sender_node_id="node_1",
        sender_actor_id="sender",
        recipient_node_id="node_1",
        recipient_actor_id="target",
        channel="test",
        priority=MessagePriority.NORMAL,
        timestamp="2027-11-04T12:00:00Z",
        nonce="nonce",
        payload=payload,
        signature="sig",
    )


def test_actor_lifecycle_and_message_processing():
    async def _runner():
        actor = CounterActor(actor_id="counter_01")
        assert actor.state == ActorState.STARTING

        await actor.start()
        assert actor.state == ActorState.ACTIVE

        # Push messages
        await actor.mailbox.push(_msg("m1", {"amount": 10}))
        await actor.mailbox.push(_msg("m2", {"amount": 25}))

        # Wait for processing
        await asyncio.sleep(0.05)
        assert actor.total == 35
        assert actor.received_messages == ["m1", "m2"]

        await actor.stop()
        assert actor.state == ActorState.TERMINATED

    asyncio.run(_runner())


def test_supervisor_auto_healing_recovery():
    async def _runner():
        dlq = DeadLetterQueue()
        supervisor = ActorSupervisor(
            restart_policy=RestartPolicy.ONE_FOR_ONE,
            max_retries=3,
            backoff_base=0.01,
            dead_letter_queue=dlq,
        )

        actor = supervisor.spawn(CrashingActor, actor_id="flaky_01")
        await supervisor.start_all()

        # Send crash trigger followed by a valid message
        await actor.mailbox.push(_msg("bad_msg", {"crash": True}))
        await actor.mailbox.push(_msg("good_msg", {"crash": False}))

        # Wait for supervisor to restart and process
        await asyncio.sleep(0.1)

        # DLQ should contain bad_msg
        assert dlq.size() == 1
        assert dlq.get_entries()[0]["message_id"] == "bad_msg"

        # Actor should be ACTIVE and have processed good_msg
        assert actor.state == ActorState.ACTIVE
        assert actor.processed == 1
        assert supervisor.get_restart_count("flaky_01") == 1

        await supervisor.stop_all()

    asyncio.run(_runner())


def test_supervisor_max_retries_termination():
    async def _runner():
        dlq = DeadLetterQueue()
        supervisor = ActorSupervisor(
            restart_policy=RestartPolicy.ONE_FOR_ONE,
            max_retries=2,
            backoff_base=0.01,
            dead_letter_queue=dlq,
        )

        actor = supervisor.spawn(CrashingActor, actor_id="perma_crash")
        await supervisor.start_all()

        # Send 3 crash messages to exceed limit of 2 retries
        await actor.mailbox.push(_msg("c1", {"crash": True}))
        await actor.mailbox.push(_msg("c2", {"crash": True}))
        await actor.mailbox.push(_msg("c3", {"crash": True}))

        await asyncio.sleep(0.15)

        assert actor.state == ActorState.TERMINATED
        assert supervisor.get_restart_count("perma_crash") >= 2

        await supervisor.stop_all()

    asyncio.run(_runner())
