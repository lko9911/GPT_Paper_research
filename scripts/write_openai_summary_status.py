"""Write a public status file for the manual OpenAI summary workflow."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATUS_MD = ROOT / "OPENAI_SUMMARY_STATUS.md"
STATUS_JSON = ROOT / "data" / "openai_summary_status.json"
SITE_META = ROOT / "data" / "site_meta.json"


def main() -> None:
    now_utc = datetime.now(UTC).replace(microsecond=0)
    now_kst = now_utc.astimezone(ZoneInfo("Asia/Seoul"))
    site_meta = _load_json(SITE_META, {})

    payload = {
        "checked_at_utc": now_utc.isoformat().replace("+00:00", "Z"),
        "checked_at_kst": now_kst.isoformat(),
        "workflow": os.getenv("GITHUB_WORKFLOW", "OpenAI summary refresh"),
        "event": os.getenv("GITHUB_EVENT_NAME", ""),
        "run_id": os.getenv("GITHUB_RUN_ID", ""),
        "run_number": os.getenv("GITHUB_RUN_NUMBER", ""),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", ""),
        "run_url": _run_url(),
        "ref": os.getenv("GITHUB_REF_NAME", ""),
        "sha": os.getenv("GITHUB_SHA", ""),
        "job_status": os.getenv("OPENAI_JOB_STATUS", ""),
        "summary_phase": os.getenv("OPENAI_SUMMARY_PHASE", ""),
        "confirm_step_outcome": os.getenv("CONFIRM_STEP_OUTCOME", ""),
        "refresh_step_outcome": os.getenv("REFRESH_STEP_OUTCOME", ""),
        "commit_step_outcome": os.getenv("COMMIT_STEP_OUTCOME", ""),
        "deploy_step_outcome": os.getenv("DEPLOY_STEP_OUTCOME", ""),
        "max_summaries": os.getenv("MAX_OPENAI_SUMMARIES", ""),
        "refresh_mode": os.getenv("REFRESH_MODE", ""),
        "confirm_openai_cost": os.getenv("CONFIRM_OPENAI_COST", ""),
        "summary_refresh_model": site_meta.get("summary_refresh_model", ""),
        "summaries_refreshed_last_success": site_meta.get("summaries_refreshed", 0),
        "last_successful_collection_utc": site_meta.get("last_run_at_utc", ""),
        "last_successful_collection_kst": _kst_display(site_meta.get("last_run_at_utc", "")),
        "paper_count": site_meta.get("paper_count", 0),
        "openai_is_manual_only": True,
    }

    STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATUS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATUS_MD.write_text(_markdown(payload), encoding="utf-8")
    print(f"Wrote {STATUS_MD.relative_to(ROOT)} and {STATUS_JSON.relative_to(ROOT)}")


def _markdown(payload: dict[str, object]) -> str:
    status = str(payload.get("job_status") or "unknown")
    phase = str(payload.get("summary_phase") or "")
    run_url = str(payload.get("run_url") or "")
    run_link = f"[{payload.get('run_id')}]({run_url})" if run_url else str(payload.get("run_id") or "-")
    return f"""# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `{payload.get('checked_at_kst')}` KST
- Workflow: `{payload.get('workflow')}`
- Event: `{payload.get('event')}`
- Run: {run_link}
- Job status: `{status}`
- Summary phase: `{phase or status}`
- Confirm step: `{payload.get('confirm_step_outcome') or '-'}`
- Refresh step: `{payload.get('refresh_step_outcome') or '-'}`
- Commit step: `{payload.get('commit_step_outcome') or '-'}`
- Deploy step: `{payload.get('deploy_step_outcome') or '-'}`
- Ref: `{payload.get('ref')}`
- Commit SHA: `{payload.get('sha')}`

## Requested Inputs

- Max summaries: `{payload.get('max_summaries') or '-'}`
- Refresh mode: `{payload.get('refresh_mode') or '-'}`
- Confirm OpenAI cost: `{payload.get('confirm_openai_cost') or '-'}`

## Last Recorded Summary Refresh

- Summary model: `{payload.get('summary_refresh_model') or '-'}`
- Summaries refreshed in last successful write: `{payload.get('summaries_refreshed_last_success')}`
- Paper count: `{payload.get('paper_count')}`

## Notes

- This workflow is manual only.
- OpenAI API calls are allowed only when `confirm_openai_cost=true`.
- Scheduled paper updates do not call OpenAI.
- Paper PDFs and publisher abstract text are not stored.
"""


def _run_url() -> str:
    repo = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    if not repo or not run_id:
        return ""
    return f"https://github.com/{repo}/actions/runs/{run_id}"


def _kst_display(value: str) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.astimezone(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S KST")


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Could not parse {path.relative_to(ROOT)} while writing OpenAI summary status: {exc}")
        return default


if __name__ == "__main__":
    main()
