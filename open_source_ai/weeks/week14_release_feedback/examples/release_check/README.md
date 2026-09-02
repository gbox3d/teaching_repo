# release_check — 릴리스 준비 점검·릴리스 노트 도구

상위 [`../README.md`](../README.md)가 실행 방법과 관찰 지점을 설명한다. 이 파일은 요약이다.

| 파일 | 역할 |
|---|---|
| `release_check.py` | 저장소 폴더를 읽기 전용으로 점검하고 `outputs/release-check-*.json`에 기록 |
| `tag_notes.py` | CHANGELOG 절을 릴리스 노트로 뽑고, `--promote`로 `[Unreleased]`를 버전 절로 승격 |
| `.env.example` | `RELEASE_REPO`·`RELEASE_TAG`·`RELEASE_VERSION` 견본 |

```powershell
uv sync
uv run python release_check.py --repo C:\classwork\team-a-repo
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0
```

- 모델·GPU·네트워크가 필요 없다.
- `uv.lock`은 이 저장소에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
