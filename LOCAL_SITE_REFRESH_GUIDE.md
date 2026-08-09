# Local Site Refresh Guide

이 문서는 GitHub Pages 사이트를 로컬 PC에서 갱신할 때 쓰는 명령만 따로 정리한 운영 메모다.

핵심 원칙:

- PowerShell 프롬프트에서 실행한다.
- `ollama run qwen2.5:7b` 안에 명령을 붙여넣지 않는다.
- Ollama는 백그라운드 서버처럼 켜져 있으면 되고, Python 스크립트가 알아서 호출한다.
- 로컬 모드는 OpenAI 토큰 비용 없이 GPU/CPU/RAM/전기만 사용한다.

## 1. 실행 전 확인

현재 위치가 프로젝트 루트인지 확인한다.

```powershell
pwd
```

정상 위치:

```text
C:\Users\user\Desktop\AML_Research\GPT_Paper_research
```

Ollama 설치와 모델을 확인한다.

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" list
```

필요 모델:

- `qwen2.5:7b`: 로컬 AI 요약
- `nomic-embed-text`: 로컬 임베딩

없으면 한 번만 받는다.

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5:7b
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull nomic-embed-text
```

## 2. 일반 논문 사이트 갱신

일반 논문 DB를 새로 수집/갱신할 때 쓴다.

```powershell
& "C:\Users\user\anaconda3\python.exe" scripts\update_papers.py
& "C:\Users\user\anaconda3\python.exe" scripts\build_split_data.py
```

변경사항 확인:

```powershell
git status --short
```

사이트 반영:

```powershell
git add data public assets index.html
git commit -m "Refresh paper site data"
git push
```

## 3. 일반 논문 로컬 AI 요약 갱신

메타데이터 요약 또는 아직 5Q가 아닌 요약을 Ollama로 갱신할 때 쓴다.

작은 테스트:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:MAX_LOCAL_SUMMARIES = "3"
$env:REFRESH_MODE = "metadata"
$env:LOCAL_REQUIRE_ABSTRACT = "false"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue
& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_summaries.py
& "C:\Users\user\anaconda3\python.exe" scripts\build_split_data.py
```

남은 메타데이터 요약을 전부 갱신:

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:MAX_LOCAL_SUMMARIES = "0"
$env:REFRESH_MODE = "metadata"
$env:LOCAL_REQUIRE_ABSTRACT = "false"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue
& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_summaries.py
& "C:\Users\user\anaconda3\python.exe" scripts\build_split_data.py
```

커밋:

```powershell
git add data public
git commit -m "Refresh local AI summaries"
git push
```

## 4. AML 추천 외부/내부 탐색

AML 추천 시스템을 로컬 임베딩으로 갱신한다.

이 명령은 다음을 함께 수행한다.

- Crossref 기반 외부 후보 탐색
- 기존 논문 DB 기반 내부 후보 탐색
- AML seed와 후보 논문의 로컬 임베딩 유사도 계산
- 기존 공개 AML 추천 목록 유지
- 새 추천 항목 추가
- 기존 추천 항목 점수/메타데이터 갱신

공개 사이트에 바로 반영:

```powershell
$env:AML_EMBEDDING_PROVIDER = "local"
$env:LOCAL_EMBEDDING_MODEL = "nomic-embed-text"
$env:AML_ALLOW_LOCAL_PUBLIC_WRITE = "true"

& "C:\Users\user\anaconda3\python.exe" scripts\run_aml_recommendation_pipeline.py --mode collect_and_score --max-candidates 0
$env:OPENALEX_RANK_TARGETS = "aml"
& "C:\Users\user\anaconda3\python.exe" scripts\enrich_openalex_venue_ranks.py
```

커밋:

```powershell
git add public/data/aml_recommended_papers.json data/aml_embeddings data/openalex_source_metrics.json
git commit -m "Refresh AML recommendations"
git push
```

미리보기만 하고 싶으면 아래 줄을 빼고 실행한다.

```powershell
$env:AML_ALLOW_LOCAL_PUBLIC_WRITE = "true"
```

그러면 공개 파일 대신 아래 private preview가 생성된다.

```text
data/private/aml_recommended_papers_local_preview.json
```

## 5. AML 추천 로컬 AI 요약 갱신

AML 추천 파일에 `Metadata summary`가 남았을 때 쓴다.

```powershell
$env:LOCAL_LLM_MODEL = "qwen2.5:7b"
$env:LOCAL_REQUIRE_ABSTRACT = "false"
$env:MAX_LOCAL_AML_SUMMARIES = "0"
Remove-Item Env:DRY_RUN -ErrorAction SilentlyContinue
& "C:\Users\user\anaconda3\python.exe" scripts\refresh_local_aml_summaries.py
```

커밋:

```powershell
git add public/data/aml_recommended_papers.json
git commit -m "Refresh AML local summaries"
git push
```

## 6. 전체 로컬 갱신 순서

전체를 한 번에 정리할 때 추천 순서:

1. 일반 논문 수집 갱신
2. 일반 논문 로컬 AI 요약 갱신
3. AML 추천 외부/내부 탐색
4. AML 추천 로컬 AI 요약 갱신
5. `git status --short` 확인
6. 커밋/푸시

## 7. 검증 명령

일반 논문과 AML 추천의 요약 출처 개수를 확인한다.

```powershell
$env:PYTHONIOENCODING = "utf-8"
@'
import json
from collections import Counter
from pathlib import Path

for path in ["data/papers.json", "public/data/aml_recommended_papers.json"]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print(path, len(data), dict(Counter((item.get("summary_provider") or "metadata") for item in data)))
'@ | & "C:\Users\user\anaconda3\python.exe" -
```

기대 상태:

- 일반 논문: `openai` 또는 `local` 중심, `metadata`는 가능하면 0
- AML 추천: `openai` 또는 `local` 중심, `metadata`는 가능하면 0

## 8. 자주 하는 실수

Ollama 채팅창에 PowerShell 명령을 붙여넣지 않는다.

잘못된 위치:

```text
>>> $env:AML_EMBEDDING_PROVIDER = "local"
```

정상 위치:

```powershell
(base) PS C:\Users\user\Desktop\AML_Research\GPT_Paper_research>
```

Ollama 채팅에서 빠져나오기:

```text
/bye
```

## 9. 비용 기준

로컬 모드:

- OpenAI API 비용 없음
- Ollama 모델과 로컬 임베딩 사용
- GPU/CPU/RAM/전기 사용
- Crossref/OpenAlex 공개 API 호출 사용

OpenAI 모드:

- `OPENAI_API_KEY`를 사용하는 요약/임베딩/AI reason 작업은 API 비용이 발생할 수 있다.
- 비용이 걱정되면 로컬 모드 환경변수를 명시하고 실행한다.

## 10. 공개 데이터 주의

커밋 전에 확인할 것:

- raw abstract 원문이 저장되지 않았는지
- PDF 파일이나 PDF 직접 링크가 들어가지 않았는지
- `data/private` 안의 개인/seed 파일이 `git status`에 잡히지 않는지
- AML 추천 갱신 후 기존 추천 수가 줄지 않고, 기존 + 신규 형태인지

빠른 확인:

```powershell
git status --short
```
