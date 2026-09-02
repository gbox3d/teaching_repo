# 모의 실기 B — 클라이언트 기능 추가와 결과 해석

공개 동형 모의 문제다. 실제 실기 패킷의 문항·값·정답이 아니다. 제한 시간은 30분이며, 답안은 실습 폴더의 `answers_B.md`에 맨 아래 양식으로 쓴다.

## B-1 · Ollama 클라이언트 기능 추가

### 요구사항

`client_starter/`를 복사한 프로젝트에서 `chat.py`의 `TODO(B-1)`을 채운다.

1. `--system` 인자: 주어지면 `{"role": "system", "content": ...}` 메시지를 `messages`의 맨 앞에 넣는다. 없으면 지금과 같이 동작한다.
2. 응답 메타 기록: `outputs/chat-*.json`에 다음 키를 추가한다.
   - `system`: 준 값, 없으면 `null`
   - `eval_count`, `eval_duration`, `total_duration`: 응답 JSON의 값 그대로(`eval_duration`·`total_duration` 단위는 나노초)
   - `tokens_per_sec`: `eval_count / (eval_duration / 1e9)`를 소수 첫째 자리까지. `eval_duration`이 0이거나 없으면 `null`
3. 요청 JSON에 `stream: false`, `think: false`, `options`가 그대로 남아 있어야 한다.
4. 모델 이름·주소는 환경변수와 인자로만 정한다. 코드에 하드코딩하지 않는다.

### 완료 조건

- [ ] `uv run python chat.py --prompt "..." --system "모든 답을 한 문장으로만 한다."`가 동작한다.
- [ ] `outputs/chat-*.json`에 위 5개 키가 있고 `tokens_per_sec`가 숫자다.
- [ ] `--system` 유무 두 실행의 `content`·`eval_count` 차이를 `answers_B.md`에 한 문장으로 적었다.
- [ ] `--model nonexistent-model`로 실행하면 사람이 읽을 메시지와 0이 아닌 종료 코드가 나온다.
- [ ] Ollama를 끄고 실행하면 연결 실패 메시지가 나온다(모델 없음 메시지와 다른 문장).

### 검증 순서

```powershell
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라."
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라." --system "모든 답을 한 문장으로만 한다."
Get-ChildItem outputs
Get-Content outputs\chat-<가장 최근>.json
uv run python chat.py --prompt "테스트" --model nonexistent-model
$LASTEXITCODE
```

Ollama를 끈 상태의 연결 실패는 서버를 잠시 멈출 수 있는 PC에서만 재현한다. 공용 서버를 쓰는 실습실에서는 `--host http://localhost:1`로 대신 재현한다.

## B-2 · pipeline 결과 해석 3문항

`fixtures/pipeline_output.json`을 연다. 5주차 `pipeline` 실행 결과를 정리한 형식의 **자체 작성 샘플**이며 실제 모델 실행 결과가 아니다. 각 문항은 판단 + 근거 + 근거로 삼은 JSON 키 이름을 적는다.

### B-2-1 · 분류 점수 해석

`text_classification.outputs`의 세 번째 결과는 `label`이 `neutral`, `score`가 `0.5137`이다.

- (a) 이 `score`는 무엇을 뜻하는가?
- (b) 이 결과를 그대로 서비스의 최종 답으로 쓰면 안 되는 이유는?
- (c) 이런 경우를 다루는 방법 1가지(코드 또는 운영).

### B-2-2 · 생성 반복과 stderr

`text_generation.outputs[0].generated_text`는 같은 문장을 반복하다가 잘려 있다.

- (a) 반복을 줄이기 위해 확인·조정할 생성 인자 2개와 각 인자의 역할.
- (b) `stderr`의 `Setting pad_token_id to eos_token_id` 메시지는 오류인가, 안내인가? 근거.
- (c) 출력이 잘린 이유를 `generation_kwargs`에서 찾아 적는다.

### B-2-3 · device와 실행 시간

`text_generation.device`는 `cpu`, `elapsed_sec`는 `6.82`다. 같은 PC에 GPU가 있다.

- (a) `pipeline(...)` 호출에서 GPU를 쓰게 하려면 무엇을 지정하는가?
- (b) 실제로 GPU에서 돌았는지 확인하는 방법 2가지.
- (c) `torch_dtype`이 `float32`인 것이 VRAM과 속도에 어떤 영향을 주는가?

## `answers_B.md` 양식

```markdown
# 모의 실기 B 답안 — student01

## B-1 기능 추가

바꾼 함수·인자:
--system 유무 비교(한 문장, eval_count 값 포함):
연결 실패 메시지(문장 그대로):
모델 없음 메시지(문장 그대로):
outputs 파일 이름 2개:
마지막 commit id:

## B-2 해석

### B-2-1
(a) 판단 / 근거 / 참조 키:
(b):
(c):

### B-2-2
(a) 인자 1 / 인자 2:
(b) 판단 / 근거:
(c):

### B-2-3
(a):
(b) 방법 1 / 방법 2:
(c):

## 못 끝낸 항목 (증상·관찰·시도)
```
