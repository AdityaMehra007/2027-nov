# PORTFOLIO GOVERNANCE: ANNUAL REVIEW & STAGE-GATE PIVOT FRAMEWORK
**Governance Standard:** OMNIA-GOV-008 | **Backlog Tasks:** OMNIA-038, OMNIA-045 | **Authority:** Investment Committee & Foundry Directorate

---

## 1. Annual Portfolio Review Charter
The OMNIA Foundry conducts a formal, audited annual portfolio review across all 24 Venture Studios to ensure rigorous capital discipline, rapid resource reallocation, and elimination of sunk cost fallacies.

### Evaluation Dimensions
Each studio programme is scored across four weighted pillars (Total Score: 0 - 100):
1. **Empirical Customer Signal (30%)**:
   - Number of active commercial/pilot agreements signed.
   - User retention and repeat usage rate ($\ge 65\%$ target).
   - Verifiable net cost savings or performance gains measured by customer.
2. **Technical Feasibility & Scientific Validation (30%)**:
   - Stage-gate evidence audit pass rate.
   - Independent scientific replication / benchmark verification.
   - Defensible IP and open-source compliance audit.
3. **Unit Economics & Capital Efficiency (25%)**:
   - Actual burn rate vs milestone delivery.
   - Gross margin trajectory ($\ge 75\%$ target for software/compute, $\ge 40\%$ for hardware/hybrid).
   - Clear capital requirements for subsequent phases (Class A through D).
4. **Safety, Governance & Compliance (15%)**:
   - Zero unresolved critical vulnerabilities in code/infrastructure.
   - Formal safety case approved for deployment.
   - Complete SHA-256 cryptographic audit chain without gaps or forks.

---

## 2. 90-Day Continue / Narrow / Pivot / Kill Framework (OMNIA-045)
At the conclusion of each 90-day execution sprint, the Studio Lead and Investment Committee convene for a binding stage review.

```
                    [ 90-Day Sprint Review ]
                               |
       +-----------------------+-----------------------+
       |                       |                       |
[ Score >= 80 ]        [ 60 <= Score < 80 ]      [ Score < 60 ]
       |                       |                       |
       v                       v                       v
 [ CONTINUE ]          [ NARROW / PIVOT ]           [ KILL ]
Advance to next       Contract scope to highest-   Immediate teardown,
stage & disburse      traction workflow; 45-day    preserve code/IP,
capital tranche       re-evaluation                reallocate talent
```

### Action Criteria
- **CONTINUE**: Meets all primary customer, technical, and capital milestones. Full next-phase budget unlocked.
- **NARROW**: Broad horizontal thesis failed; narrow focus to single high-demand vertical or job-to-be-done.
- **PIVOT**: Core technical capability validated, but commercial positioning or target customer flawed. Formulate new thesis within 14 business days.
- **KILL**: Failed feasibility, lack of customer urgency, or irreconcilable safety/regulatory barrier. Programme formally archived into Foundry Vault with lessons learned published.

---

## 3. Committee Composition & Voting Quorum
- **Voting Members**: Managing Director, Head of Research, Principal Architect, Head of Safety & Governance.
- **Quorum**: 100% attendance required; decisions recorded immutably in `omnia_foundry.db` with signed decision receipts.
