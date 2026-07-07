# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `2026-07-07T10:30:20+09:00` KST
- Workflow: `OpenAI summary refresh`
- Event: `workflow_dispatch`
- Run: [28835076321](https://github.com/lko9911/GPT_Paper_research/actions/runs/28835076321)
- Job status: `in_progress`
- Summary phase: `in_progress`
- Confirm step: `pending`
- Refresh step: `pending`
- Commit step: `pending`
- Deploy step: `pending`
- Ref: `main`
- Commit SHA: `fb3b18ae106a6b046dfad7834440b79d02251a66`

## Requested Inputs

- Max summaries: `300`
- Refresh mode: `metadata`
- Confirm OpenAI cost: `true`

## Last Recorded Summary Refresh

- Summary model: `-`
- Summaries refreshed in last successful write: `0`
- Paper count: `1520`

## Notes

- This workflow is manual only.
- OpenAI API calls are allowed only when `confirm_openai_cost=true`.
- Scheduled paper updates do not call OpenAI.
- Paper PDFs and publisher abstract text are not stored.
