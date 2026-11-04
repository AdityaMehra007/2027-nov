---
name: omniverse-agency
description: Revenue generation, micro-agency operations, client growth kits, CRM prospecting, and payment reconciliation for CASHFLOW INFINITY.
---

# CASHFLOW INFINITY: Micro-Agency & Revenue Engine

Use this skill to identify customer problems, generate high-converting Local Business Growth Kits, maintain the prospective client CRM, and track collected revenue.

## When to Use
- User asks to "generate growth kit", "find clients", "create pitch", "manage leads", or "record payment".
- Target markets: Local cafes, restaurants, salons, gyms, retail, clinics, and professional services.

## Operational Workflows

### 1. Generate Local Business Growth Kit
To generate a 10-caption, 5-hook, WhatsApp catalog package for an SMB:
```powershell
python -m omniverse.cli generate-kit --business "Business Name" --niche "Category" --city "Bengaluru"
```

### 2. View Active Lead Pipeline
```powershell
python -m omniverse.cli leads
```

### 3. Pipeline Stages
1. `NEW`: Discovered prospect.
2. `QUALIFIED`: Verified contact person and willingness to evaluate.
3. `CONTACTED`: Sample demo / Growth Kit shared.
4. `PROPOSAL_SENT`: Commercial contract and pricing offered.
5. `WON`: Agreement reached and invoice issued.
6. `LOST`: Disqualified or declined.

### 4. Revenue Reconciliation Doctrine
Only funds confirmed received in bank/escrow count as `Collected Revenue`. Unsigned contracts remain categorized strictly as `Pipeline Value`.
