"""Update data/papers.json from official metadata APIs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from enrich_semantic_scholar import enrich_with_semantic_scholar
from fetch_crossref import fetch_crossref
from fetch_openalex import fetch_openalex
from summarize import summarize_record

ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
QUERIES_PATH = ROOT / "data" / "queries.json"
DEFAULT_SINCE_YEAR = 2024


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    today = date.today().isoformat()
    since_year = _since_year()
    existing = _load_json(PAPERS_PATH, [])
    queries = _load_json(QUERIES_PATH, [])
    index = {_dedupe_key(paper): paper for paper in existing}
    added = 0

    for query in queries:
        print(f"Searching: {query}")
        candidates: list[dict[str, Any]] = []
        candidates.extend(_safe_fetch(fetch_openalex, query, since_year))
        candidates.extend(_safe_fetch(fetch_crossref, query, since_year))

        for candidate in candidates:
            if not _is_plausible(candidate, since_year):
                continue
            key = _dedupe_key(candidate)
            if key in index:
                _merge_source(index[key], candidate, today)
                continue

            enriched = enrich_with_semantic_scholar(candidate)
            summarized = summarize_record(enriched)
            paper = _finalize_record(summarized, today)
            index[_dedupe_key(paper)] = paper
            existing.append(paper)
            added += 1
            print(f"Added: {paper['title']}")

    cleaned = [_strip_transient(paper) for paper in existing]
    cleaned.sort(key=lambda paper: (paper.get("year") or 0, paper.get("relevance_score") or 0, paper.get("title") or ""), reverse=True)
    _write_json_if_changed(PAPERS_PATH, cleaned)
    print(f"Update complete. Added {added} new papers. Total {len(cleaned)} papers.")


def _safe_fetch(fetcher, query: str, since_year: int) -> list[dict[str, Any]]:
    try:
        return fetcher(query, from_year=since_year)
    except Exception as exc:
        print(f"Fetch failed for {fetcher.__name__} / '{query}': {exc}")
        return []


def _is_plausible(record: dict[str, Any], since_year: int) -> bool:
    title = record.get("title", "")
    if not title or title == "Untitled":
        return False
    year = _safe_year(record.get("year"), log=False)
    if year and year < since_year:
        return False
    text = f"{title} {record.get('_abstract', '')}".lower()
    additive_terms = ["additive manufacturing", "3d printing", "fused deposition", "fdm", "material extrusion"]
    topic_terms = [
        "multi-material",
        "multimaterial",
        "functionally graded",
        "graded material",
        "toolpath",
        "computational design",
        "material distribution",
        "material switching",
        "purge",
        "path planning",
        "digital material",
    ]
    return any(term in text for term in additive_terms) and any(term in text for term in topic_terms)


def _since_year() -> int:
    value = os.getenv("SINCE_YEAR", str(DEFAULT_SINCE_YEAR))
    try:
        return int(value)
    except ValueError:
        print(f"Invalid SINCE_YEAR={value!r}; using {DEFAULT_SINCE_YEAR}")
        return DEFAULT_SINCE_YEAR


def _finalize_record(record: dict[str, Any], today: str) -> dict[str, Any]:
    doi = (record.get("doi") or "").lower()
    paper_id = doi or _title_hash(record.get("title", ""))
    url = record.get("url") or (f"https://doi.org/{doi}" if doi else "")
    year = _safe_year(record.get("year"))
    return {
        "id": paper_id,
        "title": record.get("title", "Untitled"),
        "authors": record.get("authors", []),
        "year": year,
        "venue": record.get("venue", ""),
        "doi": doi,
        "url": url,
        "source": sorted(set(record.get("source", []))),
        "categories": record.get("categories", ["다중재료 적층제조"])[:2],
        "tags": record.get("tags", [])[:6],
        "relevance_score": int(record.get("relevance_score", 5)),
        "ai_summary_ko": record.get("ai_summary_ko", ""),
        "relevance_note_ko": record.get("relevance_note_ko", ""),
        "abstract_used_for_summary": bool(record.get("_abstract")),
        "raw_abstract_displayed": False,
        "pdf_stored": False,
        "first_added": today,
        "last_updated": today,
    }


def _merge_source(existing: dict[str, Any], candidate: dict[str, Any], today: str) -> None:
    sources = set(existing.get("source", []))
    sources.update(candidate.get("source", []))
    existing["source"] = sorted(sources)
    if not existing.get("doi") and candidate.get("doi"):
        existing["doi"] = candidate["doi"]
        existing["url"] = candidate.get("url", existing.get("url", ""))
    existing["last_updated"] = today


def _dedupe_key(record: dict[str, Any]) -> str:
    doi = (record.get("doi") or "").lower().strip()
    if doi:
        return f"doi:{doi}"
    return f"title:{_normalize_title(record.get('title', ''))}"


def _normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def _title_hash(title: str) -> str:
    return hashlib.sha256(_normalize_title(title).encode("utf-8")).hexdigest()[:16]


def _strip_transient(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def _safe_year(value: Any, log: bool = True) -> int | None:
    try:
        year = int(value)
    except (TypeError, ValueError):
        return None
    current_year = date.today().year
    if year < 1900 or year > current_year + 1:
        if log:
            print(f"Discarding implausible publication year: {year}")
        return None
    return year


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json_if_changed(path: Path, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old == text:
        print(f"No changes in {path.relative_to(ROOT)}")
        return
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
