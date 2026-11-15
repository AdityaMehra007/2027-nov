import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .core.telemetry import Tracer, MetricsRegistry, Span
from .core.circuit_breaker import CircuitBreaker
from .core.rate_limiter import TokenBucketRateLimiter
from .core.retry import RetryPolicy, ResilienceExecutor
from .core.audit import MerkleAuditLedger

from .ai_gateway.router import SmartModelRouter, ModelTier, ModelEndpoint, RouteResult
from .ai_gateway.semantic_cache import SemanticCache
from .ai_gateway.guardrails import GuardrailFirewall, SecurityViolationException
from .ai_gateway.model_provider import MockModelProvider

from .cognitive_mesh.anomaly_detector import AnomalyDetector
from .cognitive_mesh.rca_engine import RootCauseAnalyzer
from .cognitive_mesh.self_healer import SelfHealingSupervisor
from .cognitive_mesh.consensus import AgentConsensusGovernor
from .cognitive_mesh.arbitrage import ComputeArbitrageEngine, WorkloadObjective


@dataclass
class ControlPlaneRequest:
    tenant_id: str
    actor: str
    prompt: str
    preferred_tier: ModelTier = ModelTier.FAST
    embedding: Optional[List[float]] = None
    objective: WorkloadObjective = WorkloadObjective.LOW_LATENCY


@dataclass
class ControlPlaneResponse:
    success: bool
    content: str
    endpoint: str
    trace_id: str
    duration_ms: float
    cache_hit: bool = False
    is_semantic_cache: bool = False
    cost: float = 0.0
    error: Optional[str] = None


class ControlPlaneOrchestrator:
    """The Autonomous Enterprise Cognitive Control Plane integrating Epoch 1, 2, and 3."""

    def __init__(self, service_name: str = "titan-controlplane"):
        # Epoch 1: Core Distributed Resilience & Telemetry
        self.tracer = Tracer(service_name=service_name)
        self.metrics = MetricsRegistry()
        self.rate_limiters: Dict[str, TokenBucketRateLimiter] = {}
        self.audit_ledger = MerkleAuditLedger()

        # Epoch 2: AI Gateway & Semantic Layer
        self.guardrails = GuardrailFirewall(token_budget_per_minute=200000)
        self.semantic_cache = SemanticCache(similarity_threshold=0.90)
        self.router = SmartModelRouter()
        self._setup_default_endpoints()

        # Epoch 3: Cognitive Mesh & Self-Healing
        self.anomaly_detector = AnomalyDetector(window_size=25, z_score_threshold=2.5)
        self.rca_engine = RootCauseAnalyzer()
        self.self_healer = SelfHealingSupervisor()
        self.consensus_governor = AgentConsensusGovernor()
        self.arbitrage_engine = ComputeArbitrageEngine()
        self._setup_default_arbitrage_regions()

    def _setup_default_endpoints(self) -> None:
        p_flash = MockModelProvider(name="flash-provider", latency_ms=4.0)
        p_pro = MockModelProvider(name="pro-provider", latency_ms=15.0)
        p_local = MockModelProvider(name="local-provider", latency_ms=2.0)

        self.router.register_endpoint(ModelEndpoint(name="flash-core", tier=ModelTier.FAST, provider=p_flash, cost_per_1k=0.001))
        self.router.register_endpoint(ModelEndpoint(name="pro-core", tier=ModelTier.REASONING, provider=p_pro, cost_per_1k=0.015))
        self.router.register_endpoint(ModelEndpoint(name="local-edge", tier=ModelTier.LOCAL, provider=p_local, cost_per_1k=0.0002))

    def _setup_default_arbitrage_regions(self) -> None:
        self.arbitrage_engine.register_region("edge-zone-alpha", cost_per_mflop=0.012, latency_p50_ms=4.0, carbon_intensity_g_kwh=180.0)
        self.arbitrage_engine.register_region("cloud-us-east", cost_per_mflop=0.009, latency_p50_ms=35.0, carbon_intensity_g_kwh=360.0)
        self.arbitrage_engine.register_region("hydro-nordic-1", cost_per_mflop=0.007, latency_p50_ms=85.0, carbon_intensity_g_kwh=25.0)

    def _get_limiter(self, tenant_id: str) -> TokenBucketRateLimiter:
        if tenant_id not in self.rate_limiters:
            self.rate_limiters[tenant_id] = TokenBucketRateLimiter(capacity=100.0, refill_rate=20.0)
        return self.rate_limiters[tenant_id]

    def handle_request(self, req: ControlPlaneRequest) -> ControlPlaneResponse:
        start_total = time.perf_counter()
        with self.tracer.start_span("orchestrator_request") as root_span:
            root_span.set_tag("tenant.id", req.tenant_id)
            root_span.set_tag("actor", req.actor)
            root_span.set_tag("tier.preferred", req.preferred_tier.value)

            # 1. Rate Limiting Check (Epoch 1)
            limiter = self._get_limiter(req.tenant_id)
            if not limiter.acquire(1.0):
                self.metrics.inc_counter("rate_limit_exceeded")
                root_span.set_tag("error", True)
                root_span.set_tag("error.reason", "Rate limit exceeded")
                duration = (time.perf_counter() - start_total) * 1000.0
                return ControlPlaneResponse(
                    success=False,
                    content="",
                    endpoint="none",
                    trace_id=root_span.trace_id,
                    duration_ms=duration,
                    error="Tenant rate limit exceeded",
                )

            # 2. Guardrails & Safety Filter (Epoch 2)
            try:
                self.guardrails.inspect_prompt(req.prompt)
                clean_prompt, was_redacted = self.guardrails.sanitize_input(req.prompt)
                if was_redacted:
                    root_span.set_tag("security.pii_redacted", True)
            except SecurityViolationException as sve:
                self.metrics.inc_counter("security_violations")
                root_span.set_tag("error", True)
                root_span.set_tag("security.violation", str(sve))
                duration = (time.perf_counter() - start_total) * 1000.0
                return ControlPlaneResponse(
                    success=False,
                    content="",
                    endpoint="guardrails",
                    trace_id=root_span.trace_id,
                    duration_ms=duration,
                    error=str(sve),
                )

            # 3. Semantic & Exact Cache Lookup (Epoch 2)
            hit, cached_content, is_semantic = self.semantic_cache.get(clean_prompt, req.embedding)
            if hit and cached_content:
                self.metrics.inc_counter("cache_hit")
                duration = (time.perf_counter() - start_total) * 1000.0
                root_span.set_tag("cache.hit", True)
                root_span.set_tag("cache.is_semantic", is_semantic)

                self.audit_ledger.append_record(
                    actor=req.actor,
                    action="inference_cache_hit",
                    payload={"tenant_id": req.tenant_id, "prompt_hash": hash(clean_prompt), "semantic": is_semantic},
                )

                return ControlPlaneResponse(
                    success=True,
                    content=cached_content,
                    endpoint="cache",
                    trace_id=root_span.trace_id,
                    duration_ms=duration,
                    cache_hit=True,
                    is_semantic_cache=is_semantic,
                    cost=0.0,
                )

            self.metrics.inc_counter("cache_miss")

            # 4. Multi-Dimensional Arbitrage & Routing (Epoch 2 & 3)
            optimal_region = self.arbitrage_engine.select_region(req.objective)
            root_span.set_tag("compute.region", optimal_region)

            route_result = self.router.dispatch(prompt=clean_prompt, preferred_tier=req.preferred_tier)
            duration = (time.perf_counter() - start_total) * 1000.0

            # 5. Populate Cache
            self.semantic_cache.set(clean_prompt, route_result.response_text, req.embedding)

            # 6. Telemetry & Anomaly Analysis (Epoch 3)
            self.metrics.record_latency("request_latency_ms", duration)
            anomaly = self.anomaly_detector.record_metric("latency_ms", duration)
            if anomaly:
                root_span.set_tag("anomaly.detected", True)
                incident = self.rca_engine.diagnose([anomaly], context={"tenant": req.tenant_id})
                remediation = self.self_healer.formulate_remediation(anomaly)
                self.self_healer.execute_plan(remediation)

            # 7. Tamper-evident Audit Ledger
            self.audit_ledger.append_record(
                actor=req.actor,
                action="inference_executed",
                payload={
                    "tenant_id": req.tenant_id,
                    "endpoint": route_result.endpoint_name,
                    "tier": route_result.tier.value,
                    "cost": route_result.cost,
                    "duration_ms": duration,
                },
            )

            return ControlPlaneResponse(
                success=True,
                content=route_result.response_text,
                endpoint=route_result.endpoint_name,
                trace_id=root_span.trace_id,
                duration_ms=duration,
                cache_hit=False,
                cost=route_result.cost,
            )
