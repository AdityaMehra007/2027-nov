"""Benchmark metrics collection and latency percentile calculations."""

from __future__ import annotations
from dataclasses import dataclass, field
import statistics
import time
from typing import Any, Dict, List, Optional


def compute_percentiles(latencies: List[float]) -> Dict[str, float]:
    if not latencies:
        return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "min": 0.0, "max": 0.0, "mean": 0.0}

    s = sorted(latencies)
    n = len(s)

    def p(pct: float) -> float:
        idx = int(pct * (n - 1))
        return s[idx]

    return {
        "p50": round(p(0.50), 3),
        "p95": round(p(0.95), 3),
        "p99": round(p(0.99), 3),
        "min": round(s[0], 3),
        "max": round(s[-1], 3),
        "mean": round(statistics.mean(s), 3),
    }


@dataclass
class BenchmarkResult:
    name: str
    total_ops: int
    duration_sec: float
    ops_per_sec: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float
    mean_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_latencies(
        cls,
        name: str,
        latencies_ms: List[float],
        duration_sec: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BenchmarkResult:
        stats = compute_percentiles(latencies_ms)
        ops_per_sec = round(len(latencies_ms) / max(duration_sec, 0.000001), 2)
        return cls(
            name=name,
            total_ops=len(latencies_ms),
            duration_sec=round(duration_sec, 4),
            ops_per_sec=ops_per_sec,
            p50_ms=stats["p50"],
            p95_ms=stats["p95"],
            p99_ms=stats["p99"],
            min_ms=stats["min"],
            max_ms=stats["max"],
            mean_ms=stats["mean"],
            metadata=metadata or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "total_ops": self.total_ops,
            "duration_sec": self.duration_sec,
            "ops_per_sec": self.ops_per_sec,
            "latency_ms": {
                "p50": self.p50_ms,
                "p95": self.p95_ms,
                "p99": self.p99_ms,
                "min": self.min_ms,
                "max": self.max_ms,
                "mean": self.mean_ms,
            },
            "metadata": self.metadata,
        }
