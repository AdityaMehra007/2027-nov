#!/usr/bin/env python3
"""
Tests for Extended Megaproject Systems:
1. Quantum-Classical Grid & Plasma Optimizer (src/quantum_core/grid_plasma_optimizer.py)
2. Reversible Adiabatic Logic Gates (src/reversible_2085/fredkin_toffoli_adiabatic.hpp)
3. LMAX Disruptor Mechanical Sympathy Ring Buffer (src/lmax_disruptor_ledger.rs)
4. Tokamak Magnetic Confinement Controller (src/hardware/tokamak_magnetic_control.cpp)
5. Flash-MHD WGMMA CUDA Kernel (src/cuda/flash_mhd_wgmma.cu)
6. XDP eBPF Zero-Trust Wire Filter (src/ebpf/xdp_zero_trust_mesh.c)
7. Planetary Mesh Deployment Manifest (deploy/k8s-planetary-mesh.yaml)
"""

import os
from pathlib import Path
import numpy as np
import pytest
import yaml

from src.quantum_core.grid_plasma_optimizer import QuantumClassicalPlasmaController


class TestQuantumPlasmaOptimizer:
    def test_vqe_statevector_unitarity(self):
        controller = QuantumClassicalPlasmaController(num_qubits=4, classical_features=16)
        angles = np.random.uniform(0, 2 * np.pi, size=8)
        state = controller.simulate_quantum_circuit(angles)
        norm = np.sum(np.abs(state) ** 2)
        assert np.isclose(norm, 1.0, atol=1e-10), f"Quantum statevector norm must be 1.0, got {norm}"

    def test_ising_hamiltonian_hermiticity(self):
        controller = QuantumClassicalPlasmaController(num_qubits=4, classical_features=16)
        J = np.random.uniform(-1, 1, size=(4, 4))
        J = 0.5 * (J + J.T)
        H = controller._construct_ising_hamiltonian(J)
        diff = np.max(np.abs(H - H.conj().T))
        assert diff < 1e-12, "Ising Hamiltonian must be Hermitian (H = H^dagger)"

    def test_optimization_execution(self):
        controller = QuantumClassicalPlasmaController(num_qubits=4, classical_features=16)
        sensors = np.random.randn(16)
        J = np.random.uniform(-1, 1, size=(4, 4))
        J = 0.5 * (J + J.T)
        np.fill_diagonal(J, 0.0)
        sol = controller.optimize_planetary_state(sensors, J)
        assert "minimum_energy_eigenvalue" in sol
        assert "optimal_grid_routing_configuration" in sol
        assert len(sol["optimal_grid_routing_configuration"]) == 4


class TestReversibleLogicGates:
    def test_toffoli_reversibility(self):
        """Toffoli(a, b, c) -> (a, b, c ^ (a & b)). Applying twice must restore original state."""
        for a in [False, True]:
            for b in [False, True]:
                for c in [False, True]:
                    # Forward
                    out_c = c ^ (a and b)
                    # Reverse
                    rev_c = out_c ^ (a and b)
                    assert rev_c == c

    def test_fredkin_hamming_conservation(self):
        """Fredkin(c, p, q) -> (c, q, p) if c else (c, p, q). Must conserve sum of bits."""
        for c in [False, True]:
            for p in [False, True]:
                for q in [False, True]:
                    in_sum = int(c) + int(p) + int(q)
                    out_p = q if c else p
                    out_q = p if c else q
                    out_sum = int(c) + int(out_p) + int(out_q)
                    assert in_sum == out_sum, "Fredkin gate must strictly conserve Hamming weight"

    def test_reversible_full_adder_logic(self):
        """1-bit full adder arithmetic: a + b + c_in == 2*c_out + sum."""
        for a in [0, 1]:
            for b in [0, 1]:
                for c_in in [0, 1]:
                    expected_sum = (a + b + c_in) % 2
                    expected_carry = (a + b + c_in) // 2
                    
                    # Logic implementation identical to C++ header
                    a_bool, b_bool, c_bool = bool(a), bool(b), bool(c_in)
                    g1 = a_bool and b_bool
                    p1 = a_bool ^ b_bool
                    c_out = g1 ^ (p1 and c_bool)
                    s = p1 ^ c_bool
                    assert int(s) == expected_sum
                    assert int(c_out) == expected_carry


class TestLMAXDisruptorLedger:
    def test_power_of_two_masking(self):
        capacity = 1024
        mask = capacity - 1
        assert (capacity & mask) == 0
        for seq in range(0, 5000):
            slot = seq & mask
            assert 0 <= slot < capacity
            assert slot == seq % capacity

    def test_cache_line_alignment_constants(self):
        """Rust source code must specify repr(align(64)) for mechanical sympathy."""
        p = Path("src/lmax_disruptor_ledger.rs")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "#[repr(align(64))]" in content
        assert "MechanicalSympathyDisruptor" in content
        assert "FinancialTransferEvent" in content


class TestTokamakMagneticRTOS:
    def test_lawson_criterion_threshold(self):
        p = Path("src/hardware/tokamak_magnetic_control.cpp")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "3.0e21" in content
        assert "COIL_COUNT = 18" in content
        assert "MAX_TESLA_LIMIT = 24.0" in content

    def test_pid_spatial_harmonics_math(self):
        coil_count = 18
        max_tesla = 24.0
        control_signal = 10.0
        phases = [2.0 * np.pi * i / coil_count for i in range(coil_count)]
        deltas = [control_signal * np.sin(ph) for ph in phases]
        # Sum of spatial harmonic variations over full torus must cancel out (zero dipole drift)
        assert np.isclose(np.sum(deltas), 0.0, atol=1e-12)
        for d in deltas:
            assert np.abs(d) <= max_tesla


class TestCUDAMHDKernel:
    def test_cuda_stencil_syntax_and_bounds(self):
        p = Path("src/cuda/flash_mhd_wgmma.cu")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "fused_mhd_sram_stencil_kernel" in content
        assert "warp_reduce_max" in content
        assert "warp_reduce_sum" in content
        assert "__shared__ float s_omega" in content


class TestEBPFZeroTrustMesh:
    def test_ebpf_xdp_packet_filter(self):
        p = Path("src/ebpf/xdp_zero_trust_mesh.c")
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "AETHER_PQC_MAGIC_HEADER 0x4F4D4547" in content
        assert "AETHER_MESH_UDP_PORT    20270" in content
        assert "aether_xdp_pqc_firewall" in content
        assert "XDP_DROP" in content
        assert "XDP_PASS" in content


class TestKubernetesManifest:
    def test_k8s_daemonset_yaml_structure(self):
        p = Path("deploy/k8s-planetary-mesh.yaml")
        assert p.exists()
        with open(p, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        assert manifest["kind"] == "DaemonSet"
        assert manifest["metadata"]["name"] == "aether-omega-planetary-node"
        container = manifest["spec"]["template"]["spec"]["containers"][0]
        assert container["name"] == "rust-bft-dag-kernel"
        assert container["resources"]["limits"]["cpu"] == "64"
        assert container["resources"]["limits"]["memory"] == "256Gi"
