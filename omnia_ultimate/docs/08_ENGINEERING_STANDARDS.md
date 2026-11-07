# OMNIA Engineering Standards

## Architecture
- Modular monolith by default.
- Clear bounded contexts.
- Explicit API and event contracts.
- Versioned schema migrations.
- Idempotent external operations.
- Timeouts, retries, cancellation and backoff.
- No unbounded agent loops.

## Code
- Type hints/types where supported.
- Small composable modules.
- Structured errors.
- Input validation.
- Secure defaults.
- Dependency pinning.
- Reproducible builds.
- Licence inventory.
- Code review and changelog.

## Testing
- Unit tests for domain logic.
- Property-based tests for invariants where useful.
- Integration tests for persistence and contracts.
- End-to-end tests for critical user flows.
- Adversarial tests for tool and prompt boundaries.
- Performance benchmarks based on real workload.
- Backup/restore and failure-recovery tests.

## Security
- Least privilege.
- Default deny.
- No secrets in source.
- Narrow tool allowlists.
- Data minimisation.
- Tenant isolation.
- Dependency scanning.
- SBOM.
- Secret rotation.
- Audit and incident response.

## SLO discipline
Define availability, latency, correctness and recovery targets from user needs. Do not claim an SLO until monitored over a representative period.

## Release gates
No production release with unresolved critical security defects, untested tenant boundaries, absent rollback plan, no incident owner or unverified data deletion/export promises.
