"""Collect AML recommendation candidates without using OpenAI as a search engine.

External AML candidate discovery is intentionally Crossref-only and uses plain
keyword queries, without venue-specific filtering. OpenAI is used later only for
embedding-based scoring when the private cache needs new vectors.
"""

from __future__ import annotations

import os
from typing import Any

from aml_common import (
    CANDIDATE_POOL_PATH,
    PAPERS_PATH,
    candidate_key,
    load_json,
    now_iso,
    paper_text,
    write_json,
)
from fetch_crossref import fetch_crossref

DEFAULT_QUERIES = [
    "multi-material additive manufacturing",
    "functionally graded additive manufacturing",
    "digital material filament",
    "blended FDM",
    "material distribution additive manufacturing",
    "toolpath multi-material 3D printing",
    "liquid crystal elastomer 4D printing",
    "hydrogel 4D printing",
    "soft robotics 3D printing sensor",
    "projection micro stereolithography metamaterial",
]


def collect_candidates(mode: str = "score_existing", max_candidates: int = 200) -> dict[str, Any]:
    candidates: dict[str, dict[str, Any]] = {}
    _add_existing_pool(candidates, PAPERS_PATH, "existing_keyword_pool")
    if mode in {"collect_and_score", "full_refresh"}:
        _add_recent_api_candidates(candidates, max_candidates=max_candidates)
    selected = list(candidates.values())[: max(1, max_candidates)]
    payload = {
        "updated_at": now_iso(),
        "mode": mode,
        "candidate_count": len(selected),
        "candidates": selected,
    }
    write_json(CANDIDATE_POOL_PATH, payload)
    return payload


def _add_existing_pool(candidates: dict[str, dict[str, Any]], path, route: str) -> None:
    for paper in load_json(path, []):
        record = _normalize_candidate(paper, route)
        if not _has_aml_signal(record):
            continue
        _merge_candidate(candidates, record)


def _add_recent_api_candidates(candidates: dict[str, dict[str, Any]], max_candidates: int) -> None:
    since_year = int(os.getenv("AML_SINCE_YEAR", "2024"))
    per_query = max(5, min(30, max_candidates // max(1, len(DEFAULT_QUERIES))))
    for query in DEFAULT_QUERIES:
        try:
            for paper in fetch_crossref(query, rows=per_query, from_year=since_year):
                record = _normalize_candidate(paper, "crossref_keyword_search")
                record["source_api"] = "Crossref"
                if _has_aml_signal(record):
                    _merge_candidate(candidates, record)
        except Exception as exc:
            print(f"Candidate fetch skipped for Crossref query '{query}': {exc}")


def _normalize_candidate(paper: dict[str, Any], route: str) -> dict[str, Any]:
    doi = paper.get("doi", "")
    title = paper.get("title", "")
    venue = paper.get("venue") or paper.get("journal", "")
    year = paper.get("year")
    url = paper.get("url") or (f"https://doi.org/{doi}" if doi else "")
    abstract = paper.get("_abstract", "") or paper.get("abstract", "")
    return {
        "id": candidate_key(paper),
        "title": title,
        "doi": doi,
        "journal": venue,
        "venue": venue,
        "year": year,
        "authors": paper.get("authors", []) or [],
        "author_details": paper.get("author_details", []) or [],
        "corresponding_authors": paper.get("corresponding_authors", []) or [],
        "corresponding_author_available": bool(paper.get("corresponding_authors")),
        "url": url,
        "citation": paper.get("citation", ""),
        "abstract": abstract,
        "tags": paper.get("tags", []) or [],
        "categories": paper.get("categories", []) or [],
        "discovery_routes": [route],
        "source": paper.get("source", []) or [],
    }


def _merge_candidate(candidates: dict[str, dict[str, Any]], record: dict[str, Any]) -> None:
    key = record["id"]
    existing = candidates.get(key)
    if not existing:
        candidates[key] = record
        return
    existing_routes = set(existing.get("discovery_routes", []))
    existing_routes.update(record.get("discovery_routes", []))
    existing["discovery_routes"] = sorted(existing_routes)
    for field in ("abstract", "journal", "venue", "url", "doi", "author_details", "corresponding_authors"):
        if not existing.get(field) and record.get(field):
            existing[field] = record[field]
    existing["corresponding_author_available"] = bool(existing.get("corresponding_authors"))


def _has_aml_signal(record: dict[str, Any]) -> bool:
    text = paper_text(record).lower()
    signals = [
        "multi-material",
        "multimaterial",
        "functionally graded",
        "digital material",
        "dm filament",
        "blended fdm",
        "fdm",
        "fff",
        "material extrusion",
        "toolpath",
        "material switching",
        "4d printing",
        "soft robotic",
        "metamaterial",
        "hydrogel",
        "liquid crystal elastomer",
        "sensor",
        "projection micro",
        "stereolithography",
    ]
    return any(signal in text for signal in signals)


if __name__ == "__main__":
    mode = os.getenv("AML_MODE", "score_existing")
    max_candidates = int(os.getenv("AML_MAX_CANDIDATES", "200"))
    result = collect_candidates(mode=mode, max_candidates=max_candidates)
    print(f"AML candidates collected: {result['candidate_count']}")
