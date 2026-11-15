import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AnomalyEvent:
    metric_name: str
    observed_value: float
    threshold: float
    z_score: float
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class AnomalyDetector:
    """Streaming statistical anomaly detector using rolling Z-score evaluation."""

    def __init__(self, window_size: int = 30, z_score_threshold: float = 2.5):
        self.window_size = window_size
        self.z_score_threshold = z_score_threshold
        self.windows: Dict[str, List[float]] = {}

    def record_metric(self, metric_name: str, value: float) -> Optional[AnomalyEvent]:
        if metric_name not in self.windows:
            self.windows[metric_name] = []

        window = self.windows[metric_name]
        
        # We need at least 5 points to form a baseline
        if len(window) < 5:
            window.append(value)
            return None

        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std_dev = math.sqrt(variance)

        # Append new value to window
        if len(window) >= self.window_size:
            window.pop(0)
        window.append(value)

        # Check for anomaly
        if std_dev > 1e-6:
            z_score = abs(value - mean) / std_dev
            if z_score >= self.z_score_threshold:
                return AnomalyEvent(
                    metric_name=metric_name,
                    observed_value=value,
                    threshold=mean + (self.z_score_threshold * std_dev),
                    z_score=z_score,
                )

        return None
