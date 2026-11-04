from typing import List, Dict, Any, Optional
import math
from sqlmodel import Session, select
from omniverse.modules.intelligence.models import PaperTrade, TradeDirection

class Backtester:
    """Quantitative backtesting engine with risk-adjusted return and drawdown metrics."""

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
        
        # Annualized Sharpe ratio approximation
        sharpe_ratio = round((mean_return / std_dev) * math.sqrt(252), 2)

        # Max Drawdown calculation
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
