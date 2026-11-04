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
    prices = [100.0, 102.0, 101.5, 105.0, 104.0, 108.0, 112.0, 110.0, 115.0, 120.0]
    result = backtester.run_trend_following_backtest(prices)
    
    assert "total_return_pct" in result
    assert "sharpe_ratio" in result
    assert "max_drawdown_pct" in result
    assert result["total_return_pct"] > 0

def test_backtester_moving_average_crossover():
    backtester = Backtester()
    prices = [100, 102, 104, 106, 108, 110, 112, 115, 118, 122, 125, 130]
    res = backtester.run_moving_average_crossover(prices, fast_period=3, slow_period=6)
    
    assert "total_return_pct" in res
    assert "trades_count" in res
    assert "win_rate_pct" in res

def test_backtester_monte_carlo_var():
    backtester = Backtester()
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 114]
    mc = backtester.run_monte_carlo_var(prices, num_simulations=200, horizon_days=10)
    
    assert "var_95_pct" in mc
    assert "var_99_pct" in mc
    assert "expected_shortfall_cvar_pct" in mc
    assert mc["var_99_pct"] >= mc["var_95_pct"]

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
    
    portfolio = trading_engine.get_portfolio_summary()
    assert portfolio["cash_balance_inr"] == 1000000.0 - (50 * 1800.0)
    assert portfolio["open_positions_count"] == 1
