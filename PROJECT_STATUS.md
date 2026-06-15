# PROJECT_STATUS

## 2026-06-15 최신 상태

- 사용자의 운영 의도에 맞춰 `Update papers` 정기 실행 주기를 12시간마다로 정리했습니다.
- 현재 목표 cron은 `17 */12 * * *`이며 KST 기준 대략 `09:17`, `21:17`에 실행됩니다.
- 정기 업데이트는 여전히 OpenAI API를 사용하지 않습니다. 신규 논문은 사용자가 별도로 허가하기 전까지 metadata/fallback summary로 들어옵니다.

## 2026-06-13 13:26 최신 상태

- 2026-06-13 20:10에 `Robotics for Manufacturing`에서 중복 `Process Optimization`을 제거하고 `Robot-based Manufacturing` / `로봇 기반 생산제조` 서브토픽을 추가했습니다. 로봇 관련 metadata update 후 curated 논문 수는 741편입니다.
- 새로 추가된 로봇 관련 논문은 OpenAI 없이 fallback metadata summary 상태입니다.
- 2026-06-13 13:54에 태그 표시를 canonical tag 기반으로 안정화했습니다. 자유 한글/영문 태그는 데이터에 남아 있어도 카드와 필터에는 대표 태그만 언어별 label로 표시됩니다.
- 2026-06-13 13:43에 Nature/Science/Nature Materials/Science Advances 대표 논문 누락 원인을 조사하고 seed DOI 기반으로 보강했습니다. 현재 curated 논문 수는 549편입니다.
- 원인은 API 부재가 아니라 broad query 검색 결과 제한과 relevance/archive 정책이었습니다. 대표 DOI는 `data/seed_dois.json`에 고정하고 `curation_priority=true`로 메인 목록에 남깁니다.
- 새로 추가/승격된 대표 논문 중 기존 OpenAI 요약이 없던 10편은 OpenAI 없이 fallback metadata summary 상태입니다. OpenAI 적용은 사용자가 다시 명시 요청할 때만 수행해야 합니다.
- 2026-06-13 13:30에 OpenAI refresh 후 `relevance_score`가 전부 `1/10`으로 덮인 문제를 복구했습니다. 대표 DOI 보강 후 현재 점수 분포는 `5점 305편`, `6점 142편`, `7점 76편`, `8점 26편`입니다.
- 향후 `Refresh OpenAI summaries`는 `relevance_score`를 덮어쓰지 않고 기존 curated score를 유지합니다.
- curated 논문 539편 전체에 OpenAI 기반 Q5 요약이 적용되었습니다.
- `data/papers.json` 기준 `summary_provider=openai` 539편, `openai_summary_applied=true` 539편입니다.
- 한국어 Q5 요약과 영어 Q5 요약 모두 539/539편에서 확인되었습니다.
- 이번 실행은 사용자의 명시 요청에 따른 1회성 수동 실행입니다.
- `Refresh OpenAI summaries` GitHub Actions run `27454740969`가 성공했고, 결과 커밋은 `af7da22 Refresh OpenAI paper summaries`입니다.
- `data/site_meta.json`에는 `summaries_refreshed=539`, `summary_refresh_model=gpt-4o-mini`, `last_run_at_utc=2026-06-13T04:23:40Z`가 기록되어 있습니다.
- 정기 `Update papers` workflow는 여전히 OpenAI API를 사용하지 않습니다. `ALLOW_OPENAI_IN_UPDATE=false`이며 scheduled update에는 `OPENAI_API_KEY`가 전달되지 않습니다.
- repository variable `OPENAI_REFRESH_ENABLED`는 다시 `false`로 닫혀 있습니다. 다음 OpenAI refresh는 사용자가 다시 명시적으로 요청할 때만 열어야 합니다.

### 남은 주의사항
- 앞으로 자동 수집되는 신규 논문은 OpenAI 요약이 아니라 metadata summary로 들어옵니다.
- 신규 논문까지 OpenAI Q5 요약을 적용하려면 별도 수동 refresh가 필요합니다.
- 539편 전체 refresh에는 약 76분이 걸렸으므로, 다음 대량 refresh는 100편 단위 batch 방식이 더 안정적입니다.

## 2026-06-13 00:30 최신 상태

- 상단 통계 영역은 방문자 혼동을 줄이기 위해 `논문수`, `게재지`, `조사연도`, `현재 / 갱신`만 보여줍니다.
- raw candidate 수와 archive hidden 수는 footer의 작은 운영 정보로 이동했습니다.
- `data/archive_papers.json`은 삭제되거나 비공개 처리된 것이 아니라, 메인 목록에서 숨긴 공개 보존 데이터입니다.
- archive를 정말 비공개로 만들려면 GitHub Pages 배포 대상에서 제외하거나 별도 비공개 저장소/artifact로 분리해야 합니다.
- 비용 방지를 위해 정기 `Update papers` workflow는 더 이상 `OPENAI_API_KEY`를 전달하지 않으며, `scripts/update_papers.py`도 기본적으로 OpenAI 호출을 차단합니다.
- OpenAI 요약은 수동 `Refresh OpenAI summaries` workflow에서 curated papers 대상으로만 실행하는 것이 현재 운영 원칙입니다.
- 추가 절대 규칙: OpenAI API는 사용자가 명시적으로 요구할 때만 사용합니다. 새로 업데이트되는 모든 논문에는 OpenAI를 적용하지 않습니다.
- 현재 curated 414편은 모두 `openai_summary_applied=false`이며, UI 카드에는 `OpenAI 미적용` 배지가 표시됩니다.

## 2026-06-13 00:10 상태

- 공개 사이트의 raw 후보 레코드 2084개를 curated/archive 구조로 분리했습니다.
- `data/papers.json`에는 기본 사이트에 표시할 curated papers 414편만 남겼습니다.
- `data/archive_papers.json`에는 낮은 관련성 및 제목 중복 후보 1670개를 보존했습니다.
- `data/site_meta.json`은 `curated_count=414`, `raw_candidate_count=2084`, `archived_count=1670`, `hidden_low_relevance_count=1647`, `duplicate_archived_count=23`을 기록합니다.
- 상단 통계는 이후 방문자용 `논문수`, `게재지`, `조사연도`, `현재 / 갱신`으로 단순화되었고, 전체 후보/숨김 수치는 footer 운영 정보로 이동했습니다.

### 완료된 추가 개선
- 자동 수집 파이프라인이 앞으로도 curated/archive를 분리 저장하도록 `scripts/update_papers.py`를 수정했습니다.
- `.github/workflows/update-papers.yml`의 자동 커밋 대상에 `data/archive_papers.json`을 추가했습니다.
- Pages 배포와 논문 수집 workflow의 concurrency group을 분리했고, 수집 job에 60분 timeout을 추가했습니다.
- 너무 넓은 `digital twin smart manufacturing`, `digital twin manufacturing process optimization` 검색어를 제거하고 AM 맥락이 더 강한 digital twin 검색어로 교체했습니다.
- 같은 제목의 여러 버전은 정식 venue/DOI/비저장소 여부를 기준으로 대표 항목만 curated에 남깁니다.

### 알려진 주의점
- `archive_papers.json`은 삭제가 아니라 보존용입니다. 큐레이션 기준을 바꾸면 archive에서 다시 복구할 수 있습니다.
- 기본 사이트에는 curated 414편만 표시되므로, 이전의 2084개 raw 후보 수와 화면 표시 수는 더 이상 같은 의미가 아닙니다.

## 2026-06-12 23:45 최신 상태

- 현재 `data/papers.json`에는 428편의 논문 메타데이터가 저장되어 있습니다.
- `Self-driving Labs`와 `Digital Twins` 검색어 추가 후 Crossref 관련도순 검색으로 수동 보강 수집을 실행했고, 비논문 항목을 제거한 뒤 86편이 새로 남았습니다.
- OpenAlex는 현재 429 rate limit을 반환하고 있어, 이번 보강 수집은 `SKIP_OPENALEX=1`로 Crossref 중심으로 수행했습니다.
- 왼쪽 사이드바 서브토픽 카운트는 분야 내 대표 버킷 방식입니다. 따라서 각 분야의 서브토픽 및 `Others` 합계가 분야 총 논문 수와 일치합니다.
- `scripts/update_papers.py`는 `UPDATE_QUERY_FILTER`, `SKIP_OPENALEX`, `SKIP_TARGET_VENUES`, `SEARCH_PER_PAGE`, `TARGET_VENUE_PER_PAGE` 환경변수를 지원합니다.
- Crossref에서 `Review for`, `Decision letter`, `Author response`, `Title Pending`, 초청 발표 초록 같은 비논문 항목이 들어오지 않도록 필터를 보강했습니다.

### 최근 완료된 추가 개선
- Crossref 기본 정렬을 `published`에서 `relevance`로 바꿔 비정상 미래 연도 항목이 검색 상단을 차지하는 문제를 줄였습니다.
- `data/site_meta.json`은 이번 수동 수집 기준 `paper_count=428`, `papers_added=86`을 기록합니다.
- 데이터 정책 검증 결과 `raw_abstract_displayed=false`, `pdf_stored=false`가 유지됩니다.

## 2026-06-12 23:15 최신 상태

- 현재 `data/papers.json`에는 342편의 논문 메타데이터가 저장되어 있습니다.
- 왼쪽 분야 패널은 `생산/제조`, `3D 프린팅`, `4D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조`와 각 서브 토픽을 표시합니다.
- `로봇 자율 실험`은 표현이 부정확해 `Self-driving Labs` / `자율 실험실`로 정리했고, 위치도 로봇틱스가 아니라 `AI 생산제조` 분야 아래로 옮겼습니다.
- `AI 생산제조` 분야에 `Digital Twins` / `디지털 트윈` 서브 토픽을 추가했습니다.
- `제조 자동화`는 현재 데이터에서 완전히 없는 주제가 아니라, 기존 감지 키워드가 좁아 일부 항목을 놓치던 상태였습니다. `automation`, `automated`, `autonomous`, `closed-loop`, `monitoring`, `in-situ` 계열 표현을 함께 인식하도록 보강했습니다.
- `data/queries.json`에 로봇 AM, 제조 자동화, closed-loop manufacturing, self-driving lab, autonomous laboratory, materials discovery 계열 검색어를 추가했으므로 다음 자동 수집부터 해당 영역 recall이 개선됩니다.
- 현재 로컬 검증 기준으로 로봇 관련 후보는 32편, 자동화 확장 키워드 후보는 8편, self-driving lab/autonomous lab 계열 후보는 0편입니다.

### 최근 완료된 추가 개선
- 왼쪽 패널의 긴 분야명은 줄바꿈하지 않고 한 줄로 표시하며, 숫자 배지와의 간격을 넓혔습니다.
- `scripts/summarize.py`의 태그 맵도 보강해 새로 수집되는 논문이 `Self-driving Labs`/제조 자동화 태그를 받을 수 있도록 했습니다.
- 디지털 트윈, cyber-physical manufacturing, process twin 계열 표현도 프론트엔드와 수집 파이프라인에서 인식합니다.
- OpenAlex API는 일시적으로 429 rate limit을 반환할 수 있으므로, 깊은 검증이나 대량 수집은 GitHub Actions 수동 실행 또는 충분한 sleep 설정을 권장합니다.

## 2026-06-12 17:56 최신 상태

- 원격 `main` 기준 `data/papers.json`에는 156편의 논문이 저장되어 있습니다.
- 최신 자동 수집 커밋은 `34ff160 Update paper metadata`이며, `data/site_meta.json`의 `last_run_at_utc`는 `2026-06-12T06:29:37Z`입니다. 이는 KST 기준 `2026-06-12 15:29:37`입니다.
- 공개 GitHub Pages URL이 한동안 이전 `2026-06-12T04:59:53Z` 데이터를 서빙하는 현상을 확인했습니다. 원인은 데이터 커밋은 성공했지만 Pages 배포가 즉시 따라오지 않는 배포/캐시 반영 문제로 판단했습니다.
- `.github/workflows/update-papers.yml`에 데이터 업데이트 후 GitHub Pages artifact를 업로드하고 직접 배포하는 단계를 추가했습니다.

### 완료된 추가 개선
- 정기 논문 수집 workflow가 성공하면 같은 workflow 안에서 GitHub Pages를 직접 배포합니다.
- `GITHUB_TOKEN`으로 만든 데이터 커밋이 별도 push 배포 workflow를 트리거하지 않아도 공개 사이트가 최신 데이터로 갱신되도록 보강했습니다.

### 다음 확인 사항
- 다음 정기 실행 또는 수동 `workflow_dispatch` 실행 후 `https://lko9911.github.io/GPT_Paper_research/data/site_meta.json`이 최신 `last_run_at_utc`를 보여주는지 확인합니다.
- GitHub 저장소 Settings > Pages에서 현재 배포 방식이 GitHub Actions인지 branch deploy인지 확인합니다.

## 현재 프로젝트 상태 요약

GitHub Pages에서 동작 가능한 정적 논문 큐레이션 사이트와 GitHub Actions 자동 업데이트 파이프라인이 구현되어 있습니다. `data/papers.json`에는 현재 159편의 논문 메타데이터가 들어 있으며, 조사 범위는 2024년 이후 논문입니다.

## 완료된 기능

- 정적 웹사이트 기본 화면 구현
- `data/papers.json` 기반 논문 카드 렌더링
- 키워드 검색
- 카테고리 필터
- 연도 필터
- 관련성 점수순, 최신순, 제목순 정렬
- 상단 통계 표시
- DOI 열기, Source 열기, citation 복사 버튼
- OpenAlex 검색 스크립트
- Crossref 검색 스크립트
- 2024년 이후 논문만 자동 수집하는 기본 조사 범위
- DOI 우선 중복 제거 및 DOI 없는 경우 normalized title 중복 제거
- 새 논문만 요약 생성
- OpenAI API 선택적 한글/영문 요약 생성
- OpenAI key가 없을 때 fallback 한글 요약 생성
- 논문 요약을 5문항 Q/A 형식으로 생성 및 렌더링
- 기존 논문을 OpenAI로 일괄 재요약하는 수동 workflow
- Semantic Scholar API key가 있을 때 선택적 보강
- GitHub Actions 매시 실행 및 수동 실행
- 변경된 `data/papers.json`만 자동 커밋
- README, 아키텍처 문서, 상태 문서, 작업 로그 생성
- 로컬 HTTP 서버에서 `index.html`과 `data/papers.json` 응답 확인
- 저장 데이터에 `_abstract`가 남지 않고 `raw_abstract_displayed=false`, `pdf_stored=false`가 유지되는지 검증

## 부분 구현된 기능

- 관련성 점수와 분류는 OpenAI가 없을 때 휴리스틱 기반입니다.
- Source 열기 버튼은 현재 DOI URL을 사용합니다. 향후 API별 landing URL을 별도로 저장하면 더 정확해질 수 있습니다.
- API rate limit 배려는 기본 sleep, User-Agent/mailto, OpenAlex 429 retry/backoff 중심입니다. 더 큰 수집에는 실행 간격과 page 예산 조정이 필요합니다.
- 전체 342편 OpenAI 한글/영문 재요약은 자동 정기 실행이 아니라 `Refresh OpenAI summaries` 수동 workflow로만 실행됩니다.
- `ai_summary_en` 저장 필드를 지원하며, 영어 모드는 저장된 GPT 영문 요약이 있으면 이를 우선 표시하고 없으면 메타데이터 기반 영어 fallback을 표시합니다.

## 아직 구현되지 않은 기능

- Playwright 같은 브라우저 기반 시각 회귀 테스트
- 논문별 BibTeX 생성
- API별 raw metadata 감사 로그
- 검색어별 수집 결과 통계
- 수동 검수 플래그 또는 추천/숨김 기능

## 알려진 문제

- Crossref/OpenAlex 메타데이터 품질에 따라 venue, author, year가 비어 있을 수 있습니다.
- DOI가 없는 논문은 제목 정규화 기반으로 중복 제거하므로 제목 표기가 크게 다르면 중복이 남을 수 있습니다.
- 자동 필터링은 additive manufacturing 관련 키워드가 title/abstract에 있어야 통과하므로, 메타데이터에 초록이 없고 제목이 짧은 관련 논문은 누락될 수 있습니다.
- 현재 자동 수집 결과에는 넓은 biomedical 3D printing 또는 LPBF toolpath 항목이 포함될 수 있습니다. 큐레이션 품질을 높이려면 검색어와 `_is_plausible` 필터를 더 엄격하게 조정하세요.
- Science/Nature 계열 게재지는 별도로 배제하지 않습니다. 공식 메타데이터 API 검색 결과에 나오고 주제/연도 기준을 만족하면 포함될 수 있습니다.
- Nature, Science, Additive Manufacturing 계열은 UI에서 우선 추적 게재지 칩으로 표시됩니다. 현재 수집된 논문이 없으면 count가 0으로 보입니다.

## 다음 작업 추천 순서

1. 생성된 9편의 논문 목록을 검수하고 관련 없는 항목 필터링 규칙을 조정합니다.
2. GitHub Actions에서 `OPENAI_API_KEY`, `CONTACT_EMAIL`, 선택적 `SEMANTIC_SCHOLAR_API_KEY`를 설정합니다.
3. Source URL을 API별 원천 링크로 확장할지 결정합니다.
4. OpenAI 요약 품질을 보고 프롬프트와 카테고리 분류를 개선합니다.
5. GitHub Pages 배포 후 모바일 화면과 citation 복사 동작을 브라우저에서 확인합니다.
6. Nature/Science/Additive Manufacturing 논문을 더 정확히 모으려면 OpenAlex source ID 기반 venue-specific 검색을 추가합니다.
7. 기존 전체 논문을 5문항 한글/영문 형식으로 통일하려면 `Refresh OpenAI summaries` workflow를 `max_summaries=400`, `refresh_mode=non_qa`, `dry_run=false`로 수동 실행합니다.
## 2026-06-12 추가 상태

- 논문 총량 100편 제한을 제거했고, 현재 `data/papers.json`에는 145편이 저장되어 있습니다.
- OpenAlex/Crossref 공식 API 페이징을 사용하도록 fetcher를 확장했습니다.
- GitHub Actions에는 실행 안정성을 위해 `OPENALEX_MAX_PAGES=2`, `CROSSREF_MAX_PAGES=1`, `API_SLEEP_SECONDS=1.0`을 설정했습니다. 이는 전체 저장 논문 수 제한이 아니라 실행 1회당 API 예산입니다.
- 왼쪽 패널은 `생산/제조`, `3D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조`의 큰 분야와 서브 토픽을 함께 보여주도록 변경했습니다.
- 알려진 이슈: 깊은 수집 중 OpenAlex 429 rate limit이 발생할 수 있습니다. 더 많이 수집하려면 sleep을 늘리거나 수동 실행을 나누어 진행하세요.
- `data/site_meta.json`을 추가해 마지막 자동 갱신 실행 시각을 사이트 상단에 표시합니다.
# 2026-06-15 Taxonomy Status Update

## Current Taxonomy State
- The sidebar taxonomy was audited against the current 873 curated papers.
- `Volumetric AM` is now an explicit subtopic under `3D Printing`.
- `Soft robotics` is now an explicit subtopic under `Robotics for Manufacturing`.
- `MMAM` was moved from `Production / Manufacturing` to `3D Printing`, because it is more naturally an additive manufacturing subtopic in this tracker.
- Sidebar subtopic counting remains mutually exclusive within each field: each paper is assigned to the first matching subtopic bucket so that subtopic totals add up to the field total.

## Current Field/Subtopic Rationale
- `Production / Manufacturing`: broad manufacturing papers that are not primarily AM/robotics/AI/4D. Subtopics emphasize materials and process optimization.
- `3D Printing`: additive manufacturing papers. Specific AM technologies and strategies are listed before the broad `Additive Manufacturing` fallback.
- `4D Printing`: shape-changing, LCE, metamaterial, and active material papers.
- `Robotics for Manufacturing`: robot-based manufacturing and soft robotics papers. `Manufacturing Automation` is kept as a subtopic because some robot papers are primarily about automated production workflows.
- `AI Manufacturing`: ML, digital twins, self-driving labs, design automation, and manufacturing automation papers.

## Known Taxonomy Issues
- `AI Manufacturing` still has a large `Others` bucket. This is not necessarily wrong, but it suggests future subtopics such as `AI process monitoring`, `Quality prediction`, `Physics-informed ML`, or `Autonomous process control` may be useful.
- `Soft robotics` papers that also contain strong 4D printing or AI keywords can still be assigned to those higher-priority fields. This is intentional for now, but can be changed if robotics should always override AI/4D.
- Browser-level visual verification was not completed in this turn because the browser automation runtime and local `node` command were unavailable in the current environment.

## Current Tag Display Policy
- Paper cards still show at most three representative tags.
- Specific tags are prioritized over broad tags. For example, `Volumetric AM`, `Soft robotics`, `MMAM`, `FGAM`, `LCE`, `Digital Twins`, and `Self-driving Labs` are favored.
- Broad or low-signal tags such as `Additive Manufacturing`, `Review`, `Sustainability`, `Digital fabrication`, `Material behavior`, and `Reusability` are retained for fallback/filtering but are pushed behind more specific tags on paper cards.
- `Deep Learning` and `Reinforcement Learning` are normalized into `Machine Learning` for this tracker, because the site is a manufacturing literature tracker rather than a general AI taxonomy browser.
- Korean/English variants of soft robotics terms are normalized into `Soft robotics`.
- `MMAM` is treated as a canonical topic tag, not only a raw API tag. Existing papers with explicit title/metadata signals such as `multi-material` or `multimaterial` were normalized so their `tags` field includes `MMAM`.
- Sidebar topic counts should be based on stable, specific metadata signals only: title, venue, and canonical tags. Broad categories and AI summaries/relevance notes are display or curation context and must not drive sidebar bucket counts, because generic tracker wording or broad category labels can over-count topics such as `MMAM`.
