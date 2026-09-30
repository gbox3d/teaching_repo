# 3교시 — 첫 uv 실행과 첫 commit

[실습지 3교시](../../lab.md#3교시-실습--첫-uv-실행과-첫-commit)의 **실행용 제공 코드**다.
이 폴더 전체를 기존 개인 폴더의 `first_run`으로 복사한다. 숨김 파일도 포함한다.

| 실습 단계 | 파일 | 결과 |
|---|---|---|
| 문제 1 · 실행 | [sysinfo.py](sysinfo.py), [pyproject.toml](pyproject.toml) | `outputs/sysinfo.json` |
| 문제 1 · 설정 변경 | [.env.example](.env.example) | 모델 값과 출처 변화 |
| 문제 2 · commit | [.gitignore](.gitignore) | 환경·실제 설정 제외, 소스·lock 포함 |

```powershell
Set-Location C:\classwork\osa-week01\first_run
uv run python sysinfo.py
uv run python sysinfo.py --no-gpu
Copy-Item .env.example .env
```
`.env`의 모델 값을 바꾸고 재실행한다. 모델은 호출하지 않는다.
GPU가 없으면 `gpu.available: false`가 정상이고 나머지 보고서는 생성된다.
네트워크가 없을 때는 사전 준비한 Python·캐시로 실행한다. 자세한 대체 경로는 실습지의 힌트를 따른다.
첫 실행이 만든 `uv.lock`은 commit하고, `.venv`·`.env`·`outputs`는 제외한다.

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 보고서 JSON에 들어갈 항목 예상, `first_run` 확인 |
| uv 실행 | 4–14분 | `uv run python sysinfo.py`, `outputs/sysinfo.json`과 `.venv` 관찰 |
| 환경변수·경계 | 14–20분 | `.env`로 `OLLAMA_MODEL` 변경 후 재실행, `--no-gpu` 경계 경로 |
| 저장소·commit | 20–26분 | `git init`, 보고서 복사, `Add environment report` commit |
| 검증·기록 | 26–30분 | `git log --oneline -1`, `git status`, 미추적 항목 확인 |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
