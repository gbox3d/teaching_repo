# 12주차 — AI 서비스화와 배포

## 이번 주 질문

> 모델을 다른 사람이 쓸 수 있는 서비스로 만들 때 무엇이 끊기고 느려지며, 그것을 어떻게 다루는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 모델 서버(Ollama)와 앱 서버(FastAPI)의 책임을 분리해 서비스 구조를 텍스트 도식으로 그린다.
2. pydantic 스키마로 요청을 검증하고, `/health`와 `/chat`이 정상·실패 상황에서 어떤 상태 코드(200·422·502·503·504)를 돌려주는지 재현한다.
3. 스트리밍 응답(SSE)을 앱 서버에서 내보내고 Gradio UI에서 첫 글자까지의 시간, 취소, 오류 상태를 관찰한다.
4. 설정을 환경변수와 `.env.example`로 외부화하고 `.env`·`outputs/`가 Git과 이미지 밖에 있음을 확인한다.
5. uv 공식 이미지 기반 Dockerfile을 읽고 레이어 순서가 빌드 시간에 미치는 영향을 설명하며, 컨테이너에서 호스트의 Ollama에 연결한다.
6. 처음 보는 사람이 따라 할 수 있는 README 재현 절차(Docker 경로·uv 경로)를 작성하고 짝의 검증을 받는다.

## 누적 결과물

이번 주 실습은 **3차 종합과제(12주)** 의 (b) "AI 서비스 베타" 부분을 통째로 채운다. `/health`·`/chat`·`/chat/stream`을 가진 앱 서버, UI 1종, 오류 처리, `.env.example`, 두 경로의 실행 절차가 그 내용이다. 10~11주차의 실험 기록·데이터 카드·평가 결과가 (a)이고, 이번 주 3교시에서 (a)·(b)·(c)를 한 번에 점검한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 모델 서버와 앱 서버 분리, 요청·응답 스키마(pydantic), `/health`, 오류 응답(502·503·504), 타임아웃·동시 요청·로깅 | 앱 서버 세우기와 오류 응답 확인 | `outputs/smoke-*.json`(정상 1건 + 502·503·504 각 1건)과 422가 기록된 `outputs/requests.jsonl`, `GET /models` 추가 commit |
| 2교시 | 스트리밍(SSE)과 사용자 경험, FastAPI `StreamingResponse`, Gradio 최소 채팅 UI, 정적 HTML+fetch 대안과 CORS | 스트리밍 채팅 UI 연결 | `outputs/ui-turns.jsonl`(두 모드 시간 비교 + 오류 턴), 취소·오류 문구 기록 |
| 3교시 | 설정 외부화(`.env`), Dockerfile 기초(uv 공식 이미지, 레이어·캐시), 컨테이너와 호스트 Ollama 연결(`host.docker.internal`), README 재현 절차, **3차 종합과제 안내** | Dockerfile과 재현 절차 검증 | `Dockerfile`·`.dockerignore`, README 실행 절, 짝 검증 기록, 3차 과제 점검표 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, Ollama, PowerShell (1주차 `env_check.md`로 확인한 상태)
- 수업 전에 캐시된 기본 모델 `OLLAMA_MODEL`(교재 검증용 기본값 `qwen3:8b`, 내려받는 크기 약 5.2 GB, GPU 없는 PC는 `qwen3:0.6b` 약 0.5 GB). 실습 시간에 모델을 내려받지 않는다.
- Docker Desktop은 **선택**이다. 없으면 3교시는 uv 경로로 진행한다. Docker 경로를 쓰려면 수업 전에 uv 공식 베이스 이미지를 한 번 내려받아 둔다.
- 수업 전에 예제 `examples/ai_service/`를 복사해 `uv sync`를 한 번 실행해 패키지 캐시를 채워 둔다. `gradio` 의존성이 커서 첫 설치는 수 분이 걸리며, 실습 시간의 `uv sync`는 캐시에서 몇 초 안에 끝나야 한다.
- 10~11주차 산출물(`experiments/run-*.md`, `DATA_CARD.md`, `outputs/eval-*.json`, `FAILURE_ANALYSIS.md`). 어댑터가 없어도 이번 주 서비스는 기본 모델로 동작한다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 전화번호, 비밀번호나 API 토큰은 실습 파일과 공개 저장소에 넣지 않는다. `.env`는 커밋하지 않고 `.env.example`만 커밋한다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): FastAPI 앱 서버 + Ollama 클라이언트 + Gradio UI + Dockerfile + 점검 스크립트
- [따라하기 절차](walkthrough.md): 시연·실습을 `할 일 → 예상 결과 → 확인` 순으로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)
- [3차 종합과제 안내](assignment_brief.md) · [3차 종합과제 루브릭](assignment_rubric.md)

## 권장 진행 방식

1. 코드를 실행하기 전에 "모델 서버가 꺼지면 앱 서버는 무엇을 돌려줄까"를 상태 코드로 예상해 적는다.
2. 정상 경로를 먼저 확인하고, 실패는 서버를 끄는 대신 **환경변수를 바꿔** 재현한다(없는 포트, 없는 모델, 짧은 타임아웃).
3. 캡처 대신 `smoke_test.py`가 만든 JSON과 `requests.jsonl`을 증거로 쓴다.
4. UI에서는 "답이 맞는가"보다 "기다리는 동안 무엇이 보이는가, 끊기면 무엇이 보이는가"를 본다.
5. 3교시에는 자기 PC가 아니라 **짝의 PC(또는 깨끗한 폴더)** 에서 README만 보고 실행되는지를 기준으로 삼는다.

## 완료 기준

- [ ] `uv run uvicorn app.main:app --port 8000`으로 앱 서버가 뜨고 `/docs`가 열린다.
- [ ] `/health`가 `ok`이고 `/chat`이 200과 `eval_count`를 돌려준다.
- [ ] 502·503·504를 각각 한 번씩 재현해 `outputs/smoke-*.json`에 남기고, 422는 `/docs` 응답 본문과 `outputs/requests.jsonl`로 확인해 원인을 한 문장씩 적었다.
- [ ] `GET /models`를 추가했고 모델 서버가 꺼졌을 때 502가 자동으로 나온다.
- [ ] 같은 질문으로 비스트리밍·스트리밍 모드의 첫 글자까지 시간과 전체 시간을 비교했다.
- [ ] Stop·앱 서버 중단·모델 서버 실패 세 상황의 UI 문구를 기록했다.
- [ ] `.env`가 Git에 추적되지 않고 `.env.example`·`.dockerignore`·`Dockerfile`이 있다.
- [ ] Docker 경로 또는 uv 경로로 깨끗한 환경에서 `/health`가 `ok`이며, README 절차를 짝이 따라 해 결과를 남겼다.

## 제출 증거

이번 주는 3차 종합과제 제출 주차다. 아래 증거는 팀 저장소의 과제 산출물에 포함하고, 개인 실습 결과는 개인 저장소에도 누적한다.

1. 개인 실습 폴더의 `outputs/smoke-*.json`(정상 1건, 502·503·504 각 1건)과 422 요청까지 담긴 `outputs/requests.jsonl`
2. `GET /models`를 추가한 commit id
3. `outputs/ui-turns.jsonl`과 두 모드 시간 비교표, 취소·오류 문구 기록
4. `Dockerfile`, `.dockerignore`, `.env.example`, README 실행 절(두 경로), 짝 검증 기록
5. 3차 종합과제 제출: 팀 저장소 URL + 최종 commit id + README 재현 절차([안내서](assignment_brief.md) 참고)

터미널 출력과 JSON에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

13주차 `week13_test_ci_security`에서는 이번 주와 같은 구조(스키마·클라이언트 주입 지점)에 pytest를 붙이고, 가짜 Ollama 클라이언트로 오류 경로를 자동 검사한 뒤 GitHub Actions에서 `uv run pytest`·`ruff`가 초록불이 되게 만든다. 13주차 예제 `ci_lab/`은 이번 주 앱 서버를 줄여 다시 쓴 것이라 요청 필드와 예외→상태 코드 매핑(503·404·502)이 이번 주(502·503·504)와 다르다. 이번 주에 손으로 재현한 실패 경로가 그 테스트의 원본이며, 테스트를 팀 저장소로 옮길 때는 팀 코드가 정한 코드값에 맞춘다.

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Uvicorn 공식 문서](https://www.uvicorn.org/)
- [Gradio ChatInterface 문서](https://www.gradio.app/docs/gradio/chatinterface)
- [uv Docker 가이드](https://docs.astral.sh/uv/guides/integration/docker/)
- [Docker 공식 문서](https://docs.docker.com/)
- [Ollama FAQ — 네트워크 노출과 `OLLAMA_HOST`](https://github.com/ollama/ollama/blob/main/docs/faq.md)
