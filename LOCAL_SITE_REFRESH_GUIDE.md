# Local Site Refresh Guide

This guide is the copy-paste runbook for refreshing the GitHub Pages paper tracker from a local Windows PC with Ollama.

## When To Use This

- Use this when you want to refresh the site without spending OpenAI API tokens.
- Local AI summaries use Ollama with `qwen2.5:7b`.
- Local AML embeddings use Ollama with `nomic-embed-text`.
- Crossref/OpenAlex metadata lookups still call public external APIs, but the LLM/embedding work runs locally.

## Important Rule

Run these commands in PowerShell, not inside `ollama run`.

If the prompt looks like this, you are inside Ollama chat:

```text
>>>
```

Exit first:

```text
/bye
```

Then wait until the prompt looks like this again:

```powershell
(base) PS C:\Users\user\Desktop\AML_Research\GPT_Paper_research>
```

## One-Time Local Setup

Install or update the local models:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5:7b
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull nomic-embed-text
```

Confirm Ollama is responding:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:11434/api/generate `
  -ContentType "application/json" `
  -Body '{"model":"qwen2.5:7b","prompt":"Reply with exactly: ready","stream":false}'
```

## Check Before Running

```powershell
git pull
git status --short --branch
```

If `git status` shows files you did not intend to change, inspect them before continuing.

## Refresh Normal Paper Summaries Locally

Use this when metadata-only summaries remain in the normal paper database:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:LOCAL_REQUIRE_ABSTRACT = "false"
$env:MAX_LOCAL_SUMMARIES = "0"
$env:REFRESH_MODE = "metadata"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue

& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_summaries.py
& "C:\Users\user\anaconda3\python.exe" scripts\build_split_data.py
```

## Refresh AML Recommendations Locally

This runs AML external/internal discovery and scoring with local embeddings, then writes the public site file by merging with the existing recommendation list.

```powershell
$env:AML_EMBEDDING_PROVIDER = "local"
$env:LOCAL_EMBEDDING_MODEL = "nomic-embed-text"
$env:AML_ALLOW_LOCAL_PUBLIC_WRITE = "true"

& "C:\Users\user\anaconda3\python.exe" scripts\run_aml_recommendation_pipeline.py --mode collect_and_score --max-candidates 0

$env:OPENALEX_RANK_TARGETS = "aml"
& "C:\Users\user\anaconda3\python.exe" scripts\enrich_openalex_venue_ranks.py
```

If new AML recommendation records still have metadata-only summaries, convert those to local AI summaries:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:LOCAL_REQUIRE_ABSTRACT = "false"
$env:MAX_LOCAL_AML_SUMMARIES = "0"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue

& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_aml_summaries.py
```

## Verify Counts

```powershell
$env:PYTHONIOENCODING = "utf-8"
@'
import json
from collections import Counter
from pathlib import Path

targets = [
    Path("data/papers.json"),
    Path("data/papers_index.json"),
    Path("public/data/aml_recommended_papers.json"),
]

for path in targets:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "papers" in data:
        data = data["papers"]
    providers = Counter((item.get("summary_provider") or "metadata") for item in data)
    metadata_remaining = sum(
        1
        for item in data
        if (item.get("summary_provider") or "metadata") not in {"openai", "local"}
        and not item.get("openai_summary_applied")
        and not item.get("local_summary_applied")
    )
    print(path, len(data), dict(providers), "metadata_remaining", metadata_remaining)
'@ | & "C:\Users\user\anaconda3\python.exe" -
```

Expected result after a clean local refresh:

- Normal paper data should have `metadata_remaining 0`.
- AML recommendations should keep the old records and add new ones, not shrink.
- AML recommendations should have `metadata_remaining 0` after `refresh_local_aml_summaries.py`.

## Commit And Push

```powershell
git status --short
git add data/papers.json data/papers_index.json data/site_meta.json public/data public/data/papers data/aml_embeddings data/openalex_source_metrics.json
git commit -m "Refresh site data locally"
git push
```

If there is nothing to commit, Git will say so; that means the refresh did not change tracked output.

## Quick Health Checks

See whether local jobs are still running:

```powershell
Get-Process | Where-Object { $_.ProcessName -match "python|ollama" } |
  Select-Object ProcessName,Id,CPU,WorkingSet64,StartTime
```

Check GPU usage:

```powershell
nvidia-smi
```

High GPU memory usage usually means Ollama has a model loaded. GPU utilization can be low between requests.

## Safety Notes

- Do not commit `data/private/`; it is intentionally private.
- Before pushing from a new machine, check tracked private files:

```powershell
git ls-files data/private
```

  Ideally this prints nothing. If it prints a private seed/profile file, stop and decide whether that file must be removed from Git history or kept as a deliberate tracked exception.
- Do not paste PowerShell commands into the `>>>` Ollama chat prompt.
- Local AML embedding runs must use the local embedding cache files. Do not mix OpenAI and Ollama embeddings.
- The public AML recommendation refresh now merges with the existing list, so old recommendations should not disappear during normal local refreshes.
