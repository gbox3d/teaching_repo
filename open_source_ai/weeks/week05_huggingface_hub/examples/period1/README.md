# 1교시 — Hub 정보·모델 카드 읽기, 캐시 보기

`huggingface_hub` 라이브러리로 Hub에 묻는다. 모델을 내려받지 않고 정보와 카드만 읽는다. 네트워크가 필요하다.

## 처음부터 만들어 보기 — `uv init`

교재 폴더를 쓰기 전에 같은 구조를 Python 3.12로 직접 만든다. `--package`가 배포 표준 구조(`[project.scripts]`·`[build-system]`·`src/`)를 만든다.

```powershell
uv init --package --python 3.12 --vcs none my-hub
Set-Location my-hub
uv add huggingface_hub
uv run my-hub           # Hello from my-hub!
```

교재 폴더가 아닌 곳에서 실행한다. 교재 폴더 안에서 하면 교재 `pyproject.toml`에 `[tool.uv.workspace]`가 추가된다.

## 예제

```powershell
uv sync
uv run ex01
```

| 명령 | 배우는 것 | 해 보기 |
|---|---|---|
| `uv run ex01` | `HfApi().model_info()`로 license·task·gated·commit·파일 합계 읽기 | `Qwen/Qwen2.5-0.5B-Instruct`, `intfloat/multilingual-e5-small`, `meta-llama/Llama-3.2-1B-Instruct`를 차례로 입력 |
| `uv run ex02` | `ModelCard.load()`로 카드의 YAML 메타데이터와 본문 절 제목 보기 | 세 모델의 절 제목에서 "용도·학습 데이터·한계" 절 찾기 |
| `uv run ex03` | `scan_cache_dir()`로 캐시 위치·용량·commit hash 보기 | `ex02` 뒤에 다시 실행해 카드(README.md)만 캐시에 생긴 것 확인 |

같은 일을 명령으로도 할 수 있다: `uv run hf cache ls`. 라이브러리 함수와 명령이 같은 캐시를 본다.

## 안 될 때

- `Hub 오류: Repo id must use alphanumeric chars ...`: 모델 ID는 영문 `조직/이름` 형식이다.
- `Hub 오류: 401 Client Error`: 없는 저장소도 401로 나온다. 비공개 저장소일 수도 있어서 Hub가 "권한 없음"으로 답한다. 철자부터 확인한다.
- `Warning: You are sending unauthenticated requests`: 토큰 없이 쓴다는 안내다. 이번 실습은 토큰이 필요 없다.
