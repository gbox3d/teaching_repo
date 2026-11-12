# ci_lab — 테스트·CI·보안 점검이 붙은 최소 AI 서비스

13주차 예제 uv 프로젝트다. 12주차 서비스와 같은 구조(스키마·서비스·HTTP 계층)를 테스트하기 좋게 줄여 다시 썼다 — 요청 필드·예외 이름·상태 코드는 12주차와 다르다.
자세한 실행 방법과 관찰 지점은 상위 [`../README.md`](../README.md)에 있다.

## 빠른 실행

```powershell
Copy-Item .env.example .env
uv sync                                  # dev 그룹(pytest, ruff, pip-audit)까지 설치
uv run pytest -q                         # 모델 서버 없이 도는 테스트
uv run ruff check .
uv run ruff format --check .
```

## 구성

| 경로 | 역할 |
|---|---|
| `app/schemas.py` | 요청·응답 스키마(pydantic) |
| `app/ollama_client.py` | `OllamaClient` 프로토콜 + 실제 HTTP 클라이언트 + 예외 3종 |
| `app/service.py` | 클라이언트를 주입받는 서비스 로직 |
| `app/main.py` | FastAPI 앱. `get_service` 가 주입 지점, 예외→503·404·502 |
| `tests/conftest.py` | `FakeOllamaClient`, `service`·`make_service`·`api_for` fixture |
| `tests/test_schemas.py`, `test_service.py`, `test_api.py` | 스키마·서비스·HTTP 계층 테스트 |
| `tests/test_integration.py` | 실제 Ollama 가 필요한 테스트(`integration` 마커, 기본 제외) |
| `.github/workflows/ci.yml` | GitHub Actions: setup-uv → sync → ruff → pytest, 별도 audit 잡 |
| `audit_report.py` | `uv export` → `pip-audit` → `outputs/audit-*.md` |
| `security_check.ps1` | 토큰 패턴·`.env` 추적·pickle 모델 파일·`trust_remote_code` 점검 |
| `REVIEW_CHECKLIST.md` | 교차 코드리뷰 항목과 코멘트 양식 |

- 모델 ID·주소는 환경변수(`.env.example` 참고)로 읽는다. 기본값은 교재 검증용이며 실제 값은 학기별 환경 기준표에서 확정한다.
- `uv.lock` 은 이 폴더에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock` 으로 생성해 커밋한다.
- 앱을 직접 띄우려면 `uv run uvicorn app.main:app --port 8000` 이다(테스트에는 필요 없다).
