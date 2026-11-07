#!/usr/bin/env python3
"""
ADVERSARIAL STRESS TEST SUITE — MILESTONE 1 & MILESTONE 2
Author: Challenger 1 (EMPIRICAL CHALLENGER — critic, specialist)
Project: PROJECT AETHER-OMEGA 2027

Rigorous empirical challenge coverage:
1. RBAC Clearance Rejection & Unauthorized Message Forgery (Clearance Levels 1-10)
2. SHA3-512 DAG Immutability, Bit-Flips & Avalanche Tamper Detection
3. Parameter Injection & Numerical Stability on 4 Math Skills (MHD, Ising, J2, Lyapunov)
4. Bullshark Byzantine DAG Consensus Stress (Equivocation, Out-of-Order, Subdag Linearization, Energy Bounds)
5. CRYSTALS-Kyber ML-KEM-1024 Corrupted Ciphertext & Wire Protocol Resilience
"""

import asyncio
import hashlib
import os
import pytest
import numpy as np

from src.agents.swarm_runtime import (
    SKILL_REGISTRY,
    DAGVertex,
    PlanetaryDAGLedger,
    AutonomousAgentNode,
    canonical_vertex_sha3_512,
    skill_solve_mhd,
    skill_optimize_ising_grid,
    skill_orbital_ephemeris,
    skill_verify_lyapunov,
)
from src.kernel.standalone_runner import (
    BullsharkDagEngine,
    DagVertex as KernelDagVertex,
    KyberKemKeypair,
    NodeType,
    PlanetaryKernelNode,
    PlanetaryState,
    PlanetaryStateTransition,
    PostQuantumEnvelope,
    TelemetryPacket,
    WireMessage,
    compute_canonical_digest,
    sha3_512,
)


# ============================================================================
# 1. RBAC CLEARANCE REJECTION & UNAUTHORIZED MESSAGE FORGERY
# ============================================================================

class TestAdversarialRBACClearance:
    """Stress tests access control boundaries and unauthorized execution attempts."""

    @pytest.mark.parametrize("skill_name,required_lvl", [
        ("compute_orbital_laser_ephemeris", 7),
        ("solve_mhd_plasma_step", 8),
        ("optimize_ising_power_grid", 8),
        ("verify_lyapunov_stability", 9),
    ])
    def test_level_1_agent_rejected_from_all_high_clearance_skills(self, skill_name, required_lvl):
        """Attacker with Clearance 1 must be strictly rejected from invoking Level 7-9 skills."""
        dummy_args = {
            "compute_orbital_laser_ephemeris": {"altitude_km": 1000.0, "inclination_deg": 45.0},
            "solve_mhd_plasma_step": {"grid_size": 16, "steps": 2},
            "optimize_ising_power_grid": {"num_nodes": 4, "seed": 42},
            "verify_lyapunov_stability": {"jacobian_flat": [-1.0, 0.0, 0.0, -1.0], "dim": 2},
        }

        with pytest.raises(PermissionError) as exc_info:
            SKILL_REGISTRY.invoke(
                skill_name=skill_name,
                agent_id="ROGUE_ACTOR_LVL1",
                agent_clearance=1,
                **dummy_args[skill_name],
            )
        err_msg = str(exc_info.value)
        assert "[RBAC VIOLATION]" in err_msg
        assert f"Requires {required_lvl}" in err_msg
        assert "Clearance 1" in err_msg

    @pytest.mark.parametrize("clearance", [0, -1, -99])
    def test_zero_and_negative_clearance_rejected(self, clearance):
        """Zero or negative clearance values must never grant access."""
        with pytest.raises(PermissionError) as exc_info:
            SKILL_REGISTRY.invoke(
                skill_name="compute_orbital_laser_ephemeris",
                agent_id="SUBZERO_AGENT",
                agent_clearance=clearance,
                altitude_km=500.0,
            )
        assert "[RBAC VIOLATION]" in str(exc_info.value)

    def test_boundary_clearance_enforcement(self):
        """Exact clearance boundaries: clearance == required-1 fails, clearance == required passes."""
        # verify_lyapunov_stability requires clearance 9
        # Level 8 agent fails
        with pytest.raises(PermissionError):
            SKILL_REGISTRY.invoke(
                skill_name="verify_lyapunov_stability",
                agent_id="AGENT_LVL8",
                agent_clearance=8,
                jacobian_flat=[-2.0, 0.0, 0.0, -2.0],
                dim=2,
            )

        # Level 9 agent succeeds
        res9 = SKILL_REGISTRY.invoke(
            skill_name="verify_lyapunov_stability",
            agent_id="AGENT_LVL9",
            agent_clearance=9,
            jacobian_flat=[-2.0, 0.0, 0.0, -2.0],
            dim=2,
        )
        assert res9["executed_by"] == "AGENT_LVL9"
        assert res9["payload"]["lyapunov_certified_stable"] is True

    def test_forged_skill_name_rejected_with_security_fault(self):
        """Invoking arbitrary fabricated skill names triggers security fault."""
        with pytest.raises(KeyError) as exc_info:
            SKILL_REGISTRY.invoke(
                skill_name="kernel_privilege_escalation",
                agent_id="ROGUE_AGENT",
                agent_clearance=10,
            )
        assert "[SECURITY FAULT]" in str(exc_info.value)

    def test_autonomous_node_clearance_defense_protects_ledger(self):
        """When an agent node attempts an unauthorized skill, ledger append is aborted."""
        async def _run():
            ledger = PlanetaryDAGLedger()
            rogue_node = AutonomousAgentNode(
                agent_id="MALICIOUS_IMPOSTOR",
                role="Intruder",
                clearance=1,
                registry=SKILL_REGISTRY,
                ledger=ledger,
            )

            with pytest.raises(PermissionError):
                await rogue_node.execute_skill_and_commit(
                    round_num=1,
                    skill_name="verify_lyapunov_stability",
                    jacobian_flat=[-1.0, 0.0, 0.0, -1.0],
                    dim=2,
                )

            # Assert no vertex was committed to ledger
            assert len(ledger.vertices) == 0
            assert ledger.frontier_hashes == [PlanetaryDAGLedger.GENESIS_ROOT]

        asyncio.run(_run())


# ============================================================================
# 2. SHA3-512 DAG IMMUTABILITY & TAMPER DETECTION
# ============================================================================

class TestAdversarialDAGTamperDetection:
    """Stress tests SHA3-512 hashing, single-bit flips, and avalanche effect."""

    def test_single_bit_flip_in_payload_invalidates_vertex(self):
        """Mutating a single character in payload fails vertex.verify_hash()."""
        v = DAGVertex(
            vertex_id="VTX-TEST-001",
            sender_agent="HELIOS-MHD",
            round_num=1,
            parent_hashes=["0" * 128],
            payload={"telemetry_mw": 100.0, "status": "NOMINAL"},
        )
        assert v.verify_hash() is True

        # Mutate string value
        v.payload["status"] = "NOMINAM"  # 1 character flip
        assert v.verify_hash() is False

    def test_sender_identity_spoofing_detected(self):
        """Impersonating another agent invalidates vertex digest."""
        v = DAGVertex(
            vertex_id="VTX-TEST-002",
            sender_agent="WORKER_NORMAL",
            round_num=1,
            parent_hashes=["0" * 128],
            payload={"action": "PING"},
        )
        assert v.verify_hash() is True

        v.sender_agent = "CHRONOS-PRIME"
        assert v.verify_hash() is False

    def test_timestamp_replay_manipulation_detected(self):
        """Manipulating timestamp (backward or forward) invalidates hash."""
        v = DAGVertex(
            vertex_id="VTX-TEST-003",
            sender_agent="GAIA-NAVIER",
            round_num=1,
            parent_hashes=["0" * 128],
            payload={"pressure": 1.013},
        )
        assert v.verify_hash() is True

        v.timestamp_ns += 1000
        assert v.verify_hash() is False

    def test_parent_hash_reordering_invariance_and_corruption(self):
        """Canonical hashing sorts parents so re-ordering is deterministic, but modifying corrupts."""
        parent_a = "a" * 128
        parent_b = "b" * 128

        h1 = canonical_vertex_sha3_512("V1", "AGENT", 2, [parent_a, parent_b], {"k": 1}, 100)
        h2 = canonical_vertex_sha3_512("V1", "AGENT", 2, [parent_b, parent_a], {"k": 1}, 100)
        assert h1 == h2, "Canonical hash must sort parents to prevent ordering malleability"

        # Modifying a parent hash must change digest
        parent_c = "c" * 128
        h3 = canonical_vertex_sha3_512("V1", "AGENT", 2, [parent_a, parent_c], {"k": 1}, 100)
        assert h1 != h3

    def test_sha3_512_avalanche_effect(self):
        """Verify strict cryptographic avalanche effect (>200 bit flips on 1-bit input flip)."""
        dict1 = {"round": 1, "sender": "AGENT_A", "value": 100.0}
        dict2 = {"round": 1, "sender": "AGENT_A", "value": 100.1}

        h1 = hashlib.sha3_512(str(dict1).encode("utf-8")).digest()
        h2 = hashlib.sha3_512(str(dict2).encode("utf-8")).digest()

        # Count differing bits
        diff_bits = 0
        for b1, b2 in zip(h1, h2):
            diff_bits += bin(b1 ^ b2).count("1")

        # In a 512-bit hash, expected difference is ~256 bits (> 200 bits strictly required)
        assert diff_bits > 200, f"Avalanche insufficient: only {diff_bits} bits flipped"

    def test_ledger_detects_orphan_parent_insertion(self):
        """Ledger integrity check fails when a vertex points to a non-existent parent hash."""
        ledger = PlanetaryDAGLedger()
        v1 = ledger.append_vertex(sender="HELIOS-MHD", round_num=1, payload={"step": 1})

        # Manually create vertex with fake parent
        fake_parent = "f" * 128
        v2 = DAGVertex(
            vertex_id="VTX-ROGUE",
            sender_agent="HELIOS-MHD",
            round_num=2,
            parent_hashes=[fake_parent],
            payload={"step": 2},
        )
        ledger.vertices[v2.vertex_hash] = v2

        assert ledger.verify_integrity() is False


# ============================================================================
# 3. UNGROUNDED PARAMETERS & NUMERICAL STABILITY (4 MATH SKILLS)
# ============================================================================

class TestAdversarialMathSkillsParameters:
    """Stress tests boundary inputs, ungrounded parameters, and stability."""

    # --- Skill 1: MHD Orszag-Tang Solver ---
    def test_mhd_invalid_grid_sizes_raise_value_error(self):
        """MHD solver must reject zero and negative grid sizes."""
        with pytest.raises(ValueError):
            skill_solve_mhd(grid_size=0)
        with pytest.raises(ValueError):
            skill_solve_mhd(grid_size=-16)

    def test_mhd_negative_steps_raise_value_error(self):
        """MHD solver must reject negative step counts."""
        with pytest.raises(ValueError):
            skill_solve_mhd(steps=-5)

    def test_mhd_cfl_instability_triggers_tearing_mode_warning(self):
        """Injecting excessive dt (dt=10.0) violates CFL condition and triggers warning."""
        res = skill_solve_mhd(grid_size=16, steps=5, dt=10.0)
        assert res["plasma_regime"] == "TEARING_MODE_WARNING"

    def test_mhd_zero_steps_preserves_initial_energy(self):
        """Zero steps executes clean initialization without state corruption."""
        res = skill_solve_mhd(grid_size=16, steps=0)
        assert res["plasma_regime"] == "H-MODE_CONFINED"
        assert res["max_vorticity_rad_s"] == 4.0
        assert res["rms_magnetic_flux_weber"] > 0.0

    # --- Skill 2: Quantum Ising Optimizer ---
    def test_ising_out_of_bounds_node_count_rejected(self):
        """Ising solver rejects num_nodes <= 0 or > 24."""
        with pytest.raises(ValueError):
            skill_optimize_ising_grid(num_nodes=0)
        with pytest.raises(ValueError):
            skill_optimize_ising_grid(num_nodes=-4)
        with pytest.raises(ValueError):
            skill_optimize_ising_grid(num_nodes=25)

    def test_ising_single_node_ground_state(self):
        """Single qubit (N=1) ground state partition solves cleanly."""
        res = skill_optimize_ising_grid(num_nodes=1, seed=2027)
        assert len(res["optimal_hvdc_bus_spin_bitstring"]) == 1
        assert res["optimal_hvdc_bus_spin_bitstring"] in ("0", "1")
        assert res["spectral_gap_delta_e"] >= 0.0

    def test_ising_negative_seed_rejected(self):
        """Negative RNG seed raises ValueError."""
        with pytest.raises(ValueError):
            skill_optimize_ising_grid(num_nodes=4, seed=-1)

    def test_ising_reproducible_determinism(self):
        """Identical seed must yield exact bit-for-bit identical spin partitions."""
        r1 = skill_optimize_ising_grid(num_nodes=8, seed=42)
        r2 = skill_optimize_ising_grid(num_nodes=8, seed=42)
        assert r1["optimal_hvdc_bus_spin_bitstring"] == r2["optimal_hvdc_bus_spin_bitstring"]
        assert r1["ground_state_energy_eigenvalue"] == r2["ground_state_energy_eigenvalue"]

    # --- Skill 3: Relativistic J2 Ephemeris ---
    def test_orbital_subsurface_collision_rejected(self):
        """Negative or zero altitude must be rejected."""
        with pytest.raises(ValueError):
            skill_orbital_ephemeris(altitude_km=0.0)
        with pytest.raises(ValueError):
            skill_orbital_ephemeris(altitude_km=-100.0)

    def test_orbital_polar_and_equatorial_inclination_limits(self):
        """Polar orbit (90 deg) exhibits zero RAAN nodal precession."""
        polar = skill_orbital_ephemeris(altitude_km=1000.0, inclination_deg=90.0)
        assert abs(polar["j2_raan_precession_deg_per_day"]) < 1e-12

        # Equatorial orbit has maximal positive precession
        eq = skill_orbital_ephemeris(altitude_km=1000.0, inclination_deg=0.0)
        assert eq["j2_raan_precession_deg_per_day"] < 0.0  # Retrograde precession in degrees/day

    def test_orbital_velocity_monotonically_decreases_with_altitude(self):
        """Keplerian orbital velocity must strictly decrease as altitude increases."""
        leo = skill_orbital_ephemeris(altitude_km=300.0)
        geo = skill_orbital_ephemeris(altitude_km=35786.0)
        assert leo["orbital_velocity_km_s"] > geo["orbital_velocity_km_s"]

    # --- Skill 4: Continuous Lyapunov Stability Verifier ---
    def test_lyapunov_dimension_mismatch_raises_value_error(self):
        """Mismatched flat array length vs dim*dim raises ValueError."""
        with pytest.raises(ValueError):
            skill_verify_lyapunov(jacobian_flat=[-1.0, 0.0, 0.0], dim=2)  # 3 elements instead of 4

    def test_lyapunov_strictly_unstable_triggers_emergency_scram(self):
        """Positive real eigenvalues must trigger EMERGENCY_SCRAM_VETO."""
        # Unstable matrix: eigenvalues +2.0, +3.0
        A_unstable = [2.0, 0.0, 0.0, 3.0]
        res = skill_verify_lyapunov(jacobian_flat=A_unstable, dim=2)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert res["max_real_eigenvalue_A"] == 3.0

    def test_lyapunov_marginally_stable_triggers_scram(self):
        """Harmonic oscillator with zero real poles (pure imaginary) must be rejected."""
        # A = [[0, 1], [-1, 0]], eigenvalues = +/- i, real part = 0.0
        A_marginal = [0.0, 1.0, -1.0, 0.0]
        res = skill_verify_lyapunov(jacobian_flat=A_marginal, dim=2)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"

    def test_lyapunov_near_zero_hurwitz_boundary_triggers_scram(self):
        """System with pole at -1e-7 fails Hurwitz tolerance (-1e-6) and SCRAMs."""
        A_near_zero = [-1e-7, 0.0, 0.0, -1e-7]
        res = skill_verify_lyapunov(jacobian_flat=A_near_zero, dim=2)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"

    def test_lyapunov_strictly_stable_system_commits(self):
        """Strongly Hurwitz Jacobian solves A^T P + P A = -I with P > 0."""
        A_stable = [-5.0, 1.0, -1.0, -4.0]
        res = skill_verify_lyapunov(jacobian_flat=A_stable, dim=2)
        assert res["lyapunov_certified_stable"] is True
        assert res["safety_interlock_action"] == "COMMIT_APPROVED"
        assert res["min_eigenvalue_P"] > 0.0


# ============================================================================
# 4. BULLSHARK BYZANTINE DAG CONSENSUS STRESS TESTING
# ============================================================================

class TestAdversarialBullsharkConsensus:
    """Stress tests Byzantine consensus under equivocation, out-of-order rounds, and energy bounds."""

    def test_equivocating_vertex_handled_consistently(self):
        """
        Byzantine validator creates two distinct vertices V_2A and V_2B at Round 2.
        Engine must accept both without crashing; subdag linearization only orders the elected anchor.
        """
        engine = BullsharkDagEngine(total_validators=4)

        # Round 1
        r1_hashes = []
        for i in range(1, 4):
            v = KernelDagVertex.create(bytes([i] * 32), 1, [], PlanetaryStateTransition(1, 1000, 100))
            engine.insert_vertex(v)
            r1_hashes.append(v.vertex_digest)

        # Round 2: Node 1 creates honest vertex; Node 2 EQUIVOCATES
        v2_1 = KernelDagVertex.create(bytes([1] * 32), 2, r1_hashes, PlanetaryStateTransition(2, 2000, 100))
        v2_2A = KernelDagVertex.create(bytes([2] * 32), 2, r1_hashes, PlanetaryStateTransition(2, 2000, 200))
        v2_2B = KernelDagVertex.create(bytes([2] * 32), 2, r1_hashes, PlanetaryStateTransition(2, 2000, 999))
        v2_3 = KernelDagVertex.create(bytes([3] * 32), 2, r1_hashes, PlanetaryStateTransition(2, 2000, 300))

        engine.insert_vertex(v2_1)
        engine.insert_vertex(v2_2A)
        engine.insert_vertex(v2_2B)  # Equivocated vertex
        engine.insert_vertex(v2_3)

        assert len(engine.rounds_index[2]) == 4

        # Round 3: Honest nodes vote for Round 2 leader anchor (v2_1)
        r2_parents = [v2_1.vertex_digest, v2_2A.vertex_digest, v2_3.vertex_digest]
        v3_1 = KernelDagVertex.create(bytes([1] * 32), 3, r2_parents, PlanetaryStateTransition(3, 3000, 10))
        v3_2 = KernelDagVertex.create(bytes([2] * 32), 3, r2_parents, PlanetaryStateTransition(3, 3000, 10))

        engine.insert_vertex(v3_1)
        commit = engine.insert_vertex(v3_2)

        assert commit == v2_1.vertex_digest
        assert len(engine.committed_anchors) == 1
        # v2_2B must NOT be committed in the linearized history
        assert v2_2B.vertex_digest not in engine.committed_vertex_set

    def test_out_of_order_future_round_rejected_as_orphan(self):
        """A Round 3 vertex arriving before Round 2 vertices exist is rejected as an orphan."""
        engine = BullsharkDagEngine(total_validators=4)
        v1 = KernelDagVertex.create(bytes([1] * 32), 1, [], PlanetaryStateTransition(1, 1000, 100))
        engine.insert_vertex(v1)

        # Attempt to insert Round 3 vertex referencing unreceived Round 2 parent
        fake_r2_hash = bytes([0xAA] * 64)
        v3 = KernelDagVertex.create(bytes([1] * 32), 3, [fake_r2_hash, v1.vertex_digest, v1.vertex_digest], PlanetaryStateTransition(3, 3000, 100))

        with pytest.raises(ValueError, match="OrphanParentVertex"):
            engine.insert_vertex(v3)

    def test_insufficient_quorum_rejected(self):
        """Round 2 vertex with only 2 parents (< 2f+1 = 3 required) is rejected."""
        engine = BullsharkDagEngine(total_validators=4)
        v1 = KernelDagVertex.create(bytes([1] * 32), 1, [], PlanetaryStateTransition(1, 1000, 100))
        v2 = KernelDagVertex.create(bytes([2] * 32), 1, [], PlanetaryStateTransition(1, 1000, 100))
        engine.insert_vertex(v1)
        engine.insert_vertex(v2)

        v_weak = KernelDagVertex.create(
            bytes([1] * 32),
            2,
            [v1.vertex_digest, v2.vertex_digest],  # Only 2 parents, needs 3
            PlanetaryStateTransition(2, 2000, 50),
        )
        with pytest.raises(ValueError, match="InsufficientByzantineQuorum"):
            engine.insert_vertex(v_weak)

    def test_thermodynamic_energy_conservation_bound_exceeded(self):
        """State transition exceeding 1 Terawatt (|delta| > 10^18 uW) must abort state update."""
        state = PlanetaryState.genesis()
        # 1 TW + 1 uW
        illegal_trans = PlanetaryStateTransition(
            epoch_round=1,
            timestamp_tai_ns=1000,
            net_energy_delta_uw=1_000_000_000_000_000_001,
        )
        with pytest.raises(ValueError, match="ThermodynamicEnergyConservationViolation"):
            illegal_trans.verify_and_apply(state)

    def test_multi_round_anchor_linearization_prevents_duplicate_execution(self):
        """
        Verify that multiple consecutive anchor commits (Round 2 anchor at Round 3,
        Round 4 anchor at Round 5) linearize disjoint subdag sets without duplicating commits.
        """
        engine = BullsharkDagEngine(total_validators=4)

        def make_round(r: int, parents: list) -> list:
            hashes = []
            for node_id in range(1, 4):
                v = KernelDagVertex.create(
                    bytes([node_id] * 32),
                    r,
                    parents,
                    PlanetaryStateTransition(r, 1_000_000 * r + node_id, 10_000),
                )
                commit = engine.insert_vertex(v)
                hashes.append(v.vertex_digest)
            return hashes

        r1 = make_round(1, [])
        r2 = make_round(2, r1)
        r3 = make_round(3, r2)  # Commits Round 2 anchor
        assert len(engine.committed_anchors) == 1
        count_after_r3 = len(engine.linearized_history)
        assert count_after_r3 >= 4

        r4 = make_round(4, r3)
        r5 = make_round(5, r4)  # Commits Round 4 anchor
        assert len(engine.committed_anchors) == 2
        count_after_r5 = len(engine.linearized_history)
        assert count_after_r5 > count_after_r3

        # Verify no duplicates in linearized history
        assert len(engine.linearized_history) == len(set(engine.linearized_history))


# ============================================================================
# 5. CRYSTALS-KYBER ML-KEM-1024 CORRUPTED CIPHERTEXT & WIRE RESILIENCE
# ============================================================================

class TestAdversarialPostQuantumWire:
    """Stress tests ML-KEM-1024 under truncated, corrupted, and forged ciphertexts."""

    @pytest.fixture
    def kyber_parties(self):
        alice = KyberKemKeypair.generate()
        bob = KyberKemKeypair.generate()
        charlie = KyberKemKeypair.generate()
        ct = alice.encapsulate(bob.public_key)
        return alice, bob, charlie, ct

    def test_truncated_ciphertext_rejected(self, kyber_parties):
        """Ciphertexts shorter than 1568 bytes must raise InvalidCiphertextLength."""
        _, bob, _, ct = kyber_parties
        truncated_samples = [b"", b"A" * 16, b"B" * 32, ct.data[:100], ct.data[:1567]]
        for sample in truncated_samples:
            with pytest.raises(ValueError, match="InvalidCiphertextLength"):
                bob.decapsulate(sample)

    def test_oversized_ciphertext_rejected(self, kyber_parties):
        """Ciphertexts longer than 1568 bytes must raise InvalidCiphertextLength."""
        _, bob, _, ct = kyber_parties
        with pytest.raises(ValueError, match="InvalidCiphertextLength"):
            bob.decapsulate(ct.data + b"\x00")

    @pytest.mark.parametrize("byte_offset", [0, 15, 31, 32, 100, 500, 1000, 1567])
    def test_single_bit_flip_corruption_rejected(self, kyber_parties, byte_offset):
        """A single bit flip anywhere in the 1568-byte ciphertext must be detected."""
        _, bob, _, ct = kyber_parties
        corrupted = bytearray(ct.data)
        corrupted[byte_offset] ^= 0x01
        with pytest.raises(ValueError, match="InvalidKyberCiphertextOrIntegrityFailure"):
            bob.decapsulate(bytes(corrupted))

    def test_all_zeros_and_all_ones_rejected(self, kyber_parties):
        """Trivial bit patterns (all zeros / all ones) fail integrity verification."""
        _, bob, _, _ = kyber_parties
        with pytest.raises(ValueError, match="InvalidKyberCiphertextOrIntegrityFailure"):
            bob.decapsulate(b"\x00" * 1568)
        with pytest.raises(ValueError, match="InvalidKyberCiphertextOrIntegrityFailure"):
            bob.decapsulate(b"\xFF" * 1568)

    def test_cross_recipient_ciphertext_hijacking_rejected(self, kyber_parties):
        """Charlie attempting to decapsulate a ciphertext intended for Bob must fail."""
        _, _, charlie, ct = kyber_parties
        with pytest.raises(ValueError, match="InvalidKyberCiphertextOrIntegrityFailure"):
            charlie.decapsulate(ct.data)

    def test_wire_message_magic_bytes_corruption(self):
        """WireMessage with corrupt magic bytes is rejected."""
        msg = WireMessage(
            msg_type=1,
            sender_id=bytes([1] * 32),
            recipient_id=bytes([2] * 32),
            payload=b"HELLO",
        )
        encoded = bytearray(msg.encode())
        encoded[0:4] = b"BADM"
        with pytest.raises(ValueError, match="InvalidMagicBytes"):
            WireMessage.decode(bytes(encoded))

    def test_telemetry_packet_tamper_rejected_by_peer(self):
        """Mutated telemetry packet hash is rejected by peer kernel node."""
        alice = PlanetaryKernelNode(bytes([1] * 32), NodeType.TokamakFusionCore)
        bob = PlanetaryKernelNode(bytes([2] * 32), NodeType.OrbitalLaserStation)

        pkt = alice.broadcast_telemetry(net_energy_surplus_mw=500.0, compute_load_pct=30.0)
        assert pkt.verify_hash() is True

        # Mutate net energy without updating hash
        pkt.net_energy_surplus_mw = 999999.0
        assert pkt.verify_hash() is False

        accepted = bob.receive_and_process_telemetry(pkt)
        assert accepted is False
        assert alice.node_id not in bob.peer_ledger
