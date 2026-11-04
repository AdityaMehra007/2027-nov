import pytest
from pathlib import Path
from sqlmodel import Session
from omniverse.operations.health import HealthDiagnostics
from omniverse.operations.scheduler import OmniverseScheduler
from omniverse.operations.worker import WorkerDaemon
from omniverse.operations.reporter import ExecutiveReportGenerator

def test_health_diagnostics(test_db: Session):
    diagnostics = HealthDiagnostics(session=test_db)
    health = diagnostics.run_diagnostics()
    
    assert health["database_status"] == "HEALTHY"
    assert "memory_usage_mb" in health
    assert "disk_available_gb" in health
    assert health["overall_status"] == "OK"

def test_scheduler_task_registration():
    scheduler = OmniverseScheduler()
    executed = []
    
    def sample_job():
        executed.append(True)
        return "SUCCESS"
        
    scheduler.register_job("sample_check", interval_seconds=1, job_func=sample_job)
    assert "sample_check" in scheduler.list_jobs()
    
    scheduler.run_pending()
    assert len(executed) == 1

def test_worker_daemon_iteration(test_db: Session):
    worker = WorkerDaemon(session=test_db, max_cycles=1)
    results = worker.run_cycle()
    
    assert "cycle_timestamp" in results
    assert "health_check" in results
    assert results["health_check"]["overall_status"] == "OK"

def test_executive_report_generation(test_db: Session, tmp_path):
    reporter = ExecutiveReportGenerator(session=test_db, output_dir=tmp_path)
    report_file = reporter.generate_daily_brief()
    
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "CASHFLOW INFINITY: OMNIVERSE" in content
    assert "EXECUTIVE BRIEF" in content
    assert "Financial Ledger" in content
