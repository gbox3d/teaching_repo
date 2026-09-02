---
marp: true
theme: default
paginate: true
title: 13주차 BLE 출력 제어와 명령 확인
---

# 13주차

## BLE 출력 제어와 명령 확인

탭, 전송 요청, 장치 반영을 서로 다른 사건으로 본다.

---

# 이번 주 완료 조건

- Ready에서만 출력 명령
- 요청 중 중복 탭 차단
- 요청/확인/실패 상태 분리
- fake·real 같은 계약
- 잘못된 채널, timeout, disconnect 복구

---

<!-- _class: lead -->
# 1일차 — fake 출력 명령과 상태

30분 설명·라이브 시연

---

## 0–5분 — 세 사실은 다르다

```text
사용자 탭
   ≠ 앱이 명령을 수락함
      ≠ 장치 상태가 확인됨
```

성공 확인 전에 화면 스위치를 `HIGH`로 바꾸면 실패 때 거짓 상태가 된다.

---

## 5–10분 — 명령 경로

```text
XML View event
  → ViewModel / use case
    → BleGateway.writeOutput(command)
      → fake 또는 real transport
        → ESP32-C3 protocol handler
```

각 경계의 입력·출력·오류를 한 줄로 말할 수 있어야 한다.

---

## 10–15분 — Ready gate

| 연결 상태 | 출력 버튼 | 탭 결과 |
|---|---:|---|
| Idle/Scanning | 비활성 | 연결 안내 |
| Connecting/Discovering | 비활성 | 진행 상태 유지 |
| Ready | 활성 | 명령 검증 후 요청 |
| Disconnected/Error | 비활성 | 원인별 복구 |

UI 비활성화와 use case 검증을 함께 둔다.

---

## 15–20분 — 명령 계약

~~~kotlin
data class OutputCommand(
    val channel: OutputChannel, // 허용 GPIO 매핑은 TBD
    val level: OutputLevel,
)
~~~

- raw pin 숫자를 임의 전송하지 않는다.
- encoding·응답 규칙은 instructor-pinned protocol을 따른다.
- UI 문자열을 BLE payload로 바로 보내지 않는다.

---

## 20–25분 — 출력 UI 상태

```text
Unknown
  └─ request ─▶ Sending(desired)
                  ├─ confirmed ─▶ Confirmed(actual)
                  ├─ rejected  ─▶ Failed(previous)
                  └─ timeout   ─▶ Uncertain(desired, lastConfirmed)
                                      + RECONCILE_REQUIRED
```

timeout은 자동으로 `LOW`나 `HIGH`를 단정할 근거가 아니다. 동기화가 완료되어 `RecoveryGate.CLEAR`가 되기 전 새 write는 `BUSY`로 차단한다.

---

## 25–30분 — fake 실패 시연

- 정상: Ready + valid HIGH + confirmed
- 경계: 같은 level 연속 요청, 빠른 중복 탭
- 실패: invalid channel, timeout, link lost

사건 trace를 먼저 예측한 뒤 UI와 대조한다.

---

<!-- _class: lead -->
# 2일차 — 실제 출력 제어와 진단

30분 설명·라이브 시연

---

## 0–5분 — 프로토콜 계약 점검

| 항목 | 상태 |
|---|---|
| service UUID | TBD — 강의자 고정 필요 |
| output characteristic UUID | TBD — 강의자 고정 필요 |
| 허용 GPIO/채널 | TBD — 강의자 고정 필요 |
| payload/응답 | TBD — 강의자 고정 필요 |

확정본이 배포되기 전에는 숫자나 바이트를 추정하지 않는다.

---

## 5–10분 — write 가능 조건

```text
permission granted
∧ state == Ready
∧ output contract matched
∧ command valid
∧ no conflicting request
```

하나라도 거짓이면 transport write를 시작하지 않는다.

---

## 10–15분 — 요청과 확인의 상관관계

```text
t0  UserRequested(channel=A, level=HIGH)
t1  WriteDispatched(requestId=7)
t2  TransportCompleted(requestId=7)
t3  DeviceStateConfirmed(requestId=7, actual=HIGH)  // 계약 지원 시
```

어느 단계까지 가능한지는 고정된 프로토콜이 결정한다.

---

## 15–20분 — 물리 관찰은 추가 증거

| 증거 | 말할 수 있는 것 | 말할 수 없는 것 |
|---|---|---|
| UI 상태 | 앱이 이해한 상태 | 실제 전압의 정확한 값 |
| transport event | 요청 처리 단계 | 출력 회로 전체의 정상 |
| LED/출력 관찰 | 보이는 물리 변화 | protocol callback 순서 |

세 증거를 시간순으로 묶는다.

---

## 20–25분 — 실패 뒤 재시도

1. 현재 요청을 종료 상태로 만든다.
2. 연결 상태를 다시 확인한다.
3. 불확실한 출력은 `RECONCILE_REQUIRED`로 두고 새 write를 막는다.
4. 제공 읽기/동기화가 `Confirmed(actual) + CLEAR`로 끝난 뒤 사용자가 재시도한다.

무제한 자동 재전송은 출력이 두 번 적용될 위험을 검토해야 한다.

---

## 25–30분 — 실습 인계

1. fake 회귀 테스트
2. real Ready 확인
3. 출력 한 번 요청·확인
4. disconnect 또는 timeout 실패
5. 복구 후 다시 확인

펌웨어·GPIO·payload는 학생이 수정하지 않는다.

---

# 공식 자료

- Android Developers: Transfer BLE data
- Android Developers: Connect to a GATT server
- Android Developers: Lifecycle-aware coroutines for Views
