"""Shared helpers for the manual AML recommendation pipeline."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
ARCHIVE_PAPERS_PATH = ROOT / "data" / "archive_papers.json"
PROFILE_PATH = ROOT / "data" / "profiles" / "aml_lab_profile.json"
PRIVATE_DIR = ROOT / "data" / "private"
DEFAULT_SEED_PATH = PRIVATE_DIR / "aml_seed_papers_core_enriched.json"
SEED_EMBEDDINGS_PATH = PRIVATE_DIR / "aml_seed_embeddings.json"
CANDIDATE_POOL_PATH = PRIVATE_DIR / "aml_candidate_pool.json"
CANDIDATE_EMBEDDINGS_PATH = PRIVATE_DIR / "aml_candidate_embeddings.json"
SCORING_DEBUG_PATH = PRIVATE_DIR / "aml_scoring_debug.json"
RECOMMENDATION_LOG_PATH = PRIVATE_DIR / "aml_recommendation_log.json"
PUBLIC_OUTPUT_PATH = ROOT / "public" / "data" / "aml_recommended_papers.json"

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

AML_TERMS = [
    "multi-material additive manufacturing",
    "multimaterial",
    "fused filament fabrication",
    "fdm",
    "fff",
    "b-fdm",
    "digital material filament",
    "dm filament",
    "functionally graded materials",
    "functional gradients",
    "computational design",
    "material distribution control",
    "material switching",
    "toolpath-aware design",
    "toolpath",
    "4d printing",
    "soft robotics",
    "mechanical metamaterials",
    "metamaterial",
    "sensors",
    "sensor",
    "liquid crystal elastomers",
    "liquid crystal elastomer",
    "lce",
    "hydrogels",
    "hydrogel",
    "projection micro-stereolithography",
    "micro-stereolithography",
    "stereolithography",
]

NEGATIVE_TERMS = [
    "metal additive manufacturing",
    "powder bed fusion",
    "selective laser melting",
    "laser powder bed fusion",
    "biomedical scaffold",
    "scaffold",
    "process parameter optimization",
]

CORE_VENUES = {
    "additive manufacturing": 1.0,
    "nature communications": 1.0,
    "nature materials": 1.0,
    "science": 1.0,
    "science advances": 0.95,
    "science robotics": 0.95,
    "advanced materials": 0.85,
    "acs applied materials & interfaces": 0.75,
    "virtual and physical prototyping": 0.75,
}

ROUTE_SCORES = {
    "similar_to_core_seed": 1.0,
    "cited_by_core_seed": 1.0,
    "existing_keyword_pool": 0.7,
    "ai_expanded_queries": 0.6,
    "recent_openalex_topic_or_venue": 0.5,
    "venue_scan_only": 0.4,
    "topic_scan_only": 0.4,
}


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_path() -> Path:
    return Path(os.getenv("AML_SEED_PATH", str(DEFAULT_SEED_PATH)))


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def candidate_key(record: dict[str, Any]) -> str:
    doi = normalize_doi(record.get("doi", ""))
    if doi:
        return f"doi:{doi}"
    return f"title:{normalize_key(record.get('title', ''))}"


def normalize_doi(value: str | None) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def paper_text(record: dict[str, Any]) -> str:
    fields = [
        record.get("title", ""),
        record.get("abstract", ""),
        record.get("_abstract", ""),
        record.get("journal", ""),
        record.get("venue", ""),
        " ".join(record.get("tags", []) or []),
        " ".join(record.get("categories", []) or []),
    ]
    return normalize_text(" ".join(str(field) for field in fields if field))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return max(0.0, min(1.0, (dot / (norm_a * norm_b) + 1.0) / 2.0))


def average_embedding(embeddings: list[list[float]]) -> list[float]:
    clean = [embedding for embedding in embeddings if embedding]
    if not clean:
        return []
    width = len(clean[0])
    return [sum(embedding[i] for embedding in clean if len(embedding) == width) / len(clean) for i in range(width)]


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def recommendation_level(score: float) -> str:
    if score >= 0.75:
        return "High"
    if score >= 0.50:
        return "Possible"
    if score >= 0.30:
        return "Watch"
    return "Exclude"


def public_paper(record: dict[str, Any], updated_at: str) -> dict[str, Any]:
    doi = normalize_doi(record.get("doi", ""))
    url = record.get("url") or (f"https://doi.org/{doi}" if doi else "")
    authors = record.get("authors", []) or []
    return {
        "title": record.get("title", ""),
        "doi": doi,
        "journal": record.get("journal") or record.get("venue", ""),
        "year": record.get("year"),
        "authors": authors,
        "last_author": _last_author_name(record, authors),
        "author_details": record.get("author_details", []) or [],
        "corresponding_authors": record.get("corresponding_authors", []) or [],
        "corresponding_author_available": bool(record.get("corresponding_authors")),
        "url": url,
        "citation": record.get("citation", ""),
        "recommendation_level": record.get("recommendation_level", ""),
        "aml_score": round(float(record.get("aml_score", 0.0)), 4),
        "matched_topics": record.get("matched_topics", [])[:8],
        "why_recommended": record.get("why_recommended", ""),
        "reason_source": record.get("reason_source", "template"),
        "discovery_routes": record.get("discovery_routes", [])[:8],
        "related_seed_papers": record.get("related_seed_papers", [])[:3],
        "ai_summary_en": record.get("ai_summary_en", ""),
        "relevance_note_en": record.get("relevance_note_en", ""),
        "summary_provider": record.get("summary_provider", "metadata"),
        "openai_summary_applied": bool(record.get("openai_summary_applied")),
        "summary_source": record.get("summary_source", ""),
        "updated_at": updated_at,
    }


def _last_author_name(record: dict[str, Any], authors: list[Any]) -> str:
    for author in reversed(authors):
        if isinstance(author, str) and author.strip():
            return author.strip()
        if isinstance(author, dict):
            name = str(
                author.get("name")
                or author.get("display_name")
                or author.get("full_name")
                or ""
            ).strip()
            if name:
                return name
    details = record.get("author_details", []) or []
    for author in reversed(details):
        if isinstance(author, dict):
            name = str(
                author.get("name")
                or author.get("display_name")
                or author.get("full_name")
                or ""
            ).strip()
            if name:
                return name
    return ""
