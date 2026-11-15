"""
pyregex: Zero-dependency Thompson NFA Regular Expression Engine
Built for CASHFLOW INFINITY / ATLAS NEXUS reference architectures.
"""

from .matcher import match, search
from .compiler import compile_regex

__all__ = ["match", "search", "compile_regex"]
