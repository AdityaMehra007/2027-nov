# PROJECT ATLAS X

**A polyglot reference implementation for a permissioned AI execution platform.**

This repository contains an executable vertical slice, not a completed global platform.

## Architecture

- **Go control plane**: HTTP API, task lifecycle, durable append-only audit ledger.
- **Python intelligence service**: deterministic baseline career/job analysis with a provider interface; no external model or paid API required.
- **Rust policy kernel**: pure policy decision library for future WASM/native embedding. It is not yet wired into the Go request path.
- **TypeScript SDK + browser console**: typed API client and small operator console.
- **PostgreSQL/Supabase migration**: workspace-scoped schema and RLS example.
- **TLA+ sketch**: workflow safety properties for model checking.

## Local prerequisites

- Go 1.23+
- Python 3.11+
- Node.js 20+ and TypeScript compiler 5.8+
- Rust 1.85+ (optional for the policy crate; not required to run Go/Python services)

The environment used to generate this package has Go 1.23.2, Python 3.13.5 and Node 22.16.0. Rust/Cargo is not installed here, so the Rust crate is source-only in this validation run.

## Run the control plane

```bash
cd services/control-plane
go test ./...
ATLAS_API_TOKEN='local-dev-only-change-me' ATLAS_DATA_DIR='../../.atlas-data' go run ./cmd/atlasd
```

The API listens on `http://localhost:8080`.

```bash
curl -s http://localhost:8080/healthz
curl -s -X POST http://localhost:8080/v1/tasks \
  -H 'Authorization: Bearer local-dev-only-change-me' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: demo-task-001' \
  -d '{"title":"Analyse a role","description":"Compare role requirements with verified profile evidence","action_class":"draft"}'
```

For an external action, use `"action_class":"external"`. It will remain `approval_required` until an explicit approval endpoint is called. `restricted` actions are rejected.

## Run the intelligence service

```bash
cd services/intelligence
python -m unittest discover -s tests -v
python app.py
```

The service listens on `http://localhost:8090`.

```bash
curl -s -X POST http://localhost:8090/v1/job-analysis \
  -H 'Content-Type: application/json' \
  -d '{"job_title":"Operations Analyst","job_description":"Requirements: Excel, SQL, reporting, stakeholder management","profile_evidence":["Built Excel reporting dashboards","Completed SQL coursework"]}'
```

This first provider is deterministic keyword matching. It is deliberately labelled as a baseline, not a frontier model.

## Compile the TypeScript SDK and console

```bash
cd packages/typescript-sdk && tsc -p tsconfig.json
cd ../../apps/console && tsc -p tsconfig.json
python -m http.server 4173
```

Open `http://localhost:4173/apps/console/` when serving the repository root, or serve the `apps/console` directory directly and open its `index.html`.

## Rust policy kernel

```bash
cd crates/policy-kernel
cargo test
```

The crate uses Rust 2024 and no third-party dependencies. It is not integrated into the Go control plane yet. Keep one authoritative policy implementation when wiring it in; do not silently maintain divergent policy rules.

## Audit ledger

The Go control plane writes JSONL events with a SHA-256 hash chain and fsyncs each appended event. This makes edits detectable, but it is **not** a digital signature, WORM storage guarantee, multi-node consensus system or tamper-proof remote audit service. Protect the file and backups operationally.

## Security status

This is a local development reference implementation. Before real user data or public deployment, add production authentication/identity, TLS termination, secret management, rate limiting, hardened CORS/CSRF strategy, dependency scanning, backups, observability, privacy review, penetration testing and external security assessment.

The SQL migration assumes Supabase Auth (`auth.uid()`). Do not apply it unchanged to vanilla PostgreSQL.

## Project status

Implemented in this starter:
- task API with explicit approval gate;
- append-only hash-chained event ledger;
- deterministic job-analysis endpoint;
- TypeScript client and basic console;
- policy crate source and SQL schema;
- automated tests for Go and Python.

Not implemented:
- real LLM provider integration;
- actual job-board integrations;
- production identity or billing;
- distributed queue/worker fleet;
- multi-region deployment;
- hardened sandbox execution;
- enterprise readiness.
