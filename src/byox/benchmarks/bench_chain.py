"""PyChain Proof-of-Work Mining & Merkle Ledger Benchmark."""

from __future__ import annotations
import time
from typing import List
from pychain.blockchain import Blockchain
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pychain(num_txs: int = 50, difficulty: int = 1) -> List[BenchmarkResult]:
    bc = Blockchain(difficulty=difficulty)
    results: List[BenchmarkResult] = []

    # Initial block to seed miner funds
    bc.mine_pending_transactions(miner_address="treasury")

    # 1. Transaction Generation & Validation
    tx_latencies: List[float] = []
    t0_tx = time.perf_counter()

    for i in range(num_txs):
        t0 = time.perf_counter()
        bc.add_transaction(sender="treasury", recipient=f"user_{i}", amount=0.1, fee=0.001)
        tx_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_tx_time = time.perf_counter() - t0_tx
    results.append(
        BenchmarkResult.from_latencies(
            name="PyChain Transaction Ingestion",
            latencies_ms=tx_latencies,
            duration_sec=total_tx_time,
            metadata={"tx_count": num_txs},
        )
    )

    # 2. Block Mining & Proof-of-Work
    mine_latencies: List[float] = []
    t0_mine = time.perf_counter()

    for _ in range(2):
        t0 = time.perf_counter()
        bc.mine_pending_transactions(miner_address="treasury")
        mine_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_mine_time = time.perf_counter() - t0_mine
    results.append(
        BenchmarkResult.from_latencies(
            name=f"PyChain Block Mining (Diff={difficulty})",
            latencies_ms=mine_latencies,
            duration_sec=total_mine_time,
            metadata={"blocks_mined": 2, "difficulty": difficulty},
        )
    )

    # 3. Chain Integrity Verification
    t0_val = time.perf_counter()
    assert bc.is_valid_chain() is True
    val_time = (time.perf_counter() - t0_val) * 1000.0
    results.append(
        BenchmarkResult.from_latencies(
            name="PyChain Full Chain Verification",
            latencies_ms=[val_time],
            duration_sec=val_time / 1000.0,
            metadata={"chain_length": len(bc.chain)},
        )
    )

    return results
