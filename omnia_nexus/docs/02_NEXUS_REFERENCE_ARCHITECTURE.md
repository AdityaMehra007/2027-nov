# OMNIA NEXUS / ATLAS X — Reference Architecture

## 1. Programme boundaries
OMNIA is a portfolio. ATLAS X is shared digital infrastructure. Physical, scientific, medical, energy and aerospace systems retain separate domain control systems, certified safety interlocks and qualified operators.

## 2. Logical planes

### Experience plane
- Web products and operator consoles.
- Accessible UI and design system.
- Developer portal and SDK.
- Domain-specific products.

### Identity/trust plane
- OIDC/OAuth2.
- User, organisation, workspace and role model.
- RBAC plus scoped capabilities.
- Tenant isolation.
- Consent and policy enforcement.
- Approval, revocation and audit.

### Intelligence plane
- Model/provider gateway.
- Routing by quality, cost, privacy and latency.
- Prompt and policy versioning.
- Retrieval and source provenance.
- Structured output validation.
- AI evaluation and regression suite.
- Cost attribution and fallback.

### Orchestration plane
- Durable workflow state machine.
- Agent registry and task scheduler.
- Tool registry.
- Retries, timeouts, idempotency and cancellation.
- Human approval and escalation.
- Compensation and rollback hooks.

### Knowledge plane
- PostgreSQL system of record.
- Document/object storage.
- Search and optional vector retrieval.
- Entity/relationship model.
- Provenance and temporal validity.
- Data retention, export and deletion.

### Integration plane
- Connector manifest and scopes.
- OAuth and secret vault.
- Webhook signature validation.
- Rate limits and idempotency keys.
- Health checks and revocation.

### Operations plane
- CI/CD.
- Structured logs, metrics and traces.
- SLOs and error budgets.
- Backup and restore.
- Incident response.
- Cost and capacity management.

## 3. Architecture evolution
Start with a modular monolith and explicit boundaries. Extract services only for demonstrated independent scaling, security isolation, separate team ownership, deployment cadence or reliability needs.

Every distributed service requires a written consistency, ordering, retry, idempotency, failure, observability, security and recovery model.

## 4. Language policy
- Rust: selected policy, sandbox and systems components.
- Go: control plane and workers.
- Python: AI, scientific computing and evaluation.
- TypeScript: web and SDK.
- SQL: transactions, constraints and analytics.
- C/C++/CUDA/HIP: measured performance-critical work.
- SystemVerilog/VHDL: real hardware development with specialist testbenches.
- Julia/MATLAB: numerical modelling when beneficial.
- WASM/WASI: constrained portable extension execution.
- TLA+/Alloy/Lean/Coq: critical invariants.

## 5. Required invariants
1. Deny by default.
2. Every record has an owner and tenant.
3. Every external action has a specific approval or narrow pre-authorisation.
4. Restricted actions remain blocked in the general agent runtime.
5. Workflow transitions are state-validated.
6. Tool calls are capability-scoped.
7. Audit events do not expose unnecessary secrets.
8. Connector grants can be revoked.
9. Data export/deletion behavior is documented and testable.
10. Consequential outputs carry provenance.

## 6. Production requirements
Authentication, multi-tenant isolation, database migrations, secret management, rate limiting, durable queues, concurrent-worker control, monitoring, backup/restore, incident response, independent security review, privacy assessment and rollback.
