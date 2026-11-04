import urllib.parse
from typing import List, Dict, Any
from sqlmodel import Session, select
from omniverse.modules.bangalore.models import (
    SMBGrowthClient,
    BangaloreCluster,
    SMBTier,
)
from omniverse.core.telemetry import global_event_bus

class NammaBizEngine:
    """Bangalore Autonomous SMB 24/7 Growth & WhatsApp Conversion Engine.

    Empowers local cafes, boutique gyms, salons, dental clinics, and luxury PGs
    across Koramangala, Indiranagar, HSR, and Whitefield with 24/7 AI lead capture,
    retaining high-value tech workers.
    """

    CLUSTER_PRESETS = {
        BangaloreCluster.KORAMANGALA: [
            ("Specialty Coffee Lab", "4th Block, 80ft Road", "Store Director", 3999.0),
            ("Boutique Fitness & Pilates", "5th Block, near Jyoti Nivas", "Head Coach", 7999.0),
            ("Artisan Craft Microbrewery", "Koramangala 6th Block", "Operations GM", 14999.0),
        ],
        BangaloreCluster.INDIRANAGAR: [
            ("Contemporary Dermatology Studio", "100ft Road, Defence Colony", "Clinic Lead", 14999.0),
            ("Specialty Sourdough Bakery", "12th Main Road", "Founder Chef", 3999.0),
            ("High-End Co-working & Event Loft", "CMH Road", "Community Manager", 7999.0),
        ],
        BangaloreCluster.HSR_LAYOUT: [
            ("Strength & CrossFit Box", "27th Main, Sector 1", "Founder Coach", 7999.0),
            ("Executive Coliving & Luxury PG", "Sector 3, near HSR Club", "Property Head", 14999.0),
            ("Gourmet Healthy Meal Subscriptions", "19th Main, Sector 4", "Kitchen Partner", 3999.0),
        ],
        BangaloreCluster.WHITEFIELD: [
            ("Tech Executive Wellness Spa", "ITPB Main Road", "Spa Director", 7999.0),
            ("Advanced Orthodontic Lounge", "Hope Farm Junction", "Chief Dentist", 14999.0),
            ("Third Wave Roastery Cafe", "ECC Road, Whitefield", "Cafe Manager", 3999.0),
        ]
    }

    def __init__(self, session: Session):
        self.session = session

    def scan_and_seed_cluster(
        self,
        cluster: BangaloreCluster = BangaloreCluster.HSR_LAYOUT
    ) -> List[SMBGrowthClient]:
        """Discovers and logs SMB prospects for a given Bangalore cluster."""
        presets = self.CLUSTER_PRESETS.get(cluster, self.CLUSTER_PRESETS[BangaloreCluster.HSR_LAYOUT])
        created_clients = []

        for idx, (niche, landmark, contact_title, fee) in enumerate(presets):
            biz_name = f"{cluster.value} {niche}"
            phone = f"+91-98860{idx:05d}"
            tier = SMBTier.PRO if fee >= 14000 else (SMBTier.GROWTH if fee >= 7000 else SMBTier.STARTER)

            # Check if existing
            existing = self.session.exec(
                select(SMBGrowthClient).where(SMBGrowthClient.business_name == biz_name)
            ).first()

            if not existing:
                client = SMBGrowthClient(
                    business_name=biz_name,
                    niche=niche,
                    cluster=cluster,
                    landmark=landmark,
                    contact_person=f"{contact_title} ({landmark})",
                    contact_phone=phone,
                    tier=tier,
                    monthly_fee_inr=fee,
                    status="PROSPECT"
                )
                client.pitch_url = self.generate_whatsapp_pitch_link(client)
                self.session.add(client)
                self.session.commit()
                self.session.refresh(client)
                created_clients.append(client)
            else:
                created_clients.append(existing)

        global_event_bus.publish("BANGALORE_SMB_SCANNED", {
            "cluster": cluster.value,
            "prospects_count": len(created_clients)
        })

        return created_clients

    def generate_growth_kit(self, client: SMBGrowthClient) -> Dict[str, Any]:
        """Creates a complete Bangalore-tailored Growth Kit for the SMB."""
        niche = client.niche
        name = client.business_name
        cluster = client.cluster.value

        social_hooks = [
            f"Stuck at Silk Board or Outer Ring Road? Treat yourself to {name} right here in {cluster}.",
            f"Why Bengaluru techies at Google, Zepto & Swiggy swear by {name} after standup.",
            f"Skip the standard weekend queues: Here is how {name} brings top-tier {niche} to {cluster}.",
            f"Tired of generic service in {cluster}? Experience bespoke {niche} at {name}.",
            f"The best kept secret in {cluster}: Behind the scenes at {name}.",
            f"From late-night coding to weekend wellness: Why {name} is your new favorite spot.",
            f"3 reasons {cluster} locals are choosing {name} over big franchises.",
            f"Your post-sprint reward awaits at {name} ({client.landmark}).",
            f"Tag your Bangalore flatmate who desperately needs this! #BengaluruLife #{cluster}",
            f"Exclusive WhatsApp VIP perk: Get 15% off your first visit to {name}."
        ]

        whatsapp_ai_script = (
            f"🤖 *NAMMA 24/7 AI SALES CONCIERGE SCRIPT FOR {name.upper()}*\n\n"
            f"Trigger: Customer messages after 8 PM or during peak hours.\n"
            f"Response Time: < 3 seconds (Automated 24/7)\n\n"
            f"Prompt: 'Namaskara! 🙏 Welcome to {name} in {cluster}. "
            f"I am your 24/7 assistant. How can I delight you today?'\n"
            f"Options: [1] Book Appointment / Table  [2] View Menu & Pricing  [3] Talk to Manager\n"
            f"Conversion: Automatically captures customer phone, reserves slot, and confirms via WhatsApp."
        )

        review_booster = (
            f"🌟 *5-STAR GOOGLE MAPS REVIEW BOOSTER STRATEGY*\n"
            f"Step 1: Automated WhatsApp trigger 45 minutes after service.\n"
            f"Step 2: 'Loved your time at {name}? Tap here to drop a review and claim a complimentary iced brew / upgrade!'\n"
            f"Projected Impact: +45 to +90 authentic 5-star Google Reviews within 30 days in {cluster}."
        )

        return {
            "business_name": name,
            "cluster": cluster,
            "monthly_retainer_inr": client.monthly_fee_inr,
            "social_hooks": social_hooks,
            "whatsapp_ai_script": whatsapp_ai_script,
            "review_booster": review_booster,
            "direct_pitch_url": client.pitch_url
        }

    def generate_whatsapp_pitch_link(self, client: SMBGrowthClient) -> str:
        """Generates a 1-click WhatsApp click-to-chat URL with tailored pitch."""
        clean_phone = client.contact_phone.replace("+", "").replace("-", "").strip()
        message = (
            f"Namaskara {client.business_name} Team,\n\n"
            f"I noticed your high footfall in {client.cluster.value} ({client.landmark}). "
            f"We built an autonomous 24/7 AI WhatsApp Concierge for premier {client.niche} "
            f"businesses in Bengaluru that captures after-hours inquiries and adds +35 paying tech clients monthly.\n\n"
            f"Can I send you a 60-second interactive preview built specially for {client.business_name}?"
        )
        encoded = urllib.parse.quote(message)
        return f"https://wa.me/{clean_phone}?text={encoded}"
