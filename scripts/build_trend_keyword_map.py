"""Build a public keyword co-occurrence map for the research tracker.

The output intentionally stores only derived keyword counts and links. It does
not publish abstracts or long source text.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
SITE_META_PATH = ROOT / "data" / "site_meta.json"
OUTPUT_PATH = ROOT / "data" / "trend_keyword_map.json"

KEYWORDS: list[dict[str, Any]] = [
    {"id": "additive-manufacturing", "label": "Additive Manufacturing", "group": "AM", "terms": ["additive manufacturing", "3d printing", "3d print", "printed"]},
    {"id": "multi-material-am", "label": "Multi-material AM", "group": "AM", "terms": ["multi-material", "multimaterial", "multi material", "mmam"]},
    {"id": "functionally-graded-am", "label": "Functionally Graded AM", "group": "AM", "terms": ["functionally graded", "fgam", "graded material", "gradient material"]},
    {"id": "fdm-material-extrusion", "label": "FDM / Material Extrusion", "group": "AM", "terms": ["fdm", "fused deposition", "material extrusion", "filament"]},
    {"id": "vat-photopolymerization", "label": "Vat Photopolymerization", "group": "AM", "terms": ["vat photopolymerization", "vat photopolymerisation", "photopolymerization", "photopolymerisation", "dlp", "stereolithography", "sla"]},
    {"id": "volumetric-am", "label": "Volumetric AM", "group": "AM", "terms": ["volumetric additive", "volumetric printing", "tomographic", "computed axial lithography", "xolography"]},
    {"id": "toolpath-planning", "label": "Toolpath / Path Planning", "group": "Automation", "terms": ["toolpath", "path planning", "trajectory", "routing"]},
    {"id": "process-optimization", "label": "Process Optimization", "group": "Automation", "terms": ["process optimization", "parameter optimization", "optimisation", "optimization", "bayesian optimization"]},
    {"id": "closed-loop-control", "label": "Closed-loop Control", "group": "Automation", "terms": ["closed-loop", "closed loop", "feedback control", "process control", "real-time control"]},
    {"id": "monitoring", "label": "In-situ Monitoring", "group": "Automation", "terms": ["monitoring", "in-situ", "in situ", "sensing", "sensor"]},
    {"id": "digital-twin", "label": "Digital Twin", "group": "AI", "terms": ["digital twin", "digital twins", "twin-enabled", "twin-driven", "virtual twin"]},
    {"id": "machine-learning", "label": "Machine Learning", "group": "AI", "terms": ["machine learning", "ml", "neural", "deep learning", "reinforcement learning", "artificial intelligence", "ai-driven", "ai enabled"]},
    {"id": "surrogate-modeling", "label": "Surrogate Modeling", "group": "AI", "terms": ["surrogate", "reduced-order", "reduced order", "multi-fidelity", "multifidelity"]},
    {"id": "inverse-design", "label": "Inverse Design", "group": "AI", "terms": ["inverse design", "inverse-designed", "generative design", "topology optimization"]},
    {"id": "self-driving-lab", "label": "Self-driving Lab", "group": "AML", "terms": ["self-driving lab", "self driving lab", "self-driving laboratory", "autonomous laboratory", "autonomous lab", "autonomous experimentation"]},
    {"id": "active-learning", "label": "Active Learning", "group": "AML", "terms": ["active learning", "bayesian optimization", "data-efficient", "data efficient"]},
    {"id": "robotic-experimentation", "label": "Robotic Experimentation", "group": "AML", "terms": ["robotic experimentation", "robotic fluid handling", "automated reaction", "robot scientist", "robochem"]},
    {"id": "formulation-discovery", "label": "Formulation Discovery", "group": "AML", "terms": ["formulation discovery", "polymer formulation", "materials discovery", "nanomaterials discovery"]},
    {"id": "4d-printing", "label": "4D Printing", "group": "4D", "terms": ["4d printing", "4d printed", "4d-print"]},
    {"id": "lce", "label": "LCE", "group": "4D", "terms": ["liquid crystal elastomer", "liquid-crystal elastomer", "lce"]},
    {"id": "shape-morphing", "label": "Shape Morphing", "group": "4D", "terms": ["shape morphing", "morphing", "shape change", "shape-changing", "bending", "actuation"]},
    {"id": "stimuli-responsive", "label": "Stimuli-responsive", "group": "4D", "terms": ["stimuli-responsive", "stimulus-responsive", "responsive", "temperature-responsive", "light-responsive", "magneto-active"]},
    {"id": "metamaterials", "label": "Metamaterials", "group": "Materials", "terms": ["metamaterial", "metamaterials", "architected", "lattice", "auxetic", "kirigami", "origami"]},
    {"id": "soft-robotics", "label": "Soft Robotics", "group": "Robotics", "terms": ["soft robotics", "soft robot", "soft robotic", "soft actuator", "soft gripper"]},
    {"id": "robot-manufacturing", "label": "Robotic Manufacturing", "group": "Robotics", "terms": ["robotic manufacturing", "robot-based", "robot-assisted", "robot arm", "industrial robot"]},
    {"id": "composites", "label": "Composites", "group": "Materials", "terms": ["composite", "composites", "fiber", "carbon fiber", "reinforced"]},
    {"id": "alloys-metals", "label": "Metals / Alloys", "group": "Materials", "terms": ["metal", "alloy", "alloys", "stainless steel", "titanium", "aluminum", "inconel", "nitinol"]},
    {"id": "hydrogels", "label": "Hydrogels", "group": "Materials", "terms": ["hydrogel", "hydrogels"]},
    {"id": "sustainability", "label": "Sustainability", "group": "Manufacturing", "terms": ["sustainable", "sustainability", "recycling", "recyclable", "circular"]},
    {"id": "biomedical", "label": "Biomedical Applications", "group": "Application", "terms": ["biomedical", "implant", "medical", "tissue", "nerve", "bone"]},
]

GROUP_CENTERS = {
    "AM": (310, 205),
    "Automation": (525, 210),
    "AI": (620, 120),
    "AML": (710, 300),
    "4D": (285, 350),
    "Materials": (185, 170),
    "Robotics": (540, 365),
    "Manufacturing": (430, 285),
    "Application": (160, 330),
}


def main() -> None:
    papers = load_json(PAPERS_PATH, [])
    reference_date = reference_date_from_meta()
    latest_year = max((int(paper.get("year") or 0) for paper in papers), default=reference_date.year)
    keyword_by_id = {item["id"]: item for item in KEYWORDS}
    node_counts: Counter[str] = Counter()
    recent_counts: Counter[str] = Counter()
    edge_counts: Counter[tuple[str, str]] = Counter()
    edge_recent_counts: Counter[tuple[str, str]] = Counter()

    for paper in papers:
        matched = sorted(match_keywords(paper))
        if len(matched) < 1:
            continue
        is_recent = is_recent_paper(paper, reference_date, latest_year)
        for keyword_id in matched:
            node_counts[keyword_id] += 1
            if is_recent:
                recent_counts[keyword_id] += 1
        for source, target in combinations(matched, 2):
            edge = tuple(sorted((source, target)))
            edge_counts[edge] += 1
            if is_recent:
                edge_recent_counts[edge] += 1

    selected_ids = select_nodes(node_counts, recent_counts)
    nodes = build_nodes(selected_ids, node_counts, recent_counts, keyword_by_id)
    edges = build_edges(selected_ids, edge_counts, edge_recent_counts)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "derived from titles, tags, AI Q5 summaries, relevance notes, and public metadata; abstract text is not published",
        "recent_basis": f"publication year {latest_year}, plus records explicitly marked weekly-new",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Trend keyword map written: nodes={len(nodes)}, edges={len(edges)}, path={OUTPUT_PATH}")


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def reference_date_from_meta() -> datetime:
    meta = load_json(SITE_META_PATH, {})
    value = meta.get("last_run_at_utc") or meta.get("generated_at_utc") or ""
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return datetime.now(timezone.utc)


def is_recent_paper(paper: dict[str, Any], reference_date: datetime, latest_year: int) -> bool:
    if paper.get("is_weekly_new") is True or paper.get("weekly_new") is True:
        return True
    return int(paper.get("year") or 0) >= latest_year


def match_keywords(paper: dict[str, Any]) -> set[str]:
    text = normalize(" ".join([
        str(paper.get("title") or ""),
        " ".join(map(str, paper.get("tags") or [])),
        " ".join(map(str, paper.get("categories") or [])),
        str(paper.get("ai_summary_en") or ""),
        str(paper.get("relevance_note_en") or ""),
        str(paper.get("venue") or ""),
    ]))
    matched = set()
    for keyword in KEYWORDS:
        if any(term_match(text, term) for term in keyword["terms"]):
            matched.add(keyword["id"])
    return matched


def term_match(text: str, term: str) -> bool:
    needle = normalize(term)
    if len(needle) <= 3:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", text))
    return needle in text


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def select_nodes(node_counts: Counter[str], recent_counts: Counter[str]) -> list[str]:
    ranked = sorted(
        node_counts,
        key=lambda item: (recent_counts[item] * 2.4 + node_counts[item] * 0.35, node_counts[item]),
        reverse=True,
    )
    return ranked[:48]


def build_nodes(
    selected_ids: list[str],
    node_counts: Counter[str],
    recent_counts: Counter[str],
    keyword_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for keyword_id in selected_ids:
        groups[keyword_by_id[keyword_id]["group"]].append(keyword_id)
    nodes = []
    max_count = max((node_counts[item] for item in selected_ids), default=1)
    max_recent = max((recent_counts[item] for item in selected_ids), default=1)
    for group, ids in groups.items():
        center_x, center_y = GROUP_CENTERS.get(group, (460, 260))
        radius = 42 + min(34, len(ids) * 2.5)
        for index, keyword_id in enumerate(ids):
            angle = (math.tau * index / max(1, len(ids))) - math.pi / 2
            ring = radius + 12 * (index % 2)
            keyword = keyword_by_id[keyword_id]
            count = node_counts[keyword_id]
            recent = recent_counts[keyword_id]
            trend = (recent / max_recent * 0.7 if max_recent else 0) + (count / max_count * 0.3 if max_count else 0)
            nodes.append({
                "id": keyword_id,
                "label": keyword["label"],
                "group": group,
                "count": count,
                "recent_count": recent,
                "trend_score": round(trend, 4),
                "x": round(center_x + math.cos(angle) * ring, 1),
                "y": round(center_y + math.sin(angle) * ring, 1),
                "radius": round(7 + 16 * math.sqrt(count / max_count), 1),
            })
    return sorted(nodes, key=lambda item: item["trend_score"], reverse=True)


def build_edges(
    selected_ids: list[str],
    edge_counts: Counter[tuple[str, str]],
    edge_recent_counts: Counter[tuple[str, str]],
) -> list[dict[str, Any]]:
    selected = set(selected_ids)
    edges = [
        {
            "source": source,
            "target": target,
            "count": count,
            "recent_count": edge_recent_counts[(source, target)],
        }
        for (source, target), count in edge_counts.items()
        if source in selected and target in selected and count >= 3
    ]
    edges.sort(key=lambda item: (item["recent_count"], item["count"]), reverse=True)
    return edges[:130]


if __name__ == "__main__":
    main()
