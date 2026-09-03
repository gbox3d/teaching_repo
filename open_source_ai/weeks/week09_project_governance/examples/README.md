# 9주차 예제 — 팀 저장소 뼈대와 제안 도구

## 파일 구성

| 경로 | 역할 | 쓰는 교시 |
|---|---|---|
| `governance_survey_template.md` | 공개 프로젝트 2개 거버넌스 분석표 양식 | 1교시 |
| `milestone_plan_template.md` | 10~15주 역산 일정, 마일스톤 3개, Issue 표, 역할 표 | 3교시 |
| `proposal_tools/` | uv 프로젝트. 아래 스크립트 4개와 샘플 계획 | 1·2·3교시 |
| `proposal_tools/repo_health.py` | GitHub REST API로 커뮤니티 파일·릴리스 간격·상위 기여자 비율 수집 | 1교시 |
| `proposal_tools/vram_estimate.py` | 모델 후보의 추론 VRAM 추정과 12 GB 판정 | 2교시 |
| `proposal_tools/issue_plan_check.py` | `issue_plan.json`이 작고 검증 가능한 단위인지 검사 | 3교시 |
| `proposal_tools/issue_plan_push.py` | 계획의 라벨·마일스톤·Issue를 GitHub에 등록(토큰 필요, `--dry-run` 지원) | 3교시 |
| `proposal_tools/issue_plan.sample.json` | 마일스톤 3개·Issue 10개 샘플(수업 도우미 프로젝트) | 3교시 |
| `project_template/` | 팀 저장소 뼈대. 복사해서 팀 저장소의 첫 commit으로 쓴다 | 3교시 |
| `project_template/README.md` | 빈 구조(무엇·왜·설치·실행·예시·제한·라이선스·팀) | |
| `project_template/LICENSE_CHOICE.md` | MIT·Apache-2.0 선택 안내. 선택 후 삭제 | |
| `project_template/CONTRIBUTING.md` | 참여 흐름·리뷰 규칙·팀 규칙 3개 칸·의사결정 | |
| `project_template/CODE_OF_CONDUCT.md` | Contributor Covenant 채택 선언과 요약, 신고 경로 칸 | |
| `project_template/SOURCES.md` | 모델·데이터·코드·AI 도구 출처 표 | |
| `project_template/.github/` | 이슈 템플릿(feature·bug), PR 템플릿 | |
| `project_template/pyproject.toml` | uv 프로젝트 뼈대(`team-project` 엔트리포인트) | |
| `project_template/src/team_project/cli.py` | `doctor`(Ollama `/api/tags` 확인, 선택 `--chat-test`)·`version` | |
| `project_template/.env.example`, `.gitignore` | 환경변수 예시, 커밋 제외 목록 | |

## 실행 방법

원본을 훼손하지 않도록 개인 실습 폴더에 복사한 뒤 실행한다.

```powershell
Copy-Item -Recurse examples\proposal_tools C:\classwork\week09\proposal_tools
Set-Location C:\classwork\week09\proposal_tools
Copy-Item .env.example .env
uv run python repo_health.py
uv run python vram_estimate.py --candidate "qwen3:8b,8.2B,4" --candidate "qwen3:0.6b,0.6B,4"
uv run python issue_plan_check.py --plan issue_plan.sample.json
uv run python issue_plan_push.py --plan issue_plan.sample.json --repo team-a/repo --dry-run
```

첫 `uv run`이 `.venv`를 만들고 의존성(httpx, python-dotenv)을 설치한다. `uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

팀 저장소 뼈대:

```powershell
Copy-Item -Recurse examples\project_template C:\classwork\week09\team-repo
Set-Location C:\classwork\week09\team-repo
Copy-Item .env.example .env
uv run team-project doctor
uv run team-project doctor --chat-test
```

`doctor`는 `OLLAMA_HOST`의 `/api/tags`를 읽어 캐시된 모델 목록을 `outputs/doctor-*.json`에 남긴다. `--chat-test`는 `/api/chat`에 짧은 비스트리밍 요청을 한 번 보낸다(`think: false`, `num_predict: 32`).

모델 ID·양자화·용량은 환경 기준표에서 확정하며, `.env.example`의 값(`qwen3:8b`, `qwen3:0.6b` 등)은 교재 검증용 기본값이다.

## 관찰 지점

1. `repo_health.py`: `community_files` 여섯 항목이 브라우저의 Community Standards 체크와 같은가. `release_interval_days`가 사전 릴리스를 제외한 값인가. `top3_contribution_share`가 첫 페이지 기준 근사치라는 `note`.
2. `vram_estimate.py`: 같은 후보에 `--ctx`를 2048·8192·32768로 바꿨을 때 KV 캐시와 판정의 변화. 층 수·KV 헤드·헤드 차원을 주지 않으면 KV가 "미계산"으로 표시되는 것.
3. `issue_plan_check.py`: `done_when`을 비우거나 `days`를 5로 바꾸면 어떤 경고가 나오는가. 담당자 편차 경고의 기준(최대-최소 > 2).
4. `issue_plan_push.py --dry-run`: 등록될 마일스톤 마감일이 `--week10-date`를 줄 때만 계산되는 것. 실제 등록 시 422에서 담당자를 비우고 재시도하는 메시지.
5. `team-project doctor`: Ollama를 끈 상태의 한 줄 연결 실패 메시지와 종료 코드 1. 기본 모델이 캐시에 없을 때의 `[주의]` 줄.

## GPU 없을 때·네트워크 없을 때

- **GPU 없음**: 이번 주 예제는 GPU를 쓰지 않는다. `vram_estimate.py`의 `--vram-gb`를 실제 값(예: CPU 전용이면 시스템 RAM 기준)으로 바꿔 판정한다. `doctor --chat-test`는 소형 모델(`OLLAMA_MODEL=qwen3:0.6b`)로 바꿔 실행한다.
- **Ollama 미기동**: `doctor`는 연결 실패를 한 줄 메시지로 남기고 종료 코드 1을 돌려준다. 저장소 골격 검증에는 이 실패 경로도 증거가 된다.
- **네트워크 없음 또는 GitHub API 한도 소진**: `repo_health.py`는 저장소마다 실패 사유를 출력하고 JSON에 `error`를 남긴다. 분석표는 브라우저(또는 강의자가 배포한 캡처)로 채운다. `issue_plan_push.py`는 `--dry-run`으로 내용만 확인하고 Issue는 GitHub 웹에서 직접 만든다. `vram_estimate.py`·`issue_plan_check.py`는 네트워크가 필요 없다.
- **토큰 없음**: `repo_health.py`는 비인증으로 동작한다(한도가 낮으므로 두 저장소 정도만). `issue_plan_push.py`는 토큰 없이는 실행되지 않으며 웹 등록으로 대체한다.

## 복사 후 변형

- `proposal_tools/`의 스크립트는 그대로 두고 인자·`.env`·계획 JSON만 바꾼다. 스크립트를 고쳤다면 어떤 줄을 왜 바꿨는지 실습 기록에 적는다.
- `project_template/`는 팀 저장소로 옮긴 뒤 자유롭게 바꾼다. 패키지 이름을 바꿀 때는 `src/` 폴더 이름, `pyproject.toml`의 `name`·`[project.scripts]`·`[tool.hatch.build.targets.wheel]`, `cli.py`의 import를 함께 바꾸고 `uv sync`를 다시 실행한다.
- `LICENSE_CHOICE.md`는 선택이 끝나면 삭제하고 `LICENSE` 파일로 대체한다.
- `outputs/`와 `.env`는 어느 폴더에서도 커밋하지 않는다.
