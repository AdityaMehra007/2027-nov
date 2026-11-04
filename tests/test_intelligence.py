import pytest
from sqlmodel import Session
from omniverse.modules.intelligence.models import CompanyProfile, PaperTrade, TradeDirection
from omniverse.modules.intelligence.research import CompanyIntelligenceEngine
from omniverse.modules.intelligence.quant_engine import Backtester, PaperTradingEngine

def test_company_research_analysis():
    engine = CompanyIntelligenceEngine()
    profile = engine.analyze_company(
        symbol="TCS",
        name="Tata Consultancy Services",
        industry="Information Technology",
        annual_revenue_cr=240000.0,
        net_profit_margin_pct=19.5,
        debt_to_equity=0.05
    )
    
    assert profile.symbol == "TCS"
    assert profile.moat_rating in ("WIDE", "NARROW", "NONE")
    assert profile.financial_health_score > 70.0

def test_backtester_metrics():
    backtester = Backtester()
    # Simple simulated price series with steady upward trend
    prices = [100.0, 102.0, 101.5, 105.0, 104.0, 108.0, 112.0, 110.0, 115.0, 120.0]
    result = backtester.run_trend_following_backtest(prices)
    
    assert "total_return_pct" in result
    assert "sharpe_ratio" in result
    assert "max_drawdown_pct" in result
    assert result["total_return_pct"] > 0

def test_paper_trading_execution(test_db: Session):
    trading_engine = PaperTradingEngine(session=test_db, initial_capital_inr=1000000.0)
    trade = trading_engine.execute_order(
        symbol="INFY",
        direction=TradeDirection.BUY,
        quantity=50,
        price=1800.0
    )
    
    assert trade.id is not None
    assert trade.symbol == "INFY"
    assert trade.status == "OPEN"
    
    # Portfolio summary
    portfolio = trading_engine.get_portfolio_summary()
    assert portfolio["cash_balance_inr"] == 1000000.0 - (50 * 1800.0)
    assert portfolio["open_positions_count"] == 1
