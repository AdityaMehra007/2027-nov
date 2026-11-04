import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from omniverse.core.conglomerate import (
    AutonomousConglomerateKernel,
    ConglomerateMetrics,
    ConglomerateCycleReport,
)
from omniverse.core.security import SecurityGovernor
from omniverse.modules.revenue.models import Lead, LeadStage


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_conglomerate_kernel_initialization(session: Session):
    kernel = AutonomousConglomerateKernel(session=session)
    metrics = kernel.get_executive_metrics()
    assert isinstance(metrics, ConglomerateMetrics)
    assert metrics.active_leads_count >= 0
    assert metrics.saas_portfolio_count >= 0
    assert metrics.system_health_score > 0.0


def test_conglomerate_kernel_single_cycle(session: Session, tmp_path):
    kernel = AutonomousConglomerateKernel(session=session, saas_output_dir=str(tmp_path))
    report = kernel.run_cycle(city="Bengaluru", niche="Hospitality")

    assert isinstance(report, ConglomerateCycleReport)
    assert report.cycle_id.startswith("CYC-")
    assert report.leads_discovered > 0
    assert report.growth_kits_generated > 0
    assert report.saas_scaffolded is not None
    assert report.quant_arbitrage_opportunities >= 0
    assert report.health_status in ("HEALTHY", "WARNING", "DEGRADED")

    # Verify metrics updated
    metrics = kernel.get_executive_metrics()
    assert metrics.active_leads_count > 0
    assert metrics.pipeline_value_inr > 0.0


def test_conglomerate_executive_briefing(session: Session, tmp_path):
    kernel = AutonomousConglomerateKernel(session=session, saas_output_dir=str(tmp_path))
    kernel.run_cycle(city="Bengaluru", niche="Retail")
    briefing = kernel.generate_executive_briefing()

    assert "AUTONOMOUS CONGLOMERATE EXECUTIVE BRIEFING" in briefing
    assert "Pipeline Value" in briefing
    assert "Collected Revenue" in briefing
    assert "SaaS Portfolio" in briefing
    assert "Quant Division" in briefing
