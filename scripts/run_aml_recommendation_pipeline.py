"""Run the manual AML recommendation pipeline."""

from __future__ import annotations

import argparse
import os
from typing import Any

from build_aml_seed_embeddings import build_seed_embeddings
from collect_aml_candidates import collect_candidates
from generate_aml_profile import generate_profile
from score_aml_recommendations import score_recommendations


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AML recommendation pipeline")
    parser.add_argument("--mode", default=os.getenv("AML_MODE", "score_existing"), choices=["score_existing", "collect_and_score", "full_refresh"])
    parser.add_argument("--max-candidates", type=int, default=int(os.getenv("AML_MAX_CANDIDATES", "200")))
    parser.add_argument("--use-ai-judge", action="store_true", default=os.getenv("AML_USE_AI_JUDGE", "false").lower() == "true")
    parser.add_argument("--use-ai-reason", action="store_true", default=os.getenv("AML_USE_AI_REASON", "false").lower() == "true")
    parser.add_argument("--use-ai-profile", action="store_true", default=os.getenv("AML_USE_AI_PROFILE", "false").lower() == "true")
    args = parser.parse_args()

    summary = run_pipeline(
        mode=args.mode,
        max_candidates=args.max_candidates,
        use_ai_judge=args.use_ai_judge,
        use_ai_reason=args.use_ai_reason,
        use_ai_profile=args.use_ai_profile,
    )
    print("AML recommendation summary")
    for key, value in summary.items():
        print(f"- {key}: {value}")


def run_pipeline(
    mode: str,
    max_candidates: int,
    use_ai_judge: bool = False,
    use_ai_reason: bool = False,
    use_ai_profile: bool = False,
) -> dict[str, Any]:
    profile = generate_profile(use_ai_profile=use_ai_profile)
    seed_result = build_seed_embeddings()
    candidate_result = collect_candidates(mode=mode, max_candidates=max_candidates)
    score_result = score_recommendations(
        max_candidates=max_candidates,
        use_ai_judge=use_ai_judge,
        use_ai_reason=use_ai_reason,
    )
    return {
        "seed_papers_loaded": profile.get("seed_count", 0),
        "seed_embeddings_generated": seed_result.get("generated", 0),
        "candidate_count": candidate_result.get("candidate_count", 0),
        "candidates_scored": score_result.get("candidate_count", 0),
        "level_counts": score_result.get("level_counts", {}),
        "ai_judge_used": use_ai_judge,
        "ai_reason_used": use_ai_reason,
        "public_output": score_result.get("public_output", ""),
    }


if __name__ == "__main__":
    main()
