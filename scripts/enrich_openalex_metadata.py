"""Enrich stored papers with OpenAlex authorship and venue metadata.

This script does not call OpenAI, crawl publisher pages, download PDFs, or store
raw abstracts. It only uses the OpenAlex Work API by DOI to fill metadata fields
that are useful for display: detailed authorship, corresponding author flags,
affiliations, and open venue metrics.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from fetch_openalex import fetch_openalex_by_doi
from update_papers import _journal_quality

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = [ROOT / "data" / "papers.json", ROOT / "data" / "archive_papers.json"]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    max_records = int(os.getenv("OPENALEX_ENRICH_MAX", "0") or "0")
    force = _env_flag("OPENALEX_ENRICH_FORCE")
    changed_total = 0
    checked_total = 0

    for path in DEFAULT_PATHS:
        records = _load_json(path, [])
        changed = 0
        failed = 0
        for record in records:
            if max_records and checked_total >= max_records:
                break
            if not _needs_enrichment(record, force=force):
                continue
            doi = record.get("doi")
            if not doi:
                continue
            checked_total += 1
            print(f"OpenAlex metadata enrichment: {doi}")
            try:
                enriched = fetch_openalex_by_doi(doi)
            except Exception as exc:
                failed += 1
                print(f"OpenAlex metadata enrichment failed for {doi}: {exc}")
                continue
            if not enriched:
                continue
            changed += _merge_enrichment(record, enriched)
            time.sleep(float(os.getenv("API_SLEEP_SECONDS", "0.2")))

        if changed:
            _write_json(path, records)
            print(f"Wrote {path.relative_to(ROOT)} with {changed} enriched records.")
        else:
            print(f"No enrichment changes in {path.relative_to(ROOT)}.")
        if failed:
            print(f"Skipped {failed} records in {path.relative_to(ROOT)} after OpenAlex lookup failures.")
        changed_total += changed

    print(f"OpenAlex metadata enrichment complete. Checked {checked_total}; changed {changed_total}.")


def _needs_enrichment(record: dict[str, Any], force: bool = False) -> bool:
    if force:
        return bool(record.get("doi"))
    if not record.get("doi"):
        return False
    return not record.get("author_details") or not record.get("venue_metrics") or not record.get("journal_quality")


def _merge_enrichment(record: dict[str, Any], enriched: dict[str, Any]) -> int:
    changed = 0
    for key in (
        "author_details",
        "corresponding_authors",
        "corresponding_author_available",
        "openalex_work_id",
        "openalex_source_id",
        "venue_metrics",
    ):
        value = enriched.get(key)
        if value and record.get(key) != value:
            record[key] = value
            changed = 1
    quality = _journal_quality(record)
    if record.get("journal_quality") != quality:
        record["journal_quality"] = quality
        changed = 1
    return changed


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    main()
