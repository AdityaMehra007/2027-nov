#!/usr/bin/env python3
"""Example 02: Quantitative Intelligence & Monte Carlo Value-at-Risk Simulation.

Demonstrates vectorized strategy backtesting, technical indicators (RSI, MACD, Bollinger),
and institutional Monte Carlo Value-at-Risk (VaR) forecasting.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.modules.intelligence.quant_engine import Backtester
from omniverse.modules.intelligence.indicators import (
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_atr
)

def main():
    print("================================================================")
    print("  02. QUANTITATIVE LAB: MONTE CARLO VaR & INDICATORS")
    print("================================================================")

    # 15-day institutional asset trajectory (e.g. NIFTY50 index close)
    prices = [23800.0, 23950.0, 23890.0, 24100.0, 24250.0, 24180.0, 24350.0, 
              24480.0, 24420.0, 24600.0, 24750.0, 24900.0, 24820.0, 25050.0, 25200.0]

    # 1. Technical Indicators
    print("\n📈 Step 1: Evaluating Technical Indicators...")
    rsi = calculate_rsi(prices)
    macd = calculate_macd(prices)
    bb = calculate_bollinger_bands(prices)
    atr = calculate_atr(highs=[p * 1.01 for p in prices], lows=[p * 0.99 for p in prices], closes=prices)

    print(f" • Latest Price        : ₹{prices[-1]:,.2f}")
    print(f" • Relative Strength   : RSI(14) = {rsi:.2f}")
    print(f" • MACD Oscillator     : Line = {macd['macd_line']:.2f} | Signal = {macd['signal_line']:.2f} | Hist = {macd['histogram']:.2f}")
    print(f" • Bollinger Envelopes : Upper = ₹{bb['upper_band']:,.2f} | Lower = ₹{bb['lower_band']:,.2f}")
    print(f" • Average True Range  : ATR(14) = ₹{atr:.2f}")

    # 2. Backtesting
    print("\n🔄 Step 2: Running Moving Average Crossover Backtest...")
    backtester = Backtester()
    sma_res = backtester.run_moving_average_crossover(prices, fast_period=2, slow_period=5)
    print(f" • Total Return        : {sma_res['total_return_pct']}%")
    print(f" • Win Rate            : {sma_res['win_rate_pct']}% across {sma_res['trades_count']} trades")

    # 3. Monte Carlo Simulation
    print("\n🎲 Step 3: Running 1,000-Path Monte Carlo Value-at-Risk Simulation...")
    var_res = backtester.run_monte_carlo_var(prices, num_simulations=1000, horizon_days=30)
    print(f" • Value-at-Risk (95%) : {var_res['var_95_pct']}%")
    print(f" • Value-at-Risk (99%) : {var_res['var_99_pct']}%")
    print(f" • Expected Shortfall  : {var_res['expected_shortfall_cvar_pct']}% (CVaR)")
    print(f" • Simulations Run     : {var_res['num_simulations']} trajectories over {var_res['horizon_days']} days")
    print("================================================================")

if __name__ == "__main__":
    main()
