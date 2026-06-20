# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `2026-06-20T21:47:28+09:00` KST
- Workflow: `OpenAI summary refresh`
- Event: `workflow_dispatch`
- Run: [27867541329](https://github.com/lko9911/GPT_Paper_research/actions/runs/27867541329)
- Job status: `failure`
- Summary phase: `completed`
- Confirm step: `success`
- Refresh step: `success`
- Commit step: `failure`
- Deploy step: `skipped`
- Ref: `main`
- Commit SHA: `5535961088a2d013166779a4d8380e79148b8655`

## Requested Inputs

- Max summaries: `1300`
- Refresh mode: `metadata`
- Dry run: `false`
- Confirm OpenAI cost: `true`

## Last Recorded Summary Refresh

- Summary model: `-`
- Summaries refreshed in last successful write: `0`
- Paper count: `1237`

## Notes

- This workflow is manual only.
- OpenAI API calls are allowed only when `confirm_openai_cost=true`.
- Scheduled paper updates do not call OpenAI.
- Paper PDFs and publisher abstract text are not stored.
