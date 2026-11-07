import os
from pathlib import Path

pkg_dir = Path("packages/apex-core")
src_dir = pkg_dir / "src" / "apex_core"
src_dir.mkdir(parents=True, exist_ok=True)

pyproject = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "apex-core"
version = "1.0.0"
description = "The 8 Crown Jewels of Systems Engineering in Pure Python: Turing VM, LSM-Tree, Limit Order Book, Autograd, Merkle Tree, Consistent Hash Ring, Vector Clocks, and Circuit Breaker."
readme = "README.md"
authors = [{ name = "Aditya Mehra", email = "adityamehra799@gmail.com" }]
license = { text = "Apache-2.0" }
requires-python = ">=3.10"
dependencies = []
keywords = ["systems-engineering", "lsm-tree", "virtual-machine", "order-book", "autograd", "merkle-tree", "distributed-systems"]

[project.urls]
Homepage = "https://github.com/AdityaMehra007/cashflow-infinity-omniverse"
Repository = "https://github.com/AdityaMehra007/cashflow-infinity-omniverse.git"
"""

readme = """# ⚡ Apex Core: The 8 Crown Jewels of Systems Engineering

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
x = AutogradValue(3.0)
y = AutogradValue(4.0)
z = x * y + x ** 2
z.backward()
print(f"dz/dx: {x.grad}")  # 4 + 2*3 = 10.0

# 2. Limit Order Book
ob = LimitOrderBookEngine()
ob.submit_limit_order("BUY", "order_1", 100.50, 10)
ob.submit_limit_order("SELL", "order_2", 100.50, 5)
print(f"Executed Trades: {len(ob.trades)}")

# 3. LSM Database with WAL
db = ApexLSMDatabase(wal_path="/tmp/apex_wal.log")
db.put("founder", "Aditya")
print(db.get("founder"))  # Aditya
```

## 📜 License
Apache 2.0 License.
"""

(pkg_dir / "pyproject.toml").write_text(pyproject, encoding="utf-8")
(pkg_dir / "README.md").write_text(readme, encoding="utf-8")

with open("apex_singularity_kernel.py", "r", encoding="utf-8") as f:
    code = f.read()

init_code = '''"""
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
'''
(src_dir / "__init__.py").write_text(init_code, encoding="utf-8")
(src_dir / "kernel.py").write_text(code, encoding="utf-8")
print("Successfully scaffolded packages/apex-core")
