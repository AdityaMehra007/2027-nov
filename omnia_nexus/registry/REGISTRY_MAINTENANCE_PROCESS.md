# OPERATIONAL STANDARD: QUARTERLY ECOSYSTEM REGISTRY REFRESH
**Operating Standard:** OMNIA-SOP-005 | **Backlog Task:** OMNIA-050 | **Responsible Role:** Intelligence Lead

---

## 1. Registry Maintenance Purpose
The OMNIA Living Ecosystem Registry (`ECOSYSTEM_REGISTRY.csv`, `ACADEMIC_LABS_REGISTRY.csv`, `TARGET_PARTNERS.csv`) tracks 120+ frontier organizations across 15 technical domains. To prevent entity rot, obsolescence, or stale contact data, this SOP establishes an automated and human-in-the-loop quarterly audit protocol.

---

## 2. Quarterly Refresh Cadence & Timeline
| Week of Quarter | Operational Focus | Output Deliverable |
| :--- | :--- | :--- |
| **Week 10** | Automated Web & API Scraping Sweep | Drift detection report identifying defunct URLs, acquired entities, and leadership changes |
| **Week 11** | Human Validation & Analyst Enrichment | Ground-truth verification of contact points, research priorities, and funding tranches |
| **Week 12** | Database Sync & Hash Chain Notarization | Updated CSV artifacts committed; `verify_ecosystem.py` executed; SHA-256 audit log generated |
| **Week 13** | Executive Briefing & Distribution | Portfolio leads notified of new partnership candidates and competitive shifts |

---

## 3. Automation Scripts & Quality Gates
- **Automated Checker**: `omnia_nexus/src/omnia_foundry/verify_ecosystem.py` validates entity schema, required fields, and category completeness.
- **Verification Rule**: Zero entries older than 180 days permitted without active re-validation timestamp.
- **Tamper Evidence**: Every registry mutation emits an audit event (`REGISTRY_MUTATION`) to `omnia_foundry.db`.
