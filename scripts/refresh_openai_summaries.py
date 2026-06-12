"""Refresh existing paper summaries with OpenAI in a bounded manual batch.

This script is intentionally separate from the hourly metadata update so a
full-library OpenAI refresh cannot run accidentally on every schedule.
"""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fetch_openalex import fetch_openalex_by_doi
from summarize import summarize_record

ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
SITE_META_PATH = ROOT / "data" / "site_meta.json"

SUMMARY_KEYS = ("ai_summary_ko", "ai_summary_en", "relevance_note_ko", "relevance_score", "tags", "categories")


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set; skipping OpenAI summary refresh.")
        return

    papers = _load_json(PAPERS_PATH, [])
    max_items = _env_int("MAX_OPENAI_SUMMARIES", 25)
    mode = os.getenv("REFRESH_MODE", "non_qa").strip().lower()
    dry_run = _env_bool("DRY_RUN", False)
    sleep_seconds = float(os.getenv("OPENAI_REFRESH_SLEEP_SECONDS", os.getenv("API_SLEEP_SECONDS", "1.0")))

    candidates = [paper for paper in papers if _should_refresh(paper, mode)]
    if max_items > 0:
        candidates = candidates[:max_items]

    print(f"OpenAI summary refresh mode={mode}, candidates={len(candidates)}, dry_run={dry_run}")

    refreshed = 0
    skipped = 0
    failed = 0
    today = datetime.now(UTC).date().isoformat()

    for index, paper in enumerate(candidates, start=1):
        title = paper.get("title") or "Untitled"
        try:
            record = _record_for_summary(paper)
            openalex_record = _openalex_record(paper)
            if openalex_record:
                record.update({key: value for key, value in openalex_record.items() if value})
            summarized = summarize_record(record, allow_openai=True)
            if summarized.get("_summary_provider") != "openai":
                skipped += 1
                print(f"[{index}/{len(candidates)}] skipped fallback-only: {title}")
                continue
            if not dry_run:
                for key in SUMMARY_KEYS:
                    if summarized.get(key):
                        paper[key] = summarized[key]
                paper["abstract_used_for_summary"] = bool(record.get("_abstract"))
                paper["raw_abstract_displayed"] = False
                paper["pdf_stored"] = False
                paper["last_updated"] = today
                for key in list(paper):
                    if key.startswith("_"):
                        paper.pop(key, None)
            refreshed += 1
            print(f"[{index}/{len(candidates)}] refreshed: {title}")
        except Exception as exc:
            failed += 1
            print(f"[{index}/{len(candidates)}] failed: {title}: {exc}")
        time.sleep(sleep_seconds)

    if not dry_run and refreshed:
        _write_json(PAPERS_PATH, papers)
        _update_site_meta(len(papers), refreshed)

    print(f"OpenAI summary refresh done: refreshed={refreshed}, skipped={skipped}, failed={failed}")


def _should_refresh(paper: dict[str, Any], mode: str) -> bool:
    summary = str(paper.get("ai_summary_ko") or "").strip()
    if mode == "all":
        return True
    if mode == "missing":
        return not summary
    return not _is_five_question_summary(summary) or not paper.get("ai_summary_en")


def _is_five_question_summary(summary: str) -> bool:
    lines = [line.strip() for line in summary.splitlines() if line.strip()]
    if len(lines) < 5:
        return False
    return all(lines[index].startswith(f"{index + 1}.") for index in range(5))


def _record_for_summary(paper: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": paper.get("title", ""),
        "authors": paper.get("authors", []),
        "year": paper.get("year"),
        "venue": paper.get("venue", ""),
        "doi": paper.get("doi", ""),
        "url": paper.get("url", ""),
        "source": paper.get("source", []),
        "categories": paper.get("categories", []),
        "tags": paper.get("tags", []),
    }


def _openalex_record(paper: dict[str, Any]) -> dict[str, Any] | None:
    doi = paper.get("doi")
    if not doi:
        return None
    try:
        return fetch_openalex_by_doi(str(doi))
    except Exception as exc:
        print(f"OpenAlex abstract lookup failed for DOI {doi}: {exc}")
        return None


def _update_site_meta(paper_count: int, refreshed: int) -> None:
    meta = _load_json(SITE_META_PATH, {})
    now = datetime.now(UTC).replace(microsecond=0)
    meta.update(
        {
            "last_run_at_utc": now.isoformat().replace("+00:00", "Z"),
            "last_run_date": now.date().isoformat(),
            "paper_count": paper_count,
            "summaries_refreshed": refreshed,
            "summary_refresh_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        }
    )
    _write_json(SITE_META_PATH, meta)


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


if __name__ == "__main__":
    main()
