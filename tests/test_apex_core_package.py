"""
Verification test for packages/apex-core distribution.
"""
import sys
from pathlib import Path
import pytest

# Add package src to path for direct verification
pkg_src = Path(__file__).parent.parent / "packages" / "apex-core" / "src"
if str(pkg_src) not in sys.path:
    sys.path.insert(0, str(pkg_src))

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

def test_apex_core_autograd():
    x = AutogradValue(2.0)
    w = AutogradValue(-3.0)
    b = AutogradValue(6.8813735870195432)
    out = ((x * w) + b).tanh()
    out.backward()
    assert abs(out.data - 0.70710678) < 1e-4
    assert abs(x.grad - (-1.5)) < 1e-4
    assert abs(w.grad - 1.0) < 1e-4

def test_apex_core_order_book():
    ob = LimitOrderBookEngine()
    ob.submit_limit_order("BUY", "ord_b1", 150.0, 10.0)
    ob.submit_limit_order("SELL", "ord_s1", 150.0, 4.0)
    assert len(ob.trades) == 1
    assert ob.trades[0]["qty"] == 4.0
    assert ob.trades[0]["price"] == 150.0

def test_apex_core_vm():
    vm = ApexVirtualMachine(gas_limit=1000)
    prog = [
        ("PUSH", 5),
        ("PUSH", 7),
        ("ADD",),
        ("HALT",)
    ]
    res = vm.execute(prog)
    assert res["top_of_stack"] == 12

def test_apex_core_merkle():
    leaves = ["tx_0", "tx_1", "tx_2", "tx_3", "tx_4"]
    tree = MerkleTreeProver(leaves)
    proof = tree.get_proof(3)
    assert MerkleTreeProver.verify_proof("tx_3", proof, tree.root) is True
    assert MerkleTreeProver.verify_proof("forged", proof, tree.root) is False
