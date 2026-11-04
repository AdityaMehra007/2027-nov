"""Cost of living models, cluster data, and cash-flow analyses for Bangalore tech clusters."""

from __future__ import annotations

from omniverse.modules.bangalore.models import (
    BangaloreCluster,
    ClusterCostOfLiving,
    ClusterLivingAnalysis,
    SalaryBenchmark,
)

CLUSTER_COL_PROFILES: dict[BangaloreCluster, ClusterCostOfLiving] = {
    BangaloreCluster.HSR_LAYOUT: ClusterCostOfLiving(
        cluster=BangaloreCluster.HSR_LAYOUT,
        avg_1bhk_rent_inr=22000.0,
        avg_2bhk_rent_inr=38000.0,
        avg_3bhk_rent_inr=55000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=6500.0,
        lifestyle_monthly_inr=15000.0,
        utilities_monthly_inr=4500.0,
    ),
    BangaloreCluster.INDIRANAGAR: ClusterCostOfLiving(
        cluster=BangaloreCluster.INDIRANAGAR,
        avg_1bhk_rent_inr=28000.0,
        avg_2bhk_rent_inr=48000.0,
        avg_3bhk_rent_inr=75000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=7000.0,
        lifestyle_monthly_inr=22000.0,
        utilities_monthly_inr=5000.0,
    ),
    BangaloreCluster.KORAMANGALA: ClusterCostOfLiving(
        cluster=BangaloreCluster.KORAMANGALA,
        avg_1bhk_rent_inr=25000.0,
        avg_2bhk_rent_inr=44000.0,
        avg_3bhk_rent_inr=68000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=7500.0,
        lifestyle_monthly_inr=20000.0,
        utilities_monthly_inr=4800.0,
    ),
    BangaloreCluster.WHITEFIELD: ClusterCostOfLiving(
        cluster=BangaloreCluster.WHITEFIELD,
        avg_1bhk_rent_inr=18000.0,
        avg_2bhk_rent_inr=32000.0,
        avg_3bhk_rent_inr=46000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=8000.0,
        lifestyle_monthly_inr=12000.0,
        utilities_monthly_inr=4200.0,
    ),
    BangaloreCluster.BELLANDUR: ClusterCostOfLiving(
        cluster=BangaloreCluster.BELLANDUR,
        avg_1bhk_rent_inr=22000.0,
        avg_2bhk_rent_inr=36000.0,
        avg_3bhk_rent_inr=52000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=8500.0,
        lifestyle_monthly_inr=14000.0,
        utilities_monthly_inr=4500.0,
    ),
    BangaloreCluster.ELECTRONIC_CITY: ClusterCostOfLiving(
        cluster=BangaloreCluster.ELECTRONIC_CITY,
        avg_1bhk_rent_inr=14000.0,
        avg_2bhk_rent_inr=24000.0,
        avg_3bhk_rent_inr=35000.0,
        deposit_lock_months=8,
        commute_cost_monthly_inr=6000.0,
        lifestyle_monthly_inr=10000.0,
        utilities_monthly_inr=3800.0,
    ),
}


def get_cluster_col(cluster: BangaloreCluster) -> ClusterCostOfLiving:
    """Retrieves standard cost-of-living profile for a Bangalore cluster."""
    return CLUSTER_COL_PROFILES.get(cluster, CLUSTER_COL_PROFILES[BangaloreCluster.HSR_LAYOUT])


def analyze_cluster_living(
    cluster: BangaloreCluster,
    bhk: int,
    salary: SalaryBenchmark,
) -> ClusterLivingAnalysis:
    """Calculates living expenses, security deposit opportunity cost, and savings ratio."""
    col = get_cluster_col(cluster)

    if bhk == 1:
        rent = col.avg_1bhk_rent_inr
    elif bhk == 2:
        rent = col.avg_2bhk_rent_inr
    else:
        rent = col.avg_3bhk_rent_inr

    deposit_lock = rent * col.deposit_lock_months
    deposit_opp_cost = deposit_lock * 0.075  # 7.5% annual risk-free opportunity cost

    total_expenses = (
        rent
        + col.utilities_monthly_inr
        + col.commute_cost_monthly_inr
        + col.lifestyle_monthly_inr
    )
    monthly_savings = max(0.0, salary.monthly_net_in_hand_inr - total_expenses)
    savings_ratio = round(monthly_savings / max(1.0, salary.monthly_net_in_hand_inr), 4)

    return ClusterLivingAnalysis(
        cluster=cluster,
        bhk=bhk,
        rent_inr=rent,
        deposit_lock_amount_inr=deposit_lock,
        deposit_annual_opportunity_cost_inr=deposit_opp_cost,
        monthly_utilities_inr=col.utilities_monthly_inr,
        monthly_commute_inr=col.commute_cost_monthly_inr,
        monthly_lifestyle_inr=col.lifestyle_monthly_inr,
        total_monthly_expenses_inr=total_expenses,
        monthly_net_in_hand_inr=salary.monthly_net_in_hand_inr,
        monthly_savings_inr=monthly_savings,
        savings_ratio=savings_ratio,
    )
