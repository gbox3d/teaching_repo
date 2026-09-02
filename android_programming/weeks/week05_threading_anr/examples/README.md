# 5주차 예제 스니펫 — Executor, 취소, race

## 사용 범위

이 문서는 핵심 코드 조각과 관찰 지점을 제공하며 **빌드 가능한 Gradle 프로젝트는 포함하지 않는다**. 4주차 강의자 기준 프로젝트의 `DeviceControlFragment`에 package/import/resource/View 초기화를 맞춰 필요한 부분만 옮긴다.

`Thread.sleep()`은 실제 장치 통신 예제가 아니라 blocking과 취소를 관찰하기 위한 mock이다. 최종 Android 기능 코드에서 메인 스레드 blocking으로 남겨 두지 않는다.

## 파일명과 문맥

| 파일명 예시 | 위치/역할 |
|---|---|
| `DeviceControlFragment.kt` | Executor 소유, Future 취소, main UI render |
| `MockDeviceWork.kt` | 지연 가능한 순수 mock 작업 |
| `RaceExperiment.kt` | unsafe/atomic counter 비교 |
| `fragment_device_control.xml` | 실행/보조 버튼, ProgressBar, 상태 TextView |

## `MockDeviceWork.kt`

```kotlin
fun slowMockWork(durationMs: Long): Long {
    require(durationMs >= 0) { "duration must be non-negative" }
    Thread.sleep(durationMs)
    return durationMs
}
```

예상 관찰:

- worker에서 호출하면 그 worker가 지정 시간 동안 대기한다.
- main click listener에서 호출하면 input/draw queue가 지연된다.
- `Future.cancel(true)`로 interruption이 전달되면 sleep이 `InterruptedException`으로 끝날 수 있다.

## Fragment 작업 왕복 핵심

```kotlin
private val executor = Executors.newSingleThreadExecutor()
private val mainHandler = Handler(Looper.getMainLooper())
private var runningTask: Future<*>? = null
private var activeToken: Any? = null
private var statusView: TextView? = null

private fun startMockWork(durationMs: Long) {
    if (runningTask?.isDone == false) return

    val token = Any()
    activeToken = token
    renderRunning()

    runningTask = executor.submit {
        val result = try {
            Result.success(slowMockWork(durationMs))
        } catch (cancelled: InterruptedException) {
            Thread.currentThread().interrupt()
            return@submit
        } catch (error: Exception) {
            Result.failure(error)
        }
        mainHandler.post {
            if (activeToken !== token) return@post
            result.fold(
                onSuccess = { renderSuccess("${it}ms mock 완료") },
                onFailure = { renderError(it.message ?: "mock 실패") },
            )
        }
    }
}

override fun onDestroyView() {
    activeToken = null
    runningTask?.cancel(true)
    runningTask = null
    statusView = null
    super.onDestroyView()
}

override fun onDestroy() {
    executor.shutdownNow()
    super.onDestroy()
}
```

`renderRunning`, `renderSuccess`, `renderError`는 main thread에서 현재 nullable View 참조만 갱신한다. 전체 View 초기화와 다른 View 참조 정리는 기준 프로젝트 문맥에 맞춘다.

예상 관찰:

1. 800ms 작업 중에도 보조 버튼 callback이 처리된다.
2. 실행 중 중복 click은 새 task를 만들지 않는다.
3. 긴 작업 직후 Back을 누르면 token이 무효화되어 늦은 UI 결과가 무시된다.

## unsafe race 핵심

```kotlin
class UnsafeCounter {
    var value: Int = 0

    fun increment(iteration: Int) {
        val current = value
        if (iteration % 100 == 0) Thread.yield()
        value = current + 1
    }
}
```

네 worker가 같은 instance에 각 25000번 `increment()`를 호출한다. expected는 100000이지만 actual은 실행 순서에 따라 작아질 수 있다. 이 코드는 실패 현상 관찰용이다.

## atomic 수정 핵심

```kotlin
val counter = AtomicInteger(0)
val completedWorkers = AtomicInteger(0)
val workerCount = 4
val incrementsPerWorker = 25_000

repeat(workerCount) {
    executor.execute {
        repeat(incrementsPerWorker) {
            counter.incrementAndGet()
        }

        if (completedWorkers.incrementAndGet() == workerCount) {
            val actual = counter.get()
            mainHandler.post {
                renderRaceResult(expected = 100_000, actual = actual)
            }
        }
    }
}
```

위 race 실험은 여러 worker용 fixed thread pool이 있다는 문맥이다. UI 전용 단일 worker executor와 혼동하지 말고 강의자 기준 프로젝트의 별도 실험 executor를 사용한다.

## 결과 해석

| 조건 | 기대 관찰 |
|---|---|
| main blocking | draw/input 지연, ANR이라고 단정하지 않음 |
| worker mock | UI 응답 유지, 결과는 main에서 render |
| task 중 Back | 취소 요청, stale 결과 미표시 |
| unsafe 4 workers | actual이 실행마다 달라질 수 있음 |
| atomic 4 workers | 반복 실행에서 expected 100000 |

## 공식 참고 자료

- [Processes and threads — Android Developers](https://developer.android.com/guide/components/processes-and-threads)
- [ANRs — Android Developers](https://developer.android.com/topic/performance/vitals/anr)
- [Handler — Android Developers](https://developer.android.com/reference/android/os/Handler)
