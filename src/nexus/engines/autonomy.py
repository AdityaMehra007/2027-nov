"""
ATLAS NEXUS: Mission 08 - Autonomous Workflows & Human-in-the-Loop Governance
State machine orchestration, approval gates, and fault resilience.
"""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class WorkflowStep:
    name: str
    requires_approval: bool = False
    is_approved: bool = False
    is_completed: bool = False


@dataclass
class AutonomousWorkflow:
    workflow_id: str
    name: str
    steps: List[WorkflowStep]
    current_step_idx: int = 0
    status: WorkflowStatus = WorkflowStatus.PENDING
    approver: Optional[str] = None


class AutonomousWorkflowEngine:
    def __init__(self) -> None:
        self._workflows: Dict[str, AutonomousWorkflow] = {}

    def create_workflow(self, name: str, steps: List[WorkflowStep]) -> AutonomousWorkflow:
        wf_id = f"WF-{uuid.uuid4().hex[:8].upper()}"
        wf = AutonomousWorkflow(workflow_id=wf_id, name=name, steps=steps)
        self._workflows[wf_id] = wf
        return wf

    def get_workflow(self, workflow_id: str) -> Optional[AutonomousWorkflow]:
        return self._workflows.get(workflow_id)

    def step_forward(self, workflow_id: str) -> AutonomousWorkflow:
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise KeyError(f"Workflow {workflow_id} not found")

        if wf.current_step_idx >= len(wf.steps):
            wf.status = WorkflowStatus.COMPLETED
            return wf

        step = wf.steps[wf.current_step_idx]

        # Check human approval gate
        if step.requires_approval and not step.is_approved:
            wf.status = WorkflowStatus.PENDING_APPROVAL
            return wf

        # Execute step
        step.is_completed = True
        wf.current_step_idx += 1

        if wf.current_step_idx >= len(wf.steps):
            wf.status = WorkflowStatus.COMPLETED
        else:
            wf.status = WorkflowStatus.RUNNING

        return wf

    def approve_step(self, workflow_id: str, approver_email: str) -> AutonomousWorkflow:
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise KeyError(f"Workflow {workflow_id} not found")

        if wf.current_step_idx < len(wf.steps):
            step = wf.steps[wf.current_step_idx]
            step.is_approved = True
            wf.approver = approver_email
            wf.status = WorkflowStatus.RUNNING

        return wf
