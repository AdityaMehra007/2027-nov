#!/usr/bin/env python3
"""
OpenDots <-> Omniverse Master Bridge
Controls and monitors the OpenDots AI Coworker platform inside CASHFLOW INFINITY: OMNIVERSE.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OPENDOTS_DIR = BASE_DIR / "OpenDots"
SERVER_URL = "http://127.0.0.1:4310"

def get_status():
    """Check health and retrieve active spaces and dots from OpenDots."""
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/workspace")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "running": True,
                "url": SERVER_URL,
                "spaces": data.get("spaces", []),
                "dots": data.get("dots", []),
                "setup": data.get("setup", {}),
            }
    except Exception as e:
        return {
            "running": False,
            "url": SERVER_URL,
            "error": str(e),
        }

def start_server(dev_mode=False):
    """Start OpenDots server (production or dev)."""
    status = get_status()
    if status["running"]:
        print(f"[OK] OpenDots is already running at {SERVER_URL}")
        return True

    print(f"[*] Starting OpenDots from {OPENDOTS_DIR}...")
    cmd = ["npm", "run", "dev"] if dev_mode else ["node", "--env-file-if-exists=.env", "dist/server/server/index.js"]
    proc = subprocess.Popen(
        cmd,
        cwd=str(OPENDOTS_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    print(f"[+] Started process (PID {proc.pid}).")
    return True

def print_summary():
    status = get_status()
    print("=" * 60)
    print("  OPENDOTS AI COWORKERS - OMNIVERSE RUNTIME STATUS")
    print("=" * 60)
    if status["running"]:
        print(f" Status:       ONLINE [Active]")
        print(f" URL:          {status['url']}")
        print(f" Spaces Count: {len(status['spaces'])}")
        for sp in status["spaces"]:
            print(f"   * Space: {sp.get('name')} (ID: {sp.get('id')})")
        print(f" Dots Count:   {len(status['dots'])}")
        for dt in status["dots"]:
            print(f"   * Specialist Dot: {dt.get('name')} (Role: {dt.get('instructions')[:50]}...)")
        setup = status.get("setup", {})
        print(f" Model Engine: {'Configured' if setup.get('model') else 'Pending'}")
        print(f" Browser:      {'Enabled' if setup.get('browser') else 'Disabled'}")
        print(f" Intelligence: {'Connected' if setup.get('intelligence') else 'Local/Self-hosted Pending'}")
    else:
        print(f" Status:       OFFLINE")
        print(f" Detail:       {status.get('error', 'Cannot reach server')}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="OpenDots Omniverse Bridge")
    parser.add_argument("--status", action="store_true", help="Check status of OpenDots")
    parser.add_argument("--start", action="store_true", help="Start OpenDots server")
    parser.add_argument("--dev", action="store_true", help="Start in dev mode")
    args = parser.parse_args()

    if args.start:
        start_server(dev_mode=args.dev)
    else:
        print_summary()

if __name__ == "__main__":
    main()
