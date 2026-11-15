"""
ATLAS NEXUS: Command-Line Interface (CLI)
Enables direct terminal execution, telemetry inspection, and capability discovery.
"""

import argparse
import sys
from typing import List, Optional

from src.nexus.client import NexusClient


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="ATLAS NEXUS: The Civilization-Scale Intelligence & Creation Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: status
    subparsers.add_parser("status", help="Display platform status and telemetry")

    # Command: capabilities
    subparsers.add_parser("capabilities", help="List all 50 indexed institutional capabilities")

    # Command: intake
    intake_parser = subparsers.add_parser("intake", help="Parse and classify a natural language directive")
    intake_parser.add_argument("query", type=str, help="Directive query string")

    # Command: execute
    exec_parser = subparsers.add_parser("execute", help="Execute directive through Universal Orchestrator")
    exec_parser.add_argument("query", type=str, help="Directive query string")

    parsed = parser.parse_args(args)
    client = NexusClient()

    if parsed.command == "status" or parsed.command is None:
        telemetry = client.get_telemetry()
        print("=" * 60)
        print("🌌 ATLAS NEXUS: Universal Operating Infrastructure")
        print("=" * 60)
        print(f"Departments Active: {telemetry.departments_ready}")
        print(f"Indexed Capabilities: {telemetry.capabilities_indexed}")
        print(f"Active Meta-Agents: {telemetry.active_agents}")
        print(f"Audit HLC Clock: {telemetry.hlc_timestamp}")
        print("Platform Status: ONLINE & READY")
        print("=" * 60)
        return 0

    elif parsed.command == "capabilities":
        caps = client.get_capabilities()
        print(f"Indexed {len(caps)} Capabilities across 9 Institutional Departments:")
        for c in caps:
            print(f"  [{c.id:02d}] {c.name:<36} ({c.department.name})")
        return 0

    elif parsed.command == "intake":
        directive = client.submit_directive(parsed.query)
        print(f"Directive ID: {directive.directive_id}")
        print(f"Detected Intent: {directive.intent}")
        print(f"Target Departments: {[d.name for d in directive.target_departments]}")
        print(f"Capabilities Routed: {directive.requested_capabilities}")
        return 0

    elif parsed.command == "execute":
        manifest = client.execute(parsed.query)
        print(f"Execution Manifest: {manifest.directive_id} [{manifest.status}]")
        print(f"Executed Departments: {[d.name for d in manifest.executed_departments]}")
        print(f"Audit Trail Steps: {len(manifest.audit_trail)}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
