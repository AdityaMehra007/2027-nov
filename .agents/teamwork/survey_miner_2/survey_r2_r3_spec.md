# SPECIFICATION: Requirements 2 & 3 (Rust DAG Consensus, Post-Quantum Wire Protocol, C++23 RTOS, OpenQASM 3.0, SystemVerilog RTL)

**Author**: `survey_miner_2` (Teamwork Specification Miner)  
**Date**: 2026-11-07  
**Scope**: Requirements 2 & 3 from `ORIGINAL_REQUEST.md` (Project AETHER-OMEGA 2027)  
**Authoritative References**: `parsed_content.md`, `prompt_download.json`, and local workspace environment.

---

## 1. Executive Summary & Architecture Overview

Requirements 2 and 3 form the foundational systems engineering backbone of the AETHER-OMEGA 2027 platform:
1. **Requirement 2 (Distributed Core & Network Fabric)**: Implements a high-throughput, low-latency Byzantine Fault-Tolerant (BFT) Directed Acyclic Graph (DAG) consensus engine (Bullshark/Narwhal protocol) and post-quantum cryptographic mesh in Rust (`src/kernel/aether_core.rs` and `src/kernel/planetary_node.rs`). It guarantees bit-for-bit deterministic state transitions across heterogeneous architectures (x86_64, ARM64, RISC-V) via fixed-point math (`i128`), SHA3-512 state digests, and NIST FIPS 203/204 CRYSTALS-Kyber/Dilithium envelope abstractions.
2. **Requirement 3 (Hard Real-Time Control, Quantum Computing & Custom Silicon)**:
   - **RTOS & Cislunar MPC** (`src/rtos/fusion_orbital_rtos.hpp` & `src/cislunar/mass_driver_mpc.hpp`): C++23 zero-heap-allocation, hard real-time controllers executing sub-microsecond control loops. Features Lawson criterion triple-product ignition verification, non-linear Lyapunov / LQR state-space magnetic coil stabilization with spatial harmonics, superconducting quench interlocks, relativistic Bradley point-ahead laser corrections, and lunar mass driver Linear Synchronous Motor (LSM) commutation.
   - **Fault-Tolerant Quantum Circuitry** (`src/qpu/surface_code_vqe.qasm`): OpenQASM 3.0 rotated surface code syndrome extraction lattice ($d=3$ patch and generalized $d=7$ scaling) with mid-circuit non-demolition projective measurements, real-time hardware Pauli frame feedforward corrections, and QAOA/VQE Ising Hamiltonian layers.
   - **Custom Hardware RTL** (`src/silicon/prometheus_tensor_isa.sv` & `src/neuromorphic/stdp_crossbar_core.sv`): Synthesizable IEEE 1800-2017 SystemVerilog RTL providing a 64-bit systolic tensor processing element with reversible Toffoli ALU, and a neuromorphic Leaky Integrate-and-Fire (LIF) neuron core with on-chip Spike-Timing-Dependent Plasticity (STDP) learning.
   - **Self-Contained Verification**: Since local Windows environments may lack C++ compilers (`g++`, `clang++`) or RTL simulators (`verilator`, `iverilog`), comprehensive standalone Python-based AST syntax verifiers and cycle-accurate simulation runners are formally specified to ensure complete offline zero-fault test execution.

---

## 2. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | R2: Consensus | Bullshark BFT DAG Engine | Asynchronous DAG consensus with even-round leader anchor commits and $2f+1$ parent quorum threshold. | `DagVertex` with round, parents, transitions, and PQC envelope. | `Result<Option<[u8; 64]>, ConsensusFault>` (anchor commit hash). | Returns `ConsensusFault::InsufficientByzantineQuorum`, `OrphanParentVertex`, etc. | `parsed_content.md:59310` |
| 2 | R2: Consensus | Deterministic Canonical Digest | FNV-1a / Sponge-64 deterministic hashing over author, round, parents, and state transition. | Author ID, round, parent digests, `PlanetaryStateTransition`. | `[u8; 64]` canonical digest. | Mismatch triggers `InvalidPostQuantumSignature`. | `parsed_content.md:59345` |
| 3 | R2: Consensus | Deterministic Power Math | Fixed-point `i128` representation (`DeterministicMicroWatts`) in $10^{-6}$ W. | Integer microwatt energy delta. | Exact deterministic balance across architectures. | Overflow / Underflow checked via standard integer bounds. | `parsed_content.md:59315` |
| 4 | R2: Crypto | Post-Quantum Wire Envelope | NIST FIPS 203/204 envelope wrapping Kyber-1024 ciphertext and Dilithium-5 signatures. | Sender node ID, Kyber CT (1568 B), Dilithium sig (4595 B), Blake3/SHA3 digest. | Authenticated `PostQuantumEnvelope` struct. | Tampered digest rejected during vertex insertion. | `parsed_content.md:59320` |
| 5 | R2: Node | Planetary Kernel Node | Asynchronous Tokio node managing node types, local peer ledger, and telemetry heartbeats. | Node ID, `NodeType` enum, async `mpsc::Sender<TelemetryPacket>`. | Async heartbeat packet broadcast, updated ledger. | Returns `Err(String)` on channel failure or system time error. | `parsed_content.md:4273` |
| 6 | R2: Node | SHA3-512 State Hash | Cryptographic quantum-resistant hashing of telemetry packets. | Node ID, timestamp nanoseconds, energy surplus, compute load. | `[u8; 64]` SHA3-512 digest. | Mismatch logs critical Byzantine fault alert and excludes packet from grid balance. | `parsed_content.md:4315` |
| 7 | R2: Node | Global Energy Grid Balance | Verifies hash integrity for all node telemetry and calculates net planetary energy surplus. | Local zero-trust peer ledger. | Net energy surplus in MW (`f64`). | Byzantine packets logged to `eprintln!` and skipped from sum. | `parsed_content.md:4350` |
| 8 | R3: RTOS | Zero-Heap StaticMatrix Math | Stack-allocated compile-time matrix structure and unrolled matrix-vector multiplication. | `StaticMatrix<R, C>` and vector `std::array<double, C>`. | Transformed vector `std::array<double, R>`. | Enforces zero heap allocations, zero exceptions, zero RTTI. | `parsed_content.md:68870` |
| 9 | R3: RTOS | Lawson Triple Product Check | Evaluates D-T plasma self-sustaining fusion ignition condition $n_e \cdot T_i \cdot \tau_E \ge 3.0 \times 10^{21}\text{ m}^{-3}\text{keV s}$. | `TokamakSensorFrame` (electron density, ion temperature, confinement time). | `bool` (`true` if ignited / net positive). | Returns `false` if below Lawson ignition criterion threshold. | `parsed_content.md:323, 68880` |
| 10 | R3: RTOS | Superconducting Quench Interlock | Safety-critical shutdown if REBCO coil temperature $\ge 18.5\text{ K}$ or island width $\ge 0.12\text{ m}$. | `TokamakSensorFrame` coil temperature and island width. | `ActuatorCommandFrame` with `EMERGENCY_MASSIVE_GAS_INJECTION_SCRAM`. | Immediately zeroes gyrotron power and trips hardware interlock state. | `parsed_content.md:68940` |
| 11 | R3: RTOS | State-Space LQR & Lyapunov Control | 100ns feedback loop suppressing $m=2, n=1$ neoclassical tearing modes via optimal gain matrix $K_{lqr}$. | Sensor state error $[w, \dot{w}]^T$. | Feedback control vector $u = -K x$ driving ECCD power (0..50 MW). | Output clamped to safe physical limits ($[0, 50]\text{ MW}$). | `parsed_content.md:68950` |
| 12 | R3: RTOS | Spatial Harmonic Modulation | Distributes magnetic flux trim across 18 superconducting toroidal coils using resonant perturbation. | Control signal $u_1$, coil index $i \in [0, 17]$. | Coil trim current in kA clamped to $[-25.0, +25.0]\text{ kA}$. | Clamping prevents superconducting magnet quench. | `parsed_content.md:68960` |
| 13 | R3: RTOS | Relativistic Bradley Aberration | Computes point-ahead angle for orbital laser synchronization: $\theta = \frac{2 v_{\text{rel}}}{c} \times 10^6\text{ }\mu\text{rad}$. | Relative orbital velocity $v_{\text{rel}}$ in km/s. | Lead angle in microradians (`f64`). | Pure kinematic function bounded by speed of light. | `parsed_content.md:68970` |
| 14 | R3: Cislunar | Lunar Mass Driver LSM MPC | Microsecond linear synchronous motor commutation along 40 km lunar track to $L_1$ injection velocity. | `SledTelemetry` (position, velocity, levitation gap, coil temp), payload mass. | `StatorCoilCommand` (scram flag, frequency, phase current, damping). | Sled contact ($\text{gap} < 3\text{ mm}$) or quench ($T > 77\text{ K}$) triggers eddy brake scram. | `parsed_content.md:267419` |
| 15 | R3: QPU | Rotated Surface Code QEC | OpenQASM 3.0 syndrome extraction subroutine on rotated lattice with NW-ES CNOT scheduling. | 9 data qubits, 4 X-ancillas, 4 Z-ancillas (or 49 data / 48 ancillas for $d=7$). | Syndrome bits `sx[4]`, `sz[4]` via mid-circuit measurement. | Measurement triggers real-time Pauli frame feedforward corrections. | `parsed_content.md:74202` |
| 16 | R3: QPU | Hardware Feedforward Correction | Conditional Pauli-X and Pauli-Z gate application based on mid-circuit syndrome values. | Measurement bits `syndrome_x`, `syndrome_z`. | Corrected logical data qubits. | Inverts detected bit-flip or phase-flip on central data qubit. | `parsed_content.md:74260` |
| 17 | R3: QPU | QAOA/VQE Ising Evolution | Variational Ising $ZZ$ interaction layer and transverse-field mixer layer. | Classical variational parameters `gamma_ising`, `beta_mixer`. | Unitary gate execution over logical qubits and final readout. | Classical optimizer minimizes $\langle \psi | H | \psi \rangle$. | `parsed_content.md:74270` |
| 18 | R3: Silicon | Systolic Tensor Processing Element | Synthesizable 64-bit PE with west-to-east activation and north-to-south weight propagation. | `clk`, `rst_n`, `opcode[1:0]`, `act_in_west`, `weight_in_north`, `q_bits_in`. | `act_out_east`, `weight_out_south`, `acc_out`, `q_bits_out`. | Synchronous active-low reset clears internal accumulator and registers. | `parsed_content.md:339014` |
| 19 | R3: Silicon | Reversible Toffoli ALU | Zero-entropy Landauer-safe CCNOT reversible gate integrated into tensor PE. | Opcode `2'b10`, 3-bit quantum state `q_bits_in`. | Output `q_bits_out` with $q_0 \oplus (q_2 \land q_1)$. | Preserves thermodynamic information entropy. | `parsed_content.md:339045` |
| 20 | R3: Neuromorphic | LIF Neuron with On-Chip STDP | Leaky Integrate-and-Fire neuron with exponential eligibility trace and Hebbian LTP learning. | `clk`, `rst_n`, `pre_synaptic_spike`, `external_current`. | `post_synaptic_spike`, `synaptic_weight`. | Clamped at max weight (`16'sd1024`) to prevent runaway potentiation. | `parsed_content.md:264651` |
| 21 | Verification | Standalone Verification Suite | Python AST syntax parsers and cycle-accurate simulators for Rust, C++23, OpenQASM, and Verilog. | Source files (`.rs`, `.hpp`, `.qasm`, `.sv`). | Test execution reports, exit codes, assertion logs. | Reports exact syntax errors, semantic violations, and numerical divergence. | ORIGINAL_REQUEST R2 & R3 |

---

## 3. Detailed Technical Specifications

### 3.1 Requirement 2: Byzantine DAG Consensus & Post-Quantum Wire Protocol

#### 3.1.1 `src/kernel/aether_core.rs`
- **Compiler Requirements**: Native `rustc --edition=2021` or `cargo`. Zero external crate dependencies required for compilation (uses standard library `collections`, `fmt`, and deterministic bitwise logic).
- **Core Abstractions**:
  ```rust
  pub type DeterministicMicroWatts = i128;

  #[derive(Clone, Debug, PartialEq, Eq)]
  pub struct PostQuantumEnvelope {
      pub sender_node_id: [u8; 32],
      pub kyber1024_ciphertext: Vec<u8>,   // 1568 bytes ML-KEM-1024
      pub dilithium5_signature: Vec<u8>,   // 4595 bytes ML-DSA-87
      pub blake3_state_digest: [u8; 64],
  }

  #[derive(Clone, Debug, PartialEq, Eq)]
  pub struct PlanetaryStateTransition {
      pub epoch_round: u64,
      pub timestamp_tai_ns: u128,
      pub net_energy_delta_uw: DeterministicMicroWatts,
      pub tokamak_quench_flags: u32,
      pub orbital_laser_azimuth_urad: i64,
  }

  #[derive(Clone, Debug)]
  pub struct DagVertex {
      pub vertex_digest: [u8; 64],
      pub author_id: [u8; 32],
      pub round: u64,
      pub strong_parent_digests: Vec<[u8; 64]>,
      pub transition: PlanetaryStateTransition,
      pub pqc_envelope: PostQuantumEnvelope,
  }
  ```
- **Algorithms**:
  1. **Canonical Sponge Digest Calculation**:
     - Accumulator initialized to FNV offset basis: `0xcbf29ce484222325`.
     - Byte-by-byte mixing with FNV prime `0x100000001b3`.
     - Ingests `author_id`, `round.to_le_bytes()`, all parent digests, `timestamp_tai_ns.to_le_bytes()`, and `net_energy_delta_uw.to_le_bytes()`.
     - Finalizes into 64-byte array via 64 round rotations: `acc = acc.rotate_left(7) ^ (i as u64).wrapping_mul(0x9e3779b97f4a7c15)`.
  2. **Bullshark Anchor Finality Rule**:
     - For total validators $N$, fault tolerance is $f = \lfloor(N - 1) / 3\rfloor$.
     - Quorum threshold is $2f + 1$.
     - Vertices in round $R > 1$ must contain $\ge 2f + 1$ strong parents from round $R - 1$, and none can be orphans.
     - When an odd round $R \ge 3$ receives vertices, it evaluates the leader anchor at round $R - 1$.
     - If the round $R - 1$ leader anchor is referenced by $\ge f + 1$ distinct round $R$ vertices, the anchor is irrevocably finalized into `committed_anchors`.
  3. **Topological Vertex Linearization**:
     - Causal history is ordered by traversing backwards from committed anchors, ensuring a total, strictly deterministic ordering of all planetary state transitions.

#### 3.1.2 `src/kernel/planetary_node.rs`
- **Asynchronous Architecture**:
  - Uses `tokio::sync::RwLock` for zero-contention thread-safe ledger access and `tokio::sync::mpsc` channels for peer packet dissemination.
  - State hashing via SHA3-512 over node ID, nanosecond timestamp, and floating-point telemetry.
  - Zero-trust ledger verification: Every packet stored in the peer ledger is re-verified against its `state_hash` before being incorporated into the global power balance calculation.
- **CRYSTALS-Kyber KEM Interface**:
  ```rust
  pub struct KyberKemKeypair {
      pub public_key: [u8; 1568],  // ML-KEM-1024 public key
      pub secret_key: [u8; 3168],  // ML-KEM-1024 secret key
  }
  pub struct KyberCiphertext {
      pub data: [u8; 1568],
      pub shared_secret: [u8; 32],
  }
  impl KyberKemKeypair {
      pub fn generate() -> Self;
      pub fn encapsulate(&self, peer_pk: &[u8; 1568]) -> KyberCiphertext;
      pub fn decapsulate(&self, ct: &[u8; 1568]) -> Result<[u8; 32], &'static str>;
  }
  ```

---

### 3.2 Requirement 3: Hard Real-Time RTOS, Quantum Circuitry & Hardware RTL

#### 3.2.1 `src/rtos/fusion_orbital_rtos.hpp`
- **Compiler Directives**: C++23 standard, `#pragma once`, zero heap allocation (`StaticMatrix`), `-fno-exceptions -fno-rtti`.
- **Structures & Mathematical Formulations**:
  1. `TokamakSensorFrame`:
     - $n_e \in [10^{19}, 10^{21}]\text{ m}^{-3}$ (electron density)
     - $T_i \in [1.0, 30.0]\text{ keV}$ (ion temperature)
     - $\tau_E \in [0.1, 5.0]\text{ s}$ (energy confinement time)
     - $w \in [0.0, 0.2]\text{ m}$ (magnetic island width, disruption threshold $0.12\text{ m}$)
     - $\dot{w} \in \mathbb{R}$ (island growth rate in m/s)
     - $T_{\text{coil}} \in [4.2, 30.0]\text{ K}$ (REBCO quench ceiling $18.5\text{ K}$)
     - $P_{\text{cryo}} \in \mathbb{R}$ (helium pressure)
  2. **Lawson Criterion Ignition Verification**:
     $$\text{Triple Product } \Pi_{\text{Lawson}} = n_e \cdot T_i \cdot \tau_E$$
     Ignition status is validated if $\Pi_{\text{Lawson}} \ge 3.0 \times 10^{21}\text{ m}^{-3}\text{keV s}$.
  3. **LQR Optimal Feedback & ECCD Power**:
     $$u = -K_{\text{lqr}} \cdot \begin{bmatrix} w \\ \dot{w} \end{bmatrix}, \quad K_{\text{lqr}} = \begin{bmatrix} 42.8 & 11.4 \\ 19.2 & 6.5 \end{bmatrix}$$
     $$\text{Power}_{\text{gyrotron}} = \text{clamp}(u_0, 0.0, 50.0)\text{ MW}$$
  4. **Non-linear Spatial Harmonic Coil Trim**:
     For 18 toroidal/poloidal coils, spatial phase is $\theta_i = \frac{2\pi i}{18}$.
     $$I_{\text{trim}, i} = \text{clamp}\left( -u_1 \cdot \cos(2\theta_i), -25.0, +25.0 \right)\text{ kA}$$
  5. **Relativistic Bradley Aberration Lead Angle**:
     $$\theta_{\text{lead}} = \left( \frac{2 \cdot v_{\text{rel}}}{c} \right) \times 10^6\text{ }\mu\text{rad}, \quad c = 299792.458\text{ km/s}$$

#### 3.2.2 `src/cislunar/mass_driver_mpc.hpp`
- **Constants**:
  - $v_{\text{target}} = 2375.01\text{ m/s}$ (Lunar escape & $L_1$ insertion velocity)
  - $L_{\text{track}} = 40,000.0\text{ m}$
  - $\tau_p = 0.50\text{ m}$ (coil pole pitch)
  - $a_{\text{nom}} = \frac{v_{\text{target}}^2}{2 L_{\text{track}}} \approx 70.51\text{ m/s}^2$ ($\approx 7.19g$)
- **Microsecond Commutation Equations**:
  1. Safety interlocks: if $T_{\text{coil}} > 77.0\text{ K}$ or $\text{gap} < 3.0\text{ mm}$, emergency eddy current brake scram engaged.
  2. Reference kinematic profile: $v_{\text{ref}}(x) = \sqrt{2 a_{\text{nom}} \max(0, x)}$.
  3. Linear Synchronous Motor synchronous frequency:
     $$f_{\text{sync}} = \frac{v}{2 \tau_p} = \frac{v}{1.0} = v\text{ Hz}$$
  4. Lorentz thrust & phase current:
     $$F_{\text{thrust}} = m_{\text{payload}} \cdot \left( a_{\text{nom}} + 12.0(v_{\text{ref}} - v) \right)$$
     $$I_{\text{phase}} = \text{clamp}(F_{\text{thrust}} \times 1.85 \times 10^{-4}, 0.0, 150.0)\text{ kA}$$
  5. Halbach maglev damping force:
     $$F_{\text{damp}} = 4500.0 \times (15.0 - \text{gap}_{\text{mm}})\text{ N}$$

#### 3.2.3 `src/qpu/surface_code_vqe.qasm`
- **OpenQASM 3.0 Grammar**: Strict compliance with OpenQASM 3.0 gate and subroutine specifications.
- **Lattice Topology**:
  - **Distance-3 Patch** ($d=3$):
    - 9 Data qubits: $d[0..8]$ in $3 \times 3$ Cartesian grid.
    - 4 X-ancilla qubits: $ax[0..3]$ for plaquette and boundary $X$-stabilizers.
    - 4 Z-ancilla qubits: $az[0..3]$ for plaquette and boundary $Z$-stabilizers.
    - Total qubits: 17 physical qubits.
  - **Distance-7 Scaling** ($d=7$):
    - Data qubits: $d^2 = 7^2 = 49$ data qubits ($d[0..48]$).
    - Ancilla qubits: $d^2 - 1 = 48$ ancillas (24 X-ancillas, 24 Z-ancillas).
    - Total qubits: $2d^2 - 1 = 97$ physical qubits.
- **Entanglement Scheduling**:
  - CNOT operations executed in strict North $\rightarrow$ West $\rightarrow$ East $\rightarrow$ South order to eliminate fault hook errors.
- **Subroutine Definition**:
  ```qasm
  def extract_surface_code_syndromes(qubit[9] d, qubit[4] ax, qubit[4] az) -> bit[4], bit[4] {
      // resets, Hadamards, CX schedules, measurements
      return sx, sz;
  }
  ```
- **Mid-Circuit Feedforward & Pauli Frame Correction**:
  - `if (syndrome_z[0] == 1 && syndrome_z[1] == 1) { x data_q[4]; }`
  - `if (syndrome_x[0] == 1 && syndrome_x[1] == 1) { z data_q[4]; }`
- **Variational Ising Evolution**:
  - Two-qubit ZZ interaction: `cx`, `rz(2.0 * gamma_ising)`, `cx`.
  - Single-qubit transverse mixer: `rx(2.0 * beta_mixer)`.

#### 3.2.4 `src/silicon/prometheus_tensor_isa.sv`
- **Module Interface**:
  - `module prometheus_systolic_tensor_pe #(parameter int DATA_W = 16, parameter int ACC_W = 64)`
  - Input ports: `clk`, `rst_n`, `opcode[1:0]`, `act_in_west[DATA_W-1:0]`, `weight_in_north[DATA_W-1:0]`, `q_bits_in[2:0]`.
  - Output ports: `act_out_east[DATA_W-1:0]`, `weight_out_south[DATA_W-1:0]`, `acc_out[ACC_W-1:0]`, `q_bits_out[2:0]`.
- **Instruction Set**:
  - `2'b00` (`NOP`): Internal state holds, pass-through systolic registers propagate.
  - `2'b01` (`SYSTOLIC_MMA`): Fused MAC: `acc_out <= acc_out + ($signed(act_in_west) * $signed(weight_in_north))`.
  - `2'b10` (`REV_TOFFOLI`): CCNOT gate: `q_bits_out[2] <= q_bits_in[2]`, `q_bits_out[1] <= q_bits_in[1]`, `q_bits_out[0] <= q_bits_in[0] ^ (q_bits_in[2] & q_bits_in[1])`.
  - `2'b11` (`RELU_CLIP`): Non-linear activation: `acc_out <= (acc_out < 0) ? '0 : acc_out`.

#### 3.2.5 `src/neuromorphic/stdp_crossbar_core.sv`
- **Module Interface**:
  - `module lif_stdp_neuron_core #(parameter int V_WIDTH = 16, parameter signed [15:0] V_REST = -16'sd700, parameter signed [15:0] V_RESET = -16'sd750, parameter signed [15:0] V_THRESH = -16'sd500, parameter int LEAK_SHIFT = 4)`
- **Dynamics**:
  - Eligibility trace exponential decay: `pre_spike_trace <= pre_spike_trace - (pre_spike_trace >> 3) - 8'd1` when idle; resets to `255` on pre-synaptic spike.
  - Multiplierless LIF update:
    $$\text{leak} = (v_{\text{mem}} - V_{\text{REST}}) \ggg \text{LEAK\_SHIFT}$$
    $$v_{\text{next}} = v_{\text{mem}} - \text{leak} + I_{\text{syn}} + I_{\text{ext}}$$
  - Action potential generation and STDP Long-Term Potentiation (LTP):
    - When $v_{\text{next}} \ge V_{\text{THRESH}}$, emit `post_synaptic_spike = 1`, reset $v_{\text{mem}} = V_{\text{RESET}}$.
    - If $\text{trace} > 16$ and $\text{weight} < 1024$, potentiate weight: `synaptic_weight <= synaptic_weight + pre_spike_trace[7:3]`.

---

## 4. Edge Cases & Boundary Conditions

| # | Feature | Input / Condition | Expected / Observed Behavior |
|---|---------|-------------------|-----------------------------|
| 1 | BFT DAG Consensus | Genesis round ($R = 1$) vertices | Strong parent list is empty; bypasses $2f+1$ parent check; accepted as valid genesis. |
| 2 | BFT DAG Consensus | Vertex referencing non-existent parent hash | Fails with `ConsensusFault::OrphanParentVertex`; rejected before storage insertion. |
| 3 | BFT DAG Consensus | Odd round $R \ge 3$ with $< f + 1$ votes for leader anchor | Anchor remains pending; returns `Ok(None)` without finalization until quorum attained. |
| 4 | Post-Quantum Envelope | Modified byte in `kyber1024_ciphertext` or `transition` | Canonical digest mismatch; rejected with `ConsensusFault::InvalidPostQuantumSignature`. |
| 5 | Planetary Kernel | Telemetry packet with forged energy reading | Node recalculates `state_hash`; mismatch detected; excluded from energy grid balance; logs security alert. |
| 6 | Magnetic RTOS | Superconducting coil temp $T_{\text{coil}} = 18.51\text{ K} \ge 18.5\text{ K}$ | Triggers `EMERGENCY_MASSIVE_GAS_INJECTION_SCRAM`; gyrotron power clamped immediately to 0.0 MW. |
| 7 | Magnetic RTOS | Tearing island width $w = 0.125\text{ m} \ge 0.12\text{ m}$ | Disruption lock detected; enters emergency scram state. |
| 8 | Magnetic RTOS | Extreme LQR error demanding $> 50\text{ MW}$ ECCD power | Clamped to hard hardware upper bound of $50.0\text{ MW}$. |
| 9 | Mass Driver MPC | Levitation clearance $\text{gap} = 2.8\text{ mm} < 3.0\text{ mm}$ | Emergency eddy current brake scram enabled to prevent catastrophic rail strike. |
| 10 | Mass Driver MPC | Cryogenic stator temperature $T_{\text{coil}} = 78.2\text{ K} > 77.0\text{ K}$ | Liquid nitrogen boiling / coil quench threshold exceeded; scram triggered. |
| 11 | OpenQASM 3.0 QEC | Simultaneous bit-flip and phase-flip on central data qubit | `syndrome_z[0]==1 && syndrome_z[1]==1` triggers `x data_q[4]`; `syndrome_x` triggers `z data_q[4]`; restores $| \psi \rangle$. |
| 12 | Systolic Tensor PE | Active-low reset asserted (`rst_n == 0`) during ongoing MMA | All output registers (`act_out_east`, `weight_out_south`, `acc_out`, `q_bits_out`) synchronously cleared to 0. |
| 13 | Systolic Tensor PE | Negative accumulator during `RELU_CLIP` opcode (`2'b11`) | Output accumulator clamped strictly to 0 (`acc_out < 0 ? '0 : acc_out`). |
| 14 | LIF STDP Neuron | Synaptic weight reaches maximum ceiling ($16\text{sd1024}$) | Potentiation condition `synaptic_weight < 16'sd1024` evaluates false; prevents arithmetic overflow. |

---

## 5. Verification Strategy & Standalone Verification Runners

### 5.1 Environment Toolchain Status
- **Rust Toolchains**: `rustc 1.98.0` and `cargo 1.98.0` are installed and active at `C:\Users\amehr\.cargo\bin\`.
- **C++ Compilers**: `g++` and `clang++` are not installed locally.
- **Hardware Simulators**: `iverilog` and `verilator` are not installed locally.
- **Python Environment**: Python 3.13 is available with `hashlib` (including standard library `sha3_512`), `numpy`, and `scipy`.

### 5.2 Standalone Verification Runners Specification
To fulfill Acceptance Criteria 38, 41, 42, and 43 completely offline without external toolchain dependencies:
1. **Rust Verification (`tests/verify_rust_kernel.py` & native cargo)**:
   - Direct compilation: Run `rustc --edition=2021 src/kernel/aether_core.rs -o target/aether_core.exe` (or `cargo test` where configured).
   - Standalone simulation: A Python consensus simulation verifying DAG creation, FNV-1a Sponge-64 digest generation, Byzantine quorum checks ($2f+1$), orphan detection, anchor commitment rule ($f+1$ votes), and topological ordering.
2. **C++23 RTOS Verification (`tests/verify_rtos_cplusplus.py`)**:
   - Static syntax & AST validation: Checks `#pragma once`, zero dynamic allocation (`new`, `malloc`, `std::vector`), `constexpr`, `noexcept`, `-fno-exceptions`, `-fno-rtti`.
   - Behavioral & Numerical Simulation:
     - Tests Lawson criterion triple-product ignition threshold ($3.0 \times 10^{21}$).
     - Tests 100ns LQR state-space control loop and spatial harmonic coil modulation.
     - Tests emergency quench interlocks ($T \ge 18.5\text{ K}$, $w \ge 0.12\text{ m}$).
     - Tests Cislunar mass driver kinematic profile, LSM frequency, and Halbach gap damping.
3. **OpenQASM 3.0 Verification (`tests/verify_openqasm.py`)**:
   - OpenQASM 3.0 parser validating qubit declarations (`qubit[9]`, `qubit[4]`, or `qubit[49]`), `input float[64]`, `def` subroutine headers, CNOT entangling schedules, mid-circuit measurements, and feedforward conditionals.
   - Quantum Statevector Simulation: Simulates the Pauli frame update and verifies syndrome extraction correctly identifies bit/phase flips.
4. **SystemVerilog RTL Verification (`tests/verify_systemverilog_rtl.py`)**:
   - IEEE 1800-2017 RTL syntax validator checking module declarations, parameters, always_ff blocks, and synthesizability.
   - Cycle-Accurate Simulator:
     - Simulates `prometheus_systolic_tensor_pe` across opcodes `2'b00` (NOP), `2'b01` (MMA), `2'b10` (Toffoli), `2'b11` (ReLU).
     - Simulates `lif_stdp_neuron_core` verifying exponential trace decay, leaky integration, threshold spike generation, and Hebbian STDP weight potentiation.
5. **Unified Automated Test Suite Integration**:
   - `tests/test_r2_r3_standalone.py` registered with `pytest` to execute all verification runners deterministically and offline with zero exit failures.
