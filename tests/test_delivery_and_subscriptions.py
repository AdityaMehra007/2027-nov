# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Productized Delivery Service & Subscription Ledger (PROJECT ONE Phase 3 & 5)."""

import pytest
from omniverse.modules.opportunities.delivery_service import (
    SubscriptionTier,
    SubscriptionStatus,
    SubscriptionLedgerEngine,
    ProductizedDeliveryEngine,
    ServiceJobType,
    JobStatus,
)


def test_subscription_lifecycle_and_mrr():
    """Verify subscription creation, MRR aggregation, and daily revenue math."""
    ledger = SubscriptionLedgerEngine()

    # Add 3 clients on Starter ($49/mo), 2 on Managed ($99/mo), 1 on Enterprise ($299/mo)
    # Total MRR = (3 * 49) + (2 * 99) + (1 * 299) = 147 + 198 + 299 = $644.00/mo
    # Daily Average = $644.00 / 30 = $21.47/day
    ledger.subscribe_client(client_id="cli_001", client_name="Apex Logistics India", tier=SubscriptionTier.STARTER)
    ledger.subscribe_client(client_id="cli_002", client_name="Cognitive Cloud Systems", tier=SubscriptionTier.STARTER)
    ledger.subscribe_client(client_id="cli_003", client_name="DataFlow SaaS Labs", tier=SubscriptionTier.STARTER)
    ledger.subscribe_client(client_id="cli_004", client_name="FleetPulse NY", tier=SubscriptionTier.MANAGED)
    ledger.subscribe_client(client_id="cli_005", client_name="London Thames Logistics", tier=SubscriptionTier.MANAGED)
    ledger.subscribe_client(client_id="cli_006", client_name="Target India GCC", tier=SubscriptionTier.ENTERPRISE)

    metrics = ledger.get_financial_metrics()
    assert metrics["active_subscribers"] == 6
    assert metrics["mrr_usd"] == 644.0
    assert metrics["daily_avg_revenue_usd"] == pytest.approx(21.47, rel=1e-2)
    
    # Progress towards targets
    # $10/day goal ($300/mo) -> 644 / 300 = 214.7%
    # $100/day goal ($3000/mo) -> 644 / 3000 = 21.5%
    assert metrics["progress_10_usd_day_pct"] > 100.0
    assert metrics["progress_100_usd_day_pct"] > 20.0


def test_job_intake_fulfillment_and_revision():
    """Verify end-to-end service job fulfillment and client revision cycle."""
    engine = ProductizedDeliveryEngine()

    job = engine.submit_job(
        client_id="cli_001",
        job_type=ServiceJobType.WORKFLOW_AUDIT,
        payload={"workflow_name": "Freight Bill Reconciliation", "monthly_volume": 3000},
    )

    assert job.job_id.startswith("job_")
    assert job.status == JobStatus.QUEUED

    # Execute fulfillment
    fulfilled = engine.fulfill_job(job.job_id)
    assert fulfilled.status == JobStatus.COMPLETED
    assert fulfilled.qa_passed is True
    assert len(fulfilled.deliverable_artifact) > 50

    # Submit client revision
    revised = engine.request_revision(
        job_id=job.job_id,
        feedback="Add explicit payback period in days to summary table",
    )
    assert revised.revision_count == 1
    assert "payback" in revised.deliverable_artifact.lower()


def test_sandbox_payment_settlement():
    """Verify sandbox settlement creates verified ledger entries with HMAC receipt."""
    ledger = SubscriptionLedgerEngine()
    
    sub = ledger.subscribe_client(
        client_id="cli_001",
        client_name="Apex Logistics India",
        tier=SubscriptionTier.MANAGED,
    )

    receipt = ledger.process_sandbox_payment(
        subscription_id=sub.subscription_id,
        payment_method="UPI_AUTOPAY",
    )

    assert receipt["status"] == "SETTLED"
    assert receipt["amount_usd"] == 99.0
    assert len(receipt["hmac_receipt"]) == 64  # SHA-256
    assert ledger.get_reconciled_cash_usd() == 99.0
