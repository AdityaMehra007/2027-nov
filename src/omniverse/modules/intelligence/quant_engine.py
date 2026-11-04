from typing import List, Dict, Any, Optional
import math
import random
from sqlmodel import Session, select
from omniverse.modules.intelligence.models import PaperTrade, TradeDirection

class Backtester:
    """Quantitative backtesting engine with multi-strategy support,

    risk-adjusted return metrics, and Monte Carlo Value-at-Risk (VaR) modeling.
    """

    def run_trend_following_backtest(self, prices: List[float]) -> Dict[str, Any]:
        if len(prices) < 2:
            return {"error": "Need at least 2 price points"}

        returns = []
        for i in range(1, len(prices)):
            r = (prices[i] - prices[i - 1]) / prices[i - 1]
            returns.append(r)

        total_return = (prices[-1] - prices[0]) / prices[0]
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance) if variance > 0 else 0.0001
        
        sharpe_ratio = round((mean_return / std_dev) * math.sqrt(252), 2)

        peak = prices[0]
        max_dd = 0.0
        for p in prices:
            if p > peak:
                peak = p
            dd = (peak - p) / peak
            if dd > max_dd:
                max_dd = dd

        return {
            "total_return_pct": round(total_return * 100, 2),
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown_pct": round(max_dd * 100, 2),
            "data_points": len(prices)
        }

    def run_moving_average_crossover(
        self,
        prices: List[float],
        fast_period: int = 3,
        slow_period: int = 6
    ) -> Dict[str, Any]:
        """Dual moving average crossover strategy (e.g., SMA fast vs SMA slow)."""
        if len(prices) < slow_period + 1:
            return {"error": f"Need at least {slow_period + 1} price points"}

        def compute_sma(sub: List[float]) -> float:
            return sum(sub) / len(sub)

        trades = []
        in_position = False
        entry_price = 0.0

        for i in range(slow_period, len(prices)):
            fast_sma = compute_sma(prices[i - fast_period:i])
            slow_sma = compute_sma(prices[i - slow_period:i])

            if fast_sma > slow_sma and not in_position:
                in_position = True
                entry_price = prices[i]
            elif fast_sma < slow_sma and in_position:
                in_position = False
                pnl = (prices[i] - entry_price) / entry_price
                trades.append(pnl)

        # Close position at the end if open
        if in_position:
            pnl = (prices[-1] - entry_price) / entry_price
            trades.append(pnl)

        total_pnl = sum(trades) if trades else 0.0
        wins = sum(1 for t in trades if t > 0)
        win_rate = (wins / len(trades) * 100.0) if trades else 0.0

        return {
            "strategy": f"SMA_{fast_period}_{slow_period}",
            "total_return_pct": round(total_pnl * 100.0, 2),
            "trades_count": len(trades),
            "win_rate_pct": round(win_rate, 2),
            "profitable_trades": wins
        }

    def run_monte_carlo_var(
        self,
        prices: List[float],
        num_simulations: int = 200,
        horizon_days: int = 10
    ) -> Dict[str, Any]:
        """Monte Carlo simulation estimating Value at Risk (VaR 95%, 99%) and Conditional VaR."""
        if len(prices) < 2:
            return {"error": "Need at least 2 price points"}

        log_returns = []
        for i in range(1, len(prices)):
            log_returns.append(math.log(prices[i] / prices[i - 1]))

        mu = sum(log_returns) / len(log_returns)
        var_r = sum((r - mu) ** 2 for r in log_returns) / len(log_returns)
        sigma = math.sqrt(var_r) if var_r > 0 else 0.01

        simulated_returns = []
        random.seed(42)  # Deterministic seed for reproducible tests

        for _ in range(num_simulations):
            cumulative_return = 0.0
            for _ in range(horizon_days):
                # Box-Muller normal approximation
                u1 = max(0.0001, random.random())
                u2 = max(0.0001, random.random())
                z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
                daily_r = mu + sigma * z
                cumulative_return += daily_r
            simulated_returns.append(cumulative_return)

        simulated_returns.sort()

        # VaR 95% is the 5th percentile loss
        idx_95 = int(num_simulations * 0.05)
        idx_99 = int(num_simulations * 0.01)

        loss_95 = -simulated_returns[idx_95]
        loss_99 = -simulated_returns[idx_99]

        # Conditional VaR (Expected Shortfall) is average of losses exceeding VaR 95
        worst_5_pct = [-r for r in simulated_returns[:idx_95]]
        cvar = sum(worst_5_pct) / len(worst_5_pct) if worst_5_pct else loss_95

        return {
            "num_simulations": num_simulations,
            "horizon_days": horizon_days,
            "var_95_pct": round(max(0.0, loss_95 * 100.0), 2),
            "var_99_pct": round(max(0.0, loss_99 * 100.0), 2),
            "expected_shortfall_cvar_pct": round(max(0.0, cvar * 100.0), 2)
        }

class PaperTradingEngine:
    """Safe, zero-real-capital simulated execution engine."""

    def __init__(self, session: Session, initial_capital_inr: float = 1000000.0):
        self.session = session
        self.capital = initial_capital_inr

    def execute_order(
        self,
        symbol: str,
        direction: TradeDirection,
        quantity: int,
        price: float
    ) -> PaperTrade:
        total_cost = quantity * price
        if direction == TradeDirection.BUY and total_cost > self.capital:
            raise ValueError("Insufficient simulated cash balance")

        trade = PaperTrade(
            symbol=symbol,
            direction=direction,
            quantity=quantity,
            entry_price=price,
            status="OPEN"
        )
        self.session.add(trade)
        self.session.commit()
        self.session.refresh(trade)
        return trade

    def get_portfolio_summary(self) -> Dict[str, Any]:
        trades = list(self.session.exec(select(PaperTrade).where(PaperTrade.status == "OPEN")).all())
        spent = sum(t.quantity * t.entry_price for t in trades if t.direction == TradeDirection.BUY)
        cash_balance = self.capital - spent

        return {
            "initial_capital_inr": self.capital,
            "cash_balance_inr": cash_balance,
            "open_positions_count": len(trades),
            "positions": [
                {
                    "symbol": t.symbol,
                    "direction": t.direction.value,
                    "quantity": t.quantity,
                    "entry_price": t.entry_price
                }
                for t in trades
            ]
        }
