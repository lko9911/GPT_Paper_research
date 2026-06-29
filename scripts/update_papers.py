"""Update data/papers.json from official metadata APIs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import UTC, date, datetime
from html import unescape
from pathlib import Path
from typing import Any

from enrich_semantic_scholar import enrich_with_semantic_scholar
from fetch_crossref import fetch_crossref, fetch_crossref_by_doi
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
        if not _is_plausible_seed(candidate, since_year):
            print(f"Seed DOI skipped by relevance/year filter: {doi}")
            continue
        _mark_curation_priority(candidate)
        key = _dedupe_key(candidate)
        if key in index:
            _merge_existing_record(index[key], candidate, today)
            _mark_curation_priority(index[key])
            continue

        enriched = _crosscheck_openalex_metadata(enrich_with_semantic_scholar(candidate))
        summarized = summarize_record(enriched, allow_openai=allow_openai_in_update)
        _mark_curation_priority(summarized)
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

            enriched = _crosscheck_openalex_metadata(enrich_with_semantic_scholar(candidate))
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

                    enriched = _crosscheck_openalex_metadata(enrich_with_semantic_scholar(candidate))
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
            "hidden_low_venue_trust_count": split_stats.get("low_venue_trust", 0),
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


def _safe_fetch_crossref_doi(doi: str) -> dict[str, Any] | None:
    try:
        return fetch_crossref_by_doi(doi)
    except Exception as exc:
        print(f"Crossref DOI fetch failed for {doi}: {exc}")
        return None


def _crosscheck_openalex_metadata(record: dict[str, Any]) -> dict[str, Any]:
    """Use OpenAlex DOI metadata to fill author details for Crossref-only records."""

    if _env_flag("SKIP_OPENALEX"):
        return record
    doi = record.get("doi")
    if not doi:
        return record
    if record.get("_openalex_crosscheck_attempted"):
        return record
    record["_openalex_crosscheck_attempted"] = True
    sources = set(record.get("source", []))
    needs_crosscheck = (
        "OpenAlex" not in sources
        or not record.get("author_details")
        or not record.get("openalex_work_id")
    )
    if not needs_crosscheck:
        return record
    openalex_record = _safe_fetch_openalex_doi(str(doi))
    if not openalex_record:
        return record
    _merge_openalex_crosscheck(record, openalex_record)
    return record


def _merge_openalex_crosscheck(record: dict[str, Any], openalex_record: dict[str, Any]) -> None:
    sources = set(record.get("source", []))
    sources.update(openalex_record.get("source", []))
    record["source"] = sorted(sources)
    for key in (
        "author_details",
        "corresponding_authors",
        "openalex_work_id",
        "openalex_source_id",
        "venue_metrics",
    ):
        if openalex_record.get(key) and not record.get(key):
            record[key] = openalex_record[key]
    for key in ("authors", "venue", "year", "url", "_abstract"):
        if openalex_record.get(key) and not record.get(key):
            record[key] = openalex_record[key]
    record["corresponding_author_available"] = bool(record.get("corresponding_authors"))


def _is_plausible(record: dict[str, Any], since_year: int) -> bool:
    title = record.get("title", "")
    if not title or title == "Untitled":
        return False
    if _is_non_research_output(title):
        return False
    if _is_off_scope_application(record):
        return False
    raw_year = record.get("year")
    year = _safe_year(raw_year, log=False)
    if raw_year and year is None:
        return False
    if year and year < since_year:
        return False
    text = f"{title} {record.get('_abstract', '')}".lower()
    if _has_digital_twin_signal(text) and not _has_manufacturing_digital_twin_context(text):
        return False
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
        "digital twinning",
        "virtual twin",
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
        "soft actuators",
        "soft robot",
        "soft robots",
        "soft robotic",
        "soft robotics",
        "soft gripper",
        "soft robotic finger",
        "soft robotic fingers",
        "embedded actuation",
        "embedded sensing",
        "fin-ray",
        "fin ray",
        "pneumatic actuator",
        "bioinspired gripper",
        "metamaterial",
        "volumetric additive manufacturing",
        "volumetric printing",
        "computed axial lithography",
        "tomographic printing",
        "tomographic volumetric",
        "photopolymerization",
        "photopolymerisation",
        "high-throughput additive manufacturing",
        "computational design",
        "inverse design",
        "inverse-designed",
        "material distribution",
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
        "automated reaction optimization",
        "reaction optimization",
        "photochemical synthesis",
        "microfluidic reactor",
        "formulation discovery",
        "polymer formulation",
        "polymer nanoparticle",
        "thermoresponsive polymer",
        "lcst",
        "homogeneous catalysis",
        "robochem",
        "robotic fluid handling",
        "digital twin",
        "digital twins",
        "digital twinning",
        "virtual twin",
        "real-to-twin",
        "twin-enabled",
        "twin-driven",
        "process twin",
        "machine twin",
    ]
    return any(term in text for term in additive_terms) and any(term in text for term in topic_terms)


def _is_off_scope_application(record: dict[str, Any]) -> bool:
    text = f"{record.get('title', '')} {record.get('venue', '')}".lower()
    protected = [
        "dispensing volumetric additive manufacturing",
        "fin-ray effect soft robotic fingers",
        "adaptive and context-aware volumetric printing",
        "dual-wavelength volumetric microlithography",
        "alignment and actuation of liquid crystals",
        "diffusion-guided 4d microprinting",
    ]
    if any(term in text for term in protected):
        return False
    off_scope_terms = [
        "bioprint",
        "biofabricat",
        "tissue engineering",
        "organ-on-a-chip",
        "organ on a chip",
        "internal organ",
        "tissues and organs",
        "cell-based products",
        "cryopreservation",
        "dental",
        "dentistry",
        "prosthodontics",
        "prosthesis",
        "prosthetic",
        "minimally invasive",
        "endovascular",
        "pediatric patent ductus",
        "pancreas model",
        "food printing",
        "3d food printing",
        "food automation",
        "dough",
        "agricultural products",
        "medium-sized crops",
        "ripeness",
        "water treatment",
        "photovoltaic",
        "electroluminescent",
        "printed electronics",
        "stretchable electronics",
        "soft bioelectronics",
        "surface acoustic wave",
        "transducer",
        "drug delivery",
        "regenerative medicine",
        "medical education",
    ]
    return any(term in text for term in off_scope_terms)


def _has_digital_twin_signal(text: str) -> bool:
    return any(
        term in text
        for term in [
            "digital twin",
            "digital twins",
            "digital-twin",
            "digital-twins",
            "digital twinning",
            "virtual twin",
            "real-to-twin",
            "twin-enabled",
            "twin-driven",
            "process twin",
            "machine twin",
        ]
    )


def _has_manufacturing_digital_twin_context(text: str) -> bool:
    manufacturing_terms = [
        "manufacturing",
        "production",
        "additive manufacturing",
        "3d printing",
        "3-d printing",
        "4d printing",
        "4-d printing",
        "printing",
        "printed",
        "fabrication",
        "robot",
        "robotic",
        "automation",
        "automated",
        "assembly",
        "machining",
        "welding",
        "factory",
        "industrial",
        "quality",
        "powder bed",
        "laser powder",
        "lpbf",
        "fused filament",
        "fff",
        "fdm",
        "material extrusion",
        "wire arc",
        "waam",
        "directed energy",
        "binder jet",
        "vat photopolymer",
        "stereolithography",
        "dlp",
        "cnc",
    ]
    non_manufacturing_terms = [
        "urban",
        "city",
        "cities",
        "mobility",
        "supply chain",
        "pharma",
        "healthcare",
        "medical",
        "agricultural",
        "agriculture",
        "wheat",
        "crop",
        "air handling",
        "indoor",
    ]
    return any(term in text for term in manufacturing_terms) and not any(
        term in text for term in non_manufacturing_terms
    )


def _is_plausible_seed(record: dict[str, Any], since_year: int) -> bool:
    title = record.get("title", "")
    if not title or title == "Untitled":
        return False
    if _is_non_research_output(title):
        return False
    raw_year = record.get("year")
    year = _safe_year(raw_year, log=False)
    if raw_year and year is None:
        return False
    return not year or year >= since_year


def _mark_curation_priority(record: dict[str, Any]) -> None:
    record["curation_priority"] = True
    record["relevance_score"] = max(CURATED_MIN_SCORE, int(record.get("relevance_score") or 0))


def _is_non_research_output(title: str) -> bool:
    normalized_title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", title)).strip().lower()
    blocked_prefixes = (
        "addendum",
        "author correction",
        "comment on ",
        "correction",
        "correction:",
        "correction to",
        "corrigendum",
        "editorial",
        "editorial:",
        "erratum",
        "erratum to",
        "expression of concern",
        "publisher correction",
        "retraction",
        "review for ",
        "decision letter for ",
        "author response for ",
        "response to reviewers",
        "peer review for ",
        "title pending",
        "doctoral dissertation",
        "doctoral thesis",
        "master thesis",
        "master's thesis",
        "masters thesis",
        "phd thesis",
        "ph.d. thesis",
    )
    if normalized_title.startswith(blocked_prefixes):
        return True
    blocked_fragments = (
        "llm guided hypothesis generation in self-driving lab",
        "(invited)",
        " dissertation submitted ",
        " thesis submitted ",
    )
    return any(fragment in normalized_title for fragment in blocked_fragments)


def _split_curated_archive(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        key = _normalize_title(record.get("title", "")) or _dedupe_key(record)
        groups.setdefault(key, []).append(record)

    curated: list[dict[str, Any]] = []
    archive: list[dict[str, Any]] = []
    stats = {"low_relevance": 0, "duplicate_title": 0, "low_venue_trust": 0, "non_research_output": 0}

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
                if _is_low_venue_trust(record):
                    reason = "low_venue_trust"
                elif _is_non_research_output(record.get("title", "")):
                    reason = "non_research_output"
                else:
                    reason = "low_relevance"
                archive.append(_with_archive_reason(record, reason))
                stats[reason] = stats.get(reason, 0) + 1

    curated.sort(key=_sort_key, reverse=True)
    archive.sort(key=_sort_key, reverse=True)
    return curated, archive, stats


def _is_curated_candidate(record: dict[str, Any]) -> bool:
    return (
        bool(record.get("curation_priority"))
        or int(record.get("relevance_score") or 0) >= CURATED_MIN_SCORE
    ) and not _is_non_research_output(record.get("title", "")) and _is_journal_article(record)


def _is_journal_article(record: dict[str, Any]) -> bool:
    classification = _venue_classification(record)
    return classification["publication_type"] == "journal_article" and classification["venue_trust"] != "low"


def _is_low_venue_trust(record: dict[str, Any]) -> bool:
    classification = _venue_classification(record)
    return classification["venue_trust"] == "low"


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


def _venue_classification(record: dict[str, Any]) -> dict[str, str]:
    venue = unescape(str(record.get("venue") or record.get("journal") or "")).strip()
    venue_key = _normalize_title(venue)
    crossref_type = str(record.get("crossref_type") or "").lower()
    doi = str(record.get("doi") or "").lower()
    text = f"{venue_key} {crossref_type} {doi}"

    trusted_conferences = {
        "proceedings of the chi conference on human factors in computing systems",
        "proceedings of the 2025 chi conference on human factors in computing systems",
        "proceedings of the 2026 chi conference on human factors in computing systems",
        "proceedings of the extended abstracts of the chi conference on human factors in computing systems",
        "proceedings of the acm symposium on computational fabrication",
        "adjunct proceedings of the 10th acm symposium on computational fabrication",
        "ieee international conference on robotics and automation",
        "ieee/rsj international conference on intelligent robots and systems",
        "ieee rsj international conference on intelligent robots and systems",
        "ieee international conference on soft robotics",
        "ieee international conference on automation science and engineering",
    }
    low_trust_markers = (
        "international journal for research in applied science",
        "ijraset",
        "irjmets",
        "international research journal of modernization",
        "project repository journal",
        "nexus",
        "world journal",
        "global journal",
        "universal journal",
        "multidisciplinary science journal",
        "multidiszciplinaris tudomanyok",
        "nusantara science and technology proceedings",
    )
    repository_markers = (
        "arxiv",
        "chemrxiv",
        "research square",
        "ssrn",
        "techrxiv",
        "zenodo",
        "figshare",
        "repository",
        "preprint",
    )
    thesis_markers = (
        "dissertation",
        "doctoral thesis",
        "master thesis",
        "master's thesis",
        "masters thesis",
        "phd thesis",
        "ph.d. thesis",
        "university dissertation",
        "etd",
        "electronic thesis",
    )
    book_types = {
        "book-chapter",
        "book",
        "edited-book",
        "monograph",
        "reference-book",
        "reference-entry",
    }
    thesis_types = {
        "dissertation",
        "posted-content:dissertation",
    }

    if not venue or venue_key == "venue unknown":
        return {
            "publication_type": "unknown",
            "venue_trust": "low",
            "venue_trust_reason": "missing venue metadata",
        }
    if any(marker in text for marker in low_trust_markers):
        return {
            "publication_type": "low_trust_journal_or_proceedings",
            "venue_trust": "low",
            "venue_trust_reason": "venue matches local low-trust marker list",
        }
    if crossref_type in thesis_types or any(marker in text for marker in thesis_markers):
        return {
            "publication_type": "thesis_or_dissertation",
            "venue_trust": "low",
            "venue_trust_reason": "thesis/dissertation output rather than journal article",
        }
    if crossref_type == "posted-content" or any(marker in text for marker in repository_markers):
        return {
            "publication_type": "preprint_or_repository",
            "venue_trust": "low",
            "venue_trust_reason": "preprint or repository source",
        }
    if crossref_type in book_types:
        return {
            "publication_type": "book_or_chapter",
            "venue_trust": "low",
            "venue_trust_reason": "book/chapter output rather than journal or trusted conference article",
        }
    if "proceedings of the national academy of sciences" == venue_key:
        return {
            "publication_type": "journal_article",
            "venue_trust": "trusted",
            "venue_trust_reason": "PNAS journal article",
        }
    if crossref_type == "proceedings-article" or "proceedings" in venue_key or "conference" in venue_key:
        trusted = any(conference in venue_key for conference in trusted_conferences)
        return {
            "publication_type": "conference_proceedings",
            "venue_trust": "trusted" if trusted else "low",
            "venue_trust_reason": "trusted conference allowlist" if trusted else "conference/proceedings not in trusted allowlist",
        }
    if crossref_type == "journal-article" or not crossref_type:
        return {
            "publication_type": "journal_article",
            "venue_trust": "trusted",
            "venue_trust_reason": "journal article with named venue and no low-trust marker",
        }
    return {
        "publication_type": crossref_type or "other",
        "venue_trust": "low",
        "venue_trust_reason": "unsupported publication type",
    }


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
    venue_classification = _venue_classification(record)
    return {
        "id": paper_id,
        "title": record.get("title", "Untitled"),
        "authors": record.get("authors", []),
        "author_details": record.get("author_details", []),
        "corresponding_authors": record.get("corresponding_authors", []),
        "corresponding_author_available": bool(record.get("corresponding_authors")),
        "year": year,
        "venue": record.get("venue", ""),
        "openalex_work_id": record.get("openalex_work_id", ""),
        "openalex_source_id": record.get("openalex_source_id", ""),
        "venue_metrics": record.get("venue_metrics", {}),
        "journal_quality": _journal_quality(record),
        "publication_type": venue_classification["publication_type"],
        "venue_trust": venue_classification["venue_trust"],
        "venue_trust_reason": venue_classification["venue_trust_reason"],
        "doi": doi,
        "url": url,
        "source": sorted(set(record.get("source", []))),
        "categories": record.get("categories", ["Multi-material AM"])[:2],
        "tags": record.get("tags", [])[:6],
        "relevance_score": int(record.get("relevance_score", 5)),
        "curation_priority": bool(record.get("curation_priority")),
        "ai_summary_en": record.get("ai_summary_en", ""),
        "summary_provider": record.get("_summary_provider", "fallback"),
        "openai_summary_applied": record.get("_summary_provider") == "openai",
        "relevance_note_en": record.get("relevance_note_en", ""),
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
    if not existing.get("venue") and candidate.get("venue"):
        existing["venue"] = candidate["venue"]
    if not existing.get("year") and candidate.get("year"):
        existing["year"] = candidate["year"]
    if not existing.get("authors") and candidate.get("authors"):
        existing["authors"] = candidate["authors"]
    for key in (
        "author_details",
        "corresponding_authors",
        "openalex_work_id",
        "openalex_source_id",
        "venue_metrics",
    ):
        if candidate.get(key) and not existing.get(key):
            existing[key] = candidate[key]
    existing["corresponding_author_available"] = bool(existing.get("corresponding_authors"))
    existing["journal_quality"] = _journal_quality(existing)
    existing["last_updated"] = today


def _merge_existing_record(existing: dict[str, Any], candidate: dict[str, Any], today: str) -> None:
    _merge_source(existing, candidate, today)
    if existing.get("doi") and (
        not existing.get("author_details")
        or not existing.get("openalex_work_id")
        or ("OpenAlex" not in set(existing.get("source", [])) and not existing.get("corresponding_authors"))
    ):
        _crosscheck_openalex_metadata(existing)
        existing["journal_quality"] = _journal_quality(existing)
    if not existing.get("venue") and existing.get("doi"):
        crossref_record = _safe_fetch_crossref_doi(existing["doi"])
        if crossref_record:
            _merge_source(existing, crossref_record, today)
    if not _should_refresh_generic_summary(existing, candidate):
        return

    refresh_record = dict(existing)
    refresh_record.update({key: value for key, value in candidate.items() if value})
    summarized = summarize_record(refresh_record, allow_openai=False)
    for key in ("ai_summary_en", "relevance_note_en", "relevance_score", "tags", "categories"):
        if summarized.get(key):
            existing[key] = summarized[key]
    existing["summary_provider"] = "fallback"
    existing["openai_summary_applied"] = False
    existing["abstract_used_for_summary"] = bool(candidate.get("_abstract"))


def _should_refresh_generic_summary(existing: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if not candidate.get("_abstract"):
        return False
    summary = str(existing.get("ai_summary_en") or "")
    generic_markers = [
        "public metadata",
        "metadata and curated topic signals",
        "metadata-based summary",
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


def _journal_quality(record: dict[str, Any]) -> dict[str, Any]:
    """Assign a transparent journal-quality label without inventing JIF/Q values."""

    venue = unescape(str(record.get("venue") or "")).strip()
    venue_key = _normalize_title(venue)
    metrics = record.get("venue_metrics") or {}
    openalex_citedness = metrics.get("two_year_mean_citedness")
    source_type = str(metrics.get("type") or "").lower()

    high_impact = {
        "nature",
        "science",
        "nature communications",
        "nature materials",
        "nature reviews materials",
        "nature synthesis",
        "science advances",
        "science robotics",
        "proceedings of the national academy of sciences",
        "advanced materials",
        "advanced functional materials",
        "advanced science",
        "materials horizons",
    }
    core_manufacturing = {
        "additive manufacturing",
        "virtual and physical prototyping",
        "rapid prototyping journal",
        "3d printing and additive manufacturing",
        "progress in additive manufacturing",
        "journal of manufacturing processes",
        "journal of manufacturing systems",
        "manufacturing letters",
        "robotics and computer integrated manufacturing",
        "international journal of advanced manufacturing technology",
        "computer aided design",
        "acs applied materials and interfaces",
        "materials and design",
        "polymer chemistry",
        "digital discovery",
        "journal of intelligent manufacturing",
        "computers in industry",
    }
    repositories = {
        "arxiv org",
        "arxiv cornell university",
        "zenodo cern european organization for nuclear research",
        "figshare",
        "chemrxiv",
        "research square",
    }

    if venue_key in high_impact:
        label = "High-impact general journal"
        confidence = "manual_core_venue"
    elif venue_key in core_manufacturing:
        label = "Core manufacturing journal"
        confidence = "manual_core_venue"
    elif venue_key in repositories or source_type in {"repository"}:
        label = "Repository / preprint source"
        confidence = "metadata_source_type"
    elif isinstance(openalex_citedness, (int, float)):
        if openalex_citedness >= 10:
            label = "High OpenAlex citation impact"
        elif openalex_citedness >= 4:
            label = "Moderate OpenAlex citation impact"
        else:
            label = "Low or emerging OpenAlex citation impact"
        confidence = "openalex_metric_proxy"
    else:
        label = "Not classified"
        confidence = "insufficient_open_metric"

    return {
        "label": label,
        "basis": confidence,
        "official_jif": None,
        "official_quartile": None,
        "openalex_two_year_mean_citedness": openalex_citedness,
        "note": "Official JIF/quartile is not inferred. Add licensed JCR/Scopus data to populate official_jif or official_quartile.",
    }


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
