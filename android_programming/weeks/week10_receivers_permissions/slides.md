---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍(Android)
footer: 10주차 · BroadcastReceiver와 권한
---

# BroadcastReceiver

## 1일차 · [0–4분] event의 짧은 진입점

```text
system/app broadcast → Intent filter → onReceive() → 상태 갱신/작업 예약
```

질문: **Receiver가 event를 받았다는 것과 오래 실행할 권리를 얻었다는 것은 같은가?**

`onReceive()`는 main thread에서 짧게 끝낸다.

---

## 1일차 · [4–9분] 두 등록 방식

| 방식 | 활성 범위 | 핵심 주의 |
|---|---|---|
| context-registered | register~unregister/context 수명 | 해제 누락·중복 등록 |
| manifest-declared | 설치 시 등록, 허용된 event에서 app 진입 가능 | implicit broadcast 제한·노출 |

대부분의 UI 대시보드 실습은 필요한 동안만 context 등록한다.

---

## 1일차 · [9–14분] lifecycle 대칭

```text
onStart  ─ register ─▶ event 수신
onStop   ─ unregister ▶ 수신 중단
```

```kotlin
override fun onStart() { super.onStart(); registerStatusReceiver() }
override fun onStop() { unregisterReceiver(receiver); super.onStop() }
```

등록 범위는 제품 요구에 맞추되 시작/종료를 대칭으로 만든다.

---

## 1일차 · [14–20분] exported 경계

```text
app-private action → RECEIVER_NOT_EXPORTED
system/other app   → RECEIVER_EXPORTED + 입력 불신 + 필요 시 permission
```

서로 다른 출처를 한 receiver/filter에 섞지 않는다. exported receiver는 다른 앱이 unprotected broadcast를 보낼 수 있음을 고려한다.

---

## 1일차 · [20–25분] 입력은 검증한다

```kotlin
override fun onReceive(context: Context, intent: Intent) {
    if (intent.action != ACTION_STATUS) return
    val code = intent.getIntExtra(EXTRA_CODE, INVALID)
    if (code !in ALLOWED_CODES) return
    sink(code)
}
```

action namespace, package 제한, permission, payload allowlist를 조합한다.

---

## 1일차 · [25–30분] 오래 일하지 않는다

```text
onReceive main thread
 ├─ 빠른 검증·상태 전달: 가능
 └─ blocking/긴 작업: 예약 가능한 background API 검토
```

**실습:** register 수명과 event 출처를 먼저 표로 작성한다.

---

# Runtime permission과 BLE 예고

## 2일차 · [0–5분] 권한은 상태 흐름

```text
feature click → 필요성 확인 → granted?
  ├─ yes → protected action 직전 재확인 → 실행
  └─ no  → rationale? → request → grant/deny → 대체 UI
```

앱 시작 즉시 문맥 없이 요청하지 않는다.

---

## 2일차 · [5–10분] Manifest만으로 끝나지 않는다

| 단계 | 역할 |
|---|---|
| declare | 앱이 요청할 수 있는 권한 명시 |
| check | 현재 grant 상태 확인 |
| rationale | 기능과 필요한 이유 설명 |
| request | system dialog 실행 |
| result | grant/deny에 맞춰 기능·UI 변경 |

권한은 언제든 revoke될 수 있어 protected action마다 확인한다.

---

## 2일차 · [10–16분] BLE 권한 matrix

| 앱 target/환경 | scan/connect 준비 |
|---|---|
| target Android 12(API 31)+, device 31+ | `BLUETOOTH_SCAN` + `BLUETOOTH_CONNECT` runtime |
| 위 앱의 legacy device 경로 | legacy 선언 + scan 위치 runtime 경로를 공식표대로 적용 |
| target 30 이하 legacy 앱 | `BLUETOOTH`/discovery 선언과 scan용 `ACCESS_FINE_LOCATION` runtime |

수업 target/min SDK는 `TBD`; foreground scan만 다루고 실제 BLE는 12주차부터다.

---

## 2일차 · [16–21분] 최소 권한

`Smart I/O Controller`는 central 역할:

- scan: `BLUETOOTH_SCAN`
- 연결/통신: `BLUETOOTH_CONNECT`
- advertise: 사용하지 않으므로 요청하지 않음
- 위치 파생 여부와 `neverForLocation`은 기능 분석 후 결정

`neverForLocation`은 일부 BLE beacon filtering 가능성을 검토한다.

---

## 2일차 · [21–26분] 거절도 정상 상태

```kotlin
sealed interface PermissionUiState {
    data object Granted : PermissionUiState
    data object NeedsRequest : PermissionUiState
    data object NeedsRationale : PermissionUiState
    data object Denied : PermissionUiState
}
```

`shouldShow... == false` 하나만으로 “영구 거절”을 단정하지 않는다.

---

## 2일차 · [26–30분] 검증 행렬

| 경로 | 기대 UI |
|---|---|
| granted | scan 준비 활성 |
| denied | 기능 비활성 + 계속 사용 가능 |
| rationale | 왜 필요한지 + 취소 가능 |
| no BLE feature | 권한 요청 없이 unavailable |

**실습:** 실제 scan 대신 권한과 capability 상태까지만 증명한다.
