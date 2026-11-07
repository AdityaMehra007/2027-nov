"""
Apex Core: The 8 Crown Jewels of Systems Engineering in Pure Python.
"""

from .kernel import (
    ApexVirtualMachine,
    BloomFilter,
    ApexLSMDatabase,
    ConsistentHashRing,
    VectorClock,
    MerkleTreeProver,
    AutogradValue,
    LimitOrderBookEngine,
    HybridGraphPageRankEngine,
    ResilientCircuitBreaker
)

__version__ = "1.0.0"
__all__ = [
    "ApexVirtualMachine",
    "BloomFilter",
    "ApexLSMDatabase",
    "ConsistentHashRing",
    "VectorClock",
    "MerkleTreeProver",
    "AutogradValue",
    "LimitOrderBookEngine",
    "HybridGraphPageRankEngine",
    "ResilientCircuitBreaker"
]
