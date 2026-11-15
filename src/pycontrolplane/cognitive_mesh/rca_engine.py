import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .anomaly_detector import AnomalyEvent


@dataclass
class IncidentReport:
    incident_id: str
    timestamp: float
    severity: str
    summary: str
    root_cause: str
    affected_components: List[str]
    context: Dict[str, Any] = field(default_factory=dict)
    recommended_playbook: str = "AUTO_REMEDIATE"


class RootCauseAnalyzer:
    """Cognitive Root Cause Analysis (RCA) engine synthesizing cross-telemetry incidents."""

    def diagnose(
        self,
        anomalies: List[AnomalyEvent],
        context: Optional[Dict[str, Any]] = None,
    ) -> IncidentReport:
        ctx = context or {}
        incident_id = f"inc_{uuid.uuid4().hex[:8]}"
        now = time.time()

        metric_names = [a.metric_name for a in anomalies]
        max_z = max((a.z_score for a in anomalies), default=0.0)

        # Severity classification
        if max_z > 4.0 or "error_rate" in metric_names:
            severity = "CRITICAL"
        elif max_z > 2.5:
            severity = "WARNING"
        else:
            severity = "INFO"

        # Synthesis
        if "error_rate" in metric_names and "latency_ms" in metric_names:
            summary = "Correlated cascade: High latency spike accompanied by elevated error rates"
            root_cause = "Upstream provider saturation causing request queuing and downstream timeouts"
            components = ["ai_gateway", "upstream_llm_cluster"]
            playbook = "FAILOVER_AND_SHED_LOAD"
        elif "latency_ms" in metric_names:
            summary = "High latency spike detected across execution pipeline"
            root_cause = "Transient network packet loss or backend processing stall"
            components = ["network_fabric", "model_router"]
            playbook = "DYNAMIC_THROTTLE"
        elif "error_rate" in metric_names:
            summary = "Elevated error rate breach detected"
            root_cause = "Upstream model endpoint returning HTTP 5xx or rate limit rejections"
            components = ["upstream_provider"]
            playbook = "TRIP_CIRCUIT_AND_FALLBACK"
        else:
            summary = f"Telemetry variance anomaly detected in {metric_names}"
            root_cause = "Unclassified distribution shift in streaming metrics"
            components = ["system_telemetry"]
            playbook = "OBSERVE_AND_SAMPLE"

        return IncidentReport(
            incident_id=incident_id,
            timestamp=now,
            severity=severity,
            summary=summary,
            root_cause=root_cause,
            affected_components=components,
            context=ctx,
            recommended_playbook=playbook,
        )
