"""==============================================================================
PROGRAMMATIC SEO & DIRECTORY ENGINE
==============================================================================
Generates mass-scale, high-intent comparison, alternative, and local service
landing pages with valid JSON-LD schema, conversion CTAs, and XML sitemaps.
==============================================================================
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

class ProgrammaticSEOEngine:
    """High-velocity programmatic landing page and directory compiler."""

    def __init__(self, base_url: str = "https://omniverse.cashflow.io"):
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def slugify(text: str) -> str:
        """Create URL-safe lowercase slug."""
        clean = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
        return f"{clean}-alternative"

    def generate_software_alternative_page(
        self,
        competitor_name: str,
        our_product_name: str,
        niche: str,
        features_diff: List[Dict[str, Any]],
        pricing_our: str,
        pricing_competitor: str,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generates a high-converting 'X Alternative' landing page."""
        slug = self.slugify(competitor_name)
        url = f"{self.base_url}/alternatives/{slug}"

        clean_price = (
            pricing_our.replace("$", "")
            .replace("₹", "")
            .replace("/mo", "")
            .replace(",", "")
            .strip()
        )

        schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": our_product_name,
            "applicationCategory": category or "BusinessApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": clean_price,
                "priceCurrency": "USD" if "$" in pricing_our else "INR"
            },
            "description": f"The premier modern alternative to {competitor_name} for {niche}."
        }

        cat_badge = f"\n**Category**: {category}  " if category else ""

        markdown = f"""---
title: "Best {competitor_name} Alternative in 2027: Why Modern Teams Choose {our_product_name}"
description: "Looking for an alternative to {competitor_name}? Discover how {our_product_name} provides faster performance, lower pricing ({pricing_our} vs {pricing_competitor}), and 24/7 automation."
url: "{url}"
schema: {json.dumps(schema)}
---

# Why {our_product_name} is the #1 Alternative to {competitor_name}
{cat_badge}
If you are frustrated by {competitor_name}'s rising prices ({pricing_competitor}) and legacy complexity, **{our_product_name}** offers a lightweight, high-performance solution built specifically for {niche}.

## Feature Comparison Matrix

| Feature | {our_product_name} | {competitor_name} |
| :--- | :--- | :--- |
| **Pricing** | **{pricing_our}** | {pricing_competitor} |
"""
        for item in features_diff:
            markdown += f"| **{item['feature']}** | {item['us']} | {item['them']} |\n"

        markdown += f"""
## Why Switch from {competitor_name}?
1. **Immediate Time-to-Value**: Setup takes less than 3 minutes.
2. **Transparent Pricing**: No hidden contracts or tiered overage penalties.
3. **24/7 Autonomous Performance**: Self-healing background daemons guarantee zero downtime.

[Start Free Trial Today]({self.base_url}/signup?ref={slug})
"""

        return {
            "slug": slug,
            "url": url,
            "title": f"Best {competitor_name} Alternative in 2027",
            "category": category or "Software",
            "schema_json_ld": schema,
            "content_markdown": markdown
        }

    def generate_sitemap(self, pages: List[Dict[str, Any]]) -> str:
        """Generates standard Google XML sitemap."""
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for page in pages:
            xml += '  <url>\n'
            xml += f'    <loc>{page["url"]}</loc>\n'
            xml += '    <changefreq>weekly</changefreq>\n'
            xml += '    <priority>0.8</priority>\n'
            xml += '  </url>\n'
        xml += '</urlset>'
        return xml

    def batch_compile_to_disk(
        self,
        competitors: List[Union[str, Dict[str, Any]]],
        our_product: str,
        niche: str,
        output_dir: Path
    ) -> Dict[str, Any]:
        """Compiles a batch of programmatic pages and writes them to output_dir."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        pages = []
        for item in competitors:
            if isinstance(item, dict):
                comp_name = item["name"]
                cat = item.get("category", "Enterprise Software")
                item_niche = item.get("niche", niche)
                diff = item.get("features_diff", [
                    {"feature": "Autonomous 24/7 Daemon", "us": "✅ Built-in", "them": "❌ Not available"},
                    {"feature": "Zero-Brokerage Gating", "us": "✅ Included", "them": "❌ 1-2 Mo Brokerage"},
                    {"feature": "Automated Setup Time", "us": "⚡ 3 Minutes", "them": "⏳ 2-4 Weeks"}
                ])
                price_our = item.get("pricing_our", "$29/mo")
                price_comp = item.get("pricing_competitor", "$149/mo")
            else:
                comp_name = str(item)
                cat = None
                item_niche = niche
                diff = [
                    {"feature": "Autonomous 24/7 Daemon", "us": "✅ Built-in", "them": "❌ Not available"},
                    {"feature": "Zero-Brokerage Gating", "us": "✅ Included", "them": "❌ 1-2 Mo Brokerage"},
                    {"feature": "Automated Setup Time", "us": "⚡ 3 Minutes", "them": "⏳ 2-4 Weeks"}
                ]
                price_our = "$29/mo"
                price_comp = "$149/mo"

            page = self.generate_software_alternative_page(
                competitor_name=comp_name,
                our_product_name=our_product,
                niche=item_niche,
                features_diff=diff,
                pricing_our=price_our,
                pricing_competitor=price_comp,
                category=cat
            )
            file_path = output_dir / f"{page['slug']}.md"
            file_path.write_text(page["content_markdown"], encoding="utf-8")
            pages.append(page)

        sitemap_xml = self.generate_sitemap(pages)
        (output_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

        return {
            "pages_compiled": len(pages),
            "output_dir": str(output_dir),
            "sitemap_path": str(output_dir / "sitemap.xml")
        }
