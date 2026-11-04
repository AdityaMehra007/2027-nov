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


def test_compute_new_regime_tax():
    from omniverse.modules.bangalore.salary_benchmarking import compute_new_regime_tax

    # Below rebate threshold (<= 7L) should have 0 tax
    assert compute_new_regime_tax(650000.0) == 0.0
    assert compute_new_regime_tax(775000.0) == 0.0  # 775k - 75k = 700k -> 0 tax

    # 15L gross: standard deduction 75k => 14.25L taxable
    # 3-7L: 20k, 7-10L: 30k, 10-12L: 30k, 12-14.25L: 45k => 125,000 + 4% cess = 130,000
    tax_15l = compute_new_regime_tax(1500000.0)
    assert tax_15l == 130000.0

    # 30L gross: standard deduction 75k => 29.25L taxable
    # 0-15L: 140k. Above 15L (14.25L @ 30%) = 427,500. Total = 567,500 + 4% = 590,200
    tax_30l = compute_new_regime_tax(3000000.0)
    assert tax_30l == 590200.0


def test_get_salary_benchmark():
    from omniverse.modules.bangalore.salary_benchmarking import (
        get_salary_benchmark,
        compare_tiers,
    )

    gcc_sde2 = get_salary_benchmark(CompanyTier.TIER_1_GCC, TechRole.SDE_2)
    assert gcc_sde2.base_salary_inr >= 3800000.0
    assert gcc_sde2.total_ctc_inr > gcc_sde2.base_salary_inr
    assert gcc_sde2.monthly_net_in_hand_inr > 0.0

    it_sde2 = get_salary_benchmark(CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.SDE_2)
    assert it_sde2.total_ctc_inr < gcc_sde2.total_ctc_inr

    tiers = compare_tiers(TechRole.SDE_2)
    assert len(tiers) == 5
    tier_names = {t.company_tier for t in tiers}
    assert CompanyTier.TIER_1_GCC in tier_names
    assert CompanyTier.IT_SERVICES_ENTERPRISE in tier_names


def test_cost_of_living_hsr_layout():
    from omniverse.modules.bangalore.cost_of_living import (
        get_cluster_col,
        analyze_cluster_living,
    )
    from omniverse.modules.bangalore.salary_benchmarking import get_salary_benchmark

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


def test_money_flow_simulation_conservation():
    from omniverse.modules.bangalore.money_flow import simulate_capital_flow

    inflow = 100000000.0  # ₹10 Crores
    res = simulate_capital_flow(inflow_amount_inr=inflow, source="GCC_OPEX")

    assert res.capital_inflow_inr == inflow
    assert res.payroll_allocation_inr > 0.0
    assert res.residential_rent_to_landlords_inr > 0.0
    assert res.rental_deposits_frozen_inr > 0.0
    assert res.local_merchant_spend_inr > 0.0
    assert res.capital_velocity_ratio > 1.0
    assert 0.0 <= res.landlord_absorption_rate <= 1.0

    # Strict conservation test: corporate allocation breakdown must equal inflow
    allocated_sum = (
        res.payroll_allocation_inr
        + res.cloud_infra_capex_inr
        + res.commercial_office_lease_inr
    )
    assert allocated_sum == pytest.approx(inflow, rel=1e-3)


def test_project_archetypes_catalog():
    from omniverse.modules.bangalore.projects import get_project_archetypes, get_project_by_id

    projects = get_project_archetypes()
    assert len(projects) >= 5

    proj_ids = [p.project_id for p in projects]
    assert "BLR-PROJ-01" in proj_ids  # Quick-commerce
    assert "BLR-PROJ-02" in proj_ids  # FinTech UPI switch
    assert "BLR-PROJ-03" in proj_ids  # GCC Data Lake
    assert "BLR-PROJ-04" in proj_ids  # Dev Tools & SaaS
    assert "BLR-PROJ-05" in proj_ids  # Deep Tech Defense / Space

    p1 = get_project_by_id("BLR-PROJ-01")
    assert p1 is not None
    assert "Zepto" in p1.archetype_companies or "Swiggy" in p1.archetype_companies
    assert len(p1.core_tech_stack) >= 3

    p5 = get_project_by_id("BLR-PROJ-05")
    assert p5 is not None
    assert "ISRO" in p5.archetype_companies or "HAL" in p5.archetype_companies


def test_api_salary_benchmarks(tmp_path):
    from fastapi.testclient import TestClient
    from omniverse.api.app import create_app
    from omniverse.core.database import DatabaseEngine

    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    client = TestClient(app)

    res = client.get("/api/v1/bangalore/salary-benchmarks?tier=TIER_1_GCC&role=SDE_2")
    assert res.status_code == 200
    data = res.json()
    assert data["company_tier"] == "TIER_1_GCC"
    assert data["role"] == "SDE_2"
    assert data["total_ctc_inr"] > 0
    assert data["monthly_net_in_hand_inr"] > 0

    res_compare = client.get("/api/v1/bangalore/salary-compare?role=SDE_2")
    assert res_compare.status_code == 200
    assert len(res_compare.json()) == 5


def test_api_col_simulate(tmp_path):
    from fastapi.testclient import TestClient
    from omniverse.api.app import create_app
    from omniverse.core.database import DatabaseEngine

    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    client = TestClient(app)

    res = client.post("/api/v1/bangalore/col-simulate", json={
        "cluster": "HSR Layout",
        "bhk": 2,
        "company_tier": "TIER_1_GCC",
        "role": "SDE_2"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["cluster"] == "HSR Layout"
    assert data["deposit_lock_amount_inr"] == 380000.0
    assert data["savings_ratio"] > 0


def test_api_moneyflow_simulate(tmp_path):
    from fastapi.testclient import TestClient
    from omniverse.api.app import create_app
    from omniverse.core.database import DatabaseEngine

    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    client = TestClient(app)

    res = client.post("/api/v1/bangalore/moneyflow-simulate", json={
        "inflow_amount_inr": 100000000.0,
        "source": "GCC_OPEX"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["capital_inflow_inr"] == 100000000.0
    assert data["capital_velocity_ratio"] > 1.0


def test_api_projects(tmp_path):
    from fastapi.testclient import TestClient
    from omniverse.api.app import create_app
    from omniverse.core.database import DatabaseEngine

    db_file = tmp_path / "api_test.db"
    db_engine = DatabaseEngine(f"sqlite:///{db_file}")
    db_engine.init_db()
    app = create_app(db_engine=db_engine)
    client = TestClient(app)

    res = client.get("/api/v1/bangalore/projects")
    assert res.status_code == 200
    assert len(res.json()) >= 5
    assert res.json()[0]["project_id"] == "BLR-PROJ-01"

    res_single = client.get("/api/v1/bangalore/projects/BLR-PROJ-01")
    assert res_single.status_code == 200
    assert res_single.json()["project_id"] == "BLR-PROJ-01"





