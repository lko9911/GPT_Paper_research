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
    return _fetch_crossref_works(query=query, rows=rows, from_year=from_year)


def fetch_crossref_by_issn_query(
    query: str,
    issn: str,
    rows: int = 20,
    from_year: int | None = None,
) -> list[dict[str, Any]]:
    max_pages = _max_pages_from_env("CROSSREF_VENUE_MAX_PAGES", default=1)
    return _fetch_crossref_works(query=query, rows=rows, from_year=from_year, issn=issn, max_pages=max_pages)


def _fetch_crossref_works(
    query: str,
    rows: int = 20,
    from_year: int | None = None,
    issn: str | None = None,
    max_pages: int | None = None,
) -> list[dict[str, Any]]:
    sort = os.getenv("CROSSREF_SORT", "relevance")
    params: dict[str, Any] = {
        "query.bibliographic": query,
        "rows": min(rows, 1000),
        "sort": sort,
        "cursor": "*",
    }
    if sort != "relevance":
        params["order"] = os.getenv("CROSSREF_ORDER", "desc")
    contact_email = os.getenv("CONTACT_EMAIL")
    if contact_email:
        params["mailto"] = contact_email
    filters = []
    if from_year:
        filters.append(f"from-pub-date:{from_year}-01-01")
    if issn:
        filters.append(f"issn:{issn}")
    if filters:
        params["filter"] = ",".join(filters)

    works: list[dict[str, Any]] = []
    seen_cursors: set[str] = set()
    max_pages = _max_pages() if max_pages is None else max_pages
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


def fetch_crossref_by_doi(doi: str) -> dict[str, Any] | None:
    clean_doi = _clean_doi(doi)
    if not clean_doi:
        return None
    contact_email = os.getenv("CONTACT_EMAIL")
    params = {"mailto": contact_email} if contact_email else None
    response = requests.get(f"{CROSSREF_API}/{quote(clean_doi)}", params=params, headers=_headers(), timeout=30)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    item = response.json().get("message", {})
    if not item:
        return None
    time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))
    return _normalize_work(item)


def _normalize_work(item: dict[str, Any]) -> dict[str, Any]:
    doi = _clean_doi(item.get("DOI"))
    title = _clean_markup_text(_first(item.get("title"))) or "Untitled"
    venue = _clean_markup_text(_first(item.get("container-title")) or _first(item.get("event", {}).get("name")) or "")
    year = _published_year(item)
    author_details = _normalize_authors(item.get("author", []))
    authors = [author["name"] for author in author_details[:12] if author.get("name")]
    corresponding_authors = [
        author for author in author_details if author.get("is_corresponding")
    ]

    abstract = _strip_markup(item.get("abstract") or "")
    issn = item.get("ISSN") or []
    return {
        "title": title,
        "authors": authors,
        "author_details": author_details,
        "corresponding_authors": corresponding_authors,
        "corresponding_author_available": bool(corresponding_authors),
        "year": year,
        "venue": venue,
        "doi": doi,
        "url": f"https://doi.org/{quote(doi)}" if doi else item.get("URL", ""),
        "source": ["Crossref"],
        "metadata_source": "crossref",
        "crossref_type": item.get("type", ""),
        "issn": issn,
        "issn_l": item.get("ISSN-L", ""),
        "publisher": item.get("publisher", ""),
        "_abstract": abstract,
    }


def _normalize_authors(authors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    total = len(authors)
    for index, author in enumerate(authors[:100], start=1):
        given = author.get("given", "")
        family = author.get("family", "")
        name = " ".join(part for part in [given, family] if part).strip()
        if not name:
            name = author.get("name", "")
        if not name:
            continue
        affiliations = []
        for affiliation in author.get("affiliation") or []:
            name_value = affiliation.get("name")
            if name_value:
                affiliations.append({"name": name_value})
        details.append(
            {
                "name": name,
                "orcid": author.get("ORCID", ""),
                "position": author.get("sequence") or _fallback_author_position(index, total),
                "is_corresponding": _is_crossref_corresponding_author(author),
                "institutions": affiliations,
                "raw_affiliation_strings": [item["name"] for item in affiliations],
            }
        )
    return details


def _fallback_author_position(index: int, total: int) -> str:
    if index == 1:
        return "first"
    if index == total:
        return "last"
    return "middle"


def _is_crossref_corresponding_author(author: dict[str, Any]) -> bool:
    if bool(author.get("corresponding") or author.get("corresponding-author")):
        return True
    role = str(author.get("role") or author.get("contributor_role") or "").lower()
    return "correspond" in role


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


def _clean_markup_text(value: str) -> str:
    text = unescape(str(value or "")).replace("\xa0", " ")
    text = re.sub(r"</?(?:scp|i|italic|em|b|strong)\b[^>]*>", "", text, flags=re.I)
    text = re.sub(r"\s*</?(?:sub|sup)\b[^>]*>\s*", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[\u2010-\u2015\u2212]", "-", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([),.;:])", r"\1", text)
    text = re.sub(r"([(])\s+", r"\1", text)
    text = re.sub(r"(?<=\w)\s*-\s*(?=\w)", "-", text)
    return text


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
    return _max_pages_from_env("CROSSREF_MAX_PAGES", default=0)


def _max_pages_from_env(name: str, default: int = 0) -> int:
    value = os.getenv(name, str(default))
    try:
        return max(0, int(value))
    except ValueError:
        return default
