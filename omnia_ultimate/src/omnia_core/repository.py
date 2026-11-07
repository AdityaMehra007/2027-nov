from __future__ import annotations
from contextlib import contextmanager
import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any
from .audit import GENESIS, make_event
from .models import Approval, Task

class SQLiteRepository:
    """Single-node SQLite repository for local development.

    Do not treat it as a horizontally scalable production database.
    """
    def __init__(self, db_path: str | Path = "data/omnia.db"):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._initialise()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
        finally:
            conn.close()

    def _initialise(self) -> None:
        with self._lock, self._connect() as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                action TEXT NOT NULL,
                action_class TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                result_json TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approvals (
                approval_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL REFERENCES tasks(task_id),
                requested_by TEXT NOT NULL,
                reason TEXT NOT NULL,
                approved_by TEXT,
                decision_reason TEXT,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                decided_at REAL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                event_json TEXT NOT NULL
            );
            """)

    def _append_event(self, conn: sqlite3.Connection, event_type: str, aggregate_id: str,
                      actor: str, payload: dict[str, Any]) -> None:
        row = conn.execute("SELECT event_json FROM audit_events ORDER BY sequence DESC LIMIT 1").fetchone()
        previous = json.loads(row["event_json"])["event_hash"] if row else GENESIS
        event = make_event(event_type, aggregate_id, actor, payload, previous)
        conn.execute("INSERT INTO audit_events(event_json) VALUES (?)",
                     (json.dumps(event, sort_keys=True, separators=(",", ":")),))

    @staticmethod
    def _task(row: sqlite3.Row) -> Task:
        return Task(
            task_id=row["task_id"], title=row["title"], action=row["action"],
            action_class=row["action_class"], payload=json.loads(row["payload_json"]),
            status=row["status"], result=json.loads(row["result_json"]) if row["result_json"] else None,
            created_at=row["created_at"], updated_at=row["updated_at"]
        )

    def create_task(self, task: Task, actor: str = "local-user") -> Task:
        with self._lock, self._connect() as c:
            c.execute("BEGIN IMMEDIATE")
            c.execute("""INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?)""", (
                task.task_id, task.title, task.action, task.action_class,
                json.dumps(task.payload), task.status, None, task.created_at, task.updated_at
            ))
            self._append_event(c, "task.created", task.task_id, actor,
                               {"title": task.title, "action": task.action, "action_class": task.action_class})
            c.commit()
        return task

    def get_task(self, task_id: str) -> Task | None:
        with self._connect() as c:
            row = c.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            return self._task(row) if row else None

    def list_tasks(self, limit: int = 100) -> list[Task]:
        with self._connect() as c:
            rows = c.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            return [self._task(r) for r in rows]

    def update_status(self, task_id: str, status: str, actor: str,
                      result: dict[str, Any] | None = None) -> Task:
        with self._lock, self._connect() as c:
            c.execute("BEGIN IMMEDIATE")
            now = time.time()
            row = c.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if not row:
                c.rollback()
                raise KeyError("Task not found")
            result_json = json.dumps(result) if result is not None else row["result_json"]
            c.execute("UPDATE tasks SET status=?, result_json=?, updated_at=? WHERE task_id=?",
                      (status, result_json, now, task_id))
            self._append_event(c, "task.status_changed", task_id, actor,
                               {"from": row["status"], "to": status, "result_present": result is not None})
            new_row = c.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            c.commit()
            return self._task(new_row)

    def create_approval(self, approval: Approval) -> Approval:
        with self._lock, self._connect() as c:
            c.execute("BEGIN IMMEDIATE")
            c.execute("INSERT INTO approvals VALUES (?,?,?,?,?,?,?,?,?)", (
                approval.approval_id, approval.task_id, approval.requested_by, approval.reason,
                approval.approved_by, approval.decision_reason, approval.status,
                approval.created_at, approval.decided_at
            ))
            self._append_event(c, "approval.requested", approval.task_id, approval.requested_by,
                               {"approval_id": approval.approval_id, "reason": approval.reason})
            c.commit()
        return approval

    def decide_approval(self, approval_id: str, approved_by: str, reason: str, approved: bool) -> Approval:
        with self._lock, self._connect() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT * FROM approvals WHERE approval_id=?", (approval_id,)).fetchone()
            if not row:
                c.rollback()
                raise KeyError("Approval not found")
            if row["status"] != "pending":
                c.rollback()
                raise ValueError("Approval has already been decided")
            now = time.time()
            status = "approved" if approved else "rejected"
            c.execute("UPDATE approvals SET approved_by=?, decision_reason=?, status=?, decided_at=? WHERE approval_id=?",
                      (approved_by, reason, status, now, approval_id))
            self._append_event(c, "approval.decided", row["task_id"], approved_by,
                               {"approval_id": approval_id, "status": status, "reason": reason})
            new_row = c.execute("SELECT * FROM approvals WHERE approval_id=?", (approval_id,)).fetchone()
            c.commit()
            return self._approval(new_row)

    @staticmethod
    def _approval(row: sqlite3.Row) -> Approval:
        return Approval(
            approval_id=row["approval_id"], task_id=row["task_id"], requested_by=row["requested_by"],
            reason=row["reason"], approved_by=row["approved_by"],
            decision_reason=row["decision_reason"], status=row["status"],
            created_at=row["created_at"], decided_at=row["decided_at"]
        )

    def latest_approval(self, task_id: str) -> Approval | None:
        with self._connect() as c:
            row = c.execute("SELECT * FROM approvals WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
                            (task_id,)).fetchone()
            return self._approval(row) if row else None

    def events(self) -> list[dict[str, Any]]:
        with self._connect() as c:
            rows = c.execute("SELECT event_json FROM audit_events ORDER BY sequence").fetchall()
            return [json.loads(r["event_json"]) for r in rows]
