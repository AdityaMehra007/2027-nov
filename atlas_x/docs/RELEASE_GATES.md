# ATLAS Release Gates

## Gate A — Local demonstrator
- Control plane and intelligence service start.
- Unit and API tests pass.
- Approval transition enforced.
- Ledger integrity verification succeeds.

## Gate B — Private user testing
- Real identity and workspace membership.
- Cross-tenant isolation independently tested.
- Data export and deletion verified.
- No secrets in logs or client bundles.
- Privacy notice and data retention rules reviewed.

## Gate C — Public beta
- TLS, production secret management, backups and restore drills.
- Rate limiting, request timeouts, monitoring and alerting.
- Dependency/SAST/DAST checks and threat model review.
- Incident response runbook and support process.
- Terms, privacy and relevant legal review.

## Gate D — Enterprise
- SSO/SCIM where demanded.
- Admin and audit controls.
- Availability and recovery objectives backed by tests.
- Data processing terms and subprocessor disclosures.
- Independent penetration test and remediation.
- Support, change management and customer offboarding process.
