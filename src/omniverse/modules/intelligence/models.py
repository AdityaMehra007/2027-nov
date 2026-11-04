from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import time

class TradeDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class CompanyProfile(BaseModel):
    symbol: str
    name: str
    industry: str
    annual_revenue_cr: float
    net_profit_margin_pct: float
    debt_to_equity: float
    moat_rating: str
    financial_health_score: float

class PaperTrade(SQLModel, table=True):
    __tablename__ = "paper_trades"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    direction: TradeDirection
    quantity: int
    entry_price: float
    exit_price: Optional[float] = None
    status: str = Field(default="OPEN")
    pnl: Optional[float] = None
    created_at: float = Field(default_factory=time.time)
