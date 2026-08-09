"""Sync stored AI summaries into public AML recommendation records."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
AML_RECOMMENDATIONS_PATH = ROOT / "public" / "data" / "aml_recommended_papers.json"


def main() -> None:
    papers = _load_list(PAPERS_PATH)
    recommendations = _load_list(AML_RECOMMENDATIONS_PATH)
    summaries = _ai_summary_index(papers)

    updated = 0
    already_ai = 0
    missing_source = 0
    for item in recommendations:
        if _has_ai_summary(item):
            already_ai += 1
            continue
        source = summaries.get(_record_key(item))
        if not source:
            missing_source += 1
            continue
        for key, value in source.items():
            if value not in (None, "", []):
                item[key] = value
        item["summary_source"] = "curated_paper_pool"
        updated += 1

    _write_json(AML_RECOMMENDATIONS_PATH, recommendations)
    print(
        "AML recommendation summary sync complete: "
        f"updated={updated}, already_ai={already_ai}, missing_source={missing_source}, "
        f"total={len(recommendations)}"
    )


def _ai_summary_index(papers: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for paper in papers:
        if not _has_ai_summary(paper):
            continue
        summary = str(paper.get("ai_summary_en") or "").strip()
        if not summary:
            continue
        key = _record_key(paper)
        if not key:
            continue
        provider = _summary_provider(paper)
        summaries[key] = {
            "ai_summary_en": summary,
            "relevance_note_en": paper.get("relevance_note_en", ""),
            "summary_provider": provider,
            "openai_summary_applied": provider == "openai",
            "local_summary_applied": provider == "local",
            "summary_model": paper.get("summary_model", ""),
            "abstract_used_for_summary": bool(paper.get("abstract_used_for_summary")),
        }
    return summaries


def _has_ai_summary(record: dict[str, Any]) -> bool:
    return _summary_provider(record) in {"openai", "local"}


def _summary_provider(record: dict[str, Any]) -> str:
    provider = str(record.get("summary_provider") or "").strip().lower()
    if provider in {"openai", "local"}:
        return provider
    if record.get("openai_summary_applied") is True:
        return "openai"
    if record.get("local_summary_applied") is True:
        return "local"
    return provider


def _record_key(record: dict[str, Any]) -> str:
    doi = _normalize_doi(record.get("doi"))
    if doi:
        return f"doi:{doi}"
    title = _normalize_title(record.get("title", ""))
    return f"title:{title}" if title else ""


def _normalize_doi(value: Any) -> str:
    text = str(value or "").strip().lower()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", text)


def _normalize_title(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


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


if __name__ == "__main__":
    main()
