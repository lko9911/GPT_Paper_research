"""Score AML recommendation candidates with deterministic logic by default."""

from __future__ import annotations

import os
from typing import Any

from aml_common import (
    AML_TERMS,
    PAPERS_PATH,
    CANDIDATE_EMBEDDINGS_PATH,
    CANDIDATE_POOL_PATH,
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    PRIVATE_DIR,
    PROFILE_PATH,
    PUBLIC_OUTPUT_PATH,
    RECOMMENDATION_LOG_PATH,
    SCORING_DEBUG_PATH,
    SEED_EMBEDDINGS_PATH,
    average_embedding,
    candidate_key,
    clamp01,
    cosine_similarity,
    embed_text,
    embedding_provider_available,
    load_json,
    normalize_key,
    now_iso,
    paper_text,
    public_paper,
    recommendation_level,
    is_trusted_publication,
    stable_hash,
    write_json,
)

PUBLIC_AML_SCORE_THRESHOLD = float(
    os.getenv("AML_PUBLIC_SCORE_THRESHOLD", "0.905" if EMBEDDING_PROVIDER == "local" else "0.75")
)
ALLOW_LOCAL_PUBLIC_WRITE = os.getenv("AML_ALLOW_LOCAL_PUBLIC_WRITE", "false").strip().lower() in {"1", "true", "yes", "y"}
SCORE_WEIGHTS = {
    "semantic_similarity": 0.80,
    "recency_score": 0.10,
    "venue_score": 0.10,
}


def score_recommendations(
    max_candidates: int = 0,
    use_ai_judge: bool = False,
    use_ai_reason: bool = False,
) -> dict[str, Any]:
    profile = load_json(PROFILE_PATH, {})
    pool = load_json(CANDIDATE_POOL_PATH, {"candidates": []})
    pool_candidates = pool.get("candidates", [])
    candidates = pool_candidates if max_candidates <= 0 else pool_candidates[:max_candidates]
    source_summaries = _source_paper_summaries()
    seed_embeddings = load_json(SEED_EMBEDDINGS_PATH, {"items": []}).get("items", [])
    candidate_embeddings = _build_candidate_embeddings(candidates)
    scored = []
    for candidate in candidates:
        _merge_source_summary(candidate, source_summaries)
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
    previous_public = _previous_public_recommendations()
    current_public_items = [
        public_paper(item, updated_at)
        for item in scored
        if item["recommendation_level"] != "Exclude"
        and float(item.get("aml_score") or 0.0) >= PUBLIC_AML_SCORE_THRESHOLD
        and is_trusted_publication(item)
    ]
    current_public_items = _mark_new_recommendations(current_public_items, previous_public, updated_at)
    public_items = _merge_public_recommendations(current_public_items, previous_public, updated_at)
    low_venue_trust_excluded = sum(
        1
        for item in scored
        if item["recommendation_level"] != "Exclude"
        and float(item.get("aml_score") or 0.0) >= PUBLIC_AML_SCORE_THRESHOLD
        and not is_trusted_publication(item)
    )
    public_output_path = _public_output_path()
    write_json(public_output_path, public_items)
    write_json(SCORING_DEBUG_PATH, {"updated_at": updated_at, "items": scored})
    write_json(
        RECOMMENDATION_LOG_PATH,
        {
            "updated_at": updated_at,
            "candidate_count": len(candidates),
            "candidate_pool_count": len(pool_candidates),
            "score_limit": "all" if max_candidates <= 0 else max_candidates,
            "public_count": len(public_items),
            "public_write_enabled": public_output_path == PUBLIC_OUTPUT_PATH,
            "public_output": str(public_output_path),
            "public_score_threshold": PUBLIC_AML_SCORE_THRESHOLD,
            "public_low_venue_trust_excluded": low_venue_trust_excluded,
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
        "candidate_pool_count": len(pool_candidates),
        "public_score_threshold": PUBLIC_AML_SCORE_THRESHOLD,
        "public_output": str(public_output_path),
    }


def _public_output_path():
    if EMBEDDING_PROVIDER == "local" and not ALLOW_LOCAL_PUBLIC_WRITE:
        return PRIVATE_DIR / "aml_recommended_papers_local_preview.json"
    return PUBLIC_OUTPUT_PATH


def _previous_public_recommendations() -> dict[str, dict[str, Any]]:
    items = load_json(PUBLIC_OUTPUT_PATH, [])
    if not isinstance(items, list):
        return {}
    return {
        candidate_key(item): item
        for item in items
        if candidate_key(item) not in {"doi:", "title:"}
    }


def _mark_new_recommendations(
    public_items: list[dict[str, Any]],
    previous_public: dict[str, dict[str, Any]],
    updated_at: str,
) -> list[dict[str, Any]]:
    for item in public_items:
        key = candidate_key(item)
        previous = previous_public.get(key)
        is_new = previous is None
        first_added = (
            item.get("first_added")
            if is_new
            else previous.get("first_added") or previous.get("updated_at") or item.get("updated_at")
        )
        item["first_added"] = first_added or updated_at
        item["last_updated"] = updated_at
        item["is_new_recommendation"] = is_new
        item["is_weekly_new"] = is_new
        item["weekly_new"] = is_new
    return public_items


def _merge_public_recommendations(
    current_items: list[dict[str, Any]],
    previous_public: dict[str, dict[str, Any]],
    updated_at: str,
) -> list[dict[str, Any]]:
    merged = {key: dict(item) for key, item in previous_public.items()}
    for item in current_items:
        key = candidate_key(item)
        if not key or key in {"doi:", "title:"}:
            continue
        previous = merged.get(key)
        if previous:
            merged[key] = _merge_public_item(previous, item, updated_at)
        else:
            merged[key] = item
    return sorted(
        merged.values(),
        key=lambda item: (float(item.get("aml_score") or 0.0), int(item.get("year") or 0), str(item.get("title") or "")),
        reverse=True,
    )


def _merge_public_item(previous: dict[str, Any], current: dict[str, Any], updated_at: str) -> dict[str, Any]:
    merged = dict(previous)
    for key, value in current.items():
        if _has_value(value):
            merged[key] = value
    merged["first_added"] = previous.get("first_added") or previous.get("updated_at") or current.get("first_added") or updated_at
    merged["last_updated"] = updated_at
    if _has_ai_summary(previous) and not _has_ai_summary(current):
        for key in (
            "ai_summary_en",
            "relevance_note_en",
            "summary_provider",
            "openai_summary_applied",
            "local_summary_applied",
            "summary_model",
            "summary_source",
            "abstract_used_for_summary",
        ):
            if key in previous:
                merged[key] = previous[key]
    return merged


def _has_ai_summary(item: dict[str, Any]) -> bool:
    provider = str(item.get("summary_provider") or "").strip().lower()
    return provider in {"openai", "local"} or item.get("openai_summary_applied") is True or item.get("local_summary_applied") is True


def _has_value(value: Any) -> bool:
    return value is not None and value != "" and value != []


def _source_paper_summaries() -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for paper in load_json(PAPERS_PATH, []):
        summary = str(paper.get("ai_summary_en") or "").strip()
        if not summary:
            continue
        key = candidate_key(paper)
        summaries[key] = {
            "ai_summary_en": summary,
            "relevance_note_en": paper.get("relevance_note_en", ""),
            "summary_provider": paper.get("summary_provider", "metadata"),
            "openai_summary_applied": bool(paper.get("openai_summary_applied")),
            "local_summary_applied": bool(paper.get("local_summary_applied")),
            "summary_model": paper.get("summary_model", ""),
            "summary_source": "curated_paper_pool",
            "openalex_venue_rank": paper.get("openalex_venue_rank", ""),
            "openalex_venue_rank_number": paper.get("openalex_venue_rank_number"),
            "openalex_venue_rank_score": paper.get("openalex_venue_rank_score"),
            "openalex_venue_rank_percentile": paper.get("openalex_venue_rank_percentile"),
            "openalex_venue_rank_basis": paper.get("openalex_venue_rank_basis", ""),
        }
    return summaries


def _merge_source_summary(candidate: dict[str, Any], source_summaries: dict[str, dict[str, Any]]) -> None:
    source = source_summaries.get(candidate_key(candidate))
    if not source:
        return
    for key, value in source.items():
        if value:
            candidate[key] = value


def refresh_public_recommendation_reasons() -> dict[str, Any]:
    """Rewrite reasons for the already-published AML recommendations.

    This path is useful on GitHub Actions when the private AML seed file is not
    available but the public recommendation list already exists.
    """
    items = load_json(PUBLIC_OUTPUT_PATH, [])
    if not isinstance(items, list) or not items:
        raise FileNotFoundError(f"AML public recommendation output not found: {PUBLIC_OUTPUT_PATH}")
    refreshed = 0
    skipped = 0
    for item in items:
        if item.get("recommendation_level") not in {"High", "Possible"}:
            skipped += 1
            continue
        reason = _ai_reason(item)
        if not reason:
            skipped += 1
            continue
        item["why_recommended"] = reason
        item["reason_source"] = "openai"
        item["updated_at"] = now_iso()
        refreshed += 1
    write_json(PUBLIC_OUTPUT_PATH, items)
    return {
        "public_output": str(PUBLIC_OUTPUT_PATH),
        "public_count": len(items),
        "reasons_refreshed": refreshed,
        "reasons_skipped": skipped,
    }


def _build_candidate_embeddings(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    cached = load_json(CANDIDATE_EMBEDDINGS_PATH, {"items": []})
    by_key = {item.get("candidate_key"): item for item in cached.get("items", [])}
    if not embedding_provider_available():
        print(f"{EMBEDDING_PROVIDER} embedding provider is not available; using existing candidate embedding cache only.")
        return by_key
    changed = False
    for candidate in candidates:
        key = candidate_key(candidate)
        text = paper_text(candidate)
        text_hash = stable_hash(text)
        existing = by_key.get(key)
        if existing and existing.get("text_hash") == text_hash and existing.get("embedding"):
            continue
        embedding = embed_text(text)
        if not embedding:
            continue
        by_key[key] = {
            "candidate_key": key,
            "title": candidate.get("title", ""),
            "doi": candidate.get("doi", ""),
            "text_hash": text_hash,
            "embedding": embedding,
            "embedding_model": EMBEDDING_MODEL,
            "embedding_provider": EMBEDDING_PROVIDER,
            "created_at": now_iso(),
        }
        changed = True
    if changed:
        write_json(
            CANDIDATE_EMBEDDINGS_PATH,
            {
                "items": list(by_key.values()),
                "embedding_model": EMBEDDING_MODEL,
                "embedding_provider": EMBEDDING_PROVIDER,
                "updated_at": now_iso(),
            },
        )
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
    recency_score = _recency_score(candidate.get("year"))
    venue_score = _venue_score(candidate.get("journal") or candidate.get("venue", ""))

    if not candidate_embedding:
        semantic_similarity = 0.0
        profile_similarity = semantic_similarity
        max_seed_similarity = semantic_similarity
        mean_seed_similarity = semantic_similarity

    aml_score = clamp01(
        SCORE_WEIGHTS["semantic_similarity"] * semantic_similarity
        + SCORE_WEIGHTS["recency_score"] * recency_score
        + SCORE_WEIGHTS["venue_score"] * venue_score
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
            "recency_score": round(recency_score, 4),
            "venue_score": round(venue_score, 4),
            "score_weights": SCORE_WEIGHTS,
            "aml_score": round(aml_score, 4),
            "recommendation_level": level,
            "matched_topics": matched_topics[:8],
            "related_seed_papers": [top_seed] if top_seed else [],
            "why_recommended": _template_reason(matched_topics, top_seed, aml_score),
            "reason_source": "template",
        }
    )
    return result


def _matched_topics(text_lower: str, profile: dict[str, Any]) -> list[str]:
    terms = list(dict.fromkeys((profile.get("positive_keywords") or []) + AML_TERMS))
    return [term for term in terms if term.lower() in text_lower][:12]


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


def _template_reason(matched_topics: list[str], top_seed: dict[str, Any] | None, score: float) -> str:
    topics = ", ".join(matched_topics[:3]) if matched_topics else "AML seed-paper topics"
    seed_title = (top_seed or {}).get("title") or "the AML core seed set"
    return (
        f"Recommended because this paper matches {topics}. "
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


def _level_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    levels = {"High": 0, "Possible": 0, "Watch": 0, "Exclude": 0}
    for item in items:
        levels[item.get("recommendation_level", "Exclude")] = levels.get(item.get("recommendation_level", "Exclude"), 0) + 1
    return levels


if __name__ == "__main__":
    result = score_recommendations(
        max_candidates=int((os.getenv("AML_MAX_CANDIDATES") or "0").strip() or "0"),
        use_ai_judge=os.getenv("AML_USE_AI_JUDGE", "false").lower() == "true",
        use_ai_reason=os.getenv("AML_USE_AI_REASON", "false").lower() == "true",
    )
    print(result["level_counts"])
