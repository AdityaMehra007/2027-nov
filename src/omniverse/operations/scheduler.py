import time
from typing import Dict, Any, Callable, List

class ScheduledJob:
    def __init__(self, name: str, interval_seconds: int, job_func: Callable[[], Any]):
        self.name = name
        self.interval_seconds = interval_seconds
        self.job_func = job_func
        self.last_run: float = 0.0
        self.run_count: int = 0

    def should_run(self, current_time: float) -> bool:
        return (current_time - self.last_run) >= self.interval_seconds

    def execute(self, current_time: float) -> Any:
        self.last_run = current_time
        self.run_count += 1
        return self.job_func()

class OmniverseScheduler:
    """Manages recurring automated routines and audits."""

    def __init__(self):
        self._jobs: Dict[str, ScheduledJob] = {}

    def register_job(self, name: str, interval_seconds: int, job_func: Callable[[], Any]) -> None:
        self._jobs[name] = ScheduledJob(name, interval_seconds, job_func)

    def list_jobs(self) -> List[str]:
        return list(self._jobs.keys())

    def run_pending(self) -> Dict[str, Any]:
        now = time.time()
        results = {}
        for name, job in self._jobs.items():
            if job.should_run(now):
                try:
                    res = job.execute(now)
                    results[name] = {"status": "SUCCESS", "result": res}
                except Exception as e:
                    results[name] = {"status": "FAILED", "error": str(e)}
        return results
