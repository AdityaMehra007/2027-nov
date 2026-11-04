from typing import List, Dict
from omniverse.modules.markets.models import AssetClass, MarketQuote, MacroEnvironment

class MultiMarketEngine:
    """Multi-asset global market intelligence and macroeconomic regime evaluation."""

    def get_global_overview(self) -> List[MarketQuote]:
        return [
            MarketQuote(symbol="NIFTY50", name="Nifty 50 Index", asset_class=AssetClass.EQUITY, price=24500.0, currency="INR", change_24h_pct=0.65, volatility_30d=12.4),
            MarketQuote(symbol="IN10Y", name="India 10Y Benchmark Sovereign", asset_class=AssetClass.FIXED_INCOME, price=6.82, currency="Yield %", change_24h_pct=-0.04, volatility_30d=4.1),
            MarketQuote(symbol="TREPS", name="Tri-Party Repo Dealing", asset_class=AssetClass.MONEY_MARKET, price=6.45, currency="Rate %", change_24h_pct=0.01, volatility_30d=1.2),
            MarketQuote(symbol="USDINR", name="US Dollar / Indian Rupee", asset_class=AssetClass.FOREX, price=84.10, currency="INR", change_24h_pct=-0.12, volatility_30d=3.8),
            MarketQuote(symbol="BRENT", name="Brent Crude Oil", asset_class=AssetClass.COMMODITY, price=76.50, currency="USD", change_24h_pct=1.45, volatility_30d=24.5),
            MarketQuote(symbol="NIFTY_IV", name="Nifty ATM Implied Volatility", asset_class=AssetClass.DERIVATIVE, price=13.2, currency="IV %", change_24h_pct=-0.35, volatility_30d=15.0),
            MarketQuote(symbol="BTC", name="Bitcoin / USD", asset_class=AssetClass.DIGITAL_ASSET, price=72500.0, currency="USD", change_24h_pct=2.85, volatility_30d=42.0),
        ]

    def assess_macro_environment(
        self,
        inflation_cpi_pct: float,
        repo_rate_pct: float,
        gdp_growth_pct: float
    ) -> MacroEnvironment:
        real_rate = repo_rate_pct - inflation_cpi_pct

        # Regime determination
        if gdp_growth_pct >= 6.5 and inflation_cpi_pct <= 5.0:
            regime = "EXPANSION"
            stance = "NEUTRAL"
            allocation = {"Equities": 0.55, "Fixed Income": 0.25, "Commodities": 0.10, "Cash": 0.10}
        elif gdp_growth_pct < 5.0 and inflation_cpi_pct > 6.0:
            regime = "STAGFLATION"
            stance = "HAWKISH"
            allocation = {"Commodities": 0.35, "Cash": 0.35, "Fixed Income": 0.20, "Equities": 0.10}
        elif gdp_growth_pct < 4.0:
            regime = "RECESSION"
            stance = "ACCOMMODATIVE"
            allocation = {"Fixed Income": 0.50, "Cash": 0.30, "Equities": 0.20}
        else:
            regime = "SLOWDOWN"
            stance = "NEUTRAL"
            allocation = {"Fixed Income": 0.40, "Equities": 0.40, "Cash": 0.20}

        return MacroEnvironment(
            regime=regime,
            monetary_stance=stance,
            inflation_cpi_pct=inflation_cpi_pct,
            repo_rate_pct=repo_rate_pct,
            gdp_growth_pct=gdp_growth_pct,
            strategic_asset_allocation=allocation
        )
