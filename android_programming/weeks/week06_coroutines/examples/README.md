# 6주차 예제 조각

이 폴더는 강의자가 제공한 Kotlin/XML Views 기준 프로젝트에 복사해 관찰하는 코드 조각이다. **독립적으로 빌드 가능한 Gradle 프로젝트가 아니며**, package·import·Lifecycle/coroutine 의존성 버전은 학기 기준 프로젝트의 `TBD` 값에 맞춘다.

## 1. 중단 가능한 fake repository

```kotlin
class FakeConnectionRepository {
    suspend fun connect(delayMs: Long, fail: Boolean): String {
        delay(delayMs)
        if (fail) throw IOException("simulated connection failure")
        return "Ready"
    }
}
```

예상 관찰:

- `delayMs` 동안 main thread의 버튼이 반응한다.
- Job을 취소하면 반환/실패 대신 cancellation 경로로 빠진다.
- `fail = true`는 실제 장치 없이 반복 가능한 실패를 만든다.

## 2. 이전 연결에 취소 요청

```kotlin
class ControllerViewModel(
    private val repository: FakeConnectionRepository
) : ViewModel() {
    private var connectJob: Job? = null

    fun connect(delayMs: Long, fail: Boolean) {
        connectJob?.cancel()
        connectJob = viewModelScope.launch {
            try {
                println("CONNECTING ${Thread.currentThread().name}")
                val result = repository.connect(delayMs, fail)
                println("RESULT $result")
            } catch (cancelled: CancellationException) {
                println("CANCELLED")
                throw cancelled
            } catch (error: IOException) {
                println("ERROR ${error.message}")
            } finally {
                println("CLEANUP")
            }
        }
    }
}
```

예상 관찰:

- 두 번째 `connect()`는 첫 Job에 취소를 **요청**하고 새 Job을 시작한다. `cancel()`은 완료를 기다리지 않으므로 `CONNECTING(B)`와 `CLEANUP(A)`의 상대 순서는 보장되지 않는다.
- 취소가 첫 Job의 `delay` 중 전달되면 그 Job은 `CANCELLED → CLEANUP`으로 끝나고 `RESULT`를 남기지 않는다. 완료 경계와 경합하는 최신 상태 게시 문제는 7주차의 Job+요청 토큰으로 막는다.
- 일반 I/O 실패는 `ERROR`, 취소는 `CANCELLED`로 구분된다.

## 3. XML View의 최소 event 전달

```kotlin
binding.connectButton.setOnClickListener {
    viewModel.connect(delayMs = 1_000L, fail = false)
}
```

Activity/Fragment는 repository나 dispatcher를 직접 선택하지 않는다. 7주차에는 `println` 대신 `StateFlow<UiState>`를 lifecycle-aware하게 수집한다.

## 확인할 로그 순서

```text
normal: CONNECTING → RESULT Ready → CLEANUP
failure: CONNECTING → ERROR simulated connection failure → CLEANUP
replaced (one possible order): CONNECTING(A) → CONNECTING(B) → CANCELLED(A) → CLEANUP(A) → RESULT(B)
replaced (another valid order): CONNECTING(A) → CANCELLED(A) → CLEANUP(A) → CONNECTING(B) → RESULT(B)
```

`cancel()` 뒤 이전 cleanup 완료가 다음 작업의 필수 전제라면 suspend 경계에서 `cancelAndJoin()`을 사용해야 한다. 이 예제는 UI event를 막지 않는 취소 요청을 관찰하며, `TIMEOUT_MS_TBD` 등 운영 값은 임의로 확정하지 않는다.
