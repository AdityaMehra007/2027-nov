"""
PROJECT OMNIA NEXUS: User Acceptance Testing & Retention Metrics Engine
Measures task completion rates, user workflow durations, and repeat usage frequency.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, List, Dict

@dataclass
class AcceptanceSession:
    session_id: str
    user_id: str
    workflow_id: str
    completed: bool
    duration_seconds: float
    csat_score: int # 1 to 5
    timestamp: float = field(default_factory=time.time)

class AcceptanceTracker:
    def __init__(self):
        self.sessions: List[AcceptanceSession] = []

    def record_session(self, session_id: str, user_id: str, workflow_id: str,
                       completed: bool, duration_seconds: float, csat_score: int) -> AcceptanceSession:
        if not (1 <= csat_score <= 5):
            raise ValueError("CSAT score must be between 1 and 5")
        session = AcceptanceSession(
            session_id=session_id,
            user_id=user_id,
            workflow_id=workflow_id,
            completed=completed,
            duration_seconds=duration_seconds,
            csat_score=csat_score
        )
        self.sessions.append(session)
        return session

    def metrics(self) -> dict[str, Any]:
        total = len(self.sessions)
        if total == 0:
            return {"total_sessions": 0, "completion_rate": 0.0, "avg_duration_sec": 0.0, "avg_csat": 0.0}

        completed_count = sum(1 for s in self.sessions if s.completed)
        avg_duration = sum(s.duration_seconds for s in self.sessions) / total
        avg_csat = sum(s.csat_score for s in self.sessions) / total

        # Repeat users
        user_counts: Dict[str, int] = {}
        for s in self.sessions:
            user_counts[s.user_id] = user_counts.get(s.user_id, 0) + 1
        repeat_users = sum(1 for count in user_counts.values() if count > 1)

        return {
            "total_sessions": total,
            "completion_rate": round(completed_count / total, 4),
            "avg_duration_sec": round(avg_duration, 2),
            "avg_csat": round(avg_csat, 2),
            "unique_users": len(user_counts),
            "repeat_users": repeat_users,
            "repeat_rate": round(repeat_users / len(user_counts), 4) if user_counts else 0.0
        }
