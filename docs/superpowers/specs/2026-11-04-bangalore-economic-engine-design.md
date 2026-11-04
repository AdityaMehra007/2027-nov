# System Design Spec: Bengaluru Unified Economic, Salary, Money-Flow & Commercial Operating System ("Namma Cashflow Engine")

**Date**: 2026-11-04  
**Status**: DRAFT (Reviewing with User)  
**Author**: Omniverse Architecture Group  
**Target Module**: `src/omniverse/modules/bangalore`

---

## 1. Executive Summary & Vision

Bengaluru is the primary economic and technological capital of India, generating over \$50 Billion in annualized technology value. It is defined by unique economic dynamics:
- High-yield foreign operational inflows from 500+ Global Capability Centers (GCCs) and institutional Venture Capital.
- Multi-tier engineering salary bands with steep compensation bifurcation between IT services, VC unicorns, and global tech GCCs.
- The infamous **5-to-10 month rental deposit lock** that freezes billions of rupees in non-circulating landlord asset sinks.
- Hyper-dense commercial micro-clusters (Koramangala, Indiranagar, HSR Layout, Whitefield, Bellandur, Electronic City, Jayanagar, JP Nagar) with instant UPI commerce velocity.

The objective of this system is to build the comprehensive **Bengaluru Unified Economic, Salary, Money-Flow & Commercial Operating System** inside `src/omniverse/modules/bangalore`, unifying:
1. Deterministic tech salary benchmarking and net take-home calculation under the Indian New Tax Regime (FY 2026-27).
2. Hyperlocal cluster-based Cost-of-Living (CoL), rental deposit lock, and disposable income simulation.
3. Macroeconomic money-flow capital cascade simulation (tracking how ₹100Cr+ moves from corporate inflow through payroll, landlords, taxes, and merchant velocity).
4. Bengaluru engineering project archetypes and architectural directories.
5. Integration with live autonomous commerce (Zero-Brokerage Flat Radar alerts, NammaBiz SMB growth kits, dynamic UPI checkout links, and 24/7 background daemons).
6. Comprehensive CLI tools and REST API endpoints.

---

## 2. Architectural Topology & Components

```
src/omniverse/modules/bangalore/
├── __init__.py                 # Module exports
├── models.py                   # Extended with Salary, Project, MoneyFlow & Cluster models
├── salary_benchmarking.py      # Tier-based tech compensation, tax deductions & RSUs
├── cost_of_living.py           # Cluster rent, 10-mo deposit lock & disposable income
├── money_flow.py               # Macro capital velocity simulation (VC/GCC -> City -> Landlords)
├── projects.py                 # Bengaluru project archetypes, architectures & tech stacks
├── radar.py                    # Zero-brokerage rental alert engine & NLP broker filter
├── smb_engine.py               # NammaBiz growth kit generator & WhatsApp concierge
├── payment_engine.py           # UPI dynamic payment, QR intent & cryptographic receipts
├── daemon.py                   # 24/7 background orchestrator daemon
└── cli_commands.py             # CLI command handlers for salary, CoL, moneyflow & projects
```

---

## 3. Data Models & Schemas (`models.py`)

### 3.1 Company Tiers & Roles
- **`CompanyTier` (Enum)**:
  - `TIER_1_GCC`: Global Capability Centers (Walmart Tech, Goldman Sachs, Google, Uber, Target).
  - `UNICORN_SERIES_B_PLUS`: High-growth venture firms (Swiggy, Razorpay, Zepto, CRED, Meesho).
  - `EARLY_STAGE_VC`: Seed / Series A startups.
  - `IT_SERVICES_ENTERPRISE`: Indian mass tech (Infosys, TCS, Wipro, LTIMindtree).
  - `DEEP_TECH_PUBLIC`: Public sector and defense giants (ISRO, HAL, BEL).

- **`TechRole` (Enum)**:
  - `SDE_1` (Junior Engineer, 0-2 yrs)
  - `SDE_2` (Mid-level Engineer, 2-5 yrs)
  - `SDE_3_SENIOR` (Senior Engineer, 5-8 yrs)
  - `STAFF_PRINCIPAL` (Staff / Principal Architect, 8-12+ yrs)
  - `ENGINEERING_MANAGER` (Engineering Leadership)
  - `PRODUCT_MANAGER` (Product Strategy & Execution)
  - `DATA_AI_SCIENTIST` (Applied AI & ML Engineers)

### 3.2 Salary Benchmark Model (`SalaryBenchmark`)
- `company_tier: CompanyTier`
- `role: TechRole`
- `experience_years: float`
- `base_salary_inr: float`: Fixed annual pay
- `variable_bonus_inr: float`: Performance annual bonus
- `equity_annual_inr: float`: Annualized RSU/ESOP vesting
- `total_ctc_inr: float`: Total Cost to Company (`base + variable + equity`)
- `monthly_gross_inr: float`: (`base + variable`) / 12
- `annual_income_tax_inr: float`: Computed via New Tax Regime slabs + 4% cess
- `monthly_net_in_hand_inr: float`: Real in-hand bank credit on the 1st of every month

### 3.3 Cluster Cost of Living (`ClusterCostOfLiving` & `ClusterLivingAnalysis`)
- `cluster: BangaloreCluster`: Koramangala, Indiranagar, HSR Layout, Whitefield, Bellandur, Electronic City, Jayanagar, JP Nagar.
- `avg_1bhk_rent_inr`, `avg_2bhk_rent_inr`, `avg_3bhk_rent_inr`: Real market rental medians.
- `deposit_lock_months: int`: Standard 6 to 10 months deposit locked with landlord.
- `deposit_lock_amount_inr: float`: Total locked non-productive capital.
- `deposit_annual_opportunity_cost_inr: float`: Lost investment returns @ 7.5% per annum.
- `monthly_utilities_inr: float`: Electricity (BESCOM), water (BWSSB/tankers), high-speed fiber.
- `monthly_commute_inr: float`: Cabs, auto rickshaws, metro pass, petrol (adjusted for ORR/Silk Board congestion).
- `monthly_lifestyle_inr: float`: Weekend dining, microbreweries, third-wave cafes, groceries.
- `total_monthly_expenses_inr: float`: Rent + Utilities + Commute + Lifestyle.
- `monthly_savings_inr: float`: `monthly_net_in_hand_inr - total_monthly_expenses_inr`.
- `savings_ratio: float`: `monthly_savings_inr / monthly_net_in_hand_inr`.

### 3.4 Macro Money Flow Simulation (`MoneyFlowSimulationResult`)
- Inputs:
  - `capital_inflow_inr: float` (e.g. ₹100 Crores)
  - `inflow_source: str` (`GCC_OPEX`, `VC_EQUITY_ROUND`, `IT_EXPORT_BILLING`)
- Allocation & Distribution:
  - `payroll_allocation_inr: float` (~40% - 60% of corporate budget)
  - `cloud_infra_capex_inr: float` (~15% - 25% to AWS/GCP/Azure)
  - `commercial_office_lease_inr: float` (~10% - 15% to Embassy/Prestige tech parks)
- City Circulation Cascades:
  - `income_tax_tds_leakage_inr: float`: Remitted to Union Government
  - `residential_rent_to_landlords_inr: float`: Landlord rental collection
  - `rental_deposits_frozen_inr: float`: Capital frozen in 10-month tenant deposits
  - `local_merchant_spend_inr: float`: F&B, quick-commerce, retail, transport
  - `domestic_remittance_outflow_inr: float`: Sent to dependents outside Bengaluru
  - `capital_market_sip_inr: float`: Equities & mutual funds (Zerodha/Groww)
- Velocity & Economic Indicators:
  - `capital_velocity_ratio: float`: Internal velocity of funds within Bengaluru
  - `local_retainment_percentage: float`: Percentage of capital retained in Karnataka
  - `landlord_absorption_rate: float`: Proportion of net payroll captured by landlords

### 3.5 Bengaluru Project Archetype (`ProjectArchetype`)
- `project_id: str` (e.g. `BLR-PROJ-01`)
- `name: str` (e.g. "Hyperlocal Real-Time Dispatch Engine")
- `primary_sector: str` (e.g. "Quick-Commerce / Logistics")
- `archetype_companies: List[str]` (e.g. ["Zepto", "Swiggy", "Blinkit"])
- `architecture_summary: str`
- `core_tech_stack: List[str]` (e.g. ["Go", "Kafka", "H3 Spatial Index", "Redis Cluster", "PostgreSQL"])
- `scale_metrics: Dict[str, Any]` (e.g. `{"p99_latency_ms": 12, "daily_orders": 750000}`)
- `engineering_challenges: List[str]` (e.g. ["Silk Board route avoidance", "Dark store stock synchronization"])

---

## 4. Business Logic & Calculations

### 4.1 Income Tax Calculation (New Tax Regime FY 2026-27)
- Standard deduction: ₹75,000 for salaried employees.
- Slabs:
  - Up to ₹3,00,000: 0%
  - ₹3,00,001 to ₹7,00,000: 5%
  - ₹7,00,001 to ₹10,00,000: 10%
  - ₹10,00,001 to ₹12,00,000: 15%
  - ₹12,00,001 to ₹15,00,000: 20%
  - Above ₹15,00,000: 30%
- Section 87A rebate: Tax zero if taxable income <= ₹7,00,000.
- Health & Education Cess: 4% surcharge on computed income tax.
- Net Monthly In-Hand: `(Total Gross - Total Tax - PF) / 12`.

### 4.2 Cost-of-Living & 10-Month Deposit Lock Multiplier
- HSR Layout & Koramangala: 10 months deposit standard.
- Indiranagar: 10 months deposit standard.
- Whitefield & Bellandur: 6 to 8 months deposit standard.
- Electronic City: 5 to 6 months deposit standard.
- Opportunity cost: `deposit_amount * 0.075` (7.5% risk-free fixed income return lost).

---

## 5. CLI & API Interfaces

### 5.1 CLI Commands (`omniverse bangalore`)
- `python -m omniverse.cli bangalore salary --tier TIER_1_GCC --role SDE_2`: Displays detailed base, bonus, equity, CTC, and monthly take-home.
- `python -m omniverse.cli bangalore col-sim --cluster "HSR Layout" --bhk 2 --salary 3500000`: Computes living costs, deposit lock, and net savings.
- `python -m omniverse.cli bangalore moneyflow-sim --amount 100000000 --source GCC_OPEX`: Simulates ₹10Cr capital cascade.
- `python -m omniverse.cli bangalore projects`: Lists Bengaluru engineering project architectures.
- `python -m omniverse.cli bangalore overview`: Macro economic summary card of Bengaluru tech ecosystem.

### 5.2 REST API Endpoints (`/api/v1/bangalore/`)
- `GET /api/v1/bangalore/salary-benchmarks`: Query salary matrices by tier and role.
- `POST /api/v1/bangalore/col-simulate`: Calculate living expenses and deposit lock.
- `POST /api/v1/bangalore/moneyflow-simulate`: Run macro capital cascade simulation.
- `GET /api/v1/bangalore/projects`: Retrieve real-world project architectures.
- `GET /api/v1/bangalore/overview`: Ecosystem macro statistics.

---

## 6. Testing & Quality Strategy

1. **Unit Tests (`tests/test_bangalore_economic_engine.py`)**:
   - Validation of salary calculations across all 5 company tiers and 7 roles.
   - Verification of New Tax Regime tax slabs, 87A rebate, and cess calculations.
   - Cluster cost-of-living and deposit opportunity cost formula tests.
   - Money flow simulation conservation tests (sum of allocations == total inflow).
   - Project registry completeness tests.
   - FastAPI client tests for all newly registered `/api/v1/bangalore/economy/*` endpoints.
   - CLI invocation tests for `omniverse bangalore` subcommands.
2. **Backwards Compatibility**:
   - Zero regressions on existing 205+ unit tests, including existing `test_bangalore_cashflow.py`.
