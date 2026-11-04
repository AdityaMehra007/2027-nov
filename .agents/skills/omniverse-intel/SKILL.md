---
name: omniverse-intel
description: Financial intelligence, fundamental company research, quantitative backtesting, and paper trading risk management for CASHFLOW INFINITY.
---

# CASHFLOW INFINITY: Intelligence & Quantitative Lab

Use this skill to research corporate fundamentals, run quantitative strategy backtests, and simulate risk-controlled paper trading.

## When to Use
- User asks for "company research", "analyze balance sheet", "run backtest", or "check paper trading".

## Capabilities

### 1. Fundamental Company Analysis
Evaluates balance sheet solvency, profit margins, and economic moat rating (`WIDE`, `NARROW`, `NONE`).

### 2. Quantitative Backtesting
Calculates:
- Cumulative return %
- Annualized Sharpe Ratio
- Maximum Peak-to-Trough Drawdown %

### 3. Institutional Risk Guardrails
- Maximum drawdown threshold: 20%. Any strategy exceeding 20% max drawdown is automatically rejected by the `QuantAnalyst` risk engine.
- Zero live real-money execution without explicit human verification and regulatory compliance (SEBI/NSE/broker API framework).
