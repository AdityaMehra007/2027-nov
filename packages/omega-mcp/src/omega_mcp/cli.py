"""
OMEGA-MCP Command-Line Interface (CLI)
Executable entry point for omega-mcp package.
"""

import click
import json
import ast
import sys
from .server import OmegaMCPServer
from .tools import get_registered_tools, execute_tool

@click.group()
@click.version_option(version="1.0.0", prog_name="omega-mcp")
def main():
    """OMEGA-MCP: Model Context Protocol (MCP) Fleet Hub by Aditya Mehra."""
    pass

@main.command()
def list():
    """List all available MCP tools in the OMEGA fleet."""
    tools = get_registered_tools()
    click.echo(f"\n[OMEGA-MCP Fleet Hub] {len(tools)} Registered Tools:\n")
    for tool in tools:
        click.echo(f"  * {click.style(tool['name'], fg='cyan', bold=True)}")
        click.echo(f"    {tool['description']}")
        click.echo(f"    Required Args: {tool['parameters'].get('required', [])}\n")

@main.command()
@click.argument("tool_name")
@click.option("--args", "-a", default="{}", help="JSON or dict string of tool arguments")
def call(tool_name: str, args: str):
    """Call a specific tool directly from the terminal."""
    parsed_args = {}
    try:
        parsed_args = json.loads(args)
    except Exception:
        try:
            # Fallback for single-quoted Python / shell dicts
            parsed_args = ast.literal_eval(args)
            if not isinstance(parsed_args, dict):
                raise ValueError("Arguments must evaluate to a dictionary")
        except Exception as e:
            click.echo(click.style(f"Error parsing arguments '{args}': {e}", fg="red"))
            return

    click.echo(f"Executing '{tool_name}'...")
    result = execute_tool(tool_name, parsed_args)
    click.echo(json.dumps(result, indent=2))

@main.command()
def serve():
    """Start the MCP JSON-RPC 2.0 stdio server for Claude Desktop, Antigravity, or Cursor."""
    server = OmegaMCPServer()
    server.run_stdio()

if __name__ == "__main__":
    main()
