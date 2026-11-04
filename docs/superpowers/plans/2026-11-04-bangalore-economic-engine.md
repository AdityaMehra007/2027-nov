# Bengaluru Unified Economic & Cashflow Intelligence Operating System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify the complete Bengaluru Economic, Tech Salary, Money-Flow Capital Simulator, Project Archetypes Registry, and Unified CLI/API interfaces inside `src/omniverse/modules/bangalore`.

**Architecture:** A modular Python engine adhering to SQLModel and Pydantic schemas, integrating:
1. `salary_benchmarking.py`: 5 company tiers, 7 engineering roles, and Indian New Tax Regime calculations.
2. `cost_of_living.py`: 8 Bengaluru tech clusters, 10-month rental deposit locks, and net savings ratios.
3. `money_flow.py`: Macro capital cascade simulations (corporate OpEx/VC -> payroll -> tax/landlord sinks -> local merchant velocity).
4. `projects.py`: Real-world Bengaluru engineering system architectures.
5. Unified REST API endpoints and CLI commands.

**Tech Stack:** Python 3.11+, Pydantic v2, SQLModel, FastAPI, Click/Rich, Pytest.

**Spec:** `docs/superpowers/specs/2026-11-04-bangalore-economic-engine-design.md`

## Global Constraints

- Absolute evidence over assertions: 100% green pytest verification before claiming task completion.
- Mathematical precision: Income tax calculations must conform to Indian New Tax Regime (FY 2026-27 slabs, standard deduction ₹75,000, 4% health & education cess).
- Strict conservation of capital in `money_flow.py`: Sum of allocations must exactly equal total gross inflow.
- Zero breaking changes to existing `test_bangalore_cashflow.py` and existing 205 unit tests.

---

### Task 1: Domain Models & Schemas

**Files:**
- Modify: `src/omniverse/modules/bangalore/models.py`
- Create: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Produces:
  - `CompanyTier` (Enum: `TIER_1_GCC`, `UNICORN_SERIES_B_PLUS`, `EARLY_STAGE_VC`, `IT_SERVICES_ENTERPRISE`, `DEEP_TECH_PUBLIC`)
  - `TechRole` (Enum: `SDE_1`, `SDE_2`, `SDE_3_SENIOR`, `STAFF_PRINCIPAL`, `ENGINEERING_MANAGER`, `PRODUCT_MANAGER`, `DATA_AI_SCIENTIST`)
  - `ExperienceLevel` (Enum: `JUNIOR`, `MID`, `SENIOR`, `STAFF_LEAD`, `PRINCIPAL_EXEC`)
  - `SalaryBenchmark` (Pydantic model)
  - `ClusterCostOfLiving` (Pydantic model)
  - `ClusterLivingAnalysis` (Pydantic model)
  - `MoneyFlowSimulationResult` (Pydantic model)
  - `ProjectArchetype` (Pydantic model)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bangalore_economic_engine.py
import pytest
from omniverse.modules.bangalore.models import (
    CompanyTier,
    TechRole,
    ExperienceLevel,
    SalaryBenchmark,
    ClusterCostOfLiving,
    ClusterLivingAnalysis,
    MoneyFlowSimulationResult,
    ProjectArchetype,
    BangaloreCluster,
)

def test_bangalore_economic_models_instantiation():
    assert CompanyTier.TIER_1_GCC == "TIER_1_GCC"
    assert TechRole.SDE_2 == "SDE_2"
    assert ExperienceLevel.SENIOR == "SENIOR"

    salary = SalaryBenchmark(
        company_tier=CompanyTier.TIER_1_GCC,
        role=TechRole.SDE_2,
        experience_years=3.5,
        base_salary_inr=4200000.0,
        variable_bonus_inr=600000.0,
        equity_annual_inr=2200000.0,
        total_ctc_inr=7000000.0,
        monthly_gross_inr=400000.0,
        annual_income_tax_inr=1115400.0,
        monthly_net_in_hand_inr=290000.0,
    )
    assert salary.total_ctc_inr == 7000000.0
    assert salary.monthly_net_in_hand_inr == 290000.0

    col = ClusterCostOfLiving(
        cluster=BangaloreCluster.HSR_LAYOUT,
        avg_1bhk_rent_inr=22000.0,
        avg_2bhk_rent_inr=38000.0,
        avg_3bhk_rent_inr=55000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=6500.0,
        lifestyle_monthly_inr=15000.0,
        utilities_monthly_inr=4500.0,
    )
    assert col.deposit_lock_months == 10
    assert col.avg_2bhk_rent_inr == 38000.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py -v`  
Expected: FAIL with `ImportError: cannot import name 'CompanyTier' from 'omniverse.modules.bangalore.models'`

- [ ] **Step 3: Implement models in `src/omniverse/modules/bangalore/models.py`**

Add the enums and Pydantic models to `src/omniverse/modules/bangalore/models.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/models.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add economic, salary, CoL, and moneyflow models"
```

---

### Task 2: Salary Benchmarking & Indian New Tax Regime Calculator

**Files:**
- Create: `src/omniverse/modules/bangalore/salary_benchmarking.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Consumes: `CompanyTier`, `TechRole`, `SalaryBenchmark` from `models.py`
- Produces:
  - `compute_new_regime_tax(annual_taxable_inr: float) -> float`
  - `get_salary_benchmark(tier: CompanyTier, role: TechRole, experience_years: float = 3.0) -> SalaryBenchmark`
  - `compare_tiers(role: TechRole, experience_years: float = 3.0) -> list[SalaryBenchmark]`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from omniverse.modules.bangalore.salary_benchmarking import (
    compute_new_regime_tax,
    get_salary_benchmark,
    compare_tiers,
)

def test_compute_new_regime_tax():
    # Below rebate threshold (<= 7L) should have 0 tax
    assert compute_new_regime_tax(650000.0) == 0.0

    # 15L income: standard deduction 75k => 14.25L taxable
    tax_15l = compute_new_regime_tax(1500000.0)
    assert tax_15l > 100000.0

    # Surcharge/Cess: tax includes 4% Health & Education Cess
    assert tax_15l == pytest.approx(135200.0, rel=1e-2)

def test_get_salary_benchmark():
    gcc_sde2 = get_salary_benchmark(CompanyTier.TIER_1_GCC, TechRole.SDE_2)
    assert gcc_sde2.base_salary_inr >= 3500000.0
    assert gcc_sde2.total_ctc_inr > gcc_sde2.base_salary_inr
    assert gcc_sde2.monthly_net_in_hand_inr > 0.0

    it_sde2 = get_salary_benchmark(CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.SDE_2)
    assert it_sde2.total_ctc_inr < gcc_sde2.total_ctc_inr

    tiers = compare_tiers(TechRole.SDE_2)
    assert len(tiers) == 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_compute_new_regime_tax -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'omniverse.modules.bangalore.salary_benchmarking'`

- [ ] **Step 3: Implement `src/omniverse/modules/bangalore/salary_benchmarking.py`**

Implement deterministic calculations for New Tax Regime slabs, role compensations, and tier comparisons.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py -k "test_compute_new_regime_tax or test_get_salary_benchmark" -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/salary_benchmarking.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add salary benchmarking and new tax regime calculator"
```

---

### Task 3: Cluster Cost of Living & 10-Month Deposit Lock Simulator

**Files:**
- Create: `src/omniverse/modules/bangalore/cost_of_living.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Consumes: `BangaloreCluster`, `SalaryBenchmark`, `ClusterLivingAnalysis`
- Produces:
  - `CLUSTER_COL_DATA: dict[BangaloreCluster, ClusterCostOfLiving]`
  - `get_cluster_col(cluster: BangaloreCluster) -> ClusterCostOfLiving`
  - `analyze_cluster_living(cluster: BangaloreCluster, bhk: int, salary: SalaryBenchmark) -> ClusterLivingAnalysis`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from omniverse.modules.bangalore.cost_of_living import (
    get_cluster_col,
    analyze_cluster_living,
)

def test_cost_of_living_hsr_layout():
    col = get_cluster_col(BangaloreCluster.HSR_LAYOUT)
    assert col.deposit_lock_months == 10
    assert col.avg_2bhk_rent_inr == 38000.0

    salary = get_salary_benchmark(CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.SDE_2)
    analysis = analyze_cluster_living(BangaloreCluster.HSR_LAYOUT, bhk=2, salary=salary)

    assert analysis.rent_inr == 38000.0
    assert analysis.deposit_lock_amount_inr == 380000.0  # 10 months rent
    assert analysis.deposit_annual_opportunity_cost_inr == 380000.0 * 0.075
    assert analysis.monthly_savings_inr > 0.0
    assert analysis.savings_ratio > 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_cost_of_living_hsr_layout -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'omniverse.modules.bangalore.cost_of_living'`

- [ ] **Step 3: Implement `src/omniverse/modules/bangalore/cost_of_living.py`**

Define cluster benchmarks for all 8 tech clusters and calculate deposit lock drag, opportunity costs, and net savings ratios.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py::test_cost_of_living_hsr_layout -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/cost_of_living.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add cluster cost-of-living and deposit lock simulator"
```

---

### Task 4: Macro Capital Flywheel & Money Flow Simulator

**Files:**
- Create: `src/omniverse/modules/bangalore/money_flow.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Consumes: `MoneyFlowSimulationResult`
- Produces:
  - `simulate_capital_flow(inflow_amount_inr: float, source: str = "GCC_OPEX") -> MoneyFlowSimulationResult`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from omniverse.modules.bangalore.money_flow import simulate_capital_flow

def test_money_flow_simulation_conservation():
    inflow = 100000000.0  # ₹10 Crores
    res = simulate_capital_flow(inflow_amount_inr=inflow, source="GCC_OPEX")

    assert res.capital_inflow_inr == inflow
    assert res.payroll_allocation_inr > 0.0
    assert res.residential_rent_to_landlords_inr > 0.0
    assert res.rental_deposits_frozen_inr > 0.0
    assert res.local_merchant_spend_inr > 0.0
    assert res.capital_velocity_ratio > 1.0
    assert 0.0 <= res.landlord_absorption_rate <= 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_money_flow_simulation_conservation -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'omniverse.modules.bangalore.money_flow'`

- [ ] **Step 3: Implement `src/omniverse/modules/bangalore/money_flow.py`**

Simulate the cascading flow of corporate capital through payroll, landlords, merchant commerce, taxes, and investments.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py::test_money_flow_simulation_conservation -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/money_flow.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add macroeconomic money-flow capital simulator"
```

---

### Task 5: Bengaluru Project Archetypes Registry

**Files:**
- Create: `src/omniverse/modules/bangalore/projects.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Consumes: `ProjectArchetype`
- Produces:
  - `get_project_archetypes() -> list[ProjectArchetype]`
  - `get_project_by_id(project_id: str) -> ProjectArchetype | None`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from omniverse.modules.bangalore.projects import get_project_archetypes, get_project_by_id

def test_project_archetypes_catalog():
    projects = get_project_archetypes()
    assert len(projects) >= 5

    proj_ids = [p.project_id for p in projects]
    assert "BLR-PROJ-01" in proj_ids  # Quick-commerce
    assert "BLR-PROJ-02" in proj_ids  # FinTech UPI switch

    p1 = get_project_by_id("BLR-PROJ-01")
    assert p1 is not None
    assert "Zepto" in p1.archetype_companies or "Swiggy" in p1.archetype_companies
    assert len(p1.core_tech_stack) >= 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_project_archetypes_catalog -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'omniverse.modules.bangalore.projects'`

- [ ] **Step 3: Implement `src/omniverse/modules/bangalore/projects.py`**

Define the 5 Bengaluru project archetypes with architectural diagrams, tech stacks, scale metrics, and engineering challenges.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py::test_project_archetypes_catalog -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/projects.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add bengaluru tech project archetypes registry"
```

---

### Task 6: REST API Endpoints & Module Exports

**Files:**
- Modify: `src/omniverse/modules/bangalore/__init__.py`
- Modify: `src/omniverse/api/routes/bangalore.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Produces REST endpoints:
  - `GET /api/v1/bangalore/salary-benchmarks`
  - `POST /api/v1/bangalore/col-simulate`
  - `POST /api/v1/bangalore/moneyflow-simulate`
  - `GET /api/v1/bangalore/projects`
  - `GET /api/v1/bangalore/overview`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from fastapi.testclient import TestClient
from omniverse.api.app import create_app
from omniverse.core.database import DatabaseEngine

@pytest.fixture
def api_client(tmp_path):
    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    with TestClient(app) as client:
        yield client

def test_api_salary_benchmarks(api_client):
    res = api_client.get("/api/v1/bangalore/salary-benchmarks?tier=TIER_1_GCC&role=SDE_2")
    assert res.status_code == 200
    data = res.json()
    assert data["company_tier"] == "TIER_1_GCC"
    assert data["total_ctc_inr"] > 0

def test_api_col_simulate(api_client):
    res = api_client.post("/api/v1/bangalore/col-simulate", json={
        "cluster": "HSR Layout",
        "bhk": 2,
        "company_tier": "TIER_1_GCC",
        "role": "SDE_2"
    })
    assert res.status_code == 200
    assert res.json()["deposit_lock_amount_inr"] > 0

def test_api_moneyflow_simulate(api_client):
    res = api_client.post("/api/v1/bangalore/moneyflow-simulate", json={
        "inflow_amount_inr": 100000000.0,
        "source": "GCC_OPEX"
    })
    assert res.status_code == 200
    assert res.json()["capital_velocity_ratio"] > 1.0

def test_api_projects(api_client):
    res = api_client.get("/api/v1/bangalore/projects")
    assert res.status_code == 200
    assert len(res.json()) >= 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_api_salary_benchmarks -v`  
Expected: FAIL with `404 Not Found`

- [ ] **Step 3: Update `src/omniverse/modules/bangalore/__init__.py` & `src/omniverse/api/routes/bangalore.py`**

Register the new endpoints on the FastAPI router with request/response serialization.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bangalore_economic_engine.py -k "test_api" -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/__init__.py src/omniverse/api/routes/bangalore.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add REST API routes for economic, salary, and money flow engines"
```

---

### Task 7: CLI Commands & Full Ecosystem Verification

**Files:**
- Create: `src/omniverse/modules/bangalore/cli_commands.py`
- Modify: `src/omniverse/cli.py`
- Modify: `tests/test_bangalore_economic_engine.py`

**Interfaces:**
- Produces:
  - `omniverse bangalore salary`
  - `omniverse bangalore col-sim`
  - `omniverse bangalore moneyflow-sim`
  - `omniverse bangalore projects`
  - `omniverse bangalore overview`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_bangalore_economic_engine.py
from click.testing import CliRunner
from omniverse.cli import cli

def test_cli_bangalore_salary():
    runner = CliRunner()
    result = runner.invoke(cli, ["bangalore", "salary", "--tier", "TIER_1_GCC", "--role", "SDE_2"])
    assert result.exit_code == 0
    assert "TIER_1_GCC" in result.output
    assert "Monthly Net In-Hand" in result.output

def test_cli_bangalore_projects():
    runner = CliRunner()
    result = runner.invoke(cli, ["bangalore", "projects"])
    assert result.exit_code == 0
    assert "BLR-PROJ-01" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bangalore_economic_engine.py::test_cli_bangalore_salary -v`  
Expected: FAIL with `No such command 'salary'` or `exit_code != 0`

- [ ] **Step 3: Implement CLI commands in `cli_commands.py` & wire into `src/omniverse/cli.py`**

Wire the Click/Rich commands into the CLI.

- [ ] **Step 4: Run all tests to verify 100% pass rate**

Run:
```bash
pytest tests/test_bangalore_economic_engine.py -v
pytest tests/test_bangalore_cashflow.py -v
```
Expected: PASS (100% green, zero regressions)

- [ ] **Step 5: Commit**

```bash
git add src/omniverse/modules/bangalore/cli_commands.py src/omniverse/cli.py tests/test_bangalore_economic_engine.py
git commit -m "feat(bangalore): add CLI subcommands and complete ecosystem integration"
```
