#!/usr/bin/env python3
"""
AETHER-OMEGA (2027) — Standalone Verification Runner & Consensus Simulation Engine
Simulates Bullshark Byzantine DAG Consensus, SHA3-512 State Transitions,
and CRYSTALS-Kyber (ML-KEM-1024) Key Encapsulation in pure Python.
Verifies native Rust compilation via rustc 1.98.0 when available.
"""

from __future__ import annotations
import enum
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================================================
# Core Cryptographic & Math Primitives
# ============================================================================

def sha3_512(data: bytes) -> bytes:
    """Computes FIPS 202 bit-exact SHA3-512 digest."""
    return hashlib.sha3_512(data).digest()


def compute_canonical_digest(
    author_id: bytes,
    round_num: int,
    parents: List[bytes],
    transition: PlanetaryStateTransition,
) -> bytes:
    """
    Deterministic FNV-1a / Sponge-64 canonical hash matching src/kernel/aether_core.rs.
    """
    acc = 0xcbf29ce484222325
    fnv_prime = 0x100000001b3
    mask64 = 0xFFFFFFFFFFFFFFFF

    def mix(state: int, byte: int) -> int:
        state ^= byte
        return (state * fnv_prime) & mask64

    for b in author_id:
        acc = mix(acc, b)
    for b in round_num.to_bytes(8, "little", signed=False):
        acc = mix(acc, b)
    for parent in parents:
        for b in parent:
            acc = mix(acc, b)
    for b in transition.timestamp_tai_ns.to_bytes(16, "little", signed=False):
        acc = mix(acc, b)
    for b in transition.net_energy_delta_uw.to_bytes(16, "little", signed=True):
        acc = mix(acc, b)
    for b in transition.tokamak_quench_flags.to_bytes(4, "little", signed=False):
        acc = mix(acc, b)
    for b in transition.orbital_laser_azimuth_urad.to_bytes(8, "little", signed=True):
        acc = mix(acc, b)

    digest = bytearray(64)
    for i in range(64):
        # acc = acc.rotate_left(7) ^ (i * 0x9e3779b97f4a7c15)
        acc = (((acc << 7) | (acc >> 57)) & mask64) ^ ((i * 0x9e3779b97f4a7c15) & mask64)
        digest[i] = acc & 0xFF

    return bytes(digest)


# ============================================================================
# Post-Quantum Wire Envelope (ML-KEM-1024 / ML-DSA-87)
# ============================================================================

@dataclass
class PostQuantumEnvelope:
    sender_node_id: bytes             # 32 bytes
    kyber1024_ciphertext: bytes       # 1568 bytes
    dilithium5_signature: bytes       # 4595 bytes
    blake3_state_digest: bytes        # 64 bytes

    @classmethod
    def encapsulate(cls, peer_pk: bytes) -> Tuple[bytes, bytes]:
        """
        Derives ephemeral 1568-byte ciphertext and 32-byte shared secret
        matching Rust PostQuantumEnvelope::encapsulate.
        """
        if len(peer_pk) < 32:
            raise ValueError("peer_pk must be at least 32 bytes")
        ephemeral_entropy = bytearray(32)
        for i, b in enumerate(peer_pk[:32]):
            ephemeral_entropy[i] = (((b + i) & 0xFF) << 3 | ((b + i) & 0xFF) >> 5) & 0xFF

        kdf_input = bytes(ephemeral_entropy) + peer_pk[:32]
        full_hash = sha3_512(kdf_input)
        shared_secret = full_hash[:32]

        ciphertext = bytearray(1568)
        for i in range(32):
            ciphertext[i] = ephemeral_entropy[i] ^ peer_pk[i]
        for i in range(32, 1568):
            ciphertext[i] = full_hash[i % 64] ^ (i & 0xFF)

        return bytes(ciphertext), shared_secret


# ============================================================================
# Planetary State Transition
# ============================================================================

@dataclass
class PlanetaryStateTransition:
    epoch_round: int
    timestamp_tai_ns: int
    net_energy_delta_uw: int           # Fixed-point i128 Micro-Watts
    tokamak_quench_flags: int = 0
    orbital_laser_azimuth_urad: int = 0

    def serialize_canonical(self) -> bytes:
        return (
            self.epoch_round.to_bytes(8, "little", signed=False)
            + self.timestamp_tai_ns.to_bytes(16, "little", signed=False)
            + self.net_energy_delta_uw.to_bytes(16, "little", signed=True)
            + self.tokamak_quench_flags.to_bytes(4, "little", signed=False)
            + self.orbital_laser_azimuth_urad.to_bytes(8, "little", signed=True)
        )

    def verify_and_apply(self, state: PlanetaryState) -> bytes:
        max_delta = 1_000_000_000_000_000_000  # 1 TW bound
        if abs(self.net_energy_delta_uw) > max_delta:
            raise ValueError("ThermodynamicEnergyConservationViolation")

        state.epoch_round = self.epoch_round
        state.cumulative_energy_uw += self.net_energy_delta_uw
        state.tokamak_quench_flags = self.tokamak_quench_flags
        state.orbital_laser_azimuth_urad = self.orbital_laser_azimuth_urad

        root_input = state.state_root + self.serialize_canonical()
        state.state_root = sha3_512(root_input)
        return state.state_root


@dataclass
class PlanetaryState:
    epoch_round: int = 0
    cumulative_energy_uw: int = 0
    tokamak_quench_flags: int = 0
    orbital_laser_azimuth_urad: int = 0
    state_root: bytes = field(default_factory=lambda: sha3_512(b"AETHER_OMEGA_PLANETARY_GENESIS_ROOT_2027"))

    @classmethod
    def genesis(cls) -> PlanetaryState:
        return cls()


# ============================================================================
# Causal DAG Vertex Structure
# ============================================================================

@dataclass
class DagVertex:
    vertex_digest: bytes
    author_id: bytes
    round: int
    strong_parent_digests: List[bytes]
    transition: PlanetaryStateTransition
    pqc_envelope: PostQuantumEnvelope

    @classmethod
    def create(
        cls,
        author_id: bytes,
        round_num: int,
        parents: List[bytes],
        transition: PlanetaryStateTransition,
        pqc_envelope: Optional[PostQuantumEnvelope] = None,
    ) -> DagVertex:
        digest = compute_canonical_digest(author_id, round_num, parents, transition)
        if pqc_envelope is None:
            pqc_envelope = PostQuantumEnvelope(
                sender_node_id=author_id,
                kyber1024_ciphertext=b"\xAA" * 1568,
                dilithium5_signature=b"\xBB" * 4595,
                blake3_state_digest=digest,
            )
        return cls(
            vertex_digest=digest,
            author_id=author_id,
            round=round_num,
            strong_parent_digests=parents,
            transition=transition,
            pqc_envelope=pqc_envelope,
        )

    def compute_sha3_digest(self) -> bytes:
        payload = (
            self.author_id
            + self.round.to_bytes(8, "little")
            + b"".join(self.strong_parent_digests)
            + self.transition.serialize_canonical()
            + self.pqc_envelope.sender_node_id
            + self.pqc_envelope.kyber1024_ciphertext
            + self.pqc_envelope.dilithium5_signature
        )
        return sha3_512(payload)


# ============================================================================
# Bullshark Asynchronous BFT DAG Consensus Engine
# ============================================================================

class BullsharkDagEngine:
    def __init__(self, total_validators: int, validator_id: bytes = b"\x00" * 32):
        self.validator_id = validator_id
        self.total_validators = total_validators
        self.max_byzantine_faults = max(0, (total_validators - 1) // 3)
        self.current_round = 0
        self.dag_storage: Dict[bytes, DagVertex] = {}
        self.rounds_index: Dict[int, List[bytes]] = {}
        self.committed_anchors: List[bytes] = []
        self.committed_vertex_set: Set[bytes] = set()
        self.linearized_history: List[bytes] = []
        self.last_committed_batch: List[DagVertex] = []
        self.planetary_state = PlanetaryState.genesis()

    def quorum_threshold(self) -> int:
        return 2 * self.max_byzantine_faults + 1

    def anchor_vote_threshold(self) -> int:
        return self.max_byzantine_faults + 1

    def insert_vertex(self, vertex: DagVertex) -> Optional[bytes]:
        """
        Validates vertex canonical digest, quorum parents, and checks Bullshark anchor commit.
        Returns committed anchor hash if a new anchor commits, else None.
        """
        expected_digest = compute_canonical_digest(
            vertex.author_id,
            vertex.round,
            vertex.strong_parent_digests,
            vertex.transition,
        )

        if expected_digest != vertex.vertex_digest or expected_digest != vertex.pqc_envelope.blake3_state_digest:
            raise ValueError("InvalidPostQuantumSignature")

        if vertex.round > 1:
            if len(vertex.strong_parent_digests) < self.quorum_threshold():
                raise ValueError(
                    f"InsufficientByzantineQuorum: provided {len(vertex.strong_parent_digests)}, "
                    f"required {self.quorum_threshold()}"
                )
            for p in vertex.strong_parent_digests:
                if p not in self.dag_storage:
                    raise ValueError(f"OrphanParentVertex: {p[:8].hex()}")

        digest = vertex.vertex_digest
        v_round = vertex.round

        if digest in self.dag_storage:
            return None

        self.dag_storage[digest] = vertex
        self.rounds_index.setdefault(v_round, []).append(digest)
        if v_round > self.current_round:
            self.current_round = v_round

        # Bullshark Even-Round Anchor Commit Rule:
        # If round R is odd (R >= 3), check leader anchor at round R - 1
        if v_round >= 3 and v_round % 2 == 1:
            anchor_round = v_round - 1
            anchor_candidates = self.rounds_index.get(anchor_round, [])
            if anchor_candidates:
                # Deterministic leader selection across validators: round-robin starting at 0 for round 2
                leader_idx = ((anchor_round - 2) // 2) % len(anchor_candidates)
                leader_anchor = anchor_candidates[leader_idx]
                round_r_vertices = self.rounds_index.get(v_round, [])
                votes_for_anchor = 0

                for r_hash in round_r_vertices:
                    v = self.dag_storage.get(r_hash)
                    if v and leader_anchor in v.strong_parent_digests:
                        votes_for_anchor += 1

                if votes_for_anchor >= self.anchor_vote_threshold() and leader_anchor not in self.committed_anchors:
                    self.committed_anchors.append(leader_anchor)

                    # Topologically linearize subdag and apply state transitions
                    subdag = self.linearize_subdag(leader_anchor)
                    for v_exec in subdag:
                        v_exec.transition.verify_and_apply(self.planetary_state)
                        self.committed_vertex_set.add(v_exec.vertex_digest)
                        self.linearized_history.append(v_exec.vertex_digest)

                    self.last_committed_batch = subdag
                    return leader_anchor

        return None

    def add_vertex(self, vertex: DagVertex) -> List[DagVertex]:
        anchor = self.insert_vertex(vertex)
        if anchor:
            return list(self.last_committed_batch)
        return []

    def linearize_subdag(self, anchor_hash: bytes) -> List[DagVertex]:
        """
        Traverses backwards from anchor and orders uncommitted ancestors topologically.
        """
        uncommitted: List[DagVertex] = []
        visited: Set[bytes] = set()
        queue = [anchor_hash]

        while queue:
            cur = queue.pop()
            if cur in self.committed_vertex_set or cur in visited:
                continue
            visited.add(cur)
            v = self.dag_storage.get(cur)
            if v:
                uncommitted.append(v)
                for parent in v.strong_parent_digests:
                    queue.append(parent)

        # Strictly deterministic topological sort by (round asc, digest asc)
        uncommitted.sort(key=lambda x: (x.round, x.vertex_digest))
        return uncommitted

    def get_state(self) -> PlanetaryState:
        return self.planetary_state

    def get_state_root(self) -> bytes:
        return self.planetary_state.state_root


# ============================================================================
# Post-Quantum CRYSTALS-Kyber (ML-KEM-1024) Abstraction
# ============================================================================

@dataclass
class KyberCiphertext:
    data: bytes          # 1568 bytes
    shared_secret: bytes # 32 bytes


class KyberKemKeypair:
    def __init__(self, public_key: bytes, secret_key: bytes):
        self.public_key = public_key   # 1568 bytes
        self.secret_key = secret_key   # 3168 bytes

    @classmethod
    def generate(cls) -> KyberKemKeypair:
        seed = os.urandom(32)
        return cls.generate_from_seed(seed)

    @classmethod
    def generate_from_seed(cls, seed: bytes) -> KyberKemKeypair:
        pk_seed_hash = sha3_512(seed + b"KYBER_1024_PK_SEED")
        public_key = bytearray(1568)
        public_key[:32] = pk_seed_hash[:32]
        for i in range(32, 1568):
            public_key[i] = pk_seed_hash[i % 64] ^ (i & 0xFF)

        sk_seed_hash = sha3_512(seed + b"KYBER_1024_SK_SEED")
        secret_key = bytearray(3168)
        secret_key[:32] = seed
        for i in range(32, 1568):
            secret_key[i] = sk_seed_hash[i % 64] ^ (i & 0xFF)
        secret_key[1568:3136] = public_key
        h_pk = sha3_512(bytes(public_key))
        secret_key[3136:3168] = h_pk[:32]

        return cls(bytes(public_key), bytes(secret_key))

    def encapsulate(self, peer_pk: bytes) -> KyberCiphertext:
        ephemeral_seed = os.urandom(32)
        mask_hash = sha3_512(peer_pk[:32] + b"KEM_MASK")
        ss_input = ephemeral_seed + peer_pk[:32] + b"SHARED_SECRET"
        shared_secret = sha3_512(ss_input)[:32]

        ct_data = bytearray(1568)
        for i in range(32):
            ct_data[i] = ephemeral_seed[i] ^ mask_hash[i]

        tag_hash = sha3_512(ephemeral_seed + peer_pk)
        for i in range(32, 1568):
            ct_data[i] = tag_hash[i % 64] ^ (i & 0xFF)

        return KyberCiphertext(bytes(ct_data), shared_secret)

    def decapsulate(self, ct_data: bytes) -> bytes:
        if len(ct_data) != 1568:
            raise ValueError("InvalidCiphertextLength")

        recipient_pk = self.secret_key[1568:3136]
        mask_hash = sha3_512(recipient_pk[:32] + b"KEM_MASK")

        ephemeral_seed = bytearray(32)
        for i in range(32):
            ephemeral_seed[i] = ct_data[i] ^ mask_hash[i]

        expected_tag = sha3_512(bytes(ephemeral_seed) + recipient_pk)
        for i in range(32, 1568):
            if ct_data[i] != (expected_tag[i % 64] ^ (i & 0xFF)):
                raise ValueError("InvalidKyberCiphertextOrIntegrityFailure")

        ss_input = bytes(ephemeral_seed) + recipient_pk[:32] + b"SHARED_SECRET"
        return sha3_512(ss_input)[:32]


# ============================================================================
# Planetary Node Wire Protocol & Telemetry
# ============================================================================

class NodeType(enum.Enum):
    TokamakFusionCore = 1
    OrbitalLaserStation = 2
    LunarMassDriver = 3
    TerrestrialValidator = 4
    RelayMeshNode = 5


@dataclass
class TelemetryPacket:
    node_id: bytes
    node_type: NodeType
    timestamp_tai_ns: int
    net_energy_surplus_mw: float
    compute_load_pct: float
    state_hash: bytes
    signature: bytes = field(default_factory=lambda: b"\xAA" * 64)

    @classmethod
    def compute_hash(
        cls,
        node_id: bytes,
        node_type: NodeType,
        timestamp_tai_ns: int,
        net_energy_surplus_mw: float,
        compute_load_pct: float,
    ) -> bytes:
        buf = (
            node_id
            + bytes([node_type.value])
            + timestamp_tai_ns.to_bytes(16, "little", signed=False)
            + struct.pack("<d", net_energy_surplus_mw)
            + struct.pack("<d", compute_load_pct)
        )
        return sha3_512(buf)

    @classmethod
    def create(
        cls,
        node_id: bytes,
        node_type: NodeType,
        timestamp_tai_ns: int,
        net_energy_surplus_mw: float,
        compute_load_pct: float,
    ) -> TelemetryPacket:
        h = cls.compute_hash(node_id, node_type, timestamp_tai_ns, net_energy_surplus_mw, compute_load_pct)
        return cls(
            node_id=node_id,
            node_type=node_type,
            timestamp_tai_ns=timestamp_tai_ns,
            net_energy_surplus_mw=net_energy_surplus_mw,
            compute_load_pct=compute_load_pct,
            state_hash=h,
        )

    def verify_hash(self) -> bool:
        expected = self.compute_hash(
            self.node_id,
            self.node_type,
            self.timestamp_tai_ns,
            self.net_energy_surplus_mw,
            self.compute_load_pct,
        )
        return expected == self.state_hash


@dataclass
class WireMessage:
    msg_type: int
    sender_id: bytes
    recipient_id: bytes
    payload: bytes
    kem_ciphertext: Optional[bytes] = None
    magic: bytes = b"AETH"
    version: int = 1

    def encode(self) -> bytes:
        buf = bytearray()
        buf.extend(self.magic)
        buf.extend(self.version.to_bytes(2, "little"))
        buf.extend(self.msg_type.to_bytes(2, "little"))
        buf.extend(self.sender_id)
        buf.extend(self.recipient_id)
        buf.extend(len(self.payload).to_bytes(4, "little"))
        buf.extend(self.payload)
        if self.kem_ciphertext:
            buf.append(1)
            buf.extend(len(self.kem_ciphertext).to_bytes(4, "little"))
            buf.extend(self.kem_ciphertext)
        else:
            buf.append(0)
        return bytes(buf)

    @classmethod
    def decode(cls, data: bytes) -> WireMessage:
        if len(data) < 77:
            raise ValueError("BufferTooSmallForWireHeader")
        magic = data[:4]
        if magic != b"AETH":
            raise ValueError("InvalidMagicBytes")
        version = int.from_bytes(data[4:6], "little")
        msg_type = int.from_bytes(data[6:8], "little")
        sender_id = data[8:40]
        recipient_id = data[40:72]
        payload_len = int.from_bytes(data[72:76], "little")
        payload_end = 76 + payload_len
        payload = data[76:payload_end]
        has_ct = data[payload_end] == 1
        kem_ct = None
        if has_ct:
            ct_len = int.from_bytes(data[payload_end + 1 : payload_end + 5], "little")
            ct_start = payload_end + 5
            kem_ct = data[ct_start : ct_start + ct_len]
        return cls(
            magic=magic,
            version=version,
            msg_type=msg_type,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payload=payload,
            kem_ciphertext=kem_ct,
        )


class PlanetaryKernelNode:
    def __init__(self, node_id: bytes, node_type: NodeType):
        self.node_id = node_id
        self.node_type = node_type
        self.keypair = KyberKemKeypair.generate()
        self.peer_ledger: Dict[bytes, TelemetryPacket] = {}
        self.channel: List[TelemetryPacket] = []

    def broadcast_telemetry(self, net_energy_surplus_mw: float, compute_load_pct: float) -> TelemetryPacket:
        now_ns = int(time.time() * 1_000_000_000)
        packet = TelemetryPacket.create(
            self.node_id,
            self.node_type,
            now_ns,
            net_energy_surplus_mw,
            compute_load_pct,
        )
        self.peer_ledger[self.node_id] = packet
        self.channel.append(packet)
        return packet

    def receive_and_process_telemetry(self, packet: TelemetryPacket) -> bool:
        if packet.verify_hash():
            self.peer_ledger[packet.node_id] = packet
            return True
        return False

    def calculate_global_energy_grid_balance(self) -> float:
        net = 0.0
        for packet in self.peer_ledger.values():
            if packet.verify_hash():
                net += packet.net_energy_surplus_mw
        return net

    def establish_secure_channel(self, peer_pk: bytes) -> Tuple[KyberCiphertext, bytes]:
        ct = self.keypair.encapsulate(peer_pk)
        return ct, ct.shared_secret


# ============================================================================
# Verification Suite Functions
# ============================================================================

def verify_rust_compilation(workspace_root: str = "e:/2027 nov") -> Dict[str, Any]:
    """Compiles aether_core.rs and planetary_node.rs using native rustc."""
    results = {}
    rust_files = [
        ("aether_core", os.path.join(workspace_root, "src", "kernel", "aether_core.rs")),
        ("planetary_node", os.path.join(workspace_root, "src", "kernel", "planetary_node.rs")),
    ]

    for name, filepath in rust_files:
        if not os.path.exists(filepath):
            results[name] = {"success": False, "error": f"File not found: {filepath}"}
            continue

        temp_rlib = os.path.join(workspace_root, ".agents", "teamwork", "worker_m2", f"lib{name}.rlib")
        cmd = ["rustc", "--edition=2021", "--crate-type=rlib", filepath, "-o", temp_rlib]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            success = (proc.returncode == 0)
            results[name] = {
                "success": success,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            }
            if os.path.exists(temp_rlib):
                os.remove(temp_rlib)
        except Exception as e:
            results[name] = {"success": False, "error": str(e)}

    return results


def run_consensus_simulation() -> Dict[str, Any]:
    """Simulates N=4 (f=1) Bullshark DAG consensus across Rounds 1, 2, and 3."""
    engine = BullsharkDagEngine(total_validators=4)
    assert engine.quorum_threshold() == 3, f"Quorum should be 3, got {engine.quorum_threshold()}"
    assert engine.anchor_vote_threshold() == 2, f"Anchor vote threshold should be 2, got {engine.anchor_vote_threshold()}"

    def make_vertex(author_byte: int, round_num: int, parents: List[bytes]) -> DagVertex:
        author = bytes([author_byte] * 32)
        trans = PlanetaryStateTransition(
            epoch_round=round_num,
            timestamp_tai_ns=1_800_000_000_000_000_000 + round_num * 1_000_000,
            net_energy_delta_uw=450_000_000_000_000,  # +450 MW
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=48_383,
        )
        return DagVertex.create(author, round_num, parents, trans)

    # Round 1: Genesis vertices
    r1_hashes = []
    for node_id in range(1, 4):
        v = make_vertex(node_id, 1, [])
        r1_hashes.append(v.vertex_digest)
        res = engine.insert_vertex(v)
        assert res is None, "Round 1 should not commit an anchor"

    # Round 2: Anchor round referencing all 3 Round-1 vertices
    r2_hashes = []
    for node_id in range(1, 4):
        v = make_vertex(node_id, 2, r1_hashes)
        r2_hashes.append(v.vertex_digest)
        res = engine.insert_vertex(v)
        assert res is None, "Round 2 should not commit an anchor"

    # Round 3: Voting round referencing all 3 Round-2 vertices
    committed_anchor = None
    for node_id in range(1, 4):
        v = make_vertex(node_id, 3, r2_hashes)
        commit = engine.insert_vertex(v)
        if commit:
            committed_anchor = commit

    assert committed_anchor is not None, "Round 3 should have committed Round-2 anchor!"
    assert committed_anchor == r2_hashes[0], "Leader anchor should be first vertex of Round 2"
    assert len(engine.committed_anchors) == 1
    assert len(engine.linearized_history) >= 4, "Linearized history should contain causal ancestors"
    assert engine.get_state().cumulative_energy_uw > 0, "Energy state should accumulate"

    return {
        "status": "PASS",
        "committed_anchor": committed_anchor.hex()[:16],
        "linearized_vertices_count": len(engine.linearized_history),
        "cumulative_energy_mw": engine.get_state().cumulative_energy_uw / 1_000_000_000_000,
        "state_root": engine.get_state_root().hex()[:16],
    }


def run_wire_protocol_simulation() -> Dict[str, Any]:
    """Tests Kyber KEM, telemetry wire framing, and Byzantine filtering."""
    # 1. Kyber KEM Shared Secret Equality
    alice = PlanetaryKernelNode(bytes([1] * 32), NodeType.TokamakFusionCore)
    bob = PlanetaryKernelNode(bytes([2] * 32), NodeType.OrbitalLaserStation)

    ct, alice_ss = alice.establish_secure_channel(bob.keypair.public_key)
    bob_ss = bob.keypair.decapsulate(ct.data)
    assert alice_ss == bob_ss, "Shared secrets derived by Alice and Bob must be identical!"

    # 2. Tampered ciphertext rejection
    tampered_ct = bytearray(ct.data)
    tampered_ct[50] ^= 0xFF
    try:
        bob.keypair.decapsulate(bytes(tampered_ct))
        tampered_caught = False
    except ValueError:
        tampered_caught = True
    assert tampered_caught, "Tampered Kyber ciphertext must be rejected!"

    # 3. Telemetry broadcast and Byzantine filtering
    alice_pkt = alice.broadcast_telemetry(net_energy_surplus_mw=250.0, compute_load_pct=42.5)
    assert alice_pkt.verify_hash(), "Telemetry hash must verify"

    # Bob receives Alice's valid telemetry
    bob.receive_and_process_telemetry(alice_pkt)

    # Create forged / Byzantine packet
    byzantine_pkt = TelemetryPacket(
        node_id=bytes([99] * 32),
        node_type=NodeType.TerrestrialValidator,
        timestamp_tai_ns=123456789,
        net_energy_surplus_mw=999999.0,
        compute_load_pct=10.0,
        state_hash=bytes([0] * 64), # Invalid forged hash
    )
    assert not byzantine_pkt.verify_hash()
    accepted = bob.receive_and_process_telemetry(byzantine_pkt)
    assert not accepted, "Byzantine packet must be rejected from peer ledger"

    grid_balance = bob.calculate_global_energy_grid_balance()
    assert grid_balance == 250.0, f"Grid balance should only sum valid packets (expected 250.0, got {grid_balance})"

    # 4. WireMessage framing encode / decode
    msg = WireMessage(
        msg_type=1,
        sender_id=alice.node_id,
        recipient_id=bob.node_id,
        payload=b"AETHER_TELEMETRY_PAYLOAD_V1",
        kem_ciphertext=ct.data,
    )
    encoded = msg.encode()
    decoded = WireMessage.decode(encoded)
    assert decoded.msg_type == msg.msg_type
    assert decoded.sender_id == msg.sender_id
    assert decoded.payload == msg.payload
    assert decoded.kem_ciphertext == ct.data

    return {
        "status": "PASS",
        "shared_secret_match": True,
        "tamper_protection_verified": True,
        "byzantine_filtering_verified": True,
        "grid_balance_mw": grid_balance,
        "wire_framing_verified": True,
    }


def run_all_verifications(workspace_root: str = "e:/2027 nov") -> Dict[str, Any]:
    print("=" * 78)
    print("[*] RUNNING AETHER-OMEGA MILESTONE 2 VERIFICATION RUNNER")
    print("=" * 78)

    rust_compilation = verify_rust_compilation(workspace_root)
    print(f"1. Rust Toolchain Compilation: {rust_compilation}")

    consensus_result = run_consensus_simulation()
    print(f"2. Bullshark DAG Consensus Simulation: {consensus_result}")

    wire_result = run_wire_protocol_simulation()
    print(f"3. Post-Quantum Kyber & Wire Protocol: {wire_result}")

    all_passed = (
        all(r.get("success", False) for r in rust_compilation.values())
        and consensus_result.get("status") == "PASS"
        and wire_result.get("status") == "PASS"
    )

    print("=" * 78)
    print(f"VERIFICATION STATUS: {'[PASS] ALL TESTS PASSED' if all_passed else '[FAIL] SOME TESTS FAILED'}")
    print("=" * 78)

    return {
        "all_passed": all_passed,
        "rust_compilation": rust_compilation,
        "consensus_simulation": consensus_result,
        "wire_protocol_simulation": wire_result,
    }


if __name__ == "__main__":
    report = run_all_verifications()
    sys.exit(0 if report["all_passed"] else 1)
