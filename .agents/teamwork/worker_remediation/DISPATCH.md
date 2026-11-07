## 2026-11-07T17:15:14Z
From: 9bac3ec6-38e3-45f9-af49-0c09e63f189d
Priority: MESSAGE_PRIORITY_HIGH

You are the Remediation Worker for PROJECT AETHER-OMEGA 2027 (32-Engine Monorepo).
Your working directory is `e:\2027 nov\.agents\teamwork\worker_remediation\`.

Authoritative request file: `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md` (YOU MUST READ THIS FIRST).
Global project plan: `e:\2027 nov\.agents\teamwork\PROJECT.md`.
Test verification index: `e:\2027 nov\TEST_READY.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Context & Task:
In Gate 1 review, Reviewer 2 requested changes because `TEST_READY.md` lists `python src/rtos/standalone_hardware_runner.py` as an operational standalone verification command for zero-toolchain environments, but `src/rtos/standalone_hardware_runner.py` does not exist on disk!

Your concrete assignments:
1. Create `src/rtos/standalone_hardware_runner.py`:
   - Must implement standalone verification without external toolchains for:
     a) C++23 zero-allocation RTOS headers (`src/rtos/fusion_orbital_rtos.hpp` and `src/cislunar/mass_driver_mpc.hpp`): AST/lexical checking verifying zero dynamic allocations (`new`, `malloc`, `std::vector`), Lawson criterion check ($nT\tau_E \ge 3 \times 10^{21}$), and Mass Driver MPC calculation.
     b) OpenQASM 3.0 Surface Code (`src/qpu/surface_code_vqe.qasm`): syntax and stabilizer parsing for rotated surface code syndrome extraction.
     c) SystemVerilog RTL (`src/silicon/prometheus_tensor_isa.sv` and `src/neuromorphic/stdp_crossbar_core.sv`): cycle-accurate Python simulation verifying systolic matrix multiplication and neuromorphic STDP weight updates ($\Delta w$).
   - When executed with `python src/rtos/standalone_hardware_runner.py`, it must run all simulations, print verifiable verification telemetry, and exit with code 0!
2. Address the minor edge-case advisories identified by Reviewer 1 and Challengers 1 & 2:
   - In `src/agents/swarm_runtime.py`: in `skill_verify_lyapunov()`, catch `NaN`/`Inf` inputs and return `EMERGENCY_SCRAM_VETO` rather than unhandled `LinAlgError`.
   - In `src/omni_corp_engine.py`: in `ConsistentHashRing.get_preference_list()`, ensure `replication_factor <= 0` returns empty list cleanly; in `SpannerTrueTimeHLC`, validate non-negative epsilon.
   - In `prometheus_universal_genesis.py`: in `Engine19_SurfaceCodeQuantumEngine`, ensure distinct syndrome keys for all plaquettes; in `Engine26_AutomatedTheoremProverDPLL`, handle empty clause set input without crashing; in `Engine28_UniversalBytecodeCompilerAndVM`, perform compile-time parenthesis matching.
3. Execute the full test and runner suite:
   - `python src/rtos/standalone_hardware_runner.py` (must exit 0)
   - `python src/kernel/standalone_runner.py` (must exit 0)
   - `python prometheus_universal_genesis.py` (must exit 0)
   - `python -m pytest tests/test_swarm_and_pinn.py tests/test_kernel_consensus.py tests/test_rtos_quantum_rtl.py tests/test_omni_corp_engine.py tests/test_prometheus_universal_genesis.py tests/test_universal_engines_32.py tests/test_numerical_stability_lyapunov.py tests/test_offline_master_verification.py -v` (all 139+ tests must pass)
4. Update `TEST_READY.md` to reflect the operational standalone hardware runner.
5. Write your complete handoff report in `e:\2027 nov\.agents\teamwork\worker_remediation\handoff.md` and send completion message via `send_message` back to the orchestrator.
