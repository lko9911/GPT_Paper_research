# Operations and Copyright Policy

이 문서는 GitHub Pages 논문 업데이트 사이트의 전체 운영 흐름과 공개 데이터 정책을 정리한다. 특히 OpenAlex/Crossref 초록을 AI 요약 입력으로 사용할 때 발생할 수 있는 저작권 리스크를 줄이는 것을 핵심 운영 원칙으로 둔다.

## 1. 서비스 범위

- 이 사이트는 생산제조, 3D/4D printing, additive manufacturing, manufacturing automation, robotics for manufacturing, AI manufacturing 관련 논문을 추적한다.
- 사이트는 논문 원문 저장소가 아니라 메타데이터 기반 큐레이션 페이지다.
- 각 논문 카드는 제목, 저자, 연도, venue, DOI/source 링크, 주제 태그, 관련성 점수, AI/metadata summary를 제공한다.
- 사용자는 상세 내용과 원문 확인을 DOI 또는 공식 source 링크에서 수행해야 한다.

## 2. 데이터 출처

정기 업데이트는 공식 메타데이터 API를 사용한다.

- OpenAlex Works API: 논문 후보 검색, DOI 기반 조회, 일부 abstract 신호 확인
- Crossref Works API: DOI 중심 출판 메타데이터 확인
- Semantic Scholar Graph API: API key가 있을 때 DOI 기반 선택 보강
- OpenAI API: 사용자가 명시적으로 요청한 수동 summary refresh에서만 사용

금지되는 수집 방식:

- 출판사 웹페이지 직접 크롤링
- PDF 다운로드 또는 저장
- publisher abstract 원문 저장 또는 화면 표시
- Sci-Hub, 불법 mirror, 권한이 불명확한 PDF 링크 사용

## 3. 정기 업데이트 흐름

1. GitHub Actions `Update papers` workflow가 정해진 시간 또는 수동 실행으로 시작된다.
2. `scripts/update_papers.py`가 `data/queries.json`, `data/seed_dois.json`, `data/target_venues.json`를 읽는다.
3. OpenAlex와 Crossref에서 후보 논문을 조회한다.
4. DOI가 있으면 DOI 기준, 없으면 normalized title 기준으로 중복을 제거한다.
5. 주제, 연도, 비논문 여부, 관련성 점수 기준으로 curated list와 archive를 나눈다.
6. 새 논문은 metadata/fallback summary를 생성한다. 정기 업데이트에서는 OpenAI API를 호출하지 않는다.
7. 저장 직전에 `_abstract` 같은 transient abstract 필드를 제거한다.
8. `data/papers.json`, `data/archive_papers.json`, `data/site_meta.json`가 바뀌면 자동 커밋하고 GitHub Pages에 배포한다.

## 4. OpenAI 요약 운영 원칙

- 정기 업데이트에서는 `ALLOW_OPENAI_IN_UPDATE=false`를 유지한다.
- OpenAI summary refresh는 `Refresh OpenAI summaries` 수동 workflow에서만 실행한다.
- 사용자가 명시적으로 요청하지 않은 OpenAI 호출은 하지 않는다.
- refresh workflow는 `OPENAI_REFRESH_ENABLED=true`와 확인 문구가 있어야만 동작한다.
- OpenAI refresh는 summary 품질을 개선하기 위한 것이며, raw abstract를 공개 데이터로 저장하기 위한 단계가 아니다.
- `relevance_score`는 curated scoring 정책을 우선하며, summary refresh가 임의로 덮어쓰지 않도록 관리한다.

## 5. Abstract Copyright Safety

이 프로젝트의 안전 기준은 단순히 "초록 원문을 저장하지 않는다"에서 끝나지 않는다. AI summary도 publisher abstract의 close paraphrase가 되지 않도록 관리한다.

### 저장 정책

- API에서 받은 abstract는 `_abstract` transient field로만 사용한다.
- `data/papers.json`과 `data/archive_papers.json`에는 raw abstract를 저장하지 않는다.
- 공개 JSON에는 다음 정책 필드를 유지한다.
  - `abstract_used_for_summary`: abstract가 임시 입력으로 쓰였는지 여부
  - `raw_abstract_displayed`: 항상 `false`
  - `pdf_stored`: 항상 `false`
- 프론트엔드는 abstract 원문을 표시하지 않는다.

### Summary 작성 정책

- AI summary는 새로 작성된 해석/압축문이어야 한다.
- abstract 문장을 그대로 복사하거나 번역하지 않는다.
- abstract의 문장 순서, 표현 순서, 긴 명사구 나열을 따라 쓰지 않는다.
- 특히 `ai_summary_en`은 원문 abstract와 같은 언어라 close paraphrase 위험이 더 크므로 더 보수적으로 작성한다.
- unavoidable term은 허용한다. 예: 논문 제목, 재료명, 공정명, 표준 방법명, 약어.
- 하지만 8단어 이상 연속 구절이 abstract와 반복적으로 겹치는 요약은 재작성 대상으로 본다.

### 점검 기준

정기 또는 수동 점검 시 다음을 확인한다.

- `_abstract`, `abstract`, `raw_abstract`, `abstract_text`, `full_text`, `pdf_path` 같은 원문/원문성 필드가 공개 JSON에 없는지 확인
- 모든 공개 논문에서 `raw_abstract_displayed=false`인지 확인
- 모든 공개 논문에서 `pdf_stored=false`인지 확인
- URL이 PDF 직접 링크로 저장되지 않았는지 확인
- `ai_summary_en`을 OpenAlex abstract와 샘플 대조해 8~10 word shingle overlap이 과도하지 않은지 확인

## 6. 공개 저장소 정책

- GitHub Pages로 공개되는 데이터는 공개해도 되는 bibliographic metadata와 새로 작성된 summary로 제한한다.
- `data/archive_papers.json`도 GitHub Pages 배포 대상이면 공개 데이터로 취급한다.
- API key, secret, token, raw API 응답 전체, publisher abstract 원문은 저장소에 커밋하지 않는다.
- 데이터 출처와 한계를 README 또는 footer에서 투명하게 알린다.

## 7. UI 표시 정책

- 논문 카드는 DOI/source 확인을 유도한다.
- summary는 원문 대체물이 아니라 빠른 큐레이션 보조 정보로 표시한다.
- footer 또는 policy notice에는 PDF/abstract를 호스팅하지 않는다는 내용을 유지한다.
- AI summary와 metadata summary를 구분해 사용자가 summary 품질과 출처를 이해할 수 있게 한다.

## 8. 운영 체크리스트

새 기능 또는 데이터 업데이트 후 확인한다.

- JSON 파싱이 정상인지 확인
- 공개 JSON에 raw abstract/PDF 관련 값이 남지 않았는지 확인
- 논문 수, archive 수, weekly added 수가 의도대로 표시되는지 확인
- GitHub Pages 배포가 성공했는지 확인
- OpenAI 호출이 필요한 작업이면 사용자의 명시 요청과 비용 범위를 확인
- summary 정책을 바꾸는 경우 `AGENT_LOG.md`에 이유와 위험 완화 방식을 기록

## 9. 향후 개선 후보

- `ai_summary_en` 저장 전 abstract overlap 자동 검사 추가
- 기존 영어 summary 중 overlap이 높은 항목만 선별 재작성
- summary provider별 품질/저작권 위험 점검 리포트 생성
- archive를 GitHub Pages 공개 대상에서 분리할지 검토

