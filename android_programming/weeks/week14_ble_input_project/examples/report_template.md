# Smart I/O Controller — 보고서 템플릿

## 1. 제출 정보

- 제출자:
- 개인/팀 운영 공지 위치: `COURSE_POLICY_TBD`
- 팀 허용 시 역할과 commit 근거:
- 최종 commit SHA:
- 실행 환경:
- protocol revision 또는 `TBD`:

## 2. 문제와 범위

- 해결하려는 사용자 시나리오:
- Android에서 구현한 범위:
- 제공받은 BLE abstraction/firmware:
- 제외한 firmware·회로·cloud 범위:

## 3. 구조와 상태

`UI → ViewModel/use case → BLE abstraction → fake/real transport → ESP32-C3` 그림을 넣는다.

| 현재 상태 | 진입 사건 | 허용 행동 | 실패/복구 |
|---|---|---|---|
| Idle |  |  |  |
| Scanning |  |  |  |
| Connecting |  |  |  |
| Discovering |  |  |  |
| Ready |  |  |  |
| Disconnected/Error |  |  |  |

## 4. 입출력 계약

| 항목 | 확정값/`TBD` | 출처 revision | 앱에서 사용한 위치 |
|---|---|---|---|
| UUID |  |  |  |
| logical channel/GPIO |  |  |  |
| command encoding |  |  |  |
| notification encoding |  |  |  |
| ack/readback |  |  |  |

## 5. 구현 증거

- 출력 요청/확인 범위:
- 입력 notification/currentness:
- lifecycle-aware 수집:
- disconnect/reconnect:

각 주장에 화면, event log, 파일/함수 중 하나를 연결한다.

## 6. 테스트 매트릭스

| 종류 | 조건/입력 | 실행 전 예상 | 실제 | 통과 여부 | 증거 |
|---|---|---|---|---|---|
| 정상 |  |  |  |  |  |
| 경계 |  |  |  |  |  |
| 실패 |  |  |  |  |  |
| 복구 |  |  |  |  |  |

## 7. 재현 방법

1. `[실행 단계 1]`
2. `[실행 단계 2]`
3. `[실행 단계 3]`

비밀·개인 기기 주소·학생 개인정보를 넣지 않는다. 실제 SDK/도구 버전은 pinned inventory 값만 기록한다.

## 8. 알려진 제한과 회고

- 현재 제한:
- fake와 real의 차이:
- 내 예측이 틀린 지점과 수정한 모델:
- 다음 개선 한 가지:

## 9. 공식 출처

사용한 Android Developers와 Kotlin 공식 문서 링크, 접근일, 적용한 판단을 적는다.
