#!/usr/bin/env python3
"""Example 07: Model Context Protocol (MCP) Agent Orchestration.

Demonstrates programmatic discovery and execution of Omniverse tools via
the standard Model Context Protocol (MCP) interface.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.mcp.server import OmniverseMCPServer

def main():
    print("================================================================")
    print("  07. MODEL CONTEXT PROTOCOL (MCP) AGENT HARNESS")
    print("================================================================")

    server = OmniverseMCPServer()

    # 1. Discover Registered Tools
    print("\n🛠️ Step 1: Discovering Registered MCP Tools...")
    tools = server.list_tools()
    for tool in tools:
        print(f" • Tool: {tool['name']:25} | {tool['description'][:65]}...")

    # 2. Execute Aether Risk Assessment via MCP
    print("\n🌍 Step 2: Executing 'evaluate_resilience_risk' via MCP...")
    args_risk = {
        "lat": 19.0760,
        "lon": 72.8777,
        "elevation_meters": 12.0,
        "hazard": "FLOOD"
    }
    res_risk = server.call_tool("evaluate_resilience_risk", args_risk)
    print(f" • Return Status       : {res_risk.get('status', 'SUCCESS')}")
    print(f" • Vulnerability Index : {res_risk['vulnerability_index']} / 100")
    print(f" • Risk Rating         : {res_risk['risk_level']}")

    # 3. Execute Growth Kit Generation via MCP
    print("\n💼 Step 3: Executing 'generate_growth_kit' via MCP...")
    args_kit = {
        "business_name": "Artisan Bakery",
        "niche": "Bakery",
        "city": "Bengaluru"
    }
    res_kit = server.call_tool("generate_growth_kit", args_kit)
    print(f" • Target Business     : {res_kit['business_name']} ({res_kit['city']})")
    print(f" • Generated Captions  : {len(res_kit['social_captions'])} social posts ready")
    print(f" • Promotional Hooks   : {len(res_kit['promotional_hooks'])} hooks ready")
    print("================================================================")

if __name__ == "__main__":
    main()
