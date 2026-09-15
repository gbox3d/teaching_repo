# 6주차 예제 — 코루틴 카운트다운과 가짜 연결

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | Handler → `lifecycleScope.launch` + `countDown()` |
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` | 5주차 `examples/day2` 그대로 (`scanProgress`, `stopButton`에 `enabled="false"`) |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | 5주차 `examples/day2` 그대로 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | `scanJob`·[중지], `connectFake()`, `tryConnect()`, [다시 시도] |
| [day2/activity_main.xml](day2/activity_main.xml) | `activity_main.xml` | `retryButton` 추가 |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | `retry` 추가 |
| `dayN/ControlActivity.kt`, `dayN/activity_control.xml` | 제어 화면 | 4주차 그대로, 바꾸지 않는다 |
| `dayN/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 4주차 그대로. 내 파일에는 아이콘 등 줄이 더 있어도 된다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
코루틴 의존성(`kotlinx-coroutines-android`, `lifecycle-runtime-ktx`)은 4주차 `build.gradle.kts`에 이미 들어 있다.

## 1. `for (i in 5 downTo 1)` — 다섯 번 반복

```kotlin
for (i in 5 downTo 1) {
    binding.stateText.text = "검색 중… $i"
    delay(1000)
}
```

- `i`가 5, 4, 3, 2, 1로 바뀌며 중괄호 안이 다섯 번 실행된다. 대소문자 `downTo`다.
- 올라가며 세려면 `for (i in 1..5)`다. 이번 주에는 쓰지 않는다.

## 2. `lifecycleScope.launch`와 `delay` — 기다리는 동안 화면은 자유

```kotlin
lifecycleScope.launch {
    countDown()
    binding.stateText.text = "검색 완료"
}
```

| 실행 결과 | 화면 |
|---|---|
| [검색] 직후 | `검색 중… 5`, ProgressBar 표시, [검색] 비활성 |
| 1초마다 | `검색 중… 4` → `3` → `2` → `1` |
| 5초 뒤 | `검색 완료`, ProgressBar 사라짐, [검색] 활성 |

- `launch { }` 안은 코루틴이다. 위에서 아래로 읽히지만 `delay`에서 멈췄다가 1초 뒤 이어진다.
- `delay(1000)`은 메인 스레드를 붙잡지 않는다. `Thread.sleep(1000)`으로 바꾸면 5초 동안 화면이 멈추고 중간 숫자가 보이지 않는다.
- `lifecycleScope`는 이 화면(`MainActivity`)에 묶여 있어 화면이 사라지면 코루틴도 사라진다.

## 3. `suspend fun` — 멈췄다 이어지는 함수

```kotlin
private suspend fun countDown() {
    for (i in 5 downTo 1) {
        binding.stateText.text = "검색 중… $i"
        delay(1000)
    }
}
```

- 안에서 `delay`(suspend 함수)를 부르므로 `suspend`를 붙인다. 빼면 `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` 오류가 난다.
- `suspend fun`은 `launch { }` 안이나 다른 `suspend fun` 안에서만 부를 수 있다. 클릭 리스너에서 바로 부르면 같은 오류가 `countDown`에 대해 난다.

## 4. `Job.cancel()` — [중지]

```kotlin
private var scanJob: Job? = null

scanJob = lifecycleScope.launch { countDown() }

binding.stopButton.setOnClickListener {
    scanJob?.cancel()
}
```

| 실행 결과 | 화면 |
|---|---|
| `검색 중… 3`에서 [중지] | 숫자가 `3`에서 멈춘다. `검색 완료`는 나오지 않는다 |
| 이어서 [검색] | 새 코루틴이 `검색 중… 5`부터 다시 센다 |

- `launch`가 돌려주는 `Job`을 보관해야 나중에 멈출 수 있다.
- `cancel()`하면 `delay`에서 멈춰 있던 코루틴이 그 자리에서 끝난다. 그 아래 줄은 실행되지 않는다.

## 5. `withContext(Dispatchers.IO)` — 진짜 막히는 일만

```kotlin
private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
    Thread.sleep(2000)
    if (Random.nextBoolean()) {
        throw Exception("연결 실패")
    }
    true
}
```

| 하는 일 | 어디서 |
|---|---|
| `binding.xxx` 바꾸기 | 그냥 `launch { }` 안 (메인 스레드) |
| `delay` | 그냥 `launch { }` 안. 옮길 필요 없음 |
| `Thread.sleep`, 파일, 네트워크 | `withContext(Dispatchers.IO) { }` 안 |

- 중괄호 안이 다른 스레드에서 실행되고, 끝나면 메인 스레드로 돌아온다. 마지막 줄 `true`가 결과다.
- `: Boolean`은 이 함수가 참/거짓 하나를 돌려준다는 표시, `fun … = …`은 `=` 오른쪽 결과를 그대로 돌려주는 짧은 모양이다(중괄호 본문 대신). 이번 주에는 이 함수에서만 쓴다.
- `withContext` 없이 `Thread.sleep(2000)`을 쓰면 빌드는 되지만 `연결 중…`에서 2초 동안 화면이 멈춘다.
- `Random`은 `kotlin.random.Random`이다. `java.util.Random`을 import하면 `Unresolved reference 'nextBoolean'.` 오류로 빌드가 안 된다.

## 6. `try/catch` — 실패해도 앱이 꺼지지 않게

```kotlin
try {
    connectFake()
    binding.stateText.text = "연결됨"
} catch (e: Exception) {
    binding.stateText.text = "연결 실패"
    Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
    binding.retryButton.visibility = View.VISIBLE
}
```

| 실행 결과 | 화면 |
|---|---|
| `connectFake()` 성공 | `연결됨` → 제어 화면 `장치: 이름` |
| `connectFake()`가 `throw` | `연결 실패`, Toast `연결 실패`, [다시 시도] 버튼 |
| `try` 없이 `throw` | 앱 종료. Logcat `FATAL EXCEPTION` 아래 `java.lang.Exception: 연결 실패` |

- `e.message`는 `throw Exception("연결 실패")`의 괄호 안 글자다.
- `try/catch`는 `launch { }` 람다가 아니라 `suspend fun tryConnect()` 안에 둔다. 그래야 `this`가 `MainActivity`라 `Intent`·`Toast`를 4주차처럼 쓸 수 있다.

## 7. 2일차 완성 — 검색 → 연결 → 재시도

[day2/MainActivity.kt](day2/MainActivity.kt), [day2/activity_main.xml](day2/activity_main.xml), [day2/strings.xml](day2/strings.xml)을 넣고 실행한 흐름:

```text
[검색] → 검색 중… 5 … 1 → 연결 중…(2초) ─┬─ 연결됨 → 제어 화면
   [중지] → 그 숫자에서 정지                 └─ 연결 실패 + Toast + [다시 시도] → 연결 중… → …
```

카운트다운 중에 화면을 돌리면 `대기 중`으로 돌아간다. 7주차에 `ViewModel`로 해결한다.

## 공식 참고 자료

- [Android의 Kotlin 코루틴 — Android Developers](https://developer.android.com/kotlin/coroutines)
- [코루틴 기초 — Kotlin 문서](https://kotlinlang.org/docs/coroutines-basics.html)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
