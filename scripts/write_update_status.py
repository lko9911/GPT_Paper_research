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
    displayed_added = _display_papers_added(site_meta)
    raw_added = _int(site_meta.get("papers_added", 0))

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
        "update_phase": os.getenv("UPDATE_PHASE", ""),
        "schedule": os.getenv("UPDATE_CRON_DESCRIPTION", "17 1,7,13,19 * * *"),
        "last_successful_collection_utc": site_meta.get("last_run_at_utc", ""),
        "last_successful_collection_kst": _kst_display(site_meta.get("last_run_at_utc", "")),
        "paper_count": site_meta.get("paper_count", 0),
        "curated_count": site_meta.get("curated_count", site_meta.get("paper_count", 0)),
        "raw_candidate_count": site_meta.get("raw_candidate_count", 0),
        "archived_count": site_meta.get("archived_count", 0),
        "collection_mode": site_meta.get("collection_mode", ""),
        "papers_added_last_success": displayed_added,
        "papers_added_raw_last_success": raw_added,
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
    phase = str(payload.get("update_phase") or "")
    run_url = str(payload.get("run_url") or "")
    run_link = f"[{payload.get('run_id')}]({run_url})" if run_url else str(payload.get("run_id") or "-")
    kst_times = _schedule_kst_times(str(payload.get("schedule") or ""))
    added_note = _added_note(payload)
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
- Update phase: `{phase or status}`
- Ref: `{payload.get('ref')}`
- Commit SHA: `{payload.get('sha')}`

## Last Successful Collection

- Last collection time: `{payload.get('last_successful_collection_kst') or '-'}`
- Curated papers: `{payload.get('curated_count')}`
- Raw candidates: `{payload.get('raw_candidate_count')}`
- Archived hidden: `{payload.get('archived_count')}`
- Papers added in last successful run: `{payload.get('papers_added_last_success')}`{added_note}

## Schedule

- Cron: `{payload.get('schedule')}`
- Approximate KST times: {kst_times}
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


def _schedule_kst_times(schedule: str) -> str:
    if schedule == "17 1,7,13,19 * * *":
        return "`04:17`, `10:17`, `16:17`, `22:17`"
    if schedule == "17 1,13 * * *":
        return "`10:17`, `22:17`"
    if schedule == "17 */12 * * *":
        return "`09:17`, `21:17`"
    if schedule == "17 * * * *":
        return "`HH:17` every hour"
    if schedule == "0 * * * *":
        return "`HH:00` every hour"
    return "`see cron expression`"


def _display_papers_added(site_meta: dict[str, object]) -> int:
    raw_added = _int(site_meta.get("papers_added", 0))
    total = _int(site_meta.get("paper_count", site_meta.get("curated_count", 0)))
    if raw_added <= 0:
        return 0
    if _is_full_rebuild(site_meta) or (total > 0 and raw_added >= total):
        return 0
    return raw_added


def _is_full_rebuild(site_meta: dict[str, object]) -> bool:
    return "full_rebuild" in str(site_meta.get("collection_mode", "")).lower()


def _added_note(payload: dict[str, object]) -> str:
    displayed = _int(payload.get("papers_added_last_success", 0))
    raw = _int(payload.get("papers_added_raw_last_success", displayed))
    mode = str(payload.get("collection_mode") or "")
    if raw == displayed:
        return ""
    note = f" (raw rebuild count: `{raw}`"
    if mode:
        note += f"; mode: `{mode}`"
    return note + ")"


def _int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
