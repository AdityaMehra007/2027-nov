---
name: omniverse-command
description: Master control orchestrator for CASHFLOW INFINITY: OMNIVERSE. Use to inspect platform status, view global financial ledgers, and coordinate cross-division agent directives.
---

# CASHFLOW INFINITY: OMNIVERSE Command Orchestrator

The supreme operational command skill for managing the Omniverse platform inside Google Antigravity.

## When to Use
- When the user asks "check omniverse status", "show omniverse health", "overview", or "run omniverse command".
- To coordinate work across Executive, Commercial, Financial, and Operations divisions.

## Quick Actions

### 1. View System & Financial Status
Run in terminal:
```powershell
python -m omniverse.cli status
```

### 2. Launch FastAPI Interactive Command Center
```powershell
python -m omniverse.cli serve --port 8000
```
Interactive Swagger documentation will be available at `http://127.0.0.1:8000/docs`.

### 3. Safety Boundary Reminders
- Never execute live capital movements or trade orders without explicit human approval.
- All outbound communications require verified customer review.
