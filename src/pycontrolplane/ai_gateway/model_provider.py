import time
from typing import Dict, Any, Optional


class ModelProvider:
    """Base interface for underlying LLM / inference providers."""

    def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


class MockModelProvider(ModelProvider):
    """Deterministic mock provider for testing high-throughput routing & cascading fallbacks."""

    def __init__(
        self,
        name: str = "mock-model",
        simulate_failure: bool = False,
        latency_ms: float = 5.0,
        response_template: str = "Simulated response for: {prompt}",
    ):
        self.name = name
        self.simulate_failure = simulate_failure
        self.latency_ms = latency_ms
        self.response_template = response_template
        self.call_count = 0

    def generate(self, prompt: str, **kwargs: Any) -> str:
        self.call_count += 1
        if self.latency_ms > 0:
            time.sleep(self.latency_ms / 1000.0)

        if self.simulate_failure:
            raise RuntimeError(f"Simulated upstream provider outage in {self.name}")

        return self.response_template.format(prompt=prompt[:64])
