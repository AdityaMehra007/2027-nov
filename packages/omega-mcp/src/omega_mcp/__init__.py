"""
OMEGA-MCP: Model Context Protocol (MCP) Fleet Hub
Architect: Aditya Mehra (https://github.com/AdityaMehra007)
"""

__version__ = "1.0.0"
__author__ = "Aditya Mehra"
__email__ = "ashishiash007@gmail.com"

from .server import OmegaMCPServer
from .tools import register_tool, get_registered_tools

__all__ = ["OmegaMCPServer", "register_tool", "get_registered_tools", "__version__"]
