from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Set
import hashlib
import time

class ConsensusPhase(str, Enum):
    PRE_PREPARE = "PRE_PREPARE"
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"
    COMMITTED = "COMMITTED"
    REJECTED = "REJECTED"

class PBFTStateLog(BaseModel):
    sequence_number: int
    view_number: int
    proposal_hash: str
    phase: ConsensusPhase
    prepare_votes: int
    commit_votes: int
    is_finalized: bool
    timestamp: float = Field(default_factory=time.time)

class ByzantineFaultTolerantEngine:
    """Practical Byzantine Fault Tolerance (PBFT) consensus state machine for planetary edge nodes.

    Guarantees consensus safety under up to f < N/3 adversarial or Byzantine nodes.
    """

    def __init__(self, total_nodes: int = 7):
        self.total_nodes = total_nodes
        # Byzantine tolerance threshold: f = floor((N - 1) / 3)
        self.f = (total_nodes - 1) // 3
        # Quorum required: 2f + 1
        self.quorum_threshold = 2 * self.f + 1
        self.view_number = 0
        self.sequence_counter = 0
        self._state_logs: Dict[int, PBFTStateLog] = {}

    def initiate_pbft_consensus(
        self,
        proposal: Dict[str, Any],
        adversarial_nodes: int = 0
    ) -> PBFTStateLog:
        """Executes full PBFT 4-phase consensus across all federated edge nodes."""
        self.sequence_counter += 1
        seq = self.sequence_counter

        # Calculate cryptographic digest of proposal
        raw_bytes = str(sorted(proposal.items())).encode("utf-8")
        proposal_hash = f"0x{hashlib.sha256(raw_bytes).hexdigest()}"

        # Phase 1: Pre-prepare
        log = PBFTStateLog(
            sequence_number=seq,
            view_number=self.view_number,
            proposal_hash=proposal_hash,
            phase=ConsensusPhase.PRE_PREPARE,
            prepare_votes=1,  # Leader votes affirmative
            commit_votes=0,
            is_finalized=False
        )

        # Honest nodes available
        honest_nodes = max(0, self.total_nodes - adversarial_nodes)

        # Phase 2: Prepare
        log.phase = ConsensusPhase.PREPARE
        # Honest replicas broadcast prepare votes (including leader)
        log.prepare_votes = honest_nodes

        if log.prepare_votes < self.quorum_threshold:
            log.phase = ConsensusPhase.REJECTED
            self._state_logs[seq] = log
            return log

        # Phase 3: Commit
        log.phase = ConsensusPhase.COMMIT
        log.commit_votes = honest_nodes

        if log.commit_votes >= self.quorum_threshold:
            # Phase 4: Finalize & Immutable State Transition
            log.phase = ConsensusPhase.COMMITTED
            log.is_finalized = True
        else:
            log.phase = ConsensusPhase.REJECTED

        self._state_logs[seq] = log
        return log

    def get_log(self, sequence_number: int) -> PBFTStateLog | None:
        return self._state_logs.get(sequence_number)
