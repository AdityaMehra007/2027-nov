# ATLAS Security Threat Model (initial)

## Assets
- User identity and credentials
- Workspace records and uploaded documents
- Connector tokens and API secrets
- Workflow instructions and tool permissions
- AI prompts, outputs and retrieved context
- Audit events and billing/usage records

## Trust boundaries
1. Browser to control plane
2. Control plane to database/event ledger
3. Control plane to intelligence provider
4. Agent runtime to connector/tool execution
5. Tenant/workspace to tenant/workspace
6. User-approved actions to external systems

## Threats and baseline mitigations
| Threat | Baseline mitigation | Required verification |
|---|---|---|
| Cross-tenant data access | Tenant-scoped queries, RLS, isolation tests | Negative access tests for every data API |
| Prompt injection via documents/web content | Treat retrieved content as untrusted data; tool allowlists | Adversarial prompt-injection suite |
| Credential theft | Secret manager, short-lived tokens, least privilege | Secret scanning and rotation drill |
| Unsafe agent action | Capability scopes, approval gateway, action allowlist | Policy conformance tests |
| Replay/duplicate execution | Idempotency keys and deduplication | Duplicate request tests |
| Audit tampering | Hash-chained append-only records and protected backups | Tamper detection and restore test |
| Model hallucination | Source-grounded outputs, abstention and evaluation | Labelled evaluation suite |
| Denial of service | Body limits, rate limits, timeouts and quotas | Load and abuse tests |
| Supply-chain compromise | Lockfiles, dependency scans, signed builds where feasible | CI security checks |
| Sensitive data leakage | Data minimisation, redacted logs, retention controls | Log inspection and privacy tests |

## Security review requirements
Use OWASP ASVS 5.0.0 as a web application verification baseline and adapt requirements to the product. This is not a certification claim. Add a formal privacy assessment and qualified legal/security review before handling sensitive or regulated data.
