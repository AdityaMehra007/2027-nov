from typing import Optional
from omniverse.modules.bangalore.models import (
    CompanyTier,
    TechRole,
    BangaloreCluster,
)
from omniverse.modules.bangalore.salary_benchmarking import (
    get_salary_benchmark,
    compare_tiers,
)
from omniverse.modules.bangalore.cost_of_living import (
    analyze_cluster_living,
    get_cluster_col,
)
from omniverse.modules.bangalore.money_flow import simulate_capital_flow
from omniverse.modules.bangalore.projects import (
    get_project_archetypes,
    get_project_by_id,
)

def format_salary_benchmark(tier_str: str, role_str: str, exp: Optional[float] = None) -> str:
    try:
        tier = CompanyTier(tier_str)
    except ValueError:
        tier = CompanyTier.TIER_1_GCC

    try:
        role = TechRole(role_str)
    except ValueError:
        role = TechRole.SDE_2

    bench = get_salary_benchmark(tier=tier, role=role, experience_years=exp)

    lines = [
        "==================================================================",
        f"  BENGALURU TECH SALARY BENCHMARK: {bench.role.value}",
        "==================================================================",
        f"Company Tier        : {bench.company_tier.value}",
        f"Experience Level    : ~{bench.experience_years} years",
        "------------------------------------------------------------------",
        f"Fixed Annual Base   : ₹{bench.base_salary_inr:,.2f}",
        f"Performance Bonus   : ₹{bench.variable_bonus_inr:,.2f}",
        f"Annual Stock/Equity : ₹{bench.equity_annual_inr:,.2f} (RSUs / ESOPs)",
        f"Total Annual CTC    : ₹{bench.total_ctc_inr:,.2f}",
        "------------------------------------------------------------------",
        f"Monthly Gross Cash  : ₹{bench.monthly_gross_inr:,.2f}",
        f"Income Tax (Annual) : ₹{bench.annual_income_tax_inr:,.2f} (New Tax Regime FY 26-27)",
        f"Monthly Net In-Hand : ₹{bench.monthly_net_in_hand_inr:,.2f} (Bank credit on 1st)",
        "==================================================================",
    ]
    return "\n".join(lines)


def format_col_analysis(cluster_str: str, bhk: int, tier_str: str, role_str: str) -> str:
    try:
        cluster = BangaloreCluster(cluster_str)
    except ValueError:
        cluster = BangaloreCluster.HSR_LAYOUT

    try:
        tier = CompanyTier(tier_str)
    except ValueError:
        tier = CompanyTier.TIER_1_GCC

    try:
        role = TechRole(role_str)
    except ValueError:
        role = TechRole.SDE_2

    salary = get_salary_benchmark(tier=tier, role=role)
    analysis = analyze_cluster_living(cluster=cluster, bhk=bhk, salary=salary)

    lines = [
        "==================================================================",
        f"  BENGALURU COST-OF-LIVING & DEPOSIT LOCK: {analysis.cluster.value.upper()}",
        "==================================================================",
        f"Housing Format      : {analysis.bhk} BHK Apartment",
        f"Monthly House Rent  : ₹{analysis.rent_inr:,.2f} / month",
        f"10-Mo Locked Deposit: ₹{analysis.deposit_lock_amount_inr:,.2f} (Frozen with landlord)",
        f"Deposit Opp. Cost   : ₹{analysis.deposit_annual_opportunity_cost_inr:,.2f} / year (@ 7.5% risk-free)",
        "------------------------------------------------------------------",
        f"Utilities (BESCOM)  : ₹{analysis.monthly_utilities_inr:,.2f} / month",
        f"Commute & Traffic   : ₹{analysis.monthly_commute_inr:,.2f} / month (ORR congestion indexed)",
        f"Dining & Lifestyle  : ₹{analysis.monthly_lifestyle_inr:,.2f} / month (Cafes, breweries, Zepto)",
        f"Total Monthly Outflow: ₹{analysis.total_monthly_expenses_inr:,.2f} / month",
        "------------------------------------------------------------------",
        f"Monthly Net In-Hand : ₹{analysis.monthly_net_in_hand_inr:,.2f}",
        f"Monthly Net Savings : ₹{analysis.monthly_savings_inr:,.2f}",
        f"Savings Ratio       : {analysis.savings_ratio * 100:.1f}% of net income retained",
        "==================================================================",
    ]
    return "\n".join(lines)


def format_money_flow_simulation(inflow_amount_inr: float, source: str = "GCC_OPEX") -> str:
    res = simulate_capital_flow(inflow_amount_inr=inflow_amount_inr, source=source)

    lines = [
        "==================================================================",
        f"  BENGALURU CAPITAL FLYWHEEL SIMULATION ({res.inflow_source})",
        "==================================================================",
        f"Total Capital Inflow  : ₹{res.capital_inflow_inr:,.2f}",
        "------------------------------------------------------------------",
        "CORPORATE EXPENDITURE ALLOCATION:",
        f"• White-Collar Payroll: ₹{res.payroll_allocation_inr:,.2f} ({res.payroll_allocation_inr / res.capital_inflow_inr * 100:.0f}%)",
        f"• Cloud & Data Infra  : ₹{res.cloud_infra_capex_inr:,.2f} ({res.cloud_infra_capex_inr / res.capital_inflow_inr * 100:.0f}%)",
        f"• Commercial Leases   : ₹{res.commercial_office_lease_inr:,.2f} ({res.commercial_office_lease_inr / res.capital_inflow_inr * 100:.0f}%)",
        "------------------------------------------------------------------",
        "CITY CIRCULATION & CAPITAL CASCADES (From Payroll):",
        f"• TDS Tax Leakage     : ₹{res.income_tax_tds_leakage_inr:,.2f} (Remitted to Union Govt)",
        f"• Landlord House Rent : ₹{res.residential_rent_to_landlords_inr:,.2f}",
        f"• 10-Mo Deposits Lock : ₹{res.rental_deposits_frozen_inr:,.2f} (Non-circulating property sink)",
        f"• Local Merchant Spend: ₹{res.local_merchant_spend_inr:,.2f} (High-velocity UPI retail/F&B)",
        f"• Out-of-State Remit  : ₹{res.domestic_remittance_outflow_inr:,.2f} (Sent to hometowns)",
        f"• Zerodha/Groww SIPs  : ₹{res.capital_market_sip_inr:,.2f} (Capital market accumulation)",
        "------------------------------------------------------------------",
        "MACROECONOMIC INDICATORS:",
        f"Capital Velocity Ratio: {res.capital_velocity_ratio}x (Stimulated local transactions)",
        f"Landlord Absorption   : {res.landlord_absorption_rate * 100:.1f}% of net payroll captured",
        f"Local City Retainment : {res.local_retainment_percentage:.1f}% stays in Karnataka",
        "==================================================================",
    ]
    return "\n".join(lines)


def format_project_archetypes_list() -> str:
    projects = get_project_archetypes()
    lines = [
        "==================================================================",
        "  BENGALURU TOP ENGINEERING PROJECT ARCHETYPES & TECH STACKS",
        "==================================================================",
    ]
    for p in projects:
        companies_str = ", ".join(p.archetype_companies)
        stack_str = ", ".join(p.core_tech_stack)
        lines.extend([
            f"[{p.project_id}] {p.name}",
            f"  Sector     : {p.primary_sector}",
            f"  Companies  : {companies_str}",
            f"  Core Stack : {stack_str}",
            f"  Scale      : {p.scale_metrics}",
            f"  Architecture: {p.architecture_summary}",
            "------------------------------------------------------------------",
        ])
    lines.append("==================================================================")
    return "\n".join(lines)


def format_overview() -> str:
    lines = [
        "==================================================================",
        "  NAMMA CASHFLOW ENGINE — BENGALURU MACROECONOMIC OVERVIEW",
        "==================================================================",
        "City                 : Bengaluru (Silicon Valley of India)",
        "Annual Tech Economy  : ~$50+ Billion Annual Gross Value",
        "Primary Inflow Sinks : 500+ Tech GCCs, Tier-1 VCs, IT Services, ISRO",
        "Capital Velocity Rails: NPCI UPI, Real-time IMPS, RTGS",
        "Distinct Local Traits:",
        "  • 5-to-10 month interest-free rental deposit lock on apartments",
        "  • 4-tier compensation hierarchy: GCCs > Unicorns > Early VC > IT Services",
        "  • High-frequency weekend micro-commerce (Indiranagar, Koramangala, HSR)",
        "==================================================================",
    ]
    return "\n".join(lines)
