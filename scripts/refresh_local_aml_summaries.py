"""Refresh AML recommendation summaries with a local Ollama model."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from fetch_openalex import fetch_openalex_by_doi
from summarize import summarize_record


ROOT = Path(__file__).resolve().parents[1]
AML_RECOMMENDATIONS_PATH = ROOT / "public" / "data" / "aml_recommended_papers.json"

SUMMARY_KEYS = ("ai_summary_en", "relevance_note_en", "tags", "categories", "relevance_score")


def main() -> None:
    endpoint = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("LOCAL_LLM_MODEL", "qwen2.5:7b")
    if not _ollama_available(endpoint, model):
        print(f"Local LLM is not available at {endpoint} with model={model}.")
        return

    recommendations = _load_json(AML_RECOMMENDATIONS_PATH, [])
    max_items = _env_int("MAX_LOCAL_AML_SUMMARIES", 0)
    mode = os.getenv("LOCAL_AML_REFRESH_MODE", os.getenv("REFRESH_MODE", "metadata")).strip().lower()
    dry_run = _env_bool("DRY_RUN", False)
    sleep_seconds = float(os.getenv("LOCAL_REFRESH_SLEEP_SECONDS", os.getenv("API_SLEEP_SECONDS", "0.5")))

    candidates = [paper for paper in recommendations if _should_refresh(paper, mode)]
    if max_items > 0:
        candidates = candidates[:max_items]

    print(
        f"Local AML summary refresh model={model}, mode={mode}, candidates={len(candidates)}, dry_run={dry_run}"
    )

    refreshed = 0
    skipped = 0
    failed = 0

    for index, paper in enumerate(candidates, start=1):
        title = paper.get("title") or "Untitled"
        try:
            record = _record_for_summary(paper)
            openalex_record = _openalex_record(paper)
            if openalex_record:
                record.update({key: value for key, value in openalex_record.items() if value})
            summarized = summarize_record(record, allow_openai=False, allow_local=True)
            if summarized.get("_summary_provider") != "local":
                skipped += 1
                print(f"[{index}/{len(candidates)}] skipped local summary: {title}")
                continue
            if not dry_run:
                for key in SUMMARY_KEYS:
                    if summarized.get(key) is not None:
                        paper[key] = summarized[key]
                paper["abstract_used_for_summary"] = bool(record.get("_abstract"))
                paper["raw_abstract_displayed"] = False
                paper["pdf_stored"] = False
                paper["summary_provider"] = "local"
                paper["openai_summary_applied"] = False
                paper["local_summary_applied"] = True
                paper["summary_model"] = summarized.get("_summary_model") or model
                paper["summary_source"] = "local_aml_recommendation_refresh"
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
        _write_json(AML_RECOMMENDATIONS_PATH, recommendations)

    print(f"Local AML summary refresh done: refreshed={refreshed}, skipped={skipped}, failed={failed}")


def _has_ai_summary(paper: dict[str, Any]) -> bool:
    provider = str(paper.get("summary_provider") or "").strip().lower()
    return provider in {"openai", "local"} or paper.get("openai_summary_applied") is True or paper.get("local_summary_applied") is True


def _should_refresh(paper: dict[str, Any], mode: str) -> bool:
    provider = str(paper.get("summary_provider") or "").strip().lower()
    if mode in {"local", "local_rewrite", "qwen_rewrite"}:
        return provider == "local" or paper.get("local_summary_applied") is True
    if mode in {"all_non_openai", "non_openai"}:
        return provider != "openai" and paper.get("openai_summary_applied") is not True
    if mode == "missing":
        return not str(paper.get("ai_summary_en") or "").strip()
    return not _has_ai_summary(paper)


def _record_for_summary(paper: dict[str, Any]) -> dict[str, Any]:
    tags = _as_list(paper.get("tags")) or _as_list(paper.get("matched_topics"))
    categories = _as_list(paper.get("categories"))
    return {
        "title": paper.get("title", ""),
        "authors": paper.get("authors", []),
        "year": paper.get("year"),
        "venue": paper.get("venue") or paper.get("journal", ""),
        "doi": paper.get("doi", ""),
        "url": paper.get("url", ""),
        "source": paper.get("source", []),
        "categories": categories,
        "tags": tags,
        "existing_q5_summary": paper.get("ai_summary_en", ""),
        "existing_relevance_note_en": paper.get("relevance_note_en", ""),
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


def _as_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


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
