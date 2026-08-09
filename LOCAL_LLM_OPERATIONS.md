# Local LLM Summary Operations

This project can refresh selected paper summaries with a local Ollama model instead of the OpenAI API.

## Purpose

- Use the current GPU PC for a short local test period.
- Move the same workflow to the RTX 3090 workstation after quality and speed are acceptable.
- Keep OpenAI summary refresh as a separate, manual, cost-confirmed workflow.

## Local Test Setup

Install Ollama and pull a small model suitable for a 12 GB VRAM GPU:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5:7b
```

Confirm that Ollama is responding:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:11434/api/generate `
  -ContentType "application/json" `
  -Body '{"model":"qwen2.5:7b","prompt":"Reply with exactly: ready","stream":false}'
```

## Dry Run

Run one summary without writing data:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:MAX_LOCAL_SUMMARIES = "1"
$env:REFRESH_MODE = "metadata"
$env:DRY_RUN = "true"
& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_summaries.py
```

## Apply Local Summaries

Refresh a small batch of metadata/fallback summaries:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:MAX_LOCAL_SUMMARIES = "5"
$env:REFRESH_MODE = "metadata"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue
& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_summaries.py
& "C:\Users\user\anaconda3\python.exe" scripts\build_split_data.py
```

Then inspect the diff before committing.

## Modes

- `REFRESH_MODE=metadata`: refresh only metadata/fallback summaries. This is the default and does not repeatedly process already-local records.
- `REFRESH_MODE=week`: refresh weekly-new papers.
- `REFRESH_MODE=missing`: refresh records without a stored summary.
- `REFRESH_MODE=non_qa`: refresh records that are not in the five-question format.
- `REFRESH_MODE=all`: refresh all non-OpenAI records.

By default, OpenAI summaries are not overwritten. To overwrite them intentionally:

```powershell
$env:LOCAL_OVERWRITE_OPENAI = "true"
```

## Data Policy

- Local summaries use `summary_provider: "local"`.
- OpenAI summaries keep `summary_provider: "openai"` and are not overwritten by default.
- Metadata summaries keep `summary_provider: "fallback"` or `metadata`.
- Local output must not store raw abstracts or PDFs.
- Existing tags and categories are preserved and merged with local model output so topic counts do not drift because of the summarizer.

## Workstation Migration

On the RTX 3090 workstation, use the same script and change only the model:

```powershell
$env:LOCAL_LLM_MODEL = "gpt-oss:20b"
```

If that model is too slow or unstable, keep using `qwen2.5:7b` or test a 14B/32B quantized model.

## Local AML Embeddings

AML recommendation scoring can also run without OpenAI embeddings by using an Ollama embedding model.

Install the local embedding model:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull nomic-embed-text
```

Run the AML external/internal recommendation refresh with local embeddings:

```powershell
$env:AML_EMBEDDING_PROVIDER = "local"
$env:LOCAL_EMBEDDING_MODEL = "nomic-embed-text"
& "C:\Users\user\anaconda3\python.exe" scripts\run_aml_recommendation_pipeline.py --mode collect_and_score --max-candidates 0
$env:OPENALEX_RANK_TARGETS = "aml"
& "C:\Users\user\anaconda3\python.exe" scripts\enrich_openalex_venue_ranks.py
```

By default, local embedding runs write a private preview file instead of replacing the public AML recommendation list:

```text
data/private/aml_recommended_papers_local_preview.json
```

Only publish local-embedding AML recommendations intentionally:

```powershell
$env:AML_ALLOW_LOCAL_PUBLIC_WRITE = "true"
```

Local embedding caches are stored separately from OpenAI embedding caches:

- `data/aml_embeddings/aml_seed_embeddings_local_nomic-embed-text.json`
- `data/aml_embeddings/aml_candidate_embeddings_local_nomic-embed-text.json`

OpenAI and local embedding vectors must not be mixed because their dimensions and score distributions differ. The local provider therefore uses a stricter default public AML threshold.
