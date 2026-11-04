import math
from typing import Dict, Any, List
from pydantic import BaseModel

class OptionGreeks(BaseModel):
    call_price: float
    put_price: float
    delta_call: float
    delta_put: float
    gamma: float
    vega: float
    theta_call: float
    theta_put: float
    rho_call: float
    rho_put: float

class TriangularArbitrageOpportunity(BaseModel):
    pair_path: List[str]
    start_amount: float
    end_amount: float
    profit_pct: float
    arbitrage_detected: bool

class DerivativesEngine:
    """Quantitative derivatives pricing via Black-Scholes model and triangular FX arbitrage detection."""

    @staticmethod
    def _std_norm_cdf(x: float) -> float:
        """Standard normal cumulative distribution function (Abramowitz & Stegun approximation)."""
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @staticmethod
    def _std_norm_pdf(x: float) -> float:
        """Standard normal probability density function."""
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

    def calculate_black_scholes_greeks(
        self,
        spot: float,
        strike: float,
        time_to_maturity_years: float,
        risk_free_rate: float,
        volatility: float
    ) -> OptionGreeks:
        """Computes European option prices and Greeks (Delta, Gamma, Vega, Theta, Rho)."""
        if time_to_maturity_years <= 0 or volatility <= 0:
            call = max(0.0, spot - strike)
            put = max(0.0, strike - spot)
            return OptionGreeks(
                call_price=call, put_price=put,
                delta_call=1.0 if spot > strike else 0.0,
                delta_put=-1.0 if strike > spot else 0.0,
                gamma=0.0, vega=0.0,
                theta_call=0.0, theta_put=0.0,
                rho_call=0.0, rho_put=0.0
            )

        s = spot
        k = strike
        t = time_to_maturity_years
        r = risk_free_rate
        v = volatility

        d1 = (math.log(s / k) + (r + 0.5 * v * v) * t) / (v * math.sqrt(t))
        d2 = d1 - v * math.sqrt(t)

        cdf_d1 = self._std_norm_cdf(d1)
        cdf_d2 = self._std_norm_cdf(d2)
        pdf_d1 = self._std_norm_pdf(d1)

        disc = math.exp(-r * t)

        call_price = s * cdf_d1 - k * disc * cdf_d2
        put_price = k * disc * self._std_norm_cdf(-d2) - s * self._std_norm_cdf(-d1)

        delta_call = cdf_d1
        delta_put = cdf_d1 - 1.0

        gamma = pdf_d1 / (s * v * math.sqrt(t))
        vega = (s * pdf_d1 * math.sqrt(t)) / 100.0  # Per 1% vol change

        # Annualized Theta converted to 1-day decay
        theta_call = (- (s * pdf_d1 * v) / (2.0 * math.sqrt(t)) - r * k * disc * cdf_d2) / 365.0
        theta_put = (- (s * pdf_d1 * v) / (2.0 * math.sqrt(t)) + r * k * disc * self._std_norm_cdf(-d2)) / 365.0

        rho_call = (k * t * disc * cdf_d2) / 100.0  # Per 1% interest rate change
        rho_put = (-k * t * disc * self._std_norm_cdf(-d2)) / 100.0

        return OptionGreeks(
            call_price=round(call_price, 2),
            put_price=round(put_price, 2),
            delta_call=round(delta_call, 4),
            delta_put=round(delta_put, 4),
            gamma=round(gamma, 6),
            vega=round(vega, 4),
            theta_call=round(theta_call, 4),
            theta_put=round(theta_put, 4),
            rho_call=round(rho_call, 4),
            rho_put=round(rho_put, 4)
        )

    def detect_triangular_arbitrage(
        self,
        rates: Dict[str, float],
        initial_capital: float = 100000.0
    ) -> TriangularArbitrageOpportunity:
        """Detects triangular cross-currency mispricings across 3 pairs (e.g. INR -> USD -> EUR -> INR)."""
        # Default market rates if not provided
        r_usd_inr = rates.get("USD_INR", 84.15)
        r_eur_usd = rates.get("EUR_USD", 1.085)
        r_eur_inr = rates.get("EUR_INR", 91.20)

        # Path: Start INR -> buy USD -> buy EUR -> sell EUR to INR
        # 1. INR -> USD: capital / r_usd_inr
        amt_usd = initial_capital / r_usd_inr
        # 2. USD -> EUR: amt_usd / r_eur_usd
        amt_eur = amt_usd / r_eur_usd
        # 3. EUR -> INR: amt_eur * r_eur_inr
        final_inr = amt_eur * r_eur_inr

        profit_pct = ((final_inr - initial_capital) / initial_capital) * 100.0

        return TriangularArbitrageOpportunity(
            pair_path=["INR", "USD", "EUR", "INR"],
            start_amount=round(initial_capital, 2),
            end_amount=round(final_inr, 2),
            profit_pct=round(profit_pct, 4),
            arbitrage_detected=profit_pct > 0.15  # Greater than 15 bps after execution fees
        )
