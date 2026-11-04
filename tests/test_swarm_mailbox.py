"""Tests for OmniSwarm prioritized actor mailbox and dead letter queue."""

import asyncio
import pytest
from omniverse.swarm.models import MessagePriority, SwarmMessage
from omniverse.swarm.mailbox import ActorMailbox, DeadLetterQueue, MailboxFullError


def _make_msg(msg_id: str, priority: MessagePriority) -> SwarmMessage:
    return SwarmMessage(
        message_id=msg_id,
        sender_node_id="node_001",
        sender_actor_id="actor_001",
        recipient_node_id="node_001",
        recipient_actor_id="actor_002",
        channel="test",
        priority=priority,
        timestamp="2027-11-04T12:00:00Z",
        nonce="testnonce",
        payload={"index": msg_id},
        signature="testsig",
    )


def test_mailbox_priority_ordering():
    async def _runner():
        mailbox = ActorMailbox(capacity=10)

        # Push in mixed priority order
        msg_low = _make_msg("low_1", MessagePriority.LOW)
        msg_normal = _make_msg("normal_1", MessagePriority.NORMAL)
        msg_high = _make_msg("high_1", MessagePriority.HIGH)
        msg_emergency = _make_msg("emergency_1", MessagePriority.EMERGENCY)
        msg_normal_2 = _make_msg("normal_2", MessagePriority.NORMAL)

        await mailbox.push(msg_low)
        await mailbox.push(msg_normal)
        await mailbox.push(msg_high)
        await mailbox.push(msg_emergency)
        await mailbox.push(msg_normal_2)

        assert mailbox.size() == 5

        # Should pop in strict priority order: EMERGENCY (0) -> HIGH (1) -> NORMAL (2) FIFO -> LOW (3)
        p1 = await mailbox.pop()
        p2 = await mailbox.pop()
        p3 = await mailbox.pop()
        p4 = await mailbox.pop()
        p5 = await mailbox.pop()

        assert p1.message_id == "emergency_1"
        assert p2.message_id == "high_1"
        assert p3.message_id == "normal_1"
        assert p4.message_id == "normal_2"
        assert p5.message_id == "low_1"
        assert mailbox.is_empty() is True

    asyncio.run(_runner())


def test_mailbox_bounded_capacity_backpressure():
    async def _runner():
        mailbox = ActorMailbox(capacity=2)

        await mailbox.push(_make_msg("m1", MessagePriority.NORMAL))
        await mailbox.push(_make_msg("m2", MessagePriority.NORMAL))

        with pytest.raises(MailboxFullError):
            await mailbox.push(_make_msg("m3", MessagePriority.HIGH))

    asyncio.run(_runner())


def test_dead_letter_queue():
    dlq = DeadLetterQueue(max_records=100)
    assert dlq.size() == 0

    msg = _make_msg("bad_msg_1", MessagePriority.NORMAL)
    dlq.quarantine(msg, reason="JSON serialization exception in actor receive()")

    assert dlq.size() == 1
    entries = dlq.get_entries()
    assert len(entries) == 1
    assert entries[0]["message_id"] == "bad_msg_1"
    assert "JSON serialization exception" in entries[0]["reason"]
