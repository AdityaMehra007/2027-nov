# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Instant UPI Payment Engine: Deep links, QR payload generation, and UTR settlement reconciliation."""

from __future__ import annotations

import urllib.parse
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class UPIPaymentIntent(BaseModel):
    order_id: str
    vpa: str
    payee_name: str
    amount_inr: float
    currency: str = "INR"
    intent_url: str
    qr_payload: str
    qr_svg: Optional[str] = None
    status: str = "PENDING"


class InstantUPIEngine:
    """Manages instant dynamic UPI intent URLs and UTR replay-safe reconciliation."""

    def __init__(self, vpa: str = "agency@icici", payee_name: str = "Omniverse Agency"):
        self.vpa = vpa
        self.payee_name = payee_name
        self._intents: Dict[str, UPIPaymentIntent] = {}
        self._redeemed_utrs: Dict[str, str] = {}  # utr -> order_id

    def generate_upi_intent(
        self,
        order_id: str,
        amount_usd: float,
        exchange_rate: float = 86.0
    ) -> UPIPaymentIntent:
        """Generates dynamic UPI intent URL with encoded parameters."""
        amount_inr = round(amount_usd * exchange_rate, 2)
        encoded_name = urllib.parse.quote(self.payee_name)
        intent_url = f"upi://pay?pa={self.vpa}&pn={encoded_name}&am={amount_inr:.2f}&cu=INR&tn={order_id}"

        intent = UPIPaymentIntent(
            order_id=order_id,
            vpa=self.vpa,
            payee_name=self.payee_name,
            amount_inr=amount_inr,
            currency="INR",
            intent_url=intent_url,
            qr_payload=intent_url,
            qr_svg=f"<svg viewBox='0 0 100 100' data-payload='{intent_url}'></svg>",
            status="PENDING"
        )
        self._intents[order_id] = intent
        return intent

    def confirm_upi_payment(self, order_id: str, utr_number: str) -> Dict[str, Any]:
        """Validates UTR uniqueness and marks order settled with replay protection."""
        if utr_number in self._redeemed_utrs:
            return {
                "settled": False,
                "error": f"UTR number {utr_number} is already redeemed for order {self._redeemed_utrs[utr_number]}"
            }

        self._redeemed_utrs[utr_number] = order_id
        if order_id in self._intents:
            self._intents[order_id].status = "SETTLED"

        return {
            "settled": True,
            "status": "SETTLED",
            "utr": utr_number,
            "order_id": order_id
        }
