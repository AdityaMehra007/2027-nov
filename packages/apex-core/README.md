# ⚡ Apex Core: The 8 Crown Jewels of Systems Engineering

A zero-dependency, pure Python implementation of the 8 fundamental primitives that power modern distributed systems, databases, quantitative trading, and deep learning.

[![PyPI Version](https://img.shields.io/pypi/v/apex-core.svg)](https://pypi.org/project/apex-core/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Tests Passing](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)]()

---

## 💎 The 8 Crown Jewels

1. **`ApexVirtualMachine`**: Bytecode Turing-complete stack-based virtual machine with opcode execution, stack manipulation, and deterministic evaluation.
2. **`ApexLSMDatabase` & `BloomFilter`**: Log-Structured Merge-tree storage engine with Write-Ahead Logging (WAL), memory-mapped MemTable, and Bloom filters for O(1) negative lookups.
3. **`LimitOrderBookEngine`**: Sub-millisecond price-time priority financial order matching engine supporting limit, market, and cancellation mechanics.
4. **`AutogradValue`**: Scalar-level reverse-mode automatic differentiation engine with computational DAG tracking for neural network backpropagation.
5. **`MerkleTreeProver`**: Cryptographic Merkle tree generator with logarithmic inclusion proof generation and verification.
6. **`ConsistentHashRing` & `VectorClock`**: Ketama-style consistent hashing ring with virtual nodes and Lamport/Vector causality clocks.
7. **`HybridGraphPageRankEngine`**: Iterative graph ranking and PageRank power iteration with dampening factor convergence.
8. **`ResilientCircuitBreaker`**: 3-state failure governor (Closed, Open, Half-Open) with exponential recovery windows.

---

## 🚀 Quick Start

```python
from apex_core import (
    ApexVirtualMachine,
    ApexLSMDatabase,
    LimitOrderBookEngine,
    AutogradValue,
    MerkleTreeProver,
    ConsistentHashRing,
    VectorClock,
    ResilientCircuitBreaker
)

# 1. Reverse-Mode Autograd
x = AutogradValue(2.0)
w = AutogradValue(-3.0)
b = AutogradValue(6.8813735870195432)
out = ((x * w) + b).tanh()
out.backward()
print(f"dx: {x.grad}")  # -1.5

# 2. Limit Order Book
ob = LimitOrderBookEngine()
ob.submit_limit_order("BUY", "ord_b1", 150.0, 10.0)
ob.submit_limit_order("SELL", "ord_s1", 150.0, 4.0)
print(f"Executed Trades: {len(ob.trades)}")  # 1

# 3. Turing Bytecode Virtual Machine
vm = ApexVirtualMachine(gas_limit=1000)
prog = [("PUSH", 5), ("PUSH", 7), ("ADD",), ("HALT",)]
res = vm.execute(prog)
print(f"Top of stack: {res['top_of_stack']}")  # 12

# 4. Cryptographic Merkle Prover
tree = MerkleTreeProver(["tx_0", "tx_1", "tx_2", "tx_3"])
proof = tree.get_proof(2)
assert MerkleTreeProver.verify_proof("tx_2", proof, tree.root)
```

## 📜 License
Apache 2.0 License.
