"""
PyControlPlane: The Tri-Epoch Autonomous Enterprise Cognitive Control Plane.

Bridges:
- Epoch 1 (Has Built): Distributed Telemetry, Circuit Breaking, Rate Limiting & Tamper-Evident Merkle Auditing.
- Epoch 2 (Is Building): Semantic AI Gateway, Cascading Model Routing, Exact/Cosine Caching & Guardrail Firewalls.
- Epoch 3 (Will Be Building): Autonomous Cognitive SRE, Anomaly Detection, Root Cause Analysis, Self-Healing & Byzantine Multi-Agent Consensus.
"""

from .core.telemetry import Tracer, Span, LatencyHistogram, MetricsRegistry
from .core.circuit_breaker import CircuitBreaker, CircuitState, CircuitBreakerOpenException
from .core.rate_limiter import TokenBucketRateLimiter
from .core.retry import RetryPolicy, ResilienceExecutor
from .core.audit import MerkleAuditLedger, AuditRecord

from .ai_gateway.router import SmartModelRouter, ModelTier, ModelEndpoint, RouteResult
from .ai_gateway.semantic_cache import SemanticCache
from .ai_gateway.guardrails import GuardrailFirewall, SecurityViolationException
from .ai_gateway.model_provider import ModelProvider, MockModelProvider

from .cognitive_mesh.anomaly_detector import AnomalyDetector, AnomalyEvent
from .cognitive_mesh.rca_engine import RootCauseAnalyzer, IncidentReport
from .cognitive_mesh.self_healer import SelfHealingSupervisor, RemediationAction, RemediationResult
from .cognitive_mesh.consensus import AgentConsensusGovernor, AgentVote
from .cognitive_mesh.arbitrage import ComputeArbitrageEngine, WorkloadObjective

from .orchestrator import ControlPlaneOrchestrator, ControlPlaneRequest, ControlPlaneResponse

__version__ = "1.0.0"

__all__ = [
    # Core
    "Tracer",
    "Span",
    "LatencyHistogram",
    "MetricsRegistry",
    "CircuitBreaker",
    "CircuitState",
    "CircuitBreakerOpenException",
    "TokenBucketRateLimiter",
    "RetryPolicy",
    "ResilienceExecutor",
    "MerkleAuditLedger",
    "AuditRecord",
    # AI Gateway
    "SmartModelRouter",
    "ModelTier",
    "ModelEndpoint",
    "RouteResult",
    "SemanticCache",
    "GuardrailFirewall",
    "SecurityViolationException",
    "ModelProvider",
    "MockModelProvider",
    # Cognitive Mesh
    "AnomalyDetector",
    "AnomalyEvent",
    "RootCauseAnalyzer",
    "IncidentReport",
    "SelfHealingSupervisor",
    "RemediationAction",
    "RemediationResult",
    "AgentConsensusGovernor",
    "AgentVote",
    "ComputeArbitrageEngine",
    "WorkloadObjective",
    # Orchestrator
    "ControlPlaneOrchestrator",
    "ControlPlaneRequest",
    "ControlPlaneResponse",
]
