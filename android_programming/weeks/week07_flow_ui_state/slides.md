---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍(Android)
footer: 7주차 · Flow 기반 UI 상태
---

# Flow 기반 UI 상태

## 1일차 · [0–4분] 값 하나에서 시간축으로

```text
connect() → Ready              단일 결과

Idle → Scanning → Connecting → Ready → Disconnected
                         시간에 따라 변하는 상태
```

질문: **화면이 다시 나타났을 때 가장 최근 상태를 즉시 알아야 하는가?**

---

## 1일차 · [4–9분] cold Flow와 hot StateFlow

| 항목 | `Flow` | `StateFlow` |
|---|---|---|
| 수집 전 생산 | 보통 시작하지 않음 | 생산자 정책에 따라 활성 |
| 현재값 | 필수 아님 | 항상 초기/현재값 보유 |
| 새 collector | upstream 재실행 가능 | 최신값 즉시 수신 |
| UI 상태 | 변환 원천 | 상태 holder에 적합 |

수집 횟수와 생산 횟수는 같은 개념이 아니다.

---

## 1일차 · [9–14분] 상태를 서로 배타적으로

```kotlin
sealed interface ControllerUiState {
    data object Idle : ControllerUiState
    data object Scanning : ControllerUiState
    data object Connecting : ControllerUiState
    data class Ready(val deviceName: String) : ControllerUiState
    data object Empty : ControllerUiState
    data class Error(val message: String) : ControllerUiState
}
```

여러 Boolean 조합보다 불가능한 상태를 줄인다.

---

## 1일차 · [14–20분] 단방향 데이터 흐름

```text
View event ─▶ ViewModel ─▶ repository/fake stream
    ▲              │
    └── render ◀── StateFlow<UiState>
```

```kotlin
private val _uiState = MutableStateFlow<ControllerUiState>(
    ControllerUiState.Idle
)
val uiState: StateFlow<ControllerUiState> = _uiState.asStateFlow()
```

View는 상태를 직접 쓰지 않는다.

---

## 1일차 · [20–25분] Flow를 UI 상태로 변환

```kotlin
fakeTransport.states
    .map(::toUiState)
    .catch { emit(ControllerUiState.Error("연결 실패")) }
    .collect { _uiState.value = it }
```

- upstream 오류가 어디서 상태로 바뀌는지 명확히 한다.
- cancellation을 사용자 오류로 바꾸지 않는다.
- 내부 원인은 Logcat, 사용자에게는 복구 가능한 문구를 준다.

---

## 1일차 · [25–30분] 하나의 render 함수

```kotlin
private fun render(state: ControllerUiState) = with(binding) {
    progress.isVisible = state is ControllerUiState.Scanning ||
        state is ControllerUiState.Connecting
    retryButton.isVisible = state is ControllerUiState.Error
    status.text = state.label()
}
```

**실습:** 먼저 상태 전이표를 만들고 모든 `when` 분기를 구현한다.

---

# 생명주기에 맞춘 수집과 복구

## 2일차 · [0–5분] 보이지 않는 View를 갱신하지 않는다

잘못된 경계:

```kotlin
lifecycleScope.launch { viewModel.uiState.collect(::render) }
```

UI가 `STOPPED`여도 계속 수집할 수 있다. Fragment View의 수명에 맞춘다.

---

## 2일차 · [5–11분] `repeatOnLifecycle`

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect(::render)
    }
}
```

```text
STARTED: child collector 시작
STOPPED: child collector 취소
STARTED: 새 child + StateFlow 최신값
```

---

## 2일차 · [11–16분] producer와 collector 수명 분리

| 책임 | 소유자 |
|---|---|
| 연결 정책·UI 상태 | ViewModel |
| 화면 render 수집 | Fragment View lifecycle |
| 실제 transport 수명 | repository 정책 |

collector가 멈췄다고 연결 정책이 자동으로 끝나는 것은 아니다.

---

## 2일차 · [16–22분] timeout과 제한 재시도

```kotlin
withTimeout(TIMEOUT_MS_TBD) {
    fakeStates()
        .retry(RETRY_COUNT_TBD) { it is IOException }
        .collect(::updateState)
}
```

- 무한 재시도 금지
- 취소·권한 거절은 자동 재시도 대상이 아님
- 횟수·간격은 `TBD`, 수업 기준 환경에서 확정

---

## 2일차 · [22–27분] 중복 수집 찾기

```text
회전 1회 뒤 상태 한 번 emit
 ├─ render 1회: 정상
 └─ render 2회+: collector 누적 의심
```

collector 시작/종료 로그와 instance id를 함께 기록한다.

---

## 2일차 · [27–30분] 검증 행렬

| 경로 | 기대 |
|---|---|
| normal | Ready + 제어 활성 |
| boundary | STOPPED 동안 render 없음, 복귀 즉시 최신값 |
| failure | Error + 원인 로그 + 재시도 |
| timeout | 무한 spinner 없이 복구 행동 |

다음 주 개인 실기는 이 흐름의 이해를 확인한다.
