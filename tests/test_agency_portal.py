import os
import zipfile
import pytest
from pathlib import Path
from omniverse.modules.agency.models import (
    ClientAccount,
    JobOrder,
    ServiceType,
    OrderStatus,
    Deliverable,
)
from omniverse.modules.agency.portal_engine import AgencyPortalEngine


def test_portal_engine_client_management(tmp_path):
    portal = AgencyPortalEngine(bundles_root=str(tmp_path / "bundles"))
    client = portal.create_client(name="Marcus Vance", email="marcus@vancetech.io", company="Vance Tech Global")

    assert client.client_id is not None
    assert len(client.access_token) >= 32

    # Authenticate with valid token
    auth_client = portal.authenticate_client(client.access_token)
    assert auth_client is not None
    assert auth_client.email == "marcus@vancetech.io"

    # Authenticate with invalid token
    invalid = portal.authenticate_client("bad_token_12345")
    assert invalid is None


def test_portal_engine_package_deliverable_zip(tmp_path):
    bundles_dir = tmp_path / "bundles"
    portal = AgencyPortalEngine(bundles_root=str(bundles_dir))

    # Create dummy files
    order_dir = tmp_path / "artifacts" / "ord_100"
    order_dir.mkdir(parents=True)
    f1 = order_dir / "index.html"
    f1.write_text("<!DOCTYPE html><html><body>Test</body></html>", encoding="utf-8")
    f2 = order_dir / "main.py"
    f2.write_text("print('API live')", encoding="utf-8")

    order = JobOrder(
        client_id="client_test",
        service_type=ServiceType.FULLSTACK_DEV,
        brief="Test deliverable packaging",
        budget_usd=2500.0,
        status=OrderStatus.QA_VERIFIED,
        deliverables=[
            Deliverable(artifact_name="index.html", artifact_type="CODE", file_path=str(f1), checksum="111", size_bytes=len(f1.read_bytes()), qa_passed=True),
            Deliverable(artifact_name="main.py", artifact_type="CODE", file_path=str(f2), checksum="222", size_bytes=len(f2.read_bytes()), qa_passed=True),
        ]
    )

    zip_path = portal.package_order_bundle(order)
    assert os.path.exists(zip_path)
    assert zip_path.suffix == ".zip"

    # Verify zip archive contents
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        assert "index.html" in namelist
        assert "main.py" in namelist
        assert "README.md" in namelist or "MANIFEST.json" in namelist


def test_portal_engine_settle_order_payment(tmp_path):
    portal = AgencyPortalEngine(bundles_root=str(tmp_path / "bundles"))
    client = portal.create_client(name="Sarah Connor", email="sarah@skynet-defense.com", company="Cyberdyne")

    order = JobOrder(
        client_id=client.client_id,
        service_type=ServiceType.AGENT_AUTOMATION,
        brief="Defense AI agent automation",
        budget_usd=5000.0,
        status=OrderStatus.QA_VERIFIED,
    )

    settlement = portal.settle_order_payment(order=order, client=client, payment_method="STRIPE")
    assert settlement["status"] == "RECONCILED"
    assert settlement["amount_usd"] == 5000.0
    assert order.status == OrderStatus.PAID
    assert client.lifetime_spend_usd == 5000.0
