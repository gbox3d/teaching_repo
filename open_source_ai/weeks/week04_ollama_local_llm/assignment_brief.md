# 1차 종합과제 — 협업 저장소와 Ollama 로컬 모델 활용

## 목적

1장(1~4주차)에서 배운 것을 하나의 저장소로 묶는다. 다른 사람이 README만 읽고 깨끗한 PC에서 `uv sync --frozen`으로 환경을 재현하고, 공식 `ollama` 라이브러리로 로컬 모델과 대화하고(기억 포함), 그림을 읽히고, 툴 콜링으로 내 함수를 쓰게 하는 상태가 목표다. 서버나 HTTP 클라이언트를 직접 만들지 않는다. 4주차 예제를 가져다 바꿔 쓰고, 무엇을 바꿨고 무엇을 관찰했는지 설명하는 것이 핵심이다. 이 저장소는 5~7주차 RAG 답변기와 9주차 이후 팀 프로젝트의 출발점이 된다.

## 대상 범위

| 주차 | 저장소에 들어오는 것 |
|---|---|
| 1주차 | 환경 점검표(`env_check.md`), 첫 uv 실행, 개인 저장소 초기화 |
| 2주차 | GitHub 원격, 브랜치·PR·리뷰 근거, `LICENSE`, 라이선스 표(`license_matrix.md`) |
| 3주차 | uv 프로젝트(`pyproject.toml`·`uv.lock`), src 레이아웃, `[project.scripts]` CLI, 설정 로더(`config.py`), `.env.example` |
| 4주차 | `ollama` 라이브러리를 쓰는 대화(기억)·이미지·툴 콜링 기능, `week04_report.md`, `Modelfile`과 기준 모델 비교 |

## 필수 산출물

1. **저장소 문서**: `README.md`(무엇을 하는가, 준비할 것(`ollama pull qwen3.5:2b`), 설치, 실행 예시 3개(대화·이미지·툴 콜링), 재현 절차, 제한 사항, 라이선스), `LICENSE`(MIT 또는 Apache-2.0, 선택 이유 한 문장은 README에), `.env.example`, `.gitignore`(`.venv/`·`.env` 포함).
2. **uv 프로젝트**: `pyproject.toml`(의존성 하한만), `uv.lock` 커밋, src 레이아웃, `[project.scripts]`로 등록된 CLI 이름 하나. 깨끗한 폴더에서 `git clone` → `uv sync --frozen` → 실행이 성공해야 한다.
3. **Ollama 활용 기능** — 4주차 예제를 3주차 CLI의 서브커맨드로 옮긴다. 모델 호출은 `ollama.chat()`을 쓴다.
   - `chat`: 시스템 프롬프트가 있고 대화를 기억하는 채팅(`ex05_memory.py` 바탕). 시스템 프롬프트는 내가 정한 역할로 바꾼다.
   - `see <이미지 경로>`: 그림을 보내고 질문하는 기능(`ex06_vision.py` 바탕).
   - `tool`: 툴 콜링(`ex07_tools.py` 바탕). 예제 함수 외에 **직접 만든 함수를 1개 이상** 넣는다.
   - 모델 이름은 3주차 설정(`OLLAMA_MODEL`)에서 읽는다. 기본값은 `qwen3.5:2b`.
   - 예: `uv run oss-tool chat`, `uv run oss-tool see screen.png`, `uv run oss-tool tool`
4. **`week04_report.md`**: 4주차 실습 보고서 1~3절(모델 숫자표, system·temperature·기억 비교, 이미지 결과, 툴 콜링 세 단계 설명과 내 함수의 호출 기록, 내 모델 비교). 각 관찰에 **왜 그렇게 되는지 내 말로 한 문장**을 붙인다.
5. **`Modelfile`**: 팀명이 들어간 SYSTEM과, 같은 질문에 대한 기준 모델(`qwen3.5:2b`)과 내 모델의 답 비교(`week04_report.md` 3절).
6. **`evidence/`**: `chat`·`see`·`tool` 실행 화면을 복사한 텍스트 파일 각 1개(`chat.txt`, `see.txt`, `tool.txt`). `tool.txt`에는 내 함수가 불린 `[함수 실행]` 줄이 있어야 한다.
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
- [ ] `chat`·`see`·`tool` 서브커맨드가 모두 있고 `--help`가 사용법을 설명한다.
- [ ] `chat`에서 앞서 말한 내용을 다음 질문에서 기억한다.
- [ ] `tool`에 내가 만든 함수가 있고 `evidence/tool.txt`에 그 함수가 불린 줄이 있다.
- [ ] `week04_report.md` 1~3절이 채워져 있고 관찰마다 이유가 한 문장씩 있다.
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
- 측정값·비교 결과를 실제 실행 없이 적는 것. `evidence/`의 실행 화면과 보고서 내용이 맞아야 한다.
- 실습 시간에 `ollama pull`로 새 모델을 내려받는 것. 모델 준비는 수업 전 환경 기준표대로 한다.

## 배점과 마감

배점과 마감은 학교 운영 문서가 정한다. 채점 기준의 상대 배점은 [1차 종합과제 루브릭](assignment_rubric.md)에 있다.
