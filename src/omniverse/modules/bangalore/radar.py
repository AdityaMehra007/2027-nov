import re
import time
from typing import List, Dict, Any, Tuple
from sqlmodel import Session, select
from omniverse.modules.bangalore.models import (
    RentalListing,
    FlatRadarSubscriber,
    BangaloreCluster,
    RadarSubscriptionTier,
)
from omniverse.core.telemetry import global_event_bus

class BangaloreFlatRadar:
    """24/7 Real-Time Zero-Brokerage Flat & Flatmate Detection & Alert Engine.

    Monitors Bangalore rental listings across social channels, strips broker
    spam using pattern heuristics, and matches high-intent paid tech subscribers.
    """

    BROKER_PENALTY_PATTERNS = [
        r"(?<!zero\s)(?<!no\s)(?<!without\s)\bbrokerage\b",
        r"(?<!zero\s)(?<!no\s)(?<!without\s)\bbrokers?\b",
        r"\bcommission\b",
        r"\b1 month rent\b",
        r"\bone month rent\b",
        r"\bhalf month\b",
        r"\b15 days brokerage\b",
        r"\bconsultancy charges\b",
        r"\bcharges\s+apply\b",
        r"\bservice\s+fee\s+applicable\b",
    ]

    DIRECT_OWNER_PATTERNS = [
        r"\bzero brokerage\b",
        r"\bno brokerage\b",
        r"\bdirect(ly)? from owner\b",
        r"\bowner here\b",
        r"\blooking for a flatmate\b",
        r"\bflatmate replacement\b",
        r"\bmoving out of bangalore\b",
        r"\bdeposit negotiable\b",
        r"\bno broker involved\b",
        r"\bmy flat\b",
        r"\bspacious room available in 3bhk\b",
    ]

    def __init__(self, session: Session):
        self.session = session

    def evaluate_listing_content(self, text: str) -> Tuple[bool, float]:
        """Analyzes listing text for broker probability.

        Returns (is_zero_brokerage, broker_confidence).
        Confidence: 0.0 = Verified Direct Owner, 1.0 = Definite Broker Spam.
        """
        lowered = text.lower()
        broker_hits = sum(1 for p in self.BROKER_PENALTY_PATTERNS if re.search(p, lowered))
        owner_hits = sum(1 for p in self.DIRECT_OWNER_PATTERNS if re.search(p, lowered))

        if broker_hits > 0 and owner_hits == 0:
            confidence = min(0.60 + (broker_hits * 0.15), 1.0)
            return False, confidence

        if owner_hits > 0 and broker_hits == 0:
            confidence = max(0.05, 0.35 - (owner_hits * 0.10))
            return True, confidence

        if owner_hits > broker_hits:
            confidence = 0.30
            return True, confidence

        # Default neutral/unverified
        return (broker_hits == 0), 0.45

    def ingest_and_evaluate(
        self,
        title: str,
        cluster: BangaloreCluster,
        locality: str,
        bhk: int,
        rent_inr: float,
        deposit_inr: float,
        raw_content: str,
        contact_phone: str = "",
        source_platform: str = "Bangalore Flat & Flatmates",
        listing_url: str = ""
    ) -> RentalListing:
        is_zero_brokerage, confidence = self.evaluate_listing_content(raw_content)

        listing = RentalListing(
            title=title,
            cluster=cluster,
            locality=locality,
            bhk=bhk,
            rent_inr=rent_inr,
            deposit_inr=deposit_inr,
            is_zero_brokerage=is_zero_brokerage,
            broker_confidence=confidence,
            contact_phone=contact_phone,
            source_platform=source_platform,
            listing_url=listing_url,
            raw_content=raw_content,
            verified_at=time.time()
        )
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(listing)

        global_event_bus.publish("BANGALORE_LISTING_INGESTED", {
            "id": listing.id,
            "cluster": cluster.value,
            "rent_inr": rent_inr,
            "is_zero_brokerage": is_zero_brokerage,
            "confidence": confidence
        })

        return listing

    def match_subscribers(self, listing: RentalListing) -> List[Dict[str, Any]]:
        """Matches a newly ingested zero-brokerage listing against active paying subscribers."""
        if not listing.is_zero_brokerage:
            return []

        now = time.time()
        active_subs = self.session.exec(
            select(FlatRadarSubscriber).where(
                FlatRadarSubscriber.is_active == True,
                FlatRadarSubscriber.pass_expires_at > now
            )
        ).all()

        matched_alerts = []
        for sub in active_subs:
            target_list = [c.strip().lower() for c in sub.target_clusters.split(",")]
            cluster_match = (
                listing.cluster.value.lower() in target_list
                or "all" in target_list
            )
            bhk_match = (sub.preferred_bhk == 0 or sub.preferred_bhk == listing.bhk)
            budget_match = (listing.rent_inr <= sub.max_budget_inr * 1.15)  # 15% flexibility

            if cluster_match and bhk_match and budget_match:
                alert_text = (
                    f"⚡ [NAMMAFLAT 24/7 VIP ALERT] Zero-Brokerage Match!\n\n"
                    f"📍 Location: {listing.locality}, {listing.cluster.value}\n"
                    f"🏠 Type: {listing.bhk} BHK | Rent: ₹{listing.rent_inr:,.0f}/mo | Deposit: ₹{listing.deposit_inr:,.0f}\n"
                    f"✅ Verification: Direct Owner (Broker Confidence: {listing.broker_confidence * 100:.0f}%)\n"
                    f"📞 Contact: {listing.contact_phone or 'Check listing link'}\n"
                    f"🔗 Source: {listing.source_platform}\n"
                    f"💬 Tip: High demand in {listing.cluster.value}—contact within 15 mins!"
                )
                matched_alerts.append({
                    "subscriber_id": sub.id,
                    "subscriber_name": sub.name,
                    "whatsapp": sub.phone_whatsapp,
                    "tier": sub.tier.value,
                    "alert_payload": alert_text,
                    "listing_id": listing.id
                })

        return matched_alerts

    def generate_simulated_bangalore_feed(self) -> List[RentalListing]:
        """Generates realistic Bangalore direct-owner and broker listings for testing/simulation."""
        sample_posts = [
            (
                "Spacious 2BHK in HSR Layout Sector 2",
                BangaloreCluster.HSR_LAYOUT,
                "Sector 2, 27th Main",
                2,
                32000.0,
                100000.0,
                "Hey folks, moving out of Bangalore this month! Giving away our lovely 2BHK in HSR Sector 2. Direct from owner, zero brokerage. Deposit negotiable.",
                "+91-9845011223"
            ),
            (
                "1BHK in Indiranagar 12th Main near Toit",
                BangaloreCluster.INDIRANAGAR,
                "12th Main, HAL 2nd Stage",
                1,
                24000.0,
                80000.0,
                "1BHK fully furnished for bachelor or couple. Direct owner here. Walkable to Indiranagar metro station. No broker involved.",
                "+91-9980122334"
            ),
            (
                "3BHK Luxury Penthouse in Koramangala 4th Block",
                BangaloreCluster.KORAMANGALA,
                "4th Block, 80ft Road",
                3,
                55000.0,
                200000.0,
                "Premium 3BHK flat near Sony World Signal. 1 month rent brokerage applicable. Excellent amenities, covered parking.",
                "+91-9741033445"
            ),
            (
                "Private Room in 3BHK in Bellandur EcoSpace",
                BangaloreCluster.BELLANDUR,
                "Green Glen Layout, near EcoSpace",
                1,
                16500.0,
                50000.0,
                "Looking for a female flatmate in a 3BHK gated society. Zero brokerage, shared cook and maid already set up. Move in immediately.",
                "+91-9611044556"
            ),
            (
                "2BHK in Whitefield near Hope Farm",
                BangaloreCluster.WHITEFIELD,
                "ECC Road, Whitefield",
                2,
                28000.0,
                90000.0,
                "Owner post: 2BHK flat available from Dec 1. Modular kitchen, power backup. Only direct tenants, brokers please excuse.",
                "+91-9880055667"
            )
        ]

        ingested = []
        for title, cluster, locality, bhk, rent, dep, text, phone in sample_posts:
            listing = self.ingest_and_evaluate(
                title=title,
                cluster=cluster,
                locality=locality,
                bhk=bhk,
                rent_inr=rent,
                deposit_inr=dep,
                raw_content=text,
                contact_phone=phone,
                source_platform="r/bangalore & Flatmates"
            )
            ingested.append(listing)

        return ingested
