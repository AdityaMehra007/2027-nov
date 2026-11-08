import json
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from functools import lru_cache

class OmniverseSettings(BaseSettings):
    app_name: str = "CASHFLOW INFINITY: OMNIVERSE"
    version: str = "1.0.0"
    env: str = Field(default="development", description="development, staging, or production")
    db_url: str = Field(default="sqlite:///./data/omniverse.db", description="Database connection URL")
    allowed_hosts: list[str] | str = Field(
        default=["127.0.0.1", "localhost", "testserver", "*"],
        description="Allowed host headers for TrustedHostMiddleware",
    )

    @field_validator("allowed_hosts", mode="after")
    @classmethod
    def parse_allowed_hosts(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed]
                except Exception:
                    pass
            return [h.strip() for h in v.split(",") if h.strip()]
        return list(v)
    
    # Financial & Safety Governors
    safety_budget_daily_usd: float = Field(default=50.0, description="Max autonomous daily spending ceiling")
    strict_approval_required: bool = Field(default=True, description="Strict human-in-the-loop gate for external money movement")
    primary_market: str = "Bengaluru, India"
    currency: str = "INR"

    # Webhook Gateway Secrets (TM-004)
    stripe_webhook_secret: str = Field(default="whsec_mock", description="Stripe Webhook Signing Secret")
    razorpay_key_secret: str = Field(default="rzp_sec_mock", description="Razorpay Webhook Key Secret")
    rtgs_webhook_secret: str = Field(default="rtgs_sec_mock", description="RTGS Webhook HMAC Secret")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> OmniverseSettings:
    return OmniverseSettings()
