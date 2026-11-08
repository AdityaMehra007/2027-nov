---
description: Requirement for non-interactive health check flags on interactive CLI menus and launchers
globs: "*.py,scripts/**"
---

# CLI Launcher Non-Interactive Verification Invariant

1. **Mandatory `--check` / Headless Flag**:
   - Every interactive console launcher (e.g., `launch_empire.py`, menu scripts) that reads from `stdin` (`input()`) MUST support a `--check` or `--dry-run` flag.
   - When `--check` is passed, the script must initialize, print the banner/options, verify environment preconditions, and exit immediately with code `0`.
   - This ensures automated agent loops, CI pipelines, and health monitors can verify launcher integrity without hanging on `stdin`.
