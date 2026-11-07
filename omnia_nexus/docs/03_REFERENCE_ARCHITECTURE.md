# OMNIA / ATLAS X — Reference Architecture

## 1. Programme boundary
OMNIA is a portfolio. ATLAS X is the digital shared platform. Physical-world systems, labs, medical devices, industrial controls and critical infrastructure remain separate domain systems with certified control boundaries and qualified operators.

## 2. Logical planes

### Experience plane
- Web app and operator console.
- Accessible UI and component system.
- Developer portal and SDKs.
- Domain-specific applications.

### Identity and governance plane
- OIDC/OAuth2.
- Organisations, users, workspaces and roles.
- RBAC plus scoped capabilities.
- Tenant isolation.
- Consent and policy.
- Approval and revocation.
- Audit events.

### Intelligence plane
- Model provider adapter.
- Routing by quality, cost, privacy and latency.
- Prompt/version registry.
- Retrieval and source provenance.
- Structured output validation.
- Evaluation and regression harness.
- Cost attribution and fallback.

### Orchestration plane
- Durable workflow state machines.
- Agent registry.
- Tool registry.
- Scheduler and queue.
- Retry, timeout and cancellation.
- Human approval.
- Idempotency and compensation.

### Knowledge plane
- PostgreSQL system of record.
- Document and object storage.
- Search.
- Vector indexing only when demonstrated useful.
- Entity and relationship graph.
- Provenance and temporal validity.
- Data retention, export and deletion.

### Integration plane
- Connector manifest.
- OAuth scopes.
- Secret vault.
- Webhooks and signature validation.
- Rate limits.
- Idempotency keys.
- Connector health checks.
- Per-user revocation.

### Operations plane
- CI/CD.
- Structured logs.
- Metrics and distributed traces.
- SLOs and error budgets.
- Backup and restore.
- Incident response.
- Cost and capacity management.

## 3. Software architecture evolution

Start as a modular monolith with clean modules and explicit interfaces.

Extract a service only when there is evidence of:
- Independent scaling.
- Security isolation.
- Separate team ownership.
- Deployment cadence conflict.
- Reliability blast-radius reduction.
- Incompatible technology requirements.

For every service extraction, specify consistency, ordering, idempotency, retries, failure handling, observability, security and disaster recovery.

## 4. Technology matrix

| Domain | Candidate languages/technology | Decision rule |
|---|---|---|
| Policy kernel | Rust | Use where memory safety and explicit capability boundaries justify it |
| Control plane | Go | Use for concurrency-heavy services and clear operational binaries |
| AI/research | Python | Use for model ecosystem, evaluation and scientific libraries |
| UI/SDK | TypeScript | Use for web ecosystem and strong typed contracts |
| Storage | PostgreSQL/SQL | Use constraints, transactions and row-level security |
| Compute acceleration | C/C++/CUDA/HIP | Profile first; accelerator availability and licensing apply |
| Hardware logic | SystemVerilog/VHDL | Qualified hardware teams and simulation/testbench required |
| Scientific numerical | Julia/Python/MATLAB | Select by ecosystem, performance and reproducibility |
| Plugin sandbox | WebAssembly/WASI | Treat plugins as untrusted; narrow host capabilities |
| Formal modelling | TLA+/Alloy/Lean | Apply to critical state machines and invariants |

## 5. Required invariants
1. Default deny.
2. Every resource has an owner and tenant.
3. Every external action is specifically approved or covered by a narrow pre-authorisation.
4. Restricted actions cannot be authorised by generic agent permission.
5. Every workflow transition is state-validated.
6. Every tool call is capability-scoped.
7. Audit data excludes unnecessary secrets and sensitive payloads.
8. Connector grants are revocable.
9. Data export and deletion are specified.
10. Every consequential decision has provenance.

## 6. AI evaluation
Measure task success, factuality, evidence coverage, tool selection, policy violations, escalation rate, latency p50/p95/p99, cost per successful workflow, repeatability and robustness.

## 7. Production gaps
The included starter is not a production identity, multi-tenant, high-availability or external integration system. Production requires authentication, secret management, tenant isolation, durable database storage, distributed locking, rate limiting, observability, backups, incident response, independent security assessment and deployment review.
