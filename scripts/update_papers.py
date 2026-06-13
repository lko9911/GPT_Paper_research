"""Update data/papers.json from official metadata APIs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from enrich_semantic_scholar import enrich_with_semantic_scholar
from fetch_crossref import fetch_crossref
from fetch_openalex import fetch_openalex, fetch_openalex_by_doi
from summarize import summarize_record

ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
ARCHIVE_PAPERS_PATH = ROOT / "data" / "archive_papers.json"
SITE_META_PATH = ROOT / "data" / "site_meta.json"
QUERIES_PATH = ROOT / "data" / "queries.json"
TARGET_VENUES_PATH = ROOT / "data" / "target_venues.json"
SEED_DOIS_PATH = ROOT / "data" / "seed_dois.json"
DEFAULT_SINCE_YEAR = 2024
CURATED_MIN_SCORE = int(os.getenv("CURATED_MIN_SCORE", "5"))
SEARCH_PER_PAGE = int(os.getenv("SEARCH_PER_PAGE", "200"))
TARGET_VENUE_PER_PAGE = int(os.getenv("TARGET_VENUE_PER_PAGE", "200"))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    today = date.today().isoformat()
    run_started_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    since_year = _since_year()
    existing = _load_json(PAPERS_PATH, []) + _load_json(ARCHIVE_PAPERS_PATH, [])
    queries = _filtered_queries(_load_json(QUERIES_PATH, []))
    target_venues = _load_json(TARGET_VENUES_PATH, [])
    seed_dois = _load_json(SEED_DOIS_PATH, [])
    index = {_dedupe_key(paper): paper for paper in existing}
    allow_openai_in_update = _env_flag("ALLOW_OPENAI_IN_UPDATE")
    if allow_openai_in_update:
        print("ALLOW_OPENAI_IN_UPDATE is enabled. New candidates may call OpenAI before curation.")
    else:
        print("OpenAI summaries are disabled for scheduled metadata updates. Use refresh_openai_summaries.py for curated papers only.")
    added = 0

    for doi in seed_dois:
        print(f"Fetching seed DOI: {doi}")
        candidate = _safe_fetch_openalex_doi(doi)
        if not candidate:
            continue
        if not _is_plausible(candidate, since_year):
            print(f"Seed DOI skipped by relevance/year filter: {doi}")
            continue
        key = _dedupe_key(candidate)
        if key in index:
            _merge_existing_record(index[key], candidate, today)
            continue

        enriched = enrich_with_semantic_scholar(candidate)
        summarized = summarize_record(enriched, allow_openai=allow_openai_in_update)
        paper = _finalize_record(summarized, today)
        index[_dedupe_key(paper)] = paper
        existing.append(paper)
        added += 1
        print(f"Added seed DOI: {paper['title']}")

    for query in queries:
        print(f"Searching: {query}")
        candidates: list[dict[str, Any]] = []
        if _env_flag("SKIP_OPENALEX"):
            print("Skipping OpenAlex search because SKIP_OPENALEX is enabled.")
        else:
            candidates.extend(_safe_fetch(fetch_openalex, query, since_year, per_page=SEARCH_PER_PAGE))
        candidates.extend(_safe_fetch(fetch_crossref, query, since_year, rows=SEARCH_PER_PAGE))

        for candidate in candidates:
            if not _is_plausible(candidate, since_year):
                continue
            key = _dedupe_key(candidate)
            if key in index:
                _merge_existing_record(index[key], candidate, today)
                continue

            enriched = enrich_with_semantic_scholar(candidate)
            summarized = summarize_record(enriched, allow_openai=allow_openai_in_update)
            paper = _finalize_record(summarized, today)
            index[_dedupe_key(paper)] = paper
            existing.append(paper)
            added += 1
            print(f"Added: {paper['title']}")

    if _env_flag("SKIP_TARGET_VENUES"):
        print("Skipping target venue searches because SKIP_TARGET_VENUES is enabled.")
    else:
        for target in target_venues:
            venue_name = target.get("name", "Unknown venue")
            source_id = target.get("openalex_source_id", "")
            if not source_id:
                continue
            print(f"Searching target venue: {venue_name}")
            for query in queries:
                candidates = _safe_fetch_openalex_source(query, source_id, since_year)
                for candidate in candidates:
                    if not _is_plausible(candidate, since_year):
                        continue
                    key = _dedupe_key(candidate)
                    if key in index:
                        _merge_existing_record(index[key], candidate, today)
                        continue

                    enriched = enrich_with_semantic_scholar(candidate)
                    summarized = summarize_record(enriched, allow_openai=allow_openai_in_update)
                    paper = _finalize_record(summarized, today)
                    index[_dedupe_key(paper)] = paper
                    existing.append(paper)
                    added += 1
                    print(f"Added from {venue_name}: {paper['title']}")

    cleaned = [_strip_transient(paper) for paper in existing]
    curated, archive, split_stats = _split_curated_archive(cleaned)
    _write_json_if_changed(PAPERS_PATH, curated)
    _write_json_if_changed(ARCHIVE_PAPERS_PATH, archive)
    _write_json_if_changed(
        SITE_META_PATH,
        {
            "last_run_at_utc": run_started_at,
            "last_run_date": today,
            "paper_count": len(curated),
            "curated_count": len(curated),
            "raw_candidate_count": len(cleaned),
            "archived_count": len(archive),
            "hidden_low_relevance_count": split_stats["low_relevance"],
            "duplicate_archived_count": split_stats["duplicate_title"],
            "papers_added": added,
            "raw_records_added": added,
            "since_year": since_year,
            "curated_min_score": CURATED_MIN_SCORE,
            "sources": ["OpenAlex", "Crossref", "Semantic Scholar optional"],
        },
    )
    print(f"Update complete. Added {added} new records. Curated {len(curated)} papers; archived {len(archive)} of {len(cleaned)} raw candidates.")


def _safe_fetch(fetcher, query: str, since_year: int, **kwargs) -> list[dict[str, Any]]:
    try:
        return fetcher(query, from_year=since_year, **kwargs)
    except Exception as exc:
        print(f"Fetch failed for {fetcher.__name__} / '{query}': {exc}")
        return []


def _filtered_queries(queries: list[str]) -> list[str]:
    query_filter = os.getenv("UPDATE_QUERY_FILTER", "").strip()
    if not query_filter:
        return queries
    needles = [part.strip().lower() for part in query_filter.split(",") if part.strip()]
    if not needles:
        return queries
    filtered = [query for query in queries if any(needle in query.lower() for needle in needles)]
    print(f"UPDATE_QUERY_FILTER selected {len(filtered)} of {len(queries)} queries.")
    return filtered


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _safe_fetch_openalex_source(query: str, source_id: str, since_year: int) -> list[dict[str, Any]]:
    try:
        return fetch_openalex(query, per_page=TARGET_VENUE_PER_PAGE, from_year=since_year, source_id=source_id)
    except Exception as exc:
        print(f"Venue fetch failed for OpenAlex source {source_id} / '{query}': {exc}")
        return []


def _safe_fetch_openalex_doi(doi: str) -> dict[str, Any] | None:
    try:
        return fetch_openalex_by_doi(doi)
    except Exception as exc:
        print(f"DOI fetch failed for {doi}: {exc}")
        return None


def _is_plausible(record: dict[str, Any], since_year: int) -> bool:
    title = record.get("title", "")
    if not title or title == "Untitled":
        return False
    if _is_non_research_output(title):
        return False
    raw_year = record.get("year")
    year = _safe_year(raw_year, log=False)
    if raw_year and year is None:
        return False
    if year and year < since_year:
        return False
    text = f"{title} {record.get('_abstract', '')}".lower()
    additive_terms = [
        "additive manufacturing",
        "3d printing",
        "3-d printing",
        "4d printing",
        "4-d printing",
        "four-dimensional printing",
        "printed",
        "printing",
        "direct ink writing",
        "diw",
        "fused deposition",
        "fdm",
        "material extrusion",
        "materials discovery",
        "materials synthesis",
        "digital twin",
        "digital twins",
        "cyber-physical",
        "cyber physical",
    ]
    topic_terms = [
        "multi-material",
        "multimaterial",
        "functionally graded",
        "graded material",
        "liquid crystal elastomer",
        "liquid-crystal elastomer",
        " lce ",
        "4d print",
        "shape morph",
        "shape-morph",
        "shape changing",
        "stimuli-responsive",
        "stimulus-responsive",
        "soft actuator",
        "metamaterial",
        "toolpath",
        "computational design",
        "material distribution",
        "material switching",
        "purge",
        "path planning",
        "digital material",
        "self-driving lab",
        "self driving lab",
        "self-driving laboratory",
        "autonomous laboratory",
        "autonomous lab",
        "autonomous experimentation",
        "autonomous experiment",
        "closed-loop experimentation",
        "closed-loop experiment",
        "robot scientist",
        "active learning",
        "bayesian optimization",
        "digital twin",
        "digital twins",
        "cyber-physical",
        "cyber physical",
        "process twin",
        "machine twin",
    ]
    return any(term in text for term in additive_terms) and any(term in text for term in topic_terms)


def _is_non_research_output(title: str) -> bool:
    normalized_title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", title)).strip().lower()
    blocked_prefixes = (
        "review for ",
        "decision letter for ",
        "author response for ",
        "response to reviewers",
        "peer review for ",
        "title pending",
    )
    if normalized_title.startswith(blocked_prefixes):
        return True
    blocked_fragments = (
        "llm guided hypothesis generation in self-driving lab",
        "(invited)",
    )
    return any(fragment in normalized_title for fragment in blocked_fragments)


def _split_curated_archive(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        key = _normalize_title(record.get("title", "")) or _dedupe_key(record)
        groups.setdefault(key, []).append(record)

    curated: list[dict[str, Any]] = []
    archive: list[dict[str, Any]] = []
    stats = {"low_relevance": 0, "duplicate_title": 0}

    for group in groups.values():
        ranked = sorted(group, key=_curation_rank, reverse=True)
        winner = ranked[0]
        if _is_curated_candidate(winner):
            curated.append(_without_archive_reason(winner))
            for duplicate in ranked[1:]:
                archive.append(_with_archive_reason(duplicate, "duplicate_title"))
                stats["duplicate_title"] += 1
        else:
            for record in ranked:
                archive.append(_with_archive_reason(record, "low_relevance"))
                stats["low_relevance"] += 1

    curated.sort(key=_sort_key, reverse=True)
    archive.sort(key=_sort_key, reverse=True)
    return curated, archive, stats


def _is_curated_candidate(record: dict[str, Any]) -> bool:
    return int(record.get("relevance_score") or 0) >= CURATED_MIN_SCORE and not _is_non_research_output(record.get("title", ""))


def _curation_rank(record: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
    venue = record.get("venue") or ""
    doi = record.get("doi") or ""
    return (
        int(record.get("relevance_score") or 0),
        0 if _is_repository_like(venue, doi) else 1,
        1 if venue else 0,
        1 if doi else 0,
        int(record.get("year") or 0),
        record.get("title") or "",
    )


def _is_repository_like(venue: str, doi: str = "") -> bool:
    text = f"{venue} {doi}".lower()
    return any(
        marker in text
        for marker in (
            "figshare",
            "zenodo",
            "arxiv",
            "chemrxiv",
            "research square",
            "ssrn",
            "techrxiv",
            "repository",
        )
    )


def _with_archive_reason(record: dict[str, Any], reason: str) -> dict[str, Any]:
    archived = dict(record)
    archived["archive_reason"] = reason
    return archived


def _without_archive_reason(record: dict[str, Any]) -> dict[str, Any]:
    curated = dict(record)
    curated.pop("archive_reason", None)
    return curated


def _sort_key(record: dict[str, Any]) -> tuple[int, int, str]:
    return (int(record.get("year") or 0), int(record.get("relevance_score") or 0), record.get("title") or "")


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
        "ai_summary_en": record.get("ai_summary_en", ""),
        "summary_provider": record.get("_summary_provider", "fallback"),
        "openai_summary_applied": record.get("_summary_provider") == "openai",
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


def _merge_existing_record(existing: dict[str, Any], candidate: dict[str, Any], today: str) -> None:
    _merge_source(existing, candidate, today)
    if not _should_refresh_generic_summary(existing, candidate):
        return

    refresh_record = dict(existing)
    refresh_record.update({key: value for key, value in candidate.items() if value})
    summarized = summarize_record(refresh_record, allow_openai=False)
    for key in ("ai_summary_ko", "ai_summary_en", "relevance_note_ko", "relevance_score", "tags", "categories"):
        if summarized.get(key):
            existing[key] = summarized[key]
    existing["summary_provider"] = "fallback"
    existing["openai_summary_applied"] = False
    existing["abstract_used_for_summary"] = bool(candidate.get("_abstract"))


def _should_refresh_generic_summary(existing: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if not candidate.get("_abstract"):
        return False
    summary = str(existing.get("ai_summary_ko") or "")
    generic_markers = [
        "제목과 공개 메타데이터",
        "공개 메타데이터를 기준",
        "public metadata",
        "metadata and curated topic signals",
    ]
    return any(marker in summary for marker in generic_markers)


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
    if year < 1900 or year > current_year:
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
