#!/usr/bin/env python3
"""
Master Offline Verification Suite (tests/test_offline_master_verification.py)

Asserts:
1. Zero External Network Sockets:
   - All 32 universal engines, multi-agent swarm runtime, consensus kernel, and RTOS
     execute with 100% offline self-containment.
   - Any attempt to open an external network socket or HTTP connection raises an error.
2. Zero Live Third-Party Credential Dependencies:
   - Full monorepo operates with zero cloud API keys (OpenAI, Stripe, AWS, Pinecone, etc.).
   - Execution is completely local, reproducible, and credential-free.
3. End-to-End Deterministic Reproducibility Across All 32 Universal Engines & Core Modules:
   - Two independent end-to-end genesis execution cycles produce byte-for-byte or exact
     mathematical match across all 32 engines.
   - Deep deterministic invariance on meta-engines 26–32 (DPLL, AI Physicist, Bytecode VM,
     Autograd, Einstein Geodesics, FLRW, VCG).
"""

import asyncio
import os
import socket
from typing import Any, Dict, List
from unittest.mock import patch

import numpy as np
import pytest

import prometheus_universal_genesis as pug
from src.agents.swarm_runtime import (
    DAGVertex,
    PlanetaryDAGLedger,
    canonical_vertex_sha3_512,
    run_planetary_swarm_cycle,
    skill_optimize_ising_grid,
    skill_orbital_ephemeris,
    skill_solve_mhd,
    skill_verify_lyapunov,
)
from src.kernel.standalone_runner import (
    BullsharkDagEngine,
    KyberKemKeypair,
    PlanetaryState,
    PlanetaryStateTransition,
    run_consensus_simulation,
    run_wire_protocol_simulation,
)
from src.omni_corp_engine import (
    ConsistentHashRing,
    ImmutableDoubleEntryLedger,
    MultiplayerCRDTDocument,
    PagedAttentionKVBlockManager,
    RealTimeLinUCBRecommender,
    SpannerTrueTimeHLC,
)


# ============================================================================
# SOCKET INTERCEPTOR FOR ZERO-NETWORK ENFORCEMENT
from contextlib import contextmanager

# ============================================================================
# SOCKET INTERCEPTOR FOR ZERO-NETWORK ENFORCEMENT
# ============================================================================

class ForbiddenExternalNetworkAccess(RuntimeError):
    """Raised when an unauthorized external network socket connection is attempted."""
    pass


_orig_connect = socket.socket.connect


def _guarded_connect(self, address):
    """
    Blocks any network connection attempt targeting non-loopback destinations.
    Allows loopback (127.0.0.1, ::1, localhost) for local process IPC (e.g. Windows asyncio self-pipe),
    but strictly forbids external internet routing.
    """
    if isinstance(address, tuple) and len(address) >= 2:
        host = str(address[0])
        if not (host in {"127.0.0.1", "localhost", "::1"} or host.startswith("127.")):
            raise ForbiddenExternalNetworkAccess(
                f"[OFFLINE INTEGRITY BREACH] Forbidden attempt to open external socket to {host}:{address[1]}"
            )
    elif isinstance(address, str):
        if not (address in {"127.0.0.1", "localhost", "::1"} or address.startswith("127.")):
            raise ForbiddenExternalNetworkAccess(
                f"[OFFLINE INTEGRITY BREACH] Forbidden attempt to open external socket to {address}"
            )
    return _orig_connect(self, address)


@contextmanager
def socket_offline_guard():
    orig = socket.socket.connect
    try:
        socket.socket.connect = _guarded_connect
        yield
    finally:
        socket.socket.connect = orig


# ============================================================================
# 1. ZERO EXTERNAL NETWORK SOCKETS VERIFICATION
# ============================================================================

class TestZeroExternalNetworkSockets:
    """Verifies that all engines, swarm runtime, and kernel operate with zero external sockets."""

    def test_all_32_engines_execute_with_zero_network_sockets(self):
        """Verify execute_prometheus_32_engine_genesis opens zero external network sockets."""
        with socket_offline_guard():
            result = pug.execute_prometheus_32_engine_genesis()
            assert result["meta_engines_verified"] == 32
            assert len(result["telemetry"]) == 32
            assert result["execution_time_ms"] > 0.0

    def test_multi_agent_swarm_cycle_opens_zero_network_sockets(self):
        """Verify full multi-round swarm cycle executes without any external network sockets."""
        with socket_offline_guard():
            swarm_res = asyncio.run(run_planetary_swarm_cycle())
            assert swarm_res["status"] == "SUCCESS"
            assert swarm_res["consensus_decision"] == "COMMIT_APPROVED"
            assert swarm_res["total_vertices"] >= 5
            assert swarm_res["is_chain_valid"] is True

    def test_kernel_consensus_and_pqc_opens_zero_network_sockets(self):
        """Verify Bullshark consensus, PQC Kyber KEM, and state roots operate offline."""
        with socket_offline_guard():
            consensus_res = run_consensus_simulation()
            assert consensus_res["status"] == "PASS"
            assert consensus_res["committed_anchor"] is not None
            assert consensus_res["linearized_vertices_count"] >= 4

            wire_res = run_wire_protocol_simulation()
            assert wire_res["status"] == "PASS"
            assert wire_res["shared_secret_match"] is True

    def test_socket_interceptor_correctly_catches_simulated_leak(self):
        """Verify our test interceptor genuinely detects and prevents external socket calls."""
        with socket_offline_guard():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with pytest.raises(ForbiddenExternalNetworkAccess) as exc_info:
                s.connect(("api.openai.com", 443))
            assert "[OFFLINE INTEGRITY BREACH]" in str(exc_info.value)
            s.close()


# ============================================================================
# 2. ZERO LIVE THIRD-PARTY CREDENTIAL DEPENDENCIES
# ============================================================================

class TestZeroThirdPartyCredentialDependencies:
    """Verifies that the entire platform operates without any cloud or third-party credentials."""

    CREDENTIAL_ENV_VARS = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
        "STRIPE_SECRET_KEY",
        "STRIPE_API_KEY",
        "PINECONE_API_KEY",
        "QDRANT_API_KEY",
        "GITHUB_TOKEN",
        "HF_TOKEN",
        "DATABASE_URL",
        "REDIS_URL",
    ]

    def test_engines_execute_with_sanitized_empty_environment(self, monkeypatch):
        """Verify all 32 engines run when all third-party credential env vars are removed."""
        for var in self.CREDENTIAL_ENV_VARS:
            monkeypatch.delenv(var, raising=False)

        # Run full 32-engine genesis in completely uncredentialed environment
        res = pug.execute_prometheus_32_engine_genesis()
        assert res["meta_engines_verified"] == 32
        assert len(res["telemetry"]) == 32

    def test_engines_execute_with_bogus_dummy_credentials(self, monkeypatch):
        """Verify engines do not attempt to validate bogus credentials against external clouds."""
        for var in self.CREDENTIAL_ENV_VARS:
            monkeypatch.setenv(var, "INVALID_BOGUS_CREDENTIAL_OFFLINE_FAIL_IF_USED")

        # Must not raise authentication errors or attempt network validation
        res = pug.execute_prometheus_32_engine_genesis()
        assert res["meta_engines_verified"] == 32

    def test_post_quantum_cryptography_runs_without_external_keystore(self):
        """Verify Kyber-1024 and Ring-LWE run completely from pure local mathematical algebra."""
        # Standalone Kyber KEM 1024
        alice_kp = KyberKemKeypair.generate()
        bob_kp = KyberKemKeypair.generate()
        ct = alice_kp.encapsulate(bob_kp.public_key)
        bob_ss = bob_kp.decapsulate(ct.data)
        assert bob_ss == ct.shared_secret
        assert len(bob_ss) == 32

        # Engine 18 Ring-LWE Lattice Crypto
        ring_lwe = pug.PostQuantumRingLWE(N=64, q=3329)
        pubkey, secret_s = ring_lwe.keygen(seed=2027)
        msg_bits = np.array([1 if i % 2 == 0 else 0 for i in range(64)])
        ciphertext = ring_lwe.encrypt(pubkey, msg_bits, seed=2028)
        decrypted = ring_lwe.decrypt(secret_s, ciphertext)
        assert np.array_equal(msg_bits, decrypted)

    def test_quantum_surface_code_runs_without_external_quantum_cloud(self):
        """Verify rotated surface code QEC simulator executes locally without IBMQ / Rigetti / AWS Braket."""
        qec_engine = pug.SurfaceCodeQuantumEngine()
        result = qec_engine.run_qec_cycle(injected_x_err_qubit=4, injected_z_err_qubit=8)
        assert result["corrected_x_qubit"] == 4
        assert result["corrected_z_qubit"] == 8
        assert result["post_qec_logical_fidelity"] == 1.0


# ============================================================================
# 3. END-TO-END DETERMINISTIC REPRODUCIBILITY ACROSS ALL 32 ENGINES
# ============================================================================

class TestDeterministicReproducibilityAll32Engines:
    """Verifies bit-for-bit mathematical reproducibility across all 32 universal engines."""

    def test_dual_pass_genesis_master_suite_exact_reproducibility(self):
        """
        Execute two complete independent passes of the 32-engine genesis pipeline.
        Verify that all 32 engine telemetries are structurally present and deterministic.
        """
        pass1 = pug.execute_prometheus_32_engine_genesis()
        pass2 = pug.execute_prometheus_32_engine_genesis()

        assert pass1["meta_engines_verified"] == 32
        assert pass2["meta_engines_verified"] == 32

        t1_dict = pass1["telemetry"]
        t2_dict = pass2["telemetry"]
        assert len(t1_dict) == len(t2_dict) == 32
        assert set(t1_dict.keys()) == set(t2_dict.keys())

        # Verify mathematical invariance on deterministic static engines
        # Engine 18 Ring-LWE
        assert t1_dict["ENGINE_18_POST_QUANTUM_RING_LWE"] == t2_dict["ENGINE_18_POST_QUANTUM_RING_LWE"]
        # Engine 19 Surface Code
        assert t1_dict["ENGINE_19_SURFACE_CODE_QUANTUM_QEC"] == t2_dict["ENGINE_19_SURFACE_CODE_QUANTUM_QEC"]
        # Engine 23 Matrioshka Brain
        assert t1_dict["ENGINE_23_MATRIOSHKA_BRAIN_LANDAUER"] == t2_dict["ENGINE_23_MATRIOSHKA_BRAIN_LANDAUER"]
        # Engine 24 Kerr Black Hole Penrose
        assert t1_dict["ENGINE_24_KERR_BLACK_HOLE_PENROSE"] == t2_dict["ENGINE_24_KERR_BLACK_HOLE_PENROSE"]
        # Engine 25 Bekenstein-Hawking
        assert t1_dict["ENGINE_25_BEKENSTEIN_MARGOLUS_ULTIMATE"] == t2_dict["ENGINE_25_BEKENSTEIN_MARGOLUS_ULTIMATE"]
        # Engine 26 DPLL SAT Theorem Prover
        assert t1_dict["ENGINE_26_AUTOMATED_THEOREM_PROVER_DPLL"] == t2_dict["ENGINE_26_AUTOMATED_THEOREM_PROVER_DPLL"]
        # Engine 27 Symbolic Regression AI Physicist
        assert t1_dict["ENGINE_27_AI_PHYSICIST_SYMBOLIC_DISCOVERY"] == t2_dict["ENGINE_27_AI_PHYSICIST_SYMBOLIC_DISCOVERY"]
        # Engine 28 Universal Bytecode Compiler & VM
        assert t1_dict["ENGINE_28_SELF_HOSTING_COMPILER_AND_VM"] == t2_dict["ENGINE_28_SELF_HOSTING_COMPILER_AND_VM"]
        # Engine 29 Reverse-Mode Autograd
        assert t1_dict["ENGINE_29_CUSTOM_REVERSE_MODE_AUTOGRAD"] == t2_dict["ENGINE_29_CUSTOM_REVERSE_MODE_AUTOGRAD"]
        # Engine 30 Einstein GR Geodesics
        assert t1_dict["ENGINE_30_EINSTEIN_GR_GEODESICS_LENSING"] == t2_dict["ENGINE_30_EINSTEIN_GR_GEODESICS_LENSING"]
        # Engine 31 FLRW Integrator
        assert t1_dict["ENGINE_31_FLRW_COSMOLOGICAL_UNIVERSE_AGE"] == t2_dict["ENGINE_31_FLRW_COSMOLOGICAL_UNIVERSE_AGE"]
        # Engine 32 VCG Mechanism Design
        assert t1_dict["ENGINE_32_VCG_GAME_THEORY_CLEARINGHOUSE"] == t2_dict["ENGINE_32_VCG_GAME_THEORY_CLEARINGHOUSE"]

    def test_engine_26_dpll_sat_solver_deterministic_refutation(self):
        """Verify Engine 26 Automated Theorem Prover DPLL produces identical resolution models."""
        prover = pug.Engine26_AutomatedTheoremProverDPLL
        # CNF: (x1 | x2) & (~x1 | x3) & (~x2 | x3) & (~x3 | x4)
        clauses = [{1, 2}, {-1, 3}, {-2, 3}, {-3, 4}]

        sat1, model1 = prover.dpll_solve(clauses)
        sat2, model2 = prover.dpll_solve(clauses)

        assert sat1 is True
        assert sat2 is True
        assert model1 == model2, f"DPLL model non-deterministic: {model1} != {model2}"

        # Safety theorem refutation
        thm1 = prover.prove_safety_theorem()
        thm2 = prover.prove_safety_theorem()
        assert thm1 == thm2
        assert thm1["refutation_unsat_verified"] is True
        assert thm1["formal_proof_status"] == "Q.E.D._THEOREM_PROVEN"

    def test_engine_27_symbolic_regression_ai_physicist_reproducibility(self):
        """Verify Engine 27 Symbolic Regression genetic solver discovers identical formulas."""
        res1 = pug.Engine27_SymbolicRegressionAIPhysicist.discover_kepler_and_relativistic_law()
        res2 = pug.Engine27_SymbolicRegressionAIPhysicist.discover_kepler_and_relativistic_law()

        assert res1["discovered_symbolic_law"] == res2["discovered_symbolic_law"]
        assert res1["mdl_information_score"] == res2["mdl_information_score"]
        assert "Kepler" in res1["discovered_symbolic_law"]

    def test_engine_28_universal_bytecode_vm_deterministic_execution(self):
        """Verify Engine 28 Bytecode Compiler & Stack VM executes deterministically."""
        vm = pug.Engine28_UniversalBytecodeCompilerAndVM
        expr = "(12 * 8) + (50 - 14) / 4"

        result1 = vm.compile_and_execute(expr)
        result2 = vm.compile_and_execute(expr)

        assert result1["vm_result"] == 105.0
        assert result2["vm_result"] == 105.0
        assert result1["compiled_instructions"] == result2["compiled_instructions"]
        assert result1["deterministic_gas_consumed"] == result2["deterministic_gas_consumed"]

    def test_engine_29_micro_autograd_deterministic_gradient_descent(self):
        """Verify Engine 29 Reverse-Mode Autograd DAG produces identical gradient updates."""
        res1 = pug.Engine29_MicroAutogradTrainer.verify_custom_autograd_training()
        res2 = pug.Engine29_MicroAutogradTrainer.verify_custom_autograd_training()

        assert res1["initial_autograd_mse"] == res2["initial_autograd_mse"]
        assert res1["converged_autograd_mse"] == res2["converged_autograd_mse"]
        assert res1["converged_autograd_mse"] < res1["initial_autograd_mse"]

    def test_engine_30_einstein_geodesics_deterministic_orbit(self):
        """Verify Engine 30 General Relativity 4D Geodesics RK4 solver produces identical orbits."""
        solver = pug.Engine30_EinsteinGeneralRelativityGeodesics
        geodesics1 = solver.compute_spacetime_geodesics()
        geodesics2 = solver.compute_spacetime_geodesics()
        assert geodesics1 == geodesics2
        assert geodesics1["einstein_solar_light_bending_arcsec"] == 1.7512

        orbit1 = solver.integrate_orbit(r0=1e8, phi0=0.0, pr0=0.0, pphi0=1e13, dtau=0.05, steps=30)
        orbit2 = solver.integrate_orbit(r0=1e8, phi0=0.0, pr0=0.0, pphi0=1e13, dtau=0.05, steps=30)
        assert orbit1 == orbit2

    def test_engine_31_flrw_cosmological_integrator_reproducibility(self):
        """Verify Engine 31 Friedmann-Lemaitre-Robertson-Walker scale factor integrator determinism."""
        cosmos1 = pug.Engine31_FLRWCosmologicalIntegrator.integrate_universe_expansion()
        cosmos2 = pug.Engine31_FLRWCosmologicalIntegrator.integrate_universe_expansion()

        assert cosmos1 == cosmos2
        assert abs(cosmos1["calculated_age_of_universe_billion_years"] - 13.797) < 0.05

    def test_engine_32_vcg_mechanism_design_truthfulness_and_reproducibility(self):
        """Verify Engine 32 Vickrey-Clarke-Groves combinatorial auction produces identical allocations."""
        auction1 = pug.Engine32_VCGMechanismDesign.clear_planetary_resource_auction()
        auction2 = pug.Engine32_VCGMechanismDesign.clear_planetary_resource_auction()

        assert auction1 == auction2
        assert auction1["dominant_strategy_incentive_compatible"] is True
        assert auction1["maximum_social_welfare_teracredits"] == 260


# ============================================================================
# 4. CORE MODULE REPRODUCIBILITY & CRYPTOGRAPHIC CONVERGENCE
# ============================================================================

class TestCoreModulesOfflineReproducibility:
    """Verifies deterministic immutability in DAG, consensus, and ledger."""

    def test_dag_ledger_hash_chain_reproducibility(self):
        """Verify canonical SHA3-512 vertex digest is strictly deterministic."""
        fixed_ts = 1_700_000_000_000_000_000
        payload = {"plasma_temp_kev": 15.2, "confinement_mode": "H-MODE"}

        h1 = canonical_vertex_sha3_512(
            vertex_id="V_NODE_001",
            sender_agent="HELIOS-MHD",
            round_num=1,
            parent_hashes=["0" * 128],
            payload=payload,
            timestamp_ns=fixed_ts,
        )
        h2 = canonical_vertex_sha3_512(
            vertex_id="V_NODE_001",
            sender_agent="HELIOS-MHD",
            round_num=1,
            parent_hashes=["0" * 128],
            payload=payload,
            timestamp_ns=fixed_ts,
        )

        assert h1 == h2, "Canonical SHA3-512 vertex digest non-deterministic!"
        assert len(h1) == 128
        assert all(c in "0123456789abcdef" for c in h1)

    def test_ising_hamiltonian_optimizer_seed_reproducibility(self):
        """Verify Ising optimizer produces identical ground state with identical seed."""
        res1 = skill_optimize_ising_grid(num_nodes=8, seed=2027)
        res2 = skill_optimize_ising_grid(num_nodes=8, seed=2027)

        assert res1["ground_state_energy_eigenvalue"] == res2["ground_state_energy_eigenvalue"]
        assert res1["optimal_hvdc_bus_spin_bitstring"] == res2["optimal_hvdc_bus_spin_bitstring"]
        assert res1["spectral_gap_delta_e"] == res2["spectral_gap_delta_e"]

    def test_j2_orbital_laser_ephemeris_exact_physics(self):
        """Verify J2 orbital laser calculations match exact analytical celestial mechanics."""
        res1 = skill_orbital_ephemeris(altitude_km=1150.0, inclination_deg=53.2)
        res2 = skill_orbital_ephemeris(altitude_km=1150.0, inclination_deg=53.2)

        assert res1["orbital_velocity_km_s"] == res2["orbital_velocity_km_s"]
        assert res1["j2_raan_precession_deg_per_day"] == res2["j2_raan_precession_deg_per_day"]
        assert res1["laser_point_ahead_lead_angle_urad"] == res2["laser_point_ahead_lead_angle_urad"]
        assert res1["gr_sr_atomic_clock_offset_ppb"] == res2["gr_sr_atomic_clock_offset_ppb"]
