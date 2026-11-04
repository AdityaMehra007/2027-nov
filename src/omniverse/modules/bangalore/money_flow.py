"""Macro-economic capital velocity and money flow simulation across Bangalore tech corridors."""

from __future__ import annotations

from omniverse.modules.bangalore.models import MoneyFlowSimulationResult


def simulate_capital_flow(
    inflow_amount_inr: float,
    source: str = "GCC_OPEX",
) -> MoneyFlowSimulationResult:
    """Simulates how institutional capital inflows disperse across corporate, municipal,

    residential real estate, and consumer merchant sectors in Bengaluru.
    """
    inflow = float(inflow_amount_inr)

    # 1. Corporate Allocation Breakdown (strictly sums to 100% of inflow)
    payroll = round(inflow * 0.65, 2)
    commercial_lease = round(inflow * 0.20, 2)
    cloud_infra = round(inflow - payroll - commercial_lease, 2)

    # 2. Downstream dispersion from tech workforce salaries
    income_tax_tds = round(payroll * 0.25, 2)
    net_in_hand = payroll - income_tax_tds

    residential_rent = round(net_in_hand * 0.35, 2)
    rental_deposits_frozen = round(residential_rent * (10.0 / 12.0), 2)
    merchant_spend = round(net_in_hand * 0.30, 2)
    remittance_outflow = round(net_in_hand * 0.15, 2)
    capital_market_sip = round(net_in_hand - residential_rent - merchant_spend - remittance_outflow, 2)

    # 3. Macro Multipliers & Absorption Metrics
    total_local_transactions = inflow + net_in_hand + merchant_spend
    velocity_ratio = round(total_local_transactions / max(1.0, inflow), 2)
    landlord_absorption = round(residential_rent / max(1.0, payroll), 4)

    local_retained = residential_rent + merchant_spend + commercial_lease
    retainment_pct = round((local_retained / max(1.0, inflow)) * 100.0, 2)

    return MoneyFlowSimulationResult(
        capital_inflow_inr=inflow,
        inflow_source=source,
        payroll_allocation_inr=payroll,
        cloud_infra_capex_inr=cloud_infra,
        commercial_office_lease_inr=commercial_lease,
        income_tax_tds_leakage_inr=income_tax_tds,
        residential_rent_to_landlords_inr=residential_rent,
        rental_deposits_frozen_inr=rental_deposits_frozen,
        local_merchant_spend_inr=merchant_spend,
        domestic_remittance_outflow_inr=remittance_outflow,
        capital_market_sip_inr=capital_market_sip,
        capital_velocity_ratio=velocity_ratio,
        local_retainment_percentage=retainment_pct,
        landlord_absorption_rate=landlord_absorption,
    )
