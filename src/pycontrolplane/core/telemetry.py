import time
import uuid
import math
from typing import Dict, Any, List, Optional


class LatencyHistogram:
    """High-resolution latency histogram tracking distributions and percentiles."""

    def __init__(self, max_samples: int = 10000):
        self.max_samples = max_samples
        self.samples: List[float] = []
        self._is_sorted = True
        self.count = 0
        self.total_ms = 0.0

    def record(self, latency_ms: float) -> None:
        if len(self.samples) >= self.max_samples:
            self.samples.pop(0)
        self.samples.append(latency_ms)
        self.count += 1
        self.total_ms += latency_ms
        self._is_sorted = False

    def percentile(self, p: float) -> float:
        """Calculate the p-th percentile (0 <= p <= 100)."""
        if not self.samples:
            return 0.0
        if not self._is_sorted:
            self.samples.sort()
            self._is_sorted = True

        if p <= 0:
            return self.samples[0]
        if p >= 100:
            return self.samples[-1]

        k = (len(self.samples) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return self.samples[int(k)]
        d0 = self.samples[int(f)] * (c - k)
        d1 = self.samples[int(c)] * (k - f)
        return d0 + d1

    @property
    def mean(self) -> float:
        return (self.total_ms / self.count) if self.count > 0 else 0.0


class Span:
    """Distributed tracing span representing an isolated operation within a trace."""

    def __init__(
        self,
        name: str,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str] = None,
        tracer: Optional["Tracer"] = None,
    ):
        self.name = name
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.tracer = tracer
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration_ms: float = 0.0
        self.tags: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []

    def set_tag(self, key: str, value: Any) -> "Span":
        self.tags[key] = value
        return self

    def log_event(self, name: str, payload: Optional[Dict[str, Any]] = None) -> None:
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "payload": payload or {},
        })

    def start(self) -> "Span":
        self.start_time = time.perf_counter()
        return self

    def finish(self) -> None:
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        if self.tracer:
            self.tracer._record_span(self)

    def __enter__(self) -> "Span":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.set_tag("error", True)
            self.set_tag("error.message", str(exc_val))
        self.finish()


class Tracer:
    """W3C-aligned distributed tracer managing trace contexts and completed spans."""

    def __init__(self, service_name: str = "pycontrolplane"):
        self.service_name = service_name
        self.completed_spans: List[Span] = []

    def start_span(
        self,
        name: str,
        parent: Optional[Span] = None,
        trace_id: Optional[str] = None,
    ) -> Span:
        if parent:
            active_trace_id = parent.trace_id
            parent_span_id = parent.span_id
        else:
            active_trace_id = trace_id or uuid.uuid4().hex
            parent_span_id = None

        new_span_id = uuid.uuid4().hex[:16]
        span = Span(
            name=name,
            trace_id=active_trace_id,
            span_id=new_span_id,
            parent_span_id=parent_span_id,
            tracer=self,
        )
        span.set_tag("service.name", self.service_name)
        return span

    def _record_span(self, span: Span) -> None:
        self.completed_spans.append(span)


class MetricsRegistry:
    """Central metrics collector for counters, gauges, and histograms."""

    def __init__(self):
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, LatencyHistogram] = {}

    def inc_counter(self, name: str, value: float = 1.0) -> None:
        self.counters[name] = self.counters.get(name, 0.0) + value

    def set_gauge(self, name: str, value: float) -> None:
        self.gauges[name] = value

    def record_latency(self, name: str, latency_ms: float) -> None:
        if name not in self.histograms:
            self.histograms[name] = LatencyHistogram()
        self.histograms[name].record(latency_ms)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                k: {
                    "count": h.count,
                    "p50": h.percentile(50),
                    "p90": h.percentile(90),
                    "p99": h.percentile(99),
                    "mean": h.mean,
                }
                for k, h in self.histograms.items()
            },
        }
