# proposal_tools — 9주차 제안·거버넌스 도구

상위 [examples/README.md](../README.md)가 주 안내다. 이 파일은 실행 요약이다.

```powershell
Copy-Item .env.example .env
uv run python repo_health.py                                   # 1교시 · 저장소 건강 지표
uv run python vram_estimate.py --candidate "qwen3:8b,8.2B,4"   # 2교시 · VRAM 추정
uv run python issue_plan_check.py --plan issue_plan.sample.json # 3교시 · 이슈 계획 검사
uv run python issue_plan_push.py --plan issue_plan.json --repo team-a/repo --dry-run
```

- 결과는 `outputs/`에 JSON·Markdown으로 남는다. `outputs/`와 `.env`는 커밋하지 않는다.
- `uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
- GitHub 토큰은 `.env`의 `GITHUB_TOKEN`에만 둔다.
