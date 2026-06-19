# ARCHITECTURE

## 2026-06-19 Crossref-Only Full Rebuild Architecture

The scheduled paper collection pipeline now rebuilds the dataset from Crossref
search results instead of incrementally merging old data.

Current flow:

```text
Archive existing outputs
  -> Search Crossref from scratch using data/queries.json
  -> Search selected Crossref journals by ISSN using data/crossref_venue_queries.json
  -> De-duplicate by DOI, then title/year/first author
  -> Generate fallback English metadata summaries without OpenAI
  -> For records with DOI and no corresponding author, check OpenAlex by DOI only
  -> Use OpenAlex only to complete corresponding-author metadata
  -> Export data/papers.json, data/archive_papers.json, data/papers.csv, data/papers.xlsx
  -> Regenerate data/papers_index.json and lazy detail chunks
```

Important constraints:

- OpenAlex is no longer a general paper search source in `Update papers`.
- OpenAlex priority venue / source search is disabled for the scheduled dataset update.
- Crossref ISSN-targeted venue search is enabled for selected journals in `data/crossref_venue_queries.json`; these records still have `source: ["Crossref"]`.
- Existing active/archive paper records are archived before overwrite but are not used as collection seeds.
- OpenAlex DOI results never add new papers to the dataset.
- Records remain source-provenance clean: `source` is always `["Crossref"]` for rebuilt records.
- OpenAlex completion is recorded only through provenance fields:
  - `openalex_checked`
  - `openalex_used_for`
  - `openalex_crosscheck_work_id`
  - `corresponding_author_source`
- Core/non-core fields are retained for downstream compatibility but are placeholders in this rebuild:
  - `is_core_venue`
  - `core_status`
  - `venue_scope`
  - `core_source`

Main files:

- `scripts/full_rebuild_crossref_dataset.py`: full rebuild orchestrator.
- `scripts/fetch_crossref.py`: Crossref metadata normalization, including ISSN, publisher, author detail, any Crossref-provided corresponding-author flag, and ISSN-targeted works search.
- `data/crossref_venue_queries.json`: selected Crossref venue targets such as ACS AMI and Materials & Design.
- `scripts/fetch_openalex.py`: used only through DOI lookup for missing corresponding-author completion.
- `.github/workflows/update-papers.yml`: calls the full rebuild script, then `scripts/build_split_data.py`.

The previous `scripts/update_papers.py` incremental pipeline remains in the repository for reference/backward compatibility, but the active scheduled workflow does not call it.

## 2026-06-13 Seed DOI 및 Priority Curation 구조

`data/seed_dois.json`은 일반 검색 쿼리로 놓치면 안 되는 대표 논문을 DOI 기준으로 고정 추적하는 목록입니다. Nature, Science, Nature Materials, Science Advances처럼 중요한 venue의 대표 논문은 broad keyword search 상위 결과에 항상 들어온다고 보장할 수 없으므로 seed DOI로 관리합니다.

`scripts/update_papers.py`는 seed DOI를 처리할 때 일반 `_is_plausible()` keyword 필터 대신 `_is_plausible_seed()`를 사용합니다. 이 함수는 제목, 연도, 비논문 여부만 확인합니다. seed DOI는 사용자가 직접 큐레이션한 항목이므로 통과 시 `curation_priority=true`가 붙고, relevance score가 낮게 계산되어도 최소 curated 기준점인 `CURATED_MIN_SCORE` 이상으로 보정됩니다.

`_is_curated_candidate()`는 `curation_priority=true`인 논문을 archive로 숨기지 않습니다. 따라서 CRAFT처럼 일반 fallback scoring이 낮게 나온 논문도 사용자가 지정한 대표 논문이면 메인 `data/papers.json`에 남습니다.

중요한 운영 원칙:
- seed DOI 추가는 출판사 크롤링이 아니라 OpenAlex/Crossref DOI 메타데이터 조회입니다.
- seed DOI 처리에서도 OpenAI는 자동 호출하지 않습니다.
- 새로 seed로 들어온 논문은 사용자가 별도로 명시 요청하기 전까지 fallback metadata summary 상태로 둡니다.
- OpenAI Q5 refresh를 다시 실행할 때도 `relevance_score`는 덮어쓰지 않고 기존 curated score를 유지합니다.

## 2026-06-13 Robotics Subtopic Policy

`Robotics for Manufacturing` 분야는 `Manufacturing Automation`, `Robot-based Manufacturing`, `Robotic AM` 세 서브토픽을 사용합니다. `Process Optimization`은 `Production / Manufacturing` 분야에만 두고, 로봇 분야에서는 중복 표시하지 않습니다.

- `Robot-based Manufacturing`: 로봇이 제조, 생산, 제작, 조립, 가공, 용접, 프린팅을 수행하는 broader manufacturing 논문입니다.
- `Robotic AM`: 로봇 기반 적층제조, 로봇 3D/4D printing, robot-assisted additive manufacturing에 더 특화된 논문입니다.
- `Manufacturing Automation`: 자동화, closed-loop, monitoring, autonomous manufacturing처럼 제조 자동화 자체가 중심인 논문입니다.

새 로봇 관련 쿼리는 `data/queries.json`에 있으며, 정기 업데이트에서도 OpenAI는 자동 호출하지 않습니다.

## 2026-06-12 Pages 배포 보강

자동 수집 workflow인 `.github/workflows/update-papers.yml`은 `data/papers.json`과 `data/site_meta.json`을 갱신한 뒤, GitHub Pages artifact를 업로드하고 `actions/deploy-pages`로 직접 배포합니다.

이 보강의 이유는 다음과 같습니다.

- GitHub Actions의 `GITHUB_TOKEN`으로 만들어진 데이터 커밋은 원격 `main`에는 정상 반영되지만, 별도 push 기반 Pages 배포 workflow를 항상 트리거하지 않을 수 있습니다.
- 사용자는 사이트 상단의 현재 시각과 마지막 수집 실행 시각을 함께 보므로, 데이터 수집 성공 후 Pages 반영도 가능한 한 같은 workflow에서 요청하는 편이 혼동을 줄입니다.
- 따라서 정기 수집 workflow 자체가 Pages 배포까지 수행하도록 구성했습니다.

현재 관련 workflow는 두 종류입니다.

- `.github/workflows/update-papers.yml`: 6시간 주기/수동 실행으로 논문 데이터를 수집하고, 변경 사항을 커밋한 뒤 GitHub Pages를 직접 배포합니다.
- `.github/workflows/deploy-pages.yml`: `main` push 또는 수동 실행 시 정적 사이트를 GitHub Pages에 배포합니다.

## 전체 시스템 구조

이 프로젝트는 GitHub Pages에서 바로 호스팅할 수 있는 정적 프론트엔드와 GitHub Actions에서 실행되는 Python 업데이트 파이프라인으로 구성됩니다.

- 프론트엔드: `index.html`, `assets/style.css`, `assets/app.js`
- 데이터: `data/papers.json`, `data/queries.json`
- 우선 게재지: `data/target_venues.json`
- Seed DOI: `data/seed_dois.json`
- 업데이트 파이프라인: `scripts/*.py`
- 자동화: `.github/workflows/update-papers.yml`
- 문서: `README.md`, `AGENT_LOG.md`, `PROJECT_STATUS.md`, `ARCHITECTURE.md`

## 프론트엔드 구조

`index.html`은 정적 HTML이며 빌드 도구가 필요 없습니다. `assets/app.js`가 `data/papers.json`을 fetch하여 논문 카드를 렌더링합니다.

구현된 UI 기능은 다음과 같습니다.

- 키워드 검색
- 카테고리 필터
- 연도 필터
- 관련성 점수순, 최신순, 제목순 정렬
- 상단에는 현재 메인 목록에 표시되는 curated paper 수, 게재지 수, 조사 연도 범위, 현재/마지막 수집 시각을 표시
- raw 후보 수와 archive 숨김 수는 footer의 낮은 우선순위 운영 정보로 표시
- DOI 열기, Source 열기, citation 복사 버튼
- 5문항 논문 요약 Q/A 렌더링

클라이언트에는 API key를 사용하지 않습니다. GitHub Pages에서 정적 파일만 제공하므로 비밀 값은 절대 브라우저로 전달되지 않습니다.

## 데이터 구조

주 데이터 파일은 `data/papers.json`입니다. 각 항목은 사용자 요구 스키마를 따릅니다.

중요 정책 필드:

- `abstract_used_for_summary`: 초록이 요약 입력으로 사용되었는지 여부입니다.
- `raw_abstract_displayed`: 항상 `false`로 저장합니다.
- `pdf_stored`: 항상 `false`로 저장합니다.

초록 원문은 API 응답에서 `_abstract`라는 임시 필드로만 들고 있다가 저장 직전 제거합니다. 이 필드는 `data/papers.json`에 남지 않습니다.

`ai_summary_ko`와 `ai_summary_en`은 일반 문단이 아니라 다음 5문항을 순서대로 답하는 형식을 표준으로 사용합니다.

1. Topic - 이 논문은 무엇을 다루는가?
2. Problem - 어떤 문제나 한계를 해결하려는가?
3. Method - 어떤 방법이나 접근을 사용했는가?
4. Key Result - 가장 중요한 결과는 무엇인가?
5. Takeaway - 그래서 이 논문의 핵심 메시지는 무엇인가?

프론트엔드는 이 형식을 감지하면 카드 내부에 Q/A 블록으로 렌더링합니다. 영어 모드에서는 `ai_summary_en`이 있으면 우선 표시하고, 없으면 메타데이터 기반 영어 fallback을 표시합니다. 예전 문단형 요약은 기존 paragraph 형태로 fallback 표시합니다.

`data/queries.json`은 자동 검색에 사용할 기본 검색어 배열입니다.

## Python 업데이트 파이프라인 구조

진입점은 `scripts/update_papers.py`입니다.

비용 안전 정책:

- 정기 `Update papers` workflow는 OpenAI API key를 전달하지 않습니다.
- `scripts/update_papers.py`는 `ALLOW_OPENAI_IN_UPDATE=true`가 명시되지 않으면 OpenAI를 호출하지 않고 fallback 요약/분류만 생성합니다.
- OpenAI 요약은 사용자가 명시적으로 요구할 때만 별도 workflow인 `.github/workflows/refresh-openai-summaries.yml`에서 curated papers를 대상으로 실행합니다.
- 수동 OpenAI workflow도 `explicit_openai_request` 입력에 정확한 안전 문구를 넣지 않으면 실패합니다.
- 이 분리의 이유는 raw 후보 수집 단계에서 나중에 archive로 숨길 논문까지 요약하면 불필요한 API 비용이 발생하기 때문입니다.
- 각 논문에는 `summary_provider`와 `openai_summary_applied` 필드를 저장합니다. UI는 이 값을 보고 `OpenAI 미적용` 또는 `OpenAI 요약` 배지를 표시합니다.

실행 순서:

1. `data/papers.json`과 `data/queries.json`을 읽습니다.
2. 각 검색어마다 OpenAlex와 Crossref를 조회합니다. 기본 시작 연도는 `SINCE_YEAR=2024`입니다.
3. `data/seed_dois.json`에 있는 DOI는 OpenAlex DOI endpoint로 직접 조회합니다.
4. `data/target_venues.json`의 OpenAlex source ID를 사용해 Nature, Science, Additive Manufacturing 등 우선 게재지 안에서 별도 검색을 수행합니다.
5. DOI가 있으면 DOI로, DOI가 없으면 normalized title로 중복 제거합니다.
6. 새 논문이면 선택적으로 Semantic Scholar 보강을 수행합니다.
7. 새 논문에 대해서만 한글/영문 요약, 관련성 점수, 관련성 설명, 태그, 카테고리를 생성합니다.
8. 저장 전 `_abstract` 같은 transient 필드를 제거합니다.
9. 변경이 있을 때만 `data/papers.json`을 씁니다.

파일별 역할:

- `scripts/fetch_openalex.py`: OpenAlex Works API 조회 및 공통 스키마로 정규화
- `scripts/fetch_crossref.py`: Crossref Works API 조회 및 공통 스키마로 정규화
- `scripts/enrich_semantic_scholar.py`: `SEMANTIC_SCHOLAR_API_KEY`가 있을 때 DOI 기반 선택적 보강
- `scripts/summarize.py`: OpenAI 요약 생성 또는 fallback 요약 생성, 5문항 요약 형식화, 카테고리/태그/점수 생성
- `scripts/refresh_openai_summaries.py`: 기존 논문을 수동 batch로 OpenAI 재요약
- `scripts/update_papers.py`: 전체 orchestration, 중복 제거, 저장

## GitHub Actions workflow 구조

`.github/workflows/update-papers.yml`은 6시간마다 실행되며 `workflow_dispatch` 수동 실행도 지원합니다. 현재 cron은 `17 1,7,13,19 * * *`이며, KST 기준 `04:17`, `10:17`, `16:17`, `22:17`에 실행됩니다.

주요 단계:

- checkout
- Python 3.11 설정
- `requirements.txt` 설치
- `python scripts/update_papers.py` 실행
- `data/papers.json` 변경 시에만 커밋 및 push

새 논문이 없거나 API 일부가 일시 실패해도 전체 워크플로가 불필요하게 실패하지 않도록 fetch 오류는 개별 검색 단위에서 로그를 남기고 계속 진행합니다.

`.github/workflows/refresh-openai-summaries.yml`은 `OpenAI summary refresh`라는 이름으로 Actions에 표시되는 별도 수동 workflow입니다. `OPENAI_API_KEY`가 설정된 경우에만 기존 논문을 OpenAI로 5문항 한글/영문 재요약합니다. 비용 폭주를 막기 위해 `max_summaries`, `refresh_mode`, `dry_run`, `confirm_openai_cost` 입력값을 받습니다. 실제 OpenAI 호출은 `confirm_openai_cost=true`를 명시적으로 선택한 경우에만 허용됩니다. 전체 재요약 또는 영문 GPT 요약 채우기는 `max_summaries=400`, `refresh_mode=non_qa`, `dry_run=false`, `confirm_openai_cost=true`로 실행합니다.

OpenAI 요약 workflow의 상태는 `OPENAI_SUMMARY_STATUS.md`와 `data/openai_summary_status.json`에 기록합니다. 논문 수집 workflow의 `UPDATE_STATUS.md`/`data/update_status.json`과 분리되어 있어, 수집 업데이트와 비용이 발생하는 요약 작업을 별도로 추적할 수 있습니다.

## API key 및 환경변수

- `CONTACT_EMAIL`: OpenAlex/Crossref polite request에 사용합니다.
- `OPENAI_API_KEY`: 선택적 OpenAI 한글/영문 요약 생성에 사용합니다.
- `OPENAI_MODEL`: 선택적 모델명입니다. 기본값은 `gpt-4o-mini`입니다.
- `SEMANTIC_SCHOLAR_API_KEY`: 선택적 Semantic Scholar 보강에 사용합니다.
- `API_SLEEP_SECONDS`: API rate limit 배려를 위한 요청 간 대기 시간입니다. 기본값은 `0.2`초입니다.
- `SINCE_YEAR`: 자동 조사 시작 연도입니다. 기본값은 `2024`입니다.
- `MAX_OPENAI_SUMMARIES`: 수동 OpenAI 재요약 workflow에서 한 번에 처리할 최대 논문 수입니다.
- `REFRESH_MODE`: `non_qa`, `all`, `missing` 중 하나로 OpenAI 재요약 대상을 고릅니다.
- `DRY_RUN`: `true`면 OpenAI 재요약 테스트만 하고 파일을 쓰지 않습니다.

환경변수 값은 로그나 데이터 파일에 기록하지 않습니다.

## 저작권/데이터 정책

이 프로젝트는 공식 메타데이터 API만 사용합니다. 출판사 웹사이트를 직접 크롤링하지 않고 PDF를 다운로드하거나 저장하지 않습니다. API에서 받은 abstract는 한글 AI 요약 생성 입력으로만 사용하며, 웹사이트와 `data/papers.json`에는 원문 abstract를 표시하거나 보관하지 않습니다.

이 정책을 코드 레벨에서 지키기 위해 `scripts/update_papers.py`는 저장 직전 `_abstract`로 시작하는 transient 필드를 제거합니다. 프론트엔드는 원문 abstract를 읽지 않고 저장된 `ai_summary_ko` 또는 `ai_summary_en`만 표시합니다.
## 2026-06-12 수집량 정책 업데이트

- `data/papers.json`의 전체 논문 수에는 상한을 두지 않습니다.
- OpenAlex와 Crossref는 공식 API의 cursor/page 기능을 사용해 여러 페이지를 읽을 수 있습니다.
- GitHub Actions의 1회 실행은 `OPENALEX_MAX_PAGES`, `CROSSREF_MAX_PAGES`, `API_SLEEP_SECONDS`로 조절합니다. 이 값은 전체 수집량 제한이 아니라 rate limit과 timeout을 피하기 위한 실행 단위 예산입니다.
- 429 응답이 잦으면 `API_SLEEP_SECONDS`를 늘리거나 수동 실행 간격을 넓히는 것이 좋습니다.

## 2026-06-12 갱신 시각 메타데이터

- `data/site_meta.json`은 자동 업데이트 파이프라인의 마지막 실행 시각을 저장합니다.
- `last_run_at_utc`는 UTC ISO timestamp이며, 프론트엔드는 이를 KST로 변환해 상단 통계의 `최신 업데이트`에 표시합니다.
- 새 논문이 없어도 workflow가 실행되면 `data/site_meta.json`이 변경되므로, 사용자는 사이트에서 마지막 갱신 실행 시간을 확인할 수 있습니다.
## 2026-06-17 Author And Journal Metric Enrichment

The project now supports optional OpenAlex metadata enrichment for author and venue details.

### Stored Author Fields

- `author_details`: ordered authorship objects from OpenAlex, including author name, OpenAlex author ID, ORCID when available, author position, institutions, and raw affiliation strings.
- `corresponding_authors`: subset of `author_details` where OpenAlex reports `authorships.is_corresponding=true`.
- `corresponding_author_available`: boolean display helper. `false` means the API did not provide a corresponding author flag; it is not a negative claim from the publisher.

### Venue Metric Fields

- `venue_metrics`: open metadata from the OpenAlex source object when available, including ISSN, source type, host organization, works count, citation count, and OpenAlex `summary_stats`.
- `journal_quality`: transparent display label. It can use manual core venue rules, repository/preprint detection, and OpenAlex open citation proxies.
- `journal_quality.official_jif` and `journal_quality.official_quartile` remain `null` unless a licensed JCR/Scopus data source is supplied.

### Workflow

`.github/workflows/enrich-openalex-metadata.yml` exposes a manual `Enrich OpenAlex metadata` workflow. It runs `scripts/enrich_openalex_metadata.py`, calls only the official OpenAlex Work API by DOI, and commits changed `data/papers.json` / `data/archive_papers.json`.

This workflow does not call OpenAI, crawl publisher pages, download PDFs, or store raw abstracts.

### IF / Quartile Policy

Official Journal Impact Factor and quartile classification should not be inferred from OpenAlex/Crossref. If those values are needed, add a licensed import such as `data/journal_metrics.csv` with source year, metric source, ISSN, JIF, and quartile fields. Until then the UI must call the automatic label a `Venue signal`, not `Impact Factor`.
# AML Recommendation Pipeline

The existing scheduled keyword pipeline remains `.github/workflows/update-papers.yml` and must not be renamed, moved, or modified for AML recommendation work. It updates `data/papers.json`, `data/archive_papers.json`, `data/site_meta.json`, `UPDATE_STATUS.md`, and `data/update_status.json`, then deploys the Pages site.

The AML recommendation pipeline is separate and manual-only:

- Workflow: `.github/workflows/aml-recommendation-manual.yml`
- Trigger: `workflow_dispatch` only
- Seed input: `data/seed/aml_seed_papers_core_enriched.json`
- Public output: `public/data/aml_recommended_papers.json`
- Private outputs: `data/private/aml_seed_embeddings.json`, `data/private/aml_candidate_embeddings.json`, `data/private/aml_candidate_pool.json`, `data/private/aml_scoring_debug.json`, and `data/private/aml_recommendation_log.json`

Frontend integration is additive. `assets/app.js` still fetches the existing site data from:

- `data/papers.json`
- `data/site_meta.json`
- `data/update_status.json`

It additionally tries to fetch `public/data/aml_recommended_papers.json`. If that file is missing, the AML section stays hidden and the existing paper list continues to work.

# Split Public Data Loading

The source-of-truth paper files remain `data/papers.json` and `data/archive_papers.json`; do not move them because the update, enrichment, OpenAI summary, and AML workflows still use those paths.

For GitHub Pages runtime performance, the public frontend now loads split data:

- Startup active index: `data/papers_index.json`
- Active detail manifest: `data/detail_manifest.json`
- Active detail chunks: `data/details/detail_000.json`, `detail_001.json`, ...
- Archive index: `data/archive_papers_index.json`
- Archive detail manifest: `data/archive_detail_manifest.json`
- Archive detail chunks: `data/archive_details/archive_detail_000.json`, ...

`assets/app.js` loads only `data/papers_index.json` at startup. It does not load `data/papers.json` in production. A local-development fallback to `data/papers.json` exists only when `papers_index.json` is missing, and the UI shows a data-loading warning first.

The active index contains only fields needed for first-page filtering, sorting, and compact card rendering: stable id, title, authors, year, venue, DOI/URL, source, categories, tags, relevance score, update dates, summary provider flags, and safety flags. Heavy fields such as `ai_summary_en`, detailed authorship, corresponding-author arrays, OpenAlex venue metrics, journal quality metadata, and long notes live in detail chunks.

When the user clicks `Load details` on a card, the frontend loads `data/detail_manifest.json`, finds the chunk for that paper id, fetches that chunk once, caches it in memory, and re-renders the card with detailed authorship and Q5 summary data. Already-loaded chunks are not fetched again.

`scripts/build_split_data.py` regenerates all split files from `data/papers.json` and `data/archive_papers.json`. It removes Korean duplicate fields from generated public split files, including fields such as `ai_summary_ko`, `relevance_note_ko`, `archive_note_ko`, `title_ko`, `abstract_ko`, and other `_ko` / Korean / translated variants. The original source-of-truth JSON files are not deleted.

The update workflows run `scripts/build_split_data.py` after changing paper data:

- `.github/workflows/update-papers.yml`
- `.github/workflows/refresh-openai-summaries.yml`
- `.github/workflows/enrich-openalex-metadata.yml`

The current generated sizes are approximately:

- Original active `papers.json`: 10,781.5 KB
- Original archive `archive_papers.json`: 11,323.6 KB
- Generated active index: 1,488.4 KB
- Generated archive index: 1,839.4 KB, not loaded at startup
- Default initial JSON load for papers: about 1.49 MB before compression

OpenAI use is constrained:

- Embeddings are used when `OPENAI_API_KEY` is available.
- OpenAI is not used as the paper search engine.
- Candidate collection uses the existing local paper pool and, in collection modes, OpenAlex/Crossref.
- OpenAI relevance judging is controlled by `use_ai_judge` and defaults to `false`.
- OpenAI reason rewriting is controlled by `use_ai_reason` and defaults to `false`.
- Template-based recommendation reasons are used by default.

# Frontend Density Policy

As of 2026-06-18, the frontend has no runtime density mode.
The former Compact/Comfort toggle and `data-density="compact"` CSS overrides were removed.
Paper cards use the default comfortable layout at all viewport sizes, with responsive CSS handling mobile and wide screens.

# English-Only UI And Summary Architecture

As of 2026-06-18, the site is English-only.

## Frontend
- `index.html` contains English static copy and no language toggle.
- `assets/app.js` fixes language behavior to English and no longer reads `localStorage.language`.
- The frontend renders summaries from `ai_summary_en`.
- If `ai_summary_en` is missing, the frontend creates an English metadata fallback block.
- Historical `ai_summary_ko` and `relevance_note_ko` values may remain in stored data, but they are not used by the UI.

## Summary Pipeline
- `scripts/summarize.py` generates `ai_summary_en` and `relevance_note_en`.
- OpenAI output is requested as a five-question English Q5 summary:
  1. Topic
  2. Problem
  3. Method
  4. Key Result
  5. Takeaway
- Without OpenAI, the fallback summary is also English-only and is generated from metadata plus transient abstract signals without copying abstract text.

## Update Workflows
- Scheduled metadata updates still do not call OpenAI.
- Manual OpenAI refreshes remain separate and user-approved.
- `scripts/refresh_openai_summaries.py` now refreshes `ai_summary_en` only.

## Copyright / Data Policy
- Publisher abstracts are never displayed.
- PDFs are not downloaded or stored.
- DOI/source links remain the authoritative route to original papers.
- The retained historical Korean summary fields are internal legacy data only and should not be treated as the active display format.
