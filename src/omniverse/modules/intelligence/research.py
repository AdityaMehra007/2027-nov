from omniverse.modules.intelligence.models import CompanyProfile

class CompanyIntelligenceEngine:
    """Evaluates business fundamentals, balance sheet health, and competitive moats."""

    def analyze_company(
        self,
        symbol: str,
        name: str,
        industry: str,
        annual_revenue_cr: float,
        net_profit_margin_pct: float,
        debt_to_equity: float
    ) -> CompanyProfile:
        # Determine Moat rating
        if net_profit_margin_pct >= 18.0 and debt_to_equity < 0.3:
            moat = "WIDE"
        elif net_profit_margin_pct >= 10.0 and debt_to_equity < 1.0:
            moat = "NARROW"
        else:
            moat = "NONE"

        # Calculate Financial Health Score (0 - 100)
        margin_score = min(40.0, (net_profit_margin_pct / 20.0) * 40.0)
        debt_score = max(0.0, 40.0 - (debt_to_equity * 40.0))
        scale_bonus = 20.0 if annual_revenue_cr > 10000.0 else 10.0
        health_score = round(margin_score + debt_score + scale_bonus, 2)

        return CompanyProfile(
            symbol=symbol,
            name=name,
            industry=industry,
            annual_revenue_cr=annual_revenue_cr,
            net_profit_margin_pct=net_profit_margin_pct,
            debt_to_equity=debt_to_equity,
            moat_rating=moat,
            financial_health_score=health_score
        )
