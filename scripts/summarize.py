"""Generate Korean summaries and relevance metadata for new papers."""

from __future__ import annotations

import json
import os
import re
from typing import Any

CATEGORIES = [
    "리뷰 및 서베이",
    "다중재료 적층제조",
    "기능성 구배 적층제조",
    "Blended FDM / Digital Material Filament",
    "계산설계",
    "재료분포 최적화",
    "툴패스 계획",
    "재료 전환 / 퍼지 감소",
    "그래프 탐색 / 경로 계획 알고리즘",
    "적층제조를 위한 AI 및 머신러닝",
]

KEYWORDS = {
    "리뷰 및 서베이": ["review", "survey", "state of the art", "overview"],
    "다중재료 적층제조": ["multi-material", "multimaterial", "multiple material"],
    "기능성 구배 적층제조": ["functionally graded", "fgam", "graded material"],
    "Blended FDM / Digital Material Filament": ["blended fdm", "digital material filament", "dm filament", "filament blending"],
    "계산설계": ["computational design", "inverse design", "design automation", "generative design"],
    "재료분포 최적화": ["material distribution", "topology optimization", "distribution optimization"],
    "툴패스 계획": ["toolpath", "tool path", "slicing", "deposition path"],
    "재료 전환 / 퍼지 감소": ["material switching", "purge", "waste reduction", "transition"],
    "그래프 탐색 / 경로 계획 알고리즘": ["graph search", "path planning", "traveling salesman", "routing"],
    "적층제조를 위한 AI 및 머신러닝": ["machine learning", "deep learning", "artificial intelligence", "neural"],
}

TAG_MAP = {
    "FGAM": ["functionally graded", "fgam", "graded"],
    "MMAM": ["multi-material", "multimaterial", "multiple material"],
    "DM filament": ["digital material filament", "dm filament", "blended fdm", "filament blending"],
    "계산설계": ["computational design", "inverse design", "generative design"],
    "재료분포": ["material distribution", "topology optimization"],
    "툴패스": ["toolpath", "tool path", "slicing"],
    "퍼지 감소": ["purge", "material switching", "waste reduction"],
    "경로계획": ["path planning", "graph search", "routing"],
    "AI/ML": ["machine learning", "deep learning", "neural", "artificial intelligence"],
}


def summarize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Add Korean summary fields to a record.

    OPENAI_API_KEY enables model-based generation. Without it, this function
    creates a conservative Korean summary from title and metadata, avoiding any
    verbatim abstract reuse.
    """

    abstract = record.get("_abstract", "")
    if os.getenv("OPENAI_API_KEY"):
        generated = _summarize_with_openai(record, abstract)
        if generated:
            record.update(generated)
            return record

    record.update(_fallback_summary(record, abstract))
    return record


def _summarize_with_openai(record: dict[str, Any], abstract: str) -> dict[str, Any] | None:
    try:
        from openai import OpenAI

        client = OpenAI()
        prompt = {
            "title": record.get("title"),
            "authors": record.get("authors", []),
            "year": record.get("year"),
            "venue": record.get("venue"),
            "abstract_for_private_summary_only": abstract,
            "allowed_categories": CATEGORIES,
        }
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write new Korean paper summaries. Do not copy or translate abstract sentences verbatim. "
                        "Return strict JSON with ai_summary_ko, relevance_score, relevance_note_ko, tags, categories."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(prompt, ensure_ascii=False),
                },
            ],
        )
        content = response.choices[0].message.content or "{}"
        payload = json.loads(_extract_json(content))
        return _sanitize_generated(payload)
    except Exception as exc:  # Fallback keeps scheduled jobs from failing on optional AI issues.
        print(f"OpenAI summary fallback for '{record.get('title', '')}': {exc}")
        return None


def _fallback_summary(record: dict[str, Any], abstract: str) -> dict[str, Any]:
    title = record.get("title", "이 논문")
    venue = record.get("venue") or "학술 문헌"
    year = record.get("year") or "연도 미상"
    categories = _classify(record, abstract)
    tags = _tags(record, abstract, categories)
    score = _score(record, abstract, categories)

    summary = (
        f"{title}은(는) {year}년 {venue}에 보고된 연구로, "
        f"{', '.join(categories)} 관점에서 다중재료 적층제조 문헌 추적에 포함할 만한 항목입니다. "
        "제목과 공개 메타데이터를 기준으로 볼 때 재료 조성, 설계 자동화, 제조 경로 중 하나 이상과 연결됩니다."
    )
    note = (
        f"DM filament, FGAM, computational design 추적 관점에서 "
        f"{', '.join(tags[:3])} 키워드와의 연결성이 있어 관련성 {score}/10로 분류했습니다."
    )
    return {
        "ai_summary_ko": summary,
        "relevance_score": score,
        "relevance_note_ko": note,
        "tags": tags[:6],
        "categories": categories[:2],
    }


def _classify(record: dict[str, Any], abstract: str) -> list[str]:
    text = _text(record, abstract)
    scored = []
    for category, terms in KEYWORDS.items():
        score = sum(2 if term in text else 0 for term in terms)
        if score:
            scored.append((score, category))
    if not scored:
        return ["다중재료 적층제조"]
    return [category for _, category in sorted(scored, reverse=True)[:2]]


def _tags(record: dict[str, Any], abstract: str, categories: list[str]) -> list[str]:
    text = _text(record, abstract)
    tags = [tag for tag, terms in TAG_MAP.items() if any(term in text for term in terms)]
    for category in categories:
        if category not in tags and len(tags) < 6:
            tags.append(category)
    return tags or ["적층제조", "문헌추적", "메타데이터"]


def _score(record: dict[str, Any], abstract: str, categories: list[str]) -> int:
    text = _text(record, abstract)
    core_terms = [
        "multi-material",
        "multimaterial",
        "functionally graded",
        "digital material filament",
        "blended fdm",
        "computational design",
        "material distribution",
        "toolpath",
        "material switching",
        "purge",
    ]
    score = 4 + sum(1 for term in core_terms if term in text)
    score += min(len(categories), 2)
    return max(1, min(10, score))


def _text(record: dict[str, Any], abstract: str) -> str:
    return " ".join(
        [
            record.get("title", ""),
            record.get("venue", ""),
            " ".join(record.get("authors", [])),
            abstract or "",
        ]
    ).lower()


def _sanitize_generated(payload: dict[str, Any]) -> dict[str, Any]:
    categories = [category for category in payload.get("categories", []) if category in CATEGORIES][:2]
    tags = [str(tag).strip() for tag in payload.get("tags", []) if str(tag).strip()][:6]
    score = int(payload.get("relevance_score", 5))
    return {
        "ai_summary_ko": str(payload.get("ai_summary_ko", "")).strip(),
        "relevance_score": max(1, min(10, score)),
        "relevance_note_ko": str(payload.get("relevance_note_ko", "")).strip(),
        "tags": tags or ["적층제조", "문헌추적"],
        "categories": categories or ["다중재료 적층제조"],
    }


def _extract_json(content: str) -> str:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    return match.group(0) if match else content
