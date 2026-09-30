# 3교시 — 설정 로더와 비밀정보 분리

[실습지 3교시](../../lab.md#3교시-실습--설정-로더와-비밀정보-분리)의 **기본 문제 참조본**이다.
2교시의 `greet`·`sysinfo`를 그대로 두고 `config`를 추가한 시점이다.

| 실습 시간·단계 | 지금 열 파일 | 확인할 결과 |
|---|---|---|
| 0–5분 · 준비 | [pyproject.toml](pyproject.toml) | `python-dotenv` 의존성 추가 |
| 5–13분 · 문제 1 | [config.py](src/oss_tool/config.py), [cli.py](src/oss_tool/cli.py)의 `cmd_config` | 값과 출처 출력 |
| 13–19분 · 문제 2 | [.env.example](.env.example) | `default → .env → env → arg` |
| 19–25분 · 복구 | [.gitignore](.gitignore) | 가짜 .env stage 취소·제외 확인 |
| 25–30분 · 검증 | `uv run oss-tool config --json` | 비밀 값이 가려진 JSON |

기존 개인 저장소에서는 `uv add python-dotenv` 뒤 새 설정 모듈·명령만 추가한다.
참조본을 교재 밖에 복사해 비교할 때는 이 폴더의 `pyproject.toml` 옆에서:
```powershell
uv sync
uv run oss-tool config
Copy-Item .env.example .env
uv run oss-tool config
$env:OLLAMA_MODEL = "qwen3:1.7b"
uv run oss-tool config
uv run oss-tool config --model qwen3:14b
Remove-Item Env:OLLAMA_MODEL
uv run oss-tool config --json
```
`OLLAMA_MODEL`의 출처가 바뀌고, 가짜 `HF_TOKEN`을 넣어도 원문 값은 출력되지 않는다.
모델 이름은 설정 관찰용이며 실제 모델을 호출하지 않는다. GPU·Ollama 서버는 필요 없다.
`--ping`·시간초과 옵션은 선택 확장이다. [기존 통합 참조](../oss_tool/README.md)는 확장 내용을 확인할 때만 연다.
원본에는 lock이 없으므로 최초 `uv sync`, 검증된 배포 lock이 있으면 `--locked`를 사용한다.

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | `uv add python-dotenv`, 예상표(이기는 출처, 토큰 표시, staged `.env`) |
| 설정 로더 | 5–13분 | `config.py`(기본값 < `.env` < 환경변수 < 인자, 출처 기록), `config` 서브커맨드 |
| 계층 확인 | 13–19분 | `.env.example` commit → `.env` → 셸 변수 → `--model`로 출처 변화 관찰 |
| 실수 재현·복구 | 19–25분 | 가짜 토큰 `.env` → `git add -f .env` → `restore --staged` → ignore 확인 → 이력 검사 |
| 검증·기록 | 25–30분 | 검사 결과 문장, commit·push, `config --json`으로 4주차 연결 확인 |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
