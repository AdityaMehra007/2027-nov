import pytest
from omniverse.modules.markets.models import AssetClass, MarketQuote, MacroEnvironment
from omniverse.modules.markets.engine import MultiMarketEngine

def test_multi_market_feed_aggregation():
    engine = MultiMarketEngine()
    quotes = engine.get_global_overview()
    
    assert len(quotes) >= 7 # All 7 market categories
    asset_classes = {q.asset_class for q in quotes}
    assert AssetClass.EQUITY in asset_classes
    assert AssetClass.FIXED_INCOME in asset_classes
    assert AssetClass.COMMODITY in asset_classes
    assert AssetClass.FOREX in asset_classes
    assert AssetClass.DIGITAL_ASSET in asset_classes

def test_macro_environment_assessment():
    engine = MultiMarketEngine()
    macro = engine.assess_macro_environment(
        inflation_cpi_pct=4.8,
        repo_rate_pct=6.5,
        gdp_growth_pct=7.2
    )
    
    assert isinstance(macro, MacroEnvironment)
    assert macro.regime in ("EXPANSION", "SLOWDOWN", "STAGFLATION", "RECESSION")
    assert macro.monetary_stance in ("HAWKISH", "NEUTRAL", "ACCOMMODATIVE")
    assert len(macro.strategic_asset_allocation) > 0
