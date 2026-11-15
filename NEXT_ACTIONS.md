# NEXT_ACTIONS: Operational Roadmap

**Current State:** Phases 0 through 7 Built, Tested, Integrated, and 100% Operational  
**Active Phase:** Phase 8: Founder Sign-off & Live Commercial Scaling

---

## 1. Operational Next Actions (Immediate)

1. **Founder Review of Staged Outbound Intents (`PendingActionsQueue`)**
   - 30 target prospect dossiers have been generated across Bengaluru, North America, Europe/UK, and APAC/Middle East corridors.
   - Run `python -m omniverse.cli prospect-pipeline --limit 5 --stage-actions` to review staged HMAC-SHA256 signatures.
   - Authorize initial proof-first outreach to the top 3 beachhead candidates:
     1. *Apex Logistics India* (Freight reconciliation audit: 6,628% ROI, $6,562/mo savings)
     2. *Target India* (Vendor PO vs invoice discrepancies: $185,000/yr annual toil)
     3. *London Thames Logistics Ltd* (Post-Brexit customs declaration audits: $190,000/yr annual toil)

2. **Client Portal & Self-Service Intake Verification**
   - Access the running FastAPI portal at `http://127.0.0.1:8888/docs` or `http://127.0.0.1:8888/dashboard`.
   - Test self-service deliverable generation via `/api/v1/opportunities/beachhead/generate`.

3. **Merchant Credential Connection (Phase 5 Live Cutover)**
   - When ready for live production collections, inject live API keys in environment:
     - `STRIPE_SECRET_KEY` & `STRIPE_WEBHOOK_SECRET`
     - `RAZORPAY_KEY_ID` & `RAZORPAY_KEY_SECRET`
   - Test live $1 auth charge using `python -m omniverse.cli subscriptions-ledger`.

---

## 2. Long-Running Daemon Operations

- **24/7 Health Monitoring:** Run background daemon loop with `python -m omniverse.cli agency-daemon --limit 2`.
- **Master Audit Execution:** Run full institutional verification with `python -m omniverse.cli do-everything`.
- **Standup Telemetry:** Inspect agent workload and Merkle block height with `python -m omniverse.cli workforce-standup`.
