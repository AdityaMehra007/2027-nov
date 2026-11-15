# NEXT_ACTIONS: Implementation Roadmap

**Active Phase:** Phase 1 (Research Intelligence & Opportunity Scoring) COMPLETE → Phase 2 (Commercial Validation & Prospect Dossier Staging) ACTIVE

---

## Completed Milestones (Phase 1)
- [x] **Customer Taxonomy & Revenue Catalogue** (`src/omniverse/modules/opportunities/taxonomy.py`): 60+ customer categories & 50+ monetization models verified.
- [x] **Canonical Opportunity Scoring Formula** (`src/omniverse/modules/opportunities/scoring.py`): Relative ratio and 100-point rubric with SQLite persistence.
- [x] **Company Intelligence Store & Deduplication** (`src/omniverse/modules/opportunities/company_intelligence.py`): Multi-source registry with confidence scoring.
- [x] **Beachhead Deliverable Generator** (`src/omniverse/modules/opportunities/beachhead.py`): Automated audit reports with quantified COI, projected monthly savings, and tiered pricing ($49/$99/$499).
- [x] **100% Verification Coverage**: Verified via `tests/test_global_opportunity_mvp.py` and `tests/test_opportunity_scoring_engine.py`.

---

## Active Next Steps (Phase 2)

1. **Prospect Dossier Extraction & Staging (30–50 Companies)**
   - Extract candidate organizations from permitted public directories, GitHub, and local business indices.
   - Stage personalized outreach drafts into the `PendingActionsQueue` for human review (respecting the non-negotiable rule: no unsolicited outbound communication without founder sign-off).

2. **Self-Service Beachhead Web Intake Form**
   - Connect web intake form to local server (`http://127.0.0.1:8888`) or dashboard (`dist/dashboard/index.html`).
   - Allow prospective clients to upload workflow descriptions or sample invoices to receive an instant audit preview.

---

## Phase 3–5 Upcoming Milestones

3. **Productized Customer Portal & Delivery Status UI**
   - Interactive job status tracker with client-facing deliverables download.

4. **Sandbox Payment Flow Verification**
   - End-to-end checkout with mock UPI QR and Stripe test cards in `tests/test_agency_payment_gateways.py`.
   - Prepare webhook listener configuration for live deployment once production merchant credentials are provided.

5. **24/7 Daemon Health Verification**
   - Keep background health monitors and worker daemons active with rolling anomaly checks via `PyControlPlane`.
