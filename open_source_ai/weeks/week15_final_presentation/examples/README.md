# 15주차 예제 — 발표·검증·회고 템플릿과 릴리스 검증 도구

## 파일 구성

| 파일 | 역할 | 쓰는 교시 |
|---|---|---|
| `demo_outline.md` | 시연 3분 + 질의 2분 개요, 예상 질문, 장애 대체(fallback) 계획 | 1교시 |
| `question_cards.md` | 평가자·청중이 던지는 질문 카드 20개와 답하는 순서 | 1교시 |
| `presentation_log_template.md` | 청중용 발표 기록표(팀마다 한 행: 문제·실행된 것·한계·재현 절차·질의·장애, 점수 칸 없음)와 2교시 검증 대상 메모 | 1교시 |
| `peer_feedback_form.md` | 동료 피드백 양식(발표 관찰 → 재현 결과 → 제안) | 1·2·3교시 |
| `reviewer_checklist.md` | 교차 재현 검증 체크리스트(clone → `uv sync --frozen` → 실행 → 테스트 → 문서·라이선스·출처 → 비밀)와 재현 실패 Issue 양식 | 2교시 |
| `release_verify/` | 릴리스 패키지 검증 uv 프로젝트: `verify_release.py`, `checks.py`, `cross_review.ps1`, `.env.example` | 2·3교시 |
| `retrospective_template.md` | 개인 회고 양식(잘된 것·어려웠던 것·다음에 다르게·이후에 할 일) | 3교시 |
| `submission_checklist.md` | 4차 종합과제 최종 제출 체크리스트와 제출 정보 양식 | 3교시 |

템플릿은 개인 실습 폴더에 복사해 채운다. 원본은 수정하지 않고, 예시 문장을 그대로 제출하지 않는다.

## 실행 방법 (PowerShell)

### 복사와 준비

```powershell
Copy-Item -Recurse <교재 경로>\week15_final_presentation\examples .\week15-practice
Set-Location .\week15-practice\release_verify
Copy-Item .env.example .env
uv sync
```

`uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

### 교차 재현 검증(2교시) — 한 번에

```powershell
.\cross_review.ps1 -RepoUrl https://github.com/<org>/<repo>.git -Team team-b -Tag v0.1.0
```

clone → 태그 checkout → `uv sync --frozen` → `uv run --frozen pytest -q` → `verify_release.py` 순으로 실행하고 `outputs\cross-review-team-b-<시각>.log`에 남긴다. pytest에도 `--frozen`을 붙이는 이유는 lock이 없는 저장소에서 uv가 clone 폴더에 새 `uv.lock`을 만들어 "재현"이 "새 설치"로 바뀌는 것을 막기 위해서다. README 절차대로 핵심 기능을 실제로 실행하는 단계는 자동화하지 않으므로 직접 한다.

`uv sync --frozen`과 `uv run --frozen pytest`는 대상 저장소의 코드를 이 PC에서 실행한다(빌드 백엔드·`conftest.py`·테스트). 수업에서 서로 공개한 팀 저장소에만 이 스크립트를 쓰고, 출처를 모르는 저장소는 파일과 git 상태만 읽는 `verify_release.py`로만 검사한다.

### 교차 재현 검증 — 수동

```powershell
git clone <URL> .\review\team-b
git -C .\review\team-b checkout v0.1.0
Set-Location .\review\team-b
uv sync --frozen
uv run pytest -q
Set-Location ..\..
uv run python verify_release.py --repo .\review\team-b --team team-b
```

### 자기 저장소 점검(3교시)

```powershell
uv run python verify_release.py --repo <팀 저장소 경로> --team team-a --check-ollama
uv run python verify_release.py --repo <팀 저장소 경로> --team team-a --health-url http://localhost:8000/health
```

`--check-ollama`는 `OLLAMA_HOST`(기본 `http://localhost:11434`)의 `/api/tags`를 GET 해서 대상 저장소 `.env.example`의 `OLLAMA_MODEL`이 캐시되어 있는지 본다. `--health-url`은 12주차 서비스를 켠 뒤 `/health`를 확인한다. 둘 다 생략하면 네트워크 없이 동작한다.

## 관찰 지점

1. `outputs/verify-<팀>-<시각>.md`의 PASS/WARN/FAIL 분포와 각 근거. WARN은 도구가 판단을 미룬 항목이다.
2. `uv sync --frozen`이 실패할 때의 메시지: `uv.lock` 불일치·누락(릴리스 결함)인지, 네트워크·캐시(환경 문제)인지. `verify_release.py`가 `uv.lock`을 `존재하지만 git 추적 안 됨`으로 표시하면 검증 중 새로 생긴 파일이며 릴리스에는 없는 것이다.
3. README 절차대로 실행한 출력이 README의 예시 출력과 같은 형태인지.
4. 비밀 패턴 FAIL이 자리표시자(`hf_xxxx…`)인지 실제 값인지. 실제 값이면 즉시 대상 팀에 알린다.
5. `git describe --tags --exact-match`가 가리키는 태그와 제출 commit id가 같은지.

## GPU 없을 때·네트워크 없을 때 대체 경로

- 검증 도구(`verify_release.py`, `checks.py`)는 GPU·모델 없이 동작한다.
- 네트워크가 없으면 `-RepoUrl`에 USB나 공유 폴더의 로컬 경로를 준다(`-RepoUrl D:\repos\team-b`). uv 캐시에 패키지가 있으면 `uv sync --frozen`이 오프라인으로도 성공한다. `--check-ollama`·`--health-url`은 생략한다.
- 대상 팀의 모델이 이 PC에 없으면 내려받지 않는다. "환경 문제"로 기록하고 README에 모델 ID·용량·다운로드 방법이 적혀 있는지만 판단한다. 팀 README가 CPU 대체(`OLLAMA_MODEL=qwen3:0.6b` 등)를 허용하고 그 모델이 캐시되어 있으면 대체 실행한다.
- Ollama 서버가 꺼져 있으면 실행 단계는 "연결 실패 메시지가 사람이 읽을 수 있는가"를 확인하는 것으로 대체하고 그렇게 기록한다.
- 모델 ID·양자화·용량은 [학기별 환경 기준표](../../../../environment_baseline_template.md)에서 확정하며 `.env.example`의 값은 교재 검증용 기본값이다.

## 복사 후 변형

- `checks.py`의 `REQUIRED_FILES`·`OPTIONAL_FILES`·`SECRET_PATTERNS`는 팀 규칙에 맞게 늘릴 수 있다. 줄이지는 않는다.
- `reviewer_checklist.md`의 단계는 순서를 바꾸지 않는다. 단계를 건너뛰었으면 "해당 없음"과 이유를 적는다.
- `question_cards.md`에 팀 프로젝트 특성에 맞는 질문을 추가해 리허설에 쓴다.
