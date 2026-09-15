# 5주차 예제 — Thread·runOnUiThread·Handler·ProgressBar

4주차에 만든 `SmartIO` 프로젝트(package `com.example.smartio`, ViewBinding)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 |
|---|---|
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` — 4주차 아홉 줄 뒤에 `scan`·`stop`·`state_idle` 세 줄 추가 |
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` — 4주차 XML의 Switch와 [연결] 사이에 [검색] 버튼과 상태 TextView 추가 |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` — 4주차 코드 아래에 [검색] 블록 추가. `Thread`·`runOnUiThread` 버전 |
| [day2/activity_main.xml](day2/activity_main.xml) | `app › res › layout › activity_main.xml` — [검색] 자리에 [검색] [중지] 줄과 ProgressBar |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` — `Handler`·`postDelayed`·`removeCallbacks` 버전 |
| `dayN/ControlActivity.kt`, `dayN/activity_control.xml` | 4주차 `examples/day2`와 같은 파일. 바꾸지 않는다 |
| `dayN/AndroidManifest.xml`, `dayN/res/values/themes.xml` | 4주차 `examples/day2`와 같은 파일(예제 빌드용 축약본). 내 것을 그대로 둔다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`day2/strings.xml`은 `day1`과 같다. 4주차 id(`deviceNameEdit`·`autoSwitch`·`connectButton`)와 문자열 이름은 그대로 쓴다.

## 1. 메인 스레드를 막는 코드 (넣지 않는다)

```kotlin
binding.scanButton.setOnClickListener {
    binding.stateText.text = "검색 중…"
    Thread.sleep(5000)                 // 메인 스레드가 5초 동안 멈춘다
    binding.stateText.text = "검색 완료"
}
```

실행 결과: `검색 중…`이 보이지 않고 5초 뒤 바로 `검색 완료`가 된다. 그동안 Switch도 눌리지 않는다.
Logcat에 `Skipped 299 frames!  The application may be doing too much work on its main thread.`가 남는다(숫자는 실행마다 다르다).
메인 스레드가 5초 넘게 터치에 답하지 못하면 `ANR in com.example.smartio … Input dispatching timed out`으로 앱이 멈춰 선다.

## 2. `Thread { }.start()`와 `runOnUiThread { }` — 1일차

```kotlin
binding.scanButton.setOnClickListener {
    val name = binding.deviceNameEdit.text.toString()
    binding.scanButton.isEnabled = false
    binding.stateText.text = "검색 중…"
    Thread {
        Thread.sleep(5000)
        runOnUiThread {
            binding.stateText.text = "검색 완료: $name"
            binding.scanButton.isEnabled = true
            Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
        }
    }.start()
}
```

| 줄 | 뜻 |
|---|---|
| `Thread { … }.start()` | 중괄호 안을 새 스레드에서 실행한다. 여기서 기다려도 화면은 멈추지 않는다 |
| `runOnUiThread { … }` | 화면을 바꾸는 일을 메인 스레드에 넘긴다. 워커에서 `binding.…`을 직접 바꾸면 앱이 꺼진다 |
| `isEnabled = false` | 검색 중에 [검색]을 다시 누르지 못하게 한다 |
| `val name` | 람다 바깥에서 만든 변수를 5초 뒤 실행되는 람다 안에서 그대로 쓴다 |

실행 결과: 누른 직후 `검색 중…`과 회색 버튼, 5초 뒤 `검색 완료: ESP32_BLE`와 Toast.

`runOnUiThread { }` 없이 워커에서 View를 바꾸면 5초 뒤 앱이 꺼지고 Logcat에 남는다.

```text
FATAL EXCEPTION: Thread-2
android.view.ViewRootImpl$CalledFromWrongThreadException: Only the original thread that created a view hierarchy can touch its views. Expected: main Calling: Thread-2
```

## 3. `Handler`·`postDelayed`·`removeCallbacks` — 2일차

```kotlin
private val handler = Handler(Looper.getMainLooper())   // 클래스 안, onCreate 밖
```

```kotlin
val finishScan = Runnable {                      // 검색이 끝났을 때 할 일
    binding.stateText.text = "검색 완료"
    binding.scanProgress.visibility = View.GONE
    binding.scanButton.isEnabled = true
    binding.stopButton.isEnabled = false
    Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
}

binding.scanButton.setOnClickListener {
    binding.scanButton.isEnabled = false
    binding.stopButton.isEnabled = true
    binding.stateText.text = "검색 중…"
    binding.scanProgress.visibility = View.VISIBLE
    handler.postDelayed(finishScan, 5000)        // 5초 뒤 실행 예약
}

binding.stopButton.setOnClickListener {
    handler.removeCallbacks(finishScan)          // 예약 취소
    binding.stateText.text = "검색 중지"
    binding.scanProgress.visibility = View.GONE
    binding.scanButton.isEnabled = true
    binding.stopButton.isEnabled = false
}
```

- `Handler`는 메인 스레드의 메시지 큐에 일을 넣어 준다. `postDelayed`로 넣은 일은 메인 스레드가 실행하므로 `runOnUiThread`가 필요 없다.
- 취소하려면 예약할 때 넘긴 **같은** `finishScan`을 넘겨야 한다. `removeCallbacks { }`처럼 새 중괄호를 넘기면 취소되지 않고 5초 뒤 `검색 완료`가 뜬다.
- import는 `android.os.Handler`, `android.os.Looper`, `android.view.View`다. `java.util.logging.Handler`를 고르면 `Cannot create an instance of an abstract class.` 오류가 난다.

## 4. `ProgressBar`와 `visibility`

```xml
<ProgressBar
    android:id="@+id/scanProgress"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginTop="16dp"
    android:visibility="gone" />
```

| 값 | 뜻 |
|---|---|
| `View.VISIBLE` | 보인다 |
| `View.GONE` | 안 보이고 자리도 차지하지 않는다 |
| `View.INVISIBLE` | 안 보이지만 자리는 남는다 (이번 주에는 쓰지 않는다) |

기본 ProgressBar는 끝을 모르는 작업용 돌아가는 원이다. `visibility`에 `"gone"` 같은 글자를 넣으면
`Assignment type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.` 오류가 난다.

## 5. 화면이 사라질 때 예약 지우기 (선택 — 먼저 끝났다면)

```kotlin
override fun onDestroy() {
    super.onDestroy()
    handler.removeCallbacksAndMessages(null)   // 남은 예약을 모두 지운다
}
```

[검색] 직후 화면을 돌리면 옛 화면이 사라지고 새 화면은 `대기 중`으로 시작한다. 이 줄이 없으면 5초 뒤 사라진 화면의 `finishScan`이 실행되어 Toast만 엉뚱하게 뜬다.
완성본 `day2/MainActivity.kt`에는 들어 있지 않다. 실습지 "먼저 끝났다면"의 추가 과제이며, 회전해도 검색이 이어지게 하는 것은 7주차에 한다.

## 6. 2일차 완성 — 검색·중지가 되는 연결 화면

[day2/activity_main.xml](day2/activity_main.xml)과 [day2/MainActivity.kt](day2/MainActivity.kt)를 넣고 실행한 결과:

| 조작 | 화면 |
|---|---|
| 처음 실행 | [검색] 활성, [중지] 회색, 원 없음, `대기 중` |
| [검색] | [검색] 회색, [중지] 활성, 돌아가는 원, `검색 중…` |
| 그대로 5초 | 원 사라짐, `검색 완료`, Toast `검색 완료`, [검색] 복구 |
| [검색] → 2초 뒤 [중지] | 원 사라짐, `검색 중지`, [검색] 복구. 5초가 지나도 `검색 완료`가 뜨지 않는다 |

## 공식 참고 자료

- [프로세스 및 스레드 개요 — Android Developers](https://developer.android.com/guide/components/processes-and-threads)
- [Handler — Android Developers](https://developer.android.com/reference/android/os/Handler)
- [ProgressBar — Android Developers](https://developer.android.com/reference/android/widget/ProgressBar)
