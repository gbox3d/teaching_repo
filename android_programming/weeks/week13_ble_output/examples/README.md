# 13주차 예제 — 출력 명령 계약

이 문서의 Kotlin/XML은 **설계와 fake 테스트를 위한 의사코드**다. 저수준 Android BLE 호출, import, Manifest, Gradle 설정, 실제 UUID·GPIO·payload가 없으므로 빌드 가능한 앱이 아니다. 실제 수업에서는 강의자 제공 starter와 abstraction을 사용한다.

## 의미 기반 명령

```kotlin
@JvmInline
value class OutputChannel(val logicalId: String)

enum class OutputLevel { LOW, HIGH }

data class OutputCommand(
    val channel: OutputChannel,
    val level: OutputLevel,
)

enum class RequestResult {
    ACCEPTED, NOT_READY, INVALID_CHANNEL, BUSY
}

enum class RecoveryGate { CLEAR, RECONCILE_REQUIRED, RECONCILING }

interface OutputController {
    val results: Flow<OutputEvent>
    suspend fun request(command: OutputCommand): RequestResult
}
```

`logicalId`에서 실제 GPIO와 payload로의 변환은 instructor-pinned protocol adapter의 책임이다.

## 출력 사건과 UI 상태

```kotlin
sealed interface OutputEvent {
    data class Accepted(val requestId: String) : OutputEvent
    data class TransportCompleted(val requestId: String) : OutputEvent
    data class StateConfirmed(
        val requestId: String,
        val actual: OutputLevel,
    ) : OutputEvent
    data class Rejected(val reason: String) : OutputEvent
    data class TimedOut(val requestId: String) : OutputEvent
}

sealed interface OutputUiState {
    data object Unknown : OutputUiState
    data class Sending(val desired: OutputLevel) : OutputUiState
    data class Confirmed(val actual: OutputLevel) : OutputUiState
    data class Failed(val lastConfirmed: OutputLevel?) : OutputUiState
    data class Uncertain(
        val desired: OutputLevel,
        val lastConfirmed: OutputLevel?,
    ) : OutputUiState
}
```

`StateConfirmed`가 실제 계약에 존재하는지는 `TBD`다. 없다면 transport 완료와 물리 상태 확인을 같은 사건으로 만들지 않는다.

## use case gate

```kotlin
suspend fun setOutput(command: OutputCommand): RequestResult {
    if (linkState.value !is LinkState.Ready) return RequestResult.NOT_READY
    if (!protocolPolicy.isAllowed(command.channel)) return RequestResult.INVALID_CHANNEL
    if (outputState.value is OutputUiState.Sending ||
        outputState.value is OutputUiState.Uncertain
    ) return RequestResult.BUSY
    if (recoveryGate.value != RecoveryGate.CLEAR) return RequestResult.BUSY
    return controller.request(command)
}
```

timeout 또는 link lost는 `Uncertain(desired, lastConfirmed)`와 별도 `RecoveryGate.RECONCILE_REQUIRED`를 만든다. 제공된 동기화 절차를 시작하면 `RECONCILING`, 확인 가능한 실제 값으로 완료하면 `Confirmed(actual) + CLEAR`가 된다. `CLEAR` 전의 새 write는 `BUSY`로 차단하며, 읽기/확인 계약이 고정되지 않았다면 임의 값을 만들어 동기화 완료로 처리하지 않는다. 반환 타입과 함수명은 실제 starter에 맞춰 번역한다.

## XML View 역할 스케치

```xml
<!-- 실제 id/style/string은 starter 기준 -->
<LinearLayout>
    <TextView android:id="@+id/linkState" />
    <Switch android:id="@+id/outputSwitch" />
    <ProgressBar android:id="@+id/outputPending" />
    <TextView android:id="@+id/outputEvidence" />
    <Button android:id="@+id/reconcileButton" />
</LinearLayout>
```

## fake trace

```text
confirmed:
  UserRequested(HIGH) → Accepted(7) → TransportCompleted(7)
  → StateConfirmed(7, HIGH)

timeout:
  UserRequested(HIGH) → Accepted(8) → TimedOut(8)
  → Uncertain(desired=HIGH, lastConfirmed=LOW)
    + RecoveryGate.RECONCILE_REQUIRED
  → [provided reconcile completes with LOW]
    → Confirmed(LOW) + RecoveryGate.CLEAR

disconnect:
  UserRequested(LOW) → Accepted(9) → LinkLost
  → LinkState.Disconnected + OutputUiState.Uncertain
    + RecoveryGate.RECONCILE_REQUIRED
```

## 확정 대기 프로토콜

| 항목 | 값 |
|---|---|
| service UUID | `TBD — instructor pin required` |
| output characteristic UUID | `TBD — instructor pin required` |
| logical channel → GPIO | `TBD — instructor pin required` |
| command encoding | `TBD — instructor pin required` |
| completion/ack/readback 의미 | `TBD — instructor pin required` |
| timeout·retry policy | `TBD — instructor pin required` |

## 공식 자료

- [Transfer BLE data](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [Connect to a GATT server](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [Lifecycle-aware coroutines for Views](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
