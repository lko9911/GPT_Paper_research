"""Fetch paper metadata from OpenAlex without downloading PDFs."""

from __future__ import annotations

import os
import re
import time
from typing import Any
from urllib.parse import quote

import requests

OPENALEX_API = "https://api.openalex.org/works"


def fetch_openalex(
    query: str,
    per_page: int = 20,
    from_year: int | None = None,
    source_id: str | None = None,
) -> list[dict[str, Any]]:
    """Search OpenAlex and return normalized paper records.

    Abstract text is returned only in the transient "_abstract" field so the
    update pipeline can summarize it. The field is stripped before persistence.
    """

    params: dict[str, Any] = {
        "search": query,
        "per-page": min(per_page, 200),
        "sort": "publication_date:desc",
        "cursor": "*",
    }
    contact_email = os.getenv("CONTACT_EMAIL")
    if contact_email:
        params["mailto"] = contact_email
    filters = []
    if from_year:
        filters.append(f"from_publication_date:{from_year}-01-01")
    if source_id:
        filters.append(f"primary_location.source.id:{source_id}")
    if filters:
        params["filter"] = ",".join(filters)

    works: list[dict[str, Any]] = []
    seen_cursors: set[str] = set()
    max_pages = _max_pages()
    page = 0

    while True:
        response = _get_with_retry(OPENALEX_API, params=params)
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results", [])
        works.extend(_normalize_work(item) for item in results)
        page += 1
        time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

        next_cursor = (payload.get("meta") or {}).get("next_cursor")
        if not results or not next_cursor or next_cursor in seen_cursors:
            break
        if max_pages and page >= max_pages:
            break
        seen_cursors.add(next_cursor)
        params["cursor"] = next_cursor

    return works


def fetch_openalex_by_doi(doi: str) -> dict[str, Any] | None:
    doi = _clean_doi(doi)
    if not doi:
        return None
    response = _get_with_retry(f"{OPENALEX_API}/doi:{doi}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))
    return _normalize_work(response.json())


def _normalize_work(item: dict[str, Any]) -> dict[str, Any]:
    doi = _clean_doi(item.get("doi"))
    title = item.get("title") or item.get("display_name") or "Untitled"
    venue = ""
    primary_location = item.get("primary_location") or {}
    source = primary_location.get("source") or {}
    if source:
        venue = source.get("display_name") or ""
    if not venue:
        venue = (item.get("host_venue") or {}).get("display_name") or ""

    authors = []
    for authorship in item.get("authorships", [])[:12]:
        author = authorship.get("author") or {}
        if author.get("display_name"):
            authors.append(author["display_name"])

    abstract = _decode_inverted_abstract(item.get("abstract_inverted_index"))
    url = f"https://doi.org/{quote(doi)}" if doi else item.get("id", "")

    return {
        "title": title,
        "authors": authors,
        "year": item.get("publication_year"),
        "venue": venue,
        "doi": doi,
        "url": url,
        "source": ["OpenAlex"],
        "_abstract": abstract,
    }


def _decode_inverted_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, indexes in index.items():
        for position in indexes:
            positions.append((position, word))
    return " ".join(word for _, word in sorted(positions))


def _clean_doi(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()
    if value.lower().startswith("https://doi.org/"):
        value = value[16:]
    if value.lower().startswith("http://dx.doi.org/"):
        value = value[18:]
    value = value.lower().strip()
    value = re.sub(r"(\.pdf|/pdf)$", "", value)
    return value


def _headers() -> dict[str, str]:
    contact = os.getenv("CONTACT_EMAIL") or os.getenv("GITHUB_ACTOR") or "github-actions"
    return {
        "User-Agent": f"awesome-mmam-paper-tracker/1.0 ({contact})",
        "Accept": "application/json",
    }


def _get_with_retry(url: str, params: dict[str, Any] | None = None) -> requests.Response:
    retries = int(os.getenv("OPENALEX_RETRIES", "3"))
    base_sleep = float(os.getenv("API_SLEEP_SECONDS", "0.2"))
    for attempt in range(retries + 1):
        response = requests.get(url, params=params, headers=_headers(), timeout=30)
        if response.status_code != 429:
            response.raise_for_status()
            return response
        retry_after = response.headers.get("Retry-After")
        if attempt >= retries:
            response.raise_for_status()
        wait = float(retry_after) if retry_after and retry_after.isdigit() else base_sleep * (2 ** attempt + 1)
        print(f"OpenAlex rate limited; retrying in {wait:.1f}s")
        time.sleep(wait)
    raise RuntimeError("OpenAlex retry loop exhausted")


def _max_pages() -> int:
    value = os.getenv("OPENALEX_MAX_PAGES", "0")
    try:
        return max(0, int(value))
    except ValueError:
        return 0
