import pytest
from pathlib import Path
from omniverse.modules.agency.models import JobOrder, ServiceType, OrderStatus
from omniverse.modules.agency.fulfillment.code_factory import CodeFactory
from omniverse.modules.agency.portal_engine import AgencyPortalEngine
from omniverse.modules.agency.revision_manager import AutonomousRevisionAgent, RevisionResult


def test_autonomous_revision_agent_refactors_and_qa_verifies(tmp_path):
    portal = AgencyPortalEngine(bundles_root=str(tmp_path / "bundles"))
    code_factory = CodeFactory(output_root=str(tmp_path / "code"))

    order = JobOrder(
        client_id="client_rev_1",
        service_type=ServiceType.FULLSTACK_DEV,
        brief="Landing page for AI agency",
        budget_usd=3000.0,
    )
    order.deliverables = code_factory.build_project(order)
    portal.register_order(order)

    # Initial bundle
    initial_zip = portal.package_order_bundle(order)
    assert initial_zip.exists()

    agent = AutonomousRevisionAgent(portal_engine=portal)
    result = agent.apply_revision(
        order=order,
        feedback="Add dark mode high-contrast palette and tier-3 enterprise pricing section",
    )

    assert isinstance(result, RevisionResult)
    assert result.qa_verified is True
    assert len(result.files_updated) >= 1
    assert "dark mode" in result.summary.lower() or "enterprise pricing" in result.summary.lower()

    # Verify deliverable content updated on disk
    for d in order.deliverables:
        if d.artifact_name == "index.html":
            content = Path(d.file_path).read_text(encoding="utf-8")
            assert "dark" in content.lower() or "pricing" in content.lower()
            assert d.qa_passed is True

    # Bundle updated
    assert Path(result.zip_bundle_path).exists()


def test_revision_manager_handles_marketing_copy(tmp_path):
    from omniverse.modules.agency.fulfillment.marketing_factory import MarketingFactory

    portal = AgencyPortalEngine(bundles_root=str(tmp_path / "bundles"))
    mktg_factory = MarketingFactory(output_root=str(tmp_path / "mktg"))

    order = JobOrder(
        client_id="client_mktg_rev",
        service_type=ServiceType.MARKETING_SUITE,
        brief="Copywriting campaign for SaaS",
        budget_usd=2500.0,
    )
    order.deliverables = mktg_factory.build_campaign(order)
    portal.register_order(order)

    agent = AutonomousRevisionAgent(portal_engine=portal)
    result = agent.apply_revision(
        order=order,
        feedback="Include money-back guarantee and urgency countdown in sales copy",
    )

    assert result.qa_verified is True
    for d in order.deliverables:
        if d.artifact_name == "sales_copy.md":
            copy_text = Path(d.file_path).read_text(encoding="utf-8")
            assert "guarantee" in copy_text.lower()
