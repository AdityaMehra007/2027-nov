import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import List
from .transaction import Transaction

def calculate_merkle_root(transactions: List[Transaction]) -> str:
    """Computes the SHA-256 Merkle root of a list of transactions."""
    if not transactions:
        return hashlib.sha256(b"").hexdigest()

    hashes = [tx.calculate_tx_id() for tx in transactions]

    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            h = hashlib.sha256(combined.encode("utf-8")).hexdigest()
            next_level.append(h)
        hashes = next_level

    return hashes[0]

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    difficulty: int = 1
    nonce: int = 0
    merkle_root: str = ""
    hash: str = ""

    def __post_init__(self):
        if not self.merkle_root:
            self.merkle_root = calculate_merkle_root(self.transactions)
        if not self.hash:
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculates the block header hash."""
        # Ensure merkle root matches current transactions
        m_root = calculate_merkle_root(self.transactions)
        payload = f"{self.index}:{self.timestamp}:{m_root}:{self.previous_hash}:{self.nonce}:{self.difficulty}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def mine(self) -> str:
        """Performs Proof-of-Work to find a hash matching the target difficulty."""
        target = "0" * self.difficulty
        self.merkle_root = calculate_merkle_root(self.transactions)
        while True:
            h = self.calculate_hash()
            if h.startswith(target):
                self.hash = h
                return h
            self.nonce += 1
