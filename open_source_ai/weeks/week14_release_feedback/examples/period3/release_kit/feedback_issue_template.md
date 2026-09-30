# 피드백 Issue 양식

다른 팀 저장소에 Issue 를 남길 때 아래를 복사해 채운다. 저장소에 넣으려면 `.github/ISSUE_TEMPLATE/feedback.md` 로 저장한다.
좋은 Issue 의 기준은 하나다. **메인테이너가 내 PC 없이 같은 현상을 다시 볼 수 있는가.**

## 제목 규칙

- 재현 실패: `[repro] 단계 이름 — 한 줄 증상` (예: `[repro] uv sync --frozen — uv.lock 없음`)
- 제안: `[proposal] 한 줄 제안` (예: `[proposal] GPU 없는 PC 용 실행 절 추가`)
- 질문: `[question] 한 줄 질문`

## 본문

```markdown
## 종류
- [ ] 재현 실패(bug 또는 docs)  - [ ] 제안(enhancement)  - [ ] 질문(question)

## 환경
- OS:
- GPU 유무·VRAM:
- Ollama 실행 여부·모델:
- 대상 태그: v0.1.0
- 재현 시작 시각 / 걸린 시간:

## 실행한 명령 (그대로)
```powershell
git clone ...
uv sync --frozen
```

## 예상한 결과
README 의 어느 절을 보고 무엇을 기대했는가.

## 실제 결과 (전체 출력, 홈 경로·계정 이름은 지움)
```text
...
```

## README 에서 참고한 위치
절 제목 또는 줄 번호.

## 제안 (선택)
이렇게 바꾸면 처음 보는 사람이 덜 막힐 것 같다.
```

## 메인테이너가 정보를 더 요청할 때 쓰는 문장

```text
재현해 보려 합니다. 다음 세 가지를 추가로 알려 주시면 같은 환경을 만들 수 있습니다.
1. `uv run python --version` 과 `ollama --version` 출력
2. 실행한 명령 전체(복사·붙여넣기)
3. 오류가 난 시점의 전체 출력(개인 경로는 지워 주세요)
```
