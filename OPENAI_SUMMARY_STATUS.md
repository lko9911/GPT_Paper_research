# OpenAI Summary Status

This file is written by the manual OpenAI summary workflow. It is separate from `UPDATE_STATUS.md`.

## Latest Workflow Check

- Checked at: `2026-07-23T09:38:37+09:00` KST
- Workflow: `OpenAI summary refresh`
- Event: `workflow_dispatch`
- Run: [29969487450](https://github.com/lko9911/GPT_Paper_research/actions/runs/29969487450)
- Job status: `success`
- Summary phase: `completed`
- Confirm step: `success`
- Refresh step: `success`
- Commit step: `success`
- Deploy step: `success`
- Ref: `main`
- Commit SHA: `fd4e96164d39e494a0444e69830f2260f2ac0625`

## Requested Inputs

- Max summaries: `30`
- Refresh mode: `metadata`
- Confirm OpenAI cost: `true`

## Last Recorded Summary Refresh

- Summary model: `gpt-4o-mini`
- Summaries refreshed in last successful write: `30`
- Paper count: `1550`

## Notes

- This workflow is manual only.
- OpenAI API calls are allowed only when `confirm_openai_cost=true`.
- Scheduled paper updates do not call OpenAI.
- Paper PDFs and publisher abstract text are not stored.
