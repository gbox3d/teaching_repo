# 프로젝트 이름

<!--
이 양식의 절 제목에는 release_check.py 가 찾는 단서(소개·왜·설치·실행·예시·제한·라이선스·출처)가 들어 있다.
제목을 바꿔도 단서 단어는 남긴다. 괄호 안 예시는 팀 프로젝트 내용으로 바꾼다.
-->

한 줄 설명: 누구를 위해 무엇을 하는 도구인가. (예: 수업 자료를 근거로 출처를 밝히며 답하는 로컬 AI 도우미)

## 소개 — 무엇을 하는가

- 입력: (예: 한국어 질문 한 줄)
- 출력: (예: 답과 출처 파일명·chunk 번호)
- 동작 한 줄: (예: Ollama 로컬 모델 + 문서 검색(RAG) + FastAPI 서비스)

## 왜 만들었는가

- 사용자와 상황: (예: 수업 자료가 여러 파일에 흩어져 있어 찾기 어려운 학생)
- 기존 해법의 한계: (예: 클라우드 API는 비용·개인정보, 검색은 출처만 주고 답을 주지 않음)
- 이 프로젝트가 다르게 하는 것: (예: 오프라인·출처 표시·재현 가능한 uv 프로젝트)

## 설치

```powershell
git clone REPO_URL
Set-Location REPO_NAME
git checkout v0.1.0
uv sync --frozen
Copy-Item .env.example .env
```

- 필요한 것: Git, uv, Ollama(모델 `OLLAMA_MODEL` 사전 캐시). 정확한 버전은 학기별 환경 기준표를 따른다.
- GPU 없는 PC: `.env`에서 `OLLAMA_MODEL`을 소형 모델로 바꾼다. (예: `qwen3:0.6b`)

## 실행

```powershell
uv run python -m PACKAGE_NAME --help
uv run uvicorn app.main:app --reload
```

`.env`에서 바꿀 수 있는 값: `OLLAMA_HOST`, `OLLAMA_MODEL`, (팀 프로젝트 항목 추가)

## 예시

```text
입력: "uv sync --frozen 은 무엇을 보장하는가?"
출력: "uv.lock 에 적힌 버전 그대로 설치한다 ... [출처: docs/uv_basics.md#3]"
```

## 제한

- (예: 한국어·영어 질문만 검증했다.)
- (예: 12 GB VRAM 기준으로 측정했으며 CPU 에서는 응답에 수십 초가 걸린다.)
- (예: 학습 데이터가 CC-BY-NC 라 어댑터는 비상업 용도로만 쓴다.)

## 라이선스

- 코드: (예: MIT, `LICENSE` 파일)
- 모델·데이터·어댑터: `SOURCES.md`와 `MODEL_CARD.md`의 라이선스 표를 따른다. 가장 제한적인 조건이 전체에 적용된다.

## 출처

- 모델·데이터·코드 조각의 이름·버전·라이선스·URL: `SOURCES.md`
- 변경 이력: `CHANGELOG.md` · 인용: `CITATION.cff`

## AI 도구 사용 내역

| 파일·범위 | AI 도구가 만든 것 | 사람이 검증·수정한 것 |
|---|---|---|
| (예: `app/main.py` 초안) | (예: 라우터 골격) | (예: 오류 응답 코드·타임아웃 수정, 테스트 3개 작성·실행) |
| (예: README 초안) | (예: 절 구조) | (예: 설치·실행 명령을 새 폴더에서 재실행해 확인) |

## 기여

버그·제안은 Issue 로, 변경은 PR 로 받는다. 방법은 `CONTRIBUTING.md`를 따른다. Issue 에는 환경·명령·출력 세 가지를 적는다.
