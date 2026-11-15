"""Import read-only GA4 and Search Console data for local analysis."""

import csv
import json
import os
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


SCOPES = (
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
)

GA4_REPORTS = {
    "overview": {
        "dimensions": ["date"],
        "metrics": ["activeUsers", "sessions", "engagedSessions", "eventCount", "keyEvents"],
        "limit": 10000,
    },
    "acquisition": {
        "dimensions": ["sessionDefaultChannelGroup", "sessionSourceMedium", "sessionCampaignName"],
        "metrics": ["activeUsers", "sessions", "engagedSessions", "keyEvents"],
        "limit": 25000,
    },
    "landing_pages": {
        "dimensions": ["landingPagePlusQueryString", "sessionDefaultChannelGroup"],
        "metrics": ["activeUsers", "sessions", "engagedSessions", "keyEvents"],
        "limit": 25000,
    },
    "pages": {
        "dimensions": ["pagePathPlusQueryString", "pageTitle"],
        "metrics": ["screenPageViews", "activeUsers", "userEngagementDuration", "eventCount", "keyEvents"],
        "limit": 25000,
    },
    "events": {
        "dimensions": ["eventName"],
        "metrics": ["eventCount", "totalUsers", "keyEvents"],
        "limit": 10000,
    },
    "audience": {
        "dimensions": ["deviceCategory", "country"],
        "metrics": ["activeUsers", "sessions", "engagedSessions", "keyEvents"],
        "limit": 25000,
    },
}

SEARCH_CONSOLE_REPORTS = {
    "daily": ["date"],
    "queries": ["query"],
    "pages": ["page"],
    "query_pages": ["query", "page"],
    "devices": ["device"],
    "countries": ["country"],
}


class Command(BaseCommand):
    help = "Import GA4 and Search Console reports into analytics/raw (read-only APIs)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=90, help="Days in the current comparison period.")
        parser.add_argument("--end-date", help="Last date to import (YYYY-MM-DD, defaults to yesterday).")
        parser.add_argument("--output-dir", help="Override the local output directory.")
        parser.add_argument("--skip-ga4", action="store_true", help="Do not request GA4 data.")
        parser.add_argument("--skip-search-console", action="store_true", help="Do not request Search Console data.")

    def handle(self, *args, **options):
        days = options["days"]
        if days < 1 or days > 366:
            raise CommandError("--days must be between 1 and 366.")

        try:
            end_date = date.fromisoformat(options["end_date"]) if options["end_date"] else date.today() - timedelta(days=1)
        except ValueError as exc:
            raise CommandError("--end-date must use YYYY-MM-DD.") from exc

        periods = self._periods(end_date, days)
        property_id = os.environ.get("GA4_PROPERTY_ID", "").strip()
        search_console_site = os.environ.get("SEARCH_CONSOLE_SITE_URL", "").strip()
        use_ga4 = not options["skip_ga4"]
        use_search_console = not options["skip_search_console"]

        if use_ga4 and not property_id:
            raise CommandError("Set GA4_PROPERTY_ID to the numeric GA4 property ID, or pass --skip-ga4.")
        if use_search_console and not search_console_site:
            raise CommandError(
                "Set SEARCH_CONSOLE_SITE_URL (URL-prefix or sc-domain property), or pass --skip-search-console."
            )
        if not use_ga4 and not use_search_console:
            raise CommandError("At least one data source must be enabled.")

        session, credential_source = self._authorized_session()
        output_dir = Path(options["output_dir"]) if options["output_dir"] else (
            Path(settings.BASE_DIR) / "analytics" / "raw" / end_date.isoformat()
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        datasets = {}
        if use_ga4:
            for report_name, report in GA4_REPORTS.items():
                rows = []
                for period_name, period in periods.items():
                    response = self._fetch_ga4(session, property_id, report, period)
                    rows.extend(self._normalize_ga4(response, period_name))
                datasets[f"ga4_{report_name}"] = rows
                self._write_dataset(output_dir, f"ga4_{report_name}", rows)
                self.stdout.write(f"GA4 {report_name}: {len(rows)} rows")

        if use_search_console:
            for report_name, dimensions in SEARCH_CONSOLE_REPORTS.items():
                rows = []
                for period_name, period in periods.items():
                    response = self._fetch_search_console(session, search_console_site, dimensions, period)
                    rows.extend(self._normalize_search_console(response, dimensions, period_name))
                datasets[f"search_console_{report_name}"] = rows
                self._write_dataset(output_dir, f"search_console_{report_name}", rows)
                self.stdout.write(f"Search Console {report_name}: {len(rows)} rows")

        manifest = {
            "generated_at": date.today().isoformat(),
            "credential_source": credential_source,
            "periods": {name: {key: value.isoformat() for key, value in period.items()} for name, period in periods.items()},
            "ga4_property_id": property_id if use_ga4 else None,
            "search_console_site_url": search_console_site if use_search_console else None,
            "datasets": {name: len(rows) for name, rows in datasets.items()},
        }
        (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (output_dir / "summary.md").write_text(self._build_summary(datasets, periods), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Analytics import complete: {output_dir}"))

    @staticmethod
    def _periods(end_date, days):
        current_start = end_date - timedelta(days=days - 1)
        previous_end = current_start - timedelta(days=1)
        return {
            "current": {"start": current_start, "end": end_date},
            "previous": {"start": previous_end - timedelta(days=days - 1), "end": previous_end},
        }

    @staticmethod
    def _authorized_session():
        try:
            import google.auth
            from google.auth.exceptions import DefaultCredentialsError
            from google.auth.transport.requests import AuthorizedSession
        except ImportError as exc:
            raise CommandError("Install analytics dependencies with: pip install -r requirements.txt") from exc

        try:
            credentials, project_id = google.auth.default(scopes=SCOPES)
        except DefaultCredentialsError as exc:
            raise CommandError(
                "Google credentials were not found. Set GOOGLE_APPLICATION_CREDENTIALS to a read-only "
                "service-account JSON file or configure Application Default Credentials."
            ) from exc
        return AuthorizedSession(credentials), project_id or "application-default-credentials"

    @staticmethod
    def _fetch_ga4(session, property_id, report, period):
        payload = {
            "dateRanges": [{"startDate": period["start"].isoformat(), "endDate": period["end"].isoformat()}],
            "dimensions": [{"name": name} for name in report["dimensions"]],
            "metrics": [{"name": name} for name in report["metrics"]],
            "limit": str(report["limit"]),
            "keepEmptyRows": False,
        }
        url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
        response = session.post(url, json=payload, timeout=60)
        try:
            response.raise_for_status()
        except Exception as exc:
            raise CommandError(f"GA4 request failed: {response.status_code} {response.text[:500]}") from exc
        return response.json()

    @staticmethod
    def _fetch_search_console(session, site_url, dimensions, period):
        payload = {
            "startDate": period["start"].isoformat(),
            "endDate": period["end"].isoformat(),
            "dimensions": dimensions,
            "rowLimit": 25000,
            "dataState": "final",
        }
        encoded_site = quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
        response = session.post(url, json=payload, timeout=60)
        try:
            response.raise_for_status()
        except Exception as exc:
            raise CommandError(f"Search Console request failed: {response.status_code} {response.text[:500]}") from exc
        return response.json()

    @staticmethod
    def _normalize_ga4(response, period_name):
        dimensions = [item["name"] for item in response.get("dimensionHeaders", [])]
        metrics = [item["name"] for item in response.get("metricHeaders", [])]
        rows = []
        for row in response.get("rows", []):
            normalized = {"period": period_name}
            normalized.update(
                {name: value.get("value", "") for name, value in zip(dimensions, row.get("dimensionValues", []))}
            )
            normalized.update(
                {name: value.get("value", "") for name, value in zip(metrics, row.get("metricValues", []))}
            )
            rows.append(normalized)
        return rows

    @staticmethod
    def _normalize_search_console(response, dimensions, period_name):
        rows = []
        for row in response.get("rows", []):
            normalized = {"period": period_name}
            normalized.update({name: value for name, value in zip(dimensions, row.get("keys", []))})
            for metric in ("clicks", "impressions", "ctr", "position"):
                normalized[metric] = row.get(metric, 0)
            rows.append(normalized)
        return rows

    @staticmethod
    def _write_dataset(output_dir, name, rows):
        (output_dir / f"{name}.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        if not rows:
            (output_dir / f"{name}.csv").write_text("", encoding="utf-8")
            return
        fieldnames = list(dict.fromkeys(key for row in rows for key in row))
        with (output_dir / f"{name}.csv").open("w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    @classmethod
    def _build_summary(cls, datasets, periods):
        lines = [
            "# Analytics performance summary",
            "",
            f"Current: {periods['current']['start']} to {periods['current']['end']}",
            f"Previous: {periods['previous']['start']} to {periods['previous']['end']}",
            "",
        ]

        overview = datasets.get("ga4_overview", [])
        if overview:
            lines.extend(["## GA4", ""])
            for metric in ("activeUsers", "sessions", "engagedSessions", "eventCount", "keyEvents"):
                current = cls._sum(overview, metric, "current")
                previous = cls._sum(overview, metric, "previous")
                lines.append(f"- {metric}: {current:,.0f} ({cls._change(current, previous)})")
            lines.append("")

        search_daily = datasets.get("search_console_daily", [])
        if search_daily:
            lines.extend(["## Google Search", ""])
            for metric in ("clicks", "impressions"):
                current = cls._sum(search_daily, metric, "current")
                previous = cls._sum(search_daily, metric, "previous")
                lines.append(f"- {metric}: {current:,.0f} ({cls._change(current, previous)})")
            current_clicks = cls._sum(search_daily, "clicks", "current")
            current_impressions = cls._sum(search_daily, "impressions", "current")
            lines.append(f"- CTR: {(current_clicks / current_impressions * 100) if current_impressions else 0:.2f}%")
            lines.append("")

        editorial_pages = [
            row
            for row in datasets.get("ga4_pages", [])
            if str(row.get("pagePathPlusQueryString", "")).startswith("/blog/")
        ]
        if editorial_pages:
            lines.extend(["## Editorial", ""])
            for metric in ("screenPageViews", "userEngagementDuration", "eventCount", "keyEvents"):
                current = cls._sum(editorial_pages, metric, "current")
                previous = cls._sum(editorial_pages, metric, "previous")
                lines.append(f"- {metric}: {current:,.0f} ({cls._change(current, previous)})")
            lines.append("")
            lines.extend(cls._top_editorial_table(editorial_pages))

        lines.extend(cls._top_table(datasets.get("ga4_landing_pages", []), "landingPagePlusQueryString", "sessions", "Top landing pages"))
        lines.extend(cls._top_table(datasets.get("search_console_queries", []), "query", "clicks", "Top search queries"))
        lines.extend([
            "## Interpretation notes",
            "",
            "- Treat `contact_start` as intent, not a confirmed lead.",
            "- Mark the chosen business events as key events in GA4 after validating them in Realtime/DebugView.",
            "- Compare analytics changes with deploy and content publication dates before changing strategy.",
            "",
        ])
        return "\n".join(lines)

    @staticmethod
    def _top_editorial_table(rows):
        current = [row for row in rows if row.get("period") == "current"]
        current.sort(
            key=lambda row: (
                float(row.get("screenPageViews", 0) or 0),
                float(row.get("userEngagementDuration", 0) or 0),
            ),
            reverse=True,
        )
        if not current:
            return []
        lines = [
            "### Top editorial pages",
            "",
            "| page | views | engagement seconds |",
            "|---|---:|---:|",
        ]
        for row in current[:10]:
            label = str(row.get("pageTitle") or row.get("pagePathPlusQueryString") or "(not set)").replace("|", "\\|")
            views = float(row.get("screenPageViews", 0) or 0)
            engagement = float(row.get("userEngagementDuration", 0) or 0)
            lines.append(f"| {label} | {views:,.0f} | {engagement:,.0f} |")
        lines.append("")
        return lines

    @staticmethod
    def _sum(rows, metric, period):
        total = 0.0
        for row in rows:
            if row.get("period") == period:
                try:
                    total += float(row.get(metric, 0) or 0)
                except (TypeError, ValueError):
                    continue
        return total

    @staticmethod
    def _change(current, previous):
        if previous == 0:
            return "new" if current else "no change"
        return f"{((current - previous) / previous) * 100:+.1f}%"

    @staticmethod
    def _top_table(rows, dimension, metric, title):
        current = [row for row in rows if row.get("period") == "current"]
        current.sort(key=lambda row: float(row.get(metric, 0) or 0), reverse=True)
        if not current:
            return []
        lines = [f"## {title}", "", f"| {dimension} | {metric} |", "|---|---:|"]
        for row in current[:10]:
            label = str(row.get(dimension, "(not set)")).replace("|", "\\|")
            value = float(row.get(metric, 0) or 0)
            lines.append(f"| {label} | {value:,.0f} |")
        lines.append("")
        return lines
