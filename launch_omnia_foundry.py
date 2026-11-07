#!/usr/bin/env python3
"""
PROJECT OMNIA NEXUS: Supreme Operational Launcher
Unified entry point to command the OMNIA Foundry, verify audit chains,
serve the API / Executive Dashboard, and track the 24 Venture Studios & 50 Tasks.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NEXUS_DIR = BASE_DIR / "omnia_nexus"
SRC_DIR = NEXUS_DIR / "src"

if not SRC_DIR.exists():
    print(f"Error: OMNIA Foundry source directory not found at {SRC_DIR}")
    sys.exit(1)

# Set PYTHONPATH to include omnia_foundry
env = os.environ.copy()
env["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + env.get("PYTHONPATH", "")

def main():
    args = sys.argv[1:]
    if not args:
        args = ["report"]

    # Check if user requested to run the API server
    if args[0] in ["serve", "server", "dashboard", "api"]:
        port = 8000
        host = "127.0.0.1"
        for i, a in enumerate(args):
            if a in ["--port", "-p"] and i + 1 < len(args):
                port = int(args[i+1])
            if a in ["--host", "-h"] and i + 1 < len(args):
                host = args[i+1]
        print(f"\n========================================================")
        print(f"  PROJECT OMNIA NEXUS — SUPREME CONTROL PLANE SERVER")
        print(f"========================================================")
        print(f"  * Executive Dashboard : http://{host}:{port}/dashboard")
        print(f"  * Swagger OpenAPI Docs: http://{host}:{port}/docs")
        print(f"  * System Health       : http://{host}:{port}/api/v1/health")
        print(f"========================================================\n")
        cmd = [sys.executable, "-m", "uvicorn", "omnia_foundry.api:app", "--host", host, "--port", str(port)]
        result = subprocess.run(cmd, cwd=str(NEXUS_DIR), env=env)
        sys.exit(result.returncode)

    # Otherwise dispatch to CLI
    cmd = [sys.executable, "-m", "omnia_foundry.cli"] + args
    result = subprocess.run(cmd, cwd=str(NEXUS_DIR), env=env)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
