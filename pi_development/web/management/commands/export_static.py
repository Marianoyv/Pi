"""Render the public Django routes into a Firebase Hosting directory."""

import re
import shutil
import json
from html import escape
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.urls import reverse

from pi_development.web.knowledge_pages import get_public_knowledge_slugs
from pi_development.web.seo_pages import get_public_seo_page_slugs
from pi_development.web.tool_catalog import get_public_tool_slugs
from pi_development.web.work_content import get_indexable_work_case_slugs


STATIC_REFERENCE_PATTERN = re.compile(rb"/static/([A-Za-z0-9_./-]+)")
SITEMAP_SECTIONS = ("pages", "tools", "work", "seo", "content")
STATIC_REDIRECTS = {
    "/tools/": "/products/",
    "/labs/": "/products/",
    "/systems/": "/solutions/",
    "/case-studies/": "/work/",
    "/approach/": "/solutions/#process",
    "/about/": "/company/",
    "/blog/": "/insights/",
    "/services/": "/solutions/",
    "/services/web-development/": "/solutions/",
    "/services/ux-ui/": "/solutions/",
    "/services/marketing/": "/solutions/",
    "/services/seo/": "/solutions/",
    "/portfolio/": "/work/",
    "/process/": "/solutions/#process",
    "/resources/": "/products/",
}

for _product_slug in get_public_tool_slugs():
    STATIC_REDIRECTS[f"/tools/{_product_slug}/"] = f"/products/{_product_slug}/"


def get_public_html_routes():
    routes = [
        reverse("index"),
        reverse("business_solutions"),
        reverse("web_plans"),
        reverse("solutions"),
        reverse("adtech"),
        reverse("insights"),
        reverse("products"),
        reverse("work"),
        reverse("company"),
        reverse("contact"),
        reverse("policies"),
    ]
    routes.extend(reverse("product_detail", kwargs={"slug": slug}) for slug in get_public_tool_slugs())
    routes.extend(reverse("seo_page", kwargs={"slug": slug}) for slug in get_public_seo_page_slugs())
    routes.extend(reverse("knowledge_page", kwargs={"slug": slug}) for slug in get_public_knowledge_slugs())
    routes.extend(reverse("work_case", kwargs={"slug": slug}) for slug in get_indexable_work_case_slugs())
    return routes


def output_path_for_route(output_dir, route):
    if route == "/":
        return output_dir / "index.html"
    return output_dir / route.strip("/") / "index.html"


class Command(BaseCommand):
    help = "Render the public site as static files for Firebase Hosting."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="dist",
            help="Output directory relative to the project root (default: dist).",
        )

    def handle(self, *args, **options):
        if not getattr(settings, "STATIC_EXPORT", False):
            raise CommandError(
                "Use --settings=pi_development.settings.static_export so forms, metadata and assets render safely."
            )

        base_dir = Path(settings.BASE_DIR).resolve()
        output_dir = (base_dir / options["output"]).resolve()
        if output_dir == base_dir or base_dir not in output_dir.parents:
            raise CommandError("The static output directory must stay inside the project and cannot be its root.")

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

        client = Client(HTTP_HOST="testserver")
        static_references = set()
        rendered_routes = []

        for route in get_public_html_routes():
            response = client.get(route, secure=True)
            if response.status_code != 200:
                raise CommandError(f"Static route {route} returned HTTP {response.status_code}.")
            self._write_response(output_path_for_route(output_dir, route), response.content)
            static_references.update(STATIC_REFERENCE_PATTERN.findall(response.content))
            rendered_routes.append(route)

        for route, relative_output in (
            (reverse("robots_txt"), "robots.txt"),
            (reverse("sitemap"), "sitemap.xml"),
            (reverse("sitemap_news"), "sitemap-news.xml"),
        ):
            response = client.get(route, secure=True)
            if response.status_code != 200:
                raise CommandError(f"Static route {route} returned HTTP {response.status_code}.")
            self._write_response(output_dir / relative_output, response.content)

        for section in SITEMAP_SECTIONS:
            route = reverse("sitemap_section", kwargs={"section": section})
            response = client.get(route, secure=True)
            if response.status_code != 200:
                raise CommandError(f"Sitemap section {section} returned HTTP {response.status_code}.")
            self._write_response(output_dir / f"sitemap-{section}.xml", response.content)

        for source, destination in STATIC_REDIRECTS.items():
            self._write_response(
                output_path_for_route(output_dir, source),
                self._redirect_document(destination),
            )

        not_found = client.get("/__static-export-missing__/", secure=True)
        if not_found.status_code != 404:
            raise CommandError("The static 404 probe did not return HTTP 404.")
        self._write_response(output_dir / "404.html", not_found.content)
        static_references.update(STATIC_REFERENCE_PATTERN.findall(not_found.content))

        static_references.update({b"web/img/pi.ico", b"web/img/pi.png"})
        if getattr(settings, "GOOGLE_ANALYTICS_ID", ""):
            # This dependency is imported dynamically, so the HTML scan cannot discover it.
            static_references.update({b"web/js/vendor/web-vitals.js", b"web/js/vendor/web-vitals-LICENSE.txt", b"web/js/vendor/web-vitals-NOTICE.txt"})
        copied_assets = self._copy_static_assets(base_dir, output_dir, static_references)
        shutil.copy2(base_dir / "static" / "web" / "img" / "pi.ico", output_dir / "favicon.ico")

        self.stdout.write(
            self.style.SUCCESS(
                f"Static export ready: {len(rendered_routes)} HTML pages, "
                f"{len(STATIC_REDIRECTS)} redirect fallbacks, {len(SITEMAP_SECTIONS) + 2} sitemap files "
                f"and {copied_assets} static assets in {output_dir}."
            )
        )

    @staticmethod
    def _write_response(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    @staticmethod
    def _redirect_document(destination):
        target = escape(destination, quote=True)
        canonical = escape(f"{settings.SITE_URL.rstrip('/')}{destination}", quote=True)
        script_target = json.dumps(destination)
        return (
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"robots\" content=\"noindex, follow\">"
            f"<meta http-equiv=\"refresh\" content=\"0; url={target}\">"
            f"<link rel=\"canonical\" href=\"{canonical}\">"
            "<title>Page moved | Pi Development</title></head><body>"
            f"<p>This page moved to <a href=\"{target}\">{target}</a>.</p>"
            f"<script>location.replace({script_target});</script></body></html>"
        ).encode("utf-8")

    @staticmethod
    def _copy_static_assets(base_dir, output_dir, references):
        static_source = (base_dir / "static").resolve()
        copied = 0
        for encoded_reference in sorted(references):
            relative_path = Path(encoded_reference.decode("utf-8"))
            source = (static_source / relative_path).resolve()
            if static_source not in source.parents or not source.is_file():
                raise CommandError(f"Referenced static asset is missing or unsafe: {relative_path.as_posix()}")
            destination = output_dir / "static" / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied += 1
        return copied
