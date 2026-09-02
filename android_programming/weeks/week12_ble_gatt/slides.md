---
marp: true
theme: default
paginate: true
title: 12주차 BLE GATT와 연결 상태
---

# 12주차

## BLE GATT와 연결 상태

버튼 하나가 아니라 **관찰 가능한 상태 기계**를 만든다.

---

# 완료 조건

- BLE 역할 두 축 설명
- 버전 인식 권한 UX
- 제한 시간 scan
- connect 뒤 service discovery
- fake/real transport의 같은 상태 계약

---

<!-- _class: lead -->
# 1일차 — BLE 모델과 fake 연결

30분 설명·라이브 시연

---

## 0–5분 — 두 역할 축

| 연결 축 | Android 폰 | ESP32-C3 |
|---|---|---|
| central / peripheral | central: scan·연결 시작 | peripheral: advertise |
| GATT client / server | client: service 조회·요청 | server: attribute 제공 |

두 축은 관련되지만 같은 용어가 아니다.

---

## 5–10분 — advertising에서 GATT까지

```text
advertise
   ↓ scan result
connect
   ↓ link established
discover services
   ↓ required contract found
Ready
```

연결 콜백만으로 write 가능한 `Ready`가 된 것은 아니다.

---

## 10–15분 — GATT 구조

```text
GATT server (ESP32-C3)
└─ Service UUID = TBD
   ├─ Output characteristic UUID = TBD
   └─ Input characteristic UUID = TBD
```

- service는 characteristic의 묶음
- characteristic은 값과 속성을 가진 attribute
- 실제 UUID는 프로토콜 문서가 확정할 때만 입력

---

## 15–20분 — 권한은 버전 인식 결정

| 조건 | 대표 접근 |
|---|---|
| Android 12+ 대상 앱 | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` 런타임 승인 |
| 이전 대상/기기 조합 | legacy Bluetooth와 위치 관련 규칙 확인 |
| 거절 | 이유 + 다시 요청 가능한 행동 |
| 다시 묻지 않음 | 앱 설정으로 이동하는 명시적 안내 |

starter의 `PermissionPolicy`를 사용하고 한 목록을 모든 기기에 고정하지 않는다.

---

## 20–25분 — 연결 상태 기계

```text
Idle → Scanning → Connecting → Discovering → Ready
          │            │             │          │
          └────────────┴─────────────┴──────────┤
                                                ▼
                                      Disconnected / Error
```

상태마다 허용 버튼과 복구 행동을 정한다.

---

## 25–30분 — fake transport 시연

~~~kotlin
gateway.events.collect { event ->
    state = reduce(state, event) // 수업용 의사코드
}
~~~

- 정상: target 발견 → Ready
- 경계: 제한 시간까지 0대
- 실패: 권한 거절 / discovery mismatch

먼저 다음 상태를 예측하고 실행한다.

---

<!-- _class: lead -->
# 2일차 — 실제 보드 연결과 진단

30분 설명·라이브 시연

---

## 0–5분 — 실물 전환 전 계약

변하지 않는 것:

- UI 이벤트와 상태 이름
- timeout·오류·복구 규칙
- `BleGateway` 인터페이스

바뀌는 것:

- `FakeBleGateway` → 제공 `RealBleGateway`

---

## 5–10분 — scan에는 종료 조건이 있다

- 대상 식별자가 확인되면 scan 중지
- 제한 시간이 끝나면 `NoDevices`로 종료
- 무한 loop나 계속 켜 둔 scan 금지
- 재시도는 사용자의 명시 행동과 새 시간 창으로 시작

장치 이름만으로 단정하지 않고 수업용 식별 계약을 따른다.

---

## 10–15분 — 연결과 발견을 분리

| 사건 | 상태 | UI |
|---|---|---|
| target 선택 | Connecting | 연결 중, 중복 탭 차단 |
| link 연결 | Discovering | 서비스 확인 중 |
| 필수 service 확인 | Ready | 제어 활성화 |
| 필수 service 없음 | Error | 다른 장치/보드 확인 |

---

## 15–20분 — 로그는 사건 기록

```text
t+0000 ScanStarted
t+1840 DeviceSeen(label=BOARD-?)
t+1910 ConnectRequested
t+2750 LinkConnected
t+2810 DiscoveryStarted
t+3190 ContractMatched(service=TBD)
t+3200 Ready
```

실제 주소·개인 식별자는 제출 로그에서 가린다.

---

## 20–25분 — 실패 주입

- 보드 전원 끄기 → 0 devices
- 다른 보드 선택 → service mismatch 가능
- 연결 중 보드 끄기 → Disconnected/Error
- 권한 거절 → scan 시작 금지

각 경우에 “무엇을 다시 할 수 있는가?”를 UI에 둔다.

---

## 25–30분 — 실습 인계

실습 순서:

1. fake 전체 경로 재현
2. real transport로 교체
3. `Ready` 증거 확보
4. 실패 한 건 주입
5. fake/real 차이 회고

펌웨어나 UUID를 수정해 문제를 우회하지 않는다.

---

# 공식 자료

- Android Developers: BLE overview
- Android Developers: Find BLE devices
- Android Developers: Bluetooth permissions
- Android Developers: Connect/transfer GATT data
