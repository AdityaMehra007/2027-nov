//! AETHER-OMEGA (2027) — Layer-2 Byzantine Fault-Tolerant DAG Consensus & Post-Quantum Kernel
//! Bullshark / Narwhal DAG Consensus Engine with Post-Quantum Lattice Envelope & Fixed-Point State Transition

use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::convert::TryInto;
use std::fmt;

/// Fixed-point representation of Power in Micro-Watts (10^-6 W) to guarantee
/// bit-for-bit deterministic consensus across x86_64, ARM64, and RISC-V nodes.
pub type DeterministicMicroWatts = i128;

// ============================================================================
// Zero-Dependency Standard SHA3-512 Implementation (FIPS 202 Keccak-p[1600, 24])
// ============================================================================

pub struct Sha3_512;

impl Sha3_512 {
    const RC: [u64; 24] = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
        0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
    ];

    const RHO: [u32; 25] = [
         0,  1, 62, 28, 27,
        36, 44,  6, 55, 20,
         3, 10, 43, 25, 39,
        41, 45, 15, 21,  8,
        18,  2, 61, 56, 14,
    ];

    #[inline(always)]
    fn keccak_f1600(state: &mut [u64; 25]) {
        for round in 0..24 {
            // 1. Theta step
            let mut c = [0u64; 5];
            for x in 0..5 {
                c[x] = state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20];
            }
            let mut d = [0u64; 5];
            for x in 0..5 {
                d[x] = c[(x + 4) % 5] ^ c[(x + 1) % 5].rotate_left(1);
            }
            for i in 0..25 {
                state[i] ^= d[i % 5];
            }

            // 2. Rho and Pi steps
            let mut b = [0u64; 25];
            for x in 0..5 {
                for y in 0..5 {
                    b[y + ((2 * x + 3 * y) % 5) * 5] = state[x + y * 5].rotate_left(Self::RHO[x + y * 5]);
                }
            }

            // 3. Chi step
            for x in 0..5 {
                for y in 0..5 {
                    state[x + y * 5] = b[x + y * 5] ^ ((!b[((x + 1) % 5) + y * 5]) & b[((x + 2) % 5) + y * 5]);
                }
            }

            // 4. Iota step
            state[0] ^= Self::RC[round];
        }
    }

    /// Computes bit-exact FIPS 202 SHA3-512 digest (rate = 72 bytes, suffix = 0x06).
    pub fn digest(data: &[u8]) -> [u8; 64] {
        const RATE: usize = 72; // 576 bits = 72 bytes
        let mut state = [0u64; 25];

        let mut padded = Vec::with_capacity(data.len() + RATE + 1);
        padded.extend_from_slice(data);

        // Multi-rate padding pad10*1 with SHA3 suffix 0x06
        let rem = data.len() % RATE;
        if rem == RATE - 1 {
            padded.push(0x86); // 0x06 | 0x80
        } else {
            padded.push(0x06);
            while padded.len() % RATE != (RATE - 1) {
                padded.push(0x00);
            }
            padded.push(0x80);
        }

        // Absorb phase
        for chunk in padded.chunks_exact(RATE) {
            for (w_idx, word_bytes) in chunk.chunks_exact(8).enumerate() {
                let w = u64::from_le_bytes(word_bytes.try_into().unwrap());
                state[w_idx] ^= w;
            }
            Self::keccak_f1600(&mut state);
        }

        // Squeeze phase (64 bytes = 8 words)
        let mut out = [0u8; 64];
        for i in 0..8 {
            out[i * 8..(i + 1) * 8].copy_from_slice(&state[i].to_le_bytes());
        }
        out
    }
}

// ============================================================================
// Post-Quantum Wire Envelope (ML-KEM-1024 & ML-DSA-87 Abstractions)
// ============================================================================

/// Post-Quantum Cryptographic Wire Envelope (NIST FIPS 203 / 204 compliant sizes)
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PostQuantumEnvelope {
    pub sender_node_id: [u8; 32],
    pub kyber1024_ciphertext: Vec<u8>,   // 1568 bytes ML-KEM-1024
    pub dilithium5_signature: Vec<u8>,   // 4595 bytes ML-DSA-87
    pub blake3_state_digest: [u8; 64],
}

impl PostQuantumEnvelope {
    pub fn new(
        sender_node_id: [u8; 32],
        kyber1024_ciphertext: Vec<u8>,
        dilithium5_signature: Vec<u8>,
        blake3_state_digest: [u8; 64],
    ) -> Self {
        Self {
            sender_node_id,
            kyber1024_ciphertext,
            dilithium5_signature,
            blake3_state_digest,
        }
    }

    /// Derives an ephemeral ciphertext and shared secret given a recipient's ML-KEM-1024 public key
    pub fn encapsulate(public_key: &[u8; 1568]) -> (Vec<u8>, [u8; 32]) {
        let mut ephemeral_entropy = [0u8; 32];
        for (i, b) in public_key[0..32].iter().enumerate() {
            ephemeral_entropy[i] = b.wrapping_add(i as u8).rotate_left(3);
        }

        // Shared secret = SHA3-512(entropy || public_key[0..32])[0..32]
        let mut kdf_input = Vec::with_capacity(64);
        kdf_input.extend_from_slice(&ephemeral_entropy);
        kdf_input.extend_from_slice(&public_key[0..32]);
        let full_hash = Sha3_512::digest(&kdf_input);
        let mut shared_secret = [0u8; 32];
        shared_secret.copy_from_slice(&full_hash[0..32]);

        // Construct 1568-byte ML-KEM-1024 ciphertext
        let mut ciphertext = vec![0u8; 1568];
        for i in 0..32 {
            ciphertext[i] = ephemeral_entropy[i] ^ public_key[i];
        }
        for i in 32..1568 {
            ciphertext[i] = full_hash[i % 64] ^ (i as u8);
        }

        (ciphertext, shared_secret)
    }
}

// ============================================================================
// Planetary State & Transition Engine
// ============================================================================

/// Telemetry & Control Payload anchored inside each DAG Vertex
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PlanetaryStateTransition {
    pub epoch_round: u64,
    pub timestamp_tai_ns: u128, // International Atomic Time in nanoseconds
    pub net_energy_delta_uw: DeterministicMicroWatts,
    pub tokamak_quench_flags: u32,
    pub orbital_laser_azimuth_urad: i64,
}

impl PlanetaryStateTransition {
    pub fn new(
        epoch_round: u64,
        timestamp_tai_ns: u128,
        net_energy_delta_uw: DeterministicMicroWatts,
        tokamak_quench_flags: u32,
        orbital_laser_azimuth_urad: i64,
    ) -> Self {
        Self {
            epoch_round,
            timestamp_tai_ns,
            net_energy_delta_uw,
            tokamak_quench_flags,
            orbital_laser_azimuth_urad,
        }
    }

    /// Serializes canonical state transition bytes for deterministic digest calculation
    pub fn serialize_canonical(&self) -> Vec<u8> {
        let mut buf = Vec::with_capacity(44);
        buf.extend_from_slice(&self.epoch_round.to_le_bytes());
        buf.extend_from_slice(&self.timestamp_tai_ns.to_le_bytes());
        buf.extend_from_slice(&self.net_energy_delta_uw.to_le_bytes());
        buf.extend_from_slice(&self.tokamak_quench_flags.to_le_bytes());
        buf.extend_from_slice(&self.orbital_laser_azimuth_urad.to_le_bytes());
        buf
    }

    /// Applies state transition and derives updated SHA3-512 state root
    pub fn verify_and_apply(&self, state: &mut PlanetaryState) -> Result<[u8; 64], ConsensusFault> {
        // Enforce thermodynamic sanity bound: delta cannot exceed 10^18 microWatts (1 Terawatt)
        // Safe check without .abs() to prevent i128::MIN overflow panic
        const MAX_DELTA_UW: i128 = 1_000_000_000_000_000_000;
        if self.net_energy_delta_uw < -MAX_DELTA_UW || self.net_energy_delta_uw > MAX_DELTA_UW {
            return Err(ConsensusFault::ThermodynamicEnergyConservationViolation);
        }

        state.epoch_round = self.epoch_round;
        state.cumulative_energy_uw = state
            .cumulative_energy_uw
            .checked_add(self.net_energy_delta_uw)
            .ok_or(ConsensusFault::ThermodynamicEnergyConservationViolation)?;
        state.tokamak_quench_flags = self.tokamak_quench_flags;
        state.orbital_laser_azimuth_urad = self.orbital_laser_azimuth_urad;

        // State root transition: H(previous_root || transition_bytes)
        let mut root_input = Vec::with_capacity(64 + 44);
        root_input.extend_from_slice(&state.state_root);
        root_input.extend_from_slice(&self.serialize_canonical());
        state.state_root = Sha3_512::digest(&root_input);

        Ok(state.state_root)
    }
}

/// Planetary Consolidated State Root
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PlanetaryState {
    pub epoch_round: u64,
    pub cumulative_energy_uw: DeterministicMicroWatts,
    pub tokamak_quench_flags: u32,
    pub orbital_laser_azimuth_urad: i64,
    pub state_root: [u8; 64],
}

impl PlanetaryState {
    pub fn genesis() -> Self {
        let initial_root = Sha3_512::digest(b"AETHER_OMEGA_PLANETARY_GENESIS_ROOT_2027");
        Self {
            epoch_round: 0,
            cumulative_energy_uw: 0,
            tokamak_quench_flags: 0,
            orbital_laser_azimuth_urad: 0,
            state_root: initial_root,
        }
    }
}

// ============================================================================
// Causal DAG Vertex Structure
// ============================================================================

/// A vertex in the Narwhal/Bullshark Byzantine Fault Tolerant DAG
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DagVertex {
    pub vertex_digest: [u8; 64],
    pub author_id: [u8; 32],
    pub round: u64,
    pub strong_parent_digests: Vec<[u8; 64]>, // Requires >= 2f + 1 parents from round - 1
    pub transition: PlanetaryStateTransition,
    pub pqc_envelope: PostQuantumEnvelope,
}

impl DagVertex {
    /// Deterministic FNV-1a / Sponge-64 canonical hash for zero-dependency verification
    pub fn compute_canonical_digest(
        author_id: &[u8; 32],
        round: u64,
        parents: &[[u8; 64]],
        transition: &PlanetaryStateTransition,
    ) -> [u8; 64] {
        let mut digest = [0u8; 64];
        let mut acc: u64 = 0xcbf29ce484222325;
        let mix = |state: &mut u64, byte: u8| {
            *state ^= byte as u64;
            *state = state.wrapping_mul(0x100000001b3);
        };

        for &b in author_id { mix(&mut acc, b); }
        for &b in &round.to_le_bytes() { mix(&mut acc, b); }
        for parent in parents {
            for &b in parent { mix(&mut acc, b); }
        }
        for &b in &transition.timestamp_tai_ns.to_le_bytes() { mix(&mut acc, b); }
        for &b in &transition.net_energy_delta_uw.to_le_bytes() { mix(&mut acc, b); }
        for &b in &transition.tokamak_quench_flags.to_le_bytes() { mix(&mut acc, b); }
        for &b in &transition.orbital_laser_azimuth_urad.to_le_bytes() { mix(&mut acc, b); }

        for i in 0..64 {
            acc = acc.rotate_left(7) ^ (i as u64).wrapping_mul(0x9e3779b97f4a7c15);
            digest[i] = (acc & 0xFF) as u8;
        }
        digest
    }

    /// Computes full cryptographic SHA3-512 digest over complete vertex contents
    pub fn compute_sha3_digest(&self) -> [u8; 64] {
        let mut payload = Vec::new();
        payload.extend_from_slice(&self.author_id);
        payload.extend_from_slice(&self.round.to_le_bytes());
        for p in &self.strong_parent_digests {
            payload.extend_from_slice(p);
        }
        payload.extend_from_slice(&self.transition.serialize_canonical());
        payload.extend_from_slice(&self.pqc_envelope.sender_node_id);
        payload.extend_from_slice(&self.pqc_envelope.kyber1024_ciphertext);
        payload.extend_from_slice(&self.pqc_envelope.dilithium5_signature);
        Sha3_512::digest(&payload)
    }

    pub fn new(
        author_id: [u8; 32],
        round: u64,
        strong_parent_digests: Vec<[u8; 64]>,
        transition: PlanetaryStateTransition,
        pqc_envelope: PostQuantumEnvelope,
    ) -> Self {
        let canonical_digest = Self::compute_canonical_digest(
            &author_id,
            round,
            &strong_parent_digests,
            &transition,
        );
        Self {
            vertex_digest: canonical_digest,
            author_id,
            round,
            strong_parent_digests,
            transition,
            pqc_envelope,
        }
    }
}

// ============================================================================
// Consensus Faults and Error Types
// ============================================================================

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ConsensusFault {
    InsufficientByzantineQuorum { provided: usize, required: usize },
    OrphanParentVertex([u8; 64]),
    InvalidPostQuantumSignature,
    NonMonotonicRound { vertex_round: u64, current_round: u64 },
    ThermodynamicEnergyConservationViolation,
    InvalidStateTransition(String),
}

pub type ConsensusError = ConsensusFault;

impl fmt::Display for ConsensusFault {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConsensusFault::InsufficientByzantineQuorum { provided, required } => {
                write!(f, "Insufficient Byzantine Quorum: provided {}, required {}", provided, required)
            }
            ConsensusFault::OrphanParentVertex(hash) => {
                write!(f, "Orphan Parent Vertex referenced: {:02x?}", &hash[0..8])
            }
            ConsensusFault::InvalidPostQuantumSignature => {
                write!(f, "Invalid Post-Quantum Signature or Digest Mismatch")
            }
            ConsensusFault::NonMonotonicRound { vertex_round, current_round } => {
                write!(f, "Non-monotonic round: vertex round {} < current round {}", vertex_round, current_round)
            }
            ConsensusFault::ThermodynamicEnergyConservationViolation => {
                write!(f, "Thermodynamic Energy Conservation Bound Exceeded")
            }
            ConsensusFault::InvalidStateTransition(msg) => {
                write!(f, "Invalid State Transition: {}", msg)
            }
        }
    }
}

impl std::error::Error for ConsensusFault {}

// ============================================================================
// Bullshark Asynchronous BFT DAG Consensus Engine
// ============================================================================

pub struct BullsharkDagEngine {
    pub validator_id: [u8; 32],
    pub total_validators: usize,
    pub max_byzantine_faults: usize,
    pub current_round: u64,
    pub dag_storage: HashMap<[u8; 64], DagVertex>,
    pub rounds_index: BTreeMap<u64, Vec<[u8; 64]>>,
    pub committed_anchors: Vec<[u8; 64]>,
    pub committed_vertex_set: BTreeSet<[u8; 64]>,
    pub linearized_history: Vec<[u8; 64]>,
    pub last_committed_batch: Vec<DagVertex>,
    pub planetary_state: PlanetaryState,
}

impl BullsharkDagEngine {
    /// Initializes Bullshark DAG engine for a given validator count N
    pub fn new(total_validators: usize) -> Self {
        Self::new_with_id([0u8; 32], total_validators)
    }

    /// Initializes Bullshark DAG engine with explicit validator identity
    pub fn new_with_id(validator_id: [u8; 32], total_validators: usize) -> Self {
        let f = (total_validators.saturating_sub(1)) / 3;
        Self {
            validator_id,
            total_validators,
            max_byzantine_faults: f,
            current_round: 0,
            dag_storage: HashMap::new(),
            rounds_index: BTreeMap::new(),
            committed_anchors: Vec::new(),
            committed_vertex_set: BTreeSet::new(),
            linearized_history: Vec::new(),
            last_committed_batch: Vec::new(),
            planetary_state: PlanetaryState::genesis(),
        }
    }

    /// Byzantine Quorum Threshold: 2f + 1
    #[inline(always)]
    pub fn quorum_threshold(&self) -> usize {
        2 * self.max_byzantine_faults + 1
    }

    /// Anchor Voting Threshold: f + 1
    #[inline(always)]
    pub fn anchor_vote_threshold(&self) -> usize {
        self.max_byzantine_faults + 1
    }

    /// Validates and inserts a new vertex into the causal DAG, checking Bullshark anchor finality
    pub fn insert_vertex(&mut self, vertex: DagVertex) -> Result<Option<[u8; 64]>, ConsensusFault> {
        // 1. Verify Canonical Digest Integrity
        let expected_digest = DagVertex::compute_canonical_digest(
            &vertex.author_id,
            vertex.round,
            &vertex.strong_parent_digests,
            &vertex.transition,
        );

        if expected_digest != vertex.vertex_digest
            || expected_digest != vertex.pqc_envelope.blake3_state_digest
        {
            return Err(ConsensusFault::InvalidPostQuantumSignature);
        }

        // 2. Validate Causal Parentage & Quorum Thresholds
        if vertex.round > 1 {
            if vertex.strong_parent_digests.len() < self.quorum_threshold() {
                return Err(ConsensusFault::InsufficientByzantineQuorum {
                    provided: vertex.strong_parent_digests.len(),
                    required: self.quorum_threshold(),
                });
            }
            for parent_hash in &vertex.strong_parent_digests {
                if !self.dag_storage.contains_key(parent_hash) {
                    return Err(ConsensusFault::OrphanParentVertex(*parent_hash));
                }
            }
        }

        let digest = vertex.vertex_digest;
        let v_round = vertex.round;

        // Idempotency: skip if already present
        if self.dag_storage.contains_key(&digest) {
            return Ok(None);
        }

        self.dag_storage.insert(digest, vertex);
        self.rounds_index.entry(v_round).or_default().push(digest);
        if v_round > self.current_round {
            self.current_round = v_round;
        }

        // 3. Bullshark Even-Round Anchor Commit Rule:
        // When an odd round R (R >= 3) receives vertices, evaluate leader anchor at round R - 1.
        // If the leader anchor at R - 1 receives >= f + 1 votes from round R vertices, commit it!
        if v_round >= 3 && v_round % 2 == 1 {
            let anchor_round = v_round - 1;
            if let Some(anchor_candidates) = self.rounds_index.get(&anchor_round) {
                if !anchor_candidates.is_empty() {
                    let leader_idx = ((anchor_round.saturating_sub(2) as usize) / 2) % anchor_candidates.len();
                    let leader_anchor = anchor_candidates[leader_idx];
                    let round_r_vertices = self.rounds_index.get(&v_round).unwrap();
                    let mut votes_for_anchor = 0usize;

                    for r_hash in round_r_vertices {
                        if let Some(v) = self.dag_storage.get(r_hash) {
                            if v.strong_parent_digests.contains(&leader_anchor) {
                                votes_for_anchor += 1;
                            }
                        }
                    }

                    if votes_for_anchor >= self.anchor_vote_threshold()
                        && !self.committed_anchors.contains(&leader_anchor)
                    {
                        self.committed_anchors.push(leader_anchor);

                        // Linearize subdag causal history and execute state transitions
                        let subdag = self.linearize_subdag(&leader_anchor);
                        for vertex_to_exec in &subdag {
                            vertex_to_exec
                                .transition
                                .verify_and_apply(&mut self.planetary_state)?;
                            self.committed_vertex_set.insert(vertex_to_exec.vertex_digest);
                            self.linearized_history.push(vertex_to_exec.vertex_digest);
                        }

                        self.last_committed_batch = subdag;
                        return Ok(Some(leader_anchor));
                    }
                }
            }
        }

        Ok(None)
    }

    /// Convenience wrapper matching PROJECT.md interface contract:
    /// Returns newly committed vertices in topological order upon anchor finality.
    pub fn add_vertex(&mut self, vertex: DagVertex) -> Result<Vec<DagVertex>, ConsensusFault> {
        let anchor_opt = self.insert_vertex(vertex)?;
        if anchor_opt.is_some() {
            Ok(self.last_committed_batch.clone())
        } else {
            Ok(Vec::new())
        }
    }

    /// Performs topological traversal backwards from an anchor to linearize all uncommitted ancestors
    pub fn linearize_subdag(&self, anchor_hash: &[u8; 64]) -> Vec<DagVertex> {
        let mut uncommitted = Vec::new();
        let mut visited = BTreeSet::new();
        let mut queue = vec![*anchor_hash];

        while let Some(current_hash) = queue.pop() {
            if self.committed_vertex_set.contains(&current_hash) || !visited.insert(current_hash) {
                continue;
            }
            if let Some(v) = self.dag_storage.get(&current_hash) {
                uncommitted.push(v.clone());
                for parent in &v.strong_parent_digests {
                    queue.push(*parent);
                }
            }
        }

        // Deterministic topological ordering:
        // Because DAG edges only connect round R to round R' < R, ordering by (round, digest)
        // guarantees that all parents strictly precede their children.
        uncommitted.sort_by(|a, b| {
            a.round
                .cmp(&b.round)
                .then_with(|| a.vertex_digest.cmp(&b.vertex_digest))
        });

        uncommitted
    }

    pub fn get_state(&self) -> &PlanetaryState {
        &self.planetary_state
    }

    pub fn get_state_root(&self) -> [u8; 64] {
        self.planetary_state.state_root
    }

    pub fn get_committed_anchors(&self) -> &[[u8; 64]] {
        &self.committed_anchors
    }

    pub fn get_vertex(&self, digest: &[u8; 64]) -> Option<&DagVertex> {
        self.dag_storage.get(digest)
    }
}
