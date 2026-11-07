## 2026-11-07T16:15:14Z
You are `worker_m1`, a `teamwork_worker` agent.
Your working directory: `e:\2027 nov\.agents\teamwork\worker_m1\`
Authoritative request file: `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`
Project scope document: `e:\2027 nov\.agents\teamwork\PROJECT.md`
Detailed specification: `e:\2027 nov\.agents\teamwork\survey_miner_1\survey_r1_spec.md`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusive Write Ownership:
- `src/agents/swarm_runtime.py`
- `prompts/pantheon_system_prompts.yaml`
- `src/pinn/navier_stokes_mhd_pinn.py`
- `tests/test_swarm_and_pinn.py`
You MUST NOT write to any files outside these paths (except in your own working directory `e:\2027 nov\.agents\teamwork\worker_m1\`).

Task Description (Milestone 1):
Implement Requirement 1:
1. `src/agents/swarm_runtime.py`:
   - Cryptographic DAG message bus (`DAGVertex`, `PlanetaryDAGLedger`) with canonical SHA3-512 hashing (128 hex chars) and genesis root (`0`*128).
   - Role-Based Access Control (`PlanetarySkillRegistry`, clearance levels 1–10) enforcing clearance on invocation and exporting tool manifests.
   - Autonomous agent node (`AutonomousAgentNode`) executing skills and committing vertices to the DAG.
   - 4 mathematical skills:
     a) Spectral 2D MHD solver with RK4 Orszag-Tang vortex initial state, Fourier pseudo-spectral derivatives, 2/3 de-aliasing rule, and Poisson inversion.
     b) Ising Hamiltonian ground state optimizer ($H = \sum J_{ij} Z_i Z_j + \sum h_i Z_i$) over all spin states with spectral gap $\Delta E$ calculation.
     c) Relativistic J2 orbital laser ephemeris (secular RAAN precession, Bradley aberration point-ahead lead angle, and GR/SR clock drift).
     d) Continuous-Time Algebraic Lyapunov stability verifier ($A^T P + P A = -I$) checking Hurwitz stability of $A$ and positive definiteness of $P$, emitting `COMMIT_APPROVED` or `EMERGENCY_SCRAM_VETO`.
   - `run_planetary_swarm_cycle()` async entrypoint orchestrating a full multi-round swarm cycle.
2. `prompts/pantheon_system_prompts.yaml`:
   - Define contracts and system prompts for all 5 Pantheon Agents: `CHRONOS-PRIME` (clearance 10), `HELIOS-MHD` (clearance 9), `GAIA-NAVIER` (clearance 8), `Q-SHOR-SHIELD` (clearance 9), and `AEGIS-FORMAL` (clearance 10).
3. `src/pinn/navier_stokes_mhd_pinn.py`:
   - Compute 3D Magnetohydrodynamics + Navier-Stokes fluid PDE residuals using PyTorch autograd.
   - Divergence-free vector potential parameterization ($\mathbf{u} = \nabla \times \mathbf{A}_{\text{fluid}}, \mathbf{B} = \nabla \times \mathbf{A}_{\text{mag}}$).
   - Include graceful offline NumPy/analytical verification fallback so tests succeed even if torch is not installed locally.
4. `tests/test_swarm_and_pinn.py`:
   - Comprehensive test suite covering SHA3-512 DAG immutability, tampering detection, RBAC clearance enforcement, Spectral 2D MHD solver, Ising optimizer, J2 ephemeris, Lyapunov verifier, YAML prompt schema, and PINN residuals.
   - Run `pytest tests/test_swarm_and_pinn.py -v` using `run_command` and ensure 100% pass rate.
