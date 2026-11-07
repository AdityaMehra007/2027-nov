# PROJECT OMNIA NEXUS: DATA CLASSIFICATION & RETENTION POLICY

> **Governance Directive:** GOV-DATA-002  
> **Status:** Ratified Standard  
> **Compliance Standards:** ISO/IEC 27001, SOC 2 Type II, EU GDPR, India DPDP Act  

---

## 1. Data Classification Tiers

| Tier | Classification | Definition | Encryption Requirements | Retention Period |
|---|---|---|---|---|
| **Tier 1** | **Public** | Publicly accessible docs, benchmarks, press releases | In-transit (TLS 1.3) | Indefinite |
| **Tier 2** | **Internal** | Architecture notes, anonymized research metrics | AES-256 at rest, TLS 1.3 | 3 Years |
| **Tier 3** | **Confidential** | Customer interview notes, user profiles, pipeline data | AES-256 at rest with KMS, TLS 1.3 | 1 Year post-contract |
| **Tier 4** | **Restricted** | Cryptographic private keys, API secrets, unreleased patents | Hardware Security Module (HSM), Zero-Knowledge | Rotated every 90 days |

## 2. Right-to-Erasure & Disposal
* Cryptographic erasure (shredding encryption keys) is enforced upon verified tenant deletion requests.
* Immutable audit logs are pseudomonymized to maintain hash-chain mathematical integrity without retaining PII.
