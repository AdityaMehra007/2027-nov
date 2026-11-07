"""==============================================================================
QUANTITATIVE FINANCE, DERIVATIVES & MACRO INTELLIGENCE API
==============================================================================
Exposes Black-Scholes Greeks valuation, triangular currency arbitrage scanning,
and multi-asset macroeconomic regime analytics.
==============================================================================
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from omniverse.modules.intelligence.derivatives import (
    DerivativesEngine,
    OptionGreeks,
    TriangularArbitrageOpportunity
)
from omniverse.modules.markets.engine import MultiMarketEngine
from omniverse.modules.markets.models import MarketQuote, MacroEnvironment

_derivatives_engine = DerivativesEngine()
_market_engine = MultiMarketEngine()


class OptionGreeksRequest(BaseModel):
    spot: float = Field(..., gt=0.0, description="Current underlying asset price")
    strike: float = Field(..., gt=0.0, description="Option strike price")
    time_to_maturity_years: float = Field(..., gt=0.0, description="Time to expiry in years")
    risk_free_rate: float = Field(default=0.065, description="Annualized risk-free interest rate (e.g. 0.065 for 6.5%)")
    volatility: float = Field(default=0.15, gt=0.0, description="Annualized implied volatility (e.g. 0.15 for 15%)")


class ArbitrageScanRequest(BaseModel):
    initial_capital: float = Field(default=100000.0, gt=0.0)
    rates: Optional[Dict[str, float]] = None


class MacroAssessRequest(BaseModel):
    inflation_cpi_pct: float = Field(default=4.8, description="Annual CPI inflation %")
    repo_rate_pct: float = Field(default=6.5, description="Central bank policy repo rate %")
    gdp_growth_pct: float = Field(default=7.2, description="Annualized real GDP growth rate %")


def get_finance_router():
    router = APIRouter(prefix="/finance", tags=["Quantitative Finance"])

    @router.post("/greeks", response_model=OptionGreeks)
    def calculate_greeks(req: OptionGreeksRequest):
        """Computes analytic Black-Scholes option pricing and Greeks."""
        return _derivatives_engine.calculate_black_scholes_greeks(
            spot=req.spot,
            strike=req.strike,
            time_to_maturity_years=req.time_to_maturity_years,
            risk_free_rate=req.risk_free_rate,
            volatility=req.volatility
        )

    @router.post("/arbitrage", response_model=TriangularArbitrageOpportunity)
    def detect_arbitrage(req: ArbitrageScanRequest):
        """Scans triangular FX cross-rates for spatial arbitrage opportunities."""
        rates = req.rates or {}
        return _derivatives_engine.detect_triangular_arbitrage(
            rates=rates,
            initial_capital=req.initial_capital
        )

    @router.get("/quotes", response_model=List[MarketQuote])
    def get_market_quotes():
        """Returns live multi-asset benchmark quotes across equity, fixed income, and FX."""
        return _market_engine.get_global_overview()

    @router.post("/macro", response_model=MacroEnvironment)
    def assess_macro_regime(req: MacroAssessRequest):
        """Classifies macroeconomic regime and computes strategic asset allocation."""
        return _market_engine.assess_macro_environment(
            inflation_cpi_pct=req.inflation_cpi_pct,
            repo_rate_pct=req.repo_rate_pct,
            gdp_growth_pct=req.gdp_growth_pct
        )

    return router
