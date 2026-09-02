# 14주차 예제 — 릴리스 키트와 릴리스 점검 도구

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `release_kit/README_TEMPLATE.md` | 릴리스용 README 8개 절(소개·왜·설치·실행·예시·제한·라이선스·출처)과 AI 도구 사용 내역 표 양식 | 1교시 |
| `release_kit/MODEL_CARD_TEMPLATE.md` | 어댑터 공개 팀용 모델 카드(Hub frontmatter 포함) | 1교시 |
| `release_kit/CHANGELOG_TEMPLATE.md` | Keep a Changelog 형식의 `[Unreleased]` 예시와 링크 줄 | 1·2교시 |
| `release_kit/CITATION.cff` | Citation File Format 예시(`cff-version`·`title`·`version`·`authors`) | 1교시 |
| `release_kit/release_checklist.md` | 릴리스 전 점검표 6절(문서·라이선스 호환·재현·보안·버전·피드백 통로). ★ 항목은 `release_check.py`가 본다 | 1·2교시 |
| `release_kit/reproduce_by_stranger.md` | 처음 보는 사람으로 10분 안에 재현하는 규칙·절차·기록 양식 | 2교시 |
| `release_kit/reproduce_by_stranger.ps1` | clone → 태그 checkout → `uv sync --frozen` → pytest를 단계별 초와 함께 `repro-log-*.md`에 기록하는 PowerShell 스크립트 | 2교시 |
| `release_kit/feedback_issue_template.md` | 재현 실패·제안·질문 Issue 양식과 정보 추가 요청 문장 | 2·3교시 |
| `release_kit/triage_labels.md` | triage 라벨 5개, 분류 절차, 응답 문장 예시, `DECISIONS.md` 양식 | 3교시 |
| `release_kit/demo_outline.md` | 3분 시연 구성, 실패 대비, 리허설 기록, 예상 질문 5개 | 3교시 |
| `release_check/` | uv 프로젝트. `release_check.py`(릴리스 문서·버전·비밀 관리 읽기 전용 점검), `tag_notes.py`(CHANGELOG → 릴리스 노트, `--promote`) | 1·2교시 |

`release_kit/`은 청사진이 지정한 템플릿 모음이다. `release_check/`는 점검표의 ★ 항목을 자동으로 보고 릴리스 노트 초안을 만드는 보조 도구로, 템플릿과 같은 절 이름·필드 이름을 기준으로 동작한다. 템플릿은 개인 실습 폴더나 팀 저장소에 복사해 채운다. 원본은 수정하지 않고, 괄호 안 예시 문장을 그대로 제출하지 않는다.

## 실행 방법 (PowerShell)

### 복사와 준비

```powershell
Copy-Item -Recurse <교재 경로>\week14_release_feedback\examples .\week14-practice
Set-Location .\week14-practice\release_check
Copy-Item .env.example .env
uv sync
```

`.env`의 `RELEASE_REPO`에 팀 저장소 경로를 적으면 아래 명령의 `--repo`를 생략할 수 있다. 명령행 인자가 `.env` 값보다 우선한다.
`uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

### 릴리스 준비 점검(1교시)

```powershell
uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0
uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0 --require-model-card
```

README 8개 절, AI 도구 사용 내역, LICENSE, CONTRIBUTING, CHANGELOG `[Unreleased]`, CITATION.cff 필드, `SOURCES.md`, `.env` 추적 여부, `.gitignore`, `pyproject.toml` version과 태그 일치, `uv.lock` 유무를 PASS / WARN / FAIL / INFO로 보여 주고 `outputs/release-check-<시각>.json`에 남긴다. FAIL이 있으면 종료 코드 1이다. 아무 파일도 고치지 않는다.

### 릴리스 노트와 CHANGELOG 승격(2교시)

```powershell
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0 --promote
```

첫 명령은 CHANGELOG의 `[0.1.0]` 절(없으면 `[Unreleased]` 절)로 `outputs/release-notes-v0.1.0.md`를 만들고 태그 명령을 화면에 제안한다. `--promote`는 `[Unreleased]`를 `[0.1.0] - <오늘>`로 바꾸고 빈 `[Unreleased]`를 위에 새로 둔다. 바꾸기 전 원본은 `outputs/CHANGELOG.before-<시각>.md`에 복사된다. `[0.1.0]` 절이 이미 있으면 승격하지 않고 멈춘다. git 명령은 실행하지 않으므로 태그와 push는 사람이 제안된 명령을 읽고 직접 한다.

### 교차 재현(2교시)

```powershell
Set-Location C:\classwork\repro
<실습 폴더>\week14-practice\release_kit\reproduce_by_stranger.ps1 -Source https://github.com/<org>/<repo>.git -Tag v0.1.0
```

`.\repro\repro-<시각>\`에 clone하고 `.\repro\repro-log-<시각>.md`에 단계·초·결과를 남긴다. clone·checkout·`uv sync --frozen`·pytest까지만 자동이고, README 「실행」 절의 명령은 사람이 직접 실행해 기록 파일 아래에 적는다. 실행 정책 오류가 나면 `powershell -ExecutionPolicy Bypass -File .\reproduce_by_stranger.ps1 ...`처럼 파일 단위로만 우회한다.

## 관찰 지점

1. `release_check.py`의 FAIL과 WARN의 차이. FAIL은 릴리스를 막는 것(문서 없음, `.env` 추적, 버전 불일치), WARN은 사람이 판단할 것(`uv.lock` 없음, 라이선스 이름을 못 찾음).
2. README 절 제목에 단서 단어가 없을 때 `readme.sections`가 FAIL이 되는 현상. 도구는 제목 줄만 본다.
3. `--promote` 전후의 CHANGELOG diff. `[Unreleased]`가 비고 `[0.1.0] - 날짜` 절이 생겼는지, 링크 줄이 아직 `REPO_URL`인지.
4. `repro-log-*.md`의 단계별 초. `uv sync --frozen`이 가장 오래 걸리거나 가장 먼저 실패하는 단계다. 실패 메시지 첫 줄로 `uv.lock` 문제(릴리스 결함)와 네트워크 문제(환경)를 구분한다.
5. 없는 태그(`-Tag v9.9.9`)로 실행했을 때 스크립트가 checkout 단계에서 멈추고 남기는 메시지.
6. `triage_labels.md`의 응답 예시 세 가지에 공통으로 없는 것: 사람에 대한 표현, 기한 약속, "제 PC에서는 됩니다".

## GPU 없을 때·네트워크 없을 때 대체 경로

- 이번 주 예제는 모델·GPU·Ollama 없이 동작한다. `release_check.py`·`tag_notes.py`는 파일만 읽는다.
- 네트워크가 없으면 `reproduce_by_stranger.ps1 -Source`에 짝 팀 저장소의 로컬 경로(USB·공유 폴더)를 준다. uv 캐시에 패키지가 있으면 `uv sync --frozen`이 오프라인으로도 성공한다.
- GitHub Release를 만들 수 없으면 `git tag -a`까지 하고 `outputs/release-notes-v0.1.0.md` 파일을 릴리스 노트로 전달한다. Issue는 `docs/issues/<번호>.md`로 적어 두었다가 네트워크가 돌아오면 옮긴다.
- 3교시 시연 리허설에서 Ollama 서버나 모델이 없으면 `demo_outline.md`의 실패 대비 표대로 사전 실행 출력 JSON과 CLI 경로로 리허설한다. 모델을 내려받지 않는다.
- 템플릿에 적힌 모델 ID(`qwen3:0.6b`, `Qwen/Qwen2.5-0.5B-Instruct`)와 양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며, 그 값은 교재 검증용 기본값이다.

## 복사 후 변형

- `release_check.py`의 `README_SECTIONS`·`LICENSE_HINTS`·`CITATION_FIELDS`는 팀 규칙에 맞게 늘릴 수 있다. 줄이지는 않는다. 절 이름을 바꾸면 `README_TEMPLATE.md`의 단서 단어도 함께 바꾼다.
- `tag_notes.py`의 `build_notes()`에서 「실행하려면」 명령을 팀 프로젝트의 실제 실행 명령으로 바꾼다.
- `release_checklist.md`의 절 순서는 바꾸지 않는다. 해당 없는 항목은 「결과」에 "해당 없음"과 이유를 적는다.
- `triage_labels.md`의 라벨 5개는 줄이지 않는다. 팀 프로젝트에 필요한 라벨(예: `model`, `data`)은 추가한다.
- `demo_outline.md`의 4구간 시간은 합이 3분이 되게만 조정한다.
