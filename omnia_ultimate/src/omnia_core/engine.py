from __future__ import annotations
import uuid
from typing import Any, Callable
from .models import ActionClass, Approval, Task, TaskStatus
from .policy import PolicyEngine, PolicyDenied
from .repository import SQLiteRepository

Handler = Callable[[dict[str, Any]], dict[str, Any]]

class WorkflowEngine:
    """Bounded local workflow engine. Built-in handlers are simulations only."""
    def __init__(self, repository: SQLiteRepository | None = None):
        self.repo = repository or SQLiteRepository()
        self.policy = PolicyEngine()
        self.handlers: dict[str, Handler] = {
            "demo.echo": self._echo,
            "demo.external_simulation": self._external_simulation,
        }

    @staticmethod
    def _echo(payload: dict[str, Any]) -> dict[str, Any]:
        return {"mode": "demo", "echo": payload, "external_side_effect": False}

    @staticmethod
    def _external_simulation(payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "mode": "simulation_only",
            "input": payload,
            "message": "No external service was contacted and no real-world action was performed.",
            "external_side_effect": False,
        }

    def create_task(self, title: str, action: str, action_class: str,
                    payload: dict[str, Any], actor: str = "local-user") -> Task:
        if not title.strip():
            raise ValueError("title is required")
        if action not in self.handlers:
            raise ValueError("action is not allowlisted")
        klass = ActionClass(action_class)
        task = Task.new(title, action, klass, payload)
        return self.repo.create_task(task, actor)

    def request_approval(self, task_id: str, requested_by: str, reason: str) -> Approval:
        task = self._require_task(task_id)
        if task.action_class != ActionClass.APPROVAL_REQUIRED.value:
            raise ValueError("This task class does not require an approval request")
        if task.status != TaskStatus.PENDING_APPROVAL.value:
            raise ValueError("Task is not pending approval")
        approval = Approval(
            approval_id=str(uuid.uuid4()), task_id=task_id, requested_by=requested_by,
            reason=reason, approved_by=None, decision_reason=None, status="pending",
            created_at=__import__("time").time(), decided_at=None
        )
        return self.repo.create_approval(approval)

    def decide_approval(self, task_id: str, approval_id: str, approved_by: str,
                        reason: str, approved: bool) -> Approval:
        task = self._require_task(task_id)
        approval = self.repo.latest_approval(task_id)
        if not approval or approval.approval_id != approval_id:
            raise ValueError("Approval does not belong to this task or is not latest")
        result = self.repo.decide_approval(approval_id, approved_by, reason, approved)
        if approved:
            self.repo.update_status(task_id, TaskStatus.APPROVED.value, approved_by)
        else:
            self.repo.update_status(task_id, TaskStatus.CANCELLED.value, approved_by,
                                    {"reason": "approval rejected"})
        return result

    def execute(self, task_id: str, actor: str = "local-user") -> Task:
        task = self._require_task(task_id)
        approval = self.repo.latest_approval(task_id)
        approved = bool(approval and approval.status == "approved" and task.status == TaskStatus.APPROVED.value)
        self.policy.enforce(task.action_class, approved=approved)
        if task.status not in (TaskStatus.READY.value, TaskStatus.APPROVED.value):
            raise ValueError(f"Task cannot execute from state {task.status}")
        self.repo.update_status(task_id, TaskStatus.RUNNING.value, actor)
        try:
            handler = self.handlers[task.action]
            result = handler(task.payload)
            return self.repo.update_status(task_id, TaskStatus.SUCCEEDED.value, actor, result)
        except Exception as exc:
            self.repo.update_status(task_id, TaskStatus.FAILED.value, actor,
                                    {"error": type(exc).__name__, "message": str(exc)})
            raise

    def cancel(self, task_id: str, actor: str = "local-user") -> Task:
        task = self._require_task(task_id)
        if task.status in (TaskStatus.SUCCEEDED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value):
            raise ValueError("Terminal task cannot be cancelled")
        return self.repo.update_status(task_id, TaskStatus.CANCELLED.value, actor)

    def _require_task(self, task_id: str) -> Task:
        task = self.repo.get_task(task_id)
        if task is None:
            raise KeyError("Task not found")
        return task
