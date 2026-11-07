"""
Billing and Webhook Engine for PromptShield Guard
"""
import hmac
import hashlib
import time
from typing import Dict, Any

class BillingEngine:
    WEBHOOK_SECRET = "whsec_omni_live_mock_secret"

    @classmethod
    def create_checkout_session(cls, req: Dict[str, Any]) -> Dict[str, Any]:
        session_id = f"cs_live_{int(time.time() * 1000)}"
        return {
            "session_id": session_id,
            "checkout_url": f"https://checkout.stripe.com/pay/{session_id}",
            "amount": req.get("amount", 29.0),
            "currency": req.get("currency", "USD"),
            "status": "READY"
        }

    @classmethod
    def verify_webhook(cls, payload: str, signature: str) -> bool:
        expected = hmac.new(
            cls.WEBHOOK_SECRET.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
