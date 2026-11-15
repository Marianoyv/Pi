"""Fail the publishing pipeline when editorial content misses quality requirements."""

import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pi_development.web.knowledge_pages import KNOWLEDGE_PAGE_DEFINITIONS


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_TEXT_FIELDS = (
    "article_type",
    "slug",
    "title",
    "meta_description",
    "eyebrow",
    "cluster_key",
    "h1",
    "description",
    "summary",
    "search_intent",
    "business_relevance",
    "published_datetime",
    "updated_datetime",
    "image",
    "image_alt",
)
ALLOWED_CLUSTERS = {
    "adtech",
    "carrera",
    "creatividades",
    "ia",
    "producto",
    "seo-performance",
    "tecnologia-vida",
    "tracking",
    "web-actual",
}
ALLOWED_ARTICLE_TYPES = {"analysis", "case-study", "essay", "guide", "interview", "news"}


class Command(BaseCommand):
    help = "Validate every file-backed editorial article before build or deploy."

    def handle(self, *args, **options):
        articles_dir = Path(settings.BASE_DIR) / "content" / "articles"
        article_paths = sorted(articles_dir.glob("*.json"))
        if not article_paths:
            raise CommandError("No editorial JSON articles were found.")

        errors = []
        article_entries = []
        file_slugs = set()
        for article_path in article_paths:
            try:
                article = json.loads(article_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{article_path.name}: invalid JSON ({exc})")
                continue
            article_entries.append((article_path.name, article))
            if isinstance(article, dict) and isinstance(article.get("slug"), str):
                file_slugs.add(article["slug"])

        article_entries.extend(
            (f"built-in:{article['slug']}", article)
            for article in KNOWLEDGE_PAGE_DEFINITIONS
            if article.get("slug") not in file_slugs
        )

        slugs = {}
        for source_name, article in article_entries:
            article_errors = self._validate_article(article)
            slug = article.get("slug")
            if isinstance(slug, str) and slug:
                if slug in slugs:
                    article_errors.append(f"duplicate slug also used by {slugs[slug]}")
                else:
                    slugs[slug] = source_name
            errors.extend(f"{source_name}: {message}" for message in article_errors)

        if errors:
            formatted = "\n - ".join(errors)
            raise CommandError(f"Editorial validation failed:\n - {formatted}")

        self.stdout.write(self.style.SUCCESS(f"Editorial validation passed: {len(article_entries)} article(s)."))

    @staticmethod
    def _validate_article(article):
        errors = []
        if not isinstance(article, dict):
            return ["the document must be a JSON object"]

        for field in REQUIRED_TEXT_FIELDS:
            if not isinstance(article.get(field), str) or not article[field].strip():
                errors.append(f"{field} must be a non-empty string")

        slug = article.get("slug", "")
        if isinstance(slug, str) and slug and not SLUG_PATTERN.fullmatch(slug):
            errors.append("slug must contain only lowercase letters, numbers and hyphens")

        if article.get("status") != "published":
            errors.append("status must be published before deployment")

        if article.get("cluster_key") not in ALLOWED_CLUSTERS:
            errors.append(f"cluster_key must be one of: {', '.join(sorted(ALLOWED_CLUSTERS))}")

        if article.get("article_type") not in ALLOWED_ARTICLE_TYPES:
            errors.append(f"article_type must be one of: {', '.join(sorted(ALLOWED_ARTICLE_TYPES))}")

        meta_description = article.get("meta_description", "")
        if isinstance(meta_description, str) and not 120 <= len(meta_description.strip()) <= 170:
            errors.append("meta_description must contain between 120 and 170 characters")

        summary = article.get("summary", "")
        if isinstance(summary, str) and not 80 <= len(summary.strip()) <= 260:
            errors.append("summary must contain between 80 and 260 characters")

        for field in ("published_at", "updated_at"):
            value = article.get(field)
            try:
                parsed_date = date.fromisoformat(value)
                if parsed_date > date.today():
                    errors.append(f"{field} cannot be in the future")
            except (TypeError, ValueError):
                errors.append(f"{field} must use YYYY-MM-DD")

        published_at = article.get("published_at", "")
        updated_at = article.get("updated_at", "")
        if isinstance(published_at, str) and isinstance(updated_at, str) and updated_at < published_at:
            errors.append("updated_at cannot be earlier than published_at")

        parsed_datetimes = {}
        for field in ("published_datetime", "updated_datetime"):
            value = article.get(field, "")
            try:
                parsed = datetime.fromisoformat(value)
                if parsed.tzinfo is None:
                    errors.append(f"{field} must include a UTC offset")
                parsed_datetimes[field] = parsed
            except (TypeError, ValueError):
                errors.append(f"{field} must use ISO 8601 with a UTC offset")

        if all(field in parsed_datetimes for field in ("published_datetime", "updated_datetime")):
            if parsed_datetimes["updated_datetime"] < parsed_datetimes["published_datetime"]:
                errors.append("updated_datetime cannot be earlier than published_datetime")
            if parsed_datetimes["published_datetime"].date().isoformat() != published_at:
                errors.append("published_datetime must match published_at")
            if parsed_datetimes["updated_datetime"].date().isoformat() != updated_at:
                errors.append("updated_datetime must match updated_at")

        image = article.get("image", "")
        if isinstance(image, str) and image:
            image_path = Path(settings.BASE_DIR) / "static" / image
            if image_path.suffix.lower() != ".webp":
                errors.append("image must use the WebP format")
            if not image_path.is_file():
                errors.append(f"image does not exist: {image}")

        image_alt = article.get("image_alt", "")
        if isinstance(image_alt, str) and not 50 <= len(image_alt.strip()) <= 180:
            errors.append("image_alt must contain between 50 and 180 characters")

        reading_time = article.get("reading_time_minutes")
        if not isinstance(reading_time, int) or not 3 <= reading_time <= 15:
            errors.append("reading_time_minutes must be an integer between 3 and 15")

        intro = article.get("intro_paragraphs")
        if not Command._valid_text_list(intro, minimum=2):
            errors.append("intro_paragraphs must contain at least two non-empty paragraphs")

        takeaways = article.get("key_takeaways")
        if not Command._valid_text_list(takeaways, minimum=3):
            errors.append("key_takeaways must contain at least three non-empty items")

        target_audience = article.get("target_audience")
        if not Command._valid_text_list(target_audience, minimum=2):
            errors.append("target_audience must contain at least two specific audiences")

        sections = article.get("sections")
        if not isinstance(sections, list) or len(sections) < 4:
            errors.append("sections must contain at least four sections")
        else:
            for index, section in enumerate(sections, start=1):
                if not isinstance(section, dict) or not isinstance(section.get("title"), str):
                    errors.append(f"section {index} must have a title")
                    continue
                if not Command._valid_text_list(section.get("paragraphs"), minimum=1):
                    errors.append(f"section {index} must contain at least one paragraph")

        sources = article.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append("sources must contain at least one primary source")
        else:
            if not any(source.get("source_type") == "primary" for source in sources if isinstance(source, dict)):
                errors.append("at least one source must declare source_type as primary")
            for index, source in enumerate(sources, start=1):
                if not isinstance(source, dict):
                    errors.append(f"source {index} must be an object")
                    continue
                for field in ("publisher", "title", "url", "accessed_at", "source_type"):
                    if not isinstance(source.get(field), str) or not source[field].strip():
                        errors.append(f"source {index} requires {field}")
                parsed_url = urlparse(source.get("url", ""))
                if parsed_url.scheme != "https" or not parsed_url.netloc:
                    errors.append(f"source {index} must use a valid HTTPS URL")
                for field in ("published_at", "accessed_at"):
                    if not source.get(field):
                        continue
                    try:
                        date.fromisoformat(source.get(field, ""))
                    except ValueError:
                        errors.append(f"source {index} {field} must use YYYY-MM-DD")

        faqs = article.get("faqs")
        if not isinstance(faqs, list) or len(faqs) < 2:
            errors.append("faqs must contain at least two useful questions")

        word_count = Command._word_count(article)
        if word_count < 500:
            errors.append(f"article is too thin ({word_count} words; minimum 500)")
        if word_count > 1800:
            errors.append(f"article is too long ({word_count} words; maximum 1800)")

        return errors

    @staticmethod
    def _valid_text_list(value, minimum):
        return (
            isinstance(value, list)
            and len(value) >= minimum
            and all(isinstance(item, str) and item.strip() for item in value)
        )

    @staticmethod
    def _word_count(article):
        text_parts = []
        text_parts.extend(article.get("intro_paragraphs", []))
        text_parts.extend(article.get("key_takeaways", []))
        for section in article.get("sections", []):
            if isinstance(section, dict):
                text_parts.extend(section.get("paragraphs", []))
                text_parts.extend(section.get("bullets", []))
        for faq in article.get("faqs", []):
            if isinstance(faq, dict):
                text_parts.extend([faq.get("question", ""), faq.get("answer", "")])
        return len(" ".join(part for part in text_parts if isinstance(part, str)).split())
