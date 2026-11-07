from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import time, uuid

TASK_STATES = {"not_started", "researching", "specified", "in_progress", "in_review",
               "testing", "blocked", "completed", "rejected", "deferred"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
EVIDENCE_CLASSES = {"fact", "estimate", "hypothesis", "observation", "opinion"}

def identifier(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"

@dataclass(frozen=True)
class Record:
    id: str
    created_at: float
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
