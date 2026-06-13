"""Write a small public status file for the paper update workflow."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATUS_MD = ROOT / "UPDATE_STATUS.md"
STATUS_JSON = ROOT / "data" / "update_status.json"
SITE_META = ROOT / "data" / "site_meta.json"


def main() -> None:
    now_utc = datetime.now(UTC).replace(microsecond=0)
    now_kst = now_utc.astimezone(ZoneInfo("Asia/Seoul"))
    site_meta = _load_json(SITE_META, {})

    payload = {
        "checked_at_utc": now_utc.isoformat().replace("+00:00", "Z"),
        "checked_at_kst": now_kst.isoformat(),
        "workflow": os.getenv("GITHUB_WORKFLOW", "Update papers"),
        "event": os.getenv("GITHUB_EVENT_NAME", ""),
        "run_id": os.getenv("GITHUB_RUN_ID", ""),
        "run_number": os.getenv("GITHUB_RUN_NUMBER", ""),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", ""),
        "run_url": _run_url(),
        "ref": os.getenv("GITHUB_REF_NAME", ""),
        "sha": os.getenv("GITHUB_SHA", ""),
        "job_status": os.getenv("UPDATE_JOB_STATUS", ""),
        "update_step_outcome": os.getenv("UPDATE_STEP_OUTCOME", ""),
        "commit_step_outcome": os.getenv("COMMIT_STEP_OUTCOME", ""),
        "deploy_step_outcome": os.getenv("DEPLOY_STEP_OUTCOME", ""),
        "schedule": os.getenv("UPDATE_CRON_DESCRIPTION", "17 */6 * * *"),
        "last_successful_collection_utc": site_meta.get("last_run_at_utc", ""),
        "last_successful_collection_kst": _kst_display(site_meta.get("last_run_at_utc", "")),
        "paper_count": site_meta.get("paper_count", 0),
        "curated_count": site_meta.get("curated_count", site_meta.get("paper_count", 0)),
        "raw_candidate_count": site_meta.get("raw_candidate_count", 0),
        "archived_count": site_meta.get("archived_count", 0),
        "papers_added_last_success": site_meta.get("papers_added", 0),
        "openai_scheduled_updates_enabled": False,
    }

    STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATUS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATUS_MD.write_text(_markdown(payload), encoding="utf-8")
    print(f"Wrote {STATUS_MD.relative_to(ROOT)} and {STATUS_JSON.relative_to(ROOT)}")


def _markdown(payload: dict[str, object]) -> str:
    status = str(payload.get("job_status") or "unknown")
    update = str(payload.get("update_step_outcome") or "unknown")
    commit = str(payload.get("commit_step_outcome") or "unknown")
    deploy = str(payload.get("deploy_step_outcome") or "unknown")
    run_url = str(payload.get("run_url") or "")
    run_link = f"[{payload.get('run_id')}]({run_url})" if run_url else str(payload.get("run_id") or "-")
    return f"""# Update Status

This file is written by GitHub Actions so the latest paper-update state can be checked without opening the Actions UI.

## Latest Workflow Check

- Checked at: `{payload.get('checked_at_kst')}` KST
- Workflow: `{payload.get('workflow')}`
- Event: `{payload.get('event')}`
- Run: {run_link}
- Job status: `{status}`
- Update step: `{update}`
- Commit step: `{commit}`
- Deploy step: `{deploy}`
- Ref: `{payload.get('ref')}`
- Commit SHA: `{payload.get('sha')}`

## Last Successful Collection

- Last collection time: `{payload.get('last_successful_collection_kst') or '-'}`
- Curated papers: `{payload.get('curated_count')}`
- Raw candidates: `{payload.get('raw_candidate_count')}`
- Archived hidden: `{payload.get('archived_count')}`
- Papers added in last successful run: `{payload.get('papers_added_last_success')}`

## Schedule

- Cron: `{payload.get('schedule')}`
- Approximate KST times: `03:17`, `09:17`, `15:17`, `21:17`
- OpenAI in scheduled updates: `disabled`

## Notes

- If the scheduled run is skipped by GitHub, this file will not change for that slot.
- If the workflow starts but fails, this file should still update with the failure state.
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
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
