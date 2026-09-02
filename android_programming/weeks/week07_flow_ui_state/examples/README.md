# 7주차 예제 조각

다음 코드는 강의자의 Kotlin/XML Views 기준 프로젝트에 복사해 쓰는 최소 조각이다. **독립 Gradle 프로젝트가 아니며**, package·import·Lifecycle/coroutine 의존성 버전은 학기 기준표의 `TBD`를 따른다.

## 1. UI 상태와 ViewModel

```kotlin
sealed interface ControllerUiState {
    data object Idle : ControllerUiState
    data object Scanning : ControllerUiState
    data object Connecting : ControllerUiState
    data class Ready(val deviceName: String) : ControllerUiState
    data object Empty : ControllerUiState
    data class Error(val message: String) : ControllerUiState
}

class ControllerViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<ControllerUiState>(ControllerUiState.Idle)
    val uiState: StateFlow<ControllerUiState> = _uiState.asStateFlow()

    private var simulationJob: Job? = null
    private var latestRequestId = 0L

    fun simulateSuccess() {
        val requestId = ++latestRequestId
        simulationJob?.cancel()
        simulationJob = viewModelScope.launch {
            publishIfLatest(requestId, ControllerUiState.Scanning)
            delay(500)
            publishIfLatest(requestId, ControllerUiState.Connecting)
            delay(500)
            publishIfLatest(requestId, ControllerUiState.Ready("Demo Device"))
        }
    }

    private fun publishIfLatest(
        requestId: Long,
        state: ControllerUiState,
    ) {
        if (requestId == latestRequestId) {
            _uiState.value = state
        }
    }
}
```

예상 관찰:

- 새 collector는 가장 최근 상태를 즉시 받고, 외부 코드는 `_uiState`를 변경할 수 없다.
- `simulateSuccess()`를 연속 호출하면 이전 `simulationJob`에 취소를 요청한다.
- `cancel()`은 이전 Job의 종료를 기다리지 않지만 요청 ID가 오래된 Job의 `Connecting/Ready` 게시를 차단하므로 최신 호출만 최종 상태를 만든다.

## 2. XML Fragment에서 안전하게 collect

```kotlin
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)

    viewLifecycleOwner.lifecycleScope.launch {
        viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.uiState.collect { state ->
                render(state)
            }
        }
    }
}
```

예상 관찰:

- Fragment View가 STARTED이면 새 상태를 render한다.
- STOPPED이면 반복 block의 collector가 취소되어 View를 갱신하지 않는다.
- 다시 STARTED가 되면 새 collector가 StateFlow의 최신값을 즉시 받는다.

## 3. 상태 전체를 결정하는 render

```kotlin
private fun render(state: ControllerUiState) = with(binding) {
    progress.isVisible = state is ControllerUiState.Scanning ||
        state is ControllerUiState.Connecting
    retryButton.isVisible = state is ControllerUiState.Error
    controlButton.isEnabled = state is ControllerUiState.Ready
    statusText.text = when (state) {
        ControllerUiState.Idle -> "대기"
        ControllerUiState.Scanning -> "검색 중"
        ControllerUiState.Connecting -> "연결 중"
        is ControllerUiState.Ready -> "연결됨: ${state.deviceName}"
        ControllerUiState.Empty -> "검색 결과 없음"
        is ControllerUiState.Error -> state.message
    }
}
```

예상 관찰: Ready→Error로 전이하면 제어 버튼이 비활성화되고 retry가 보이며, 이전 progress 상태가 남지 않는다.

## 금지할 비교 기준

```kotlin
// UI를 갱신하는 Flow에는 사용하지 않는다.
viewLifecycleOwner.lifecycleScope.launch {
    viewModel.uiState.collect(::render)
}
```

이 코드는 lifecycleScope 안에 있어도 `STOPPED` 시 collection을 자동 중단하지 않는다. 공식 Android 문서의 `repeatOnLifecycle` 패턴을 사용한다.
