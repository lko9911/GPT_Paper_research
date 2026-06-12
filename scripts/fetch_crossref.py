"""Fetch paper metadata from Crossref without publisher crawling."""

from __future__ import annotations

import os
import re
import time
from html import unescape
from typing import Any
from urllib.parse import quote

import requests

CROSSREF_API = "https://api.crossref.org/works"


def fetch_crossref(query: str, rows: int = 20, from_year: int | None = None) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "query.bibliographic": query,
        "rows": min(rows, 1000),
        "sort": "published",
        "order": "desc",
        "cursor": "*",
    }
    contact_email = os.getenv("CONTACT_EMAIL")
    if contact_email:
        params["mailto"] = contact_email
    if from_year:
        params["filter"] = f"from-pub-date:{from_year}-01-01"

    works: list[dict[str, Any]] = []
    seen_cursors: set[str] = set()
    max_pages = _max_pages()
    page = 0

    while True:
        response = requests.get(CROSSREF_API, params=params, headers=_headers(), timeout=30)
        response.raise_for_status()
        message = response.json().get("message", {})
        items = message.get("items", [])
        works.extend(_normalize_work(item) for item in items)
        page += 1
        time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

        next_cursor = message.get("next-cursor")
        if not items or not next_cursor or next_cursor in seen_cursors:
            break
        if max_pages and page >= max_pages:
            break
        seen_cursors.add(next_cursor)
        params["cursor"] = next_cursor

    return works


def _normalize_work(item: dict[str, Any]) -> dict[str, Any]:
    doi = _clean_doi(item.get("DOI"))
    title = _first(item.get("title")) or "Untitled"
    venue = _first(item.get("container-title")) or _first(item.get("event", {}).get("name")) or ""
    year = _published_year(item)
    authors = []
    for author in item.get("author", [])[:12]:
        given = author.get("given", "")
        family = author.get("family", "")
        name = " ".join(part for part in [given, family] if part).strip()
        if name:
            authors.append(name)

    abstract = _strip_markup(item.get("abstract") or "")
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": doi,
        "url": f"https://doi.org/{quote(doi)}" if doi else item.get("URL", ""),
        "source": ["Crossref"],
        "_abstract": abstract,
    }


def _published_year(item: dict[str, Any]) -> int | None:
    for key in ["published-print", "published-online", "published", "issued"]:
        parts = (item.get(key) or {}).get("date-parts") or []
        if parts and parts[0]:
            return parts[0][0]
    return None


def _first(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value) if value else ""


def _strip_markup(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def _clean_doi(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    value = re.sub(r"(\.pdf|/pdf)$", "", value)
    return value


def _headers() -> dict[str, str]:
    contact = os.getenv("CONTACT_EMAIL") or os.getenv("GITHUB_ACTOR") or "github-actions"
    return {
        "User-Agent": f"awesome-mmam-paper-tracker/1.0 ({contact})",
        "Accept": "application/json",
    }


def _max_pages() -> int:
    value = os.getenv("CROSSREF_MAX_PAGES", "0")
    try:
        return max(0, int(value))
    except ValueError:
        return 0
