# 7주차 예제 — ViewModel과 StateFlow

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/ConnViewModel.kt](day1/ConnViewModel.kt) | `app › kotlin+java › com.example.smartio › ConnViewModel.kt` (새 파일: New › Kotlin Class/File › Class) | 6주차 카운트다운·`connectFake()`·`tryConnect()`를 옮기고 `resultText`·`listener`·`show()`를 더했다 |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `by viewModels()`, 리스너에서 `viewModel.startScan()` 등 호출, 등록(`// 6.`)·다시 읽기(`// 7.`)·해제(`// 8.`)·`showState()`(`// 9.`) |
| [day1/activity_main.xml](day1/activity_main.xml), [day1/strings.xml](day1/strings.xml) | `app › res › layout › activity_main.xml`, `app › res › values › strings.xml` | 6주차 `examples/day2` 그대로 |
| [day2/ConnState.kt](day2/ConnState.kt) | `app › kotlin+java › com.example.smartio › ConnState.kt` (새 파일: New › Kotlin Class/File › Object) | 상태 문자열 상수 다섯 개 |
| [day2/ConnViewModel.kt](day2/ConnViewModel.kt) | `ConnViewModel.kt` | `resultText`·`listener`·`show()` → `_state`/`state`, `_seconds`/`seconds`, `disconnect()` 추가 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | 리스너는 한 줄씩, [해제] 리스너, 틀 두 개와 `when`. `onDestroy()`·`showState()` 삭제 |
| [day2/activity_main.xml](day2/activity_main.xml) | `activity_main.xml` | 가로 줄에 `disconnectButton` 추가 |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | `disconnect` 추가 |
| `dayN/ControlActivity.kt`, `dayN/activity_control.xml` | 제어 화면 | 4주차 그대로, 바꾸지 않는다 |
| `dayN/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 4주차 그대로. 내 파일에는 아이콘 등 줄이 더 있어도 된다. ViewModel·상수 파일은 화면이 아니라서 Manifest에 적지 않는다 |

Kotlin 파일 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
ViewModel·StateFlow 의존성(`activity-ktx`, `lifecycle-viewmodel-ktx`, `lifecycle-runtime-ktx`, `kotlinx-coroutines-android`)은 4주차 `build.gradle.kts`에 이미 들어 있다.
Logcat 필터는 `package:mine tag:Conn`이다.

## 1. `class`와 프로퍼티

```kotlin
class Counter {
    var count = 0
    fun plus() { count = count + 1 }
}

fun main() {
    val a = Counter()
    a.plus()
    a.plus()
    println(a.count)
}
```

| 실행 결과 | 출력 |
|---|---|
| Kotlin Playground에서 실행 | `2` |

- `class`는 설계도다. `Counter()`로 객체를 하나 만들고, 객체 안의 변수(**프로퍼티**)와 함수는 `a.count`, `a.plus()`처럼 점으로 부른다.
- `ConnViewModel`도 클래스다. `MainActivity`는 `viewModel.resultText`처럼 점으로 프로퍼티를 읽는다.

## 2. `ViewModel`과 `by viewModels()` — 회전해도 같은 객체

```kotlin
class ConnViewModel : ViewModel() {
    var resultText = "대기 중"
}
```

```kotlin
// MainActivity 클래스 안
private val viewModel: ConnViewModel by viewModels()
```

| 조작 | `viewModel` |
|---|---|
| 앱 시작 | 새 `ConnViewModel`이 만들어진다 |
| 회전 | 옛 화면 `onDestroy` → 새 화면 `onCreate`. 새 화면도 **같은 객체**를 받으므로 `resultText`가 남아 있다 |
| [뒤로]로 연결 화면을 닫음 | 화면과 함께 ViewModel도 정리된다 |

- `: ViewModel()`은 `ViewModel`을 물려받는다는 표시다. 빼면 `viewModelScope`를 쓸 수 없다.
- `private val viewModel = ConnViewModel()`로 직접 만들면 빌드는 되지만 회전할 때마다 새 객체가 생겨 `대기 중`으로 돌아간다.

## 3. `viewModelScope.launch` — 화면이 새로 만들어져도 계속 도는 코루틴

```kotlin
fun startScan() {
    if (scanJob?.isActive == true) {
        return
    }
    scanJob = viewModelScope.launch {
        for (i in 5 downTo 1) {
            show("검색 중… $i")
            delay(1000)
        }
        tryConnect()
    }
}
```

| 실행 결과 | Logcat `tag:Conn` |
|---|---|
| [검색] | `검색 중… 5` → 1초마다 `4`·`3`·`2`·`1` → `연결 중…` → `연결됨` 또는 `연결 실패` |
| 카운트다운 중 회전 | 줄이 끊기지 않고, 두 번씩 찍히지도 않는다 |

- 6주차 `lifecycleScope`는 화면과 함께 취소되었다. `viewModelScope`는 ViewModel에 묶여 있어 회전을 넘어 계속 돈다.
- `if (scanJob?.isActive == true) { return }`: 회전한 새 화면에서 [검색]을 다시 눌러도 코루틴이 하나 더 생기지 않게 막는다.
- ViewModel 안에는 `binding`이 없다. `binding`을 쓰면 `Unresolved reference 'binding'.`으로 빌드가 안 된다.

## 4. 1일차 — 알림 등록·해제와 회전 뒤 다시 읽기

```kotlin
// ConnViewModel
var listener: ((String) -> Unit)? = null

private fun show(text: String) {
    Log.d("Conn", text)
    resultText = text
    listener?.invoke(text)
}
```

```kotlin
// MainActivity onCreate 끝
viewModel.listener = { text ->
    showState(text)
}
binding.stateText.text = viewModel.resultText
if (viewModel.resultText == "연결 실패") {
    binding.retryButton.visibility = View.VISIBLE
}

// onCreate 아래
override fun onDestroy() {
    super.onDestroy()
    viewModel.listener = null
}
```

| 회전한 때 | 회전 뒤 화면 |
|---|---|
| `연결 실패`와 [다시 시도] | 그대로 남는다 |
| `검색 중… 3` | 글자는 곧바로 `검색 중… 3`, 1초 뒤 `2`로 이어진다. 그러나 [검색] 켬·[중지] 끔·ProgressBar 없음(XML 처음 모양) |

- `listener`는 글자 하나를 받는 코드를 넣어 두는 변수(틀)다. 화면이 없을 때는 `null`이라 `?.invoke`로 부른다.
- 등록은 `onCreate`, 해제는 `onDestroy`. 회전하면 옛 화면이 비우고 새 화면이 다시 등록한다.
- 1일차는 **글자만** 되살린다. 버튼까지 되살리는 방법이 2일차다.

## 5. `object ConnState`와 `when`

```kotlin
object ConnState {
    const val DISCONNECTED = "연결 안 됨"
    const val CONNECTING = "연결 중"
    const val DISCOVERING = "서비스 확인 중"
    const val READY = "준비됨"
    const val LOST = "끊김"
}
```

```kotlin
when (state) {
    ConnState.READY -> {
        binding.disconnectButton.isEnabled = true
    }
    ConnState.LOST -> {
        binding.scanButton.isEnabled = true
        binding.retryButton.visibility = View.VISIBLE
    }
}
```

- `object`는 이름으로 바로 부르는 하나뿐인 묶음이다. `ConnState.READY`처럼 쓴다.
- `const val`은 바뀌지 않는 상수다. `ConnState.REDY`처럼 틀리면 `Unresolved reference 'REDY'.`로 바로 드러난다.
- `class ConnState`로 쓰면 `const val` 줄마다 `Const 'val' is only allowed on top level, in named objects, or in companion objects.`가 난다.
- 이름과 값은 12주차 bleuno 라이브러리의 `ConnState`와 같다.

## 6. `MutableStateFlow` / `StateFlow` — 안에서만 바꾸고 밖에는 읽기 전용

```kotlin
private val _state = MutableStateFlow(ConnState.DISCONNECTED)
val state: StateFlow<String> = _state
private val _seconds = MutableStateFlow(0)
val seconds: StateFlow<Int> = _seconds

fun disconnect() {
    _state.value = ConnState.DISCONNECTED
}
```

| 코드 | 결과 |
|---|---|
| `_state.value = ConnState.READY` (ViewModel 안) | 받고 있는 화면의 `collect { }`가 `준비됨`으로 다시 실행된다 |
| `viewModel.state.value = ConnState.DISCONNECTED` (화면) | 빌드 오류 `'val' cannot be reassigned.` |

- `StateFlow`는 지금 값 하나를 늘 들고 있다. 처음 값은 `MutableStateFlow(…)` 괄호 안의 값이다.
- 화면은 읽기만 하고, 값을 바꾸는 일은 `disconnect()` 같은 ViewModel 함수에 맡긴다.

## 7. 틀과 `collect` — 화면이 보일 때만 받는다

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            binding.stateText.text = state
            // 먼저 모두 끄고, when (state)로 켤 것만 켠다
        }
    }
}

lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.seconds.collect { seconds ->
            if (seconds > 0) {
                binding.stateText.text = "연결 중… $seconds"
            }
        }
    }
}
```

| 때 | 틀이 하는 일 |
|---|---|
| 화면이 보이기 시작 | 받기를 시작하고 **지금 값**을 곧바로 받는다 |
| 값이 바뀜 | `collect { }` 안을 다시 실행한다 |
| 회전·홈으로 나감 | 받기를 멈춘다. 다시 보이면 마지막 값부터 다시 받는다 |

- 학생은 틀을 복사하고 `collect { }` 안만 채운다. 받을 값이 둘이면 틀도 둘이고, `seconds` 틀은 `state` 틀 **아래**에 둔다.
- 틀 없이 `collect`를 부르면 `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.`
- `collect` 안에 `startActivity`나 Toast를 두면 회전하거나 돌아올 때마다 또 실행된다. 그래서 2일차 완성본은 성공해도 제어 화면으로 자동 이동하지 않고, 실패 Toast도 없다.

## 8. 2일차 완성 — 상태별 화면

[day2/ConnState.kt](day2/ConnState.kt), [day2/ConnViewModel.kt](day2/ConnViewModel.kt), [day2/MainActivity.kt](day2/MainActivity.kt), [day2/activity_main.xml](day2/activity_main.xml), [day2/strings.xml](day2/strings.xml)을 넣고 실행한 결과:

| 상태 | `stateText` | [검색] | [중지] | [해제] | [다시 시도] | ProgressBar | [연결] |
|---|---|---|---|---|---|---|---|
| 시작 `DISCONNECTED` | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |
| [검색] → `CONNECTING` | `연결 중… 5` → `4`·`3`·`2`·`1` | 끔 | 켬 | 끔 | 숨김 | 보임 | 켬 |
| 5초 뒤 `DISCOVERING` | `서비스 확인 중` (2초) | 끔 | 끔 | 끔 | 숨김 | 보임 | 켬 |
| 성공 `READY` | `준비됨` | 끔 | 끔 | **켬** | 숨김 | 숨김 | 켬 |
| 실패 `LOST` | `끊김` | 켬 | 끔 | 끔 | **보임** | 숨김 | 켬 |
| `CONNECTING`에서 [중지] | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |
| `READY`에서 [해제] | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |

- 어느 상태에서든 회전하면 같은 글자·버튼이 그대로 보인다. `연결 중… 3`에서 돌리면 새 화면이 곧바로 `연결 중… 3`을 보이고 1초 뒤 `2`로 이어진다.
- [연결]은 4주차와 같다. `준비됨`에서 [연결]을 누르면 제어 화면으로 가고, [뒤로]로 돌아오면 `준비됨`이 그대로 보인다.

```text
[검색] → 연결 중… 5 … 1 → 서비스 확인 중(2초) ─┬─ 준비됨 → [해제] → 연결 안 됨
   [중지] → 연결 안 됨                          └─ 끊김 → [다시 시도] → 서비스 확인 중 → …
```

## 공식 참고 자료

- [ViewModel 개요 — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Android의 StateFlow 및 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴(repeatOnLifecycle) — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [object 선언 — Kotlin 문서](https://kotlinlang.org/docs/object-declarations.html)
