# 3주차 예제 — oss-tool 프로젝트 골격과 재현 검사

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `oss_tool/` | uv 프로젝트. 3주차의 참조 구현이며 아래 파일을 담는다 | 1·2·3교시 |
| `oss_tool/pyproject.toml` | 의존성 `httpx`, `python-dotenv`(버전 고정 없음), `[project.scripts] oss-tool`, hatchling 빌드 백엔드, src 레이아웃 지정 | 1·2교시 |
| `oss_tool/src/oss_tool/__init__.py` | 패키지 표식과 `__version__` | 2교시 |
| `oss_tool/src/oss_tool/cli.py` | `greet`·`sysinfo`·`config` 서브커맨드. 결과는 stdout, 로그는 stderr | 2·3교시 |
| `oss_tool/src/oss_tool/sysinfo.py` | 1주차 `sysinfo.py`를 모듈로 정리한 것. `collect()`가 OS·CPU·RAM·GPU dict를 돌려준다 | 2교시 |
| `oss_tool/src/oss_tool/config.py` | 기본값 < `.env` < 셸 환경변수 < 명령 인자 순서의 설정 로더. 값마다 출처를 기록하고 비밀은 가린다 | 3교시 |
| `oss_tool/.env.example` | 이 프로젝트가 읽는 설정 키 목록과 예시값. `.env`로 복사한다 | 3교시 |
| `oss_tool/.gitignore` | `.venv/`, `.env`, `outputs/`, `__pycache__/` 등 커밋 제외 | 1교시 |
| `oss_tool/README.md` | 짧은 실행 안내. 2교시 "실행 절차 세 줄"의 예 | 2교시 |
| `reproduce_check.ps1` | 깨끗한 폴더에 clone → `uv sync --frozen` → 확인 명령. 결과를 `outputs/reproduce-*.md`에 기록 | 1교시 |
| `week03_notes_template.md` | 예상표·실패 경로·출처 관찰·이력 검사 기록 양식. 개인 저장소 `notes/week03.md`로 복사 | 전체 |

## 실행 방법

원본을 두고 개인 실습 폴더에 복사한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week03_reproducible_python\examples"
New-Item -ItemType Directory -Force C:\classwork\week03 | Out-Null
Copy-Item "$src\reproduce_check.ps1" C:\classwork\week03\
Copy-Item -Recurse "$src\oss_tool" C:\classwork\week03\oss_tool
```

예제 프로젝트 자체를 돌려 보려면(수업 전 캐시 겸용):

```powershell
Set-Location C:\classwork\week03\oss_tool
uv sync
uv run oss-tool --help
uv run oss-tool greet --name student01
uv run oss-tool sysinfo
uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json | Select-Object os, python
uv run oss-tool config
Copy-Item .env.example .env          # 값을 바꾼 뒤 다시 config 를 실행해 출처가 바뀌는지 본다
uv run oss-tool config --model qwen3:0.6b
uv run oss-tool config --json
```

재현 검사(1교시). `-Source`는 commit이 있는 git 저장소여야 하고 `-Dest`는 없는 폴더여야 한다. `-Keep`을 주면 복제본을 남긴다.

```powershell
Set-Location C:\classwork\week03
.\reproduce_check.ps1 -Source C:\classwork\osa-practice -Dest C:\classwork\_repro\osa-practice -Check 'uv run python -c "import httpx; print(httpx.__version__)"' -Keep
```

실습에서는 개인 저장소에 예제 폴더를 통째로 복사하지 않는다. 1교시에 `uv init`으로 직접 만들고, 2·3교시에 막힐 때 파일 단위로 열어 비교하거나 `sysinfo.py`·`config.py`처럼 지정된 파일만 가져온다.

`uv run`은 `.venv`가 없거나 `pyproject.toml`이 바뀌면 프로젝트를 다시 설치한다. 수업 전에 `uv sync`를 한 번 실행해 두면 실습 중 네트워크가 필요 없다.

## 관찰 지점

1. `uv sync` 출력에 프로젝트 자신이 `osa-week03-oss-tool==0.1.0 (from file:///...)`로 설치된다. 빌드 백엔드가 있어야 이 줄이 생기고, 그 결과 `.venv\Scripts\oss-tool.exe`가 만들어진다.
2. `[project.scripts]`의 함수 이름을 틀리게 바꾸면 `uv sync`는 통과하고 실행 때 `ImportError: cannot import name ...`이 난다. 설치와 실행의 실패 시점이 다르다.
3. 결과는 stdout, 진행 로그(`INFO oss_tool: 저장: ...`)는 stderr다. `2>$null`로 stderr를 버려도 JSON이 온전하다.
4. `sysinfo --json`은 stdout에 `ensure_ascii=True`로 쓰고 파일에는 `ensure_ascii=False`로 쓴다. 파이프의 콘솔 인코딩과 파일의 가독성을 따로 챙긴 것이다.
5. `config`의 출처 열이 `default` → `.env` → `env` → `arg`로 바뀐다. 좁은 범위일수록 우선한다.
6. `HF_TOKEN`처럼 비밀로 보이는 키는 `(설정됨, 가려짐)`으로만 표시되고 `outputs/config-*.json`에도 값이 저장되지 않는다. `outputs/`도 유출 경로다.
7. uv는 `.venv` 안에 `*` 한 줄짜리 `.gitignore`를 넣어 두므로 루트 `.gitignore` 없이도 `git status`에 `.venv/`가 보이지 않는다. 그래도 루트 `.gitignore`에 `.venv/`를 명시한다. 다른 도구가 만든 가상환경은 스스로를 무시하지 않는다.
8. `reproduce_check.ps1`의 2단계는 복제본에 `.venv`·`.env`가 없고 `uv.lock`이 있어야 OK다. `uv.lock`을 지우고 `uv sync --frozen`을 실행하면 실패하고, 플래그 없이 실행하면 새로 해석해 lock을 만든다.

## GPU 없을 때·네트워크 없을 때

- 이번 주는 GPU·모델·Ollama 서버가 필요 없다. `sysinfo`는 `nvidia-smi`가 없으면 `gpu.available: false`와 이유를 기록하고 정상 종료한다. GPU 없는 PC에서는 그 출력이 정상 경로다.
- 네트워크가 없으면 캐시만 쓴다. 수업 전에 이 예제에서 `uv sync`를 했다면 `httpx`·`python-dotenv`·`hatchling`이 캐시에 있다. `uv add --offline httpx`, `uv sync --frozen --offline`처럼 `--offline`을 붙인다. `uv init`이 Python을 내려받으려 하면 `uv python list`로 설치된 버전을 확인하고 조교에게 알린다.
- Ollama는 3교시 확장 문제 `config --ping`에서만 쓴다. 서버가 꺼져 있으면 `연결 실패: ...` 한 문장과 종료 코드 2가 나오는 것이 정상 관찰이다.
- Windows PowerShell 5.1에서 `reproduce_check.ps1`을 실행하면 한글 메시지가 깨질 수 있다. 판정(OK/FAIL)·종료 코드·로그 파일은 영향이 없다. `pwsh`(PowerShell 7)로 실행하면 깨지지 않는다. 실행 정책 오류는 `pwsh -ExecutionPolicy Bypass -File .\reproduce_check.ps1 ...`로 우회한다.
- `ConvertFrom-Json`은 Windows PowerShell 5.1에서 여러 줄 입력을 바로 받지 못한다. 예시처럼 `| Out-String |`을 사이에 넣는다.

## 복사 후 변형

- `sysinfo.py`는 1주차 코드의 모듈 버전이므로 개인 저장소에 그대로 가져가도 된다. `cli.py`의 `greet`·`sysinfo`·`config` 연결은 실습지의 단계대로 직접 쓴다.
- `config.py`의 `DEFAULTS`는 교재 검증용 값이다. 환경 기준표가 정한 값은 코드가 아니라 `.env`에 쓴다.
- `.env.example`에 키를 추가하면 `config.py`의 `DEFAULTS` 또는 `OPTIONAL_KEYS`에도 같은 키를 넣어야 `config`가 보여 준다.
- `outputs/`는 커밋하지 않는다. 증거로 남길 로그는 `notes/`에 복사한다.
- `reproduce_check.ps1`의 `-Check`에는 어떤 명령이든 줄 수 있다. 2교시 뒤에는 `-Check 'uv run oss-tool greet --name student01'`로 다시 검사해 본다.

## 기본값과 환경 기준표

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 주소. 4주차부터 실제 호출에 쓴다 |
| `OLLAMA_MODEL` | `qwen3:8b` | 기본 생성 모델(RTX 4070 기준). CPU 대체는 `qwen3:0.6b` |
| `HF_TOKEN` | (비어 있음) | Hugging Face 토큰. 5주차 이후 필요할 때만 `.env`에 채운다 |

모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 위 값은 교재 검증용 기본값이다. `uv.lock`은 만들지 않았다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
