"""Prioritized actor mailboxes and dead letter queue for OmniSwarm."""

from __future__ import annotations

import asyncio
import datetime
import itertools
from typing import Any
from omniverse.swarm.models import MessagePriority, SwarmMessage


class MailboxFullError(Exception):
    """Raised when an actor's bounded mailbox capacity is breached."""
    pass


class DeadLetterQueue:
    """Quarantines unprocessable or poison-pill messages with execution error metadata."""

    def __init__(self, max_records: int = 1000) -> None:
        self.max_records = max_records
        self._entries: list[dict[str, Any]] = []

    def quarantine(self, message: SwarmMessage, reason: str) -> None:
        """Appends a quarantined message record to the DLQ."""
        record = {
            "message_id": message.message_id,
            "sender_node_id": message.sender_node_id,
            "sender_actor_id": message.sender_actor_id,
            "channel": message.channel,
            "reason": reason,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "payload": message.payload,
        }
        self._entries.append(record)
        if len(self._entries) > self.max_records:
            self._entries.pop(0)

    def size(self) -> int:
        """Returns the number of quarantined messages."""
        return len(self._entries)

    def get_entries(self, limit: int = 50) -> list[dict[str, Any]]:
        """Returns up to `limit` latest DLQ entries."""
        return list(self._entries[-limit:])


class ActorMailbox:
    """Priority-queued, bounded async mailbox for a Swarm virtual actor."""

    def __init__(self, capacity: int = 1000) -> None:
        self.capacity = capacity
        self._queue: asyncio.PriorityQueue[tuple[int, int, SwarmMessage]] = asyncio.PriorityQueue(maxsize=capacity)
        self._counter = itertools.count()

    async def push(self, message: SwarmMessage) -> None:
        """Enqueues a message based on its priority. Raises MailboxFullError if at capacity."""
        if self._queue.full():
            raise MailboxFullError(
                f"Actor mailbox capacity limit ({self.capacity}) reached; backpressure triggered."
            )
        seq = next(self._counter)
        priority_val = int(message.priority)
        await self._queue.put((priority_val, seq, message))

    async def pop(self) -> SwarmMessage:
        """Dequeues the next highest-priority message (blocks if empty)."""
        _prio, _seq, message = await self._queue.get()
        return message

    def size(self) -> int:
        """Returns the current number of queued messages in the mailbox."""
        return self._queue.qsize()

    def is_empty(self) -> bool:
        """Returns True if the mailbox contains no pending messages."""
        return self._queue.empty()
