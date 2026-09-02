# Smart I/O Controller — 2~3분 시연 개요

## 메타데이터

- 제출자 또는 정책 확정 시 팀명:
- 발표자:
- 개인/팀 정책 공지 위치: `COURSE_POLICY_TBD`
- commit SHA:
- protocol revision 또는 `TBD`:
- 보드 라벨:
- fake/real transport:

## 시연 타임라인

| 목표 시각 | 장면 | 말할 핵심 | 화면·로그 증거 |
|---:|---|---|---|
| 0:00~0:20 | 문제·구조 | 앱 한 문장, 학생/강의자 범위 | 아키텍처 한 장 |
| 0:20~1:00 | 연결 | scan 종료 조건, Connecting/Discovering/Ready | event trace |
| 1:00~1:40 | 출력 | 요청과 확인 가능 범위 | UI + event + 물리 관찰 |
| 1:40~2:20 | 입력 | notification, receivedAt, currentness | 입력 변화 로그 |
| 2:20~2:50 | 실패·복구 | disconnect, stale, reconnect, 새 epoch | 전후 상태 |
| 2:50~3:00 | 회고 | 알려진 제한과 commit | 제출 정보 |

## fallback

- 실물 장비 이상을 강의자에게 알린 시각:
- fake transport로 같은 계약을 재현할 시나리오:
- 실물에서 관찰하지 못한 부분을 꾸며 쓰지 않았는가: [ ]

## 개인 구술 연결

- 내가 설명할 함수/상태 전이:
- 실패 주입 전 예상:
- 실제 관찰과 차이:
- 다음 디버깅 단계:
