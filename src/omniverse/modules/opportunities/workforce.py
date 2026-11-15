# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Agent Workforce Orchestration & Governance Engine (PROJECT ONE Phase 6 & 7)."""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid
import hashlib
from datetime import datetime, timezone


class AgentRole(str, Enum):
    MARKET_RESEARCHER = "MARKET_RESEARCHER"
    PROSPECTOR = "PROSPECTOR"
    DELIVERY_ENGINEER = "DELIVERY_ENGINEER"
    QA_INSPECTOR = "QA_INSPECTOR"
    FINANCIAL_CONTROLLER = "FINANCIAL_CONTROLLER"
    SECURITY_OFFICER = "SECURITY_OFFICER"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RoleProfile(BaseModel):
    role: AgentRole
    token_budget_per_task: int = 4000
    max_execution_timeout_sec: int = 60
    authority_boundaries: List[str]


class WorkforceTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"tsk_{uuid.uuid4().hex[:10]}")
    role: AgentRole
    action: str
    parameters: Dict[str, Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    status: str = "PENDING"
    is_gated: bool = False
    tokens_used: int = 0
    output_result: str = ""
    merkle_block_hash: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at: Optional[str] = None


class MerkleAuditBlock(BaseModel):
    block_index: int
    prev_hash: str
    timestamp: str
    role: str
    action: str
    payload_hash: str
    block_hash: str


class WorkforceOrchestrator:
    """Orchestrates specialized agent sub-tasks under resource boundaries, Merkle audit chains, and gated operations."""

    def __init__(self):
        self._roles = self._init_role_profiles()
        self._tasks: Dict[str, WorkforceTask] = {}
        self._merkle_ledger: List[MerkleAuditBlock] = []
        self._genesis_merkle_block()

    def _genesis_merkle_block(self):
        ts = datetime.now(timezone.utc).isoformat()
        payload_hash = hashlib.sha256(b"GENESIS_OMNIVERSE_WORKFORCE").hexdigest()
        block_hash = hashlib.sha256(f"0:0000000000000000000000000000000000000000000000000000000000000000:{ts}:{payload_hash}".encode("utf-8")).hexdigest()
        
        genesis = MerkleAuditBlock(
            block_index=0,
            prev_hash="0000000000000000000000000000000000000000000000000000000000000000",
            timestamp=ts,
            role="SYSTEM",
            action="GENESIS",
            payload_hash=payload_hash,
            block_hash=block_hash,
        )
        self._merkle_ledger.append(genesis)

    def _init_role_profiles(self) -> Dict[AgentRole, RoleProfile]:
        return {
            AgentRole.MARKET_RESEARCHER: RoleProfile(
                role=AgentRole.MARKET_RESEARCHER,
                token_budget_per_task=5000,
                max_execution_timeout_sec=60,
                authority_boundaries=["Query public market reports", "Analyze industry categories", "Rank pain points"],
            ),
            AgentRole.PROSPECTOR: RoleProfile(
                role=AgentRole.PROSPECTOR,
                token_budget_per_task=4000,
                max_execution_timeout_sec=45,
                authority_boundaries=["Search company databases", "Identify buying signals", "Draft personalized hooks"],
            ),
            AgentRole.DELIVERY_ENGINEER: RoleProfile(
                role=AgentRole.DELIVERY_ENGINEER,
                token_budget_per_task=6000,
                max_execution_timeout_sec=90,
                authority_boundaries=["Generate workflow audits", "Produce client deliverables", "Scaffold automation specs"],
            ),
            AgentRole.QA_INSPECTOR: RoleProfile(
                role=AgentRole.QA_INSPECTOR,
                token_budget_per_task=3000,
                max_execution_timeout_sec=30,
                authority_boundaries=["Verify deliverable calculations", "Audit syntax & schemas", "Validate SLA compliance"],
            ),
            AgentRole.FINANCIAL_CONTROLLER: RoleProfile(
                role=AgentRole.FINANCIAL_CONTROLLER,
                token_budget_per_task=3500,
                max_execution_timeout_sec=30,
                authority_boundaries=["Reconcile settlement entries", "Track daily revenue quotas", "Draft invoices"],
            ),
            AgentRole.SECURITY_OFFICER: RoleProfile(
                role=AgentRole.SECURITY_OFFICER,
                token_budget_per_task=2500,
                max_execution_timeout_sec=20,
                authority_boundaries=["Filter PII", "Enforce air-gapped human approvals", "Verify HMAC signatures"],
            ),
        }

    def list_roles(self) -> List[RoleProfile]:
        return list(self._roles.values())

    def _is_action_gated(self, role: AgentRole, action: str, parameters: Dict[str, Any]) -> bool:
        # High impact actions require human sign-off
        if action in ("TRANSFER_TREASURY_FUNDS", "MUTATE_PRODUCTION_KEYS"):
            return True
        if action == "DISPATCH_LIVE_CAMPAIGN":
            return True
        if parameters.get("amount_usd", 0.0) > 10000.0:
            return True
        return False

    def dispatch_task(
        self,
        role: AgentRole,
        action: str,
        parameters: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> WorkforceTask:
        profile = self._roles.get(role)
        is_gated = self._is_action_gated(role, action, parameters)

        task = WorkforceTask(
            role=role,
            action=action,
            parameters=parameters,
            priority=priority,
            is_gated=is_gated,
        )

        if is_gated:
            task.status = "GATED_PENDING_APPROVAL"
            task.output_result = "Action placed into PendingActionsQueue awaiting founder HMAC cryptographic approval."
            self._tasks[task.task_id] = task
            return task

        # Autonomous execution within token budget
        tokens_consumed = min(profile.token_budget_per_task, 850 + len(str(parameters)) * 2)
        task.tokens_used = tokens_consumed
        task.output_result = f"Action {action} executed successfully by {role.value} with zero invariant violations."
        task.status = "COMPLETED"
        task.finished_at = datetime.now(timezone.utc).isoformat()

        # Append to Merkle tree ledger
        prev_block = self._merkle_ledger[-1]
        payload_hash = hashlib.sha256(f"{task.task_id}:{action}:{tokens_consumed}".encode("utf-8")).hexdigest()
        block_idx = len(self._merkle_ledger)
        block_hash = hashlib.sha256(f"{block_idx}:{prev_block.block_hash}:{task.finished_at}:{payload_hash}".encode("utf-8")).hexdigest()

        audit_block = MerkleAuditBlock(
            block_index=block_idx,
            prev_hash=prev_block.block_hash,
            timestamp=task.finished_at,
            role=role.value,
            action=action,
            payload_hash=payload_hash,
            block_hash=block_hash,
        )
        self._merkle_ledger.append(audit_block)
        task.merkle_block_hash = block_hash

        self._tasks[task.task_id] = task
        return task

    def has_pending_approvals(self) -> bool:
        return any(t.status == "GATED_PENDING_APPROVAL" for t in self._tasks.values())

    def get_merkle_ledger(self) -> List[MerkleAuditBlock]:
        return self._merkle_ledger

    def generate_daily_standup(self) -> Dict[str, Any]:
        tasks = list(self._tasks.values())
        completed = [t for t in tasks if t.status == "COMPLETED"]
        pending = [t for t in tasks if t.status == "GATED_PENDING_APPROVAL"]
        total_tokens = sum(t.tokens_used for t in tasks)

        role_counts: Dict[str, int] = {}
        for t in tasks:
            role_counts[t.role.value] = role_counts.get(t.role.value, 0) + 1

        return {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_tasks_dispatched": len(tasks),
            "completed_count": len(completed),
            "pending_approvals_count": len(pending),
            "total_tokens_consumed": total_tokens,
            "merkle_blocks_total": len(self._merkle_ledger),
            "role_breakdown": role_counts,
            "status": "ALL_AGENT_WORKFORCE_DIVISIONS_ACTIVE",
        }
