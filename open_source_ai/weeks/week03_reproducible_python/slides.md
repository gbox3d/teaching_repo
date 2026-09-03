---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 3주차"
footer: "재현 가능한 Python 오픈소스 프로젝트"
---

# 3주차
## 재현 가능한 Python 오픈소스 프로젝트

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 재현성 실패, 가상환경, uv 명령 흐름, `pyproject.toml`·`uv.lock` | uv 프로젝트를 만들고 깨끗한 폴더에서 재현하기 |
| 2교시 | src 레이아웃, 엔트리포인트, argparse·logging, README 실행 절차 | oss-tool CLI 완성하기 |
| 3교시 | 설정과 코드 분리, `.env`, 설정 계층, 이미 커밋된 비밀 | 설정 로더와 비밀정보 분리 |

이번 주 질문: **다른 PC에서 같은 결과가 나오게 하려면 무엇을 넣고 무엇을 빼는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 내 PC에서만 되는 코드는 오픈소스가 아니다

---

## 0–3분 · "내 PC에서는 됩니다"의 정체

```text
A: pip install requests transformers      (전역, 작년에 설치)
B: pip install transformers               (전역, 오늘 최신)
같은 코드 → A는 동작, B는 ImportError 또는 다른 결과
```

- 어떤 패키지가, 어떤 버전으로, 어디에 설치됐는지 아무도 모른다
- 프로젝트 두 개가 한 Python을 공유하면 하나를 고칠 때 다른 하나가 깨진다
- 저장소에는 코드만 있고 **환경은 내 머릿속에만** 있다

**질문:** 2주차에 짝의 저장소를 clone했을 때 실행까지 됐는가? 무엇이 부족했는가?

---

## 3–6분 · 가상환경: 프로젝트마다 다른 방

```text
C:\classwork\
 ├─ osa-practice\.venv\    ← 이 프로젝트만의 Python + 패키지
 └─ other-proj\.venv\      ← 다른 버전이어도 서로 간섭 없음
```

- 가상환경 = 프로젝트 전용 **격리된 패키지 폴더**
- 지우고 다시 만들 수 있어야 한다 → 그래서 커밋하지 않는다
- 격리만으로는 부족하다: **무엇을 설치했는지 기록**이 함께 있어야 재현된다

---

## 6–9분 · uv 하나가 맡는 네 가지 일

| 일 | 예전 방식 | uv |
|---|---|---|
| Python 준비 | 설치 프로그램, PATH 수정 | `.python-version`을 읽어 자동 준비 |
| 가상환경 | `python -m venv`, activate | `.venv` 자동 생성·자동 사용 |
| 의존성 선언 | `requirements.txt` 손으로 편집 | `uv add`가 `pyproject.toml` 갱신 |
| 정확한 버전 고정 | `pip freeze` | `uv.lock` 자동 생성 |

activate를 외우지 않는다. **`uv run`이 항상 이 프로젝트의 `.venv`로 실행**한다.

---

## 9–12분 · 다섯 명령의 흐름

```powershell
uv init                  # pyproject.toml, .python-version 생성
uv add httpx             # 의존성 추가 + .venv 생성 + uv.lock 갱신
uv lock                  # pyproject → uv.lock 해석 (add가 이미 했다면 변화 없음)
uv sync --frozen         # uv.lock 그대로 .venv 설치 (받는 사람 쪽)
uv run python main.py    # .venv의 Python으로 실행
```

- 만드는 사람: `init → add → (lock) → run`
- 받는 사람: `clone → sync --frozen → run`

**질문:** `uv sync --frozen`은 `pyproject.toml`과 `uv.lock` 중 어느 것을 읽는가?

---

## 12–15분 · pyproject.toml과 uv.lock의 관계

```toml
# pyproject.toml — 사람이 쓰는 "의도"
dependencies = ["httpx"]
```

```text
# uv.lock — 도구가 만든 "결과". 손으로 고치지 않는다
httpx <정확한 버전> ← anyio, certifi, h11, httpcore, idna, ...
각 패키지의 정확한 버전 + 파일 해시 (개수는 해석 시점마다 다르다)
```

- `pyproject.toml`: 이름만 적어도 된다("httpx가 필요하다")
- `uv.lock`: 오늘 해석한 **전체 트리의 정확한 버전**을 고정
- 둘 다 커밋한다. lock이 없으면 다음 사람은 **다른 오늘**을 해석한다

---

## 15–17분 · 커밋할 것과 뺄 것

| 커밋한다 | 커밋하지 않는다 |
|---|---|
| `pyproject.toml` | `.venv/` (프로젝트마다 수 MB~수 GB) |
| `uv.lock` | `__pycache__/`, `*.pyc` |
| `.python-version` | `.env` (3교시) |
| `src/`, `README.md`, `.gitignore` | `outputs/` (실행 결과) |

기준은 하나다. **"다시 만들 수 있는 것은 빼고, 다시 만들 수 없는 것은 넣는다."**

---

## 17–20분 · 실습 인계

[1교시 실습 — uv 프로젝트를 만들고 깨끗한 폴더에서 재현하기](lab.md#1교시-실습--uv-프로젝트를-만들고-깨끗한-폴더에서-재현하기)

완료 조건:

1. `pyproject.toml`과 `uv.lock`이 commit되고 `.venv/`는 `git status`에 보이지 않는다
2. 깨끗한 폴더에 clone → `uv sync --frozen` → `import httpx`가 성공한 로그가 있다
3. `uv.lock`을 지우면 `--frozen`이 왜 실패하는지 한 문장으로 적었다

실습 30분 뒤 휴식 10분. 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 스크립트 한 장을 설치 가능한 도구로

---

## 0–3분 · 왜 구조가 필요한가

```text
지금:  uv run python sysinfo.py           # 파일 위치를 알아야 실행된다
목표:  uv run oss-tool sysinfo --json     # 어디서든 이름으로 실행된다
```

- 파일이 셋만 넘어도 `from sysinfo import ...`가 현재 폴더에 따라 깨진다
- 다른 사람은 "어느 파일을 실행하라는 것인지"부터 묻는다
- 이름 있는 명령 하나가 README의 실행 절차를 **세 줄**로 줄인다

**질문:** `python sysinfo.py`를 저장소 밖의 다른 폴더에서 실행하면 무엇이 깨지는가?

---

## 3–6분 · src 레이아웃과 패키지·모듈

```text
osa-practice/
 ├─ pyproject.toml
 ├─ src/
 │   └─ oss_tool/          ← 패키지 (폴더 + __init__.py)
 │       ├─ __init__.py
 │       ├─ cli.py          ← 모듈
 │       ├─ sysinfo.py
 │       └─ config.py
 └─ outputs/               ← 실행 결과, 커밋 안 함
```

- `src/` 아래 두면 **설치된 패키지**만 import된다 → 현재 폴더에 의존하는 버그가 사라진다
- 패키지 이름은 `oss_tool`(밑줄), 명령 이름은 `oss-tool`(하이픈)

---

## 6–9분 · 엔트리포인트: 이름과 함수를 잇는 한 줄

```toml
[project.scripts]
oss-tool = "oss_tool.cli:main"      # 명령 이름 = "패키지.모듈:함수"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oss_tool"]
```

- `uv sync`가 프로젝트를 `.venv`에 **편집 가능 설치** → `.venv\Scripts\oss-tool.exe`가 생긴다
- `main()`의 반환값이 종료 코드가 된다(0이 성공)

---

## 9–12분 · argparse 서브커맨드 설계

```python
parser = argparse.ArgumentParser(prog="oss-tool")
sub = parser.add_subparsers(dest="command", required=True)

greet = sub.add_parser("greet", help="인사말 출력")
greet.add_argument("--name", default="student01")
greet.set_defaults(func=cmd_greet)

args = parser.parse_args()
return args.func(args)            # 서브커맨드별 함수로 분기
```

- `git commit`, `uv add`처럼 **동사 하나 = 서브커맨드 하나**
- `--help`는 공짜다. `help=` 한 줄이 곧 문서다

**질문:** `--name`의 기본값을 코드에 두는 것과 설정 파일에 두는 것은 무엇이 다른가?

---

## 12–15분 · print가 아니라 logging

```python
import logging, sys
log = logging.getLogger("oss_tool")
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(levelname)s %(name)s: %(message)s")

log.info("저장: %s", path)        # 진행 상황 → stderr
print(json.dumps(result))        # 결과 → stdout
```

- 결과는 **stdout**, 진행·경고는 **stderr** → `| ConvertFrom-Json`이 깨지지 않는다
- `--verbose`로 `DEBUG`를 켠다: 코드를 고치지 않고 정보량을 바꾼다

---

## 15–17분 · README의 실행 절차 세 줄

```markdown
## 실행
1. `uv sync --frozen`
2. `uv run oss-tool greet --name student01`
3. `uv run oss-tool sysinfo --json`   (결과는 outputs/ 에 저장)
```

- 처음 보는 사람이 **복사해서 붙여넣기만** 하면 되는 형태
- 옵션 목록은 `--help`에 맡기고 README에는 흐름만 적는다

---

## 17–20분 · 실습 인계

[2교시 실습 — oss-tool CLI 완성하기](lab.md#2교시-실습--oss-tool-cli-완성하기)

완료 조건:

1. `uv run oss-tool greet --name student01`이 인사말을 출력한다
2. `uv run oss-tool sysinfo --json`이 유효한 JSON을 출력하고 `outputs/`에 파일을 남긴다
3. README에 실행 절차 세 줄이 있고 commit했다

실습 30분 뒤 휴식 10분. 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 설정은 저장소 밖에, 코드는 저장소 안에

---

## 0–3분 · 코드에 박힌 설정의 대가

```python
HOST = "http://10.0.0.5:11434"       # 강의실 서버 주소
TOKEN = "hf_(실제 토큰)"              # 내 토큰
```

- PC가 바뀌면 코드를 고친다 → 고친 코드가 commit된다 → 모두가 내 주소를 받는다
- 토큰이 저장소에 들어가면 **공개하는 순간 유출**이다
- 코드와 설정을 분리하면 같은 코드가 강의실·집·CI에서 그대로 돈다

**질문:** 강의실 PC와 집 PC의 Ollama 주소가 다르면 코드는 몇 줄 바뀌어야 하는가?

---

## 3–6분 · .env와 .env.example

```text
.env.example   ← 커밋한다. 키 이름과 예시값·설명만
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
HF_TOKEN=

.env           ← 커밋하지 않는다. 내 PC의 실제 값
```

- `.env.example`은 "이 프로젝트가 읽는 설정 목록"이라는 **문서**다
- 새 PC에서는 `Copy-Item .env.example .env` 뒤 값만 채운다
- 비밀이 아닌 값(`OLLAMA_MODEL`)도 같은 통로로 다룬다

---

## 6–9분 · python-dotenv와 os.environ

```python
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()                        # .env → os.environ (이미 있는 변수는 덮지 않음)
os.environ.get("OLLAMA_HOST")        # 셸 변수와 .env 값이 섞여 보인다

file_values = dotenv_values(".env")  # .env 만 dict 로 읽는다 → 출처 추적 가능
```

- 셸에서 `$env:OLLAMA_MODEL = "qwen3:1.7b"`를 주면 `.env`보다 우선한다
- 예제 `config.py`는 `dotenv_values`로 **어디서 온 값인지**까지 기록한다

---

## 9–12분 · 설정 계층: 기본값 < .env < 환경변수 < 인자

```text
기본값     DEFAULTS["OLLAMA_MODEL"] = "qwen3:8b"    코드 안, 교재 검증용
  ↓ 덮어씀
.env       OLLAMA_MODEL=qwen3:0.6b                 이 PC 의 상시 설정
  ↓ 덮어씀
환경변수   $env:OLLAMA_MODEL = "..."                이 셸 창에서만
  ↓ 덮어씀
인자       --model qwen3:14b                       이 실행 한 번만
```

**좁은 범위일수록 우선한다.** `oss-tool config`는 값과 함께 출처를 보여 준다

---

## 12–15분 · 이미 커밋된 비밀은 지워도 남는다

```text
commit 3  .env 삭제           ← 지금 파일은 없지만
commit 2  README 수정
commit 1  .env 추가 (토큰)    ← git log -p 로 누구나 읽는다
```

- `.gitignore`는 **아직 추적되지 않은** 파일만 막는다. 이미 add된 파일은 못 막는다
- push된 비밀은 "지운" 것이 아니다 → **토큰을 폐기하고 새로 발급(회전)** 이 유일한 해결
- 이력 재작성은 최후 수단이며 협업자 전원에게 영향을 준다

**질문:** `.gitignore`에 `.env`를 넣었는데 `git status`에 `.env`가 계속 보인다. 왜인가?

---

## 15–17분 · 실수 복구 흐름

```powershell
git add .                          # 실수: .env 가 staged
git status                         # "new file: .env" 발견
git restore --staged .env          # stage 에서만 내림 (파일은 그대로)
code .gitignore                    # .env 줄 추가: 앞으로 막기
git log --all --oneline -- .env    # 비어 있으면 이력에 없다
git log --all -p -S "fake-token"   # 문자열로도 검사
```

commit 전에 잡으면 이력에 남지 않는다. **`git status`를 읽는 습관**이 첫 번째 방어선이다

---

## 17–20분 · 실습 인계

[3교시 실습 — 설정 로더와 비밀정보 분리](lab.md#3교시-실습--설정-로더와-비밀정보-분리)

완료 조건:

1. `uv run oss-tool config`가 `OLLAMA_HOST`·`OLLAMA_MODEL`의 값과 출처를 출력한다
2. `.env.example`은 commit되고 `.env`는 `.gitignore`로 막혀 있다
3. `git log`로 검사해 비밀이 이력에 없다는 문장을 적었다

실습 30분 뒤 휴식 10분.

---

## 이번 주 정리

```text
재현:  pyproject.toml(의도) + uv.lock(결과) 커밋, .venv 제외 → uv sync --frozen
구조:  src/oss_tool + [project.scripts] → uv run oss-tool <서브커맨드>
설정:  기본값 < .env < 환경변수 < 인자, .env.example 만 커밋
```

다음 주(`week04_ollama_local_llm`)는 이 `config.py`가 읽는 `OLLAMA_HOST`·`OLLAMA_MODEL`로 **실제 로컬 모델을 호출**한다.
