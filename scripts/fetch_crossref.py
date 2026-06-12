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
        "rows": rows,
        "sort": "published",
        "order": "desc",
    }
    contact_email = os.getenv("CONTACT_EMAIL")
    if contact_email:
        params["mailto"] = contact_email
    if from_year:
        params["filter"] = f"from-pub-date:{from_year}-01-01"

    response = requests.get(CROSSREF_API, params=params, headers=_headers(), timeout=30)
    response.raise_for_status()
    time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

    return [_normalize_work(item) for item in response.json().get("message", {}).get("items", [])]


def _normalize_work(item: dict[str, Any]) -> dict[str, Any]:
    doi = (item.get("DOI") or "").lower()
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


def _headers() -> dict[str, str]:
    contact = os.getenv("CONTACT_EMAIL") or os.getenv("GITHUB_ACTOR") or "github-actions"
    return {
        "User-Agent": f"awesome-mmam-paper-tracker/1.0 ({contact})",
        "Accept": "application/json",
    }
