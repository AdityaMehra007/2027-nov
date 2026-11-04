"""Omniverse Core Subsystem: Configuration, Database, Security Governance, and Telemetry."""

from omniverse.core.config import OmniverseSettings, get_settings
from omniverse.core.database import DatabaseEngine, get_session
from omniverse.core.security import SecurityGovernor, ActionType, ApprovalStatus
from omniverse.core.telemetry import EventBus
from omniverse.core.llm_arbitrator import (
    ModelProvider,
    ModelTier,
    TaskCategory,
    ModelSpec,
    ArbitrationRequest,
    ArbitrationResult,
    ArbitrationResponse,
    HybridLLMArbitrator
)

# Deferred dynamic import for Conglomerate to eliminate circular import chains
def __getattr__(name: str):
    if name in ("AutonomousConglomerateKernel", "ConglomerateMetrics", "ConglomerateCycleReport"):
        import omniverse.core.conglomerate as _conglomerate
        return getattr(_conglomerate, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "OmniverseSettings",
    "get_settings",
    "DatabaseEngine",
    "get_session",
    "SecurityGovernor",
    "ActionType",
    "ApprovalStatus",
    "EventBus",
    "ModelProvider",
    "ModelTier",
    "TaskCategory",
    "ModelSpec",
    "ArbitrationRequest",
    "ArbitrationResult",
    "ArbitrationResponse",
    "HybridLLMArbitrator",
    "AutonomousConglomerateKernel",
    "ConglomerateMetrics",
    "ConglomerateCycleReport",
]
