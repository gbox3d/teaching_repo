# 12주차 예제 — BLE 추상화와 상태 계약

이 문서는 **인터페이스·상태·테스트 설계를 위한 의사코드**다. Android BLE 저수준 API, import, Manifest, Gradle 설정을 모두 포함한 빌드 가능한 앱이 아니다. 실제 수업에서는 강의자가 제공한 starter와 BLE 추상화를 사용한다.

## 역할 모델

| 축 | Android 앱 | Tenstar ESP32-C3 |
|---|---|---|
| 연결 | central | peripheral |
| GATT | client | server |

## 제공 추상화의 개념 계약

```kotlin
interface BleGateway {
    val events: Flow<BleEvent>
    suspend fun startScan(limit: ScanLimit)
    suspend fun stopScan()
    suspend fun connect(device: DeviceId)
    suspend fun disconnect()
}

sealed interface BleEvent {
    data object ScanStarted : BleEvent
    data class DeviceSeen(val id: DeviceId, val label: String?) : BleEvent
    data class ScanStopped(val reason: StopReason) : BleEvent
    data class LinkConnected(val id: DeviceId) : BleEvent
    data object DiscoveryStarted : BleEvent
    data class ContractMatched(val serviceId: String) : BleEvent
    data class Failed(val stage: Stage, val kind: FailureKind) : BleEvent
    data class LinkLost(val cause: String) : BleEvent
}

sealed interface LinkInput {
    data class UserSelected(val id: DeviceId) : LinkInput
    data class FromGateway(val event: BleEvent) : LinkInput
}
```

reducer는 사용자 선택과 gateway 사건을 함께 받되 둘의 출처를 구분한다. 정확한 클래스와 함수명은 starter가 권위 원본이다.

## 상태 reducer 규칙 예

```text
Idle + FromGateway(ScanStarted)                 -> Scanning
Scanning + FromGateway(DeviceSeen)              -> Scanning (후보 갱신)
Scanning + UserSelected(device)                 -> Connecting
Connecting + FromGateway(ScanStopped(TARGET_FOUND)) -> Connecting (감사용 self-transition)
Connecting + FromGateway(LinkConnected)         -> Discovering
Discovering + FromGateway(DiscoveryStarted)      -> Discovering (감사용 self-transition)
Discovering + FromGateway(ContractMatched)       -> Ready
Scanning + FromGateway(ScanStopped(TIME_LIMIT))  -> Disconnected(NO_DEVICES)
Ready + FromGateway(LinkLost)                    -> Disconnected
any + FromGateway(Failed)                        -> Error
```

`UserSelected(device)`를 처리하면 reducer 밖 command handler가 `stopScan()`과 `connect(device)` 효과를 요청한다. 그 결과 gateway가 보내는 `ScanStopped(TARGET_FOUND)`는 연결 상태를 바꾸지 않는 감사용 event다. 따라서 target 발견 뒤 scan이 끝났다는 증거와 `Scanning → Connecting`을 일으킨 사용자 선택을 혼동하지 않는다. `DiscoveryStarted`도 link 연결 뒤 discovery 요청이 시작됐음을 기록하는 `Discovering → Discovering` 감사용 event이며, `ContractMatched`가 실제 Ready 전이를 만든다. 불가능한 `(state, event)` 조합은 조용히 무시하지 말고 진단 로그를 남긴다.

## 버전 인식 권한 체크

| 조건 | 수업에서 확인할 것 |
|---|---|
| Android 12 이상을 대상으로 하는 앱 | Nearby devices 계열의 scan/connect 런타임 승인 |
| legacy 대상/기기 | 공식 문서의 Bluetooth·위치 규칙과 starter policy 결과 |
| 거절 | 다시 요청 가능 여부와 설명 UI |
| 다시 묻지 않음 | 설정 이동 안내와 취소 경로 |

앱의 실제 `targetSdk`와 기기 OS 조합은 개강 전 pinned inventory와 제공 `PermissionPolicy`로 판정한다.

## 확정 대기 계약

| 항목 | 값 |
|---|---|
| service UUID | `TBD — instructor pin required` |
| output characteristic UUID | `TBD — instructor pin required` |
| input characteristic UUID | `TBD — instructor pin required` |
| 허용 GPIO | `TBD — instructor pin required` |
| message encoding | `TBD — instructor pin required` |
| 장치 advertising 식별 | `TBD — instructor pin required` |

## fake 시나리오

```text
happy: ScanStarted → DeviceSeen → UserSelected(device)
       → ScanStopped(TARGET_FOUND) → LinkConnected
       → DiscoveryStarted → ContractMatched → Ready

no-device: ScanStarted → ScanStopped(TIME_LIMIT)

mismatch: ScanStarted → DeviceSeen → UserSelected(device)
          → ScanStopped(TARGET_FOUND) → LinkConnected
          → DiscoveryStarted → Failed(DISCOVERY, CONTRACT_MISMATCH)
```

## 공식 자료

- [Bluetooth Low Energy overview](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [Find BLE devices](https://developer.android.com/develop/connectivity/bluetooth/ble/find-ble-devices)
- [Bluetooth permissions](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [Connect to a GATT server](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
