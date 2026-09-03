# 13주차 — 테스트·CI·보안·코드리뷰

## 이번 주 질문

> 모델 호출이 들어간 코드를 어떻게 자동으로 검사하고, 다른 사람의 변경을 어떻게 안전하게 받아들이는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. pytest의 발견 규칙·`assert`·fixture·parametrize로 스키마와 서비스 로직의 단위 테스트를 작성한다.
2. 의존성 주입으로 모델 호출을 격리해, Ollama 서버 없이 정상·오류 경로(422·503·404·502)를 자동으로 검사한다.
3. 실제 서버가 필요한 느린 테스트를 마커로 분리하고, ruff로 lint·format 검사를 통과시킨다.
4. GitHub Actions workflow(`on`·`jobs`·`steps`, `setup-uv`, 캐시)를 작성해 PR 상태 체크의 초록불·빨간불을 만들고 실패 로그에서 첫 오류를 찾는다.
5. `uv export`→`pip-audit`으로 의존성 취약점을 감사하고, 비밀 패턴·pickle 모델 파일·`trust_remote_code`를 점검 스크립트로 찾아 조치를 기록한다.
6. 체크리스트에 따라 다른 팀의 PR을 근거→문제→제안 구조로 리뷰하고 판정한다.

## 누적 결과물

이번 주 실습은 **4차 종합과제(15주)** "최종 오픈소스 릴리스 패키지"의 품질·보안 부분을 채운다. 수업 시간에는 예제 복사본 `ci_lab/`과 그것을 push한 연습 저장소 `week13-ci-lab`에서 테스트·workflow·감사·보안 점검을 만든다. 여기서 만든 `tests/`와 `.github/workflows/ci.yml`을 팀 저장소로 옮겨(요청 필드와 상태 코드는 팀 코드에 맞춘다) 초록불을 만드는 것이 다음 수업 전까지 끝내야 할 일이다. 14주차 `v0.1.0` 릴리스와 4차 과제의 `uv run pytest -q` 통과가 그 상태를 전제로 하기 때문이다. 12주차 3차 과제의 서비스 베타가 테스트 대상이다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | pytest 구조(발견·assert·fixture·parametrize), 모델 호출 격리(가짜 클라이언트·의존성 주입), 단위 vs 통합과 느린 테스트 표시, ruff(lint·format) | 가짜 클라이언트로 서비스 테스트 만들기 | `uv run pytest` 출력(추가한 테스트 3개 포함 통과), `ruff check`·`ruff format --check` 통과 출력 |
| 2교시 | GitHub Actions workflow 구조(`on`·`jobs`·`steps`), `astral-sh/setup-uv`와 캐시, PR 상태 체크·branch protection, 실패 로그 읽기 | GitHub Actions로 초록불과 빨간불 만들기 | Actions 실행 URL(성공 1·실패 1), 실패한 step 이름과 첫 오류 줄, 수정 commit |
| 3교시 | 공급망 보안(`pip-audit`, lock 검증, 타이포스쿼팅), 비밀 유출 방지(gitignore·secret scanning·pre-commit), 모델 파일 안전(pickle vs safetensors, `trust_remote_code`), 교차 코드리뷰 체크리스트 | 의존성 감사와 비밀 검색, 교차 리뷰 | `outputs/audit-*.md`, `outputs/security-*.md`(깨끗한 결과 + 심어 둔 문제를 잡은 결과), 리뷰 코멘트 URL |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell (1주차 `env_check.md`로 확인한 상태). Ollama는 통합 테스트에만 필요하며 없어도 이번 주 실습은 진행된다.
- GitHub 계정(2주차)과 팀 저장소(9주차). 2교시는 새 저장소를 만들어 push하므로 로그인 상태를 확인한다.
- 12주차 서비스 코드(`ai_service/`)와 3차 과제 저장소. 예제 `ci_lab/`은 같은 구조를 줄여 다시 쓴 것이므로 12주차 코드가 없어도 실습은 가능하다(요청 필드·예외 이름·상태 코드는 12주차와 다르다).
- 네트워크: 2교시 GitHub Actions와 3교시 `pip-audit`은 네트워크가 필요하다. 없을 때의 대체 경로는 [실행 예제](examples/README.md)에 있다.
- 수업 전 `uv sync`를 한 번 실행해 패키지 캐시를 채워 둔다. 기본 모델(`OLLAMA_MODEL`)은 이미 캐시되어 있으며 실습 시간에 모델을 내려받지 않는다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 전화번호, 비밀번호나 API 토큰은 실습 파일과 공개 저장소에 넣지 않는다. 3교시에 심어 두는 "가짜 토큰"은 커밋하지 않고 검출 확인 뒤 즉시 삭제한다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 가짜 클라이언트 테스트 + GitHub Actions workflow + 감사·보안 점검 스크립트 + 리뷰 체크리스트
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 테스트를 쓰기 전에 "이 테스트가 실패하면 무엇이 잘못된 것인가"를 한 문장으로 적는다. 그 문장이 안 나오면 테스트가 아니라 실행 기록이다.
2. 정상 경로 테스트를 먼저 통과시키고, 12주차에서 손으로 재현했던 실패 경로(연결 실패·모델 없음·잘못된 요청)를 가짜 클라이언트의 `fail_with`로 옮긴다.
3. CI는 로컬에서 통과한 것만 push한다. 빨간불은 **일부러** 한 번 만들어 로그 읽는 순서를 몸에 익힌다.
4. 감사·보안 점검 결과는 캡처 대신 `outputs/`의 Markdown을 증거로 쓴다. 찾은 비밀의 내용은 어디에도 다시 적지 않는다.
5. 리뷰 코멘트는 근거(파일·줄·로그)가 없으면 남기지 않는다. 취향은 `nit`로 표시하고 판정에 넣지 않는다.

## 완료 기준

- [ ] 예제 복사본에서 `uv run pytest -q`가 통과하고, 직접 추가한 테스트 3개(공백 prompt 거절·system 프롬프트 순서·모델 없음→404)가 포함되어 있다.
- [ ] `uv run ruff check .`와 `uv run ruff format --check .`가 통과하며, 일부러 만든 lint 오류를 `--fix`로 고친 기록이 있다.
- [ ] `uv run pytest -m integration`이 `RUN_INTEGRATION` 유무에 따라 `skipped` 또는 실제 실행으로 갈리는 것을 확인했다.
- [ ] GitHub 저장소의 Actions에 성공 실행 1건과 실패 실행 1건이 있고, 실패한 step 이름과 첫 오류 줄을 기록했다.
- [ ] PR이 초록불 상태로 merge되었다.
- [ ] `outputs/audit-*.md`에 검사한 패키지 수·취약점 수와 다음 행동이 있다(네트워크가 없으면 `--sample` 결과와 그 사실).
- [ ] `security_check.ps1`이 깨끗한 저장소에서 문제 0건, 심어 둔 `.env` 스테이지·가짜 토큰·`.pt` 파일을 모두 잡았고, 심은 것을 전부 제거했다.
- [ ] 다른 팀 PR에 체크리스트 기반 코멘트 2개 이상과 판정을 남기고 코멘트 URL을 기록했다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `uv run pytest -q` 최종 출력과 추가한 테스트 3개의 commit id
2. `ruff check`·`ruff format --check` 통과 출력, 일부러 만든 오류와 `--fix` 전후 diff 요약
3. Actions 실행 URL 2개(성공·실패), 실패 step 이름·첫 오류 줄·수정 commit id, merge된 PR URL
4. `evidence/week13/audit-*.md`, `evidence/week13/security-*.md`(깨끗한 결과 1 + 문제 검출 결과 1)
5. `reviews/week13.md`: 리뷰한 PR URL, 판정, 코멘트 URL, 받은 응답 요약

터미널 출력과 Markdown에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보와 토큰 패턴이 없는지 `security_check.ps1`로 다시 확인한다.

## 다음 주 연결

14주차 `week14_release_feedback`에서는 CI가 초록불인 팀 저장소를 `v0.1.0`으로 릴리스한다. README·LICENSE·CHANGELOG·Model Card를 점검표로 보완하고, 다른 팀이 README만 보고 재현하도록 한 뒤 피드백 Issue를 받는다. 이번 주 `REVIEW_CHECKLIST.md`의 보안·출처 항목이 릴리스 점검표에 그대로 들어간다. 다음 수업 전에 이번 주 `tests/`와 `.github/workflows/ci.yml`을 팀 저장소로 옮기고 Actions가 초록불인지 확인한다. 옮기지 못한 팀은 그 사실과 남은 작업을 팀 저장소 Issue로 남긴다.

## 참고 자료

- [pytest 공식 문서](https://docs.pytest.org/)
- [Ruff 공식 문서](https://docs.astral.sh/ruff/)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [astral-sh/setup-uv 액션 README](https://github.com/astral-sh/setup-uv)
- [pip-audit (PyPI)](https://pypi.org/project/pip-audit/)
- [safetensors 공식 문서](https://huggingface.co/docs/safetensors/)
- [GitHub secret scanning 문서](https://docs.github.com/en/code-security/secret-scanning)
