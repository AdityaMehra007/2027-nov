---
description: Guardrail for GitHub Actions workflow file operations and OAuth scope boundaries
globs: ".github/**,deploy/**"
---

# GitHub Workflow Scope & CI/CD Deployment Guardrails

1. **OAuth Scope Verification Before Touching `.github/workflows/`**:
   - GitHub OAuth tokens without the explicit `workflow` scope reject any `git push` containing changes in `.github/workflows/*`.
   - Before creating or modifying workflow files, verify token scopes via `gh auth status`.

2. **Decoupled Workflow Blueprint Pattern**:
   - If the active token lacks the `workflow` scope, do NOT write directly to `.github/workflows/`, as it will block commits and pushes for the entire codebase.
   - Store CI/CD workflow definitions under `deploy/ci-workflow.yml` or `docs/ci/`.
   - Provide the user with the direct refresh command to grant scope:
     ```bash
     gh auth refresh -h github.com -s workflow
     ```
