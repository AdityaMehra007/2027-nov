import pytest
import os
from omniverse.core.config import OmniverseSettings
from omniverse.core.security import SecurityGovernor, ActionType, ApprovalStatus
from omniverse.core.telemetry import EventBus
from omniverse.core.database import DatabaseEngine

def test_config_defaults():
    settings = OmniverseSettings()
    assert settings.app_name == "CASHFLOW INFINITY: OMNIVERSE"
    assert settings.env in ("development", "staging", "production")
    assert settings.safety_budget_daily_usd >= 10.0
    assert "sqlite" in settings.db_url or "postgresql" in settings.db_url

def test_security_governor_approval():
    governor = SecurityGovernor()
    
    # Financial movement requires approval
    status = governor.check_action(ActionType.FINANCIAL_TRANSFER, details={"amount": 500})
    assert status == ApprovalStatus.REQUIRES_APPROVAL
    assert not governor.is_permitted(ActionType.FINANCIAL_TRANSFER)
    
    # After granting approval
    req_id = governor.request_approval(ActionType.FINANCIAL_TRANSFER, details={"amount": 500})
    governor.grant_approval(req_id)
    assert governor.is_permitted(ActionType.FINANCIAL_TRANSFER, req_id=req_id)

def test_telemetry_event_bus():
    bus = EventBus()
    bus.publish("SYSTEM_STARTUP", {"version": "1.0.0"})
    bus.publish("LEAD_CREATED", {"lead_id": 1, "business": "Acme Cafe"})
    
    events = bus.get_events()
    assert len(events) == 2
    assert events[0]["event_name"] == "SYSTEM_STARTUP"
    assert events[1]["payload"]["business"] == "Acme Cafe"

def test_database_engine(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()
    with db.get_session() as session:
        assert session is not None
