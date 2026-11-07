# ATLAS Engineering Standards

## Architecture
- Explicit bounded contexts and ownership.
- Modular monolith until service extraction is justified by independent scaling, deployment, security isolation or ownership.
- API contracts versioned and tested.
- Event schemas versioned; additive evolution preferred.
- Timeouts, retries with jitter and idempotency for remote calls.
- No distributed transaction assumption; use outbox/saga patterns only when the workflow requires them.

## Code quality
- Strict typing where supported.
- Formatting, linting, static analysis and dependency checks in CI.
- Small cohesive modules; no hidden global state.
- Explicit error contracts; no swallowed exceptions.
- Deterministic tests for policy and domain logic.
- Property-based and fuzz testing for parsers and state transitions when supported.

## Reliability
- Define service-level indicators before service-level objectives.
- Measure success rate, tail latency, error rate, queue age and cost per successful workflow.
- Backups and restoration tests before production use.
- Runbooks for incidents, degraded mode and provider outage.

## AI engineering
- Version models, prompts, tool schemas and evaluation datasets.
- Separate model output from validated domain state.
- Never let model text directly authorise a tool invocation.
- Enforce schemas, permission checks and policy in deterministic code.
- Record model/provider, latency, token/cost estimates and outcome.
- Evaluate task completion, factuality, calibration, refusal behaviour and injection resilience.

## Security engineering
- Deny by default.
- Least privilege, short-lived credentials and tenant isolation.
- Separate development, staging and production credentials.
- No secrets in source, logs or client bundles.
- Review permissions for every connector and action.
- Human approval for consequential side effects.

## Release gates
- Reproducible build.
- Critical test suite passes.
- No unresolved critical/high security defect.
- Data migration and rollback plan reviewed.
- Monitoring and incident owner assigned.
- User documentation and known limitations published.
