# 20. Security Documentation & Air-Gapped Governor
**Project:** PROJECT ONE // Cryptographic Defense Layer  
**Date:** 2026-11-15  

## Security Invariants
- **Air-Gapped Governor:** Financial actions > $10k USD and external outreach emails require manual HMAC-SHA256 founder approval.
- **Guardrail Firewall:** Real-time regex sanitization of credit cards, social security numbers, API tokens, and PII.
- **Zero-Egress Isolation:** Cloudflare VPC and Docker isolation preventing unauthorized third-party telemetry leakage.
