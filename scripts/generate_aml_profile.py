"""Generate an AML lab profile from seed papers."""

from __future__ import annotations

import os
from collections import Counter
from typing import Any

from aml_common import AML_TERMS, NEGATIVE_TERMS, PROFILE_PATH, load_json, now_iso, paper_text, seed_path, write_json


def generate_profile(use_ai_profile: bool = False) -> dict[str, Any]:
    path = seed_path()
    if not path.exists():
        raise FileNotFoundError(f"AML seed file not found: {path}")
    seeds = load_json(path, [])
    if not isinstance(seeds, list) or not seeds:
        raise ValueError(f"AML seed file must contain a non-empty list: {path}")

    profile = None
    if use_ai_profile and os.getenv("OPENAI_API_KEY"):
        profile = _try_ai_profile(seeds)
    if not profile:
        profile = _fallback_profile(seeds)
    write_json(PROFILE_PATH, profile)
    return profile


def _fallback_profile(seeds: list[dict[str, Any]]) -> dict[str, Any]:
    text = " ".join(paper_text(seed).lower() for seed in seeds)
    positive = _rank_terms(text, AML_TERMS, minimum=1)
    if not positive:
        positive = AML_TERMS[:12]
    negative = NEGATIVE_TERMS
    representative = [
        {
            "id": seed.get("id") or seed.get("doi") or seed.get("title", ""),
            "title": seed.get("title", ""),
            "doi": seed.get("doi", ""),
            "year": seed.get("year"),
            "journal": seed.get("journal") or seed.get("venue", ""),
        }
        for seed in seeds[:20]
    ]
    return {
        "profile_name": "AML lab recommendation profile",
        "generated_at": now_iso(),
        "source_seed_path": str(seed_path()),
        "seed_count": len(seeds),
        "core_research_areas": [
            "multi-material additive manufacturing",
            "functionally graded additive manufacturing",
            "digital material filament and blended FDM",
            "4D printing and soft active materials",
            "computational design for material distribution",
        ],
        "methodological_interests": [
            "fused filament fabrication",
            "toolpath-aware design",
            "embedding-based literature recommendation",
            "deterministic topic scoring",
        ],
        "application_interests": [
            "soft robotics",
            "mechanical metamaterials",
            "sensors",
            "liquid crystal elastomers",
            "hydrogels",
            "projection micro-stereolithography",
        ],
        "high_relevance_criteria": [
            "Directly connects material distribution or toolpaths to multi-material AM.",
            "Uses FDM/FFF, DM filament, FGAM, 4D printing, LCEs, hydrogels, sensors, or metamaterials.",
            "Provides design or fabrication methods useful for AML lab research directions.",
        ],
        "low_relevance_criteria": [
            "Only studies metal AM process parameters without material design relevance.",
            "Only studies powder bed fusion defects or selective laser melting without AML topic overlap.",
            "Only discusses biomedical scaffolds without multi-material, gradient, or design relevance.",
            "Broad review papers with weak connection to AML seed topics.",
        ],
        "positive_keywords": positive,
        "negative_keywords": negative,
        "representative_seed_papers": representative,
    }


def _rank_terms(text: str, terms: list[str], minimum: int = 1) -> list[str]:
    counts = Counter()
    for term in terms:
        count = text.count(term.lower())
        if count >= minimum:
            counts[term] = count
    return [term for term, _ in counts.most_common(30)]


def _try_ai_profile(seeds: list[dict[str, Any]]) -> dict[str, Any] | None:
    try:
        from openai import OpenAI

        client = OpenAI()
        seed_brief = [
            {
                "title": seed.get("title", ""),
                "doi": seed.get("doi", ""),
                "journal": seed.get("journal", ""),
                "year": seed.get("year"),
                "abstract": str(seed.get("abstract", ""))[:1200],
            }
            for seed in seeds[:30]
        ]
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Create a concise AML lab paper-recommendation profile as strict JSON. "
                        "Do not include raw abstracts. Include core_research_areas, methodological_interests, "
                        "application_interests, high_relevance_criteria, low_relevance_criteria, "
                        "positive_keywords, negative_keywords."
                    ),
                },
                {"role": "user", "content": str(seed_brief)},
            ],
        )
        payload = response.choices[0].message.content or "{}"
        import json

        profile = json.loads(payload)
        profile["profile_name"] = "AML lab recommendation profile"
        profile["generated_at"] = now_iso()
        profile["source_seed_path"] = str(seed_path())
        profile["seed_count"] = len(seeds)
        profile["representative_seed_papers"] = [
            {
                "id": seed.get("id") or seed.get("doi") or seed.get("title", ""),
                "title": seed.get("title", ""),
                "doi": seed.get("doi", ""),
                "year": seed.get("year"),
                "journal": seed.get("journal") or seed.get("venue", ""),
            }
            for seed in seeds[:20]
        ]
        return profile
    except Exception as exc:
        print(f"AI profile generation skipped/fell back: {exc}")
        return None


if __name__ == "__main__":
    generate_profile(use_ai_profile=os.getenv("AML_USE_AI_PROFILE", "false").lower() == "true")
