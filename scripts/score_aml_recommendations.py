"""Score AML recommendation candidates with deterministic logic by default."""

from __future__ import annotations

import os
from typing import Any

from aml_common import (
    AML_TERMS,
    CANDIDATE_EMBEDDINGS_PATH,
    CANDIDATE_POOL_PATH,
    EMBEDDING_MODEL,
    NEGATIVE_TERMS,
    PROFILE_PATH,
    PUBLIC_OUTPUT_PATH,
    RECOMMENDATION_LOG_PATH,
    ROUTE_SCORES,
    SCORING_DEBUG_PATH,
    SEED_EMBEDDINGS_PATH,
    average_embedding,
    candidate_key,
    clamp01,
    cosine_similarity,
    load_json,
    normalize_key,
    now_iso,
    paper_text,
    public_paper,
    recommendation_level,
    stable_hash,
    write_json,
)


def score_recommendations(
    max_candidates: int = 200,
    use_ai_judge: bool = False,
    use_ai_reason: bool = False,
) -> dict[str, Any]:
    profile = load_json(PROFILE_PATH, {})
    pool = load_json(CANDIDATE_POOL_PATH, {"candidates": []})
    candidates = pool.get("candidates", [])[: max(1, max_candidates)]
    seed_embeddings = load_json(SEED_EMBEDDINGS_PATH, {"items": []}).get("items", [])
    candidate_embeddings = _build_candidate_embeddings(candidates)
    scored = []
    for candidate in candidates:
        score = _score_one(candidate, profile, seed_embeddings, candidate_embeddings)
        if use_ai_judge and 0.35 < score["aml_score"] < 0.80:
            score = _apply_ai_judge(score)
        if use_ai_reason and score["recommendation_level"] in {"High", "Possible"}:
            ai_reason = _ai_reason(score)
            if ai_reason:
                score["why_recommended"] = ai_reason
                score["reason_source"] = "openai"
        scored.append(score)

    scored.sort(key=lambda item: (item["aml_score"], item.get("year") or 0), reverse=True)
    updated_at = now_iso()
    public_items = [public_paper(item, updated_at) for item in scored if item["recommendation_level"] != "Exclude"]
    write_json(PUBLIC_OUTPUT_PATH, public_items)
    write_json(SCORING_DEBUG_PATH, {"updated_at": updated_at, "items": scored})
    write_json(
        RECOMMENDATION_LOG_PATH,
        {
            "updated_at": updated_at,
            "candidate_count": len(candidates),
            "public_count": len(public_items),
            "use_ai_judge": use_ai_judge,
            "use_ai_reason": use_ai_reason,
            "level_counts": _level_counts(scored),
        },
    )
    return {
        "items": scored,
        "public_items": public_items,
        "level_counts": _level_counts(scored),
        "candidate_count": len(candidates),
        "public_output": str(PUBLIC_OUTPUT_PATH),
    }


def _build_candidate_embeddings(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    cached = load_json(CANDIDATE_EMBEDDINGS_PATH, {"items": []})
    by_key = {item.get("candidate_key"): item for item in cached.get("items", [])}
    if not os.getenv("OPENAI_API_KEY"):
        return by_key
    from openai import OpenAI

    client = OpenAI()
    changed = False
    for candidate in candidates:
        key = candidate_key(candidate)
        text = paper_text(candidate)
        text_hash = stable_hash(text)
        existing = by_key.get(key)
        if existing and existing.get("text_hash") == text_hash and existing.get("embedding"):
            continue
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=text[:8000])
        by_key[key] = {
            "candidate_key": key,
            "title": candidate.get("title", ""),
            "doi": candidate.get("doi", ""),
            "text_hash": text_hash,
            "embedding": response.data[0].embedding,
            "embedding_model": EMBEDDING_MODEL,
            "created_at": now_iso(),
        }
        changed = True
    if changed:
        write_json(CANDIDATE_EMBEDDINGS_PATH, {"items": list(by_key.values()), "updated_at": now_iso()})
    return by_key


def _score_one(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    seed_embeddings: list[dict[str, Any]],
    candidate_embeddings: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    text = paper_text(candidate)
    text_lower = text.lower()
    candidate_embedding = (candidate_embeddings.get(candidate_key(candidate)) or {}).get("embedding", [])
    seed_vectors = [item.get("embedding", []) for item in seed_embeddings if item.get("embedding")]
    profile_vector = average_embedding(seed_vectors)
    seed_sims = [cosine_similarity(candidate_embedding, vector) for vector in seed_vectors] if candidate_embedding else []
    profile_similarity = cosine_similarity(candidate_embedding, profile_vector) if candidate_embedding and profile_vector else 0.0
    max_seed_similarity = max(seed_sims) if seed_sims else 0.0
    mean_seed_similarity = sum(seed_sims) / len(seed_sims) if seed_sims else 0.0
    semantic_similarity = 0.50 * profile_similarity + 0.35 * max_seed_similarity + 0.15 * mean_seed_similarity

    matched_topics = _matched_topics(text_lower, profile)
    keyword_score = _keyword_score(text_lower, matched_topics, profile)
    route_score = _route_score(candidate.get("discovery_routes", []))
    recency_score = _recency_score(candidate.get("year"))
    venue_score = _venue_score(candidate.get("journal") or candidate.get("venue", ""))

    if not candidate_embedding:
        semantic_similarity = 0.65 * keyword_score + 0.20 * route_score + 0.10 * recency_score + 0.05 * venue_score
        profile_similarity = semantic_similarity
        max_seed_similarity = semantic_similarity
        mean_seed_similarity = semantic_similarity

    aml_score = clamp01(
        0.60 * semantic_similarity
        + 0.20 * keyword_score
        + 0.10 * route_score
        + 0.05 * recency_score
        + 0.05 * venue_score
    )
    top_seed = _top_seed(seed_embeddings, seed_sims)
    level = recommendation_level(aml_score)
    result = dict(candidate)
    result.update(
        {
            "profile_similarity": round(profile_similarity, 4),
            "max_seed_similarity": round(max_seed_similarity, 4),
            "mean_seed_similarity": round(mean_seed_similarity, 4),
            "semantic_similarity": round(semantic_similarity, 4),
            "keyword_score": round(keyword_score, 4),
            "route_score": round(route_score, 4),
            "recency_score": round(recency_score, 4),
            "venue_score": round(venue_score, 4),
            "aml_score": round(aml_score, 4),
            "recommendation_level": level,
            "matched_topics": matched_topics[:8],
            "related_seed_papers": [top_seed] if top_seed else [],
            "why_recommended": _template_reason(matched_topics, top_seed, candidate.get("discovery_routes", []), aml_score),
            "reason_source": "template",
        }
    )
    return result


def _matched_topics(text_lower: str, profile: dict[str, Any]) -> list[str]:
    terms = list(dict.fromkeys((profile.get("positive_keywords") or []) + AML_TERMS))
    return [term for term in terms if term.lower() in text_lower][:12]


def _keyword_score(text_lower: str, matched_topics: list[str], profile: dict[str, Any]) -> float:
    positive_terms = list(dict.fromkeys((profile.get("positive_keywords") or []) + AML_TERMS))
    negative_terms = list(dict.fromkeys((profile.get("negative_keywords") or []) + NEGATIVE_TERMS))
    positive_hits = sum(1 for term in positive_terms if term.lower() in text_lower)
    negative_hits = sum(1 for term in negative_terms if term.lower() in text_lower)
    return clamp01((positive_hits / 8.0) - (negative_hits * 0.08) + (0.05 if matched_topics else 0.0))


def _route_score(routes: list[str]) -> float:
    if not routes:
        return 0.0
    return max(ROUTE_SCORES.get(route, 0.3) for route in routes)


def _recency_score(year: Any) -> float:
    try:
        year_int = int(year)
    except (TypeError, ValueError):
        return 0.4
    if year_int >= 2026:
        return 1.0
    if year_int == 2025:
        return 0.85
    if year_int == 2024:
        return 0.7
    return 0.35


def _venue_score(venue: str) -> float:
    text = normalize_key(venue)
    if not text:
        return 0.3
    if "additive manufacturing" in text:
        return 1.0
    if "nature" in text or "science" in text:
        return 0.95
    if "advanced materials" in text or "soft robotics" in text:
        return 0.8
    return 0.5


def _top_seed(seed_embeddings: list[dict[str, Any]], seed_sims: list[float]) -> dict[str, Any] | None:
    if not seed_embeddings or not seed_sims:
        return None
    index = max(range(len(seed_sims)), key=lambda idx: seed_sims[idx])
    seed = seed_embeddings[index]
    return {"title": seed.get("title", ""), "doi": seed.get("doi", ""), "similarity": round(seed_sims[index], 4)}


def _template_reason(matched_topics: list[str], top_seed: dict[str, Any] | None, routes: list[str], score: float) -> str:
    topics = ", ".join(matched_topics[:3]) if matched_topics else "AML seed-paper topics"
    seed_title = (top_seed or {}).get("title") or "the AML core seed set"
    route_text = ", ".join(routes) if routes else "candidate screening"
    return (
        f"Recommended because this paper matches {topics} and was found through {route_text}. "
        f"It is closest to {seed_title}; deterministic AML score: {score:.2f}."
    )


def _apply_ai_judge(score: dict[str, Any]) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        return score
    try:
        from openai import OpenAI

        client = OpenAI()
        prompt = {
            "title": score.get("title", ""),
            "journal": score.get("journal", ""),
            "year": score.get("year"),
            "matched_topics": score.get("matched_topics", []),
            "deterministic_aml_score": score.get("aml_score"),
        }
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Judge AML lab relevance. Return strict JSON with relevance_score integer 0-5, "
                        "matched_topics array, why_recommended short string, exclude_reason string or null, confidence 0-1."
                    ),
                },
                {"role": "user", "content": str(prompt)},
            ],
        )
        import json

        payload = json.loads(response.choices[0].message.content or "{}")
        ai_score = clamp01(float(payload.get("relevance_score", 0)) / 5.0)
        revised = clamp01(0.75 * float(score["aml_score"]) + 0.25 * ai_score)
        score["deterministic_aml_score"] = score["aml_score"]
        score["ai_relevance_score"] = round(ai_score, 4)
        score["aml_score"] = round(revised, 4)
        score["recommendation_level"] = recommendation_level(revised)
        if payload.get("matched_topics"):
            score["matched_topics"] = payload["matched_topics"][:8]
        if payload.get("why_recommended"):
            score["why_recommended"] = str(payload["why_recommended"])[:500]
            score["reason_source"] = "openai_judge"
        if payload.get("exclude_reason"):
            score["exclude_reason"] = str(payload["exclude_reason"])[:300]
    except Exception as exc:
        print(f"AI judge skipped for '{score.get('title', '')}': {exc}")
    return score


def _ai_reason(score: dict[str, Any]) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return ""
    try:
        from openai import OpenAI

        client = OpenAI()
        top_seed = (score.get("related_seed_papers") or [{}])[0] or {}
        prompt = {
            "title": score.get("title", ""),
            "journal": score.get("journal") or score.get("venue", ""),
            "year": score.get("year"),
            "authors": (score.get("authors") or [])[:6],
            "matched_topics": score.get("matched_topics", [])[:8],
            "aml_score_0_to_1": score.get("aml_score"),
            "recommendation_level": score.get("recommendation_level", ""),
            "discovery_routes": _public_route_labels(score.get("discovery_routes", [])[:5]),
            "nearest_seed_title": top_seed.get("title", ""),
            "nearest_seed_similarity": top_seed.get("similarity"),
        }
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Write one concise public-safe English sentence explaining why this paper is recommended "
                        "for an AML research profile. Use the supplied metadata only. Do not mention internal route "
                        "names such as existing_keyword_pool, deterministic scoring, JSON fields, or hidden data. "
                        "Do not reproduce abstracts or claim results not present in the metadata."
                    ),
                },
                {"role": "user", "content": str(prompt)},
            ],
        )
        return (response.choices[0].message.content or "").strip()[:500]
    except Exception as exc:
        print(f"AI reason skipped for '{score.get('title', '')}': {exc}")
        return ""


def _public_route_labels(routes: list[str]) -> list[str]:
    labels = {
        "existing_keyword_pool": "existing curated paper pool",
        "crossref_keyword_search": "Crossref keyword search",
    }
    return [labels.get(route, "candidate screening") for route in routes]


def _level_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    levels = {"High": 0, "Possible": 0, "Watch": 0, "Exclude": 0}
    for item in items:
        levels[item.get("recommendation_level", "Exclude")] = levels.get(item.get("recommendation_level", "Exclude"), 0) + 1
    return levels


if __name__ == "__main__":
    result = score_recommendations(
        max_candidates=int(os.getenv("AML_MAX_CANDIDATES", "200")),
        use_ai_judge=os.getenv("AML_USE_AI_JUDGE", "false").lower() == "true",
        use_ai_reason=os.getenv("AML_USE_AI_REASON", "false").lower() == "true",
    )
    print(result["level_counts"])
