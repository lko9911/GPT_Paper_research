"""Assign simple OpenAlex-based venue ranks to stored papers.

This uses only the OpenAlex Sources API. It does not use JCR, scrape publisher
pages, call OpenAI, download PDFs, or infer official quartiles.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PAPERS_PATH = DATA_DIR / "papers.json"
ARCHIVE_PATH = DATA_DIR / "archive_papers.json"
SOURCE_METRICS_PATH = DATA_DIR / "openalex_source_metrics.json"
AML_RECOMMENDATIONS_PATH = ROOT / "public" / "data" / "aml_recommended_papers.json"
OPENALEX_SOURCES_API = "https://api.openalex.org/sources"
RANK_BASIS = "Internal OpenAlex 2yr mean citedness percentile among tracked venues; not JCR."


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    targets = _rank_targets()
    active = _load_list(PAPERS_PATH)
    archive = _load_list(ARCHIVE_PATH)
    aml_recommendations = _load_list(AML_RECOMMENDATIONS_PATH) if AML_RECOMMENDATIONS_PATH.exists() else []
    cache = _load_cache()

    records = []
    if _should_rank_papers(targets):
        records.extend(active)
        records.extend(archive)
    if _should_rank_aml(targets):
        records.extend(aml_recommendations)
    venue_requests = _unique_venue_requests(records)
    fetched = 0
    for venue_key, request in sorted(venue_requests.items()):
        if venue_key in cache["venues"]:
            continue
        source = _fetch_source_for_request(request)
        cache["venues"][venue_key] = source or {"matched": False, "venue": request["venue"], "fetched_at": _now_iso()}
        fetched += 1
        time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

    _assign_ranks(cache)
    active_changed = _apply_ranks(active, cache) if _should_rank_papers(targets) else 0
    archive_changed = _apply_ranks(archive, cache) if _should_rank_papers(targets) else 0
    aml_changed = _apply_aml_ranks(aml_recommendations, active, cache) if _should_rank_aml(targets) and aml_recommendations else 0

    cache["rank_basis"] = RANK_BASIS
    cache["venue_count"] = len(cache["venues"])
    cache["matched_venue_count"] = sum(1 for source in cache["venues"].values() if source.get("matched"))
    if fetched or active_changed or archive_changed or aml_changed:
        cache["updated_at"] = _now_iso()
    _write_json(SOURCE_METRICS_PATH, cache)
    if _should_rank_papers(targets):
        _write_json(PAPERS_PATH, active)
        _write_json(ARCHIVE_PATH, archive)
    if aml_recommendations:
        _write_json(AML_RECOMMENDATIONS_PATH, aml_recommendations)

    print(
        "OpenAlex venue rank enrichment complete: "
        f"venues={len(venue_requests)}, fetched={fetched}, matched={cache['matched_venue_count']}, "
        f"active_changed={active_changed}, archive_changed={archive_changed}, aml_changed={aml_changed}"
    )


def _rank_targets() -> set[str]:
    raw = os.getenv("OPENALEX_RANK_TARGETS", "all")
    targets = {item.strip().lower() for item in raw.split(",") if item.strip()}
    return targets or {"all"}


def _should_rank_papers(targets: set[str]) -> bool:
    return "all" in targets or "papers" in targets


def _should_rank_aml(targets: set[str]) -> bool:
    return "all" in targets or "aml" in targets


def _unique_venue_requests(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    requests_by_venue: dict[str, dict[str, Any]] = {}
    for record in records:
        venue = str(record.get("venue") or record.get("journal") or "").strip()
        if not venue or venue.lower() == "venue unknown":
            continue
        venue_key = _normalize_key(venue)
        if not venue_key:
            continue
        issns = _record_issns(record)
        current = requests_by_venue.setdefault(venue_key, {"venue": venue, "issns": []})
        current["issns"] = sorted(set(current["issns"]) | set(issns))
    return requests_by_venue


def _record_issns(record: dict[str, Any]) -> list[str]:
    values: list[Any] = []
    for key in ("issn", "issn_l"):
        value = record.get(key)
        if isinstance(value, list):
            values.extend(value)
        elif value:
            values.append(value)
    return sorted({_normalize_issn(value) for value in values if _normalize_issn(value)})


def _fetch_source_for_request(request: dict[str, Any]) -> dict[str, Any] | None:
    for issn in request.get("issns", []):
        source = _fetch_source_by_issn(issn)
        if source:
            return source
    return None


def _fetch_source_by_issn(issn: str) -> dict[str, Any] | None:
    params = {"filter": f"issn:{issn}", "per-page": 5}
    contact_email = os.getenv("CONTACT_EMAIL")
    if contact_email:
        params["mailto"] = contact_email
    try:
        response = _get_with_retry(OPENALEX_SOURCES_API, params=params)
    except Exception as exc:
        print(f"OpenAlex source lookup failed for ISSN {issn}: {exc}")
        return None
    results = response.json().get("results", [])
    if not results:
        return None
    source = max(results, key=_source_choice_score)
    return _normalize_source(source)


def _source_choice_score(source: dict[str, Any]) -> tuple[int, int, int]:
    return (
        1 if source.get("type") == "journal" else 0,
        1 if source.get("summary_stats", {}).get("2yr_mean_citedness") is not None else 0,
        int(source.get("works_count") or 0),
    )


def _normalize_source(source: dict[str, Any]) -> dict[str, Any]:
    summary = source.get("summary_stats") or {}
    return {
        "matched": True,
        "source": "OpenAlex",
        "source_id": source.get("id", ""),
        "display_name": source.get("display_name", ""),
        "abbreviated_title": source.get("abbreviated_title", ""),
        "issn": source.get("issn") or [],
        "issn_l": source.get("issn_l", ""),
        "type": source.get("type", ""),
        "host_organization_name": source.get("host_organization_name", ""),
        "homepage_url": source.get("homepage_url", ""),
        "works_count": source.get("works_count"),
        "cited_by_count": source.get("cited_by_count"),
        "two_year_mean_citedness": _float_or_none(summary.get("2yr_mean_citedness")),
        "h_index": summary.get("h_index"),
        "i10_index": summary.get("i10_index"),
        "is_core": bool(source.get("is_core")),
        "is_oa": source.get("is_oa"),
        "is_in_doaj": source.get("is_in_doaj"),
        "updated_date": source.get("updated_date", ""),
        "fetched_at": _now_iso(),
    }


def _assign_ranks(cache: dict[str, Any]) -> None:
    matched = [
        source
        for source in cache["venues"].values()
        if source.get("matched") and source.get("type") == "journal"
    ]
    scored = [source for source in matched if source.get("two_year_mean_citedness") is not None]
    scored.sort(key=lambda source: float(source.get("two_year_mean_citedness") or 0.0), reverse=True)
    n = len(scored)
    for position, source in enumerate(scored):
        rank = min(4, math.floor(position * 4 / max(n, 1)) + 1)
        percentile = 1.0 - (position / max(n - 1, 1)) if n > 1 else 1.0
        source["openalex_venue_rank"] = f"Rank {rank}"
        source["openalex_venue_rank_number"] = rank
        source["openalex_venue_rank_percentile"] = round(percentile, 4)
        source["openalex_venue_rank_score"] = source.get("two_year_mean_citedness")
        source["openalex_venue_rank_basis"] = RANK_BASIS

    for source in matched:
        if source.get("openalex_venue_rank"):
            continue
        source["openalex_venue_rank"] = "Rank 4"
        source["openalex_venue_rank_number"] = 4
        source["openalex_venue_rank_percentile"] = 0.0
        source["openalex_venue_rank_score"] = 0.0
        source["openalex_venue_rank_basis"] = RANK_BASIS


def _apply_ranks(records: list[dict[str, Any]], cache: dict[str, Any]) -> int:
    changed = 0
    for record in records:
        source = _source_for_record(record, cache)
        new_fields = _rank_fields(source)
        if not new_fields:
            continue
        for key, value in new_fields.items():
            if record.get(key) != value:
                record[key] = value
                changed += 1
        metrics = _venue_metrics(source)
        if metrics and record.get("venue_metrics") != metrics:
            record["venue_metrics"] = metrics
            changed += 1
        quality = dict(record.get("journal_quality") or {})
        if source.get("two_year_mean_citedness") is not None:
            quality["openalex_two_year_mean_citedness"] = source.get("two_year_mean_citedness")
            quality["openalex_venue_rank"] = source.get("openalex_venue_rank")
            quality["openalex_venue_rank_basis"] = RANK_BASIS
            if record.get("journal_quality") != quality:
                record["journal_quality"] = quality
                changed += 1
    return changed


def _apply_aml_ranks(
    aml_items: list[dict[str, Any]],
    active_records: list[dict[str, Any]],
    cache: dict[str, Any],
) -> int:
    active_by_key = {_record_key(record): record for record in active_records if _record_key(record)}
    changed = 0
    for item in aml_items:
        source_record = active_by_key.get(_record_key(item))
        if source_record:
            fields = {key: source_record.get(key) for key in _rank_field_names() if source_record.get(key) not in (None, "")}
        else:
            source = _source_for_record({"venue": item.get("journal") or item.get("venue")}, cache)
            fields = _rank_fields(source)
        for key, value in fields.items():
            if item.get(key) != value:
                item[key] = value
                changed += 1
    return changed


def _source_for_record(record: dict[str, Any], cache: dict[str, Any]) -> dict[str, Any]:
    venue = str(record.get("venue") or record.get("journal") or "").strip()
    return cache["venues"].get(_normalize_key(venue), {}) if venue else {}


def _rank_fields(source: dict[str, Any]) -> dict[str, Any]:
    if not source or not source.get("matched") or not source.get("openalex_venue_rank"):
        return {}
    return {
        "openalex_source_id": source.get("source_id", ""),
        "openalex_venue_rank": source.get("openalex_venue_rank", ""),
        "openalex_venue_rank_number": source.get("openalex_venue_rank_number"),
        "openalex_venue_rank_score": source.get("openalex_venue_rank_score"),
        "openalex_venue_rank_percentile": source.get("openalex_venue_rank_percentile"),
        "openalex_venue_rank_basis": source.get("openalex_venue_rank_basis", RANK_BASIS),
    }


def _rank_field_names() -> tuple[str, ...]:
    return (
        "openalex_source_id",
        "openalex_venue_rank",
        "openalex_venue_rank_number",
        "openalex_venue_rank_score",
        "openalex_venue_rank_percentile",
        "openalex_venue_rank_basis",
    )


def _venue_metrics(source: dict[str, Any]) -> dict[str, Any]:
    if not source or not source.get("matched"):
        return {}
    return {
        "source": "OpenAlex",
        "source_id": source.get("source_id", ""),
        "issn_l": source.get("issn_l", ""),
        "issn": source.get("issn") or [],
        "type": source.get("type", ""),
        "host_organization_name": source.get("host_organization_name", ""),
        "works_count": source.get("works_count"),
        "cited_by_count": source.get("cited_by_count"),
        "two_year_mean_citedness": source.get("two_year_mean_citedness"),
        "h_index": source.get("h_index"),
        "i10_index": source.get("i10_index"),
        "is_core": source.get("is_core"),
        "is_oa": source.get("is_oa"),
        "is_in_doaj": source.get("is_in_doaj"),
    }


def _load_cache() -> dict[str, Any]:
    if SOURCE_METRICS_PATH.exists():
        data = json.loads(SOURCE_METRICS_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data.setdefault("venues", {})
            return data
    return {"updated_at": "", "rank_basis": RANK_BASIS, "venues": {}}


def _load_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON array")
    return data


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _get_with_retry(url: str, params: dict[str, Any]) -> requests.Response:
    retries = int(os.getenv("OPENALEX_RETRIES", "3"))
    base_sleep = float(os.getenv("API_SLEEP_SECONDS", "0.2"))
    headers = {
        "User-Agent": f"aml-paper-tracker/1.0 ({os.getenv('CONTACT_EMAIL') or os.getenv('GITHUB_ACTOR') or 'local'})",
        "Accept": "application/json",
    }
    for attempt in range(retries + 1):
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code != 429:
            response.raise_for_status()
            return response
        if attempt >= retries:
            response.raise_for_status()
        wait = base_sleep * (2 ** attempt + 1)
        print(f"OpenAlex source lookup rate limited; retrying in {wait:.1f}s")
        time.sleep(wait)
    raise RuntimeError("OpenAlex source retry loop exhausted")


def _record_key(record: dict[str, Any]) -> str:
    doi = str(record.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi}"
    title = _normalize_key(str(record.get("title") or ""))
    return f"title:{title}" if title else ""


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def _normalize_issn(value: Any) -> str:
    text = re.sub(r"[^0-9Xx]", "", str(value or ""))
    if len(text) != 8:
        return ""
    return f"{text[:4]}-{text[4:].upper()}"


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    main()
