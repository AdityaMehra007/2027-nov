import os
import pytest
from omniverse.modules.agency.models import JobOrder, ServiceType, OrderStatus
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory
from omniverse.modules.agency.fulfillment.marketing_factory import MarketingFactory
from omniverse.modules.agency.fulfillment.automation_factory import AutomationFactory


def test_code_factory_builds_fullstack_project(tmp_path):
    factory = CodeFactory(output_root=str(tmp_path / "code_builds"))
    order = JobOrder(
        client_id="client_test_001",
        service_type=ServiceType.FULLSTACK_DEV,
        brief="Build AI analytics dashboard landing page with dark mode and fastapi backend",
        budget_usd=3000.0,
    )
    deliverables = factory.build_project(order)
    assert len(deliverables) >= 3

    artifact_names = [d.artifact_name for d in deliverables]
    assert "index.html" in artifact_names
    assert "main.py" in artifact_names
    assert "README.md" in artifact_names

    for d in deliverables:
        assert os.path.exists(d.file_path)
        assert d.size_bytes > 0
        assert len(d.checksum) == 64  # SHA256 length


def test_marketing_factory_builds_campaign(tmp_path):
    factory = MarketingFactory(output_root=str(tmp_path / "marketing_builds"))
    order = JobOrder(
        client_id="client_test_002",
        service_type=ServiceType.MARKETING_SUITE,
        brief="Launch high-ticket dental aesthetics growth marketing campaign in Koramangala",
        budget_usd=2000.0,
    )
    deliverables = factory.build_campaign(order)
    assert len(deliverables) >= 4

    artifact_names = [d.artifact_name for d in deliverables]
    assert "sales_copy.md" in artifact_names
    assert "ad_pack.json" in artifact_names
    assert "email_drip_sequence.md" in artifact_names
    assert "schema_org.json" in artifact_names

    for d in deliverables:
        assert os.path.exists(d.file_path)
        assert d.artifact_type == "MARKETING"


def test_automation_factory_builds_agent_bundle(tmp_path):
    factory = AutomationFactory(output_root=str(tmp_path / "agent_builds"))
    order = JobOrder(
        client_id="client_test_003",
        service_type=ServiceType.AGENT_AUTOMATION,
        brief="Build 24/7 autonomous WhatsApp customer support agent with inventory tools",
        budget_usd=4000.0,
    )
    deliverables = factory.build_agent_bundle(order)
    assert len(deliverables) >= 3

    artifact_names = [d.artifact_name for d in deliverables]
    assert "agent_runtime.py" in artifact_names
    assert "mcp_tools.json" in artifact_names
    assert "webhook_bot.py" in artifact_names

    for d in deliverables:
        assert os.path.exists(d.file_path)
        assert d.artifact_type == "AGENT_SPEC"
