# Knowledge Item (KI): Tier-1 Enterprise Architectural Conventions & Operating Procedures
## CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC

### 1. Inviolable Architectural Principles
- **Zero-Placeholder Law**: No `// TODO`, `// FIXME`, mock returns, or stubbed endpoints in production paths. Every API route, model, and CLI command must be backed by a functional, tested implementation.
- **Evidence Before Claims**: 100% green test suite required before committing or claiming completion.
- **Strict Financial Distinction**: Pipeline Value (speculative) != Collected Revenue (cleared bank / on-chain settled funds).
- **Dual-Key Security Gating**: Any financial movement exceeding thresholds or outbound communications requires HMAC-SHA256 human-in-the-loop sign-off stored in immutable `security_audit_records`.

### 2. Multi-Rail Settlement Matrix
- **NPCI UPI 2.0**: Managed via `InstantUPIEngine` (`src/omniverse/modules/agency/upi_gateway.py`). Generates RFC-compliant UPI intents and dynamic QR SVG payloads. Replay attacks prevented via UTR tracking.
- **Web3 Crypto Escrow**: Managed via `Web3CryptoEscrow` (`src/omniverse/modules/agency/crypto_gateway.py`). Supports Solana, Base, Ethereum, Polygon USDC/USDT escrow deposits with on-chain cryptographic transaction hash validation.
- **ISO 20022 Enterprise Banking**: Managed via `ISO20022Engine` (`src/omniverse/modules/bangalore/iso20022.py`). Supports `pain.001` (credit transfers), `pacs.008` (interbank settlements), and `camt.053` (bank statements).

### 3. Autonomous Agency & Self-Healing Pipeline
- **Continuous Execution**: 24/7 background agent loop via `AutonomousAgencyDaemon` (`src/omniverse/modules/agency/daemon.py`).
- **Autonomous Fulfillment**: Code Factory, Marketing Factory, Automation Factory.
- **Self-Healing Revision**: `AutonomousRevisionAgent` (`src/omniverse/modules/agency/revision_manager.py`) refactors frontend, backend, and copywriting deliverables in response to client feedback, re-runs pre-flight QA, and regenerates distribution ZIP bundles.
- **Programmatic Inbound Magnet**: `ProgrammaticSEOMagnet` (`src/omniverse/modules/agency/inbound_pseo.py`) generates organic alternative pages with Schema.org JSON-LD and booking CTAs.

### 4. Health Diagnostics & Container Probes
- `/healthz`: Immediate liveness check for container orchestrators.
- `/readyz`: Deep readiness probe verifying database connectivity and disk write capabilities.
