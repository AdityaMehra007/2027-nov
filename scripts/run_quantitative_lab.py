"""==============================================================================
QUANTITATIVE MULTI-ASSET RISK & ARBITRAGE LAB
==============================================================================
Simulates Monte Carlo Value-at-Risk across major assets:
- NIFTY50
- SPY
- BTC
- ETH
Calculates Sharpe ratio, maximum drawdown, and Black-Scholes Greeks.
==============================================================================
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from omniverse.modules.intelligence.quant_engine import Backtester
from omniverse.modules.intelligence.indicators import (
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
)
from omniverse.modules.intelligence.derivatives import DerivativesEngine

def run_quant_lab():
    print("=" * 70)
    print("  🚀 CASHFLOW INFINITY: QUANTITATIVE RISK & ARBITRAGE LAB")
    print("=" * 70)

    report_dir = Path("reports/quant")
    report_dir.mkdir(parents=True, exist_ok=True)

    backtester = Backtester()
    derivatives = DerivativesEngine()

    assets = ["NIFTY50", "SPY", "BTC", "ETH"]
    portfolio_results = {}

    for sym in assets:
        print(f"\n[ASSET AUDIT] >>> {sym}")
        vol_mult = 3.0 if "BTC" in sym or "ETH" in sym else 1.0
        prices = [100.0 + (i * 0.8) + ((-1)**i * 1.5 * vol_mult) for i in range(100)]

        # Trend & Drawdown
        trend = backtester.run_trend_following_backtest(prices)

        # Monte Carlo VaR
        mc = backtester.run_monte_carlo_var(
            prices=prices,
            num_simulations=1000,
            horizon_days=10
        )

        # Calculate Indicators
        rsi = calculate_rsi(prices, period=14)
        macd = calculate_macd(prices)
        bb = calculate_bollinger_bands(prices)

        print(f"  • Total Return: {trend['total_return_pct']}% | Sharpe: {trend['sharpe_ratio']}")
        print(f"  • VaR (95%): {mc['var_95_pct']}% | VaR (99%): {mc['var_99_pct']}%")
        print(f"  • Max Drawdown: {trend['max_drawdown_pct']}% (Limit: <20.0%)")
        print(f"  • RSI (14): {rsi:.2f} | MACD: {macd['macd_line']:.2f}")

        portfolio_results[sym] = {
            "trend": trend,
            "monte_carlo": mc,
            "rsi_14": rsi,
            "macd": macd,
            "bollinger": bb
        }

    # Derivatives pricing (Call Option & Greeks)
    greeks = derivatives.calculate_black_scholes_greeks(
        spot=100.0,
        strike=105.0,
        time_to_maturity_years=0.25,
        risk_free_rate=0.05,
        volatility=0.25
    )
    print("\n[DERIVATIVES DESK] >>> Black-Scholes Call Valuation")
    print(f"  • Spot: $100.00 | Strike: $105.00 | Maturity: 3 months")
    print(f"  • Call Price: ${greeks.call_price:.2f} | Put Price: ${greeks.put_price:.2f}")
    print(f"  • Delta: {greeks.delta_call:.4f} | Gamma: {greeks.gamma:.4f} | Vega: {greeks.vega:.4f}")

    portfolio_results["derivatives_pricing"] = greeks.model_dump()

    # Write report
    json_path = report_dir / "portfolio_risk_report.json"
    json_path.write_text(json.dumps(portfolio_results, indent=2), encoding="utf-8")

    md_path = report_dir / "portfolio_risk_report.md"
    md_content = f"""# Autonomous Quantitative Risk & Portfolio Report
**Date**: November 2026 / 2027 Edition  
**Framework**: Cashflow Infinity Risk Engine  
**Simulation Mode**: 1,000-Simulation Monte Carlo  

## Asset Risk Matrices

| Symbol | Total Return | Sharpe Ratio | 95% VaR | 99% VaR | Max Drawdown | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for sym in assets:
        t = portfolio_results[sym]["trend"]
        mc_data = portfolio_results[sym]["monte_carlo"]
        status = "PASSED (<20%)" if t['max_drawdown_pct'] < 20.0 else "EXCEEDED"
        md_content += f"| **{sym}** | {t['total_return_pct']}% | {t['sharpe_ratio']} | {mc_data['var_95_pct']}% | {mc_data['var_99_pct']}% | {t['max_drawdown_pct']}% | {status} |\n"

    md_content += f"""
## Derivatives & Greeks Pricing (European Options)
- **Call Price**: ${greeks.call_price:.2f}
- **Put Price**: ${greeks.put_price:.2f}
- **Delta (Call)**: {greeks.delta_call:.4f}
- **Gamma**: {greeks.gamma:.4f}
- **Vega**: {greeks.vega:.4f}
- **Theta (Call)**: {greeks.theta_call:.4f}
- **Rho (Call)**: {greeks.rho_call:.4f}
"""
    md_path.write_text(md_content, encoding="utf-8")

    print("\n" + "=" * 70)
    print(f"✅ Quantitative reports generated:")
    print(f"   • {json_path}")
    print(f"   • {md_path}")
    print("=" * 70)

if __name__ == "__main__":
    run_quant_lab()
