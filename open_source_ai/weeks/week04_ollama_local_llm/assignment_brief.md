# 1차 종합과제 — 협업 저장소와 Ollama 로컬 API 클라이언트

## 목적

1장(1~4주차)에서 배운 것을 하나의 저장소로 묶는다. 다른 사람이 README만 읽고 깨끗한 PC에서 `uv sync --frozen`으로 환경을 재현하고, 로컬 Ollama 서버에 `chat`·`stream` 서브커맨드로 대화하며, 서버가 꺼져 있거나 모델 이름이 틀렸을 때 사람이 읽을 메시지를 보는 상태가 목표다. 이 저장소는 5~7주차 RAG 답변기와 9주차 이후 팀 프로젝트의 출발점이 된다.

## 대상 범위

| 주차 | 저장소에 들어오는 것 |
|---|---|
| 1주차 | 환경 점검표(`env_check.md`), 첫 uv 실행, 개인 저장소 초기화 |
| 2주차 | GitHub 원격, 브랜치·PR·리뷰 근거, `LICENSE`, 라이선스 표(`license_matrix.md`) |
| 3주차 | uv 프로젝트(`pyproject.toml`·`uv.lock`), src 레이아웃, `[project.scripts]` CLI, 설정 로더(`config.py`), `.env.example` |
| 4주차 | Ollama 클라이언트(`chat`·`stream`), 오류 처리, `outputs/` 기록, `model_report.md`, `Modelfile`과 전후 비교 |

## 필수 산출물

1. **저장소 문서**: `README.md`(무엇을 하는가, 준비할 것(모델 이름은 환경변수), 설치, 실행 예시 2개 이상, 재현 절차, 제한 사항, 라이선스), `LICENSE`(MIT 또는 Apache-2.0, 선택 이유 한 문장은 README에), `.env.example`, `.gitignore`(`.venv/`·`.env`·`outputs/` 포함).
2. **uv 프로젝트**: `pyproject.toml`(의존성 하한만), `uv.lock` 커밋, src 레이아웃, `[project.scripts]`로 등록된 CLI 이름 하나. 깨끗한 폴더에서 `git clone` → `uv sync --frozen` → 실행이 성공해야 한다.
3. **Ollama 클라이언트 CLI**:
   - `chat` 서브커맨드(비스트리밍)와 `stream` 서브커맨드(스트리밍) — 예: `uv run oss-tool chat --prompt "…"`, `uv run oss-tool stream --prompt "…"`
   - 옵션: `--model`, `--host`, `--system`, `--temperature`, `--num-predict`, `--seed` (이름은 달라도 되나 README에 표로 적는다)
   - 설정 우선순위: 기본값 < `.env`·환경변수(`OLLAMA_HOST`·`OLLAMA_MODEL`) < 명령행 인자
   - 요청 JSON에 `stream`, `think`(기본 `false`, 이유 주석), `options` 명시
   - 오류 처리: 연결 실패·모델 없음(HTTP 404)·시간 초과를 스택 트레이스 없이 한 문장 메시지와 0이 아닌 종료 코드로 처리
   - `outputs/`에 요청·응답·메타(`eval_count`, `eval_duration`, tokens/s, `done_reason`)를 JSON으로 기록
4. **`model_report.md`**: 모델 2개(기본·소형)의 파라미터 수, 양자화, 컨텍스트 길이, 파일 크기, 메모리 크기, PROCESSOR, tokens/s와 같은 질문 3개에 대한 답 차이, 계산과 실측 대조, 결론.
5. **`Modelfile`과 전후 비교표**: 시스템 프롬프트가 들어간 커스텀 모델 정의와, 기준 모델·커스텀 v1·SYSTEM 한 줄 변경 v2의 답을 같은 질문 3개로 비교한 표(`model_report.md` 5절).
6. **`evidence/`**: `outputs/`에서 고른 JSON 2~3개(정상 호출 1, 스트리밍 1, temperature 비교 1), 실패 메시지 원문과 종료 코드를 적은 `failures.md`, temperature·seed 비교 문단 `temperature_compare.md`.
7. **협업 근거**: Issue 2개 이상(하나는 4주차 기능 제안), PR 2개 이상(하나는 4주차 기능이며 리뷰를 받은 뒤 merge), 본인이 남긴 리뷰 코멘트 1개 이상. URL을 README 또는 `CONTRIBUTING.md` 끝의 표에 적는다.

## 제출 형식

- 저장소 URL(GitHub, 공개 또는 강의자에게 접근 권한 부여)
- 최종 commit id: `git rev-parse HEAD` 출력 40자
- README의 "재현 절차" 절: `git clone` → `uv sync --frozen` → 모델 준비(환경변수로 이름 지정, 다운로드 명령은 README에만) → 실행 명령 → 예상 출력 한 줄. 채점자는 이 절만 보고 실행한다.
- 팀으로 제출하는 경우 README에 팀원별 기여 표를 둔다(아래 "개인 기여 증거").

## 개인 기여 증거

팀이어도 개인별로 다음을 남긴다. 표시 이름은 GitHub 계정이며 실명·학번은 적지 않는다.

| 항목 | 최소 | 근거 |
|---|---|---|
| commit | 5개 이상, 의도가 드러나는 메시지 | `git log --author=<계정> --oneline` |
| Issue | 1개 이상 작성 | Issue URL |
| PR | 1개 이상 작성·merge | PR URL |
| Review | 다른 사람 PR에 코멘트 1개 이상 | 코멘트 URL |

## 제출 전 검사

- [ ] 새 폴더에 `git clone`하고 `uv sync --frozen`이 오류 없이 끝난다.
- [ ] README의 실행 명령을 그대로 복사해 실행하면 답이 나온다.
- [ ] `chat`과 `stream` 서브커맨드가 모두 있고 `--help`가 옵션을 설명한다.
- [ ] `OLLAMA_HOST`를 틀린 포트로 바꾸면 한 문장 메시지와 0이 아닌 종료 코드가 나온다.
- [ ] `--model no-such-model`이 404를 사람이 읽을 문장으로 바꾼다.
- [ ] 요청 JSON에 `stream`·`think`·`options`가 명시되어 있고 `think:false`의 이유 주석이 있다.
- [ ] `outputs/`는 `.gitignore`에 있고 `evidence/`에 JSON 2~3개가 있다.
- [ ] `model_report.md`에 모델 2개의 표와 답 비교, 5절 전후 비교표가 채워져 있다.
- [ ] `Modelfile`의 `FROM`이 README에 적은 모델 이름과 같다.
- [ ] `LICENSE` 파일이 있고 README에 라이선스 이름과 선택 이유가 있다.
- [ ] `.env`, 토큰, 비밀번호, 실명, 학번, 사용자 홈 경로가 저장소 어디에도 없다(`git log -p`로 이력까지 확인).
- [ ] Issue·PR·Review URL이 README 또는 `CONTRIBUTING.md`에 있고 모두 열린다.
- [ ] 최종 commit id가 제출한 값과 같다.

## 금지 사항

- `.env`, 실제 토큰·비밀번호, 실명·학번·전화번호 등 개인정보를 저장소에 넣는 것. 이력에 한 번이라도 들어갔으면 제거 절차와 토큰 회전 사실을 README에 적는다.
- 모델 가중치 파일(blob·GGUF)을 저장소에 커밋하는 것. 모델은 이름과 준비 명령만 적는다.
- 재현 불가능한 캡처만 제출하는 것. 모든 결과는 명령과 commit으로 재현되어야 한다.
- 출처와 라이선스 없이 다른 저장소의 코드를 붙여 넣는 것. 가져온 코드는 출처 URL과 라이선스를 파일 머리와 README에 적는다.
- 측정값·비교 결과를 실제 실행 없이 적는 것. `evidence/`의 JSON과 보고서 숫자가 맞아야 한다.
- 실습 시간에 `ollama pull`로 새 모델을 내려받는 것. 모델 준비는 수업 전 환경 기준표대로 한다.

## 배점과 마감

배점과 마감은 학교 운영 문서가 정한다. 채점 기준의 상대 배점은 [1차 종합과제 루브릭](assignment_rubric.md)에 있다.
