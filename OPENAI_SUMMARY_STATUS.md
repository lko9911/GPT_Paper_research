# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `2026-06-20T21:49:41+09:00` KST
- Workflow: `OpenAI summary refresh`
- Event: `workflow_dispatch`
- Run: [27871672851](https://github.com/lko9911/GPT_Paper_research/actions/runs/27871672851)
- Job status: `in_progress`
- Summary phase: `in_progress`
- Confirm step: `pending`
- Refresh step: `pending`
- Commit step: `pending`
- Deploy step: `pending`
- Ref: `main`
- Commit SHA: `bd7edb9e11dc0a6953c18f35b89bd6559d621b25`

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
