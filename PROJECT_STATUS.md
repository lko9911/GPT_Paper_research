# PROJECT_STATUS

## 2026-06-12 23:15 최신 상태

- 현재 `data/papers.json`에는 342편의 논문 메타데이터가 저장되어 있습니다.
- 왼쪽 분야 패널은 `생산/제조`, `3D 프린팅`, `4D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조`와 각 서브 토픽을 표시합니다.
- `로봇 자율 실험`은 표현이 부정확해 `Self-driving Labs` / `자율 실험실`로 정리했고, 위치도 로봇틱스가 아니라 `AI 생산제조` 분야 아래로 옮겼습니다.
- `제조 자동화`는 현재 데이터에서 완전히 없는 주제가 아니라, 기존 감지 키워드가 좁아 일부 항목을 놓치던 상태였습니다. `automation`, `automated`, `autonomous`, `closed-loop`, `monitoring`, `in-situ` 계열 표현을 함께 인식하도록 보강했습니다.
- `data/queries.json`에 로봇 AM, 제조 자동화, closed-loop manufacturing, self-driving lab, autonomous laboratory, materials discovery 계열 검색어를 추가했으므로 다음 자동 수집부터 해당 영역 recall이 개선됩니다.
- 현재 로컬 검증 기준으로 로봇 관련 후보는 32편, 자동화 확장 키워드 후보는 8편, self-driving lab/autonomous lab 계열 후보는 0편입니다.

### 최근 완료된 추가 개선
- 왼쪽 패널의 긴 분야명은 줄바꿈하지 않고 한 줄로 표시하며, 숫자 배지와의 간격을 넓혔습니다.
- `scripts/summarize.py`의 태그 맵도 보강해 새로 수집되는 논문이 `Self-driving Labs`/제조 자동화 태그를 받을 수 있도록 했습니다.
- OpenAlex API는 일시적으로 429 rate limit을 반환할 수 있으므로, 깊은 검증이나 대량 수집은 GitHub Actions 수동 실행 또는 충분한 sleep 설정을 권장합니다.

## 2026-06-12 17:56 최신 상태

- 원격 `main` 기준 `data/papers.json`에는 156편의 논문이 저장되어 있습니다.
- 최신 자동 수집 커밋은 `34ff160 Update paper metadata`이며, `data/site_meta.json`의 `last_run_at_utc`는 `2026-06-12T06:29:37Z`입니다. 이는 KST 기준 `2026-06-12 15:29:37`입니다.
- 공개 GitHub Pages URL이 한동안 이전 `2026-06-12T04:59:53Z` 데이터를 서빙하는 현상을 확인했습니다. 원인은 데이터 커밋은 성공했지만 Pages 배포가 즉시 따라오지 않는 배포/캐시 반영 문제로 판단했습니다.
- `.github/workflows/update-papers.yml`에 데이터 업데이트 후 GitHub Pages artifact를 업로드하고 직접 배포하는 단계를 추가했습니다.

### 완료된 추가 개선
- 매시간 논문 수집 workflow가 성공하면 같은 workflow 안에서 GitHub Pages를 직접 배포합니다.
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
