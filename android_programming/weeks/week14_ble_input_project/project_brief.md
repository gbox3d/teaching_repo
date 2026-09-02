# 14주차 2차 과제 명세 — Smart I/O Controller

## 과제 목표

사전 플래시된 Tenstar ESP32-C3와 제공 BLE 추상화를 사용해 다음 한 줄의 Android 앱을 완성한다.

> 장치를 찾아 연결하고, 디지털 출력을 제어하며, 디지털 입력 notification을 표시하고, 권한·미발견·끊김·timeout에서 복구하는 Kotlin/XML View 앱

## 점수

- 발표: 12점
- 보고서: 8점
- 합계: 20점

세부 기준은 [rubric.md](rubric.md)를 따른다.

## 제출 단위 정책 — 미확정

> **COURSE_POLICY_TBD:** 개인 과제 또는 2인 팀 과제 여부, 팀원 간 산출물 점수 적용 방식은 강의자 공식 공지로 확정한다. 이 명세는 어느 쪽도 임의 선택하지 않는다.

정책 확정과 무관하게 다음은 유지한다.

- 각 학생의 개인 구술 설명을 별도 기록한다.
- 각 학생이 상태 예측과 장애 대응 질문에 직접 답한다.
- 팀 제출이 허용되면 보고서에 역할·commit·검증 기여를 사실대로 적는다.
- 같은 점수 또는 차등 점수 적용은 공식 공지 없이는 추정하지 않는다.

## 필수 기능

1. 버전 인식 권한 안내와 거절 복구
2. 제한 시간 scan과 수업용 장치 식별
3. `Idle → Scanning → Connecting → Discovering → Ready → Disconnected/Error` 상태 표시
4. 필수 GATT 계약과 입력 구독 성공 뒤 Ready 판정
5. Ready에서 허용 출력 1개 이상 제어
6. 입력 1개 이상의 notification과 수신 시각/currentness 표시
7. 장치 미발견, 권한 거절, disconnect, timeout의 사용자 안내와 복구
8. fake/real transport 전환과 같은 UI·상태 계약

## 기술·안전 범위

- Android: Kotlin + XML View, ViewModel, coroutine/Flow
- 장치: 강의자가 펌웨어를 설치한 Tenstar ESP32-C3
- 학생 범위: Android 앱, 상태 관리, 오류 UX, 테스트, 설명
- 제외: ESP32-C3 펌웨어 코딩·빌드·플래싱, 회로 변경, Wi-Fi/cloud 기본 기능
- 보드 이상은 강의자에게 교환 요청하고 학생이 복구 이미지를 쓰지 않는다.

## Protocol freeze gate

다음 값은 강의자 확정본이 배포되기 전까지 `TBD — instructor pin required`다.

- service UUID와 output/input characteristic UUID
- 허용 GPIO 또는 논리 채널 매핑
- 명령·응답·notification payload encoding
- ack/readback 의미, timeout과 retry 기준
- advertising 장치 식별 규칙

확정 전에는 임의 값을 코드·보고서·슬라이드에 넣지 않는다. 확정본 배포 후에는 출처 파일과 revision을 보고서에 기록한다.

## 필수 시연 시나리오

1. 권한 상태 확인 후 대상 scan
2. Connecting·Discovering을 거쳐 Ready
3. 출력 1회 변경과 확인 가능한 증거 설명
4. 입력 변화 notification과 수신 시각 표시
5. 보드 전원 off 또는 제공 failure control로 disconnect
6. 출력 비활성·입력 stale 확인
7. 사용자 행동으로 reconnect 후 새 입력 current 확인

목표 길이는 2~3분이다. 실제 발표 시간·순서·영상 허용 정책은 수업 공지를 따른다.

## 필수 테스트

| 종류 | 최소 시나리오 |
|---|---|
| 정상 | fake Ready, real Ready, output, input notification |
| 경계 | devices=0, 동일 입력 반복, 같은 출력 level 요청 |
| 실패 | 권한 거절, discovery/subscription mismatch, timeout, disconnect |
| 복구 | 권한 안내, 새 scan, reconnect, 새 epoch input |

## 제출물

- Android source와 실행 안내
- 프로토콜 revision 또는 `TBD` 표
- 정상·경계·실패·복구 테스트 증거
- 2~3분 demo 자료 또는 수업 공지에 따른 현장 시연
- 보고서 PDF/문서(형식은 LMS 공지 우선)
- 개인 구술 기록과 역할/commit 근거(팀 허용 시에도 개인별)
- 최종 commit SHA와 제출 체크리스트

실제 LMS 위치, 마감, 파일명, 지각 정책은 이 문서가 추정하지 않으며 공식 공지를 따른다.

## 완료 정의

- 필수 기능이 fake에서 모두 재현된다.
- 실물 이용 가능 시 real 정상과 disconnect/reconnect가 재현된다.
- 장비 장애 시 fake 증거와 장비 이상 기록으로 앱·장비 문제를 분리한다.
- 보고서 주장마다 화면·event log·테스트 중 하나 이상의 근거가 연결된다.
- 개인 구술에서 현재 상태, 다음 사건, 실패 원인, 복구 행동을 설명한다.
