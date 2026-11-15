"""Build a compact, deterministic memory file for the daily editorial automation."""

import json
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from pi_development.web.knowledge_pages import get_knowledge_page, get_public_knowledge_slugs
from pi_development.web.seo_pages import get_public_seo_page_slugs, get_seo_page
from pi_development.web.tool_catalog import get_public_tool_slugs, get_tool


class Command(BaseCommand):
    help = "Generate the compact editorial coverage and internal-link index."

    def handle(self, *args, **options):
        articles = []
        for slug in get_public_knowledge_slugs():
            page = get_knowledge_page(slug)
            articles.append(
                {
                    "published_at": page.get("published_at"),
                    "slug": page["slug"],
                    "title": page["h1"],
                    "cluster": page.get("cluster_key"),
                    "search_intent": page.get("search_intent") or page["h1"],
                    "source_urls": [source["url"] for source in page.get("sources", [])],
                }
            )
        articles.sort(key=lambda item: (item.get("published_at") or "", item["slug"]), reverse=True)

        products = []
        for slug in get_public_tool_slugs():
            tool = get_tool(slug)
            products.append({"slug": slug, "name": tool["name"], "url": f"/products/{slug}/"})

        guides = []
        for slug in get_public_seo_page_slugs():
            page = get_seo_page(slug)
            guides.append({"slug": slug, "title": page["h1"], "url": f"/{slug}/"})

        index = {
            "version": 1,
            "generated_on": date.today().isoformat(),
            "instructions": "Use recent_articles to prevent duplicate coverage and internal_links to avoid scanning the project.",
            "recent_articles": articles[:120],
            "internal_links": {
                "products": products,
                "guides": guides,
                "commercial_pages": [
                    {"name": "AdTech", "url": "/adtech/"},
                    {"name": "Solutions", "url": "/solutions/"},
                    {"name": "Contact", "url": "/contact/"}
                ]
            }
        }

        output_path = Path(settings.BASE_DIR) / "content" / "editorial" / "index.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Editorial index ready: {len(articles)} article(s)."))
