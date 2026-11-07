# Status and Limitations

## Included implementation
- Python standard-library HTTP server.
- SQLite task and approval persistence.
- Default-deny action policy for restricted action classes.
- Explicit approval requirement for approval-gated action class.
- Allowlisted in-process demo handlers.
- Hash-chained audit events.
- Unit and integration tests.

## Not included
- Real identity/authentication.
- Multi-tenant isolation.
- Production security boundary.
- External connectors.
- Real-world actions or account integration.
- Distributed scheduler.
- Durable distributed execution.
- High availability.
- Production secrets management.
- Rust kernel binding.
- LLM provider integration.
- Frontend application.
- Kubernetes or multi-region deployment.

## Audit caveat
The hash chain detects accidental or unsophisticated record alteration when the chain is checked. A local database administrator could rewrite the database and recompute the entire chain. Production requires signed checkpoints anchored outside the database, secure key management and independent log retention.

## Policy caveat
The policy module is a prototype application-level gate. It is not a hardened security kernel or sandbox. The HTTP API has no authentication and must remain bound to localhost.
