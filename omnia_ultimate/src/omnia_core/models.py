from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any
import time
import uuid

class ActionClass(str, Enum):
    READ_ONLY = "read_only"
    DRAFT = "draft"
    APPROVAL_REQUIRED = "approval_required"
    RESTRICTED = "restricted"

class TaskStatus(str, Enum):
    READY = "ready"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    action: str
    action_class: str
    payload: dict[str, Any]
    status: str
    result: dict[str, Any] | None
    created_at: float
    updated_at: float

    @staticmethod
    def new(title: str, action: str, action_class: ActionClass, payload: dict[str, Any]) -> "Task":
        now = time.time()
        status = TaskStatus.PENDING_APPROVAL if action_class == ActionClass.APPROVAL_REQUIRED else TaskStatus.READY
        return Task(
            task_id=str(uuid.uuid4()),
            title=title,
            action=action,
            action_class=action_class.value,
            payload=payload,
            status=status.value,
            result=None,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class Approval:
    approval_id: str
    task_id: str
    requested_by: str
    reason: str
    approved_by: str | None
    decision_reason: str | None
    status: str
    created_at: float
    decided_at: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
