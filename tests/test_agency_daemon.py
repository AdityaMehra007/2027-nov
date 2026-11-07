import pytest
from omniverse.modules.agency.daemon import AutonomousAgencyDaemon, AgencyCycleReport


def test_agency_daemon_single_cycle():
    daemon = AutonomousAgencyDaemon()
    report = daemon.run_cycle(limit=2, budget_per_order=3000.0)

    assert isinstance(report, AgencyCycleReport)
    assert report.cycle_number >= 1
    assert report.leads_hunted == 2
    assert report.audits_performed == 2
    assert report.pitches_generated == 2
    assert report.deliverables_completed >= 2
    assert report.pipeline_value_generated_usd > 0.0
    assert report.duration_sec >= 0.0


def test_agency_daemon_summary():
    daemon = AutonomousAgencyDaemon()
    daemon.run_cycle(limit=1, budget_per_order=2500.0)
    summary = daemon.get_aggregate_summary()

    assert summary["total_cycles_executed"] >= 1
    assert summary["total_leads_processed"] >= 1
    assert summary["pipeline_value_usd"] >= 2500.0
