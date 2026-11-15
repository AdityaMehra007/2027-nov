import time
from typing import List, Optional
from .transaction import Transaction
from .block import Block, calculate_merkle_root

class Blockchain:
    def __init__(self, difficulty: int = 1, mining_reward: float = 50.0):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = mining_reward
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the initial genesis block."""
        genesis_tx = Transaction(
            sender="COINBASE",
            recipient="GENESIS_POOL",
            amount=0.0,
            timestamp=0.0
        )
        genesis_block = Block(
            index=0,
            timestamp=0.0,
            transactions=[genesis_tx],
            previous_hash="0" * 64,
            difficulty=self.difficulty
        )
        genesis_block.mine()
        self.chain = [genesis_block]

    def get_balance(self, address: str) -> float:
        """Calculates the current confirmed balance of an address."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= (tx.amount + tx.fee)
        return balance

    def add_transaction(self, sender: str, recipient: str, amount: float, fee: float = 0.0) -> bool:
        """Adds a new transaction to the mempool if sender has sufficient balance."""
        if sender != "COINBASE":
            current_balance = self.get_balance(sender)
            # Also account for pending unconfirmed spends
            pending_spent = sum(
                tx.amount + tx.fee for tx in self.pending_transactions if tx.sender == sender
            )
            if current_balance < (pending_spent + amount + fee):
                return False

        tx = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            fee=fee,
            timestamp=time.time()
        )
        self.pending_transactions.append(tx)
        return True

    def mine_pending_transactions(self, miner_address: str) -> Block:
        """Packages pending transactions and a coinbase reward into a new block, mines it, and appends to chain."""
        total_fees = sum(tx.fee for tx in self.pending_transactions)
        reward_tx = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.mining_reward + total_fees,
            timestamp=time.time()
        )

        block_txs = [reward_tx] + self.pending_transactions
        prev_hash = self.chain[-1].hash

        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=block_txs,
            previous_hash=prev_hash,
            difficulty=self.difficulty
        )
        block.mine()

        self.chain.append(block)
        self.pending_transactions = []
        return block

    def is_valid_chain(self, chain: Optional[List[Block]] = None) -> bool:
        """Validates the cryptographic integrity and proof-of-work of a blockchain."""
        if chain is None:
            chain = self.chain

        if not chain:
            return False

        # Validate genesis
        genesis = chain[0]
        if genesis.index != 0 or genesis.previous_hash != "0" * 64:
            return False
        if genesis.merkle_root != calculate_merkle_root(genesis.transactions):
            return False

        for i in range(1, len(chain)):
            current = chain[i]
            prev = chain[i - 1]

            if current.previous_hash != prev.hash:
                return False

            if current.hash != current.calculate_hash():
                return False

            target = "0" * current.difficulty
            if not current.hash.startswith(target):
                return False

            if current.merkle_root != calculate_merkle_root(current.transactions):
                return False

            for tx in current.transactions:
                if tx.tx_id != tx.calculate_tx_id():
                    return False

        return True

    def resolve_conflicts(self, foreign_chains: List[List[Block]]) -> bool:
        """Consensus: adopts the longest valid chain across candidate networks."""
        longest_chain = None
        max_length = len(self.chain)

        for candidate in foreign_chains:
            if len(candidate) > max_length and self.is_valid_chain(candidate):
                max_length = len(candidate)
                longest_chain = candidate

        if longest_chain:
            self.chain = longest_chain
            return True

        return False
