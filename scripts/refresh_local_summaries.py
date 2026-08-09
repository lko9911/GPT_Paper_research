"""Refresh paper summaries with a local Ollama model.

This script mirrors the bounded manual OpenAI refresh, but it talks only to a
local Ollama server. It is intended for low-cost local testing on a GPU PC and
later migration to a larger workstation.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fetch_openalex import fetch_openalex_by_doi
from summarize import summarize_record

ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
SITE_META_PATH = ROOT / "data" / "site_meta.json"

SUMMARY_KEYS = ("ai_summary_en", "relevance_note_en", "tags", "categories", "relevance_score")


def main() -> None:
    endpoint = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("LOCAL_LLM_MODEL", "qwen2.5:7b")
    if not _ollama_available(endpoint, model):
        print(f"Local LLM is not available at {endpoint} with model={model}.")
        return

    papers = _load_json(PAPERS_PATH, [])
    max_items = _env_int("MAX_LOCAL_SUMMARIES", 5)
    mode = os.getenv("REFRESH_MODE", "metadata").strip().lower()
    dry_run = _env_bool("DRY_RUN", False)
    overwrite_openai = _env_bool("LOCAL_OVERWRITE_OPENAI", False)
    sleep_seconds = float(os.getenv("LOCAL_REFRESH_SLEEP_SECONDS", os.getenv("API_SLEEP_SECONDS", "0.5")))

    candidates = [paper for paper in papers if _should_refresh(paper, mode, overwrite_openai)]
    if max_items > 0:
        candidates = candidates[:max_items]

    print(
        f"Local summary refresh model={model}, mode={mode}, candidates={len(candidates)}, "
        f"dry_run={dry_run}, overwrite_openai={overwrite_openai}"
    )

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
            has_abstract = bool(record.get("_abstract"))
            require_abstract = _env_bool("LOCAL_REQUIRE_ABSTRACT", True)
            summarized = summarize_record(record, allow_openai=False, allow_local=not (require_abstract and not has_abstract))
            provider = summarized.get("_summary_provider")
            if provider not in {"local", "fallback"}:
                skipped += 1
                print(f"[{index}/{len(candidates)}] skipped fallback-only: {title}")
                continue
            if not dry_run:
                for key in SUMMARY_KEYS:
                    if summarized.get(key) is not None:
                        paper[key] = summarized[key]
                paper["abstract_used_for_summary"] = bool(record.get("_abstract"))
                paper["raw_abstract_displayed"] = False
                paper["pdf_stored"] = False
                paper["summary_provider"] = provider
                paper["openai_summary_applied"] = False
                paper["local_summary_applied"] = provider == "local"
                if provider == "local":
                    paper["summary_model"] = summarized.get("_summary_model") or model
                else:
                    paper.pop("summary_model", None)
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
        _update_site_meta(len(papers), refreshed, model)

    print(f"Local summary refresh done: refreshed={refreshed}, skipped={skipped}, failed={failed}")


def _should_refresh(paper: dict[str, Any], mode: str, overwrite_openai: bool) -> bool:
    provider = str(paper.get("summary_provider") or "").strip().lower()
    is_openai = provider == "openai" or paper.get("openai_summary_applied") is True
    if is_openai and not overwrite_openai:
        return False

    summary = str(paper.get("ai_summary_en") or "").strip()
    if mode == "all":
        return True
    if mode in {"week", "weekly", "new"}:
        return bool(paper.get("is_weekly_new") or paper.get("weekly_new"))
    if mode in {"metadata", "fallback"}:
        return provider in {"", "fallback", "metadata", "metadata-based"}
    if mode == "missing":
        return not summary
    return not _is_five_question_summary(summary)


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


def _ollama_available(endpoint: str, model: str) -> bool:
    try:
        request = urllib.request.Request(endpoint.rstrip("/") + "/api/tags", method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
        models = payload.get("models") or []
        return any(item.get("name") == model or item.get("model") == model for item in models)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False


def _update_site_meta(paper_count: int, refreshed: int, model: str) -> None:
    meta = _load_json(SITE_META_PATH, {})
    now = datetime.now(UTC).replace(microsecond=0)
    meta.update(
        {
            "last_run_at_utc": now.isoformat().replace("+00:00", "Z"),
            "last_run_date": now.date().isoformat(),
            "paper_count": paper_count,
            "summaries_refreshed": refreshed,
            "summary_refresh_model": model,
            "summary_refresh_provider": "local",
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
