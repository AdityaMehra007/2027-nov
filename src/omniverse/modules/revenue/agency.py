from typing import List
from omniverse.modules.revenue.models import GrowthKit

class GrowthKitGenerator:
    """Generates production-grade local business growth kits, social captions,

    promotional hooks, and WhatsApp catalog copy.
    """

    def generate(self, business_name: str, niche: str, city: str = "Bengaluru") -> GrowthKit:
        captions: List[str] = [
            f"Craving perfection? Discover why {business_name} is {city}'s top choice for {niche}. Visit us today!",
            f"Behind the scenes at {business_name}: Passion, quality, and dedication in every detail. #Experience{city}",
            f"Weekend plans? Treat yourself to something special at {business_name}. Book your spot now!",
            f"Customer love: 'The best {niche} in {city}!' Thank you for making {business_name} your home.",
            f"Did you know? At {business_name}, we craft every experience with premium standards. Drop by today!",
            f"Mid-week boost: Elevate your routine with {business_name}. Direct message us to learn more.",
            f"Fresh, authentic, and local. That is the {business_name} promise right here in {city}.",
            f"Tag someone who needs a visit to {business_name} this week! #BestOf{city}",
            f"Limited seasonal special: Experience our signature {niche} collection exclusively at {business_name}.",
            f"Your satisfaction is our obsession. Connect with {business_name} on WhatsApp for direct perks!"
        ]

        hooks: List[str] = [
            f"Why {city} locals are switching to {business_name} for premium {niche}.",
            f"3 reasons why your current {niche} routine is missing out on {business_name}.",
            f"How {business_name} delivers 5-star quality without the premium price tag in {city}.",
            f"Stop settling for average {niche}: Here is what makes {business_name} different.",
            f"The secret behind {business_name}'s fastest-growing customer community in {city}."
        ]

        whatsapp_catalog = (
            f"🌟 Welcome to {business_name} Official WhatsApp Store!\n\n"
            f"📍 Location: {city}\n"
            f"🎯 Focus: Premier {niche}\n\n"
            f"✨ Our Signature Packages:\n"
            f"1. Standard Growth Experience — Essential quality and swift service.\n"
            f"2. Executive Selection — Tailored care and VIP perks.\n"
            f"3. Custom Requests — Dedicated consultations.\n\n"
            f"💬 Reply 'ORDER' or 'BOOK' to get instant assistance from our team!"
        )

        pitch = (
            f"Hi {business_name} Team,\n\n"
            f"I came across {business_name} in {city} and love your work in {niche}. "
            f"We put together a tailored growth kit featuring 10 custom social campaigns, "
            f"WhatsApp direct-response sales copy, and 5 high-converting customer hooks designed "
            f"to bring 15-25 new paying customers to your door this month.\n\n"
            f"Can I send over the sample kit for you to review? No obligation at all."
        )

        return GrowthKit(
            business_name=business_name,
            niche=niche,
            city=city,
            social_captions=captions,
            promotional_hooks=hooks,
            whatsapp_catalog_copy=whatsapp_catalog,
            outreach_pitch=pitch
        )
