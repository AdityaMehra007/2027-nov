import pytest
import time
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from omniverse.modules.bangalore.models import (
    BangaloreCluster,
    SMBTier,
    RadarSubscriptionTier,
    SMBGrowthClient,
    RentalListing,
    FlatRadarSubscriber,
    BangaloreCashTransaction,
    BangaloreCashflowSummary,
)
from omniverse.modules.bangalore.radar import BangaloreFlatRadar
from omniverse.modules.bangalore.smb_engine import NammaBizEngine
from omniverse.modules.bangalore.payment_engine import BangaloreUPIEngine
from omniverse.modules.bangalore.daemon import Bangalore247CashDaemon
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine
from omniverse.core.telemetry import global_event_bus

@pytest.fixture
def mem_session(tmp_path):
    db_file = tmp_path / "mem_session.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def test_client(tmp_path):
    db_file = tmp_path / "bangalore_api.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    with TestClient(app) as client:
        yield client

def test_bangalore_models_and_enums():
    assert BangaloreCluster.KORAMANGALA == "Koramangala"
    assert BangaloreCluster.HSR_LAYOUT == "HSR Layout"
    assert BangaloreCluster.INDIRANAGAR == "Indiranagar"
    assert BangaloreCluster.WHITEFIELD == "Whitefield"
    assert RadarSubscriptionTier.PRO_RELOCATOR == "PRO_RELOCATOR"
    assert SMBTier.STARTER == "STARTER"

def test_flat_radar_broker_detection(mem_session):
    radar = BangaloreFlatRadar(mem_session)

    # 1. Obvious Broker Post
    broker_text = "3BHK available in Koramangala 4th block. 1 month rent brokerage applicable. Contact fast."
    is_zero, conf = radar.evaluate_listing_content(broker_text)
    assert is_zero is False
    assert conf >= 0.60

    # 2. Genuine Direct Owner Post
    owner_text = "Hi all, moving out of Bengaluru! 2BHK in HSR Sector 2. Direct from owner, zero brokerage. Deposit negotiable."
    is_zero_owner, conf_owner = radar.evaluate_listing_content(owner_text)
    assert is_zero_owner is True
    assert conf_owner <= 0.35

    # 3. Flatmate replacement
    flatmate_text = "Looking for a flatmate in Bellandur near EcoSpace. No broker involved, shared cook."
    is_zero_fm, conf_fm = radar.evaluate_listing_content(flatmate_text)
    assert is_zero_fm is True

def test_flat_radar_subscriber_matching(mem_session):
    radar = BangaloreFlatRadar(mem_session)
    upi_engine = BangaloreUPIEngine(mem_session)

    # Subscribe a user for HSR Layout
    txn, sub = upi_engine.settle_radar_payment(
        transaction_id="TXN-TEST-001",
        name="Vikram Singh",
        phone_whatsapp="+91-9880099887",
        tier=RadarSubscriptionTier.PRO_RELOCATOR,
        amount_inr=499.0,
        target_clusters="HSR Layout,Koramangala",
        preferred_bhk=2,
        max_budget_inr=35000.0
    )
    assert sub.is_active is True
    assert sub.vip_access_key.startswith("VIP-")

    # Ingest a matching zero-brokerage 2BHK in HSR
    listing = radar.ingest_and_evaluate(
        title="Spacious 2BHK in HSR Sector 1",
        cluster=BangaloreCluster.HSR_LAYOUT,
        locality="27th Main",
        bhk=2,
        rent_inr=32000.0,
        deposit_inr=100000.0,
        raw_content="Direct from owner, zero brokerage. 2BHK in HSR Sector 1.",
        contact_phone="+91-9845012345"
    )
    assert listing.is_zero_brokerage is True

    alerts = radar.match_subscribers(listing)
    assert len(alerts) >= 1
    matched = alerts[0]
    assert matched["subscriber_name"] == "Vikram Singh"
    assert "HSR Layout" in matched["alert_payload"]
    assert "Zero-Brokerage Match" in matched["alert_payload"]

def test_namma_biz_smb_engine(mem_session):
    smb_engine = NammaBizEngine(mem_session)
    clients = smb_engine.scan_and_seed_cluster(BangaloreCluster.INDIRANAGAR)
    assert len(clients) >= 3

    client = clients[0]
    kit = smb_engine.generate_growth_kit(client)
    assert kit["business_name"] == client.business_name
    assert kit["cluster"] == "Indiranagar"
    assert len(kit["social_hooks"]) == 10
    assert "Silk Board" in kit["social_hooks"][0] or "Indiranagar" in kit["social_hooks"][0]
    assert "wa.me" in kit["direct_pitch_url"]
    assert "NAMMA 24/7 AI SALES CONCIERGE" in kit["whatsapp_ai_script"]

def test_upi_engine_checkout_and_settlement(mem_session):
    upi_engine = BangaloreUPIEngine(mem_session)

    checkout = upi_engine.checkout_radar_subscription(
        name="Sneha Rao",
        phone_whatsapp="+91-9876543210",
        tier=RadarSubscriptionTier.SPRINT_HUNTER
    )
    assert checkout["amount_inr"] == 199.0
    assert "upi://pay?" in checkout["upi_intent_uri"]
    assert "pa=cashflow.bangalore%40icici" in checkout["upi_intent_uri"]

    txn, sub = upi_engine.settle_radar_payment(
        transaction_id=checkout["transaction_id"],
        name=checkout["subscriber_name"],
        phone_whatsapp=checkout["phone_whatsapp"],
        tier=RadarSubscriptionTier.SPRINT_HUNTER,
        amount_inr=checkout["amount_inr"]
    )
    assert txn.status == "SETTLED"
    assert sub.is_active is True
    assert sub.total_paid_inr == 199.0

    receipt = upi_engine.generate_cryptographic_receipt(txn)
    assert isinstance(receipt, str)
    assert len(receipt) == 64

def test_smb_retainer_settlement(mem_session):
    smb_engine = NammaBizEngine(mem_session)
    upi_engine = BangaloreUPIEngine(mem_session)

    clients = smb_engine.scan_and_seed_cluster(BangaloreCluster.WHITEFIELD)
    client = clients[0]
    assert client.status == "PROSPECT"

    txn, updated_client = upi_engine.settle_smb_retainer(
        client_id=client.id,
        amount_inr=7999.0
    )
    assert txn.amount_inr == 7999.0
    assert updated_client.status == "ACTIVE_RETAINER"
    assert updated_client.is_active is True

def test_bangalore_daemon_cycle(mem_session):
    daemon = Bangalore247CashDaemon(mem_session)
    res = daemon.run_cycle(cluster=BangaloreCluster.KORAMANGALA, simulate_listings=True)

    assert res["cycle_number"] == 1
    assert res["cluster"] == "Koramangala"
    assert res["smb_prospects_found"] >= 3
    assert res["listings_processed"] == 5

    summary = daemon.get_summary()
    assert summary.city == "Bengaluru"
    assert summary.status == "RUNNING_24_7"
    assert "Koramangala" in summary.cluster_hotspots

def test_bangalore_api_endpoints(test_client):
    # 1. Status
    res_status = test_client.get("/api/v1/bangalore/status")
    assert res_status.status_code == 200
    data = res_status.json()
    assert data["city"] == "Bengaluru"
    assert data["status"] == "RUNNING_24_7"

    # 2. Evaluate Listing
    res_eval = test_client.post("/api/v1/bangalore/flat-radar/evaluate", json={
        "raw_text": "Direct owner here! 1BHK in Indiranagar near metro. Zero brokerage."
    })
    assert res_eval.status_code == 200
    assert res_eval.json()["is_zero_brokerage"] is True

    # 3. Scan Cluster
    res_scan = test_client.post("/api/v1/bangalore/prospects/scan", json={
        "cluster": "HSR Layout"
    })
    assert res_scan.status_code == 200
    assert res_scan.json()["count"] >= 3

    # 4. Checkout Radar
    res_co = test_client.post("/api/v1/bangalore/checkout/radar", json={
        "name": "Nikhil Kamath",
        "phone_whatsapp": "+91-9988776655",
        "tier": "PRO_RELOCATOR"
    })
    assert res_co.status_code == 200
    assert "upi://pay?" in res_co.json()["upi_intent_uri"]

    # 5. Settle Radar
    txn_id = res_co.json()["transaction_id"]
    res_settle = test_client.post("/api/v1/bangalore/settle/radar", json={
        "transaction_id": txn_id,
        "name": "Nikhil Kamath",
        "phone_whatsapp": "+91-9988776655",
        "tier": "PRO_RELOCATOR",
        "amount_inr": 499.0
    })
    assert res_settle.status_code == 200
    assert res_settle.json()["status"] == "SETTLED"
    assert "vip_access_key" in res_settle.json()
