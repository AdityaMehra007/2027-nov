from pathlib import Path
import urllib.parse
from omniverse.modules.revenue.models import GrowthKit

class GrowthKitExporter:
    """Exports structured Growth Kits into client proposals, social calendars,

    and one-click WhatsApp direct response links.
    """

    def generate_whatsapp_click_url(self, phone_number: str, message_text: str) -> str:
        clean_phone = "".join(c for c in phone_number if c.isdigit())
        encoded_text = urllib.parse.quote(message_text)
        return f"https://wa.me/{clean_phone}?text={encoded_text}"

    def generate_client_proposal_deck(self, kit: GrowthKit, pricing_inr: float = 25000.0) -> str:
        captions_md = "\n".join([f"### Day {i+1} Campaign\n> {cap}\n" for i, cap in enumerate(kit.social_captions)])
        hooks_md = "\n".join([f"- **Hook {i+1}**: {hook}" for i, hook in enumerate(kit.promotional_hooks)])

        doc = f"""# COMMERCIAL PROPOSAL & GROWTH PLAYBOOK
**Client:** {kit.business_name}  
**Sector:** {kit.niche} ({kit.city})  
**Prepared by:** CASHFLOW INFINITY Micro-Agency  
**Investment:** ₹{pricing_inr:,.2f} / month  

---

## 🎯 Executive Summary
We have analyzed the customer acquisition funnel for {kit.business_name} in {kit.city}. This playbook delivers 10 localized social conversion campaigns, direct-response conversational commerce for WhatsApp, and high-engagement customer acquisition hooks.

---

## 📱 1. WhatsApp Conversational Storefront Copy
```text
{kit.whatsapp_catalog_copy}
```

---

## 🚀 2. High-Converting Promotional Hooks
{hooks_md}

---

## 📅 3. 10-Day Omnichannel Social Media Campaign
{captions_md}

---

## 🤝 4. Commercial Terms & Onboarding
- **Turnaround Time**: Same-day asset deployment.
- **Support**: Dedicated account management and weekly analytics review.
- **Guarantee**: Verified quality and bespoke adjustments within 48 hours.
"""
        return doc

    def export_markdown(self, kit: GrowthKit, output_path: Path, pricing_inr: float = 25000.0) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_client_proposal_deck(kit, pricing_inr)
        output_path.write_text(content, encoding="utf-8")
        return output_path
