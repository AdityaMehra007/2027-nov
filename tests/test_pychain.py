import pytest
import time
from src.pychain.transaction import Transaction
from src.pychain.block import Block, calculate_merkle_root
from src.pychain.blockchain import Blockchain

def test_transaction_creation_and_hashing():
    tx = Transaction(
        sender="alice",
        recipient="bob",
        amount=50.0,
        fee=1.0,
        timestamp=1000.0,
    )
    assert tx.tx_id is not None
    assert len(tx.tx_id) == 64
    assert tx.is_coinbase() is False

    coinbase = Transaction(
        sender="COINBASE",
        recipient="miner_1",
        amount=10.0,
        timestamp=1000.0
    )
    assert coinbase.is_coinbase() is True

def test_merkle_root_calculation():
    # Empty transactions
    empty_root = calculate_merkle_root([])
    assert len(empty_root) == 64

    # Single transaction
    tx1 = Transaction(sender="a", recipient="b", amount=10.0, timestamp=1.0)
    root1 = calculate_merkle_root([tx1])
    assert len(root1) == 64

    # Two transactions
    tx2 = Transaction(sender="b", recipient="c", amount=5.0, timestamp=2.0)
    root2 = calculate_merkle_root([tx1, tx2])
    assert len(root2) == 64
    assert root2 != root1

    # Three transactions (odd, duplicates last)
    tx3 = Transaction(sender="c", recipient="d", amount=2.0, timestamp=3.0)
    root3 = calculate_merkle_root([tx1, tx2, tx3])
    assert len(root3) == 64

def test_block_mining_satisfies_difficulty():
    tx = Transaction(sender="genesis", recipient="alice", amount=100.0, timestamp=1.0)
    block = Block(
        index=1,
        timestamp=1000.0,
        transactions=[tx],
        previous_hash="0" * 64,
        difficulty=2
    )
    block.mine()
    assert block.hash.startswith("00")
    assert block.merkle_root == calculate_merkle_root([tx])

def test_blockchain_initialization_and_genesis():
    bc = Blockchain(difficulty=1, mining_reward=50.0)
    assert len(bc.chain) == 1
    genesis = bc.chain[0]
    assert genesis.index == 0
    assert genesis.previous_hash == "0" * 64
    assert bc.is_valid_chain() is True

def test_add_transaction_and_mine():
    bc = Blockchain(difficulty=1, mining_reward=50.0)
    # Give alice initial funds via mining
    bc.mine_pending_transactions(miner_address="alice")
    assert bc.get_balance("alice") == 50.0
    assert len(bc.chain) == 2

    # Alice sends 20 to Bob with fee 1.0
    success = bc.add_transaction("alice", "bob", amount=20.0, fee=1.0)
    assert success is True
    assert len(bc.pending_transactions) == 1

    # Miner mines block
    bc.mine_pending_transactions(miner_address="charlie")
    assert len(bc.chain) == 3
    # Alice spent 20 + 1 fee = 21 -> remaining 29
    assert bc.get_balance("alice") == 29.0
    # Bob received 20
    assert bc.get_balance("bob") == 20.0
    # Charlie received block reward 50 + fee 1.0 = 51.0
    assert bc.get_balance("charlie") == 51.0
    assert bc.is_valid_chain() is True

def test_insufficient_funds_rejected():
    bc = Blockchain(difficulty=1, mining_reward=50.0)
    # Alice has 0 balance
    success = bc.add_transaction("alice", "bob", amount=10.0)
    assert success is False
    assert len(bc.pending_transactions) == 0

def test_tamper_detected():
    bc = Blockchain(difficulty=1, mining_reward=50.0)
    bc.mine_pending_transactions(miner_address="alice")
    bc.add_transaction("alice", "bob", amount=10.0)
    bc.mine_pending_transactions(miner_address="charlie")
    assert bc.is_valid_chain() is True

    # Tamper with transaction in block 2
    bc.chain[2].transactions[0].amount = 9999.0
    assert bc.is_valid_chain() is False

def test_consensus_longest_chain():
    node1 = Blockchain(difficulty=1, mining_reward=50.0)
    node2 = Blockchain(difficulty=1, mining_reward=50.0)

    # Node1 mines 2 blocks
    node1.mine_pending_transactions("miner1")
    node1.mine_pending_transactions("miner1")

    # Node2 mines 3 blocks
    node2.mine_pending_transactions("miner2")
    node2.mine_pending_transactions("miner2")
    node2.mine_pending_transactions("miner2")

    assert len(node1.chain) == 3
    assert len(node2.chain) == 4

    # Node1 resolves conflicts with node2
    replaced = node1.resolve_conflicts([node2.chain])
    assert replaced is True
    assert len(node1.chain) == 4
    assert node1.get_balance("miner2") == 150.0
