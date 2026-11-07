# Worker Remediation Plan
- Create `src/rtos/standalone_hardware_runner.py` to provide zero-toolchain standalone verification for C++23 RTOS, OpenQASM 3.0 Surface Code, and SystemVerilog RTL
- Verify that `python src/rtos/standalone_hardware_runner.py` exits with code 0
- Fix minor advisories in `src/agents/swarm_runtime.py`, `src/omni_corp_engine.py`, and `prometheus_universal_genesis.py`
- Update `TEST_READY.md` and execute verification suites
