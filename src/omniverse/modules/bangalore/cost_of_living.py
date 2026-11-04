from typing import Dict
from omniverse.modules.bangalore.models import (
    BangaloreCluster,
    ClusterCostOfLiving,
    ClusterLivingAnalysis,
    SalaryBenchmark,
)

CLUSTER_COL_DATA: Dict[BangaloreCluster, ClusterCostOfLiving] = {
    BangaloreCluster.KORAMANGALA: ClusterCostOfLiving(
        cluster=BangaloreCluster.KORAMANGALA,
        avg_1bhk_rent_inr=24000.0,
        avg_2bhk_rent_inr=42000.0,
        avg_3bhk_rent_inr=65000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=7000.0,
        lifestyle_monthly_inr=18000.0,
        utilities_monthly_inr=5000.0,
    ),
    BangaloreCluster.INDIRANAGAR: ClusterCostOfLiving(
        cluster=BangaloreCluster.INDIRANAGAR,
        avg_1bhk_rent_inr=26000.0,
        avg_2bhk_rent_inr=45000.0,
        avg_3bhk_rent_inr=70000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=6500.0,
        lifestyle_monthly_inr=22000.0,
        utilities_monthly_inr=5500.0,
    ),
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
    BangaloreCluster.WHITEFIELD: ClusterCostOfLiving(
        cluster=BangaloreCluster.WHITEFIELD,
        avg_1bhk_rent_inr=18000.0,
        avg_2bhk_rent_inr=32000.0,
        avg_3bhk_rent_inr=48000.0,
        deposit_lock_months=8,
        commute_cost_monthly_inr=8500.0,
        lifestyle_monthly_inr=12000.0,
        utilities_monthly_inr=4500.0,
    ),
    BangaloreCluster.BELLANDUR: ClusterCostOfLiving(
        cluster=BangaloreCluster.BELLANDUR,
        avg_1bhk_rent_inr=20000.0,
        avg_2bhk_rent_inr=36000.0,
        avg_3bhk_rent_inr=52000.0,
        deposit_lock_months=8,
        commute_cost_monthly_inr=8000.0,
        lifestyle_monthly_inr=14000.0,
        utilities_monthly_inr=5000.0,
    ),
    BangaloreCluster.ELECTRONIC_CITY: ClusterCostOfLiving(
        cluster=BangaloreCluster.ELECTRONIC_CITY,
        avg_1bhk_rent_inr=14000.0,
        avg_2bhk_rent_inr=24000.0,
        avg_3bhk_rent_inr=35000.0,
        deposit_lock_months=6,
        commute_cost_monthly_inr=7500.0,
        lifestyle_monthly_inr=9000.0,
        utilities_monthly_inr=3500.0,
    ),
    BangaloreCluster.JAYANAGAR: ClusterCostOfLiving(
        cluster=BangaloreCluster.JAYANAGAR,
        avg_1bhk_rent_inr=19000.0,
        avg_2bhk_rent_inr=30000.0,
        avg_3bhk_rent_inr=45000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=5000.0,
        lifestyle_monthly_inr=11000.0,
        utilities_monthly_inr=4000.0,
    ),
    BangaloreCluster.JP_NAGAR: ClusterCostOfLiving(
        cluster=BangaloreCluster.JP_NAGAR,
        avg_1bhk_rent_inr=18000.0,
        avg_2bhk_rent_inr=28000.0,
        avg_3bhk_rent_inr=42000.0,
        deposit_lock_months=10,
        commute_cost_monthly_inr=5500.0,
        lifestyle_monthly_inr=11000.0,
        utilities_monthly_inr=4000.0,
    ),
}


def get_cluster_col(cluster: BangaloreCluster) -> ClusterCostOfLiving:
    """Retrieves standard cost-of-living metrics for a target Bengaluru cluster."""
    if cluster in CLUSTER_COL_DATA:
        return CLUSTER_COL_DATA[cluster]
    return CLUSTER_COL_DATA[BangaloreCluster.HSR_LAYOUT]


def analyze_cluster_living(
    cluster: BangaloreCluster,
    bhk: int,
    salary: SalaryBenchmark,
    risk_free_rate: float = 0.075,
) -> ClusterLivingAnalysis:
    """Computes full cost of living, 10-month rental deposit lock, and savings."""
    col = get_cluster_col(cluster)

    if bhk <= 1:
        rent = col.avg_1bhk_rent_inr
    elif bhk == 2:
        rent = col.avg_2bhk_rent_inr
    else:
        rent = col.avg_3bhk_rent_inr

    deposit_amount = round(rent * col.deposit_lock_months, 2)
    deposit_opp_cost_annual = round(deposit_amount * risk_free_rate, 2)

    total_monthly_expenses = round(
        rent + col.utilities_monthly_inr + col.commute_cost_monthly_inr + col.lifestyle_monthly_inr,
        2
    )

    monthly_net = salary.monthly_net_in_hand_inr
    monthly_savings = round(monthly_net - total_monthly_expenses, 2)

    savings_ratio = 0.0
    if monthly_net > 0:
        savings_ratio = round(monthly_savings / monthly_net, 4)

    return ClusterLivingAnalysis(
        cluster=cluster,
        bhk=bhk,
        rent_inr=rent,
        deposit_lock_amount_inr=deposit_amount,
        deposit_annual_opportunity_cost_inr=deposit_opp_cost_annual,
        monthly_utilities_inr=col.utilities_monthly_inr,
        monthly_commute_inr=col.commute_cost_monthly_inr,
        monthly_lifestyle_inr=col.lifestyle_monthly_inr,
        total_monthly_expenses_inr=total_monthly_expenses,
        monthly_net_in_hand_inr=monthly_net,
        monthly_savings_inr=monthly_savings,
        savings_ratio=savings_ratio,
    )
