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

