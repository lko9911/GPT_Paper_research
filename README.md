# AI Manufacturing and 3D/4D Printing Research

Local refresh commands for site updates are summarized in [`LOCAL_SITE_REFRESH_GUIDE.md`](LOCAL_SITE_REFRESH_GUIDE.md).

## Current Collection Mode

The main paper dataset is now rebuilt in **Crossref-only full rebuild mode**.

The scheduled `Update papers` workflow runs:

```bash
python scripts/full_rebuild_crossref_dataset.py
python scripts/build_split_data.py
python scripts/build_trend_keyword_map.py
```

Collection policy:

- Crossref is the only paper discovery/search source.
- Existing `data/papers.json` and `data/archive_papers.json` are archived before overwrite but are not merged into the new result.
- OpenAlex general search is disabled.
- OpenAlex source/priority venue search is disabled.
- Selected journals can be searched through Crossref ISSN-targeted queries in `data/crossref_venue_queries.json`; this is still Crossref-only discovery.
- OpenAlex is used only when a Crossref result has a DOI and lacks corresponding-author metadata.
- OpenAlex DOI lookup may complete `corresponding_authors`, but it must not add new papers or change `source` away from `["Crossref"]`.
- OpenAI is not used by the scheduled update.

Main outputs:

- `data/papers.json`: active curated Crossref-based records.
- `data/archive_papers.json`: archived low-relevance/duplicate records from the same Crossref rebuild.
- `data/papers.csv`: active dataset CSV export.
- `data/papers.xlsx`: active dataset Excel export.
- `data/papers_index.json` and `data/details/detail_*.json`: GitHub Pages startup index and lazy detail chunks.
- `data/trend_keyword_map.json`: public keyword co-occurrence network for the trend map. It stores derived keyword/link counts only, not abstracts.
- `data/crossref_venue_queries.json`: optional Crossref ISSN-targeted venue queries, currently including `ACS Applied Materials & Interfaces` and `Materials & Design`.
- `data/old_exports/full_rebuild_*/`: compressed backup of the previous dataset/output files.

## Current Language Policy

The public site is English-only. The previous Korean UI mode has been removed.
New OpenAI summaries and metadata fallback summaries are generated as English Q5 summaries only.
Historical Korean summary fields may still exist in older JSON records, but the frontend no longer displays or refreshes them.

## AML Recommendation Engine

The existing keyword-based paper update still runs automatically every 6 hours through
`.github/workflows/update-papers.yml`. Do not use that workflow for AML recommendation.

AML recommendation is a separate manual-only workflow:

1. Keep the AML seed JSON at `data/private/aml_seed_papers_core_enriched.json`.
2. This single private seed JSON is intentionally tracked for the private repository, but GitHub Pages deployment excludes `data/private/` so it is not served by the website.
3. Go to `Actions > AML Recommendation Manual > Run workflow`.
4. Choose `score_existing`, `collect_and_score`, or `full_refresh`.
5. Leave `max_candidates` as `0` or blank to score all collected AML candidates. Set a positive number only for quick testing.
6. Keep `use_ai_judge=false`. The default `use_ai_reason=true` writes the public recommendation reason with OpenAI; set it to `false` only when you want template-only, no text-model cost.
7. Keep `reset_embeddings=false` for normal runs. Set it to `true` only after changing the AML seed file and intentionally rebuilding the embedding cache.

The AML pipeline uses OpenAI embeddings when `OPENAI_API_KEY` is available, but it does not use OpenAI as the paper search engine. In `collect_and_score` and `full_refresh`, external AML candidate discovery uses Crossref keyword search only, with no venue-specific filter. OpenAI relevance judging is optional and disabled by default. OpenAI recommendation-reason writing is enabled by default in the manual workflow and uses structured metadata, AML score, matched topics, and seed similarity rather than internal route names. Reusable embedding vectors are stored in `data/aml_embeddings/` and committed so later manual runs can reuse them. Candidate pools, debug logs, raw data, and PDFs remain ignored by Git. Public-safe recommendations are written to `public/data/aml_recommended_papers.json`.

During `full_refresh`, the site marks `New` only for recommendations that were not present in the previous `public/data/aml_recommended_papers.json`. Existing recommendations keep their prior `first_added` value and are not relabeled as new just because the refresh ran.

After AML recommendations are scored, the manual workflow runs an AML-only OpenAlex Sources rank enrichment step. Existing papers keep their stored OA Rank, and newly discovered Crossref AML candidates can receive `OA Rank 1` through `OA Rank 4` when their journal ISSN can be matched through OpenAlex Sources. This rank remains an internal venue signal, not JCR.

Venue cards and paper cards may show `OA Rank 1` through `OA Rank 4`. This is an internal OpenAlex-based venue signal, calculated from OpenAlex Sources metadata for journals in this tracker. It is not JCR Impact Factor, not an official quartile, and not a Scopus ranking.

Only recommendations with `AML score >= 0.75` are published to the public recommendation JSON and displayed on the site.

AML score uses only:

- 80% semantic similarity to the AML seed-paper profile
- 10% recency score
- 10% venue score

Keyword score and discovery-route score are intentionally not part of the AML score because candidates are already collected through AML keyword/search routes.

If the private AML seed file is not available on the GitHub Actions runner, `use_ai_reason=true` falls back to refreshing only the public `why_recommended` text for the already-published AML recommendations in `score_existing` mode. Full candidate scoring still requires the private seed file locally or on the runner.

For external AML discovery, use `collect_and_score` or `full_refresh` only after the seed file is available on the runner. These modes intentionally fail when the seed file is missing, so a manual run does not appear to succeed while doing only a reason refresh.

Optional secret override is still supported through `AML_SEED_PAPERS_JSON_B64` or `AML_SEED_PAPERS_JSON`, but the normal path is the tracked private seed file.

## Split Data for Faster GitHub Pages Loading

The production website should load `data/papers_index.json`, not the full `data/papers.json`, on first visit. Full source-of-truth files remain in place for automation:

- Source of truth: `data/papers.json`, `data/archive_papers.json`
- Startup index: `data/papers_index.json`
- Lazy details: `data/detail_manifest.json`, `data/details/detail_*.json`
- Archive split output: `data/archive_papers_index.json`, `data/archive_detail_manifest.json`, `data/archive_details/archive_detail_*.json`

Regenerate split files after changing paper data:

```bash
python scripts/build_split_data.py
```

The script prints size reporting for original files, generated indexes, detail chunks, estimated startup load, and reduction ratio. It also removes Korean duplicate fields from generated public split JSON files. The original full JSON files are not deleted.

Local test:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`. In the browser Network tab, the first paper-data request should be `data/papers_index.json`. The full `data/papers.json` should not be requested unless `papers_index.json` is missing and the local fallback is triggered. Detail chunks under `data/details/` should appear only after clicking `Load details` on a paper card.

생산·제조, 3D/4D 프린팅, 로봇틱스, AI 제조 분야를 위한 AI 기반 논문 큐레이션 저장소입니다. GitHub Pages에서 동작하는 정적 웹사이트와 GitHub Actions 기반 자동 업데이트 파이프라인을 포함합니다.

## 프로젝트 목적

이 저장소는 multi-material additive manufacturing, functionally graded additive manufacturing, blended FDM, digital material filament, computational design, toolpath optimization, material switching optimization 관련 논문 메타데이터를 주기적으로 수집하고, DOI 링크와 한글/영문 AI 요약을 함께 보여줍니다. 요약은 논문 리뷰에 바로 쓰기 쉽도록 `Topic`, `Problem`, `Method`, `Key Result`, `Takeaway`의 5문항 형식으로 작성합니다.

현재 자동 조사 범위는 2024년 이후 논문입니다. `SINCE_YEAR` 환경변수로 시작 연도를 바꿀 수 있으며 기본값은 `2024`입니다.

## 데이터 출처

- Paper discovery and baseline metadata: Crossref Works API
- Corresponding-author completion only: OpenAlex Works API by DOI lookup
- OpenAlex is not used as a general paper search source in the scheduled update.
- Semantic Scholar is not used by the current Crossref-only full rebuild workflow.

출판사 웹사이트를 직접 크롤링하지 않으며 PDF를 다운로드하거나 저장하지 않습니다.

## 저작권 정책

- 저장하는 데이터는 제목, 저자, 연도, 저널/학회명, DOI, URL, source, category, tag, AI-generated Korean/English summary로 제한합니다.
- API에서 초록을 제공하더라도 `data/papers.json`에는 원문 초록을 저장하지 않습니다.
- 초록은 새 한글/영문 요약을 생성하기 위한 임시 입력으로만 사용합니다.
- 웹사이트에는 출판사 초록, summary, description 문장을 그대로 표시하지 않습니다.
- 각 논문 카드에는 DOI/source 링크를 표시하여 원문 확인은 공식 링크에서 하도록 안내합니다.
- 전체 업데이트 절차, 공개 데이터 기준, AI summary close paraphrase 방지 원칙은 [`OPERATIONS_POLICY.md`](OPERATIONS_POLICY.md)에 따로 정리합니다.

## API key 설정 방법

GitHub 저장소의 `Settings > Secrets and variables > Actions`에서 다음 값을 설정할 수 있습니다.

- `CONTACT_EMAIL`: OpenAlex/Crossref polite pool 및 User-Agent에 사용할 연락 이메일입니다.
- `OPENAI_API_KEY`: 선택 사항입니다. 정기 업데이트에는 사용하지 않고, 사용자가 명시적으로 허가한 수동 `OpenAI summary refresh` workflow에서만 5문항 형식의 한글/영문 요약 생성에 사용합니다.
- `SEMANTIC_SCHOLAR_API_KEY`: 선택 사항입니다. 있으면 DOI 기반 Semantic Scholar 메타데이터 보강을 시도합니다.
- `OPENAI_MODEL`: 선택 사항입니다. Repository variable로 설정하며 기본값은 `gpt-4o-mini`입니다.

키가 없어도 파이프라인은 실패하지 않습니다. 정기 업데이트는 기본적으로 제목, 메타데이터, API에서 임시로 받은 초록 신호를 바탕으로 5문항 형식의 fallback 요약을 생성합니다. 초록 원문은 저장하지 않습니다.

## 로컬 실행 방법

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python scripts/full_rebuild_crossref_dataset.py
python scripts/build_split_data.py
python -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 열면 정적 사이트를 확인할 수 있습니다.

## GitHub Pages 배포 방법

1. 저장소를 GitHub에 push합니다.
2. `Settings > Pages`로 이동합니다.
3. Source를 `Deploy from a branch`로 선택합니다.
4. Branch를 `main` 또는 사용하는 기본 브랜치, folder를 `/root`로 설정합니다.
5. 배포 후 Pages URL에서 `index.html`이 `data/papers.json`을 불러와 렌더링합니다.

## 자동 업데이트

`.github/workflows/update-papers.yml`은 다음 조건에서 실행됩니다.

- 6시간마다 cron 실행
- `workflow_dispatch` 수동 실행

워크플로는 Python 의존성을 설치하고 `scripts/full_rebuild_crossref_dataset.py`와 `scripts/build_split_data.py`를 실행합니다. `data/papers.json`이 변경된 경우에만 자동 커밋합니다. 새 논문이 없어도 정상 종료되도록 구성해 불필요한 실패 알림을 줄였습니다.

## OpenAI로 기존 논문 전체 재요약

`OPENAI_API_KEY`를 GitHub Actions secret에 설정한 뒤, 기존 논문 요약을 OpenAI 기반 5문항 한글/영문 형식으로 다시 만들 수 있습니다.

1. GitHub 저장소의 `Actions` 탭으로 이동합니다.
2. `OpenAI summary refresh` workflow를 선택합니다.
3. `Run workflow`를 누릅니다.
4. 전체 라이브러리를 갱신하려면 다음 값을 사용합니다.

```txt
max_summaries: 400
refresh_mode: non_qa
confirm_openai_cost: true
```

`confirm_openai_cost=true`를 선택해야 실제 OpenAI API 호출이 허용됩니다. 이 workflow는 수동 실행 전용이며, 실행되면 요약 결과를 저장하고 GitHub Pages에 배포합니다. 비용을 작게 테스트하려면 `max_summaries=5`, `refresh_mode=metadata`, `confirm_openai_cost=true`처럼 작은 batch로 실행하세요.

이 workflow는 정기 실행되지 않고 수동 실행만 지원합니다. 따라서 OpenAI 비용이 주기적으로 반복 발생하지 않습니다.

## 논문 수동 추가/수정 방법

`data/papers.json`에 아래 스키마를 맞춰 항목을 추가하거나 수정합니다.

```json
{
  "id": "doi-or-hash",
  "title": "...",
  "authors": ["..."],
  "year": 2026,
  "venue": "...",
  "doi": "10.xxxx/xxxxx",
  "url": "https://doi.org/...",
  "source": ["OpenAlex", "Crossref"],
  "categories": ["기능성 구배 적층제조"],
  "tags": ["FGAM", "MMAM", "계산설계"],
  "relevance_score": 8,
  "ai_summary_ko": "1. Topic - 이 논문은 무엇을 다루는가? ...\n2. Problem - 어떤 문제나 한계를 해결하려는가? ...\n3. Method - 어떤 방법이나 접근을 사용했는가? ...\n4. Key Result - 가장 중요한 결과는 무엇인가? ...\n5. Takeaway - 그래서 이 논문의 핵심 메시지는 무엇인가? ...",
  "ai_summary_en": "1. Topic - ...\n2. Problem - ...\n3. Method - ...\n4. Key Result - ...\n5. Takeaway - ...",
  "relevance_note_ko": "...",
  "abstract_used_for_summary": true,
  "raw_abstract_displayed": false,
  "pdf_stored": false,
  "first_added": "YYYY-MM-DD",
  "last_updated": "YYYY-MM-DD"
}
```

`raw_abstract_displayed`와 `pdf_stored`는 정책 확인을 위해 `false`로 유지합니다.

중요하지만 자동 검색 순위에서 누락되는 논문은 `data/seed_dois.json`에 DOI를 추가하세요. 업데이트 파이프라인이 DOI로 OpenAlex를 직접 조회해 주제/연도 기준을 만족하면 `data/papers.json`에 추가합니다.

## 검색어 수정 방법

`data/queries.json`의 문자열 배열을 수정하면 다음 자동 실행부터 검색 범위가 바뀝니다. 너무 넓은 검색어는 관련 없는 논문을 늘릴 수 있으므로, additive manufacturing과 설계/재료/툴패스 맥락이 함께 드러나는 검색어를 권장합니다.

## 논문을 가져오는 기준

자동 파이프라인은 다음 조건을 만족하는 항목만 `data/papers.json`에 추가합니다.

- OpenAlex 또는 Crossref 공식 API에서 검색된 항목
- 기본적으로 2024년 이후로 식별된 항목
- 제목이 비어 있지 않은 항목
- DOI가 있으면 DOI 기준으로 중복 제거, DOI가 없으면 정규화된 제목 기준으로 중복 제거
- 제목 또는 API 초록 메타데이터에 additive manufacturing, 3D printing, FDM, material extrusion 계열 표현이 있는 항목
- 제목 또는 API 초록 메타데이터에 multi-material, functionally graded, digital material, computational design, material distribution, toolpath, material switching, purge, path planning 계열 표현이 있는 항목
- 출판사 웹사이트 직접 크롤링, PDF 다운로드, 원문 초록 저장 없이 처리 가능한 항목

Science, Nature, Nature Communications, Advanced Materials 같은 게재지도 OpenAlex/Crossref 메타데이터에 잡히고 위 기준을 만족하면 포함될 수 있습니다. 특정 출판사나 저널을 직접 크롤링하지는 않습니다.

현재 UI에서 우선 추적하는 게재지는 다음과 같습니다.

- Nature
- Nature Communications
- Nature Materials
- Nature Reviews Materials
- Science
- Science Advances
- Science Robotics
- Additive Manufacturing

이 목록은 `data/target_venues.json`에 OpenAlex source ID와 함께 저장되어 있습니다. 자동 업데이트는 일반 주제 검색에 더해 우선 추적 게재지 안에서 별도 검색도 수행합니다.

## 한계점

- 메타데이터 API의 색인 상태에 따라 최신 논문 반영이 지연될 수 있습니다.
- DOI가 없는 논문은 normalized title hash로 중복 제거하므로 제목 변형이 큰 경우 중복이 생길 수 있습니다.
- `OPENAI_API_KEY`가 없을 때 생성되는 fallback 요약은 초록이 있으면 초록을 임시 입력으로 참고하지만, 모델 기반 정밀 요약보다는 보수적일 수 있습니다.
- 자동 분류와 관련성 점수는 휴리스틱 또는 AI 생성 결과이므로 최종 판단은 DOI 링크의 원문을 확인해야 합니다.
- 논문 수 총량 제한은 두지 않지만, OpenAlex/Crossref API의 응답 범위와 rate limit에 영향을 받습니다.
## 2026-06-12 최신 수집 정책 업데이트

- 저장되는 논문 수에는 상한을 두지 않습니다. 기존 100편 제한은 제거했습니다.
- OpenAlex와 Crossref의 공식 API 페이징을 사용해 한 페이지보다 넓게 수집합니다.
- GitHub Actions는 6시간 주기로 안정적으로 끝나야 하므로 실행 1회당 `OPENALEX_MAX_PAGES`, `CROSSREF_MAX_PAGES`, `API_SLEEP_SECONDS`를 사용합니다. 이는 전체 논문 수 제한이 아니라 API rate limit과 Actions timeout을 피하기 위한 실행 예산입니다.
- 더 깊은 일회성 수집이 필요하면 workflow 또는 로컬 환경에서 `OPENALEX_MAX_PAGES`와 `CROSSREF_MAX_PAGES`를 높여 수동 실행하면 됩니다.
- `data/site_meta.json`에는 마지막 자동 갱신 실행 시각이 저장되며, 사이트 상단의 `최신 업데이트`에 KST 기준으로 표시됩니다.
