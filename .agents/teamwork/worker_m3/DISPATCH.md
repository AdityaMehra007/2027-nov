## 2026-11-07T16:15:36Z
You are `worker_m3`, a `teamwork_worker` agent.
Your working directory: `e:\2027 nov\.agents\teamwork\worker_m3\`
Authoritative request file: `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`
Project scope document: `e:\2027 nov\.agents\teamwork\PROJECT.md`
Detailed specification: `e:\2027 nov\.agents\teamwork\survey_miner_2\survey_r2_r3_spec.md`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusive Write Ownership:
- `src/rtos/fusion_orbital_rtos.hpp`
- `src/cislunar/mass_driver_mpc.hpp`
- `src/qpu/surface_code_vqe.qasm`
- `src/silicon/prometheus_tensor_isa.sv`
- `src/neuromorphic/stdp_crossbar_core.sv`
- `tests/test_rtos_quantum_rtl.py`
You MUST NOT write to any files outside these paths (except in your own working directory `e:\2027 nov\.agents\teamwork\worker_m3\`).

Task Description (Milestone 3):
Implement Requirement 3:
1. `src/rtos/fusion_orbital_rtos.hpp`:
   - C++23 zero-allocation magnetic coil confinement controller (`StaticMatrix` template class on stack).
   - Lawson criterion triple product ignition check ($n_e \cdot T_i \cdot \tau_E \ge 3.0 \times 10^{21}\text{ m}^{-3}\text{keV s}$) and REBCO quench thermal interlock ($T \ge 18.5\text{ K}$).
   - 100ns LQR state-space tearing mode stabilization loop, 18-coil spatial harmonic decomposition, and Bradley point-ahead lead angle.
2. `src/cislunar/mass_driver_mpc.hpp`:
   - Lunar Mass Driver Model Predictive Controller on a 40km electromagnetic launch track.
   - $2375.01\text{ m/s}$ $L_1$ injection velocity targeting, LSM synchronous frequency modulation, Lorentz thrust, and Halbach gap magnetic damping.
3. `src/qpu/surface_code_vqe.qasm`:
   - Valid OpenQASM 3.0 rotated surface code syndrome extraction lattice ($d=3$ and $d=7$ scaling).
   - NW-ES CNOT entangling schedule, mid-circuit projective measurement, feedforward Pauli frame corrections, and QAOA Ising evolution.
4. `src/silicon/prometheus_tensor_isa.sv`:
   - Synthesizable SystemVerilog (IEEE 1800-2017) RISC-V systolic tensor processing element (`prometheus_systolic_tensor_pe`).
   - 64-bit accumulator, fused single-cycle multiply-accumulate (MMA), reversible Landauer-safe Toffoli CCNOT ALU, and parametric ReLU clipping.
5. `src/neuromorphic/stdp_crossbar_core.sv`:
   - Synthesizable SystemVerilog neuromorphic spike-timing-dependent plasticity core (`lif_stdp_neuron_core`).
   - Multiplierless Leaky Integrate-and-Fire (LIF) membrane equation, exponential eligibility trace decay, and Hebbian STDP long-term potentiation / depression.
6. Standalone syntax and simulation verification runner in `tests/test_rtos_quantum_rtl.py`:
   - Complete Python AST and cycle-accurate simulation runner testing C++23, OpenQASM 3.0, and SystemVerilog RTL modules offline.
   - Run `pytest tests/test_rtos_quantum_rtl.py -v` using `run_command` and ensure 100% pass rate.
