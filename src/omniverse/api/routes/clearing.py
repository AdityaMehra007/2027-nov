"""==============================================================================
GLOBAL FINANCIAL CLEARING & MULTI-CURRENCY SETTLEMENT API
==============================================================================
Sub-millisecond multi-currency atomic gross settlement, FX hedging, and
liquidity reserve monitoring for OmniSwarm Treasury.
==============================================================================
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from omniverse.modules.settlement.clearing import (
    GlobalClearingHouse,
    CurrencyCode,
    SettlementTransaction
)

_clearing_house = GlobalClearingHouse()


class SettlementQuoteRequest(BaseModel):
    source_currency: CurrencyCode
    target_currency: CurrencyCode
    source_amount: float = Field(..., gt=0.0)


class SettlementExecuteRequest(BaseModel):
    sender_id: str
    recipient_id: str
    source_currency: CurrencyCode
    target_currency: CurrencyCode
    source_amount: float = Field(..., gt=0.0)


def get_clearing_router():
    router = APIRouter(prefix="/clearing", tags=["Treasury & Clearing"])

    @router.get("/reserves")
    def get_reserves() -> Dict[str, Any]:
        """Returns live multi-currency liquidity reserves held by the clearing house."""
        reserves = _clearing_house.get_liquidity_reserves()
        return {
            "status": "OPERATIONAL",
            "reserves": {k.value: round(v, 2) for k, v in reserves.items()}
        }

    @router.get("/rates")
    def get_fx_rates() -> Dict[str, Any]:
        """Returns base INR exchange rates and supported currency corridors."""
        return {
            "base_currency": "INR",
            "rates": {k.value: v for k, v in _clearing_house._FX_BASE_RATES_INR.items()},
            "supported_currencies": [c.value for c in CurrencyCode]
        }

    @router.post("/quote")
    def get_settlement_quote(req: SettlementQuoteRequest) -> Dict[str, Any]:
        """Calculates effective exchange rate and target settlement amount."""
        rate_src = _clearing_house._FX_BASE_RATES_INR.get(req.source_currency, 1.0)
        rate_tgt = _clearing_house._FX_BASE_RATES_INR.get(req.target_currency, 1.0)
        effective_rate = rate_src / rate_tgt
        target_amount = round(req.source_amount * effective_rate, 2)

        return {
            "source_currency": req.source_currency.value,
            "target_currency": req.target_currency.value,
            "source_amount": req.source_amount,
            "target_amount": target_amount,
            "effective_rate": round(effective_rate, 6),
            "fee_rate_bps": 15,  # 0.15% Omniverse clearing fee
            "fee_amount": round(target_amount * 0.0015, 2)
        }

    @router.post("/settle", response_model=SettlementTransaction)
    def execute_settlement(req: SettlementExecuteRequest):
        """Executes atomic cross-currency RTGS settlement."""
        try:
            return _clearing_house.execute_atomic_settlement(
                sender_id=req.sender_id,
                recipient_id=req.recipient_id,
                source_currency=req.source_currency,
                target_currency=req.target_currency,
                source_amount=req.source_amount
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Settlement failed: {str(e)}")

    return router
