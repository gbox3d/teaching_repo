# 14주차 — BLE 입력 알림과 Smart I/O 통합 프로젝트

## 이번 주 질문

입력 notification이 끊기거나 다시 연결되어도, 앱이 오래된 값을 현재 상태처럼 보이지 않게 하면서 출력 제어와 하나의 신뢰 가능한 화면으로 통합하려면 어떻게 해야 할까?

## 측정 가능한 학습 목표

- GATT notification 구독과 일반 read의 차이를 사건 흐름으로 설명한다.
- 제공 BLE 추상화의 입력 `Flow`를 lifecycle-aware하게 수집하고 XML View에 최신 상태·수신 시각을 표시한다.
- `Idle → Scanning → Connecting → Discovering → Ready → Disconnected/Error` 상태에 입력 구독·출력 제어 가능 조건을 결합한다.
- fake와 real transport에서 정상 입력, 빠른 반복, disconnect, reconnect, timeout을 재현하고 오래된 세션 사건을 배제한다.
- 2~3분 안에 출력·입력·실패 복구를 재현하고 설계 선택을 개인 언어로 설명한다.

## 1일차 — 입력 notification과 재연결

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | notification 구독, 입력 상태 동기화, lifecycle 수집, disconnect/reconnect 정책 |
| 직접 실습 60분 | fake 입력 stream, 반복·끊김·오래된 사건 검증, 통합 상태 화면 구현 |

## 2일차 — 통합·리허설·평가 증거

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | 통합 시나리오, 평가 루브릭, 장애 대응, 개인 구술 증거와 제출 점검 |
| 직접 실습 60분 | real 보드 통합, 정상·실패 리허설/시연, 보고서·체크리스트 증거 완성 |

두 수업일 모두 정확히 `30분 설명·시연 + 60분 실습`이다. 실제 평가 순서·시연 인원 배치는 분반 공지에 따른다.

## 선수 지식과 준비물

- 12주차 연결 상태 기계와 13주차 출력 명령 상태
- 제공 `BleGateway`, fake transport, 입력 관찰 추상화
- 강의자가 펌웨어를 설치한 Tenstar ESP32-C3와 수업용 입력·출력 회로
- service/characteristic UUID, GPIO, 메시지·notification payload는 확정 전까지 `TBD`
- 학생은 펌웨어 코딩·빌드·플래싱과 보드 회로 변경을 하지 않는다.

## 프로젝트 운영 정책 — 확정 필요

> **COURSE_POLICY_TBD:** 최종 제출 단위를 개인으로 할지 2인 팀으로 할지는 이 문서에서 확정하지 않는다. 강의자의 공식 수업 공지가 권위 원본이다. 팀 제출이 허용되더라도 각 학생의 코드 흐름 설명, 상태 예측, 장애 대응은 **개인 구술 증거**로 별도 기록한다. 팀 점수 공유·차등 적용 방식도 공식 공지 전에는 추정하지 않는다.

## 평가와 자료

- 총 20점 = **발표 12점 + 보고서 8점**
- [프로젝트 명세](project_brief.md)
- [20점 루브릭](rubric.md)
- [Marp 슬라이드](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [60분 실습지](lab.md)
- [시연·보고서·제출 템플릿](examples/README.md)

## 완료 증거

- fake/real의 입력 notification과 출력 제어 통합 trace
- 정상 입력, 빠른 반복, disconnect/reconnect, timeout 검증표
- disconnect 동안 입력을 `Unknown/Stale`로 표시하고 새 세션 사건 뒤 현재화한 증거
- 2~3분 시연 기록과 개인 구술 질문 응답
- rubric 자기 점검, 보고서, 제출 체크리스트, commit SHA

## 다음 주

[15주차 — 기말 개인 실기](../week15_final_exam/README.md)에서 공개 starter를 읽고 Android·BLE 상태와 오류 대응을 개인 구현·시연으로 확인한다.

## 공식 참고 자료

- [Transfer BLE data — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [Bluetooth LE in the background — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/background)
- [Lifecycle-aware coroutines for Views — Android Developers](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
- [Bluetooth permissions — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [Kotlin Flow — Kotlin Documentation](https://kotlinlang.org/docs/flow.html)
