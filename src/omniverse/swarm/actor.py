"""Virtual actor abstraction and OTP-style supervision trees for OmniSwarm."""

from __future__ import annotations

import asyncio
import logging
from enum import Enum
from typing import Any, TypeVar
from omniverse.swarm.mailbox import ActorMailbox, DeadLetterQueue
from omniverse.swarm.models import ActorState, SwarmMessage

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="SwarmActor")


class RestartPolicy(str, Enum):
    """Supervision restart policies."""

    ONE_FOR_ONE = "ONE_FOR_ONE"
    ALL_FOR_ONE = "ALL_FOR_ONE"


class SwarmActor:
    """Base class for all virtual actors in the OmniSwarm mesh."""

    def __init__(self, actor_id: str, mailbox_capacity: int = 1000) -> None:
        self.actor_id = actor_id
        self.state: ActorState = ActorState.STARTING
        self.mailbox = ActorMailbox(capacity=mailbox_capacity)
        self._loop_task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """Starts the actor's asynchronous mailbox consumption loop."""
        self._stop_event.clear()
        self.state = ActorState.ACTIVE
        self._loop_task = asyncio.create_task(self._run_loop())

    async def _run_loop(self) -> None:
        """Internal processing loop consuming messages from mailbox."""
        while not self._stop_event.is_set():
            try:
                # Wait for next message or cancellation
                message = await self.mailbox.pop()
                if self._stop_event.is_set():
                    break
                self.state = ActorState.BUSY
                try:
                    await self.receive(message)
                finally:
                    if not self._stop_event.is_set() and self.state != ActorState.FAILED:
                        self.state = ActorState.ACTIVE
            except asyncio.CancelledError:
                break

    async def receive(self, message: SwarmMessage) -> Any:
        """Handler for inbound messages. Subclasses override this method."""
        raise NotImplementedError("Subclasses must implement receive()")

    async def stop(self) -> None:
        """Gracefully halts the actor and drains or terminates processing."""
        self._stop_event.set()
        self.state = ActorState.TERMINATED
        if self._loop_task and not self._loop_task.done():
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass


class ActorSupervisor:
    """Supervises actor lifecycles, provides auto-healing, and manages DLQ quarantine."""

    def __init__(
        self,
        restart_policy: RestartPolicy = RestartPolicy.ONE_FOR_ONE,
        max_retries: int = 5,
        retry_window_seconds: float = 60.0,
        backoff_base: float = 0.05,
        dead_letter_queue: DeadLetterQueue | None = None,
    ) -> None:
        self.restart_policy = restart_policy
        self.max_retries = max_retries
        self.retry_window_seconds = retry_window_seconds
        self.backoff_base = backoff_base
        self.dlq = dead_letter_queue or DeadLetterQueue()

        self._actors: dict[str, SwarmActor] = {}
        self._restart_counts: dict[str, int] = {}
        self._supervised_tasks: dict[str, asyncio.Task[None]] = {}
        self._running = False

    def spawn(self, actor_cls: type[T], actor_id: str, **kwargs: Any) -> T:
        """Instantiates and registers an actor under supervision."""
        actor = actor_cls(actor_id=actor_id, **kwargs)
        self._actors[actor_id] = actor
        self._restart_counts[actor_id] = 0
        return actor

    def get_actor(self, actor_id: str) -> SwarmActor | None:
        """Retrieves an active supervised actor by ID."""
        return self._actors.get(actor_id)

    def get_restart_count(self, actor_id: str) -> int:
        """Returns how many times the specified actor has been auto-restarted."""
        return self._restart_counts.get(actor_id, 0)

    async def start_all(self) -> None:
        """Starts supervision loops for all registered actors."""
        self._running = True
        for actor_id, actor in list(self._actors.items()):
            self._supervised_tasks[actor_id] = asyncio.create_task(
                self._supervision_loop(actor)
            )

    async def _supervision_loop(self, actor: SwarmActor) -> None:
        """Supervises an individual actor, intercepting crashes and executing restarts."""
        actor_id = actor.actor_id
        while self._running:
            actor.state = ActorState.ACTIVE
            actor._stop_event.clear()
            current_msg: SwarmMessage | None = None

            try:
                while self._running and not actor._stop_event.is_set():
                    current_msg = await actor.mailbox.pop()
                    if actor._stop_event.is_set() or not self._running:
                        break
                    actor.state = ActorState.BUSY
                    try:
                        await actor.receive(current_msg)
                    finally:
                        if not actor._stop_event.is_set():
                            actor.state = ActorState.ACTIVE
                    current_msg = None
            except asyncio.CancelledError:
                break
            except Exception as exc:
                actor.state = ActorState.FAILED
                logger.error(
                    "Actor %s crashed with error: %s", actor_id, exc, exc_info=True
                )

                # Quarantine the failing message to DLQ
                if current_msg is not None:
                    self.dlq.quarantine(current_msg, reason=f"Unhandled crash: {exc}")
                    current_msg = None

                self._restart_counts[actor_id] += 1
                attempts = self._restart_counts[actor_id]

                if attempts > self.max_retries:
                    logger.critical(
                        "Actor %s exceeded maximum retries (%d). Terminating.",
                        actor_id,
                        self.max_retries,
                    )
                    actor.state = ActorState.TERMINATED
                    break

                # Exponential backoff
                delay = min(self.backoff_base * (2 ** (attempts - 1)), 5.0)
                await asyncio.sleep(delay)

    async def stop_all(self) -> None:
        """Halts all supervised actors and supervisor tasks."""
        self._running = False
        for actor_id, task in list(self._supervised_tasks.items()):
            task.cancel()
        for actor_id, actor in list(self._actors.items()):
            await actor.stop()
        self._supervised_tasks.clear()
