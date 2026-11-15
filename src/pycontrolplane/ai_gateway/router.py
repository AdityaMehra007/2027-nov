import time
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from .model_provider import ModelProvider
from ..core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException


class ModelTier(str, Enum):
    LOCAL = "LOCAL"          # On-premise / Edge / Pure-Python PyTransformer
    FAST = "FAST"            # High-throughput flash models (low latency, lowest cost)
    REASONING = "REASONING"  # Deep multi-step reasoning models


@dataclass
class ModelEndpoint:
    name: str
    tier: ModelTier
    provider: ModelProvider
    cost_per_1k: float = 0.001
    is_active: bool = True
    breaker: Optional[CircuitBreaker] = None

    def __post_init__(self):
        if self.breaker is None:
            self.breaker = CircuitBreaker(name=f"breaker_{self.name}", failure_threshold=3, recovery_timeout_sec=5.0)


@dataclass
class RouteResult:
    endpoint_name: str
    tier: ModelTier
    response_text: str
    cost: float
    latency_ms: float
    used_fallback: bool


class SmartModelRouter:
    """Dynamic LLM router supporting latency/cost optimization and zero-downtime cascading fallback."""

    def __init__(self):
        self.endpoints: Dict[str, ModelEndpoint] = {}
        # Fallback hierarchy
        self.fallback_order = {
            ModelTier.LOCAL: [ModelTier.LOCAL, ModelTier.FAST, ModelTier.REASONING],
            ModelTier.FAST: [ModelTier.FAST, ModelTier.REASONING, ModelTier.LOCAL],
            ModelTier.REASONING: [ModelTier.REASONING, ModelTier.FAST, ModelTier.LOCAL],
        }

    def register_endpoint(self, endpoint: ModelEndpoint) -> None:
        self.endpoints[endpoint.name] = endpoint

    def dispatch(
        self,
        prompt: str,
        preferred_tier: ModelTier = ModelTier.FAST,
        **kwargs: Any,
    ) -> RouteResult:
        candidate_tiers = self.fallback_order.get(preferred_tier, [preferred_tier])
        last_error: Optional[Exception] = None

        for tier in candidate_tiers:
            matching_endpoints = [
                ep for ep in self.endpoints.values()
                if ep.tier == tier and ep.is_active
            ]

            for ep in matching_endpoints:
                try:
                    if ep.breaker:
                        ep.breaker.check_execution()

                    start_time = time.perf_counter()
                    response_text = ep.provider.generate(prompt, **kwargs)
                    duration_ms = (time.perf_counter() - start_time) * 1000.0

                    if ep.breaker:
                        ep.breaker.record_success()

                    token_estimate = max(1, len(prompt.split()) + len(response_text.split()))
                    cost = (token_estimate / 1000.0) * ep.cost_per_1k

                    return RouteResult(
                        endpoint_name=ep.name,
                        tier=ep.tier,
                        response_text=response_text,
                        cost=cost,
                        latency_ms=duration_ms,
                        used_fallback=(ep.tier != preferred_tier),
                    )

                except Exception as exc:
                    if ep.breaker:
                        ep.breaker.record_failure()
                    last_error = exc
                    continue

        if last_error:
            raise RuntimeError(f"All model endpoints and fallbacks exhausted: {last_error}")
        raise RuntimeError("No active endpoints registered in routing table")
