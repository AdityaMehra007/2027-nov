---
name: omniverse-ops
description: 24/7 background worker daemons, scheduled health monitors, and system diagnostics for CASHFLOW INFINITY.
---

# CASHFLOW INFINITY: 24/7 Continuous Operations

Use this skill to inspect daemon health, verify background schedulers, and monitor resource consumption.

## When to Use
- User asks to "check daemon", "run health check", "view system resources", or "monitor 24/7 jobs".

## Health Diagnostics
The operational watchdog evaluates:
1. Database connectivity and query execution latency.
2. Available disk storage (alerts if below 1.0 GB).
3. Process memory usage.
4. Active scheduled job queues.

## Running Background Audits
Trigger immediate system inspection via CLI:
```powershell
python -m omniverse.cli status
```
