from html.parser import HTMLParser
from time import monotonic
from urllib.parse import urlparse

import requests
from django.conf import settings

from pi_development.web.tool_availability import require_remote_url_tools_enabled


HTML_SNAPSHOT_LIMIT = 350000
AD_SLOT_HINT_TOKENS = (
    "div-gpt-ad",
    "adslot",
    "ad-slot",
    "ad_slot",
    "data-ad-slot",
    "data-ad-unit",
    "google_ads",
)


class HttpSnapshotParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._inside_title = False
        self.title = ""
        self.meta_description = ""
        self.robots = ""
        self.canonical = ""
        self.h1_count = 0
        self.script_sources = []
        self.iframe_sources = []
        self.slot_hints = []

    def handle_starttag(self, tag, attrs):
        attrs_map = {key.lower(): value for key, value in attrs}
        if tag == "title":
            self._inside_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta":
            name = (attrs_map.get("name") or "").lower()
            if name == "description" and not self.meta_description:
                self.meta_description = attrs_map.get("content") or ""
            if name == "robots" and not self.robots:
                self.robots = attrs_map.get("content") or ""
        if tag == "link" and "canonical" in (attrs_map.get("rel") or "").lower():
            self.canonical = attrs_map.get("href") or ""
        if tag == "script" and attrs_map.get("src"):
            self.script_sources.append(attrs_map.get("src") or "")
        if tag == "iframe" and attrs_map.get("src"):
            self.iframe_sources.append(attrs_map.get("src") or "")

        self._collect_slot_hints(attrs_map)

    def handle_endtag(self, tag):
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data):
        if self._inside_title and not self.title:
            self.title = data.strip()

    def _collect_slot_hints(self, attrs_map):
        raw_values = [
            attrs_map.get("id") or "",
            attrs_map.get("class") or "",
            attrs_map.get("data-ad-slot") or "",
            attrs_map.get("data-ad-unit") or "",
            attrs_map.get("data-slot") or "",
            attrs_map.get("data-google-query-id") or "",
        ]
        for value in raw_values:
            lowered = value.lower()
            if lowered and any(token in lowered for token in AD_SLOT_HINT_TOKENS):
                self.slot_hints.append(value)


def fetch_site_snapshot(url):
    require_remote_url_tools_enabled()
    start = monotonic()
    parsed_url = urlparse(url)

    try:
        response = requests.get(
            url,
            timeout=settings.TOOLS_HTTP_TIMEOUT,
            headers={
                "User-Agent": "PiDevelopment-Tools/1.0 (+https://pidevelopment.web.app)"
            },
        )
        elapsed_ms = int((monotonic() - start) * 1000)
        content_type = (response.headers.get("Content-Type") or "").lower()
        html_excerpt = response.text[:HTML_SNAPSHOT_LIMIT] if "html" in content_type and response.text else ""
        parser = HttpSnapshotParser()
        if html_excerpt:
            parser.feed(html_excerpt)

        return {
            "available": True,
            "status_code": response.status_code,
            "final_url": response.url,
            "content_type": content_type or "No informado",
            "response_time_ms": elapsed_ms,
            "https": parsed_url.scheme == "https",
            "redirected": response.url != url,
            "title": parser.title,
            "meta_description": parser.meta_description,
            "robots": parser.robots,
            "canonical": parser.canonical,
            "h1_count": parser.h1_count,
            "html_excerpt": html_excerpt,
            "script_sources": parser.script_sources,
            "iframe_sources": parser.iframe_sources,
            "slot_hints": parser.slot_hints,
        }
    except requests.RequestException as exc:
        return {
            "available": False,
            "error": str(exc),
            "status_code": None,
            "final_url": "",
            "content_type": "",
            "response_time_ms": None,
            "https": parsed_url.scheme == "https",
            "redirected": False,
            "title": "",
            "meta_description": "",
            "robots": "",
            "canonical": "",
            "h1_count": 0,
            "html_excerpt": "",
            "script_sources": [],
            "iframe_sources": [],
            "slot_hints": [],
        }
