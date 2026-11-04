import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from omniverse.core.database import DatabaseEngine
from omniverse.core.config import get_settings
from omniverse.core.security import SecurityGovernor, ActionType
from omniverse.core.telemetry import global_event_bus
from omniverse.agents.executive import ChiefRevenueArchitect
from omniverse.agents.commercial import SalesDirector
from omniverse.agents.quant import QuantAnalyst
from omniverse.agents.base import AgentTask
from omniverse.modules.revenue.agency import GrowthKitGenerator
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.revenue.models import LeadStage
from omniverse.modules.intelligence.quant_engine import Backtester, PaperTradingEngine, TradeDirection
from omniverse.modules.intelligence.research import CompanyIntelligenceEngine
from omniverse.operations.health import HealthDiagnostics
from omniverse.api.app import create_app

def test_full_omniverse_lifecycle_e2e(tmp_path):
    # 1. Setup isolated database
    db_file = tmp_path / "omniverse_e2e.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()

    # 2. Executive Agent prioritisation
    architect = ChiefRevenueArchitect()
    opp_eval = architect.execute_task(AgentTask(
        task_type="evaluate_opportunity",
        payload={"niche": "Specialty Bakery", "city": "Bengaluru", "urgency": "High"}
    ))
    assert opp_eval["priority_level"] == "HIGH"

    # 3. Commercial Agent pitch preparation
    sales_dir = SalesDirector()
    pitch = sales_dir.execute_task(AgentTask(
        task_type="prepare_pitch",
        payload={"business_name": "Lumiere Pastry", "estimated_value_inr": 25000.0}
    ))
    assert "Lumiere Pastry" in pitch["pitch_strategy"]

    # 4. Generate Production Growth Kit
    kit_gen = GrowthKitGenerator()
    kit = kit_gen.generate("Lumiere Pastry", "Specialty Bakery", "Bengaluru")
    assert len(kit.social_captions) == 10
    assert len(kit.promotional_hooks) == 5

    # 5. Pipeline Progression & Payment Reconciliation
    with db_engine.get_session() as session:
        pipeline = LeadPipeline(session)
        lead = pipeline.create_lead(
            business_name="Lumiere Pastry",
            category="Specialty Bakery",
            city="Bengaluru",
            estimated_value_inr=25000.0
        )
        assert lead.status == LeadStage.NEW

        pipeline.advance_stage(lead.id, LeadStage.QUALIFIED)
        pipeline.advance_stage(lead.id, LeadStage.WON)

        payments = PaymentWorkflow(session)
        invoice = payments.create_invoice(lead.id, 25000.0)
        payments.record_payment(invoice.id, reference="UPI-SUCCESS-8841")

        ledger = payments.get_financial_ledger()
        assert ledger["collected_revenue_inr"] == 25000.0
        assert ledger["outstanding_receivables_inr"] == 0.0

    # 6. Quant Engine & Risk Validation
    backtester = Backtester()
    prices = [100.0, 105.0, 103.0, 110.0, 115.0, 125.0]
    bt_res = backtester.run_trend_following_backtest(prices)
    assert bt_res["total_return_pct"] == 25.0

    quant_analyst = QuantAnalyst()
    risk_review = quant_analyst.execute_task(AgentTask(
        task_type="risk_assessment",
        payload={"max_drawdown_pct": bt_res["max_drawdown_pct"], "sharpe_ratio": bt_res["sharpe_ratio"]}
    ))
    assert risk_review["risk_verdict"] == "APPROVED"

    with db_engine.get_session() as session:
        paper_engine = PaperTradingEngine(session, initial_capital_inr=500000.0)
        paper_trade = paper_engine.execute_order("TCS", TradeDirection.BUY, 10, 3500.0)
        assert paper_trade.id is not None

    # 7. Operational Health Probe
    with db_engine.get_session() as session:
        diagnostics = HealthDiagnostics(session)
        health = diagnostics.run_diagnostics()
        assert health["overall_status"] == "OK"
        assert health["database_status"] == "HEALTHY"

    # 8. API Verification
    app = create_app(db_engine=db_engine)
    with TestClient(app) as client:
        summary_res = client.get("/api/v1/dashboard/summary")
        assert summary_res.status_code == 200
        summary_data = summary_res.json()
        assert summary_data["financial_ledger"]["collected_revenue_inr"] == 25000.0
        assert summary_data["pipeline_summary"]["total_leads"] == 1
