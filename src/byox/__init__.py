"""BYOX - Build-Your-Own-X Canonical Systems Suite & Workbench."""

from .workbench import BYOXWorkbench
from .benchmarks.runner import run_all_benchmarks
from .benchmarks.metrics import BenchmarkResult

__version__ = "1.0.0"

__all__ = [
    "BYOXWorkbench",
    "run_all_benchmarks",
    "BenchmarkResult",
]
