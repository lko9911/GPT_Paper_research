"""Optional Semantic Scholar enrichment.

This module is used only when SEMANTIC_SCHOLAR_API_KEY is available. It does
not download PDFs and it does not persist raw abstracts.
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper"


def enrich_with_semantic_scholar(record: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    doi = record.get("doi")
    if not api_key or not doi:
        return record

    fields = "title,year,venue,authors,abstract,url,externalIds"
    url = f"{SEMANTIC_SCHOLAR_API}/DOI:{doi}"
    response = requests.get(
        url,
        params={"fields": fields},
        headers={"x-api-key": api_key, "User-Agent": "awesome-mmam-paper-tracker/1.0"},
        timeout=30,
    )
    if response.status_code == 404:
        return record
    response.raise_for_status()
    time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

    payload = response.json()
    if payload.get("venue") and not record.get("venue"):
        record["venue"] = payload["venue"]
    if payload.get("year") and not record.get("year"):
        record["year"] = payload["year"]
    if payload.get("authors") and not record.get("authors"):
        record["authors"] = [author.get("name", "") for author in payload["authors"] if author.get("name")]
    if payload.get("abstract") and not record.get("_abstract"):
        record["_abstract"] = payload["abstract"]
    if "Semantic Scholar" not in record.setdefault("source", []):
        record["source"].append("Semantic Scholar")
    return record
