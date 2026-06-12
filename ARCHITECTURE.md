# ARCHITECTURE

## 전체 시스템 구조

이 프로젝트는 GitHub Pages에서 바로 호스팅할 수 있는 정적 프론트엔드와 GitHub Actions에서 실행되는 Python 업데이트 파이프라인으로 구성됩니다.

- 프론트엔드: `index.html`, `assets/style.css`, `assets/app.js`
- 데이터: `data/papers.json`, `data/queries.json`
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
- 전체 논문 수, 카테고리 수, 최신 업데이트 날짜, 이번 주 추가 논문 수 표시
- DOI 열기, Source 열기, citation 복사 버튼

클라이언트에는 API key를 사용하지 않습니다. GitHub Pages에서 정적 파일만 제공하므로 비밀 값은 절대 브라우저로 전달되지 않습니다.

## 데이터 구조

주 데이터 파일은 `data/papers.json`입니다. 각 항목은 사용자 요구 스키마를 따릅니다.

중요 정책 필드:

- `abstract_used_for_summary`: 초록이 요약 입력으로 사용되었는지 여부입니다.
- `raw_abstract_displayed`: 항상 `false`로 저장합니다.
- `pdf_stored`: 항상 `false`로 저장합니다.

초록 원문은 API 응답에서 `_abstract`라는 임시 필드로만 들고 있다가 저장 직전 제거합니다. 이 필드는 `data/papers.json`에 남지 않습니다.

`data/queries.json`은 자동 검색에 사용할 기본 검색어 배열입니다.

## Python 업데이트 파이프라인 구조

진입점은 `scripts/update_papers.py`입니다.

실행 순서:

1. `data/papers.json`과 `data/queries.json`을 읽습니다.
2. 각 검색어마다 OpenAlex와 Crossref를 조회합니다. 기본 시작 연도는 `SINCE_YEAR=2024`입니다.
3. DOI가 있으면 DOI로, DOI가 없으면 normalized title로 중복 제거합니다.
4. 새 논문이면 선택적으로 Semantic Scholar 보강을 수행합니다.
5. 새 논문에 대해서만 한글 요약, 관련성 점수, 관련성 설명, 태그, 카테고리를 생성합니다.
6. 저장 전 `_abstract` 같은 transient 필드를 제거합니다.
7. 변경이 있을 때만 `data/papers.json`을 씁니다.

파일별 역할:

- `scripts/fetch_openalex.py`: OpenAlex Works API 조회 및 공통 스키마로 정규화
- `scripts/fetch_crossref.py`: Crossref Works API 조회 및 공통 스키마로 정규화
- `scripts/enrich_semantic_scholar.py`: `SEMANTIC_SCHOLAR_API_KEY`가 있을 때 DOI 기반 선택적 보강
- `scripts/summarize.py`: OpenAI 요약 생성 또는 fallback 요약 생성, 카테고리/태그/점수 생성
- `scripts/update_papers.py`: 전체 orchestration, 중복 제거, 저장

## GitHub Actions workflow 구조

`.github/workflows/update-papers.yml`은 매시 정각 실행되며 `workflow_dispatch` 수동 실행도 지원합니다.

주요 단계:

- checkout
- Python 3.11 설정
- `requirements.txt` 설치
- `python scripts/update_papers.py` 실행
- `data/papers.json` 변경 시에만 커밋 및 push

새 논문이 없거나 API 일부가 일시 실패해도 전체 워크플로가 불필요하게 실패하지 않도록 fetch 오류는 개별 검색 단위에서 로그를 남기고 계속 진행합니다.

## API key 및 환경변수

- `CONTACT_EMAIL`: OpenAlex/Crossref polite request에 사용합니다.
- `OPENAI_API_KEY`: 선택적 OpenAI 요약 생성에 사용합니다.
- `OPENAI_MODEL`: 선택적 모델명입니다. 기본값은 `gpt-4o-mini`입니다.
- `SEMANTIC_SCHOLAR_API_KEY`: 선택적 Semantic Scholar 보강에 사용합니다.
- `API_SLEEP_SECONDS`: API rate limit 배려를 위한 요청 간 대기 시간입니다. 기본값은 `0.2`초입니다.
- `SINCE_YEAR`: 자동 조사 시작 연도입니다. 기본값은 `2024`입니다.

환경변수 값은 로그나 데이터 파일에 기록하지 않습니다.

## 저작권/데이터 정책

이 프로젝트는 공식 메타데이터 API만 사용합니다. 출판사 웹사이트를 직접 크롤링하지 않고 PDF를 다운로드하거나 저장하지 않습니다. API에서 받은 abstract는 한글 AI 요약 생성 입력으로만 사용하며, 웹사이트와 `data/papers.json`에는 원문 abstract를 표시하거나 보관하지 않습니다.

이 정책을 코드 레벨에서 지키기 위해 `scripts/update_papers.py`는 저장 직전 `_abstract`로 시작하는 transient 필드를 제거합니다. 프론트엔드도 `ai_summary_ko`만 표시합니다.
