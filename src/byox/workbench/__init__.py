"""BYOX Workbench Package."""

from .server import WorkbenchServer

# Alias for high-level naming
BYOXWorkbench = WorkbenchServer

__version__ = "1.0.0"

__all__ = ["WorkbenchServer", "BYOXWorkbench"]
