import pytest
from omniverse.modules.planetary_mesh.bft_consensus import (
    ByzantineFaultTolerantEngine,
    ConsensusPhase,
    PBFTStateLog
)

def test_pbft_consensus_honest_network():
    # 7 nodes: f = (7 - 1) // 3 = 2. Quorum = 2f + 1 = 5.
    bft = ByzantineFaultTolerantEngine(total_nodes=7)
    proposal = {"action": "TRIGGER_EMERGENCY_CORRIDOR", "zone": "SECTOR-9"}

    log = bft.initiate_pbft_consensus(proposal=proposal, adversarial_nodes=0)

    assert isinstance(log, PBFTStateLog)
    assert log.phase == ConsensusPhase.COMMITTED
    assert log.is_finalized is True
    assert log.prepare_votes == 7
    assert log.commit_votes == 7
    assert log.proposal_hash.startswith("0x")

def test_pbft_consensus_with_tolerated_adversaries():
    # With 7 nodes, f=2 adversaries can be tolerated
    bft = ByzantineFaultTolerantEngine(total_nodes=7)
    proposal = {"action": "UPDATE_LIQUIDITY_LEDGER", "amount": 1000000}

    log = bft.initiate_pbft_consensus(proposal=proposal, adversarial_nodes=2)

    assert log.phase == ConsensusPhase.COMMITTED
    assert log.is_finalized is True
    assert log.prepare_votes == 5  # 7 - 2 = 5 >= quorum (5)

def test_pbft_consensus_rejects_excess_adversaries():
    # With 7 nodes, 3 adversaries exceed f=2 threshold
    bft = ByzantineFaultTolerantEngine(total_nodes=7)
    proposal = {"action": "MALICIOUS_STATE_OVERWRITE"}

    log = bft.initiate_pbft_consensus(proposal=proposal, adversarial_nodes=3)

    assert log.phase == ConsensusPhase.REJECTED
    assert log.is_finalized is False
