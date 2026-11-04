from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class OmniverseSettings(BaseSettings):
    app_name: str = "CASHFLOW INFINITY: OMNIVERSE"
    version: str = "1.0.0"
    env: str = Field(default="development", description="development, staging, or production")
    db_url: str = Field(default="sqlite:///./data/omniverse.db", description="Database connection URL")
    allowed_hosts: list[str] = Field(
        default=["127.0.0.1", "localhost", "testserver", "*"],
        description="Allowed host headers for TrustedHostMiddleware",
    )
    
    # Financial & Safety Governors
    safety_budget_daily_usd: float = Field(default=50.0, description="Max autonomous daily spending ceiling")
    strict_approval_required: bool = Field(default=True, description="Strict human-in-the-loop gate for external money movement")
    primary_market: str = "Bengaluru, India"
    currency: str = "INR"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> OmniverseSettings:
    return OmniverseSettings()
