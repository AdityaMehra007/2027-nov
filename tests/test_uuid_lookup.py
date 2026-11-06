import uuid
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.modules.revenue.models import Lead, Invoice, Proposal, Offer, LeadStage, InvoiceStatus
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow


def is_valid_uuid4(val: str) -> bool:
    try:
        parsed = uuid.UUID(str(val), version=4)
        return str(parsed) == str(val)
    except (ValueError, TypeError, AttributeError):
        return False


@pytest.fixture(name="client")
def client_fixture(tmp_path):
    db_file = tmp_path / "uuid_test.db"
    db_engine = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db_engine.init_db()

    app = create_app(db_engine=db_engine)
    with TestClient(app) as test_client:
        yield test_client


def test_models_uuid_generation(test_db: Session):
    lead = Lead(
        business_name="Indiranagar Tech Lab",
        category="Tech",
        city="Bengaluru",
        estimated_value_inr=50000.0,
    )
    test_db.add(lead)
    test_db.commit()
    test_db.refresh(lead)

    assert lead.id is not None
    assert lead.uuid is not None
    assert is_valid_uuid4(lead.uuid)

    offer = Offer(
        title="Enterprise Growth Kit",
        niche="Tech",
        price_inr=30000.0,
        deliverables_summary="Full Stack Strategy",
    )
    test_db.add(offer)
    test_db.commit()
    test_db.refresh(offer)

    proposal = Proposal(
        lead_id=lead.id,
        offer_id=offer.id,
        custom_pitch="Accelerate Indiranagar Tech",
        pricing_inr=30000.0,
    )
    test_db.add(proposal)
    test_db.commit()
    test_db.refresh(proposal)

    assert proposal.id is not None
    assert proposal.uuid is not None
    assert is_valid_uuid4(proposal.uuid)

    invoice = Invoice(
        lead_id=lead.id,
        amount_inr=30000.0,
        currency="INR",
        status=InvoiceStatus.ISSUED,
    )
    test_db.add(invoice)
    test_db.commit()
    test_db.refresh(invoice)

    assert invoice.id is not None
    assert invoice.uuid is not None
    assert is_valid_uuid4(invoice.uuid)


def test_pipeline_and_payment_get_by_identifier(test_db: Session):
    pipeline = LeadPipeline(session=test_db)
    lead = pipeline.create_lead(
        business_name="Koramangala Coffee Roasters",
        category="Cafe",
        city="Bengaluru",
        estimated_value_inr=25000.0,
    )
    assert is_valid_uuid4(lead.uuid)

    # Lookup by integer ID
    found_by_int = pipeline.get_lead(lead.id)
    assert found_by_int is not None
    assert found_by_int.id == lead.id
    assert found_by_int.uuid == lead.uuid

    # Lookup by string representation of integer ID
    found_by_str_int = pipeline.get_lead(str(lead.id))
    assert found_by_str_int is not None
    assert found_by_str_int.id == lead.id

    # Lookup by UUID string
    found_by_uuid = pipeline.get_lead(lead.uuid)
    assert found_by_uuid is not None
    assert found_by_uuid.id == lead.id
    assert found_by_uuid.uuid == lead.uuid

    # Lookup non-existent leads
    assert pipeline.get_lead(999999) is None
    assert pipeline.get_lead("999999") is None
    assert pipeline.get_lead(str(uuid.uuid4())) is None
    assert pipeline.get_lead("non-existent-identifier") is None

    # Test PaymentWorkflow.get_invoice
    payments = PaymentWorkflow(session=test_db)
    invoice = payments.create_invoice(lead_id=lead.id, amount_inr=25000.0)
    assert is_valid_uuid4(invoice.uuid)

    # Lookup by integer ID
    inv_by_int = payments.get_invoice(invoice.id)
    assert inv_by_int is not None
    assert inv_by_int.id == invoice.id
    assert inv_by_int.uuid == invoice.uuid

    # Lookup by str int
    inv_by_str_int = payments.get_invoice(str(invoice.id))
    assert inv_by_str_int is not None
    assert inv_by_str_int.id == invoice.id

    # Lookup by UUID string
    inv_by_uuid = payments.get_invoice(invoice.uuid)
    assert inv_by_uuid is not None
    assert inv_by_uuid.id == invoice.id
    assert inv_by_uuid.uuid == invoice.uuid

    # Lookup non-existent invoices
    assert payments.get_invoice(999999) is None
    assert payments.get_invoice("999999") is None
    assert payments.get_invoice(str(uuid.uuid4())) is None
    assert payments.get_invoice("non-existent-identifier") is None


def test_api_lead_uuid_lookup(client: TestClient):
    # Create lead via API
    create_res = client.post(
        "/api/v1/revenue/leads",
        json={
            "business_name": "Whitefield AI Labs",
            "category": "Technology",
            "city": "Bengaluru",
            "estimated_value_inr": 75000.0,
            "contact_person": "Ananya Sharma",
            "contact_channel": "WhatsApp",
            "contact_info": "+919988776655",
        },
    )
    assert create_res.status_code == 200
    lead_data = create_res.json()

    lead_id = lead_data["id"]
    lead_uuid = lead_data["uuid"]

    assert lead_id is not None
    assert is_valid_uuid4(lead_uuid)

    # 1. Retrieve lead by integer ID
    get_by_id_res = client.get(f"/api/v1/revenue/leads/{lead_id}")
    assert get_by_id_res.status_code == 200
    retrieved_by_id = get_by_id_res.json()
    assert retrieved_by_id["id"] == lead_id
    assert retrieved_by_id["uuid"] == lead_uuid
    assert retrieved_by_id["business_name"] == "Whitefield AI Labs"

    # 2. Retrieve lead by string UUID
    get_by_uuid_res = client.get(f"/api/v1/revenue/leads/{lead_uuid}")
    assert get_by_uuid_res.status_code == 200
    retrieved_by_uuid = get_by_uuid_res.json()
    assert retrieved_by_uuid["id"] == lead_id
    assert retrieved_by_uuid["uuid"] == lead_uuid
    assert retrieved_by_uuid["business_name"] == "Whitefield AI Labs"

    # 3. 404 behavior for unknown integer ID
    not_found_int = client.get("/api/v1/revenue/leads/999999")
    assert not_found_int.status_code == 404
    assert not_found_int.json()["detail"] == "Lead not found"

    # 4. 404 behavior for unknown UUID string
    random_uuid = str(uuid.uuid4())
    not_found_uuid = client.get(f"/api/v1/revenue/leads/{random_uuid}")
    assert not_found_uuid.status_code == 404
    assert not_found_uuid.json()["detail"] == "Lead not found"


def test_api_invoice_uuid_lookup(client: TestClient):
    # Create lead first
    lead_res = client.post(
        "/api/v1/revenue/leads",
        json={
            "business_name": "MG Road Retailers",
            "category": "Retail",
            "city": "Bengaluru",
            "estimated_value_inr": 40000.0,
        },
    )
    assert lead_res.status_code == 200
    lead_id = lead_res.json()["id"]

    # Create invoice via API
    inv_res = client.post(
        "/api/v1/revenue/invoices",
        json={
            "lead_id": lead_id,
            "amount_inr": 40000.0,
        },
    )
    assert inv_res.status_code == 200
    invoice_data = inv_res.json()

    invoice_id = invoice_data["id"]
    invoice_uuid = invoice_data["uuid"]

    assert invoice_id is not None
    assert is_valid_uuid4(invoice_uuid)

    # 1. Retrieve invoice by integer ID
    get_by_id_res = client.get(f"/api/v1/revenue/invoices/{invoice_id}")
    assert get_by_id_res.status_code == 200
    retrieved_by_id = get_by_id_res.json()
    assert retrieved_by_id["id"] == invoice_id
    assert retrieved_by_id["uuid"] == invoice_uuid
    assert retrieved_by_id["amount_inr"] == 40000.0

    # 2. Retrieve invoice by string UUID
    get_by_uuid_res = client.get(f"/api/v1/revenue/invoices/{invoice_uuid}")
    assert get_by_uuid_res.status_code == 200
    retrieved_by_uuid = get_by_uuid_res.json()
    assert retrieved_by_uuid["id"] == invoice_id
    assert retrieved_by_uuid["uuid"] == invoice_uuid
    assert retrieved_by_uuid["amount_inr"] == 40000.0

    # 3. 404 behavior for unknown integer ID
    not_found_int = client.get("/api/v1/revenue/invoices/999999")
    assert not_found_int.status_code == 404
    assert not_found_int.json()["detail"] == "Invoice not found"

    # 4. 404 behavior for unknown UUID string
    random_uuid = str(uuid.uuid4())
    not_found_uuid = client.get(f"/api/v1/revenue/invoices/{random_uuid}")
    assert not_found_uuid.status_code == 404
    assert not_found_uuid.json()["detail"] == "Invoice not found"
