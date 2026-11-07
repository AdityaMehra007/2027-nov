"""
Test Suite for OMEGA-MCP Standalone Package
Validates tool registry, JSON-RPC 2.0 dispatching, and CLI execution.
"""

import pytest
import json
from omega_mcp.server import OmegaMCPServer
from omega_mcp.tools import get_registered_tools, execute_tool

def test_omega_mcp_tools_registry():
    tools = get_registered_tools()
    assert len(tools) >= 4
    tool_names = [t["name"] for t in tools]
    assert "bengaluru_startup_radar" in tool_names
    assert "generate_growth_kit" in tool_names
    assert "evaluate_resilience_risk" in tool_names
    assert "double_entry_ledger_clearing" in tool_names

def test_omega_mcp_startup_radar_execution():
    res = execute_tool("bengaluru_startup_radar", {"query": "Sarvam"})
    assert res["status"] == "success"
    assert res["output"]["count"] >= 1
    assert any("Sarvam" in r["name"] for r in res["output"]["results"])

def test_omega_mcp_growth_kit_execution():
    res = execute_tool("generate_growth_kit", {
        "business_name": "Apex Engineering",
        "niche": "Autonomous Systems",
        "city": "Bengaluru"
    })
    assert res["status"] == "success"
    assert "Apex Engineering" in res["output"]["business_name"]
    assert len(res["output"]["hooks"]) >= 2

def test_omega_mcp_ledger_clearing_zero_leak():
    res = execute_tool("double_entry_ledger_clearing", {
        "debit_account": "ACC_PRIMARY",
        "credit_account": "ACC_ESCROW",
        "amount": 75000.0,
        "currency": "INR"
    })
    assert res["status"] == "success"
    assert res["output"]["zero_leak_verified"] is True
    assert res["output"]["status"] == "SETTLED"

def test_omega_mcp_server_jsonrpc_list():
    server = OmegaMCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    resp = server.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 1
    assert "tools" in resp["result"]
    assert len(resp["result"]["tools"]) >= 4

def test_omega_mcp_server_jsonrpc_call():
    server = OmegaMCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "evaluate_resilience_risk",
            "arguments": {
                "lat": 12.9716,
                "lon": 77.5946,
                "hazard": "FLOOD"
            }
        }
    }
    resp = server.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 2
    content = resp["result"]["content"][0]["text"]
    parsed = json.loads(content)
    assert parsed["status"] == "success"
    assert parsed["tool"] == "evaluate_resilience_risk"
