# AGENT_LOG

## 2026-06-12 10:19

### 변경 요약
- GitHub Pages용 정적 Awesome-style 논문 큐레이션 사이트의 초기 구현을 생성했습니다.
- OpenAlex, Crossref, 선택적 Semantic Scholar, 선택적 OpenAI 요약 생성을 포함한 Python 업데이트 파이프라인을 추가했습니다.
- 저작권 정책상 raw abstract와 PDF를 저장하지 않는 데이터 흐름을 코드와 문서에 명시했습니다.

### 수정/생성한 파일
- `index.html`: 헤더, 안내 문구, 통계, 검색/필터 UI, 논문 목록 영역을 가진 정적 페이지를 생성했습니다.
- `assets/style.css`: academic Awesome-list 스타일의 반응형 레이아웃과 카드/배지/버튼 스타일을 구현했습니다.
- `assets/app.js`: `data/papers.json` 로딩, 검색, 카테고리 필터, 연도 필터, 정렬, 통계, citation 복사 기능을 구현했습니다.
- `data/papers.json`: 초기 빈 논문 데이터 배열을 생성했습니다.
- `data/queries.json`: 기본 검색어 배열을 생성했습니다.
- `scripts/fetch_openalex.py`: OpenAlex Works API 조회와 메타데이터 정규화를 구현했습니다.
- `scripts/fetch_crossref.py`: Crossref Works API 조회와 메타데이터 정규화를 구현했습니다.
- `scripts/enrich_semantic_scholar.py`: `SEMANTIC_SCHOLAR_API_KEY`가 있을 때 DOI 기반 선택적 보강을 구현했습니다.
- `scripts/summarize.py`: OpenAI 기반 한글 요약 생성과 API key가 없을 때의 fallback 요약/태그/카테고리/관련성 점수 생성을 구현했습니다.
- `scripts/update_papers.py`: 검색어 순회, API 호출, 중복 제거, 새 논문 요약, transient abstract 제거, `papers.json` 저장을 orchestration합니다.
- `requirements.txt`: `requests`, `openai` 의존성을 추가했습니다.
- `.github/workflows/update-papers.yml`: 매시 실행, 수동 실행, 데이터 변경 시 자동 커밋 workflow를 추가했습니다.
- `README.md`: 프로젝트 목적, 데이터 출처, 저작권 정책, API key, 로컬 실행, Pages 배포, 수동 수정, 검색어 수정, 한계점을 한글로 문서화했습니다.
- `ARCHITECTURE.md`: 전체 구조, 프론트엔드, 데이터, Python 파이프라인, GitHub Actions, 환경변수, 저작권 정책을 설명했습니다.
- `PROJECT_STATUS.md`: 완료/부분 구현/미구현 기능, 알려진 문제, 다음 작업 순서를 정리했습니다.
- `AGENT_LOG.md`: 현재 작업 기록과 인수인계 정보를 생성했습니다.

### 구현한 기능
- GitHub Pages에서 동작하는 빌드 없는 정적 웹사이트
- 논문 카드에 제목, 저자, 연도, venue, DOI/source 링크, source API, 카테고리, 태그, 관련성 점수, 한글 AI 요약, 마지막 업데이트 표시
- 키워드 검색, 카테고리 필터, 연도 필터, 관련성/최신/제목 정렬
- 상단 통계: 전체 논문 수, 카테고리 수, 최신 업데이트 날짜, 이번 주 추가 논문 수
- OpenAlex와 Crossref 기반 최소 수집 파이프라인
- Semantic Scholar 선택적 보강
- OpenAI 선택적 한글 요약 생성
- OpenAI key가 없을 때 abstract 원문을 복사하지 않는 fallback 요약
- DOI 우선 중복 제거, DOI가 없으면 normalized title 중복 제거
- 새 논문이 없으면 GitHub Actions가 실패하지 않는 자동 업데이트

### 설계 결정
- 출판사 웹사이트 크롤링 대신 OpenAlex/Crossref/Semantic Scholar 공식 API만 사용했습니다.
- PDF는 다운로드하지 않고 저장 필드 `pdf_stored`를 항상 `false`로 둡니다.
- API abstract는 `_abstract` transient 필드로만 전달하고 저장 직전 제거합니다. raw abstract를 표시하지 않는 이유는 출판사 초록 문장의 재게시 위험을 줄이고, 사이트가 AI가 새로 작성한 한글 요약만 제공하도록 하기 위해서입니다.
- `OPENAI_API_KEY`가 없어도 자동 업데이트가 멈추지 않도록 fallback 요약을 만들었습니다. 이 fallback은 제목과 메타데이터 기반으로 작성되어 초록 문장을 복사하지 않습니다.
- 새 논문이 없는 실행도 정상 상태이므로 workflow가 실패하지 않게 했습니다. 정기 실행에서 변경 없음은 오류가 아니라 기대 가능한 상태입니다.
- 클라이언트 코드는 `papers.json`만 읽고 모든 API key는 GitHub Actions 환경변수로만 사용합니다.

### 남은 작업
- 실제 API 실행으로 `data/papers.json`을 채우고 결과 품질을 검수해야 합니다.
- 관련 없는 논문이 많이 들어오면 `_is_plausible` 필터와 검색어를 조정해야 합니다.
- Source 열기 버튼은 현재 DOI URL을 사용하므로 API별 source landing URL을 별도 필드로 확장할 수 있습니다.
- 브라우저에서 GitHub Pages 배포 화면과 모바일 반응형을 확인하면 좋습니다.

### 주의사항
- API key, secret, token 값은 문서나 로그에 기록하지 마세요.
- `data/papers.json`에 raw abstract 또는 PDF 경로를 추가하지 마세요.
- 자동 커밋은 `data/papers.json` 변경 시에만 수행됩니다.
- OpenAI 요약은 새 논문에 대해서만 생성됩니다. 기존 논문의 요약을 재생성하려면 해당 항목을 수동으로 제거하거나 별도 재요약 스크립트를 추가해야 합니다.

## 2026-06-12 10:20

### 변경 요약
- 로컬 Windows PowerShell에서 실제 업데이트 스크립트를 실행하던 중 유니코드 논문 제목 출력이 CP949 인코딩에서 실패하는 문제를 발견하고 수정했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 실행 시작 시 `sys.stdout` 인코딩을 UTF-8로 재설정하도록 수정했습니다.
- `AGENT_LOG.md`: 검증 중 발견한 문제와 수정 내용을 기록했습니다.

### 구현한 기능
- 유니코드 하이픈, 특수기호, 비영문 논문 제목이 로그에 포함되어도 Windows 콘솔에서 업데이트가 중단되지 않도록 했습니다.

### 설계 결정
- 논문 제목을 손실 변환하지 않고 UTF-8 출력 환경을 우선 설정했습니다. GitHub Actions의 Ubuntu 환경에도 무해한 변경입니다.

### 남은 작업
- 업데이트 스크립트를 다시 실행해 실제 API 수집과 `data/papers.json` 저장까지 검증해야 합니다.

### 주의사항
- 이 변경은 출력 인코딩만 다루며, 저장 데이터의 UTF-8 정책은 그대로 유지됩니다.

## 2026-06-12 10:21

### 변경 요약
- 실제 OpenAlex/Crossref API를 사용해 업데이트 파이프라인을 실행했고 `data/papers.json`에 9편의 논문을 저장했습니다.
- 저장 데이터 정책과 로컬 정적 서버 응답을 검증했습니다.
- 현재 프로젝트 상태 문서를 실제 데이터 상태에 맞게 갱신했습니다.

### 수정/생성한 파일
- `data/papers.json`: API 검색 결과 9편을 사용자 요구 스키마에 맞춰 저장했습니다.
- `PROJECT_STATUS.md`: 현재 논문 수, 검증 결과, 알려진 큐레이션 품질 이슈, 다음 작업 순서를 갱신했습니다.
- `AGENT_LOG.md`: 실제 실행 및 검증 기록을 추가했습니다.

### 구현한 기능
- 로컬에서 `python scripts/update_papers.py` 실행 성공을 확인했습니다.
- `python -m py_compile`로 Python 스크립트 문법 검사를 통과했습니다.
- `data/papers.json`에 `_abstract` transient 필드가 남지 않는지 확인했습니다.
- 모든 저장 항목의 `raw_abstract_displayed=false`, `pdf_stored=false`를 확인했습니다.
- `python -m http.server 8000`으로 로컬 정적 서버를 띄우고 `index.html`, `data/papers.json` HTTP 200 응답을 확인했습니다.

### 설계 결정
- 초기 데이터가 완전히 비어 있으면 UI는 동작하지만 큐레이션 사이트로 바로 확인하기 어렵기 때문에, 공식 메타데이터 API를 한 번 실행해 seed 데이터를 생성했습니다.
- 일부 넓은 주제의 논문이 포함될 수 있음을 문서화하고, 다음 작업자가 검색어와 필터를 조정하도록 인수인계했습니다.

### 남은 작업
- 수집된 9편을 사람이 검수해 이 저장소의 핵심 범위와 맞지 않는 항목을 제거하거나 필터를 강화해야 합니다.
- 브라우저 자동화 도구가 현재 세션에 노출되지 않아 스크린샷 기반 검증은 수행하지 못했습니다. 로컬 서버와 HTTP 응답 검증은 완료했습니다.

### 주의사항
- 로컬 확인용 서버는 `http://localhost:8000`에서 실행 중이며 프로세스 ID는 `16360`입니다.
- 다음 에이전트가 같은 포트를 사용하려면 기존 서버 프로세스를 종료하거나 다른 포트를 선택하세요.

## 2026-06-12 10:22

### 변경 요약
- 업데이트 스크립트를 같은 데이터 상태에서 재실행해 새 논문이 없는 경우에도 성공 종료되는지 확인했습니다.

### 수정/생성한 파일
- `AGENT_LOG.md`: 새 논문 없음 경로 검증 결과를 추가했습니다.

### 구현한 기능
- `python scripts/update_papers.py` 재실행 결과 `Added 0 new papers`, `No changes in data/papers.json`로 정상 종료됨을 확인했습니다.

### 설계 결정
- 정기 실행에서 새 논문이 없는 상황은 오류가 아니므로, workflow가 실패하지 않는 현재 동작을 유지합니다.

### 남은 작업
- 실제 GitHub Actions 환경에서 secrets 설정 후 수동 실행으로 동일 동작을 확인하면 됩니다.

### 주의사항
- 새 논문이 없을 때 자동 커밋 단계는 `git diff --quiet -- data/papers.json` 조건으로 건너뜁니다.

## 2026-06-12 10:23

### 변경 요약
- 원격 GitHub 저장소 `lko9911/GPT_Paper_research`에 초기 사이트 구현을 커밋하고 push했습니다.
- GitHub Pages 배포를 자동화하기 위한 별도 workflow와 Python 캐시 제외 규칙을 추가했습니다.

### 수정/생성한 파일
- `.gitignore`: Python 캐시, 가상환경, `.env` 파일이 커밋되지 않도록 추가했습니다.
- `.github/workflows/deploy-pages.yml`: `main` 브랜치 push 또는 수동 실행 시 정적 사이트를 GitHub Pages로 배포하는 workflow를 추가했습니다.
- `AGENT_LOG.md`: 원격 push와 배포 workflow 추가 내용을 기록했습니다.

### 구현한 기능
- GitHub Actions 기반 Pages 배포 경로를 추가했습니다.
- 캐시 파일이 이후 커밋에 포함되지 않도록 방지했습니다.

### 설계 결정
- GitHub 저장소 Settings에서 branch 배포를 수동 설정하지 않아도 동작할 가능성이 높은 `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages` 조합을 사용했습니다.

### 남은 작업
- GitHub 저장소의 Pages 설정이 GitHub Actions 배포를 허용하는지 확인해야 합니다.
- 이미 올라간 `scripts/__pycache__` 파일은 다음 커밋에서 제거해야 합니다.

### 주의사항
- GitHub Pages URL은 배포 workflow가 성공한 뒤 `https://lko9911.github.io/GPT_Paper_research/` 형태로 접근할 수 있습니다.

## 2026-06-12 10:24

### 변경 요약
- `BunnySoCrazy/Awesome-3D-Generation`의 큰 방향인 topic navigation, 카테고리별 compact list, pill형 링크/태그 구조를 참고해 UI를 재설계했습니다.
- 원본 사이트의 시각 요소나 데이터 구조를 복제하지 않고, MMAM/FGAM 논문 트래커에 맞는 독립적인 정보 구조로 바꿨습니다.

### 수정/생성한 파일
- `index.html`: 상단 topic navigation과 태그 필터 select를 추가하고, 깨져 보이던 한글 문자열을 UTF-8 기준으로 다시 정리했습니다.
- `assets/app.js`: featured topic 필터, 태그 필터, 카테고리별 그룹 렌더링, 태그 클릭 필터링, compact paper row 렌더링을 구현했습니다.
- `assets/style.css`: 카드형 UI를 카테고리 섹션 + 논문 row + 우측 score/link rail 구조로 재설계했습니다.
- `AGENT_LOG.md`: UI 참고 방향과 변경 사항을 기록했습니다.

### 구현한 기능
- 상단 topic pill 클릭으로 MMAM, FGAM, DM filament, 계산설계 등 주요 태그를 빠르게 필터링합니다.
- 카테고리별로 논문 목록이 묶여 Awesome-list처럼 훑어보기 쉬워졌습니다.
- 각 논문은 제목, 메타데이터, 요약, 관련성 설명, category/tag, score, year, Paper/DOI/Copy Cite 링크를 compact하게 표시합니다.
- 태그 badge를 클릭하면 해당 태그로 필터링됩니다.

### 설계 결정
- 참고 레포처럼 topic-first 탐색과 compact listing 감각은 가져오되, visual preview table은 사용하지 않았습니다. 이 프로젝트는 PDF/이미지 미리보기를 저장하지 않는 정책이 있으므로 텍스트 기반 큐레이션이 더 적합합니다.
- Paper 링크는 DOI URL로 연결하여 원문 접근을 공식 DOI/source로 유도합니다.

### 남은 작업
- GitHub Pages 배포 후 실제 공개 URL에서 UI 렌더링을 확인해야 합니다.
- 브라우저 기반 시각 검증 도구가 없으면 HTTP 응답과 정적 파일 검증으로 대체합니다.

### 주의사항
- 참고 사이트를 그대로 복사하지 말라는 요구에 맞춰 색상, 레이아웃, 데이터 표현, 텍스트를 독립적으로 구성했습니다.

## 2026-06-12 10:25

### 변경 요약
- 사용자의 요청에 따라 주제별 행, 게재지별 열로 논문 분포를 볼 수 있는 매트릭스 UI를 추가했습니다.
- 게재지 필터를 추가하고, 매트릭스 셀 클릭으로 해당 주제와 게재지 조합을 바로 필터링할 수 있게 했습니다.

### 수정/생성한 파일
- `index.html`: 게재지 필터 select와 `Topic x Venue` 매트릭스 섹션을 추가했습니다.
- `assets/app.js`: venue 수집, 상위 venue column 생성, 주제 x 게재지 matrix 렌더링, matrix cell 클릭 필터, matrix filter 해제 기능을 구현했습니다.
- `assets/style.css`: matrix table, count cell, active cell, responsive horizontal scroll 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 매트릭스 기능 구현 내용을 기록했습니다.

### 구현한 기능
- 행은 카테고리/주제, 열은 게재지로 구성된 논문 수 분포표를 표시합니다.
- 셀의 숫자를 클릭하면 해당 주제와 게재지 조합에 맞는 논문만 아래 목록에 표시됩니다.
- `매트릭스 필터 해제` 버튼으로 matrix 기반 필터를 초기화할 수 있습니다.
- 게재지별 select 필터를 검색 UI에 추가했습니다.
- 게재지가 많아질 경우 상위 8개 게재지를 열로 보여주고 나머지는 `Other venues`로 묶도록 설계했습니다.

### 설계 결정
- 현재 데이터는 9편이고 게재지가 모두 1편씩이지만, 앞으로 자동 수집으로 열이 늘어날 수 있어 기본 상한을 8개로 설정했습니다.
- 매트릭스는 전체 데이터 분포를 보여주고, 검색/태그/연도 필터와 조합되어 아래 목록을 좁히는 탐색 도구로 사용됩니다.

### 남은 작업
- 실제 배포 후 공개 URL에서 matrix UI가 표시되는지 확인해야 합니다.
- 논문 수가 많아지면 venue alias 정규화 규칙을 추가해 같은 학회/저널의 표기 차이를 합칠 수 있습니다.

### 주의사항
- venue 값은 OpenAlex/Crossref 메타데이터 품질에 의존합니다. 비어 있으면 `Venue unknown`으로 표시됩니다.

## 2026-06-12 10:26

### 변경 요약
- 사용자가 지적한 2030년 논문 항목을 조사했고, 출판연도가 아니라 원문 저장소의 embargo 종료일이 메타데이터에 섞인 값으로 판단해 수정했습니다.
- 미래 연도 같은 비정상 publication year가 다시 저장되지 않도록 방어 로직을 추가했습니다.

### 수정/생성한 파일
- `data/papers.json`: DOI `10.7273/000007857` 항목의 year를 2030에서 2025로, venue를 `Open MIND`에서 `Washington State University Dissertation`으로 보정했습니다. 요약과 관련성 설명에서도 2030 표현을 제거했습니다.
- `scripts/update_papers.py`: 저장 전 publication year가 1900 미만이거나 현재 연도보다 1년을 초과하면 비정상 값으로 보고 `None` 처리하는 `_safe_year` 함수를 추가했습니다.
- `AGENT_LOG.md`: 데이터 품질 이슈와 수정 내용을 기록했습니다.

### 구현한 기능
- 잘못된 미래 연도 메타데이터가 사이트에 표시되지 않도록 했습니다.
- 수동 검수로 확인된 학위논문 메타데이터를 보정했습니다.

### 설계 결정
- 학술 메타데이터 API가 embargo date, online ahead date, deposit date 등을 publication year처럼 잘못 전달할 수 있으므로, 현재 연도보다 1년 이상 미래인 값은 표시하지 않는 보수적 정책을 적용했습니다.
- 사용자가 이미 본 잘못된 항목은 실제 출처 확인 후 2025년 학위논문으로 수동 보정했습니다.

### 남은 작업
- 향후 데이터 품질을 더 높이려면 DOI별 Crossref/OpenAlex/Semantic Scholar 값을 비교해 연도 충돌 시 더 신뢰도 높은 값을 선택하는 로직을 추가할 수 있습니다.

### 주의사항
- 원문 저장소에 PDF 항목이 있더라도 이 프로젝트는 PDF를 다운로드하거나 저장하지 않습니다.

## 2026-06-12 10:27

### 변경 요약
- 사용자의 요청에 따라 자동 조사 범위를 2025년 이후로 고정하고, 논문을 가져오는 기준을 문서화했습니다.
- Science/Nature 계열 게재지도 공식 메타데이터 API에서 검색되고 주제 기준을 만족하면 포함될 수 있음을 명확히 했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: `SINCE_YEAR` 환경변수와 기본값 `2025`를 추가하고, OpenAlex/Crossref 호출에 시작 연도 필터를 전달하도록 수정했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 실행 환경에 `SINCE_YEAR: "2025"`를 명시했습니다.
- `README.md`: 조사 범위, 논문 수집 기준, Science/Nature 포함 가능 조건을 추가했습니다.
- `ARCHITECTURE.md`: 업데이트 파이프라인과 환경변수 설명에 `SINCE_YEAR`를 추가했습니다.
- `PROJECT_STATUS.md`: 2025년 이후 수집 기준과 Science/Nature 계열 처리 방침을 기록했습니다.
- `data/papers.json`: PowerShell 인코딩 영향으로 깨져 있던 수동 보정 요약 문장을 UTF-8 한글 문장으로 복구했습니다.
- `AGENT_LOG.md`: 이번 기준 변경과 검증 내용을 기록했습니다.

### 구현한 기능
- 기본적으로 2025년 이후 논문만 수집합니다.
- 2025년 이전 논문은 `_is_plausible` 단계에서 제외됩니다.
- 현재 연도보다 1년을 초과하는 미래 연도는 비정상 메타데이터로 버립니다.
- 공식 API에서 검색되는 모든 게재지를 대상으로 하며 Science, Nature 같은 특정 출판사를 배제하지 않습니다.

### 설계 결정
- 게재지 이름으로 포함 여부를 결정하지 않고, 연구 주제와 연도 기준으로 포함 여부를 판단합니다. 고급 저널만 따로 크롤링하면 저작권/접근 정책 리스크가 커지기 때문입니다.
- Science/Nature 논문도 DOI와 메타데이터 API를 통해 들어오는 경우만 포함합니다.

### 남은 작업
- 원한다면 `target_venues.json` 같은 파일을 추가해 Science, Nature, Nature Communications, Advanced Materials 등 관심 게재지를 우선 표시하거나 별도 필터로 강조할 수 있습니다.

### 주의사항
- 메타데이터 API에는 embargo date나 잘못된 미래 연도 값이 섞일 수 있어 방어 로직이 필요합니다.

## 2026-06-12 10:28

### 변경 요약
- Nature, Science, Additive Manufacturing 계열 게재지를 우선 추적 대상으로 추가했습니다.
- 프론트엔드 JS의 한글 UI 문자열을 UTF-8 기준으로 다시 정리했습니다.

### 수정/생성한 파일
- `index.html`: 상단에 우선 추적 게재지 navigation을 추가했습니다.
- `assets/app.js`: `TARGET_VENUES` 목록, target venue chip, target venue 필터링, 우선 게재지 count 표시, 축약 venue 이름 표시를 구현했습니다.
- `assets/style.css`: 우선 게재지 pill 스타일을 추가했습니다.
- `data/queries.json`: Additive Manufacturing, Nature, Science 조합 검색어를 추가했습니다.
- `README.md`: 우선 추적 게재지 목록을 문서화했습니다.
- `PROJECT_STATUS.md`: 우선 추적 게재지 상태와 다음 개선 작업을 기록했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- Nature, Nature Communications, Nature Materials, Nature Reviews Materials, Science, Science Advances, Science Robotics, Additive Manufacturing을 별도 칩으로 보여줍니다.
- 각 칩에는 현재 수집된 논문 수가 표시됩니다.
- 칩을 클릭하면 해당 게재지 논문만 필터링됩니다.
- 게재지 select에도 우선 추적 게재지가 포함됩니다.

### 설계 결정
- 특정 출판사 사이트를 직접 크롤링하지 않고 공식 메타데이터 API에서 검색되는 항목만 포함합니다.
- 지금 단계에서는 source ID 고정 검색보다 검색어 보강과 UI 강조를 먼저 적용했습니다. OpenAlex source ID 기반 검색은 다음 단계에서 더 정확하게 추가할 수 있습니다.

### 남은 작업
- Nature/Science/Additive Manufacturing 논문을 더 정확히 모으려면 OpenAlex Sources API로 source ID를 고정한 venue-specific 검색을 추가하세요.

### 주의사항
- 현재 데이터에 해당 게재지 논문이 없으면 칩 count가 0으로 표시됩니다. 0은 배제가 아니라 아직 수집 결과가 없다는 뜻입니다.

## 2026-06-12 10:29

### 변경 요약
- 사용자가 지정한 `BunnySoCrazy/Awesome-3D-Generation`의 실제 `index.html` UI 방향을 참고해, 현재 사이트를 gallery-style awesome list에 더 가깝게 재구성했습니다.
- 그대로 복제하지 않고, 이 프로젝트의 저작권 정책에 맞게 이미지 미리보기 대신 자동 생성 preview tile을 사용했습니다.

### 수정/생성한 파일
- `index.html`: 중앙 정렬 헤더 폭을 넓히고, 본문을 sticky sidebar + content 레이아웃으로 변경했습니다. `side-topic-nav`, `side-venue-nav` 빠른 탐색 영역을 추가했습니다.
- `assets/app.js`: sidebar navigation 생성, 카테고리별 anchor id 생성, paper row 렌더링을 gallery card 렌더링으로 변경, preview tile initials 생성 기능을 추가했습니다.
- `assets/style.css`: 참고 UI의 핵심 감각인 넓은 페이지, sticky sidebar, section title left accent, auto-fill card grid, hover lift/scale, preview area, card content/link layout을 우리 디자인으로 재작성했습니다.
- `AGENT_LOG.md`: UI 재구성 의도와 변경 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 sidebar에서 카테고리 섹션으로 빠르게 이동할 수 있습니다.
- 왼쪽 sidebar에서 Nature/Science/Additive Manufacturing 등 우선 게재지 필터를 바로 적용할 수 있습니다.
- 논문 목록은 카테고리별 grid card로 표시됩니다.
- 각 카드 상단에는 PDF/이미지 대신 카테고리 약어, 연도, 관련성 점수를 보여주는 preview tile이 표시됩니다.
- 카드 hover 시 살짝 떠오르는 gallery interaction을 적용했습니다.

### 설계 결정
- 참고 사이트의 실제 preview image 카드는 그대로 가져오지 않았습니다. 이 프로젝트는 PDF, 출판사 이미지, 원문 초록을 호스팅하지 않는 정책이 있으므로, 이미지 대신 메타데이터 기반 preview tile을 생성하는 방식이 더 안전합니다.
- 참고 UI의 구조적 특징인 header, sidebar, section, card grid, link pill만 우리 데이터 모델에 맞게 재해석했습니다.

### 남은 작업
- 브라우저 자동화 도구가 현재 세션에 노출되지 않아 스크린샷 기반 시각 검증은 수행하지 못했습니다. 배포 후 실제 브라우저에서 card grid와 sidebar 스크롤을 확인하면 좋습니다.

### 주의사항
- `assets/app.js`는 Node가 설치되어 있지 않아 `node --check`로 문법 검사를 수행할 수 없습니다. 정적 훅과 로컬 HTTP 응답 검증으로 대체했습니다.

## 2026-06-12 10:30

### 변경 요약
- 사용자가 논문이 표시되지 않는다고 알려주어 프론트엔드 렌더링 문제를 조사했습니다.
- JS 파일은 내려오고 데이터도 정상 제공되지만, optional chaining 같은 최신 JS 문법이 일부 브라우저/검증 환경에서 스크립트 실행을 막을 수 있음을 확인했습니다.

### 수정/생성한 파일
- `assets/app.js`: optional chaining `?.`, `Array.prototype.at`, `String.prototype.replaceAll`, `Array.prototype.flatMap` 사용을 제거하고 더 호환성 높은 문법으로 변경했습니다.
- `assets/style.css`: 필수 기능이 아닌 CSS `:has()` 선택자를 제거했습니다.
- `AGENT_LOG.md`: 표시 오류 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- 구형 또는 제한된 브라우저 환경에서도 JS가 파싱되고 논문 렌더링이 실행될 가능성을 높였습니다.
- Python `esprima` 파서로 `assets/app.js` 문법 검사를 통과했습니다.
- 로컬 HTTP 서버에서 `index.html`과 `assets/app.js` 응답을 확인했습니다.

### 설계 결정
- 최신 문법의 간결함보다 GitHub Pages 방문자의 브라우저 호환성을 우선했습니다.
- 논문이 표시되지 않는 장애를 막기 위해 렌더링 경로의 optional chaining과 최신 prototype 메서드를 제거했습니다.

### 남은 작업
- 공개 Pages 배포 후 실제 URL에서 사용자가 논문 카드가 보이는지 확인해야 합니다.

### 주의사항
- Node가 설치되어 있지 않아 `node --check`는 계속 사용할 수 없습니다. 대신 `esprima` 기반 문법 검사를 사용했습니다.

## 2026-06-12 10:31

### 변경 요약
- 사용자가 sidebar `Venues`가 실제 기능을 하지 않는다고 지적해 UX를 수정했습니다.
- 우선 추적 게재지에 현재 논문이 0편이면 클릭 가능한 필터처럼 보이지 않도록 비활성화했습니다.
- sidebar `Venues`에는 실제 데이터에 존재하는 모든 게재지를 표시하고 클릭 시 필터링되도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: 실제 venue count 목록 생성, sidebar venue 필터링, All venues 버튼, 0개 우선 게재지 비활성화, venue priority 판별 함수를 추가했습니다.
- `assets/style.css`: 비활성 venue pill 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UX 수정 내용을 기록했습니다.

### 구현한 기능
- sidebar `Venues`에서 현재 수집된 게재지별 논문 수를 볼 수 있습니다.
- 실제 게재지를 클릭하면 해당 venue 논문만 표시됩니다.
- `All venues`를 클릭하면 venue 필터를 해제합니다.
- Nature/Science/Additive Manufacturing 등 우선 추적 게재지는 논문이 0편이면 disabled 상태로 표시됩니다.

### 설계 결정
- 0개 우선 게재지 칩을 숨기지 않고 비활성화했습니다. 사용자가 해당 게재지가 추적 대상임은 알 수 있고, 동시에 현재는 결과가 없다는 것도 알 수 있기 때문입니다.

### 남은 작업
- 공개 Pages 배포 후 sidebar venue 필터가 보이는지 확인해야 합니다.

### 주의사항
- 현재 데이터의 venue는 모두 1편씩이라 sidebar venue 필터는 각 게재지별로 1편씩 표시할 가능성이 큽니다.

## 2026-06-12 10:32

### 변경 요약
- 사용자의 요청에 따라 논문 카드의 이미지/preview 영역을 제거했습니다.
- 연도와 관련성 점수는 카드 상단의 작은 텍스트 badge로 이동했습니다.

### 수정/생성한 파일
- `assets/app.js`: `preview-tile` 렌더링과 `previewInitials` 함수를 제거하고 `card-topline` badge를 추가했습니다.
- `assets/style.css`: preview tile 스타일을 제거하고 card topline badge 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 단순화 작업을 기록했습니다.

### 구현한 기능
- 논문 카드는 이제 이미지 없이 텍스트 중심으로 표시됩니다.
- 카드 상단에는 연도와 관련성 점수만 compact하게 표시됩니다.

### 설계 결정
- 이미지/preview 영역을 제거하면 참고 사이트와는 다소 달라지지만, 이 프로젝트의 저작권 정책과 논문 큐레이션 목적에는 더 적합합니다.

### 남은 작업
- 공개 Pages 배포 후 카드가 이미지 없이 정상 표시되는지 확인해야 합니다.

### 주의사항
- 향후 이미지가 필요하더라도 출판사 figure, PDF thumbnail, abstract image를 저장하지 않는 정책은 유지해야 합니다.

## 2026-06-12 10:33

### 변경 요약
- 사용자의 요청에 따라 자동 조사 시작 연도를 2024년으로 변경했습니다.
- 프론트엔드 기본 정렬을 관련성 점수순에서 최신순으로 변경했습니다.
- 2024년 이후 기준으로 업데이트 스크립트를 실행해 새 논문 1편을 추가했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 기본 `SINCE_YEAR`를 2025에서 2024로 변경했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 환경변수 `SINCE_YEAR`를 `2024`로 변경했습니다.
- `index.html`: 정렬 select의 기본 옵션을 `최신순`으로 변경했습니다.
- `README.md`: 조사 범위 설명을 2024년 이후로 수정했습니다.
- `ARCHITECTURE.md`: 파이프라인 시작 연도와 환경변수 설명을 2024로 수정했습니다.
- `PROJECT_STATUS.md`: 완료 기능의 조사 범위를 2024년 이후로 수정했습니다.
- `data/papers.json`: 2024년 이후 기준 재수집으로 새 논문 1편을 추가했습니다.
- `AGENT_LOG.md`: 이번 조사 범위 변경과 검증 내용을 기록했습니다.

### 구현한 기능
- 자동 수집은 이제 2024년 이후 논문을 대상으로 합니다.
- 웹사이트의 기본 정렬은 최신순입니다.
- 로컬에서 `SINCE_YEAR=2024 python scripts/update_papers.py` 실행을 완료했습니다.

### 설계 결정
- 시작 연도는 코드 기본값과 GitHub Actions 환경변수를 둘 다 변경했습니다. 로컬 실행과 CI 실행이 서로 다른 범위를 쓰지 않도록 하기 위해서입니다.

### 남은 작업
- 2024년 논문이 실제로 들어오는지 다음 정기 업데이트 결과를 관찰해야 합니다. 현재 데이터에는 2025년과 2026년 항목만 있습니다.

### 주의사항
- 2024년 이후 범위이므로 2024, 2025, 2026 항목이 모두 포함될 수 있습니다.
