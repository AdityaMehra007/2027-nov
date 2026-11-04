from typing import List, Dict, Tuple
from omniverse.modules.bangalore.models import (
    CompanyTier,
    TechRole,
    SalaryBenchmark,
)

def compute_new_regime_tax(annual_gross_inr: float) -> float:
    """Calculates income tax under the Indian New Tax Regime (FY 2026-27).

    - Standard deduction: ₹75,000 for salaried employees
    - Section 87A rebate: zero tax if taxable income <= ₹7,00,000
    - Health & Education Cess: 4% surcharge on final tax
    """
    standard_deduction = 75000.0
    taxable = max(0.0, annual_gross_inr - standard_deduction)

    if taxable <= 700000.0:
        return 0.0

    tax = 0.0

    # Slab 1: Up to 3,00,000 @ 0%
    # Slab 2: 3,00,001 to 7,00,000 (4,00,000 @ 5%) = 20,000
    if taxable > 300000.0:
        tax += min(taxable - 300000.0, 400000.0) * 0.05

    # Slab 3: 7,00,001 to 10,00,000 (3,00,000 @ 10%) = 30,000
    if taxable > 700000.0:
        tax += min(taxable - 700000.0, 300000.0) * 0.10

    # Slab 4: 10,00,001 to 12,00,000 (2,00,000 @ 15%) = 30,000
    if taxable > 1000000.0:
        tax += min(taxable - 1000000.0, 200000.0) * 0.15

    # Slab 5: 12,00,001 to 15,00,000 (3,00,000 @ 20%) = 60,000
    if taxable > 1200000.0:
        tax += min(taxable - 1200000.0, 300000.0) * 0.20

    # Slab 6: Above 15,00,000 @ 30%
    if taxable > 1500000.0:
        tax += (taxable - 1500000.0) * 0.30

    # 4% Health & Education Cess
    cess = tax * 0.04
    return round(tax + cess, 2)


# Baseline Salary Matrices: (Base_INR, Variable_Percent, Equity_Percent_Of_Base, Default_Exp_Years)
COMPENSATION_MATRIX: Dict[Tuple[CompanyTier, TechRole], Tuple[float, float, float, float]] = {
    # 1. Tier 1 GCCs (Google, Uber, Walmart Tech, Goldman Sachs, Target)
    (CompanyTier.TIER_1_GCC, TechRole.SDE_1): (2600000.0, 0.15, 0.35, 1.5),
    (CompanyTier.TIER_1_GCC, TechRole.SDE_2): (4400000.0, 0.15, 0.45, 3.5),
    (CompanyTier.TIER_1_GCC, TechRole.SDE_3_SENIOR): (6800000.0, 0.20, 0.60, 6.5),
    (CompanyTier.TIER_1_GCC, TechRole.STAFF_PRINCIPAL): (10500000.0, 0.25, 0.85, 10.0),
    (CompanyTier.TIER_1_GCC, TechRole.ENGINEERING_MANAGER): (8800000.0, 0.25, 0.70, 8.5),
    (CompanyTier.TIER_1_GCC, TechRole.PRODUCT_MANAGER): (5500000.0, 0.20, 0.40, 5.0),
    (CompanyTier.TIER_1_GCC, TechRole.DATA_AI_SCIENTIST): (5000000.0, 0.20, 0.50, 4.0),

    # 2. Unicorns & Series B+ (Swiggy, Razorpay, Zepto, CRED, Meesho)
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.SDE_1): (1800000.0, 0.10, 0.25, 1.5),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.SDE_2): (3400000.0, 0.15, 0.40, 3.5),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.SDE_3_SENIOR): (5400000.0, 0.15, 0.50, 6.5),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.STAFF_PRINCIPAL): (8500000.0, 0.20, 0.75, 10.0),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.ENGINEERING_MANAGER): (7200000.0, 0.20, 0.60, 8.5),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.PRODUCT_MANAGER): (4400000.0, 0.15, 0.35, 5.0),
    (CompanyTier.UNICORN_SERIES_B_PLUS, TechRole.DATA_AI_SCIENTIST): (4000000.0, 0.15, 0.45, 4.0),

    # 3. Early Stage VC (Seed / Series A)
    (CompanyTier.EARLY_STAGE_VC, TechRole.SDE_1): (1200000.0, 0.05, 0.40, 1.5),
    (CompanyTier.EARLY_STAGE_VC, TechRole.SDE_2): (2400000.0, 0.10, 0.50, 3.5),
    (CompanyTier.EARLY_STAGE_VC, TechRole.SDE_3_SENIOR): (3800000.0, 0.10, 0.70, 6.5),
    (CompanyTier.EARLY_STAGE_VC, TechRole.STAFF_PRINCIPAL): (5800000.0, 0.15, 1.00, 10.0),
    (CompanyTier.EARLY_STAGE_VC, TechRole.ENGINEERING_MANAGER): (4800000.0, 0.15, 0.80, 8.5),
    (CompanyTier.EARLY_STAGE_VC, TechRole.PRODUCT_MANAGER): (3000000.0, 0.10, 0.50, 5.0),
    (CompanyTier.EARLY_STAGE_VC, TechRole.DATA_AI_SCIENTIST): (2800000.0, 0.10, 0.60, 4.0),

    # 4. IT Services Enterprise (Infosys, TCS, Wipro, LTIMindtree)
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.SDE_1): (450000.0, 0.10, 0.00, 1.5),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.SDE_2): (1100000.0, 0.12, 0.00, 3.5),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.SDE_3_SENIOR): (2000000.0, 0.15, 0.00, 6.5),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.STAFF_PRINCIPAL): (3600000.0, 0.20, 0.05, 10.0),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.ENGINEERING_MANAGER): (3200000.0, 0.20, 0.05, 8.5),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.PRODUCT_MANAGER): (2200000.0, 0.15, 0.00, 5.0),
    (CompanyTier.IT_SERVICES_ENTERPRISE, TechRole.DATA_AI_SCIENTIST): (1800000.0, 0.15, 0.00, 4.0),

    # 5. Deep Tech & Defense Public (ISRO, HAL, BEL, DRDO)
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.SDE_1): (800000.0, 0.20, 0.00, 1.5),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.SDE_2): (1400000.0, 0.25, 0.00, 3.5),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.SDE_3_SENIOR): (2200000.0, 0.30, 0.00, 6.5),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.STAFF_PRINCIPAL): (3400000.0, 0.35, 0.00, 10.0),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.ENGINEERING_MANAGER): (3000000.0, 0.30, 0.00, 8.5),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.PRODUCT_MANAGER): (2000000.0, 0.25, 0.00, 5.0),
    (CompanyTier.DEEP_TECH_PUBLIC, TechRole.DATA_AI_SCIENTIST): (2100000.0, 0.25, 0.00, 4.0),
}


def get_salary_benchmark(
    tier: CompanyTier,
    role: TechRole,
    experience_years: float = None,
) -> SalaryBenchmark:
    """Computes a realistic salary benchmark with take-home pay and tax."""
    key = (tier, role)
    if key not in COMPENSATION_MATRIX:
        # Default fallback
        base, var_pct, eq_pct, exp = (2000000.0, 0.10, 0.20, 3.0)
    else:
        base, var_pct, eq_pct, exp = COMPENSATION_MATRIX[key]

    if experience_years is None:
        experience_years = exp

    var_bonus = round(base * var_pct, 2)
    equity = round(base * eq_pct, 2)
    total_ctc = round(base + var_bonus + equity, 2)

    # Cash compensation subject to income tax and EPF
    cash_gross = base + var_bonus
    monthly_gross = round(cash_gross / 12.0, 2)

    tax_annual = compute_new_regime_tax(cash_gross)

    # Standard EPF deduction capped at 12% of basic (or ceiling 21,600/year minimum)
    epf_annual = min(base * 0.12, 180000.0)

    annual_net_cash = max(0.0, cash_gross - tax_annual - epf_annual)
    monthly_net = round(annual_net_cash / 12.0, 2)

    return SalaryBenchmark(
        company_tier=tier,
        role=role,
        experience_years=experience_years,
        base_salary_inr=base,
        variable_bonus_inr=var_bonus,
        equity_annual_inr=equity,
        total_ctc_inr=total_ctc,
        monthly_gross_inr=monthly_gross,
        annual_income_tax_inr=tax_annual,
        monthly_net_in_hand_inr=monthly_net,
    )


def compare_tiers(role: TechRole, experience_years: float = None) -> List[SalaryBenchmark]:
    """Returns salary benchmarks across all 5 company tiers for a given role."""
    tiers = [
        CompanyTier.TIER_1_GCC,
        CompanyTier.UNICORN_SERIES_B_PLUS,
        CompanyTier.EARLY_STAGE_VC,
        CompanyTier.IT_SERVICES_ENTERPRISE,
        CompanyTier.DEEP_TECH_PUBLIC,
    ]
    return [get_salary_benchmark(tier, role, experience_years) for tier in tiers]
