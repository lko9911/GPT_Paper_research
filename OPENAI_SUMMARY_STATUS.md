# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `2026-06-16T13:48:40+09:00` KST
- Workflow: `OpenAI summary refresh`
- Event: `workflow_dispatch`
- Run: [27592334411](https://github.com/lko9911/GPT_Paper_research/actions/runs/27592334411)
- Job status: `success`
- Summary phase: `completed`
- Confirm step: `success`
- Refresh step: `success`
- Commit step: `success`
- Deploy step: `success`
- Ref: `main`
- Commit SHA: `6d1888ee49cdc0dd57f86a3026797e1e0ddc8400`

## Requested Inputs

- Max summaries: `600`
- Refresh mode: `metadata`
- Dry run: `false`
- Confirm OpenAI cost: `true`

## Last Recorded Summary Refresh

- Summary model: `gpt-4o-mini`
- Summaries refreshed in last successful write: `548`
- Paper count: `1288`

## Notes

- This workflow is manual only.
- OpenAI API calls are allowed only when `confirm_openai_cost=true`.
- Scheduled paper updates do not call OpenAI.
- Paper PDFs and publisher abstract text are not stored.
