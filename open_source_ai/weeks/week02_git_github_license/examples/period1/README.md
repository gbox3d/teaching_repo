# 1교시 — 원격 연결과 충돌 1회 해결

[실습지 1교시](../../lab.md#1교시-실습--원격-연결과-충돌-1회-해결)에서 사용하는 **시연·확장 도구**다.
기본 실습은 개인 저장소에서 원격 연결→두 브랜치 수정→충돌 해결 순서로 직접 진행한다.
[merge_conflict_demo.ps1](merge_conflict_demo.ps1)은 문제 2와 같은 충돌을 별도 연습 저장소에 재현한다.

교재 밖의 빈 연습 폴더로 스크립트를 복사한 뒤:
```powershell
powershell -ExecutionPolicy Bypass -File .\merge_conflict_demo.ps1
Set-Location .\conflict-demo
```
`conflict-demo` 저장소에 `UU README.md`와 충돌 마커가 남는다.
해결 순서는 실습지 문제 2를 따르고 마지막 `git status`와 그래프를 기록한다.
네트워크가 없으면 실습지의 로컬 bare 원격 대체 경로로 진행한다.
Python·GPU는 사용하지 않는다.

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | GitHub 빈 저장소 생성, 예상표 작성 |
| 원격 연결 | 5–12분 | `remote add`, 첫 `push -u`, 추적 상태 확인 |
| 충돌 재현 | 12–20분 | `feature/readme`와 `main`에서 같은 줄 수정, merge |
| 충돌 해결 | 20–25분 | 마커 읽기, 결과 문장 작성, merge commit, push |
| 검증·기록 | 25–30분 | graph 출력, 상태 문장 기록 |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
