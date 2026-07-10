"""Build lightweight public indexes and lazy-loaded detail chunks.

The source-of-truth JSON files remain data/papers.json and
data/archive_papers.json. The GitHub Pages frontend should load the generated
index files first and fetch detail chunks only when a paper needs full details.
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PAPERS_PATH = DATA_DIR / "papers.json"
ARCHIVE_PATH = DATA_DIR / "archive_papers.json"

ACTIVE_INDEX_PATH = DATA_DIR / "papers_index.json"
ARCHIVE_INDEX_PATH = DATA_DIR / "archive_papers_index.json"
ACTIVE_DETAILS_DIR = DATA_DIR / "details"
ARCHIVE_DETAILS_DIR = DATA_DIR / "archive_details"
ACTIVE_MANIFEST_PATH = DATA_DIR / "detail_manifest.json"
ARCHIVE_MANIFEST_PATH = DATA_DIR / "archive_detail_manifest.json"

CHUNK_SIZE = 250

INDEX_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "source",
    "categories",
    "tags",
    "relevance_score",
    "first_added",
    "last_updated",
    "summary_provider",
    "openai_summary_applied",
    "corresponding_authors",
    "curation_priority",
    "is_core_venue",
    "publication_type",
    "venue_trust",
    "openalex_venue_rank",
    "openalex_venue_rank_number",
    "openalex_venue_rank_score",
    "openalex_venue_rank_percentile",
    "openalex_venue_rank_basis",
    "is_weekly_new",
    "archive_reason",
    "archive_scope_reasons",
}

KO_DUPLICATE_KEYS = {
    "title_ko",
    "abstract_ko",
    "summary_ko",
    "reason_ko",
    "recommendation_ko",
    "korean_title",
    "korean_abstract",
    "translated_title",
    "translated_abstract",
    "ai_summary_ko",
    "relevance_note_ko",
    "archive_note_ko",
    "ko",
}


def main() -> None:
    active = _load_records(PAPERS_PATH)
    archive = _load_records(ARCHIVE_PATH)

    active_report = _build_dataset(
        records=active,
        index_path=ACTIVE_INDEX_PATH,
        details_dir=ACTIVE_DETAILS_DIR,
        manifest_path=ACTIVE_MANIFEST_PATH,
        chunk_prefix="detail",
        status="active",
    )
    archive_report = _build_dataset(
        records=archive,
        index_path=ARCHIVE_INDEX_PATH,
        details_dir=ARCHIVE_DETAILS_DIR,
        manifest_path=ARCHIVE_MANIFEST_PATH,
        chunk_prefix="archive_detail",
        status="archived",
    )

    original_active = PAPERS_PATH.stat().st_size
    original_archive = ARCHIVE_PATH.stat().st_size if ARCHIVE_PATH.exists() else 0
    initial_load = ACTIVE_INDEX_PATH.stat().st_size
    combined_original = original_active + original_archive
    reduction = 100 * (1 - (initial_load / combined_original)) if combined_original else 0

    print("Split data build complete.")
    print(f"Original papers.json size: {_fmt(original_active)}")
    print(f"Original archive data size: {_fmt(original_archive)}")
    print(f"Combined original size: {_fmt(combined_original)}")
    print(f"New papers_index.json size: {_fmt(ACTIVE_INDEX_PATH.stat().st_size)}")
    print(f"New archive_papers_index.json size: {_fmt(ARCHIVE_INDEX_PATH.stat().st_size)}")
    print(f"Total active detail data size: {_fmt(active_report['detail_size'])}")
    print(f"Total archive detail data size: {_fmt(archive_report['detail_size'])}")
    print(f"Estimated initial load size for default view: {_fmt(initial_load)}")
    print(f"Estimated reduction in initial JSON load: {reduction:.1f}%")
    print(f"Active detail chunks: {active_report['chunks']}")
    print(f"Archive detail chunks: {archive_report['chunks']}")
    print(f"Removed Korean duplicate fields: {active_report['ko_fields'] + archive_report['ko_fields']}")


def _load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    return data


def _build_dataset(
    records: list[dict[str, Any]],
    index_path: Path,
    details_dir: Path,
    manifest_path: Path,
    chunk_prefix: str,
    status: str,
) -> dict[str, Any]:
    _reset_dir(details_dir)
    index_records: list[dict[str, Any]] = []
    detail_records: dict[str, dict[str, Any]] = {}
    manifest: dict[str, str] = {}
    ko_removed = 0

    for record in records:
        cleaned, removed = _strip_korean_duplicates(record)
        ko_removed += removed
        paper_id = str(cleaned.get("id") or cleaned.get("doi") or _title_key(cleaned.get("title", "")))
        if not paper_id:
            continue
        cleaned["id"] = paper_id

        index = {key: cleaned[key] for key in sorted(INDEX_FIELDS) if key in cleaned}
        if "corresponding_authors" in index:
            index["corresponding_authors"] = _compact_corresponding_authors(index["corresponding_authors"])
            if not index["corresponding_authors"]:
                index.pop("corresponding_authors", None)
        index["id"] = paper_id
        index["status"] = status
        index_records.append(index)

        detail = {key: value for key, value in cleaned.items() if key not in INDEX_FIELDS}
        detail["id"] = paper_id
        detail_records[paper_id] = detail

    chunk_count = math.ceil(len(index_records) / CHUNK_SIZE) if index_records else 0
    for chunk_number in range(chunk_count):
        start = chunk_number * CHUNK_SIZE
        stop = start + CHUNK_SIZE
        chunk_items = index_records[start:stop]
        file_name = f"{chunk_prefix}_{chunk_number:03d}.json"
        chunk_path = details_dir / file_name
        payload = {item["id"]: detail_records.get(item["id"], {"id": item["id"]}) for item in chunk_items}
        _write_json(chunk_path, payload)
        for item in chunk_items:
            manifest[item["id"]] = file_name

    _write_json(index_path, index_records)
    _write_json(manifest_path, manifest)

    return {
        "chunks": chunk_count,
        "detail_size": sum(path.stat().st_size for path in details_dir.glob("*.json")),
        "ko_fields": ko_removed,
    }


def _strip_korean_duplicates(record: dict[str, Any]) -> tuple[dict[str, Any], int]:
    removed = 0
    cleaned: dict[str, Any] = {}
    for key, value in record.items():
        if _is_korean_duplicate_key(key):
            removed += 1
            continue
        cleaned[key] = value
    return cleaned, removed


def _compact_corresponding_authors(authors: Any) -> list[dict[str, Any]]:
    if not isinstance(authors, list):
        return []
    compact: list[dict[str, Any]] = []
    for author in authors:
        if not isinstance(author, dict):
            continue
        name = str(author.get("name") or "").strip()
        if not name:
            continue
        compact_author: dict[str, Any] = {
            "name": name,
            "is_corresponding": True,
        }
        compact.append({key: value for key, value in compact_author.items() if value not in (None, "", [])})
    return compact


def _is_korean_duplicate_key(key: str) -> bool:
    lowered = key.lower()
    return (
        lowered in KO_DUPLICATE_KEYS
        or lowered.endswith("_ko")
        or "korean" in lowered
        or lowered.startswith("ko_")
        or "translated_" in lowered
    )


def _reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _title_key(value: str) -> str:
    return "title:" + " ".join(str(value or "").lower().split())


def _fmt(size: int) -> str:
    return f"{size / 1024:.1f} KB"


if __name__ == "__main__":
    main()
