#!/usr/bin/env python3
"""
OpenClaw <-> Omniverse & Dev Universe Bridge
Enables OpenClaw personal AI assistant and autonomous agent gateway to:
- Query 11,900+ curated developer resources across 13 repositories
- Deploy and manage self-hosted SaaS stacks (Vaultwarden, Nextcloud, Umami, etc.)
- Access Omniverse quantitative intelligence, RTGS ledgers, and benchmarks
- Generate native OpenClaw skill definitions for the local gateway
"""

import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "dev_universe.db"
OPENCLAW_DIR = BASE_DIR / "openclaw"
OMNIVERSE_SKILL_DIR = OPENCLAW_DIR / "skills" / "omniverse"

def get_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search_knowledge(query: str, item_type: str = None, limit: int = 10):
    """Bridge function for OpenClaw agents to query developer knowledge."""
    from scripts.search_dev_universe import search
    return search(query=query, item_type=item_type, limit=limit)

def get_system_status():
    """Retrieve Omniverse & Dev Universe operational status."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM resources")
    total_resources = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT source_repo FROM resources")
    sources = [r[0] for r in cursor.fetchall()]
    conn.close()

    status = {
        "status": "ONLINE",
        "omniverse_engine": "CASHFLOW INFINITY: OMNIVERSE Dual-Core OS",
        "knowledge_resources_indexed": total_resources,
        "ecosystems_connected": len(sources),
        "connected_sources": sources,
        "openclaw_integrated": OPENCLAW_DIR.exists(),
        "opendots_integrated": (BASE_DIR / "OpenDots").exists()
    }
    return status

def generate_openclaw_skill():
    """Generates a native OpenClaw SKILL.md definition inside openclaw/skills/omniverse/."""
    OMNIVERSE_SKILL_DIR.mkdir(parents=True, exist_ok=True)
    skill_file = OMNIVERSE_SKILL_DIR / "SKILL.md"

    content = """---
name: omniverse
description: "Query 11,900+ developer resources, self-hosted Docker stacks, and Omniverse institutional OS intelligence."
homepage: https://github.com/AdityaMehra007/cashflow-infinity-omniverse
metadata:
  {
    "openclaw":
      {
        "emoji": "🌌",
        "requires": { "bins": ["python"] },
        "install": [],
      },
  }
---

# Omniverse & Dev Universe Knowledge Gateway

Connects OpenClaw to the unified knowledge base and institutional OS:
- Query books, courses, APIs, system design, and algorithms across 13 repositories
- Search self-hosted open-source SaaS alternatives (replaces Notion, Slack, Google Drive)
- Inspect high-throughput financial benchmarks and dual-core OS health

## Commands

```bash
# Search developer knowledge
python scripts/search_dev_universe.py -q "<topic>"

# Search self-hosted alternatives
python scripts/search_dev_universe.py --saas "<product>"

# Launch self-hosted Docker stack
python scripts/selfhosted_launcher.py generate <stack_name>
```
"""
    skill_file.write_text(content, encoding="utf-8")
    return skill_file

def main():
    parser = argparse.ArgumentParser(description="OpenClaw <-> Omniverse Bridge CLI")
    parser.add_argument("--status", action="store_true", help="Print bridge status")
    parser.add_argument("--search", type=str, help="Search developer resources")
    parser.add_argument("--type", type=str, help="Filter search by type")
    parser.add_argument("--install-skill", action="store_true", help="Install Omniverse skill into OpenClaw")

    args = parser.parse_args()

    if args.install_skill:
        path = generate_openclaw_skill()
        print(f"[+] Installed Omniverse skill definition to: {path}")
        return

    if args.search:
        results = search_knowledge(args.search, item_type=args.type)
        print(f"[*] Found {len(results)} matches for '{args.search}':\n")
        for r in results:
            print(f"  [{r['type']}] {r['title']} ({r['category']})")
            print(f"    {r['url']}\n")
        return

    # Default to status
    status = get_system_status()
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
