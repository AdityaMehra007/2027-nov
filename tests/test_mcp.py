import pytest
from omniverse.mcp.server import OmniverseMCPServer

def test_mcp_server_tools_registration():
    server = OmniverseMCPServer()
    tools = server.list_tools()
    
    assert len(tools) >= 3
    tool_names = [t["name"] for t in tools]
    assert "generate_growth_kit" in tool_names
    assert "get_system_status" in tool_names
    assert "evaluate_resilience_risk" in tool_names

def test_mcp_server_call_tool():
    server = OmniverseMCPServer()
    result = server.call_tool(
        tool_name="generate_growth_kit",
        arguments={
            "business_name": "Artisan Tea Co",
            "niche": "Specialty Tea",
            "city": "Bengaluru"
        }
    )
    assert "social_captions" in result
    assert len(result["social_captions"]) == 10
