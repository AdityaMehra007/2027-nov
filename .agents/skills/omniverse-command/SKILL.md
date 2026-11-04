---
name: omniverse-command
description: Master control orchestrator for CASHFLOW INFINITY: OMNIVERSE. Use to inspect platform status, view global financial ledgers, and coordinate cross-division agent directives.
---

# CASHFLOW INFINITY: OMNIVERSE Command Orchestrator

The supreme operational command skill for managing the dual-core institutional OS inside Google Antigravity. Unifies Core Alpha (Autonomous Agency, Vectorized Quant Lab, Monte Carlo VaR, RTGS Clearing) and Core Beta (Planetary Mesh, PBFT Consensus, Sentinel-1 SAR Radar Flood Mapping, Crisis Logistics ERP).

## When to Use
- When the user asks "check omniverse status", "show omniverse health", "run benchmark", "launch tui", or "run omniverse command".
- To coordinate work across Autonomous Agency, Financial Intelligence, Aether Planetary Mesh, and Autonomous Evolution divisions.

## Command Line Interface (CLI) Master Reference

All commands are run using `python -m omniverse.cli <command>`.

### 1. Cyberpunk Terminal UI (TUI)
Real-time ASCII terminal dashboard displaying RTGS status, quant metrics, mesh consensus, and live logs:
```powershell
python -m omniverse.cli tui --refresh-rate 1.0
```

### 2. High-Throughput Institutional Benchmarks
Run multi-threaded benchmarks across PBFT consensus, Black-Scholes Greeks, SAR radar ingestion, and RTGS clearing:
```powershell
python -m omniverse.cli benchmark --iterations 5
```

### 3. Quantitative Derivatives & Triangular Arbitrage
Compute analytical Black-Scholes option pricing, full Greeks ($\Delta, \Gamma, \Theta, \mathcal{V}, \rho$), and FX/Crypto triangular cross-rate arbitrage:
```powershell
python -m omniverse.cli derivatives --spot 100 --strike 105 --rate 0.05 --vol 0.20 --time 0.5
```

### 4. Sentinel-1 SAR Radar Flood Detection
Simulate orbital radar backscatter processing with 2D Gaussian speckle filtering, Otsu bimodal valley thresholding, and WGS84 geo-inundation polygon generation:
```powershell
python -m omniverse.cli sar-flood --grid-size 64
```

### 5. Planetary PBFT Consensus Engine
Execute 4-phase Byzantine Fault Tolerant consensus across a 6-continent mesh, validating 3f+1 resilience with simulated malicious nodes:
```powershell
python -m omniverse.cli pbft-consensus --nodes 4 --faulty 1
```

### 6. Self-Healing AST Code Auditor
Run static AST analysis, docstring validation, complexity scoring, and automatic healing on the codebase:
```powershell
python -m omniverse.cli self-heal --path src/omniverse
```

### 7. FastAPI Interactive Command Center & WebSocket Stream
Launch the institutional REST API and live dashboard:
```powershell
python -m omniverse.cli serve --host 127.0.0.1 --port 8888
```
- Interactive Swagger docs: `http://127.0.0.1:8888/docs`
- Live UI Dashboard: `http://127.0.0.1:8888/dashboard`

## Safety Boundaries & Institutional Governance
- `SecurityGovernor`: Live capital transfers above institutional thresholds ($10,000 USD) require cryptographic air-gapped human sign-off.
- All live outbound communications require verified customer review.
- Automated tests must maintain 100% pass rate (`pytest -q`).
