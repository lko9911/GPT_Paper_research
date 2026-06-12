# PROJECT_STATUS

## 현재 프로젝트 상태 요약

GitHub Pages에서 동작 가능한 정적 논문 큐레이션 사이트와 GitHub Actions 자동 업데이트 파이프라인의 최소 동작 버전이 구현되어 있습니다. 로컬에서 업데이트 스크립트를 1회 실행해 `data/papers.json`에는 현재 9편의 논문 메타데이터가 들어 있습니다.

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
- OpenAI API 선택적 요약 생성
- OpenAI key가 없을 때 fallback 한글 요약 생성
- Semantic Scholar API key가 있을 때 선택적 보강
- GitHub Actions 매시 실행 및 수동 실행
- 변경된 `data/papers.json`만 자동 커밋
- README, 아키텍처 문서, 상태 문서, 작업 로그 생성
- 로컬 HTTP 서버에서 `index.html`과 `data/papers.json` 응답 확인
- 저장 데이터에 `_abstract`가 남지 않고 `raw_abstract_displayed=false`, `pdf_stored=false`가 유지되는지 검증

## 부분 구현된 기능

- 관련성 점수와 분류는 OpenAI가 없을 때 휴리스틱 기반입니다.
- Source 열기 버튼은 현재 DOI URL을 사용합니다. 향후 API별 landing URL을 별도로 저장하면 더 정확해질 수 있습니다.
- API rate limit 배려는 기본 sleep과 User-Agent/mailto 중심입니다. 대규모 검색에는 backoff 전략을 추가할 수 있습니다.

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
