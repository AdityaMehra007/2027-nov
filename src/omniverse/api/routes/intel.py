from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from omniverse.modules.intelligence.research import CompanyIntelligenceEngine
from omniverse.modules.intelligence.quant_engine import Backtester

class CompanyAnalysisRequest(BaseModel):
    symbol: str
    name: str
    industry: str
    annual_revenue_cr: float
    net_profit_margin_pct: float
    debt_to_equity: float

class BacktestRequest(BaseModel):
    prices: List[float]

def get_intel_router():
    router = APIRouter(prefix="/intel", tags=["Intelligence"])

    @router.post("/company")
    def analyze_company(req: CompanyAnalysisRequest):
        engine = CompanyIntelligenceEngine()
        return engine.analyze_company(
            symbol=req.symbol,
            name=req.name,
            industry=req.industry,
            annual_revenue_cr=req.annual_revenue_cr,
            net_profit_margin_pct=req.net_profit_margin_pct,
            debt_to_equity=req.debt_to_equity
        )

    @router.post("/backtest")
    def run_backtest(req: BacktestRequest):
        backtester = Backtester()
        return backtester.run_trend_following_backtest(req.prices)

    return router
