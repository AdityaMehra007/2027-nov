from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import time

class AssetClass(str, Enum):
    EQUITY = "EQUITY"
    FIXED_INCOME = "FIXED_INCOME"
    MONEY_MARKET = "MONEY_MARKET"
    FOREX = "FOREX"
    COMMODITY = "COMMODITY"
    DERIVATIVE = "DERIVATIVE"
    DIGITAL_ASSET = "DIGITAL_ASSET"

class MarketQuote(BaseModel):
    symbol: str
    name: str
    asset_class: AssetClass
    price: float
    currency: str
    change_24h_pct: float
    volatility_30d: float

class MacroEnvironment(BaseModel):
    regime: str
    monetary_stance: str
    inflation_cpi_pct: float
    repo_rate_pct: float
    gdp_growth_pct: float
    strategic_asset_allocation: Dict[str, float]
    updated_at: float = Field(default_factory=time.time)
