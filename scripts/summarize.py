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

TAG_CATEGORY_ALIASES = {
    "툴패스": "툴패스 계획",
    "경로계획": "그래프 탐색 / 경로 계획 알고리즘",
    "재료분포": "재료분포 최적화",
    "퍼지 감소": "재료 전환 / 퍼지 감소",
    "계산설계": "계산설계",
    "MMAM": "다중재료 적층제조",
    "FGAM": "기능성 구배 적층제조",
    "AI/ML": "적층제조를 위한 AI 및 머신러닝",
}


def summarize_record(record: dict[str, Any], allow_openai: bool = True) -> dict[str, Any]:
    """Add Korean summary fields to a record.

    OPENAI_API_KEY enables model-based generation. Without it, this function
    creates a conservative Korean summary from transient abstract signals and
    metadata, avoiding any verbatim abstract reuse.
    """

    abstract = record.get("_abstract", "")
    if allow_openai and os.getenv("OPENAI_API_KEY"):
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
    summary = _abstract_based_summary(record, abstract, categories, tags, year, venue)
    note = (
        f"DM filament, FGAM, computational design 추적 관점에서 "
        f"{', '.join(tags[:3])} 키워드와 연결되어 관련성 {score}/10로 분류했습니다."
    )
    return {
        "ai_summary_ko": summary,
        "relevance_score": score,
        "relevance_note_ko": note,
        "tags": tags[:6],
        "categories": categories[:2],
    }


def _abstract_based_summary(
    record: dict[str, Any],
    abstract: str,
    categories: list[str],
    tags: list[str],
    year: Any,
    venue: str,
) -> str:
    title = record.get("title", "이 논문")
    text = _text(record, abstract)
    focus = _join_phrases(
        _matched_phrases(
            text,
            [
                ("digital tectonics", "디지털 제작과 건축적 구성"),
                ("ornamental", "재료 표현과 장식적 설계 사고"),
                ("material articulation", "재료의 연결과 표현 방식"),
                ("multi-material", "다중재료 구조"),
                ("multimaterial", "다중재료 구조"),
                ("functionally graded", "기능성 구배 재료"),
                ("graded", "구배 재료"),
                ("blended fdm", "혼합 FDM 공정"),
                ("digital material filament", "디지털 재료 필라멘트"),
                ("toolpath", "툴패스 설계"),
                ("path planning", "경로 계획"),
                ("topology optimization", "위상 최적화"),
                ("computational design", "계산설계"),
                ("robotic", "로봇 기반 제조"),
                ("4d printing", "4D 프린팅"),
                ("metamaterial", "메타물질"),
                ("liquid crystal elastomer", "액정 엘라스토머"),
            ],
        ),
        fallback=", ".join(tags[:2] or categories[:1]),
    )
    method = _join_phrases(
        _matched_phrases(
            text,
            [
                ("conceptual", "개념적 논의"),
                ("discuss", "개념적 논의"),
                ("propose", "개념 제안"),
                ("framework", "설계 프레임워크"),
                ("method", "방법론"),
                ("optimization", "최적화"),
                ("simulation", "시뮬레이션"),
                ("machine learning", "머신러닝"),
                ("deep learning", "딥러닝"),
                ("reinforcement learning", "강화학습"),
                ("experiment", "실험 검증"),
                ("fabrication", "제작 실험"),
                ("analysis", "분석"),
                ("review", "문헌 검토"),
                ("survey", "문헌 조사"),
            ],
        ),
        fallback="공개 초록의 문제 설정과 접근법",
    )
    outcome = _join_phrases(
        _matched_phrases(
            text,
            [
                ("performance", "성능"),
                ("mechanical", "기계적 특성"),
                ("accuracy", "정밀도"),
                ("efficiency", "공정 효율"),
                ("reusability", "재사용성"),
                ("sustainability", "지속가능성"),
                ("design", "설계 가능성"),
                ("manufacturing", "제조 적용성"),
                ("application", "응용 가능성"),
            ],
        ),
        fallback="설계와 제조 관점의 의미",
    )

    if abstract:
        return (
            f"{title}은(는) {year}년 {venue}에 발표된 연구로, {_object_phrase(focus)} 중심 주제로 다룹니다. "
            f"초록 내용을 바탕으로 보면 연구는 {_object_phrase(method)} 통해 {outcome}을 검토하며, "
            "제조·설계 문헌 추적에서 참고할 만한 시사점을 제공합니다."
        )

    return (
        f"{title}은(는) {year}년 {venue}에 발표된 항목으로, 공개 메타데이터상 {focus}와 관련됩니다. "
        "초록이 제공되지 않아 제목·venue·키워드만으로 보수적으로 요약했으며, 자세한 내용은 DOI 원문 확인이 필요합니다."
    )


def _matched_phrases(text: str, term_phrases: list[tuple[str, str]], limit: int = 3) -> list[str]:
    phrases: list[str] = []
    for term, phrase in term_phrases:
        if term in text and phrase not in phrases:
            phrases.append(phrase)
        if len(phrases) >= limit:
            break
    return phrases


def _join_phrases(phrases: list[str], fallback: str) -> str:
    clean = [phrase for phrase in phrases if phrase]
    if not clean:
        return fallback or "관련 주제"
    if len(clean) == 1:
        return clean[0]
    return ", ".join(clean[:-1]) + f" 및 {clean[-1]}"


def _object_phrase(text: str) -> str:
    if not text:
        return "관련 주제를"
    return f"{text}을" if _has_final_consonant(text[-1]) else f"{text}를"


def _has_final_consonant(char: str) -> bool:
    code = ord(char)
    if 0xAC00 <= code <= 0xD7A3:
        return (code - 0xAC00) % 28 != 0
    return False


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
    return _dedupe_tags(tags, categories) or ["적층제조", "문헌추적", "메타데이터"]


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
    tags = [str(tag).strip() for tag in payload.get("tags", []) if str(tag).strip()]
    score = int(payload.get("relevance_score", 5))
    return {
        "ai_summary_ko": str(payload.get("ai_summary_ko", "")).strip(),
        "relevance_score": max(1, min(10, score)),
        "relevance_note_ko": str(payload.get("relevance_note_ko", "")).strip(),
        "tags": _dedupe_tags(tags, categories)[:6] or ["적층제조", "문헌추적"],
        "categories": categories or ["다중재료 적층제조"],
    }


def _dedupe_tags(tags: list[str], categories: list[str]) -> list[str]:
    category_set = set(categories)
    seen: set[str] = set()
    cleaned = []
    for tag in tags:
        if not tag or tag in seen:
            continue
        seen.add(tag)
        if tag in category_set:
            continue
        alias_category = TAG_CATEGORY_ALIASES.get(tag)
        if alias_category and alias_category in category_set:
            continue
        cleaned.append(tag)
    return cleaned


def _extract_json(content: str) -> str:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    return match.group(0) if match else content
