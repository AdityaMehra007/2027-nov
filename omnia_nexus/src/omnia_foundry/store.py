from __future__ import annotations
import json, sqlite3, time
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from .audit import GENESIS, make_event

class Store:
    """Single-user, local SQLite store. Not production or multi-tenant safe."""
    def __init__(self, path: str | Path = "data/omnia_foundry.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.init()

    @contextmanager
    def connect(self):
        c = sqlite3.connect(self.path, timeout=15)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA journal_mode=WAL")
        try:
            yield c
        finally:
            c.close()

    def init(self):
        with self.connect() as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS programmes(
              programme_id TEXT PRIMARY KEY, name TEXT NOT NULL, domain TEXT NOT NULL,
              owner TEXT NOT NULL, thesis TEXT NOT NULL, stage TEXT NOT NULL,
              status TEXT NOT NULL, created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tasks(
              task_id TEXT PRIMARY KEY, programme_id TEXT,
              title TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL,
              owner TEXT NOT NULL, acceptance TEXT NOT NULL, created_at REAL NOT NULL,
              updated_at REAL NOT NULL,
              FOREIGN KEY(programme_id) REFERENCES programmes(programme_id)
            );
            CREATE TABLE IF NOT EXISTS experiments(
              experiment_id TEXT PRIMARY KEY, programme_id TEXT,
              hypothesis TEXT NOT NULL, protocol TEXT NOT NULL, status TEXT NOT NULL,
              outcome TEXT, evidence_id TEXT, created_at REAL NOT NULL,
              updated_at REAL NOT NULL,
              FOREIGN KEY(programme_id) REFERENCES programmes(programme_id)
            );
            CREATE TABLE IF NOT EXISTS evidence(
              evidence_id TEXT PRIMARY KEY, claim TEXT NOT NULL, source TEXT NOT NULL,
              source_date TEXT, classification TEXT NOT NULL, confidence TEXT NOT NULL,
              notes TEXT NOT NULL, created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approvals(
              approval_id TEXT PRIMARY KEY, action TEXT NOT NULL, details TEXT NOT NULL,
              requested_by TEXT NOT NULL, status TEXT NOT NULL, approved_by TEXT,
              decision_reason TEXT, created_at REAL NOT NULL, decided_at REAL
            );
            CREATE TABLE IF NOT EXISTS audit_events(
              seq INTEGER PRIMARY KEY AUTOINCREMENT, event_json TEXT NOT NULL
            );
            """)

    def log(self, c, kind: str, object_id: str, actor: str, payload: dict[str, Any]):
        row = c.execute("SELECT event_json FROM audit_events ORDER BY seq DESC LIMIT 1").fetchone()
        prev = json.loads(row["event_json"])["event_hash"] if row else GENESIS
        event = make_event(kind, object_id, actor, payload, prev)
        c.execute("INSERT INTO audit_events(event_json) VALUES(?)",
                  (json.dumps(event, sort_keys=True, separators=(",", ":")),))

    def add_programme(self, programme_id, name, domain, owner, thesis, actor="founder"):
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            c.execute("INSERT INTO programmes VALUES(?,?,?,?,?,?,?,?)",
                      (programme_id, name, domain, owner, thesis, "discovery", "active", now))
            self.log(c, "programme.created", programme_id, actor, {"name": name, "domain": domain})
            c.commit()
        return programme_id

    def add_task(self, task_id, programme_id, title, priority, owner, acceptance, actor="founder"):
        if priority not in {"P0", "P1", "P2", "P3"}:
            raise ValueError("Invalid priority")
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            if programme_id:
                exists = c.execute("SELECT 1 FROM programmes WHERE programme_id=?", (programme_id,)).fetchone()
                if not exists:
                    raise ValueError("Programme does not exist")
            c.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?)",
                      (task_id, programme_id, title, priority, "not_started", owner, acceptance, now, now))
            self.log(c, "task.created", task_id, actor, {"title": title, "priority": priority, "owner": owner})
            c.commit()
        return task_id

    def set_task_status(self, task_id, status, actor="founder"):
        from .models import TASK_STATES
        if status not in TASK_STATES:
            raise ValueError("Invalid task state")
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT status FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if not row:
                raise KeyError("Task not found")
            old = row["status"]
            now = time.time()
            c.execute("UPDATE tasks SET status=?, updated_at=? WHERE task_id=?", (status, now, task_id))
            self.log(c, "task.status_changed", task_id, actor, {"from": old, "to": status})
            c.commit()

    def add_evidence(self, evidence_id, claim, source, source_date, classification, confidence, notes, actor="researcher"):
        if classification not in {"fact", "estimate", "hypothesis", "observation", "opinion"}:
            raise ValueError("Invalid evidence classification")
        if confidence not in {"low", "medium", "high"}:
            raise ValueError("Invalid confidence")
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            c.execute("INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?)",
                      (evidence_id, claim, source, source_date, classification, confidence, notes, now))
            self.log(c, "evidence.created", evidence_id, actor,
                     {"claim": claim, "source": source, "classification": classification, "confidence": confidence})
            c.commit()
        return evidence_id

    def add_experiment(self, experiment_id, programme_id, hypothesis, protocol, actor="researcher"):
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            if programme_id:
                exists = c.execute("SELECT 1 FROM programmes WHERE programme_id=?", (programme_id,)).fetchone()
                if not exists:
                    raise ValueError("Programme does not exist")
            c.execute("INSERT INTO experiments VALUES(?,?,?,?,?,?,?,?,?)",
                      (experiment_id, programme_id, hypothesis, protocol, "designed", None, None, now, now))
            self.log(c, "experiment.created", experiment_id, actor, {"hypothesis": hypothesis})
            c.commit()
        return experiment_id

    def complete_experiment(self, experiment_id, outcome, evidence_id, actor="researcher"):
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            exp = c.execute("SELECT * FROM experiments WHERE experiment_id=?", (experiment_id,)).fetchone()
            if not exp:
                raise KeyError("Experiment not found")
            ev = c.execute("SELECT 1 FROM evidence WHERE evidence_id=?", (evidence_id,)).fetchone()
            if not ev:
                raise ValueError("Evidence record required to complete an experiment")
            c.execute("UPDATE experiments SET status='completed', outcome=?, evidence_id=?, updated_at=? WHERE experiment_id=?",
                      (outcome, evidence_id, now, experiment_id))
            self.log(c, "experiment.completed", experiment_id, actor,
                     {"outcome": outcome, "evidence_id": evidence_id})
            c.commit()

    def request_approval(self, approval_id, action, details, requested_by):
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            c.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,?,?,?)",
                      (approval_id, action, details, requested_by, "pending", None, None, now, None))
            self.log(c, "approval.requested", approval_id, requested_by, {"action": action, "details": details})
            c.commit()

    def decide_approval(self, approval_id, approved_by, reason, approve: bool):
        now = time.time()
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT status FROM approvals WHERE approval_id=?", (approval_id,)).fetchone()
            if not row:
                raise KeyError("Approval not found")
            if row["status"] != "pending":
                raise ValueError("Approval already decided")
            status = "approved" if approve else "rejected"
            c.execute("UPDATE approvals SET status=?, approved_by=?, decision_reason=?, decided_at=? WHERE approval_id=?",
                      (status, approved_by, reason, now, approval_id))
            self.log(c, "approval.decided", approval_id, approved_by, {"status": status, "reason": reason})
            c.commit()

    def rows(self, table: str):
        allowed = {"programmes", "tasks", "experiments", "evidence", "approvals"}
        if table not in allowed:
            raise ValueError("Invalid table")
        with self.connect() as c:
            return [dict(r) for r in c.execute(f"SELECT * FROM {table} ORDER BY created_at DESC").fetchall()]

    def audit_events(self):
        with self.connect() as c:
            return [json.loads(r["event_json"]) for r in c.execute("SELECT event_json FROM audit_events ORDER BY seq")]
