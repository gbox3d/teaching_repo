# 14주차 예제·템플릿 안내

이 폴더는 프로젝트 설명과 증거 수집을 위한 Markdown 템플릿을 제공한다. Kotlin 조각은 설계용 의사코드이며 import, Manifest, Gradle, 실제 UUID·payload를 갖춘 빌드 가능한 Android 앱이 아니다.

## 템플릿

- [2~3분 시연 개요](demo_outline.md)
- [보고서 템플릿](report_template.md)
- [제출 체크리스트](submission_checklist.md)
- [개인 구술 증거표](individual_oral_evidence.md)

## 입력 관찰 의사코드

```kotlin
data class InputEvent(
    val channel: InputChannel,
    val level: InputLevel,
    val receivedAt: Instant,
    val connectionEpoch: Long,
)

sealed interface InputUiState {
    data object Unknown : InputUiState
    data class Current(val event: InputEvent) : InputUiState
    data class Stale(val last: InputEvent?) : InputUiState
    data class Failed(val recovery: Recovery) : InputUiState
}

sealed interface InputLinkEvent {
    val connectionEpoch: Long

    data class ConnectionStarted(
        override val connectionEpoch: Long,
    ) : InputLinkEvent

    data class ReadyEntered(
        override val connectionEpoch: Long,
    ) : InputLinkEvent

    data class LeftReady(
        override val connectionEpoch: Long,
    ) : InputLinkEvent
}

fun reduceInput(
    state: InputUiState,
    event: InputEvent,
    currentEpoch: Long,
    linkState: LinkState,
): InputUiState = when {
    linkState !is LinkState.Ready -> state
    event.connectionEpoch != currentEpoch -> state
    else -> InputUiState.Current(event)
}

fun reduceLinkForInput(
    state: InputUiState,
    event: InputLinkEvent,
    currentEpoch: Long,
): InputUiState {
    if (event.connectionEpoch != currentEpoch) return state
    return when (event) {
        is InputLinkEvent.ConnectionStarted -> InputUiState.Unknown
        is InputLinkEvent.ReadyEntered -> InputUiState.Unknown
        is InputLinkEvent.LeftReady -> state.asStale()
    }
}

fun InputUiState.asStale(): InputUiState = when (this) {
    is InputUiState.Current -> InputUiState.Stale(last = event)
    is InputUiState.Stale -> this
    else -> InputUiState.Stale(last = null)
}
```

link state가 Ready를 벗어나면 `LeftReady(epoch)`를 즉시 보내 마지막 `Current`를 stale로 만든다. 새 epoch를 할당해 연결을 시작할 때 `ConnectionStarted(epoch)`, 필수 구독을 마치고 Ready에 진입할 때 `ReadyEntered(epoch)`를 보내 각각 `Unknown`으로 초기화한다. reducer는 오래된 epoch의 link event도 무시한다. Ready 자체는 입력 값을 만들지 않으며, 같은 epoch의 **새 notification 또는 pinned snapshot**이 `reduceInput`을 통과해야만 `Current`가 된다. 실제 `Instant`, error, event 타입은 starter 계약에 맞춘다.

## lifecycle-aware 수집 스케치

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        launch { viewModel.linkState.collect(::renderLink) }
        launch { viewModel.inputState.collect(::renderInput) }
    }
}
```

## 확정 대기 계약

| 항목 | 값 |
|---|---|
| service/output/input UUID | `TBD — instructor pin required` |
| logical channel/GPIO | `TBD — instructor pin required` |
| command/notification encoding | `TBD — instructor pin required` |
| subscription confirmation | `TBD — instructor pin required` |
| snapshot/readback semantics | `TBD — instructor pin required` |
| retry/timeout constants | `TBD — instructor pin required` |

## 공식 자료

- [Transfer BLE data](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [Bluetooth LE in the background](https://developer.android.com/develop/connectivity/bluetooth/ble/background)
- [Lifecycle-aware coroutines for Views](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
- [Kotlin Flow](https://kotlinlang.org/docs/flow.html)
