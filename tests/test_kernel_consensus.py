#!/usr/bin/env python3
"""
Tests for Milestone 2: Byzantine DAG Consensus & Post-Quantum Wire Protocol
Verifies:
- Native Rust compilation of src/kernel/aether_core.rs and src/kernel/planetary_node.rs
- FNV-1a Sponge-64 canonical digest determinism
- FIPS 202 SHA3-512 state checks
- Bullshark DAG asynchronous consensus engine (Genesis, Quorum, Orphan rejection, Anchor commit)
- Causal DAG topological subdag linearization and deterministic state execution
- CRYSTALS-Kyber (ML-KEM-1024) key encapsulation abstractions and shared secret recovery
- Planetary node wire protocol, telemetry packets, and Byzantine fault filtering
"""

import os
import subprocess
import pytest
from src.kernel.standalone_runner import (
    BullsharkDagEngine,
    DagVertex,
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
    verify_rust_compilation,
)

WORKSPACE_ROOT = "e:/2027 nov"


class TestRustKernelCompilation:
    def test_rustc_compiles_aether_core(self):
        """Verify that src/kernel/aether_core.rs compiles cleanly via native rustc."""
        filepath = os.path.join(WORKSPACE_ROOT, "src", "kernel", "aether_core.rs")
        assert os.path.exists(filepath), f"File missing: {filepath}"

        temp_rlib = os.path.join(WORKSPACE_ROOT, ".agents", "teamwork", "worker_m2", "libaether_core_test.rlib")
        cmd = ["rustc", "--edition=2021", "--crate-type=rlib", filepath, "-o", temp_rlib]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        try:
            assert proc.returncode == 0, f"rustc failed with stderr: {proc.stderr}"
            assert os.path.exists(temp_rlib)
        finally:
            if os.path.exists(temp_rlib):
                os.remove(temp_rlib)

    def test_rustc_compiles_planetary_node(self):
        """Verify that src/kernel/planetary_node.rs compiles cleanly via native rustc."""
        filepath = os.path.join(WORKSPACE_ROOT, "src", "kernel", "planetary_node.rs")
        assert os.path.exists(filepath), f"File missing: {filepath}"

        temp_rlib = os.path.join(WORKSPACE_ROOT, ".agents", "teamwork", "worker_m2", "libplanetary_node_test.rlib")
        cmd = ["rustc", "--edition=2021", "--crate-type=rlib", filepath, "-o", temp_rlib]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        try:
            assert proc.returncode == 0, f"rustc failed with stderr: {proc.stderr}"
            assert os.path.exists(temp_rlib)
        finally:
            if os.path.exists(temp_rlib):
                os.remove(temp_rlib)


class TestCryptographicPrimitives:
    def test_sha3_512_known_vectors(self):
        """Verify SHA3-512 against known test vectors."""
        import hashlib
        for test_bytes in [b"", b"AETHER", b"BFT_CONSENSUS_2027", b"\x00" * 72, b"\xFF" * 150]:
            expected = hashlib.sha3_512(test_bytes).digest()
            actual = sha3_512(test_bytes)
            assert actual == expected, f"Mismatch for input {test_bytes[:16]!r}"

    def test_canonical_sponge64_determinism(self):
        """Verify FNV-1a Sponge-64 produces deterministic 64-byte output sensitive to single-byte flips."""
        author = bytes([1] * 32)
        trans1 = PlanetaryStateTransition(
            epoch_round=1,
            timestamp_tai_ns=1_000_000,
            net_energy_delta_uw=100_000,
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=10,
        )
        digest1 = compute_canonical_digest(author, 1, [], trans1)
        digest2 = compute_canonical_digest(author, 1, [], trans1)
        assert len(digest1) == 64
        assert digest1 == digest2

        # Sensitivity: flip 1 bit in author
        author_alt = bytes([2] + [1] * 31)
        digest_alt = compute_canonical_digest(author_alt, 1, [], trans1)
        assert digest_alt != digest1


class TestBullsharkDagConsensus:
    def test_bullshark_genesis_round(self):
        """Round 1 genesis vertices have no parents and are accepted."""
        engine = BullsharkDagEngine(total_validators=4)
        author = bytes([1] * 32)
        trans = PlanetaryStateTransition(epoch_round=1, timestamp_tai_ns=1_000, net_energy_delta_uw=500)
        v = DagVertex.create(author, 1, [], trans)

        commit = engine.insert_vertex(v)
        assert commit is None
        assert v.vertex_digest in engine.dag_storage
        assert engine.current_round == 1

    def test_bullshark_insufficient_quorum_rejection(self):
        """Round > 1 vertices with < 2f+1 parents must be rejected."""
        engine = BullsharkDagEngine(total_validators=4)  # f=1, quorum=3
        author1 = bytes([1] * 32)
        v1 = DagVertex.create(author1, 1, [], PlanetaryStateTransition(1, 100, 10))
        engine.insert_vertex(v1)

        # Round 2 vertex with only 1 parent (< 3 required)
        author2 = bytes([2] * 32)
        v2 = DagVertex.create(author2, 2, [v1.vertex_digest], PlanetaryStateTransition(2, 200, 20))
        with pytest.raises(ValueError, match="InsufficientByzantineQuorum"):
            engine.insert_vertex(v2)

    def test_bullshark_orphan_parent_rejection(self):
        """Round > 1 vertex referencing non-existent parent hash must be rejected."""
        engine = BullsharkDagEngine(total_validators=4)
        fake_parents = [bytes([i] * 64) for i in range(1, 4)]
        v = DagVertex.create(bytes([1] * 32), 2, fake_parents, PlanetaryStateTransition(2, 200, 20))
        with pytest.raises(ValueError, match="OrphanParentVertex"):
            engine.insert_vertex(v)

    def test_bullshark_signature_tamper_rejection(self):
        """Tampered digest or signature in PostQuantumEnvelope must be rejected."""
        engine = BullsharkDagEngine(total_validators=4)
        v = DagVertex.create(bytes([1] * 32), 1, [], PlanetaryStateTransition(1, 100, 10))
        # Tamper with the blake3_state_digest in pqc_envelope
        v.pqc_envelope.blake3_state_digest = bytes([0xFF] * 64)
        with pytest.raises(ValueError, match="InvalidPostQuantumSignature"):
            engine.insert_vertex(v)

    def test_bullshark_even_round_anchor_commit_and_linearization(self):
        """
        Tests 3 rounds with N=4, f=1:
        Round 1: 3 vertices
        Round 2: 3 vertices referencing Round 1
        Round 3: 3 vertices referencing Round 2 -> triggers Round 2 anchor commit!
        """
        engine = BullsharkDagEngine(total_validators=4)

        def make_v(author_id: int, r: int, parents: list) -> DagVertex:
            return DagVertex.create(
                bytes([author_id] * 32),
                r,
                parents,
                PlanetaryStateTransition(
                    epoch_round=r,
                    timestamp_tai_ns=1_000_000 * r + author_id,
                    net_energy_delta_uw=100_000_000,
                ),
            )

        # Round 1
        r1 = [make_v(i, 1, []) for i in range(1, 4)]
        r1_digests = [v.vertex_digest for v in r1]
        for v in r1:
            assert engine.insert_vertex(v) is None

        # Round 2
        r2 = [make_v(i, 2, r1_digests) for i in range(1, 4)]
        r2_digests = [v.vertex_digest for v in r2]
        for v in r2:
            assert engine.insert_vertex(v) is None

        # Round 3
        r3 = [make_v(i, 3, r2_digests) for i in range(1, 4)]
        committed_anchor = None
        for v in r3:
            commit = engine.insert_vertex(v)
            if commit:
                committed_anchor = commit

        assert committed_anchor is not None, "Anchor should have been committed"
        assert committed_anchor == r2_digests[0], "Leader anchor is first vertex of Round 2"
        assert committed_anchor in engine.committed_anchors

        # State transitions should have executed
        state = engine.get_state()
        assert state.cumulative_energy_uw == 4 * 100_000_000  # Leader anchor + 3 causal ancestors in Round 1
        assert len(engine.linearized_history) == 4

        # Check topological order: round 1 vertices must strictly precede round 2 anchor
        rounds_in_order = [engine.dag_storage[d].round for d in engine.linearized_history]
        assert rounds_in_order == sorted(rounds_in_order)


class TestPostQuantumKyberKEM:
    def test_kyber_keypair_generation_sizes(self):
        """Verify ML-KEM-1024 public and secret key sizes."""
        kp = KyberKemKeypair.generate()
        assert len(kp.public_key) == 1568
        assert len(kp.secret_key) == 3168

    def test_kyber_encapsulate_decapsulate_shared_secret(self):
        """Verify that encapsulation against peer public key and decapsulation yield identical shared secret."""
        alice_kp = KyberKemKeypair.generate()
        bob_kp = KyberKemKeypair.generate()

        ct = alice_kp.encapsulate(bob_kp.public_key)
        assert len(ct.data) == 1568
        assert len(ct.shared_secret) == 32

        bob_ss = bob_kp.decapsulate(ct.data)
        assert bob_ss == ct.shared_secret

    def test_kyber_tampered_ciphertext_rejected(self):
        """Verify that altering even 1 bit in Kyber ciphertext causes decapsulation failure."""
        alice_kp = KyberKemKeypair.generate()
        bob_kp = KyberKemKeypair.generate()

        ct = alice_kp.encapsulate(bob_kp.public_key)
        tampered_data = bytearray(ct.data)
        tampered_data[100] ^= 0x01

        with pytest.raises(ValueError, match="InvalidKyberCiphertextOrIntegrityFailure"):
            bob_kp.decapsulate(bytes(tampered_data))


class TestPlanetaryNodeWireProtocol:
    def test_telemetry_packet_sha3_verification(self):
        """Verify TelemetryPacket SHA3-512 calculation and integrity check."""
        node_id = bytes([42] * 32)
        pkt = TelemetryPacket.create(
            node_id=node_id,
            node_type=NodeType.TokamakFusionCore,
            timestamp_tai_ns=1_700_000_000_000_000_000,
            net_energy_surplus_mw=350.5,
            compute_load_pct=78.2,
        )
        assert pkt.verify_hash()

        # Tampering with energy surplus invalidates hash
        pkt.net_energy_surplus_mw = 999.0
        assert not pkt.verify_hash()

    def test_planetary_kernel_node_byzantine_filtering(self):
        """Verify that forged/Byzantine telemetry packets are excluded from grid balance."""
        validator = PlanetaryKernelNode(bytes([10] * 32), NodeType.TerrestrialValidator)

        # Valid telemetry from Tokamak
        tokamak = PlanetaryKernelNode(bytes([20] * 32), NodeType.TokamakFusionCore)
        valid_pkt = tokamak.broadcast_telemetry(net_energy_surplus_mw=500.0, compute_load_pct=50.0)

        # Ingest valid packet
        assert validator.receive_and_process_telemetry(valid_pkt)

        # Attempt to ingest forged packet
        forged_pkt = TelemetryPacket(
            node_id=bytes([99] * 32),
            node_type=NodeType.LunarMassDriver,
            timestamp_tai_ns=1000,
            net_energy_surplus_mw=1_000_000.0,
            compute_load_pct=1.0,
            state_hash=bytes([0] * 64),
        )
        assert not validator.receive_and_process_telemetry(forged_pkt)

        # Grid balance only includes valid telemetry
        balance = validator.calculate_global_energy_grid_balance()
        assert balance == 500.0

    def test_wire_message_framing_roundtrip(self):
        """Verify WireMessage binary serialization and deserialization."""
        msg = WireMessage(
            msg_type=2,
            sender_id=bytes([1] * 32),
            recipient_id=bytes([2] * 32),
            payload=b"TRANSACTION_PROPOSAL_DATA",
            kem_ciphertext=bytes([0xAA] * 1568),
        )
        encoded = msg.encode()
        assert encoded.startswith(b"AETH")

        decoded = WireMessage.decode(encoded)
        assert decoded.magic == b"AETH"
        assert decoded.version == 1
        assert decoded.msg_type == 2
        assert decoded.sender_id == bytes([1] * 32)
        assert decoded.recipient_id == bytes([2] * 32)
        assert decoded.payload == b"TRANSACTION_PROPOSAL_DATA"
        assert decoded.kem_ciphertext == bytes([0xAA] * 1568)

    def test_wire_message_invalid_magic_rejected(self):
        """Verify corrupted magic bytes raise an error."""
        msg = WireMessage(1, bytes([0] * 32), bytes([0] * 32), b"test")
        encoded = bytearray(msg.encode())
        encoded[0:4] = b"BADM"
        with pytest.raises(ValueError, match="InvalidMagicBytes"):
            WireMessage.decode(bytes(encoded))
