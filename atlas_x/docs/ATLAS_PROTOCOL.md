# ATLAS Protocol v0.1 — design contract

## Resource model
- Principal: authenticated user or service identity.
- Workspace: tenant security boundary.
- Capability: narrowly scoped permission to perform an operation.
- Workflow: versioned state machine describing tasks and transitions.
- Tool: registered operation with schema, permission scope, timeout, idempotency strategy and effect classification.
- Evidence: source-backed artefact supporting a claim or result.
- Approval: explicit grant for a specific action, scope and context.
- Receipt: immutable record of an attempted or completed action.

## Tool invocation envelope (logical schema)
```json
{
  "invocation_id": "uuid",
  "principal_id": "uuid",
  "workspace_id": "uuid",
  "workflow_id": "uuid",
  "tool_id": "connector.operation",
  "tool_version": "1.0.0",
  "effect_class": "read|draft|external|restricted",
  "input": {},
  "approval_id": null,
  "idempotency_key": "opaque-key",
  "deadline": "RFC3339 timestamp"
}
```

## Required execution semantics
1. Authenticate principal.
2. Resolve workspace and membership.
3. Validate tool and version.
4. Validate input against a strict schema.
5. Evaluate capability and policy in deterministic code.
6. Verify action-specific approval where necessary.
7. Enforce timeout, rate and resource budgets.
8. Execute with idempotency protection where supported.
9. Record outcome and evidence receipt.
10. Return a typed result or typed failure.

Model-generated content is untrusted input. A model may propose a tool call; it cannot authorise it.
