# Agent Guidelines: CASHFLOW INFINITY (OMNIVERSE)

This repository houses the planetary dual-core autonomous operating system for **CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC**.

## Agent skills

### Issue tracker

GitHub issues tracked under `AdityaMehra007/cashflow-infinity-omniverse` using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical triage roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout with root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.

---

## Engineering Guidelines

### 1. Test-Driven Development (TDD)
- Strictly adhere to red-green-refactor cycles.
- Run tests via `pytest` or `python -m pytest`. Ensure 100% test passing before completing work.

### 2. Domain Vocabulary
- Always use canonical terminology defined in `GLOSSARY.md`.
- Consult existing decisions in `docs/adr/` before proposing architectural changes.

### 3. Issue & PR Workflow
- When asked to plan work, use `/to-spec` and `/to-tickets` to publish tracer-bullet issues on GitHub.
- For high-level initiatives, use `/wayfinder` to construct dependency maps using native GitHub issue blocking.
