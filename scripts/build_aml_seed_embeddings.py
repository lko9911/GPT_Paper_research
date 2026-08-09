"""Build cached embeddings for AML seed papers."""

from __future__ import annotations

from typing import Any

from aml_common import (
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    SEED_EMBEDDINGS_PATH,
    embed_text,
    embedding_provider_available,
    load_json,
    now_iso,
    paper_text,
    seed_path,
    stable_hash,
    write_json,
)


def build_seed_embeddings() -> dict[str, Any]:
    path = seed_path()
    if not path.exists():
        raise FileNotFoundError(f"AML seed file not found: {path}")
    seeds = load_json(path, [])
    cached = load_json(SEED_EMBEDDINGS_PATH, {"items": []})
    cache_by_id = {item.get("seed_id"): item for item in cached.get("items", [])}

    if not embedding_provider_available():
        print(f"{EMBEDDING_PROVIDER} embedding provider is not available; skipping seed embedding generation.")
        return {"items": list(cache_by_id.values()), "generated": 0, "skipped_unavailable": True}

    items = []
    generated = 0
    for seed in seeds:
        seed_id = str(seed.get("id") or seed.get("doi") or stable_hash(seed.get("title", "")))
        text = paper_text(seed)
        text_hash = stable_hash(text)
        existing = cache_by_id.get(seed_id)
        if existing and existing.get("text_hash") == text_hash and existing.get("embedding"):
            items.append(existing)
            continue
        embedding = embed_text(text)
        if not embedding:
            continue
        items.append(
            {
                "seed_id": seed_id,
                "title": seed.get("title", ""),
                "doi": seed.get("doi", ""),
                "text_hash": text_hash,
                "embedding": embedding,
                "embedding_model": EMBEDDING_MODEL,
                "embedding_provider": EMBEDDING_PROVIDER,
                "created_at": now_iso(),
            }
        )
        generated += 1

    payload = {
        "items": items,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_provider": EMBEDDING_PROVIDER,
        "updated_at": now_iso(),
    }
    write_json(SEED_EMBEDDINGS_PATH, payload)
    return {"items": items, "generated": generated, "skipped_unavailable": False}


if __name__ == "__main__":
    result = build_seed_embeddings()
    print(f"Seed embeddings: items={len(result.get('items', []))}, generated={result.get('generated', 0)}")
