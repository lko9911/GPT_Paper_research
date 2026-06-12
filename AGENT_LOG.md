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

## 2026-06-12 10:34

### 변경 요약
- 사용자가 Nature/Science/Additive Manufacturing에 논문이 없는 이유를 물어, 기존 파이프라인이 venue 이름을 검색어에 섞는 수준이었고 실제 저널 내부 검색을 하지 않았음을 확인했습니다.
- OpenAlex source ID 기반 우선 게재지 검색을 추가했습니다.
- 2024년 이후 기준으로 업데이트를 실행해 우선 게재지 논문 12편을 추가했습니다.

### 수정/생성한 파일
- `data/target_venues.json`: Nature, Nature Communications, Nature Materials, Nature Reviews Materials, Science, Science Advances, Science Robotics, Additive Manufacturing의 OpenAlex source ID를 저장했습니다.
- `scripts/fetch_openalex.py`: `source_id` 인자를 추가해 `primary_location.source.id` 필터로 특정 게재지 내부 검색을 지원하도록 수정했습니다.
- `scripts/update_papers.py`: 일반 검색 후 `data/target_venues.json`을 순회하며 우선 게재지 내부 검색을 수행하도록 확장했습니다.
- `data/papers.json`: 우선 게재지 검색 결과 12편을 추가해 총 22편이 되었습니다.
- `README.md`: 우선 게재지 목록이 source ID 기반으로 검색된다는 설명을 추가했습니다.
- `ARCHITECTURE.md`: target venue 검색 단계를 파이프라인 설명에 추가했습니다.
- `AGENT_LOG.md`: 이번 원인 분석과 구현 내용을 기록했습니다.

### 구현한 기능
- 우선 게재지별 OpenAlex source ID 검색
- Nature Communications, Science, Additive Manufacturing 등에서 공식 API 메타데이터 기반 논문 수집
- 기존 DOI/title 중복 제거와 저작권 정책 유지

### 설계 결정
- 저널 페이지를 직접 크롤링하지 않고 OpenAlex source ID를 사용했습니다. 이 방식은 공식 메타데이터 API만 사용하면서도 특정 게재지 안의 논문을 정확히 찾을 수 있습니다.
- venue별 검색은 API 호출 수를 과도하게 늘리지 않도록 기본 검색어 앞쪽 6개만 사용합니다.

### 남은 작업
- target venue별 검색어를 별도 파일로 세분화하면 Nature/Science 계열의 관련 없는 논문 유입을 더 줄일 수 있습니다.
- 새로 추가된 12편의 관련성을 사람이 검수하면 큐레이션 품질이 좋아집니다.

### 주의사항
- 현재 target venue count는 Additive Manufacturing 9편, Nature Communications 2편, Science 1편입니다.

## 2026-06-12 10:35

### 변경 요약
- 사용자가 `툴패스 계획`, `그래프 탐색 / 경로 계획 알고리즘`, `툴패스`, `경로계획`처럼 카테고리와 태그가 중복 노출되는 문제를 지적해 개선했습니다.

### 수정/생성한 파일
- `assets/app.js`: 표시용 태그에서 카테고리와 동일하거나 의미가 겹치는 태그를 숨기는 `visibleTags` 로직을 추가했습니다.
- `scripts/summarize.py`: 새로 생성되는 요약/태그에서도 카테고리와 중복되는 태그를 제거하도록 `_dedupe_tags` 로직을 추가했습니다.
- `data/papers.json`: 기존 22편의 태그를 중복 제거 규칙으로 정리했습니다.
- `AGENT_LOG.md`: 이번 태그 중복 개선 내용을 기록했습니다.

### 구현한 기능
- 카드에 카테고리와 같은 태그가 반복 표시되지 않습니다.
- `툴패스`는 `툴패스 계획` 카테고리가 있을 때 숨깁니다.
- `경로계획`은 `그래프 탐색 / 경로 계획 알고리즘` 카테고리가 있을 때 숨깁니다.
- `MMAM`, `FGAM`, `재료분포`, `퍼지 감소`, `AI/ML`도 각각 대응 카테고리와 중복되면 숨깁니다.

### 설계 결정
- 데이터 스키마의 `categories`와 `tags`는 유지하되, UI에서는 중복 태그를 숨기고 데이터 생성 단계에서는 새 중복을 줄이는 이중 방어를 적용했습니다.

### 남은 작업
- 향후 더 많은 논문이 들어오면 태그 alias 목록을 추가로 확장할 수 있습니다.

### 주의사항
- 중복 태그를 숨기더라도 검색 haystack에는 표시용 태그가 반영되므로, 카테고리/태그 필터 설계를 계속 관찰해야 합니다.

## 2026-06-12 10:36

### 변경 요약
- 사용자가 Nature Communications DOI `10.1038/s41467-024-47480-5` 논문이 검색되지 않는 문제를 제기했습니다.
- 원인은 OpenAlex venue 검색이 최신순 상위 일부만 가져와 2024 핵심 논문이 최신 2026 논문 뒤로 밀린 것이었습니다.
- 검색 순위에 의존하지 않도록 seed DOI 직접 조회 기능을 추가하고 해당 논문을 추가했습니다.

### 수정/생성한 파일
- `data/seed_dois.json`: 중요 논문 DOI 목록을 추가하고 `10.1038/s41467-024-47480-5`를 등록했습니다.
- `scripts/fetch_openalex.py`: DOI로 OpenAlex works endpoint를 직접 조회하는 `fetch_openalex_by_doi` 함수를 추가했습니다.
- `scripts/update_papers.py`: seed DOI를 먼저 조회하고 기존 중복 제거/요약/저장 파이프라인에 태우도록 수정했습니다.
- `data/papers.json`: `3D printing with a 3D printed digital material filament for programming functional gradients` 논문을 추가했습니다.
- `README.md`: 자동 검색에서 누락되는 중요 논문은 `data/seed_dois.json`에 DOI를 추가하는 방식으로 보완할 수 있음을 문서화했습니다.
- `ARCHITECTURE.md`: seed DOI 조회 단계를 파이프라인 설명에 추가했습니다.
- `AGENT_LOG.md`: 이번 누락 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- DOI 기반 강제 포함 후보 조회
- 검색 순위에서 밀리는 핵심 논문 보완
- 기존 저작권 정책 유지: abstract 저장 없음, PDF 저장 없음

### 설계 결정
- 특정 Nature 페이지를 크롤링하지 않고 DOI를 통해 OpenAlex 공식 메타데이터를 조회했습니다.
- seed DOI는 사람이 중요 논문을 알고 있을 때 사용하는 보완 경로로 설계했습니다.

### 남은 작업
- 핵심 분야 논문을 추가로 알고 있다면 `data/seed_dois.json`에 DOI를 계속 추가하면 됩니다.

### 주의사항
- seed DOI도 `_is_plausible`의 주제/연도 필터를 통과해야 저장됩니다.

## 2026-06-12 10:37

### 변경 요약
- 사용자의 UI 요청에 따라 왼쪽 floating 패널은 분야 선택 전용으로 정리하고, 게재지는 본문에서 별도 보드로 볼 수 있게 변경했습니다.

### 수정/생성한 파일
- `index.html`: sidebar에서 Venues nav를 제거하고, 본문에 `게재지별 보기` 섹션과 `venue-board`를 추가했습니다.
- `assets/app.js`: sidebar 분야 선택 버튼, venue board 렌더링, venue card 클릭 필터링 로직을 추가했습니다.
- `assets/style.css`: venue section, venue board, venue card 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 구조 변경을 기록했습니다.

### 구현한 기능
- 왼쪽 floating 패널에서는 분야/카테고리만 선택합니다.
- 본문 `게재지별 보기` 섹션에서 실제 게재지별 논문 수를 볼 수 있습니다.
- 게재지 카드를 클릭하면 아래 논문 목록이 해당 게재지로 필터링됩니다.
- `All venues` 카드로 게재지 필터를 초기화할 수 있습니다.

### 설계 결정
- 분야 선택과 게재지 선택을 분리해 탐색 목적을 명확히 했습니다.
- 게재지는 별도 보드로 제공해 Nature/Science/Additive Manufacturing 같은 우선 게재지와 실제 수집 게재지를 더 넓게 볼 수 있게 했습니다.

### 남은 작업
- 공개 Pages 배포 후 좌측 분야 패널과 게재지 보드가 의도대로 표시되는지 확인해야 합니다.

### 주의사항
- sidebar 분야 버튼은 category select와 동기화됩니다. 게재지 보드는 venue select 또는 priority venue 필터와 동기화됩니다.

## 2026-06-12 10:38

### 변경 요약
- 사용자가 “가져올 수 있는 것을 다 가져오되 100편을 넘으면 하지 말라”고 요청했습니다.
- 먼저 dry-run으로 확장 수집 후보를 확인했고, 총 50편으로 100편 이하임을 확인한 뒤 실제 수집을 수행했습니다.
- 기존 23편에서 27편을 추가해 총 50편이 되었습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 일반 검색 per-page와 target venue 검색 per-page를 50으로 확대하고, target venue 검색은 전체 검색어를 사용하도록 변경했습니다. `MAX_TOTAL_PAPERS` 기본값 100을 추가했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 환경변수 `MAX_TOTAL_PAPERS: "100"`을 추가했습니다.
- `data/papers.json`: 확장 수집 결과 27편을 추가했습니다.
- `README.md`: 자동 수집 총량 상한 100편 설명을 추가했습니다.
- `ARCHITECTURE.md`: `MAX_TOTAL_PAPERS` 환경변수 설명을 추가했습니다.
- `AGENT_LOG.md`: 이번 확장 수집 기록을 추가했습니다.

### 구현한 기능
- 확장 수집 기준에서 총량 100편 제한을 적용합니다.
- OpenAlex 일반 검색과 우선 게재지 검색을 더 넓게 가져옵니다.
- 2024년 이후, DOI/title 중복 제거, raw abstract/PDF 저장 금지 정책은 유지합니다.

### 설계 결정
- 100편 제한을 코드와 GitHub Actions 환경변수 양쪽에 명시했습니다.
- 너무 많은 논문을 무작정 가져오지 않도록 상한을 유지하면서, 현재 범위에서는 가능한 후보를 더 넓게 수집했습니다.

### 남은 작업
- 새로 추가된 27편 중 주제 적합성이 낮은 항목은 사람이 검수해 제거하거나 `_is_plausible` 필터를 더 엄격하게 조정할 수 있습니다.

### 주의사항
- 현재 데이터 분포는 총 50편, 2024년 6편, 2025년 22편, 2026년 22편입니다.

## 2026-06-12 10:39

### 변경 요약
- 사용자의 요청에 따라 `Topic x Venue / 주제별 게재지 분포` 매트릭스 섹션을 제거했습니다.

### 수정/생성한 파일
- `index.html`: matrix section HTML을 제거했습니다.
- `assets/app.js`: matrix 렌더링, matrix 필터 상태, matrix cell 클릭 필터링 관련 코드를 제거했습니다.
- `assets/style.css`: matrix table, matrix count, matrix section 스타일을 제거했습니다.
- `AGENT_LOG.md`: 이번 제거 작업을 기록했습니다.

### 구현한 기능
- 페이지에서 `Topic x Venue / 주제별 게재지 분포`가 더 이상 표시되지 않습니다.
- `게재지별 보기` 보드는 유지됩니다.

### 설계 결정
- 게재지 탐색은 별도 venue board로 충분히 제공되므로, 복잡한 matrix UI는 제거해 화면 밀도를 낮췄습니다.

### 남은 작업
- 공개 Pages 배포 후 matrix 섹션이 사라졌는지 확인해야 합니다.

### 주의사항
- matrix 기반 필터 기능도 함께 제거되었습니다. 분야 필터는 왼쪽 패널, 게재지 필터는 venue board와 select로 수행합니다.

## 2026-06-12 10:40

### 변경 요약
- 사용자의 요청에 따라 UI의 큰 분야 체계를 `생산/제조`, `3D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조` 네 축으로 재구성했습니다.

### 수정/생성한 파일
- `index.html`: 카테고리 라벨을 분야 라벨로 변경하고, 결과 그룹 설명을 `Papers by Field`로 수정했습니다.
- `assets/app.js`: `FIELD_ORDER`와 `deriveField` 함수를 추가해 논문을 네 큰 분야로 자동 분류하도록 변경했습니다. 왼쪽 분야 선택 패널, 분야 필터, 논문 그룹 제목이 큰 분야 기준으로 동작합니다.
- `AGENT_LOG.md`: 이번 분야 체계 변경 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 floating 패널은 네 큰 분야 기준으로 논문 수를 보여줍니다.
- 분야 필터도 네 큰 분야 기준으로 동작합니다.
- 논문 목록 그룹도 네 큰 분야 기준으로 묶입니다.
- 기존 세부 카테고리와 태그는 카드 내부 보조 badge로 유지됩니다.

### 설계 결정
- 기존 세부 카테고리 데이터를 삭제하지 않고 UI에서만 큰 분야를 파생했습니다. 자동 요약/분류 데이터는 그대로 보존하면서 탐색 UX만 단순화하기 위해서입니다.
- 큰 분야 분류는 제목, venue, tag, 기존 category를 이용한 휴리스틱으로 계산합니다. AI와 로봇틱스는 3D 프린팅보다 우선 분류합니다.

### 남은 작업
- 사람이 보기에 어색하게 분류된 논문이 있으면 `deriveField` 규칙을 더 조정할 수 있습니다.

### 주의사항
- 현재 로컬 계산 기준 분포는 3D 프린팅 25편, 생산/제조 16편, AI 생산제조 6편, 로봇틱스(생산제조) 3편입니다.

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
## 2026-06-12 13:00

### 변경 요약
- 사용자 요청에 따라 왼쪽 패널을 큰 분야와 서브 토픽 구조로 개편했습니다.
- 논문 총량 100편 제한을 제거하고, OpenAlex/Crossref 공식 API 페이징으로 수집 범위를 확장했습니다.
- 실제 네트워크 수집을 실행해 `data/papers.json`을 50편에서 145편으로 늘렸습니다.
- UI 한글 문자열 일부가 깨져 있던 문제를 `index.html`과 `assets/app.js`에서 복구했습니다.
- API rate limit을 고려해 GitHub Actions의 1회 실행 페이지 예산과 sleep 값을 명시했습니다.

### 수정/생성한 파일
- `index.html`: 깨진 한글 문구를 복구하고 왼쪽 패널 제목을 `분야 및 서브 토픽`으로 변경했습니다.
- `assets/app.js`: `생산/제조`, `3D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조` 분야 분류와 서브 토픽 필터를 구현했습니다.
- `assets/style.css`: 분야/서브 토픽 사이드바와 서브 토픽 badge 스타일을 추가했습니다.
- `scripts/fetch_openalex.py`: OpenAlex cursor pagination과 DOI `/pdf` suffix 정리를 추가했습니다.
- `scripts/fetch_crossref.py`: Crossref cursor pagination과 DOI suffix 정리를 추가했습니다.
- `scripts/update_papers.py`: 논문 총량 제한 제거 상태를 유지하고 페이지당 수집량을 200으로 확장했습니다.
- `.github/workflows/update-papers.yml`: `API_SLEEP_SECONDS`, `OPENALEX_MAX_PAGES`, `CROSSREF_MAX_PAGES`를 추가해 Actions timeout/rate limit 위험을 낮췄습니다.
- `data/papers.json`: 공식 메타데이터 API로 수집한 논문을 145편까지 확장하고, `/pdf`가 붙은 DOI 중복 1건을 정리했습니다.
- `README.md`: 최신 수집 정책 업데이트를 문서화했습니다.
- `ARCHITECTURE.md`: API 페이징과 실행 예산 정책을 문서화했습니다.
- `PROJECT_STATUS.md`: 현재 총 논문 수, 완료 기능, 알려진 rate limit 이슈를 기록했습니다.
- `AGENT_LOG.md`: 이번 작업 기록을 추가했습니다.

### 구현한 기능
- 왼쪽 사이드바에서 큰 분야를 선택하면 해당 분야 논문만 표시됩니다.
- 큰 분야 아래 서브 토픽을 선택하면 분야와 서브 토픽 조건이 함께 적용됩니다.
- 태그 필터에서도 서브 토픽을 선택할 수 있습니다.
- 논문 카드에는 기존 카테고리/태그와 함께 계산된 서브 토픽 badge가 표시됩니다.
- OpenAlex/Crossref 검색은 한 페이지만 가져오지 않고 공식 API pagination을 사용할 수 있습니다.

### 설계 결정
- `data/papers.json`의 전체 논문 수에는 상한을 두지 않았습니다.
- 다만 GitHub Actions는 1시간마다 실행되고 timeout/rate limit이 있으므로 실행 1회당 page budget을 둡니다. 이는 전체 수집량 제한이 아니라 운영 안정성을 위한 장치입니다.
- 출판사 사이트를 직접 크롤링하지 않고, PDF도 저장하지 않으며, raw abstract는 저장/표시하지 않는 기존 정책을 유지했습니다.
- 큰 분야는 기존 저장 카테고리를 삭제하지 않고 UI 계산값으로 도출합니다. 기존 세부 카테고리는 카드 badge로 보존합니다.
- DOI가 `/pdf`로 끝나는 경우 링크 품질을 위해 suffix를 제거합니다. PDF를 다운로드하거나 저장한 것은 아닙니다.

### 남은 작업
- 더 깊은 전체 수집을 원하면 `OPENALEX_MAX_PAGES`와 `CROSSREF_MAX_PAGES`를 높이고 `API_SLEEP_SECONDS`도 함께 늘려 수동 실행하세요.
- OpenAlex 429가 반복되면 target venue 검색을 여러 workflow job 또는 날짜 구간으로 나누는 개선이 필요합니다.
- 일부 느슨한 검색어는 주변 제조/3D 프린팅 논문까지 포함할 수 있으므로 relevance rule을 연구실 기준에 맞게 더 조정할 수 있습니다.

### 주의사항
- API key, secret, token은 로그나 클라이언트 코드에 기록하지 않았습니다.
- 이번 네트워크 수집 중 OpenAlex 429 rate limit이 일부 발생했지만 workflow가 실패하지 않도록 fetch 실패는 로그만 남기고 계속 진행하는 구조입니다.
- raw abstract가 표시되지 않는 이유는 출판사 초록 원문 재게시 위험을 피하기 위해서입니다.
- PDF를 저장하지 않는 이유는 저작권 파일 호스팅 위험을 피하고 DOI/source 링크를 통해 원문 확인을 유도하기 위해서입니다.
- 로컬 브라우저 자동화 도구는 이번 세션에서 노출되지 않아 HTTP 200 응답, JS 파서, Python py_compile, 데이터 정책 검증으로 대체했습니다.
## 2026-06-12 13:11

### 변경 요약
- 상단 통계의 `분야 수` 표시를 `서브토픽 수`로 변경했습니다.
- 표시 숫자도 큰 분야 4개가 아니라 현재 논문들에서 계산되는 고유 서브 토픽 개수를 세도록 변경했습니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `서브토픽 수`로 변경했습니다.
- `assets/app.js`: `updateStats()`에서 `deriveSubtopics()` 결과의 고유 개수를 계산하도록 변경했습니다.
- `AGENT_LOG.md`: 이번 변경 기록을 추가했습니다.

### 구현한 기능
- 상단 통계 카드가 실제 서브 토픽 규모를 보여줍니다.

### 설계 결정
- 기존 DOM id `stat-categories`는 HTML/JS 변경 범위를 줄이기 위해 유지했습니다. 사용자에게 보이는 라벨과 값은 서브토픽 기준입니다.

### 남은 작업
- 없음.

### 주의사항
- JS 문법 검증은 `esprima`로 통과했습니다.
## 2026-06-12 13:16

### 변경 요약
- 상단 통계가 `서브토픽 수`만 표시하던 방식을 `분야 / 서브토픽` 구조로 바로잡았습니다.
- 사용자가 의도한 4개 큰 분야 안의 여러 토픽 구조가 보이도록 숫자를 `분야 개수 / 서브토픽 개수` 형식으로 표시합니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `분야 / 서브토픽`으로 변경했습니다.
- `assets/app.js`: `updateStats()`에서 큰 분야 개수와 서브토픽 개수를 함께 계산해 표시하도록 변경했습니다.
- `AGENT_LOG.md`: 이번 정정 사항을 기록했습니다.

### 구현한 기능
- 상단 통계 카드가 예를 들어 `4 / 18`처럼 큰 분야와 하위 토픽 규모를 함께 보여줍니다.

### 설계 결정
- 왼쪽 패널의 계층 구조와 상단 통계의 표현을 맞추기 위해 단일 서브토픽 수보다 `분야 / 서브토픽` 조합 표현을 선택했습니다.

### 남은 작업
- 없음.

### 주의사항
- 기존 DOM id `stat-categories`는 변경하지 않았습니다. 기능상 의미는 이제 `분야 / 서브토픽`입니다.
## 2026-06-12 13:18

### 변경 요약
- 상단 우선 게재지 pill에서 수집 논문이 0편인 venue를 숨기도록 개선했습니다.
- `게재지별 보기` 섹션을 `게재지 필터`로 정리하고, 큰 카드 영역과 compact 기타 게재지 리스트로 나누었습니다.
- venue dropdown에서도 실제 수집된 게재지만 표시되도록 정리했습니다.

### 수정/생성한 파일
- `assets/app.js`: `buildVenueNav()`가 0편 venue를 건너뛰도록 수정하고, `renderVenueBoard()`를 주요 게재지와 기타 게재지 compact 리스트 구조로 변경했습니다.
- `assets/style.css`: venue pill count badge, 주요 venue card, 기타 venue chip/list 스타일을 추가했습니다.
- `index.html`: 섹션 제목과 설명 문구를 더 명확하게 수정했습니다.
- `AGENT_LOG.md`: 이번 UI 개선 기록을 추가했습니다.

### 구현한 기능
- 상단에는 `All venues`와 실제 논문이 있는 우선 게재지만 표시됩니다.
- 아래 게재지 필터는 `All venues`, 주요 게재지, 기타 게재지 상위 항목으로 나뉘어 덜 난잡하게 보입니다.
- 기타 게재지 chip도 클릭하면 기존 카드와 동일하게 논문 목록을 필터링합니다.

### 설계 결정
- 0편 venue를 보여주면 사용자가 “왜 없지?”라는 노이즈를 먼저 보게 되므로 기본 UI에서는 숨겼습니다.
- 전체 venue를 완전히 숨기지 않고, 실제 수집된 기타 게재지는 compact list로 남겨 탐색 가능성을 유지했습니다.

### 남은 작업
- 필요하면 기타 게재지 리스트에 `더 보기/접기` 인터랙션을 추가할 수 있습니다.

### 주의사항
- `Additive manufacturing`처럼 대소문자가 다른 venue명은 기존 normalize 기반 매칭으로 우선 게재지에 포함됩니다.
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 13:21

### 변경 요약
- 상단 통계의 두 번째 카드가 다시 `서브토픽 수`만 표시하도록 수정했습니다.
- 게재지 영역에서 기타 게재지 긴 목록을 완전히 제거하고, 주요 게재지 카드만 남겼습니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `서브토픽 수`로 변경하고, venue 섹션 제목/설명을 `주요 게재지` 중심으로 수정했습니다.
- `assets/app.js`: venue board에서 기타 게재지 목록 생성 로직과 `venueChip()` 함수를 제거했습니다.
- `assets/style.css`: 기타 게재지 compact list/chip 스타일을 제거했습니다.
- `AGENT_LOG.md`: 이번 정정 사항을 기록했습니다.

### 구현한 기능
- 통계 숫자는 고유 서브토픽 개수만 보여줍니다.
- 게재지 보드에는 `All venues`와 실제 논문이 있는 주요 게재지 카드만 표시됩니다.
- 기타 전체 게재지는 별도 긴 리스트로 펼치지 않고, 상단 필터 드롭다운을 통해 선택하도록 정리했습니다.

### 설계 결정
- 사용자가 화면에서 긴 venue 목록을 읽어야 하는 부담을 줄이기 위해 기타 게재지 preview를 제거했습니다.
- 주요 게재지 탐색과 전체 venue 탐색을 분리했습니다. 빠른 탐색은 카드, 세부 탐색은 드롭다운이 담당합니다.

### 남은 작업
- 필요하면 venue 드롭다운에도 검색형 combobox를 붙일 수 있습니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
- 한글 문구는 UTF-8 기준으로 정상 포함되어 있음을 확인했습니다.
## 2026-06-12 13:26

### 변경 요약
- 게재지 보드를 너무 줄였던 문제를 보완해 기준 기반 표시 방식으로 변경했습니다.
- 핵심 타깃 venue와 데이터에서 2편 이상 반복 등장한 관련 학술지를 함께 표시하도록 했습니다.
- preprint/repository/unknown 계열 venue는 보드에서는 제외하고, 전체 드롭다운에서만 선택 가능하게 유지했습니다.

### 수정/생성한 파일
- `index.html`: 게재지 표시 기준 설명을 추가했습니다.
- `assets/app.js`: `shouldShowDiscoveredVenue()`와 `isNonJournalVenue()`를 추가해 venue 보드 표시 기준을 구현했습니다.
- `assets/style.css`: venue 표시 기준 안내 문구 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 기준 변경을 기록했습니다.

### 구현한 기능
- 보드에 `All venues`, 핵심 타깃 venue, 관련성이 높은 반복 등장 학술지가 표시됩니다.
- 현재 데이터 기준 보드에는 Additive Manufacturing, Nature Communications, Science와 Polymers, IJAMT, Machines, Rapid Prototyping Journal 등 관련 venue가 함께 표시됩니다.

### 설계 결정
- 기준은 `핵심 타깃 venue` 또는 `2편 이상 반복 등장 + 제조/소재/기계/로봇/프린팅 관련 venue명`으로 잡았습니다.
- `Venue unknown`, `arXiv`, `Research Square`, `ChemRxiv`, repository, dissertation, proceedings 계열은 학술지 보드 노이즈를 줄이기 위해 제외했습니다.
- 제외된 venue도 데이터에서 삭제하지 않고 드롭다운 필터로 접근 가능하게 유지했습니다.

### 남은 작업
- venue 품질 기준을 더 엄밀하게 하려면 ISSN 기반 source type 또는 OpenAlex source metadata를 저장하는 개선이 필요합니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
- 현재 기준은 데이터 기반 휴리스틱이며, 학술지 등급 평가를 의미하지 않습니다.
## 2026-06-12 13:29

### 변경 요약
- 게재지 보드 기준을 사용자 요청에 맞춰 `2편 이상 개별 표시 + 그 외 묶음`으로 변경했습니다.
- 2편 미만이거나 학술지로 보기 어려운 출처는 개별 카드로 펼치지 않고 `그 외` 카드에 묶었습니다.

### 수정/생성한 파일
- `index.html`: 게재지 기준 설명을 `2편 이상 개별 표시, 나머지 그 외 묶음`으로 수정했습니다.
- `assets/app.js`: venue board 표시 기준을 count 기반으로 바꾸고 `그 외` 그룹 필터를 추가했습니다.
- `assets/style.css`: `그 외` venue 카드가 일반 카드와 구분되도록 muted/dashed 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- 2편 이상 수집된 학술지는 개별 카드로 표시됩니다.
- 나머지는 `그 외` 카드 하나로 묶이며, 카드에는 `2편 이하의 학술지` badge가 표시됩니다.
- `그 외` 카드를 누르면 해당 묶음에 포함된 논문만 필터링됩니다.
- 위쪽 venue quick pill도 2편 이상 기준으로 맞췄습니다.

### 설계 결정
- `Venue unknown`, `arXiv`, `Research Square`, repository 계열은 논문 수가 2편 이상이어도 학술지 카드로는 표시하지 않고 그 외로 묶습니다.
- 전체 venue 접근성은 드롭다운 필터에 남겨두었습니다.

### 남은 작업
- 더 엄밀한 학술지 판별이 필요하면 OpenAlex source type/ISSN metadata를 저장하는 방식으로 개선할 수 있습니다.

### 주의사항
- 현재 데이터 기준 개별 표시 venue는 11개이고, 그 외 그룹은 64개 venue/77편 논문입니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:34

### 변경 요약
- 게재지 보드에 `Others` 카드를 같은 카드 그룹 안에 표시하도록 정리했습니다.
- 핵심 게재지는 1편이어도 개별 표시하고, 2편 이상 수집된 일반 학술지도 개별 표시하며, 나머지는 `Others`로 묶습니다.

### 수정/생성한 파일
- `assets/app.js`: venue board를 `핵심 게재지 + 2편 이상 학술지 + Others` 순서로 렌더링하도록 수정했습니다.
- `index.html`: venue 기준 설명 문구를 새 구조에 맞게 수정했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- `Others` 카드가 `All venues`, `Nat. Commun.`, `Science`, `Additive Manufacturing` 등과 같은 영역에 표시됩니다.
- `Others` 카드에는 `2편 이하의 학술지` badge가 표시됩니다.
- `Others`를 클릭하면 묶인 venue의 논문만 필터링됩니다.

### 설계 결정
- Nature/Science/Additive Manufacturing 계열 같은 핵심 타깃 venue는 1편이어도 개별 표시합니다.
- 일반 venue는 2편 이상일 때 개별 표시하고, 나머지는 Others로 묶어 화면 밀도를 낮춥니다.

### 남은 작업
- 없음.

### 주의사항
- 현재 데이터 기준 Others에는 63개 venue, 76편 논문이 묶입니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:37

### 변경 요약
- `3D 프린팅` 분야의 서브토픽에 `DLP`를 추가했습니다.
- 큰 분야에 `4D 프린팅`을 새로 추가했습니다.
- 4D/DLP 관련 키워드 기반 분류 규칙을 추가했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FIELD_ORDER`, `FIELD_SUBTOPICS`, featured topics, `deriveField()`, `deriveSubtopics()`를 수정했습니다.
- `AGENT_LOG.md`: 이번 분류 체계 변경을 기록했습니다.

### 구현한 기능
- `4D printing`, `4D-printed`, `4D print` 계열 논문은 큰 분야 `4D 프린팅`으로 분류됩니다.
- `DLP`, `digital light processing`, `vat photopolymerization`, `stereolithography`, `SLA` 계열 논문은 `DLP` 서브토픽으로 표시됩니다.
- `4D 프린팅`에는 `4D printing`, `Active materials`, `Shape morphing`, `Stimuli-responsive` 서브토픽을 추가했습니다.

### 설계 결정
- 4D 관련 논문은 AI/3D/로봇 키워드보다 먼저 판별해 별도 큰 분야로 빠지게 했습니다.
- DLP는 독립 큰 분야가 아니라 3D 프린팅 내부 공정/방식 서브토픽으로 배치했습니다.

### 남은 작업
- DLP 범위를 더 넓히려면 `projection micro-stereolithography`, `two-photon polymerization` 같은 광중합 세부 키워드를 추가할 수 있습니다.

### 주의사항
- 현재 데이터 기준 4D 관련 논문은 3편, DLP/vat photopolymerization 관련 논문은 2편이 탐지됩니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:58

### 변경 요약
- 자동 갱신 실행 시각을 사이트에서 확인할 수 있도록 `data/site_meta.json` 메타데이터를 추가했습니다.
- GitHub Actions가 새 논문이 없어도 마지막 실행 시각을 커밋할 수 있도록 workflow를 수정했습니다.
- 프론트엔드 상단 통계의 `최신 업데이트`가 마지막 파이프라인 실행 시각을 KST로 표시하도록 변경했습니다.

### 수정/생성한 파일
- `data/site_meta.json`: 마지막 실행 UTC 시각, 날짜, 논문 수, 추가 논문 수, 수집 시작 연도, 데이터 출처를 저장하는 메타 파일을 추가했습니다.
- `scripts/update_papers.py`: 실행 시작 시각을 UTC ISO timestamp로 기록하고 `site_meta.json`을 매번 갱신하도록 수정했습니다.
- `.github/workflows/update-papers.yml`: 자동 커밋 대상에 `data/site_meta.json`을 추가했습니다.
- `assets/app.js`: `site_meta.json`을 fetch하고 `last_run_at_utc`를 KST 표시로 변환해 상단 통계에 보여주도록 수정했습니다.
- `README.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`: 갱신 시각 메타데이터 정책을 문서화했습니다.
- `AGENT_LOG.md`: 이번 변경 기록을 추가했습니다.

### 구현한 기능
- 사이트 상단의 `최신 업데이트`가 논문별 날짜가 아니라 마지막 자동 갱신 실행 시간을 표시합니다.
- 표시 형식은 `YYYY-MM-DD HH:mm KST`입니다.
- 새 논문이 없어도 workflow 실행 시각이 남습니다.

### 설계 결정
- 논문 데이터와 실행 메타데이터를 분리하기 위해 `papers.json`에 전역 필드를 섞지 않고 `site_meta.json`을 별도로 만들었습니다.
- `last_run_at_utc`는 UTC로 저장하고, 브라우저에서 KST로 변환합니다.
- `site_meta.json` 로딩 실패 시 기존 논문 `last_updated` 날짜를 fallback으로 사용합니다.

### 남은 작업
- 필요하면 `papers_added`를 UI에 추가해 마지막 실행에서 몇 편이 추가되었는지도 표시할 수 있습니다.

### 주의사항
- `site_meta.json`은 자동 실행 때마다 바뀌므로 GitHub Actions가 매시간 커밋을 만들 수 있습니다.
- JS 문법 검증과 Python py_compile을 통과했습니다.
## 2026-06-12 14:00

### 변경 요약
- 상단 `최신 업데이트` 카드에서 날짜만 보이던 표시를 날짜와 시간이 함께 보이도록 개선했습니다.
- 날짜와 시간을 한 줄에 밀어 넣지 않고 날짜/시간 두 줄로 렌더링해 카드 안에서 잘리지 않게 했습니다.

### 수정/생성한 파일
- `assets/app.js`: `renderUpdatedStat()`을 추가하고 `formatRunTime()`이 날짜와 시간을 분리해서 반환하도록 수정했습니다.
- `assets/style.css`: `stat-datetime` 스타일을 추가해 날짜와 시간이 안정적으로 표시되도록 했습니다.
- `data/site_meta.json`: 현재 배포 기준 마지막 실행 시각을 갱신했습니다.
- `AGENT_LOG.md`: 이번 표시 개선 기록을 추가했습니다.

### 구현한 기능
- `최신 업데이트` 카드가 `2026-06-12`와 `13:59 KST`처럼 날짜와 시간을 함께 표시합니다.
- `site_meta.json`이 없거나 로딩 실패하면 기존 날짜 fallback을 유지합니다.

### 설계 결정
- 날짜/시간을 두 줄로 나누어 작은 통계 카드에서도 잘리지 않게 했습니다.
- 저장은 UTC, 표시는 KST 원칙을 유지했습니다.

### 남은 작업
- 없음.

### 주의사항
- JS 문법 검증을 통과했습니다.
## 2026-06-12 14:02

### 변경 요약
- 사용자가 최신 업데이트 시간 표시가 아직 보이지 않는다고 알려주어, 정적 asset 캐시 문제를 줄이기 위한 cache-busting query를 추가했습니다.

### 수정/생성한 파일
- `index.html`: `assets/style.css`와 `assets/app.js` 로드 URL에 `v=20260612-1402`를 추가했습니다.
- `AGENT_LOG.md`: 이번 캐시 무효화 변경 기록을 추가했습니다.

### 구현한 기능
- GitHub Pages 또는 브라우저가 이전 JS/CSS를 계속 사용하는 상황을 줄입니다.
- 최신 업데이트 시간 표시 코드가 포함된 새 `app.js`를 더 확실히 불러오게 됩니다.

### 설계 결정
- 빌드 도구가 없는 정적 사이트이므로 파일명 해시 대신 query string 버전을 사용했습니다.

### 남은 작업
- 향후 CSS/JS 변경이 있을 때 버전 query를 함께 갱신하면 캐시 문제를 줄일 수 있습니다.

### 주의사항
- 배포된 `data/site_meta.json`에는 현재 `2026-06-12T04:59:53Z`, 즉 `2026-06-12 13:59 KST`가 들어 있습니다.
## 2026-06-12 14:07

### 변경 요약
- 우측 상단에 다크/라이트 모드 토글과 한글/영문 UI 토글을 추가했습니다.
- 사용자의 선택을 `localStorage`에 저장해 새로고침 후에도 유지되도록 했습니다.
- 정적 UI 라벨과 주요 동적 라벨이 언어 설정에 따라 바뀌도록 했습니다.

### 수정/생성한 파일
- `index.html`: 헤더 우측 상단에 `theme-toggle`, `language-toggle` 버튼을 추가하고 CSS/JS cache-busting 버전을 갱신했습니다.
- `assets/style.css`: 다크 테마 CSS 변수, 토글 버튼 스타일, 주요 패널/카드 다크 모드 보정 스타일을 추가했습니다.
- `assets/app.js`: UI 번역 사전, 테마/언어 상태 관리, `localStorage` 저장, 정적/동적 문구 갱신 로직을 추가했습니다.
- `AGENT_LOG.md`: 이번 기능 추가를 기록했습니다.

### 구현한 기능
- `Dark` 버튼을 누르면 다크 모드와 라이트 모드를 전환합니다.
- `EN`/`KO` 버튼을 누르면 주요 UI 문구가 영문/한글로 전환됩니다.
- 논문 제목, 저자, venue, DOI, AI 요약은 원 데이터 보존을 위해 번역하지 않습니다.
- 토글 상태는 브라우저에 저장됩니다.

### 설계 결정
- 빌드 도구 없는 GitHub Pages 정적 사이트이므로 CSS 변수와 vanilla JavaScript로 구현했습니다.
- 논문 메타데이터 자체를 번역하지 않고, 탐색 UI/라벨 중심으로만 언어 전환합니다.
- 캐시 문제를 줄이기 위해 `style.css`와 `app.js` query version을 `20260612-1412`로 갱신했습니다.

### 남은 작업
- 더 완전한 영문 모드를 원하면 카테고리/서브토픽 명칭 자체도 영문 별칭으로 표시하는 매핑을 추가할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:16

### 변경 요약
- 사용자가 우측/사이드 패널의 분야 및 서브토픽명이 영어 모드에서 바뀌지 않는 문제를 지적해 표시명 번역 매핑을 추가했습니다.
- 영어 모드에서 분야 패널, 그룹 제목, 카테고리/태그 드롭다운, badge가 영어 표시명을 사용하도록 수정했습니다.

### 수정/생성한 파일
- `assets/app.js`: `LABEL_TRANSLATIONS`와 `displayLabel()`을 추가하고 동적 라벨 렌더링 지점에 적용했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1420`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 수정 기록을 추가했습니다.

### 구현한 기능
- 영어 모드에서 `생산/제조`는 `Production/Manufacturing`, `3D 프린팅`은 `3D Printing`, `4D 프린팅`은 `4D Printing` 등으로 표시됩니다.
- 서브토픽과 기존 카테고리 badge도 가능한 범위에서 영어로 표시됩니다.
- 내부 필터 값은 한국어 원키를 유지하므로 기존 필터 로직은 그대로 동작합니다.

### 설계 결정
- 데이터 자체를 수정하지 않고 UI 표시명만 변환했습니다.
- 번역되지 않은 전문 약어와 고유명사는 그대로 유지합니다.

### 남은 작업
- 더 완전한 영문 모드를 원하면 모든 자동 생성 태그에 대한 별칭을 계속 보강할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:25

### 변경 요약
- 전체 UI의 글자 크기, 카드 밀도, 반응형 레이아웃을 재조정했습니다.
- 기존 기능을 유지하면서 더 polished한 academic dashboard 느낌이 나도록 visual refinement CSS layer를 추가했습니다.

### 수정/생성한 파일
- `assets/style.css`: 타이포 스케일, 카드/필터/통계/venue/paper card spacing, hover 효과, 모바일 레이아웃을 조정하는 refinement layer를 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1430`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 최적화 기록을 추가했습니다.

### 구현한 기능
- 헤더 H1과 부제 크기를 줄여 첫 화면 정보 밀도를 개선했습니다.
- 왼쪽 분야 패널 폭을 넓히고 서브토픽 글자 크기와 행간을 정리했습니다.
- 통계 카드, 필터 폼, venue 카드, 논문 카드의 글자 크기와 padding을 통일했습니다.
- 논문 카드 grid 최소 폭을 키워 제목/요약이 덜 답답하게 보이도록 했습니다.
- 모바일에서는 통계가 2열, 필터가 1열로 안정적으로 접히도록 보정했습니다.

### 설계 결정
- 기존 CSS를 대규모로 재작성하지 않고 하단 override layer로 덧씌웠습니다. 기능 리스크를 줄이기 위해서입니다.
- decorative 요소는 과하게 추가하지 않고 배경에 아주 약한 수직 그라데이션과 그림자 계층만 사용했습니다.
- 카드 radius는 기존 지침에 맞춰 8px 이하를 유지했습니다.

### 남은 작업
- 실제 브라우저 스크린샷 기준으로 더 미세한 줄바꿈/높이 조정이 필요할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:35

### 변경 요약
- 다크 모드에서 일부 색 대비가 어색한 문제를 개선했습니다.
- 다크 전용 contrast pass를 추가해 배경, 패널, 버튼, badge, notice, 입력창, 링크 버튼의 색을 일관되게 조정했습니다.

### 수정/생성한 파일
- `assets/style.css`: 다크 모드 색상 변수와 컴포넌트별 대비 보정 스타일을 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1438`로 갱신했습니다.
- `AGENT_LOG.md`: 이번 다크 모드 색상 보정 기록을 추가했습니다.

### 구현한 기능
- 다크 모드에서 notice, badge, card topline, form input, venue/topic pill, link button의 텍스트 대비가 더 안정적으로 보입니다.
- active/hover 상태가 과하게 밝거나 탁하게 보이지 않도록 blue/green/amber 계열을 다크 팔레트에 맞췄습니다.
- placeholder와 muted text 색상을 어두운 배경에서 읽기 쉬운 수준으로 조정했습니다.

### 설계 결정
- 기존 라이트 모드 색상은 건드리지 않고 `:root[data-theme="dark"]` override만 추가했습니다.
- 색상은 pure black이 아니라 deep navy 계열을 사용해 눈부심을 줄였습니다.

### 남은 작업
- 실제 브라우저에서 특정 카드/배지가 여전히 튀면 해당 컴포넌트별로 추가 미세 조정할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:46

### 변경 요약
- 사용자가 상단 시간이 13시에서 멈춰 보인다고 지적해, 현재 시각과 마지막 수집 실행 시각을 분리해서 표시하도록 변경했습니다.
- `현재 / 갱신` 카드가 현재 KST 시각을 1분마다 갱신하고, 작은 글씨로 마지막 수집 실행 시각을 함께 보여줍니다.

### 수정/생성한 파일
- `assets/app.js`: `renderUpdatedStat()`을 현재 시각 기준으로 렌더링하도록 수정하고, 1분마다 `updateStats()`를 다시 호출하는 timer를 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1446`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- 상단 카드가 `현재 날짜`와 `현재 HH:mm KST`를 실시간에 가깝게 표시합니다.
- 같은 줄에 `수집 HH:mm KST`로 마지막 자동 수집 실행 시각을 표시합니다.

### 설계 결정
- `site_meta.json`의 시간은 실시간 시계가 아니라 마지막 수집 실행 시각이므로, UI에서 두 의미를 분리했습니다.
- 초 단위 갱신은 불필요하다고 판단해 1분 단위 갱신으로 구현했습니다.

### 남은 작업
- GitHub Actions의 `Update papers` cron 실행이 최근 기록에 보이지 않아, 필요하면 Actions 설정/스케줄 활성화 여부를 별도로 확인해야 합니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
