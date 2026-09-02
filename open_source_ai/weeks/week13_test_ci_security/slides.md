---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 13주차"
footer: "테스트·CI·보안·코드리뷰"
---

# 13주차
## 테스트·CI·보안·코드리뷰

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | pytest 구조, 모델 호출 격리, 단위 vs 통합, ruff | 가짜 클라이언트로 서비스 테스트 만들기 |
| 2교시 | GitHub Actions 구조, setup-uv·캐시, 상태 체크, 실패 로그 | GitHub Actions로 초록불과 빨간불 만들기 |
| 3교시 | 공급망 보안, 비밀 유출 방지, 모델 파일 안전, 리뷰 체크리스트 | 의존성 감사와 비밀 검색, 교차 리뷰 |

이번 주 질문: **모델 호출이 들어간 코드를 어떻게 자동으로 검사하고, 다른 사람의 변경을 어떻게 안전하게 받아들이는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 모델을 끄고도 검사한다

---

## 0–3분 · "내 PC에서는 됨"을 자동화한다

12주차에 502·503·504를 **손으로** 재현했다 — 환경변수 바꾸고, 서버 재시작하고, 눈으로 확인.

- 리뷰어마다, PR마다 그 절차를 반복하면 결국 아무도 안 한다
- 테스트 = 그 확인 절차를 **코드로 적어 둔 것**. `uv run pytest` 한 줄로 반복
- 검사하는 것: 우리 코드의 변환·검증·오류 매핑
- 검사하지 않는 것: 모델 답의 품질(11주차 평가의 일)

**질문:** 모델 답이 매번 달라지는데, 무엇을 `assert`할 수 있는가?

---

## 3–6분 · pytest 구조 — 발견·assert·출력

```python
# tests/test_schemas.py   ← 파일 test_*.py, 함수 test_* 이면 자동으로 찾는다
from app.schemas import ChatRequest

def test_valid_request_uses_defaults():
    request = ChatRequest(prompt="질문")
    assert request.temperature == 0.2   # 실패하면 양쪽 값을 함께 보여 준다
```

```text
uv run pytest -q
...........F.......                                            [100%]
FAILED tests/test_service.py::test_chat_converts_fake_response - assert 1500000.0 == 1500.0
```

실패 요약의 `assert 왼쪽 == 오른쪽`이 첫 단서다. 스택을 다 읽기 전에 **두 값의 차이**를 말한다.

---

## 6–9분 · fixture와 parametrize

```python
@pytest.fixture
def service(fake_client):                # 같은 이름의 인자에 주입된다
    return ChatService(client=fake_client, model="fake-model:test", host="http://fake")

@pytest.mark.parametrize("body", [
    {"prompt": ""}, {"prompt": "안녕", "temperature": 5.0}, {"prompt": "안녕", "max_tokens": 0},
])
def test_out_of_range_request_is_rejected(body):
    with pytest.raises(ValidationError):
        ChatRequest(**body)
```

- fixture: 준비 코드를 한 곳에. `tests/conftest.py`에 두면 모든 테스트 파일이 공유한다
- parametrize: 같은 검사를 여러 입력으로. 실패하면 **어느 입력**인지 표시된다

---

## 9–12분 · 모델 호출 격리 — 의존성 주입

```text
운영:   main.py get_service() ─▶ ChatService(client=HttpOllamaClient) ─▶ Ollama :11434
테스트: conftest.py            ─▶ ChatService(client=FakeOllamaClient) ─▶ 미리 정한 dict
```

- 서비스는 구체 클래스가 아니라 **모양(Protocol)** — `chat()`·`list_models()` — 에만 의존한다
- 가짜는 `reply`·`fail_with`로 정상·오류를 마음대로 만들고, `calls`로 무엇을 넘겼는지 본다
- HTTP 계층은 `app.dependency_overrides[get_service]` + `TestClient` — uvicorn 없이 422·503을 확인
- 12주차의 `get_client`가 바로 이 자리다

**질문:** 가짜의 응답 모양이 실제 Ollama와 다르면, 통과한 테스트는 무엇을 보장하는가?

---

## 12–15분 · 단위·통합, 느린 테스트 표시

| 종류 | 대상 | 필요한 것 | 속도 | 언제 |
|---|---|---|---|---|
| 단위 | 스키마·서비스 | 없음 | ms | 매 저장, 매 push |
| HTTP 계층 | 라우팅·상태 코드 | TestClient | ms | 매 push |
| 통합 | 실제 Ollama | 서버·모델·GPU | 초~분 | 릴리스 전 수동 |

```toml
[tool.pytest.ini_options]
addopts = "-m 'not integration'"        # 기본 실행에서 제외
markers = ["integration: 실제 Ollama 서버가 필요한 느린 테스트"]
```

파일 맨 위 `pytestmark = pytest.mark.integration` + `RUN_INTEGRATION=1`일 때만 실제로 돈다.

---

## 15–17분 · ruff — lint와 format

```powershell
uv run ruff check .             # 문제 목록. --fix 는 안전한 것만 자동 수정
uv run ruff format --check .    # 고치지 않고 검사만 (CI 용)
uv run ruff format .            # 실제로 고친다
```

- lint: 안 쓰는 import(F401), 정의 안 된 이름(F821), import 순서(I), 흔한 버그(B), 긴 줄(E501)
- format: 줄바꿈·따옴표·공백 — **취향 논쟁을 도구에 넘긴다**
- 규칙은 `pyproject.toml`의 `[tool.ruff]`에 둔다. 팀 전체가 같은 규칙을 쓴다

**질문:** "여기 공백 두 칸"이라는 코멘트가 사라지면 리뷰어는 무엇에 시간을 쓰게 되는가?

---

## 17–20분 · 실습 인계

[1교시 실습 — 가짜 클라이언트로 서비스 테스트 만들기](lab.md#1교시-실습--가짜-클라이언트로-서비스-테스트-만들기)

완료 조건:

1. 테스트 3개(공백 prompt 거절·system 프롬프트 순서·모델 없음→404)를 추가해 `uv run pytest`가 통과한다
2. `ruff check`·`ruff format --check`가 통과하고, 일부러 만든 오류를 `--fix`로 고친 기록이 있다
3. `pytest -m integration`이 `RUN_INTEGRATION` 유무에 따라 `skipped`와 실제 실행으로 갈린다

실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 내 PC 밖에서 검사가 돈다

---

## 0–3분 · CI가 하는 일

```text
push / PR ─▶ GitHub 가 깨끗한 가상 머신을 빌린다 ─▶ checkout ─▶ uv sync ─▶ ruff ─▶ pytest ─▶ 초록 / 빨강
```

- "내 PC에서는 됨"이 통하지 않는 곳에서 **매번 같은 절차**
- 결과가 PR에 상태 체크로 붙는다 — 리뷰어는 로그 대신 초록불을 본다
- 3주차 재현성(`uv sync`) + 1교시 테스트가 합쳐진 것

**질문:** CI가 초록불이면 "버그가 없다"는 뜻인가?

---

## 3–6분 · workflow 구조 — on·jobs·steps

```text
.github/workflows/ci.yml       ← 저장소 루트 기준 이 경로여야 인식한다
├─ on:           언제 (push, pull_request, workflow_dispatch)
├─ permissions:  토큰 권한 (contents: read 가 최소)
└─ jobs:
   └─ test:      runs-on: ubuntu-latest
      └─ steps:  uses(남이 만든 액션) / run(셸 명령) 을 순서대로
```

- job은 서로 다른 머신에서 병렬로, step은 한 머신에서 순서대로
- step 하나가 실패하면 그 job은 거기서 멈춘다 → **실패한 step 이름**이 첫 단서

---

## 6–9분 · ci.yml 읽기

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with: { enable-cache: true }
      - run: uv python install          # requires-python 을 읽는다
      - run: uv sync                    # lock 을 커밋했다면 --frozen
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest -q
```

로컬에서 치던 명령과 **같은 명령**이다. 다른 것은 PC뿐이다.

---

## 9–12분 · setup-uv, 캐시, lock 검증

- `astral-sh/setup-uv`: uv 설치 + `enable-cache: true`면 내려받은 패키지를 다음 실행에 재사용
- 첫 실행과 두 번째 실행의 `uv sync` 시간을 비교해 본다
- `uv sync --frozen`: lock을 갱신하지 않고 그대로 설치. lock과 pyproject가 어긋나면 **실패** → "lock을 안 올린 PR"을 잡는다
- 러너는 Linux다 — `C:\` 경로, `.ps1`은 CI에서 돌지 않는다
- 액션 메이저 버전(`@v4`, `@v6`)은 환경 기준표에서 확정한다

**질문:** 캐시가 오래된 취약 버전을 붙들 수 있는가? 설치 버전을 결정하는 것은 무엇인가?

---

## 12–15분 · PR 상태 체크와 branch protection

| 표시 | 뜻 | 리뷰어의 행동 |
|---|---|---|
| 노란 원 | 실행 중 | 기다린다 |
| 초록 체크 | required 잡 모두 통과 | 코드 리뷰 시작 |
| 빨간 X | 하나 이상 실패 | 로그 링크를 코멘트에 붙이고 수정 요청 |

- Settings → Branches → `main` 보호 규칙: **required status checks** + PR 필수
- 빨간불이면 merge 버튼이 잠긴다. 관리자도 예외로 두지 않는다
- 이 규칙을 9주차 `CONTRIBUTING.md`에 한 줄로 적는다

---

## 15–17분 · 실패 로그 읽는 순서

```text
1. Actions 탭 → 실패한 실행 → 빨간 job 클릭
2. step 목록에서 X 가 붙은 하나 → 그 step 의 명령이 무엇이었는가
3. 로그의 첫 오류 줄(FAILED …, error:, E501 …)을 복사
4. 로컬에서 같은 명령을 실행해 재현 → 고침 → push → 다시 초록불
```

- 맨 아래가 아니라 **첫 오류**를 본다. 뒤의 오류는 대개 첫 오류의 결과다
- 로컬은 되는데 CI만 실패: OS 차이(경로·대소문자), 캐시 없는 상태, 환경변수 없음

**질문:** 로컬 `pytest`는 통과하는데 CI에서 `ModuleNotFoundError`가 난다. 무엇부터 의심하는가?

---

## 17–20분 · 실습 인계

[2교시 실습 — GitHub Actions로 초록불과 빨간불 만들기](lab.md#2교시-실습--github-actions로-초록불과-빨간불-만들기)

완료 조건:

1. 새 저장소에 push해 Actions 첫 실행이 초록불이고 PR에 상태 체크가 붙었다
2. 일부러 깨뜨린 commit으로 빨간불을 만들고 **실패한 step 이름과 첫 오류 줄**을 기록했다
3. 고친 commit으로 다시 초록불을 만들어 PR을 merge했다

실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 남의 코드를 안전하게 받아들인다

---

## 0–3분 · 공급망 — 내가 쓴 300줄, 가져온 수만 줄

```text
ci_lab (내 코드 약 300줄)
 ├─ fastapi ─ starlette ─ anyio ─ …
 ├─ pydantic ─ pydantic-core ─ typing-extensions
 ├─ httpx ─ httpcore ─ h11 ─ certifi
 └─ pytest, ruff, pip-audit ─ …           → uv export 로 세어 보면 40개가 넘는다
```

- 내 코드가 안전해도 의존성 하나의 구멍으로 서비스가 뚫린다
- **모델 파일도 의존성이다** — 가중치 파일 안에 코드가 들어갈 수 있다

**질문:** `uv sync` 한 번에 몇 개의 패키지가 들어오는지 세어 본 적이 있는가?

---

## 3–6분 · pip-audit — 알려진 취약점 대조

```powershell
uv export --format requirements-txt --no-hashes -o outputs/requirements-audit.txt
uv run pip-audit -r outputs/requirements-audit.txt --no-deps
uv run python audit_report.py            # 위 둘 + outputs/audit-*.md 요약
```

결과 읽기: 패키지 · 설치 버전 · 취약점 ID(PYSEC·GHSA·CVE) · **고친 버전**

- 고친 버전 있음 → 하한 올리기 → `uv lock` → 테스트 → PR
- 고친 버전 없음 → 우리가 그 기능을 쓰는지 판단하고 기록
- 취약점 DB 조회는 네트워크가 필요하다. CI의 `audit` 잡은 `continue-on-error`

---

## 6–9분 · lock 검증과 타이포스쿼팅

| 위험 | 예 | 방어 |
|---|---|---|
| 이름 한 글자 다른 패키지 | `requests` ↔ `reqeusts` | 설치 전 PyPI 페이지·저장소 링크·다운로드 수 확인 |
| lock 없이 설치 | 오늘과 내일의 버전이 다름 | `uv.lock` 커밋 + `uv sync --frozen` |
| 배포 파일 변조 | 같은 버전, 다른 내용 | lock의 sha256을 uv가 대조 |
| "버전만 올렸어요" PR | 의존성 diff 미확인 | `uv.lock` diff 읽기 + CI 초록불 |

`uv add` 전에 이름을 **한 번 더 읽는다**. 오타 패키지는 설치되는 순간 코드를 실행할 수 있다.

---

## 9–12분 · 비밀 유출 방지 — 세 겹

```text
1겹 내 PC:   .gitignore(.env) + security_check.ps1(커밋 전)   ← pre-commit 훅으로 자동화 가능
2겹 GitHub:  secret scanning + push protection(패턴이 보이면 push 자체를 막는다)
3겹 사고 후: 히스토리에 남았다면 지우는 것으로 끝나지 않는다 → 토큰 회전(폐기·재발급)
```

- `security_check.ps1`: 토큰 패턴 · `.env` 추적 · pickle 모델 파일 · `trust_remote_code` — 찾은 줄의 **내용은 출력하지 않는다**
- 3주차 `git log -p` 검사와 같은 원칙: 한 번 push된 비밀은 유출된 것으로 본다

**질문:** push protection이 막았다. 그 토큰은 아직 안전한가?

---

## 12–15분 · 모델 파일 안전 — pickle vs safetensors

| 형식 | 로드 방식 | 위험 |
|---|---|---|
| `.pkl`, `.pt`, `.bin` (pickle) | Python 객체 역직렬화 = 코드 실행 가능 | 파일을 여는 것만으로 임의 코드 |
| `.safetensors` | 텐서 데이터만, 코드 없음 | 낮음. Hub 기본(`Qwen/Qwen2.5-0.5B-Instruct` 등) |
| `.gguf` (Ollama) | 가중치 + 메타데이터 | 낮음 |

- `trust_remote_code=True`: 모델 저장소의 **Python 코드를 실행**한다 → 저장소·revision 고정, 코드를 읽고, 기록
- 출처 불명 어댑터·체크포인트는 받지 않는다. `SOURCES.md`에 revision·해시를 남긴다

---

## 15–17분 · 교차 코드리뷰 — 무엇을 보고 어떻게 말하는가

순서: 설명·Issue → CI 초록불 → 테스트 유무 → 오류 경로 → 비밀·의존성 → 출처·문서 (`REVIEW_CHECKLIST.md`)

```text
[근거] app/service.py 42줄: total_duration 을 1_000 으로 나눈다.
[문제] Ollama 는 나노초라서 결과가 ms 가 아니다. test_service 의 1500.0 과 어긋난다.
[제안] 1_000_000 으로 나누고 변수 이름에 단위(duration_ms)를 남긴다.
```

- 코멘트 하나 = **근거(파일:줄) → 문제 → 제안**. 취향은 `nit`
- 판정은 둘 중 하나: 승인 / 수정 요청(+ 무엇이 되면 승인할지)

**질문:** "이 코드는 별로다"와 위 코멘트의 차이는 무엇인가?

---

## 17–20분 · 실습 인계

[3교시 실습 — 의존성 감사와 비밀 검색, 교차 리뷰](lab.md#3교시-실습--의존성-감사와-비밀-검색-교차-리뷰)

완료 조건:

1. `outputs/audit-*.md`에 검사한 패키지 수·취약점 수·다음 행동이 있다
2. `security_check.ps1`이 깨끗한 저장소에서 0건, 심어 둔 `.env`·가짜 토큰·`.pt`를 모두 잡았고 심은 것을 제거했다
3. 다른 팀 PR에 체크리스트 기반 코멘트 2개 이상과 판정을 남기고 URL을 기록했다

실습 30분 뒤 휴식 10분.

---

## 이번 주 정리

```text
테스트: 가짜 클라이언트 주입 → 모델 없이 변환·검증·오류 매핑을 검사 → 느린 것은 마커로 분리
CI:     push·PR → 깨끗한 머신 → uv sync → ruff → pytest → 초록불이어야 merge
보안:   pip-audit(의존성) + security_check(비밀·모델 파일) + 체크리스트 리뷰(사람)
```

기계가 잡을 것은 기계에게(ruff·pytest·CI·pip-audit), 사람은 **근거 있는 판단**에 시간을 쓴다.

다음 주(`week14_release_feedback`): 초록불이 켜진 저장소를 `v0.1.0`으로 릴리스한다.
