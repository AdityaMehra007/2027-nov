import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AgentVote:
    agent_id: str
    approve: bool
    signature: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class GatedOperation:
    op_id: str
    op_type: str
    payload: Dict[str, Any]
    created_at: float
    votes: Dict[str, AgentVote] = field(default_factory=dict)
    executed: bool = False


class AgentConsensusGovernor:
    """Byzantine-resilient Multi-Agent Consensus Governor for Gated Operations (GLOSSARY.md)."""

    def __init__(self, required_quorum: int = 3, approval_ratio: float = 0.66):
        self.required_quorum = required_quorum
        self.approval_ratio = approval_ratio
        self.pending_actions_queue: Dict[str, GatedOperation] = {}

    def propose_operation(self, op_type: str, payload: Dict[str, Any]) -> str:
        op_id = f"op_{uuid.uuid4().hex[:12]}"
        self.pending_actions_queue[op_id] = GatedOperation(
            op_id=op_id,
            op_type=op_type,
            payload=payload,
            created_at=time.time(),
        )
        return op_id

    def cast_vote(self, op_id: str, vote: AgentVote) -> None:
        if op_id not in self.pending_actions_queue:
            raise KeyError(f"Operation '{op_id}' not found in PendingActionsQueue")

        op = self.pending_actions_queue[op_id]
        op.votes[vote.agent_id] = vote

    def is_approved(self, op_id: str) -> bool:
        if op_id not in self.pending_actions_queue:
            return False

        op = self.pending_actions_queue[op_id]
        total_votes = len(op.votes)
        if total_votes < self.required_quorum:
            return False

        approvals = sum(1 for v in op.votes.values() if v.approve)
        ratio = approvals / total_votes
        return ratio >= self.approval_ratio

    def get_operation(self, op_id: str) -> GatedOperation:
        return self.pending_actions_queue[op_id]
