"""Commercial Deal Closer Agent: Assembles executive proposals, demo links, and instant checkout URLs."""

from __future__ import annotations

import urllib.parse
from typing import Dict, Any
from omniverse.agents.base import BaseAgent, AgentTask
from omniverse.core.telemetry import global_event_bus


class CommercialDealCloserAgent(BaseAgent):
    """Autonomous commercial closer that converts pipeline opportunities into confirmed deals."""

    @property
    def role_name(self) -> str:
        return "CommercialCloser"

    @property
    def division(self) -> str:
        return "Commercial"

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        payload = task.payload
        client_name = payload.get("client_name", "Target Client")
        client_hub = payload.get("hub", "GLOBAL")
        price_usd = float(payload.get("price_usd", 15000.0))
        demo_url = payload.get("demo_url", f"https://demo.omniverse.io/client/{urllib.parse.quote(client_name)}")

        # Construct One-Click Checkout URL
        checkout_url = f"https://checkout.stripe.com/pay/cs_live_{urllib.parse.quote(client_name.lower().replace(' ', '_'))}?amount={int(price_usd*100)}&currency=usd"
        whatsapp_msg = urllib.parse.quote(
            f"Hello {client_name} Team! We have autonomously engineered your fullstack solution and AI concierge. "
            f"Review live demo here: {demo_url}. Ready to deploy immediately."
        )
        whatsapp_link = f"https://wa.me/14155552671?text={whatsapp_msg}"

        proposal = {
            "client_name": client_name,
            "hub": client_hub,
            "quoted_contract_usd": price_usd,
            "demo_preview_url": demo_url,
            "checkout_payment_url": checkout_url,
            "whatsapp_direct_outreach": whatsapp_link,
            "closing_pitch": (
                f"We have solved your primary operational bottlenecks by manufacturing a custom "
                f"full-stack platform and autonomous AI agent. Estimated 12-month ROI: 450%."
            ),
        }

        global_event_bus.publish("COMMERCIAL_PROPOSAL_DISPATCHED", {
            "client": client_name,
            "quoted_usd": price_usd,
        })

        return {
            "status": "SUCCESS",
            "proposal": proposal,
        }
