# Original User Request

## Initial Request — 2026-11-07T16:01:15Z

Build and test the complete 32-Engine Monorepo line-by-line across Python solvers, Rust DAG consensus, C++23 RTOS, Verilog RTL, and automated verification suites for production.

Working directory: e:\2027 nov
Integrity mode: development

Reference material: Google AI Studio session context from `e:\2027 nov\parsed_content.md` and `e:\2027 nov\prompt_download.json` (PROJECT AETHER-OMEGA 2027 and 32-Engine Universal Singularity & Bicentennial Omniverse).

## Requirements

### R1. Multi-Agent Swarm Runtime, Physics Solvers & PINN
Build and test the multi-agent swarm runtime and mathematical skills in `src/agents/swarm_runtime.py` featuring a cryptographic DAG message bus (SHA3-512), role-based access control (RBAC), and 4 mathematical skills: Spectral 2D MHD solver with RK4 Orszag-Tang vortex, Ising Hamiltonian ground state optimizer, Relativistic J2 orbital laser ephemeris, and Continuous-Time Algebraic Lyapunov stability verifier (A^T P + P A = -Q). Define the 5 Pantheon Agent prompts and contracts in `prompts/pantheon_system_prompts.yaml` (CHRONOS-PRIME, HELIOS-MHD, GAIA-NAVIER, Q-SHOR-SHIELD, AEGIS-FORMAL). Implement the 3D Magnetohydrodynamics + Navier-Stokes fluid PDE residuals using PyTorch autograd in `src/pinn/navier_stokes_mhd_pinn.py`.

### R2. Byzantine DAG Consensus & Post-Quantum Wire Protocol
Implement asynchronous Byzantine DAG consensus and wire protocol in Rust (`src/kernel/aether_core.rs` and `planetary_node.rs`), including asynchronous DAG vertex ordering, SHA3-512 state verification, and CRYSTALS-Kyber post-quantum key encapsulation abstractions. Provide standalone syntax and simulation verification runners when native Rust cargo toolchains are not available locally.

### R3. Hard Real-Time RTOS, Quantum Circuitry & Hardware RTL
Develop the C++23 zero-allocation magnetic coil confinement controller with Lawson criterion ignition check and Lyapunov non-linear stabilization loop in `src/rtos/fusion_orbital_rtos.hpp` and `src/cislunar/mass_driver_mpc.hpp`. Implement OpenQASM 3.0 rotated surface code (d=7) syndrome extraction and stabilizer lattice in `src/qpu/surface_code_vqe.qasm`, and SystemVerilog RTL for RISC-V systolic tensor ISA in `src/silicon/prometheus_tensor_isa.sv` and neuromorphic STDP crossbar in `src/neuromorphic/stdp_crossbar_core.sv`, with standalone syntax and verification runners where hardware toolchains are not installed locally.

### R4. The 32 Universal Engines
Construct and integrate all 32 Universal Engines in `prometheus_universal_genesis.py` and `src/omni_corp_engine.py`. This includes Engines 1–25 (such as TrueTime HLC, Stripe Ledger, L3 HFT Order Book, Raft/Kafka distributed log, and PagedAttention KV-Cache) and Engines 26–32 (DPLL SAT Theorem Prover, Symbolic Regression AI Physicist, Bytecode Compiler & Stack VM, Autograd engine from scratch, Einstein 4D geodesic solver, FLRW cosmological integrator, and VCG combinatorial auction).

### R5. Automated Verification Harness & Offline Environment Constraints
Implement a comprehensive automated test suite and verification harness under `tests/` verifying all 32 engines, mathematical convergence, formal stability eigenvalues, and zero-fault tolerance. All implementation, execution, and tests must operate in a self-contained, offline environment without requiring external network access or live third-party API credentials.

## Acceptance Criteria

### Multi-Agent Swarm, Skills & PINN
- [ ] `src/agents/swarm_runtime.py` implements SHA3-512 DAG message bus, RBAC, and all 4 mathematical skills (Spectral 2D MHD, Ising Hamiltonian, Relativistic J2, Lyapunov formal verifier).
- [ ] `prompts/pantheon_system_prompts.yaml` defines contracts and system prompts for CHRONOS-PRIME, HELIOS-MHD, GAIA-NAVIER, Q-SHOR-SHIELD, and AEGIS-FORMAL.
- [ ] `src/pinn/navier_stokes_mhd_pinn.py` computes 3D MHD and Navier-Stokes PDE residuals via PyTorch autograd.

### Byzantine DAG Consensus & Wire Protocol
- [ ] `src/kernel/aether_core.rs` and `planetary_node.rs` define asynchronous vertex ordering, SHA3-512 state checks, and CRYSTALS-Kyber KEM abstractions.
- [ ] Consensus and protocol logic pass automated tests, using native cargo where available or standalone simulation runner when cargo is absent.

### Real-Time RTOS, Quantum & Silicon RTL
- [ ] `src/rtos/fusion_orbital_rtos.hpp` and `src/cislunar/mass_driver_mpc.hpp` provide zero-heap-allocation controller interfaces, Lawson criterion ignition checks, and Lyapunov stability loops.
- [ ] `src/qpu/surface_code_vqe.qasm` contains valid OpenQASM 3.0 syntax for rotated surface code (d=7) syndrome extraction.
- [ ] `src/silicon/prometheus_tensor_isa.sv` and `src/neuromorphic/stdp_crossbar_core.sv` contain valid SystemVerilog RTL modules verified by native simulator or standalone syntax verifier.

### 32 Universal Engines
- [ ] `prometheus_universal_genesis.py` and `src/omni_corp_engine.py` implement all 32 engines (Engines 1–25 including TrueTime HLC, Stripe Ledger, L3 HFT Order Book, Raft/Kafka log, PagedAttention KV-Cache; Engines 26–32 including DPLL SAT solver, Symbolic Regression AI Physicist, Bytecode VM, autograd engine, Einstein geodesic solver, FLRW integrator, and VCG auction).
- [ ] Each of the 32 engines exposes an executable interface capable of processing deterministic inputs and producing verifiable outputs.

### Automated Test Suite & Environment
- [ ] Automated test files in `tests/` execute against all 32 engines and core components.
- [ ] Tests verify numerical convergence, stability eigenvalues (A^T P + P A = -Q), and zero-fault tolerance.
- [ ] All tests execute and pass completely offline without external network or external service dependencies.
