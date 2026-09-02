# release_verify — 릴리스 패키지 검증 도구

15주차 2교시 교차 재현 검증과 3교시 최종 제출 자가 점검에 쓰는 uv 프로젝트다. 자세한 실행 방법과 관찰 지점은 상위 [examples/README.md](../README.md)를 본다.

| 파일 | 역할 |
|---|---|
| `verify_release.py` | 저장소 폴더를 검사해 `outputs/verify-<팀>-<시각>.md`·`.json` 보고서를 만든다 |
| `checks.py` | 필수 파일·`.gitignore`·git 태그·README 절·비밀 패턴 검사 함수 |
| `cross_review.ps1` | clone → 태그 checkout → `uv sync --frozen` → pytest → `verify_release.py`를 한 번에 실행하고 로그를 남긴다 |
| `.env.example` | `OLLAMA_HOST`, `SERVICE_HEALTH_URL`, `REVIEWER` 예시 |

```powershell
uv sync
uv run python verify_release.py --repo <검증할 저장소 폴더> --team team-a
```

- 모델·GPU 없이 실행된다. `--check-ollama`와 `--health-url`만 네트워크(로컬 서버)를 쓴다.
- `uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
- 도구는 사람의 판단을 대신하지 않는다. WARN은 직접 읽고 판단하고, FAIL도 원인을 환경 문제·릴리스 결함·설계 한계로 구분해 기록한다.
