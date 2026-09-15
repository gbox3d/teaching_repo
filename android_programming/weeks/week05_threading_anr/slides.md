---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 5주차
footer: 메인 스레드와 백그라운드 · Thread · Handler
---

# 메인 스레드와 백그라운드: Thread·Handler

4주차에 만든 연결 화면에 **[검색]** 버튼을 답니다.
5초 걸리는 검색을 흉내 내면서 화면이 **멈추지 않게** 만드는 것이 이번 주 목표입니다.

```text
Smart I/O Controller
장치 이름 [ESP32_BLE      ]
자동 연결                 (  )
      [검색] [중지]
         ◌
       검색 중…
        [연결]
```

---

# 1일차 — 화면이 멈추지 않게: 메인 스레드와 Thread

`30분 설명·시연 → 60분 실습`

1. 오늘 문법: 람다 안에서 바깥 변수 쓰기
2. [검색]에 `Thread.sleep(5000)`을 넣으면 생기는 일
3. `Thread { }.start()`와 `runOnUiThread { }`

---

## 1일차 · 0–5분 — 오늘 문법: 람다 안에서 바깥 변수 쓰기

```kotlin
var count = 0                          // 람다 바깥
plusButton.setOnClickListener {        // 람다 { }
    count = count + 1                  // 바깥 변수를 바꾼다 (2주차)
}
```

```kotlin
val name = binding.deviceNameEdit.text.toString()   // 람다 바깥
Thread {
    Thread.sleep(5000)
    runOnUiThread { binding.stateText.text = "검색 완료: $name" }
}.start()
```

- `{ }` 안에서는 바깥에서 만든 변수를 그대로 읽고 바꿀 수 있습니다.
- 람다가 **5초 뒤에** 실행돼도 `name`을 기억하고 있습니다.

---

## 1일차 · 5–15분 ① — [검색]에 Thread.sleep(5000)을 넣으면

```kotlin
binding.scanButton.setOnClickListener {
    binding.stateText.text = "검색 중…"
    Thread.sleep(5000)                 // 5초 동안 기다린다 (잘못된 코드)
    binding.stateText.text = "검색 완료"
}
```

관찰:

- `검색 중…`이 화면에 **보이지 않고**, 5초 뒤 바로 `검색 완료`가 됩니다.
- 그동안 Switch도 [연결]도 눌리지 않습니다.
- Logcat: `Skipped 299 frames! The application may be doing too much work on its main thread.` (숫자는 실행마다 다름)

---

## 1일차 · 5–15분 ② — 메인 스레드와 메시지 큐

```text
터치 ─┐
그리기 ┼─▶ 메시지 큐 ─▶ 메인 스레드가 하나씩 처리
클릭 ─┘                     │
                    한 일이 길면 뒤의 일이 모두 기다린다
```

- 화면을 그리는 일과 버튼 클릭은 **메인 스레드** 한 줄에서 순서대로 처리됩니다.
- `Thread.sleep(5000)`은 이 줄을 5초 동안 막습니다. 그래서 글자도 안 바뀌고 버튼도 안 눌립니다.
- `stateText.text = "검색 중…"`은 큐에 “다시 그려 달라”고 넣은 것일 뿐, 그리는 일은 클릭 처리가 끝난 뒤입니다.

---

## 1일차 · 5–15분 ③ — ANR: 응답 없음

메인 스레드가 **5초 넘게** 터치에 답하지 못하면 시스템이 앱을 멈춰 세웁니다.

```text
ANR in com.example.smartio (com.example.smartio/.MainActivity)
Reason: Input dispatching timed out (... Waited 5002ms for MotionEvent).
```

- ANR = Application Not Responding. “앱이 응답하지 않습니다” 대화상자가 뜰 수 있습니다.
- 규칙 하나: **메인 스레드에서는 오래 기다리는 일을 하지 않는다.**
- 그러면 5초 기다리는 일은 누가 할까요? → 다른 스레드

---

## 1일차 · 15–25분 ① — Thread { }.start()와 runOnUiThread { }

```kotlin
binding.scanButton.isEnabled = false
binding.stateText.text = "검색 중…"
Thread {                               // 새 스레드에서 할 일
    Thread.sleep(5000)                 // 여기서 기다려도 화면은 멈추지 않는다
    runOnUiThread {                    // 화면을 바꾸는 일은 메인 스레드에 맡긴다
        binding.stateText.text = "검색 완료"
        binding.scanButton.isEnabled = true
    }
}.start()                              // start()를 빠뜨리면 아무 일도 안 일어난다
```

```text
메인: 클릭 → "검색 중…" 표시 → Thread 시작 → (자유롭게 그리기·클릭 처리) → "검색 완료"·버튼 복구
워커:                   5초 대기 ──▶ runOnUiThread { … } ──▶ 메인에 넘김 ─┘
```

---

## 1일차 · 15–25분 ② — 워커 스레드에서 View를 만지면

```kotlin
Thread {
    Thread.sleep(5000)
    binding.stateText.text = "검색 완료"      // runOnUiThread 없이 바꾸면?
}.start()
```

앱이 꺼지고 Logcat에 이렇게 남습니다.

```text
FATAL EXCEPTION: Thread-2
android.view.ViewRootImpl$CalledFromWrongThreadException:
Only the original thread that created a view hierarchy can touch its views.
Expected: main Calling: Thread-2
```

- View는 **메인 스레드만** 바꿀 수 있습니다. 워커에서는 `runOnUiThread { }`로 감쌉니다.
- `isEnabled = false`로 검색 중에 [검색]을 다시 못 누르게 막습니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--검색-버튼을-멈추지-않게-만들기-60분) · [따라하기](walkthrough.md#1일차)

1. 연결 화면에 [검색] 버튼과 상태 TextView를 추가합니다.
2. 누르면 버튼을 비활성화하고 `검색 중…`을 보입니다.
3. `Thread`에서 5초 기다린 뒤 `runOnUiThread`로 `검색 완료`·버튼 복구·Toast.

**설명 합계: 5+10+10+5 = 30분**

막히면 `.start()`, `runOnUiThread { }` 안에 View 코드가 있는지부터 확인합니다.

---

# 2일차 — 예약과 취소: Handler·postDelayed·ProgressBar

`30분 설명·시연 → 60분 실습`

1. 작년 BLE 특강 코드에서 `postDelayed` 찾기
2. `Handler(Looper.getMainLooper())`로 5초 뒤 일 예약하고 [중지]로 취소하기
3. `ProgressBar`로 검색 중임을 보여 주기

---

## 2일차 · 0–5분 — 작년 특강 코드 한 조각: postDelayed

강의자의 BLE 테스트 앱(12주에 다시 봅니다)에서 검색을 5초 뒤에 멈추는 부분입니다.

```kotlin
private val mHandlerBleScanTimeout = Handler(Looper.getMainLooper())

bluetoothLeScanner.startScan(mScanCallback)
mHandlerBleScanTimeout.postDelayed({
    bluetoothLeScanner.stopScan(mScanCallback)
    Log.d("MainActivity", "scan timeout")
}, 5000)
```

- “5초 뒤에 이 코드를 실행해 줘”를 **한 줄**로 씁니다. 새 스레드도, `sleep`도 없습니다.
- 오늘은 이 한 줄을 우리 [검색]에 옮깁니다.

---

## 2일차 · 5–15분 ① — Handler(Looper.getMainLooper())와 postDelayed

```kotlin
private val handler = Handler(Looper.getMainLooper())   // 클래스 안, onCreate 밖
```

```kotlin
handler.postDelayed({
    binding.stateText.text = "검색 완료"      // 메인 스레드에서 실행된다
}, 5000)
```

- `Handler`는 메인 스레드의 **메시지 큐에 일을 넣어 주는 손잡이**입니다.
- `postDelayed(할 일, 밀리초)`: 큐에 “5000ms 뒤에 실행” 표를 붙여 넣습니다.
- 메인 스레드가 실행하므로 `runOnUiThread`가 필요 없습니다.
- `Handler`·`Looper`가 빨간색이면 Alt+Enter → `android.os` 것을 고릅니다.
- 이 형태(이름 없는 `{ }`)는 **취소할 수 없습니다** → 다음 장에서 이름을 붙입니다.

---

## 2일차 · 5–15분 ② — 이름 붙인 일 Runnable과 removeCallbacks

```kotlin
val finishScan = Runnable {            // 할 일에 이름을 붙여 둔다
    binding.stateText.text = "검색 완료"
    binding.scanButton.isEnabled = true
}

handler.postDelayed(finishScan, 5000)  // [검색]: 5초 뒤 실행 예약
handler.removeCallbacks(finishScan)    // [중지]: 그 예약을 취소
```

- 취소하려면 **같은 이름**을 넘겨야 합니다. `removeCallbacks { }`처럼 새 `{ }`를 주면 취소되지 않습니다.
- `removeCallbacks`는 **아직 실행되지 않은** 예약만 뺍니다. 이미 실행된 뒤에는 할 일이 없습니다.

---

## 2일차 · 15–25분 ① — ProgressBar: 돌아가는 원

```xml
<ProgressBar
    android:id="@+id/scanProgress"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:visibility="gone" />
```

```kotlin
binding.scanProgress.visibility = View.VISIBLE   // 보이기
binding.scanProgress.visibility = View.GONE      // 자리까지 없애기
```

- 기본 ProgressBar는 끝을 모르는 작업용 **돌아가는 원**입니다. 숫자는 필요 없습니다.
- `View`가 빨간색이면 Alt+Enter → `android.view.View`.

---

## 2일차 · 15–25분 ② — 검색 중과 아닐 때 화면 표

| 상황 | [검색] | [중지] | ProgressBar | 상태 글자 |
|---|---|---|---|---|
| 처음 | 활성 | 비활성 | `GONE` | `대기 중` |
| [검색] 누름 | 비활성 | 활성 | `VISIBLE` | `검색 중…` |
| 5초 뒤 `finishScan` | 활성 | 비활성 | `GONE` | `검색 완료` + Toast |
| [중지] 누름 | 활성 | 비활성 | `GONE` | `검색 중지` |

- 한 상황마다 **네 가지**를 함께 바꿉니다. 하나라도 빠지면 버튼이 눌리지 않거나 원이 계속 돕니다.
- XML에서 [중지]는 `android:enabled="false"`, ProgressBar는 `android:visibility="gone"`으로 시작합니다.

---

## 2일차 · 25–30분 — AsyncTask 한 줄, 이제 직접 해 보기

[2일차 실습](lab.md#2일차--handler로-예약하고-중지로-취소하기-60분) · [따라하기](walkthrough.md#2일차)

1. 1일차의 `Thread`를 `handler.postDelayed(finishScan, 5000)`으로 바꿉니다.
2. [중지] 버튼: `removeCallbacks(finishScan)` + 화면 되돌리기.
3. 검색 중에만 ProgressBar가 보이게 합니다.

옛날 코드에는 `AsyncTask`라는 도구가 보입니다. 지금은 쓰지 않는 레거시이고, 우리는 6주차부터 **코루틴**을 씁니다.

**설명 합계: 5+10+10+5 = 30분**

---

## 제출하기

2일차가 끝나면 세 가지를 한 번 제출합니다.

1. **`MainActivity.kt`**
2. **`activity_main.xml`**
3. **실행 화면 캡처 2장**: 검색 중(버튼 비활성·ProgressBar 표시) 화면, `검색 완료` Toast가 보이는 화면 또는 [중지]를 누른 뒤 화면

---

## 다음 주 미리 보기

검색 중에 남은 시간을 `5, 4, 3, 2, 1`로 세어 보이려면 `postDelayed`를 다섯 번 겹쳐 써야 합니다.

6주차에는 **코루틴**의 `delay(1000)` 한 줄로 카운트다운을 만들고, 가짜 연결이 실패했을 때 [다시 시도]하는 흐름을 만듭니다.
