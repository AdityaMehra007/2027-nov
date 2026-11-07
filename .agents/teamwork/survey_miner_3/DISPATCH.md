## 2026-11-07T16:05:01Z
You are `survey_miner_3`, a `teamwork_spec_miner` agent.
Your working directory: `e:\2027 nov\.agents\teamwork\survey_miner_3\`
Authoritative request file: `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`

Your mission:
Survey and mine exact specifications, definitions, inputs/outputs, and test expectations for Requirements 4 and 5:
R4. The 32 Universal Engines:
- Construct and integrate all 32 Universal Engines in `prometheus_universal_genesis.py` and `src/omni_corp_engine.py`.
- Enumerate every single engine (1 through 25, and 26 through 32):
  Engines 1–25: TrueTime HLC, Stripe Ledger, L3 HFT Order Book, Raft/Kafka distributed log, PagedAttention KV-Cache, and others.
  Engines 26–32: DPLL SAT Theorem Prover, Symbolic Regression AI Physicist, Bytecode Compiler & Stack VM, Autograd engine from scratch, Einstein 4D geodesic solver, FLRW cosmological integrator, VCG combinatorial auction.
- Identify the exact names, expected classes, interfaces, deterministic inputs, and verifiable outputs for each of the 32 engines.

R5. Automated Verification Harness & Offline Environment Constraints:
- Automated test files in `tests/` executing against all 32 engines and core components.
- Verification of numerical convergence, stability eigenvalues (A^T P + P A = -Q), and zero-fault tolerance.
- Offline constraints: must execute and pass completely offline without external network or external service dependencies.

Instructions:
1. Read `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`.
2. Inspect `e:\2027 nov\parsed_content.md` and `e:\2027 nov\prompt_download.json` for all sections mentioning the 32 Universal Engines, prometheus_universal_genesis, omni_corp_engine, and tests.
3. Check existing files in `prometheus_universal_genesis.py`, `src/omni_corp_engine.py`, and `tests/` to see what is already implemented, partially implemented, or missing.
4. Record your findings, exact engine inventory table (Engine #, Name, Class/Function signature, Deterministic inputs, Verifiable outputs), and test harness specs into:
   `e:\2027 nov\.agents\teamwork\survey_miner_3\survey_r4_r5_spec.md`
   and write a standard `handoff.md` in your working directory.
5. Send a completion message back to the orchestrator. Do not edit source code. Only write to your working directory.
