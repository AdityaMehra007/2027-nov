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
