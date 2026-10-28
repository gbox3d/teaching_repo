# 2교시 — pipeline으로 분류·생성

`transformers`의 `pipeline` 한 줄이 토크나이저·모델·후처리를 묶어 준다. 모델은 수업 전에 받아 둔 캐시에서 읽는다.

```powershell
uv sync
uv run ex04
```

| 명령 | 배우는 것 | 해 보기 |
|---|---|---|
| `uv run ex04` | `pipeline("text-classification", model=, revision=, device=)` | 한국어·영어 문장을 넣어 라벨·점수·시간 비교 |
| `uv run ex05` | `pipeline("text-generation")`에 4주차와 같은 `messages`를 넣기 | 같은 질문을 4주차 Ollama `ex02`에도 해서 답 비교 |

## 공용 패키지 — `src/shared/`

두 예제가 함께 쓰는 모델 ID·revision과 장치 고르기(`pick_device()`)는 `src/shared/__init__.py`에 있다. 예제는 `from shared import CLS_MODEL, pick_device`처럼 라이브러리를 쓰듯 가져온다. revision을 commit hash로 고정하거나 모델을 바꿀 때는 이 파일만 고친다. `shared`는 명령이 필요 없으므로 `[project.scripts]`에는 없고 `module-name`에만 있다.

## 장치 비교

`pick_device()`는 NVIDIA GPU가 있으면 `cuda`, Apple 실리콘이면 `mps`, 아니면 `cpu`를 고른다. CPU와 비교할 때는 예제의 `DEVICE = pick_device()`를 `DEVICE = "cpu"`로 바꿔 다시 실행한다. 첫 실행의 "로드" 시간에는 다운로드가 섞일 수 있으므로 두 번째 실행을 기준으로 잰다.

## 안 될 때

- `Both max_new_tokens ... and max_length ... seem to have been set`: 모델 설정의 기본값과 겹친다는 안내다. `max_new_tokens`가 쓰이므로 무시해도 된다.
- Traceback 맨 아래가 `OSError: ... is not a valid git identifier`: `src/shared/__init__.py`의 `*_REVISION` 철자를 1교시 `ex01`의 commit과 대조한다. Traceback은 맨 아래 줄이 이유다.
- `Torch not compiled with CUDA enabled`: CUDA 휠이 아니다. 이번 실습은 `DEVICE = "cpu"`로 진행하고 조교에게 알린다.
