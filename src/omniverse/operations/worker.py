import time
from typing import Dict, Any, Optional
from sqlmodel import Session
from omniverse.operations.health import HealthDiagnostics
from omniverse.operations.scheduler import OmniverseScheduler
from omniverse.core.telemetry import global_event_bus

class WorkerDaemon:
    """Continuous operations worker managing periodic health checks,

    pipeline integrity audits, and reporting.
    """

    def __init__(self, session: Session, max_cycles: Optional[int] = None):
        self.session = session
        self.max_cycles = max_cycles
        self.diagnostics = HealthDiagnostics(session)
        self.scheduler = OmniverseScheduler()
        self._setup_default_jobs()

    def _setup_default_jobs(self) -> None:
        self.scheduler.register_job(
            "health_audit",
            interval_seconds=60,
            job_func=self.diagnostics.run_diagnostics
        )

    def run_cycle(self) -> Dict[str, Any]:
        """Runs a single background evaluation cycle."""
        now = time.time()
        health = self.diagnostics.run_diagnostics()
        scheduled_results = self.scheduler.run_pending()

        global_event_bus.publish("WORKER_CYCLE_EXECUTED", {
            "timestamp": now,
            "overall_status": health.get("overall_status")
        })

        return {
            "cycle_timestamp": now,
            "health_check": health,
            "scheduled_jobs": scheduled_results
        }
