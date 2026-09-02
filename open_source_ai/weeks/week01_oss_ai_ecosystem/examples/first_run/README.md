# first_run — 첫 uv 실행

3주차에 uv 프로젝트를 본격적으로 다루기 전에 "복사 → `uv run` → 결과 파일 → commit" 한 바퀴를 돌려 보는 최소 예제다. 실행 방법·관찰 지점·대체 경로는 상위 [`../README.md`](../README.md)가 기준이다.

```powershell
uv run python sysinfo.py
uv run python sysinfo.py --no-gpu
uv run python sysinfo.py --print
```

- 결과: `outputs/sysinfo.json` (OS·CPU·RAM·디스크·GPU·Python·환경변수)
- 설정: `.env.example`을 `.env`로 복사해 `OLLAMA_HOST`, `OLLAMA_MODEL`을 바꾼다. `.env`는 커밋하지 않는다.
- 의존성: `python-dotenv` 하나. 없어도 실행되며 `.env`만 읽지 않는다.
- `uv.lock`은 아직 없다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
