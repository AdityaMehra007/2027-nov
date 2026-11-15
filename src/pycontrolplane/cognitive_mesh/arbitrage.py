from enum import Enum
from dataclasses import dataclass
from typing import Dict


class WorkloadObjective(str, Enum):
    LOW_COST = "LOW_COST"
    LOW_LATENCY = "LOW_LATENCY"
    LOW_CARBON = "LOW_CARBON"


@dataclass
class RegionProfile:
    name: str
    cost_per_mflop: float
    latency_p50_ms: float
    carbon_intensity_g_kwh: float


class ComputeArbitrageEngine:
    """Multi-dimensional dynamic compute dispatcher balancing cost, latency, and carbon intensity."""

    def __init__(self):
        self.regions: Dict[str, RegionProfile] = {}

    def register_region(
        self,
        name: str,
        cost_per_mflop: float,
        latency_p50_ms: float,
        carbon_intensity_g_kwh: float,
    ) -> None:
        self.regions[name] = RegionProfile(
            name=name,
            cost_per_mflop=cost_per_mflop,
            latency_p50_ms=latency_p50_ms,
            carbon_intensity_g_kwh=carbon_intensity_g_kwh,
        )

    def select_region(self, objective: WorkloadObjective = WorkloadObjective.LOW_LATENCY) -> str:
        if not self.regions:
            raise RuntimeError("No compute regions registered for arbitrage")

        if objective == WorkloadObjective.LOW_COST:
            # Sort by cost ascending, tie break by latency
            return min(self.regions.values(), key=lambda r: (r.cost_per_mflop, r.latency_p50_ms)).name
        elif objective == WorkloadObjective.LOW_LATENCY:
            # Sort by latency ascending, tie break by cost
            return min(self.regions.values(), key=lambda r: (r.latency_p50_ms, r.cost_per_mflop)).name
        elif objective == WorkloadObjective.LOW_CARBON:
            # Sort by carbon intensity ascending, tie break by cost
            return min(self.regions.values(), key=lambda r: (r.carbon_intensity_g_kwh, r.cost_per_mflop)).name
        else:
            return next(iter(self.regions.keys()))
