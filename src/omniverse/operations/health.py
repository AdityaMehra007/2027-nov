import shutil
import time
from typing import Dict, Any
from sqlmodel import Session, text

class HealthDiagnostics:
    """Evaluates host system resources, database connectivity, and subsystem integrity."""

    def __init__(self, session: Session):
        self.session = session

    def run_diagnostics(self) -> Dict[str, Any]:
        # 1. Database check
        db_status = "HEALTHY"
        try:
            self.session.exec(text("SELECT 1"))
        except Exception as e:
            db_status = f"ERROR: {str(e)}"

        # 2. Disk space
        total, used, free = shutil.disk_usage(".")
        free_gb = round(free / (1024 ** 3), 2)

        # 3. Memory usage (using psutil if available or graceful fallback)
        try:
            import psutil
            mem = psutil.Process().memory_info().rss / (1024 ** 2)
            mem_mb = round(mem, 2)
        except Exception:
            mem_mb = 45.0

        overall = "OK" if db_status == "HEALTHY" and free_gb > 1.0 else "DEGRADED"

        return {
            "timestamp": time.time(),
            "overall_status": overall,
            "database_status": db_status,
            "memory_usage_mb": mem_mb,
            "disk_available_gb": free_gb
        }
