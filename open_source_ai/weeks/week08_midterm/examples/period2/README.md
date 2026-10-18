# 8주차 2교시 — 모의 실기 B Git 상황 판단과 Ollama 툴 콜링

공개 모의 실기 B의 **문항**이다. 별도 시작 코드는 없다. B-2 실기는 모의 A에서 만든 `week8-hello`를 GitHub에 올리고, B-4 실기는 4주차 3교시 `period3` 프로젝트(`ex07` 툴 콜링)를 그대로 쓴다. 정답은 포함하지 않는다.

기준: [실습지의 2교시](../../lab.md#2교시-실습--모의-실기-b-git-상황-판단과-ollama-툴-콜링). 아래 시간은 실습 30분의 구간이며, 설명 20분·휴식 10분은 기존 시간표를 따른다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–3분 | 문항 읽고 완료 조건 표시 | `tasks_B.md` |
| 3–9분 | Git 기록 흐름, `git status` 읽기 | `tasks_B.md` B-1 |
| 9–17분 | GitHub에 올리기(실기) | `tasks_B.md` B-2, 모의 A의 `week8-hello` |
| 17–22분 | Ollama 사용법 개념 문항 | `tasks_B.md` B-3 |
| 22–30분 | 툴 콜링 함수 추가·실행·기록 | 4주차 `period3/src/ex07/tools.py`, `answers_B.md` |

## 이전 산출물과 시작 위치

B-2는 1교시 A-2에서 만든 `week8-hello`를 쓴다(없으면 아무 uv 프로젝트). GitHub는 2주차 계정으로 로그인해 둔다. B-4는 4주차 3교시에 만든 `C:\classwork\week04\period3`에서 한다. 없으면 교재 `week04_ollama_local_llm/examples/period3`를 복사하고 `uv sync`한다. 모델은 사전 캐시한 `qwen3.5:2b`만 사용한다.

## 실행 순서

```powershell
Set-Location C:\classwork\week04\period3
ollama show qwen3.5:2b      # Capabilities 에 tools 가 있는지 본다
uv sync
code src\ex07\tools.py      # discount_price 추가, TOOLS 등록
uv run ex07                 # 지정 질문 입력 → [함수 실행] 줄 기록 → /bye
```

B-1·B-3은 모델 없이 읽고 답한다. B-2는 `git remote add origin <URL>` → `git push -u origin main` → README 수정 → `git add`·`commit`·`push` 순서다. B-4는 `[함수 실행]` 줄과 `AI>` 답을 그대로 `answers_B.md`에 붙인다.

## 예상 출력과 완료 확인

`[함수 실행] discount_price({'price': 25000, 'percent': 20}) -> 20000.0`처럼 모델이 새 함수를 부른 줄이 보여야 한다. 함수 결과와 `AI>` 답이 다르면 함수 결과가 정답이다. 모델이 함수를 부르지 않으면 질문이나 docstring을 바꿔 다시 시도하고, 바꾼 내용과 결과를 적는다.

## 대체 경로

GPU가 없는 PC도 `qwen3.5:2b`로 진행한다(느릴 뿐이다). Ollama 서버가 없으면 B-1~B-3과 B-4-1·B-4-4·B-4-5를 먼저 끝내고, 실행 기록은 서버가 있는 PC에서 남긴다. 없는 실행 결과를 답안에 쓰지 않는다.

실측 결과·답안은 개인 실습 폴더에 기록한다. 실제 비밀정보와 환경 폴더를 공개하지 않는다.
