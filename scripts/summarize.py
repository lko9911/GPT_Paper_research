"""Generate English summaries and relevance metadata for new papers."""

from __future__ import annotations

import json
import os
import re
import ast
from typing import Any

CATEGORIES = [
    "Reviews and Surveys",
    "Multi-material AM",
    "Functionally Graded AM",
    "Blended FDM / Digital Material Filament",
    "Computational Design",
    "Material Distribution Optimization",
    "Toolpath Planning",
    "Material Switching / Purge Reduction",
    "Graph Search / Path Planning",
    "AI and Machine Learning for AM",
]

KEYWORDS = {
    "Reviews and Surveys": ["review", "survey", "state of the art", "overview"],
    "Multi-material AM": ["multi-material", "multimaterial", "multiple material"],
    "Functionally Graded AM": ["functionally graded", "fgam", "graded material"],
    "Blended FDM / Digital Material Filament": ["blended fdm", "digital material filament", "dm filament", "filament blending"],
    "Computational Design": ["computational design", "inverse design", "design automation", "generative design"],
    "Material Distribution Optimization": ["material distribution", "topology optimization", "distribution optimization"],
    "Toolpath Planning": ["toolpath", "tool path", "slicing", "deposition path"],
    "Material Switching / Purge Reduction": ["material switching", "purge", "waste reduction", "transition"],
    "Graph Search / Path Planning": ["graph search", "path planning", "traveling salesman", "routing"],
    "AI and Machine Learning for AM": ["machine learning", "deep learning", "artificial intelligence", "neural"],
}

TAG_MAP = {
    "FGAM": ["functionally graded", "fgam", "graded"],
    "MMAM": ["multi-material", "multimaterial", "multiple material"],
    "DM filament": ["digital material filament", "dm filament", "blended fdm", "filament blending"],
    "LCE": ["liquid crystal elastomer", "liquid-crystal elastomer", " lce "],
    "4D printing": ["4d printing", "4-d printing", "four-dimensional printing", "shape morphing", "shape-morphing"],
    "Metamaterials": ["metamaterial", "metamaterials", "mechanical metamaterial"],
    "Digital fabrication": ["digital tectonics", "digital craftsmanship", "large-scale additive manufacturing"],
    "Toolpath strategy": ["toolpath", "tool path", "woven toolpath", "slicing"],
    "Material behavior": ["material behaviour", "material behavior", "material intelligence"],
    "Computational design": ["computational design", "inverse design", "generative design"],
    "Material distribution": ["material distribution", "topology optimization"],
    "Material switching": ["purge", "material switching", "waste reduction"],
    "Path planning": ["path planning", "graph search", "routing"],
    "Machine learning": ["machine learning", "deep learning", "neural", "artificial intelligence"],
    "DLP": ["dlp", "digital light process", "digital light processing", "digital light projection"],
    "SLA": ["stereolithography", "stereo lithography", " sla "],
    "Vat photopolymerization": ["vat photopolymerization", "vat photopolymerisation", "vat polymerization", "vat polymerisation"],
    "Volumetric AM": [
        "volumetric additive manufacturing",
        "volumetric printing",
        "computed axial lithography",
        "tomographic printing",
        "tomographic volumetric",
    ],
    "FDM/Material extrusion": ["fdm", "fused deposition", "material extrusion", "filament"],
    "Soft robotics": [
        "soft robotic",
        "soft robotics",
        "soft gripper",
        "soft robotic finger",
        "soft robotic fingers",
        "fin-ray",
        "fin ray",
        "pneumatic actuator",
        "bioinspired gripper",
    ],
    "Self-driving Labs": [
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
    ],
    "Digital Twins": [
        "digital twin",
        "digital twins",
        "digital twinning",
        "virtual twin",
        "real-to-twin",
        "twin-enabled",
        "twin-driven",
        "process twin",
        "machine twin",
    ],
    "Manufacturing automation": [
        "manufacturing automation",
        "automated manufacturing",
        "automation",
        "automated",
        "autonomous",
        "closed-loop",
        "closed loop",
        "monitoring",
        "in-situ",
        "in situ",
    ],
    "Robot-based Manufacturing": [
        "robot-based manufacturing",
        "robotic manufacturing",
        "robotic fabrication",
        "robot-assisted manufacturing",
        "robotic assembly",
        "robotic machining",
        "robotic welding",
    ],
    "Process optimization": ["process optimization", "process optimisation", "parameter optimization", "parameter optimisation"],
}

TAG_CATEGORY_ALIASES = {
    "Toolpath strategy": "Toolpath Planning",
    "Path planning": "Graph Search / Path Planning",
    "Material distribution": "Material Distribution Optimization",
    "Material switching": "Material Switching / Purge Reduction",
    "Computational design": "Computational Design",
    "MMAM": "Multi-material AM",
    "FGAM": "Functionally Graded AM",
    "Machine learning": "AI and Machine Learning for AM",
    "Soft robotics": "Computational Design",
}

GENERIC_TAGS = {"적층제조", "문헌추적", "메타데이터", "3D 프린팅"}

TAG_ALIASES = {
    "다중재료": "MMAM",
    "다중 재료": "MMAM",
    "Multi-material AM": "MMAM",
    "Multi-material": "MMAM",
    "Multimaterial": "MMAM",
    "multi-material": "MMAM",
    "multimaterial": "MMAM",
    "기능성 구배": "FGAM",
    "디지털 제작": "Digital fabrication",
    "툴패스 전략": "Toolpath strategy",
    "툴패스": "Toolpath strategy",
    "Toolpath": "Toolpath strategy",
    "Toolpath planning": "Toolpath strategy",
    "재료 거동": "Material behavior",
    "계산설계": "Computational design",
    "Computational Design": "Computational design",
    "재료분포": "Material distribution",
    "Material Distribution": "Material distribution",
    "퍼지 감소": "Material switching",
    "경로계획": "Path planning",
    "Path Planning": "Path planning",
    "AI/ML": "Machine learning",
    "ML": "Machine learning",
    "Machine Learning": "Machine learning",
    "Deep Learning": "Machine learning",
    "deep learning": "Machine learning",
    "Reinforcement Learning": "Machine learning",
    "reinforcement learning": "Machine learning",
    "딥러닝": "Machine learning",
    "강화 학습": "Machine learning",
    "기계 학습": "Machine learning",
    "머신 러닝": "Machine learning",
    "메타물질": "Metamaterials",
    "FDM": "FDM/Material extrusion",
    "FDM / Material Extrusion": "FDM/Material extrusion",
    "Material extrusion": "FDM/Material extrusion",
    "Digital Light Processing": "DLP",
    "Digital light processing": "DLP",
    "Digital Light Process": "DLP",
    "Digital light process": "DLP",
    "디지털 광 처리": "DLP",
    "DLP 프린터": "DLP",
    "Stereolithography": "SLA",
    "stereolithography": "SLA",
    "Vat photopolymerization": "Vat photopolymerization",
    "vat photopolymerization": "Vat photopolymerization",
    "vat photopolymerisation": "Vat photopolymerization",
    "Robotic autonomous experimentation": "Self-driving Labs",
    "Soft robotics": "Soft robotics",
    "Soft Robotics": "Soft robotics",
    "Soft robot": "Soft robotics",
    "Soft robots": "Soft robotics",
    "소프트 로보틱스": "Soft robotics",
    "소프트 로봇": "Soft robotics",
    "소프트 액추에이터": "Soft robotics",
    "Autonomous experimentation": "Self-driving Labs",
    "Self-driving lab": "Self-driving Labs",
    "Self-driving Labs": "Self-driving Labs",
    "Closed-loop experiment": "Self-driving Labs",
    "Digital twin": "Digital Twins",
    "Digital twins": "Digital Twins",
    "Digital Twins": "Digital Twins",
    "4D Printing": "4D printing",
    "Active Materials": "Active materials",
}


def summarize_record(record: dict[str, Any], allow_openai: bool = True) -> dict[str, Any]:
    """Add English summary fields to a record.

    OPENAI_API_KEY enables model-based generation. Without it, this function
    creates a conservative English summary from transient abstract signals and
    metadata, avoiding any verbatim abstract reuse.
    """

    abstract = record.get("_abstract", "")
    if allow_openai and os.getenv("OPENAI_API_KEY"):
        generated = _summarize_with_openai(record, abstract)
        if generated:
            record.update(generated)
            record["_summary_provider"] = "openai"
            return record

    record.update(_fallback_summary(record, abstract))
    record["_summary_provider"] = "fallback"
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
                        "You write new English paper summaries. Do not copy or translate abstract sentences verbatim. "
                        "Do not closely paraphrase the abstract, preserve its sentence order, or reuse long technical noun-phrase chains from it. "
                        "Each answer must be newly written from the bibliographic facts and high-level meaning only; use compact synthesis, not abstract rewriting. "
                        "The ai_summary_en field must answer exactly these five labeled questions in English, each in one concise sentence: "
                        "1. Topic -, 2. Problem -, 3. Method -, 4. Key Result -, 5. Takeaway -. "
                        "For ai_summary_en, avoid eight-or-more-word overlaps with the abstract except unavoidable paper titles, material names, or standard method names. "
                        "Return strict JSON with ai_summary_en, relevance_score, relevance_note_en, tags, categories."
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
        return _sanitize_generated(payload, _text(record, abstract))
    except Exception as exc:  # Fallback keeps scheduled jobs from failing on optional AI issues.
        print(f"OpenAI summary fallback for '{record.get('title', '')}': {exc}")
        return None


def _fallback_summary(record: dict[str, Any], abstract: str) -> dict[str, Any]:
    title = record.get("title", "This paper")
    venue = record.get("venue") or "an unknown venue"
    year = record.get("year") or "an undated year"
    categories = _classify(record, abstract)
    tags = _tags(record, abstract, categories)
    score = _score(record, abstract, categories)
    tag_phrase = _english_list(tags[:3] or categories[:2]) or "manufacturing research"
    summary = _format_english_five_question_summary(
        f"{title} is a {year} paper from {venue} about {tag_phrase}.",
        f"It is tracked because it addresses a design, process, material, or automation issue connected to {tag_phrase}.",
        "The fallback summary is generated from title, venue, metadata, topic tags, and any transient abstract signal without reproducing abstract text.",
        "The detailed finding should be verified in the DOI source; this tracker records the paper's topic-level contribution and relevance.",
        f"It is useful for this tracker as comparison or background literature for {tag_phrase}; current relevance score is {score}/10.",
    )
    note = f"Relevant to the tracker through {tag_phrase}; score: {score}/10."
    return {
        "ai_summary_en": summary,
        "relevance_score": score,
        "relevance_note_en": note,
        "tags": tags[:6],
        "categories": categories[:2],
    }


def _format_english_five_question_summary(subject: str, problem: str, approach: str, finding: str, usefulness: str) -> str:
    return "\n".join(
        [
            f"1. Topic - {subject}",
            f"2. Problem - {problem}",
            f"3. Method - {approach}",
            f"4. Key Result - {finding}",
            f"5. Takeaway - {usefulness}",
        ]
    )


def _english_list(items: list[str]) -> str:
    clean = [str(item).strip() for item in items if str(item).strip()]
    if not clean:
        return ""
    if len(clean) == 1:
        return clean[0]
    if len(clean) == 2:
        return f"{clean[0]} and {clean[1]}"
    return f"{', '.join(clean[:-1])}, and {clean[-1]}"


def _abstract_based_summary(
    record: dict[str, Any],
    abstract: str,
    categories: list[str],
    tags: list[str],
    year: Any,
    venue: str,
    score: int,
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
        subject = _study_subject(title, text, focus)
        problem = _study_problem(text, focus)
        approach = _study_approach(text, method)
        contribution = _study_contribution(text, outcome)
        usefulness = _study_takeaway(tags, categories, score, text)
        return _format_five_question_summary(subject, problem, approach, contribution, usefulness)

    subject = f"{title}은(는) {year}년 {venue}에 발표된 항목으로, 공개 메타데이터상 {focus}와 관련됩니다."
    return _format_five_question_summary(
        subject,
        "초록이 제공되지 않아 구체적인 문제 설정은 DOI 원문 확인이 필요합니다.",
        "제목, venue, DOI 메타데이터, 키워드 신호를 바탕으로 보수적으로 분류했습니다.",
        "공개 메타데이터만으로는 핵심 결과를 단정하지 않고, 관련 주제 여부만 확인했습니다.",
        _study_takeaway(tags, categories, score, text),
    )


def _study_subject(title: str, text: str, focus: str) -> str:
    if has_terms(text, ["ornament", "large-scale additive manufacturing"]):
        return "대형 적층제조에서 장식을 표면 장식이 아니라 재료 거동, 공정 흔적, 제작 논리가 드러나는 설계 요소로 해석합니다."
    if has_terms(text, ["liquid crystal elastomer", "4d printing"]):
        return "액정 엘라스토머를 4D 프린팅으로 제작해 열이나 자극에 따라 형상이 변하는 구조를 구현합니다."
    if has_terms(text, ["continuous fiber", "liquid crystal elastomer"]):
        return "연속섬유 보강과 액정 엘라스토머 프린팅을 결합해 변형 성능과 구조적 강성을 함께 다룹니다."
    if has_terms(text, ["toolpath", "optimization"]):
        return "툴패스와 공정 조건을 설계 변수로 삼아 적층제조 결과의 품질과 효율을 개선하는 방법을 다룹니다."
    if has_terms(text, ["multi-material", "3d printing"]) or has_terms(text, ["multimaterial", "3d printing"]):
        return "서로 다른 재료를 한 구조 안에 배치하거나 전환하는 다중재료 3D 프린팅 문제를 다룹니다."
    if has_terms(text, ["functionally graded"]) or has_terms(text, ["graded", "additive manufacturing"]):
        return "재료 조성이나 물성을 위치에 따라 달리하는 기능성 구배 적층제조를 다룹니다."
    if has_terms(text, ["robot", "additive manufacturing"]):
        return "로봇 기반 적층제조에서 경로, 자세, 제작 가능성을 함께 고려하는 제조 문제를 다룹니다."
    if has_terms(text, ["machine learning"]) or has_terms(text, ["deep learning"]):
        return "제조 데이터와 학습 기반 모델을 이용해 공정 이해나 설계 자동화를 개선하는 연구입니다."
    return f"{focus}와 관련된 제조·설계 문제를 구체적인 연구 대상으로 삼습니다."


def _study_approach(text: str, method: str) -> str:
    details = []
    if has_terms(text, ["case studies"]):
        details.append("디자인 사례를 비교하고")
    if has_terms(text, ["agent-based"]):
        details.append("agent-based 조형 로직을 활용하며")
    if has_terms(text, ["data-informed"]):
        details.append("데이터 기반 변조를 적용하고")
    if has_terms(text, ["woven toolpath"]):
        details.append("직조형 툴패스 전략을 설계에 통합합니다")
    if has_terms(text, ["simulation"]):
        details.append("시뮬레이션으로 거동을 예측합니다")
    if has_terms(text, ["experiment"]) or has_terms(text, ["fabrication"]):
        details.append("제작 실험으로 구현 가능성을 확인합니다")
    if has_terms(text, ["optimization"]):
        details.append("최적화 절차로 설계안을 탐색합니다")
    if details:
        sentence = _join_korean_clauses(details)
        sentence = sentence.rstrip(".")
        if sentence.endswith("합니다"):
            return f"접근 방식은 {sentence[:-3]}하는 것입니다."
        if sentence.endswith("다"):
            return f"접근 방식은 {sentence}는 점입니다."
        return f"접근 방식은 {sentence}는 점입니다."
    return f"{method}을(를) 통해 문제를 분석하고 구현 방향을 제시합니다."


def _study_contribution(text: str, outcome: str) -> str:
    if has_terms(text, ["toolpath", "material behaviour"]) or has_terms(text, ["toolpath", "material behavior"]):
        return "핵심 기여는 툴패스와 재료 반응을 단순 제작 수단이 아니라 형태와 공간 구성을 만드는 설계 언어로 연결한 점입니다."
    if has_terms(text, ["matter", "performance", "application"]):
        return "핵심 기여는 재료, 성능, 적용 가능성을 하나의 설계 논리 안에서 함께 해석한 점입니다."
    if has_terms(text, ["mechanical", "performance"]):
        return "핵심 기여는 프린팅 전략이 기계적 성능과 구조 응답에 미치는 영향을 구체적으로 보여준 점입니다."
    if has_terms(text, ["accuracy"]) or has_terms(text, ["efficiency"]):
        return "핵심 기여는 제조 정확도나 공정 효율을 개선할 수 있는 실질적인 설계 기준을 제시한 점입니다."
    return f"핵심 기여는 {outcome}을(를) 제조·설계 관점에서 해석할 수 있게 한 점입니다."


def _study_problem(text: str, focus: str) -> str:
    if has_terms(text, ["ornament", "large-scale additive manufacturing"]):
        return "대형 적층제조에서 장식, 툴패스, 재료 거동이 분리되어 해석되는 문제를 다룹니다."
    if has_terms(text, ["liquid crystal elastomer", "4d printing"]):
        return "자극 반응 재료를 원하는 형상 변화와 구조 성능으로 안정적으로 프린팅하는 문제를 다룹니다."
    if has_terms(text, ["multi-material", "3d printing"]) or has_terms(text, ["multimaterial", "3d printing"]):
        return "서로 다른 재료의 배치, 전환, 계면 특성을 원하는 기능으로 연결하는 문제를 다룹니다."
    if has_terms(text, ["toolpath", "optimization"]):
        return "툴패스 선택이 품질, 시간, 재료 사용량, 성능에 미치는 영향을 줄이는 문제를 다룹니다."
    if has_terms(text, ["robot", "path planning"]):
        return "로봇 제조에서 경로 계획과 제작 가능성을 동시에 만족시키는 문제를 다룹니다."
    if has_terms(text, ["machine learning"]) or has_terms(text, ["deep learning"]):
        return "제조 공정의 복잡한 변수와 결과 사이의 관계를 데이터 기반으로 파악하는 문제를 다룹니다."
    return f"{focus}와 관련된 설계·제조상의 병목을 이해하거나 완화하려는 문제를 다룹니다."


def _study_takeaway(tags: list[str], categories: list[str], score: int, text: str) -> str:
    topic = _join_phrases(tags[:3] or categories[:2], "제조·설계")
    if has_terms(text, ["toolpath"]) and ("material behaviour" in text or "material behavior" in text):
        return "툴패스와 재료 거동은 단순한 제작 조건이 아니라 구조 성능과 표현을 결정하는 설계 변수라는 점이 핵심 메시지입니다."
    if any(tag in tags for tag in ["LCE", "4D printing", "Metamaterials"]):
        return "자극 반응 재료와 4D 프린팅을 결합하면 형상 변화 구조를 설계 가능한 제조 대상으로 다룰 수 있다는 점이 핵심 메시지입니다."
    if any(tag in tags for tag in ["MMAM", "FGAM", "DM filament", "FDM/Material extrusion"]):
        return "재료 배치와 공정 설계를 함께 최적화해야 다중재료 제조의 성능 이점을 얻을 수 있다는 점이 핵심 메시지입니다."
    return f"{topic} 관점에서 관련성 {score}/10로 평가되며, 핵심 메시지는 제조 방법과 설계 목표를 함께 해석해야 한다는 점입니다."


def _format_five_question_summary(
    subject: str,
    problem: str,
    approach: str,
    finding: str,
    usefulness: str,
) -> str:
    return "\n".join(
        [
            f"1. Topic - 이 논문은 무엇을 다루는가? {subject}",
            f"2. Problem - 어떤 문제나 한계를 해결하려는가? {problem}",
            f"3. Method - 어떤 방법이나 접근을 사용했는가? {approach}",
            f"4. Key Result - 가장 중요한 결과는 무엇인가? {finding}",
            f"5. Takeaway - 그래서 이 논문의 핵심 메시지는 무엇인가? {usefulness}",
        ]
    )


def has_terms(text: str, terms: list[str]) -> bool:
    return all(term in text for term in terms)


def _join_korean_clauses(clauses: list[str]) -> str:
    if not clauses:
        return ""
    if len(clauses) == 1:
        return clauses[0]
    return ", ".join(clauses[:-1]) + f" 마지막으로 {clauses[-1]}"


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
        return ["Multi-material AM"]
    return [category for _, category in sorted(scored, reverse=True)[:2]]


def _tags(record: dict[str, Any], abstract: str, categories: list[str]) -> list[str]:
    text = _text(record, abstract)
    tags = []
    for tag, terms in TAG_MAP.items():
        if not any(term in text for term in terms):
            continue
        if tag == "Digital Twins" and not _is_manufacturing_digital_twin(text):
            continue
        tags.append(tag)
    for category in categories:
        if category not in tags and len(tags) < 6:
            tags.append(category)
    return _dedupe_tags(tags, categories) or _fallback_tags(text, categories)


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
    if _is_manufacturing_digital_twin(text):
        score = max(score, 7)
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


def _sanitize_generated(payload: dict[str, Any], source_text: str = "") -> dict[str, Any]:
    categories = [category for category in payload.get("categories", []) if category in CATEGORIES][:2]
    tags = [str(tag).strip() for tag in payload.get("tags", []) if str(tag).strip()]
    cleaned_tags = _dedupe_tags(tags, categories, source_text)[:6] or _fallback_tags("", categories)
    score = int(payload.get("relevance_score", 5))
    if source_text and _is_manufacturing_digital_twin(source_text):
        score = max(score, 7)
    return {
        "ai_summary_en": _normalize_generated_summary(payload.get("ai_summary_en"), _en_summary_labels()),
        "relevance_score": max(1, min(10, score)),
        "relevance_note_en": str(payload.get("relevance_note_en", "")).strip(),
        "tags": cleaned_tags,
        "categories": categories or ["Multi-material AM"],
    }


def _ko_summary_labels() -> list[str]:
    return [
        "Topic - 이 논문은 무엇을 다루는가?",
        "Problem - 어떤 문제나 한계를 해결하려는가?",
        "Method - 어떤 방법이나 접근을 사용했는가?",
        "Key Result - 가장 중요한 결과는 무엇인가?",
        "Takeaway - 그래서 이 논문의 핵심 메시지는 무엇인가?",
    ]


def _en_summary_labels() -> list[str]:
    return [
        "Topic -",
        "Problem -",
        "Method -",
        "Key Result -",
        "Takeaway -",
    ]


def _normalize_generated_summary(value: Any, labels: list[str]) -> str:
    if isinstance(value, dict):
        lines = []
        for index, label in enumerate(labels, start=1):
            short_label = label.split("-", 1)[0].strip()
            answer = value.get(str(index)) or value.get(index) or value.get(label) or value.get(short_label) or ""
            answer = str(answer).strip()
            if answer:
                lines.append(f"{index}. {label} {answer}")
        if lines:
            return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for index, answer in enumerate(value[:5], start=1):
            answer = str(answer).strip()
            if answer:
                lines.append(f"{index}. {labels[index - 1]} {answer}")
        if lines:
            return "\n".join(lines)
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = ast.literal_eval(text)
                if isinstance(parsed, (dict, list)):
                    return _normalize_generated_summary(parsed, labels)
            except (SyntaxError, ValueError):
                pass
        return text
    return str(value or "").strip()


def _dedupe_tags(tags: list[str], categories: list[str], source_text: str = "") -> list[str]:
    category_set = set(categories)
    seen: set[str] = set()
    cleaned = []
    for tag in tags:
        tag = _canonical_tag(tag)
        if not tag or tag in GENERIC_TAGS or tag in seen:
            continue
        if tag == "Digital Twins" and source_text and not _is_manufacturing_digital_twin(source_text):
            continue
        seen.add(tag)
        if tag in category_set:
            continue
        alias_category = TAG_CATEGORY_ALIASES.get(tag)
        if alias_category and alias_category in category_set:
            continue
        cleaned.append(tag)
    return cleaned


def _is_manufacturing_digital_twin(text: str) -> bool:
    digital_twin_terms = [
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
    return (
        any(term in text for term in digital_twin_terms)
        and any(term in text for term in manufacturing_terms)
        and not any(term in text for term in non_manufacturing_terms)
    )


def _canonical_tag(tag: str) -> str:
    value = str(tag or "").strip()
    if not value:
        return ""
    return TAG_ALIASES.get(value, value)


def _fallback_tags(text: str, categories: list[str]) -> list[str]:
    if "툴패스 계획" in categories:
        return ["Toolpath strategy"]
    if "그래프 탐색 / 경로 계획 알고리즘" in categories:
        return ["Path planning"]
    if "재료분포 최적화" in categories:
        return ["Material distribution"]
    if "재료 전환 / 퍼지 감소" in categories:
        return ["Material switching"]
    if "계산설계" in categories:
        return ["Computational design"]
    if "기능성 구배 적층제조" in categories:
        return ["FGAM"]
    if "적층제조를 위한 AI 및 머신러닝" in categories:
        return ["Machine learning"]
    if "다중재료 적층제조" in categories:
        return ["MMAM"]
    return ["Additive manufacturing"]


def _extract_json(content: str) -> str:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    return match.group(0) if match else content
