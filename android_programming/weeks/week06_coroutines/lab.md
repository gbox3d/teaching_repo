# 6주차 실습 — 코루틴 카운트다운과 가짜 연결

이번 주에는 5주차 `SmartIO`의 [검색]을 코루틴으로 다시 만든다. 처음에는 예제를 그대로 옮기고,
실행에 성공하면 [중지]와 실패 처리를 직접 완성한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 코루틴 카운트다운 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 5주차 `SmartIO`를 열어 실행하고, [검색]·[중지]의 Handler 코드를 지운다 |
| 10–30분 | `lifecycleScope.launch { }` 안에 `for … downTo`와 `delay(1000)`으로 `검색 중… 5`→`1` 카운트다운을 만든다 |
| 30–40분 | `delay`를 `Thread.sleep`으로 바꿔 관찰하고 되돌린다 |
| 40–55분 | 카운트다운을 `suspend fun countDown()`으로 묶는다 |
| 55–60분 | 실행 화면을 캡처하고 프로젝트를 저장한다 |

### 1. Handler 코드 지우기

`MainActivity.kt`에서 5주차 2일차에 넣은 `Handler` 관련 코드를 여섯 군데 지운다. 정확한 목록은 [따라하기 2단계](walkthrough.md#2-handler-코드-지우기)에 있다.

1. `private val handler = Handler(Looper.getMainLooper())` 한 줄
2. `val finishScan = Runnable { … }` 블록 전체
3. [검색] 리스너 안의 `stopButton.isEnabled = true`, `stateText.text = "검색 중…"`, `handler.postDelayed(...)` 세 줄
4. `binding.stopButton.setOnClickListener { … }` 블록 전체
5. `onDestroy()`를 넣었다면 그 블록 전체
6. `import android.os.Handler`, `import android.os.Looper`

4주차의 `connectButton`·`autoSwitch` 코드는 남긴다. [검색] 리스너에는 `isEnabled = false`와 `scanProgress.visibility = View.VISIBLE` 두 줄만 남는다.
지운 뒤 실행해서 화면이 그대로 뜨면 다음으로 간다. `handler`에 빨간 줄이 남아 있으면 5번을 확인한다.

### 2. 카운트다운 만들기

[검색] 리스너 안을 아래 모양으로 채운다. `lifecycleScope`, `launch`, `delay`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 import한다.

```kotlin
lifecycleScope.launch {
    for (i in 5 downTo 1) {
        binding.stateText.text = "검색 중… $i"
        delay(1000)
    }
    binding.stateText.text = "검색 완료"
}
```

- [검색]을 누르는 순간 `isEnabled = false`와 ProgressBar 표시(5주차 방식)를 먼저 하고, `검색 완료` 뒤에 되돌린다.
- 실행해서 `검색 중… 5`부터 `검색 중… 1`까지 1초마다 바뀌면 성공이다.
- 카운트다운 중에 장치 이름 EditText에 글자를 넣어 본다. 들어가면 화면이 멈추지 않은 것이다.

### 3. delay와 Thread.sleep 비교하기

`delay(1000)`을 `Thread.sleep(1000)`으로 **한 곳만** 바꾸고 실행한다. 관찰한 뒤 반드시 `delay(1000)`으로 되돌린다.

| 관찰할 것 | `delay(1000)` | `Thread.sleep(1000)` |
|---|---|---|
| 숫자 5→1이 하나씩 보이는가 |  |  |
| 카운트다운 중 EditText에 글자가 들어가는가 |  |  |
| 5초 뒤 `검색 완료`가 보이는가 |  |  |

### 4. countDown()으로 묶기

`for` 블록을 `private suspend fun countDown()`으로 옮기고 `launch { }` 안에서는 `countDown()` 한 줄로 부른다.

- 함수 위치는 `onCreate()`의 마지막 `}` 아래, 클래스의 마지막 `}` 위다.
- `suspend`를 빼면 `delay` 줄에 빨간 줄이 생긴다. 왜 그런지 [막혔을 때](#막혔을-때)의 문구를 읽어 본다.
- 막히면 [1일차 완성 코드](examples/day1/MainActivity.kt)와 한 줄씩 비교한다.

### 5. 오늘 확인할 것

- [ ] [검색]을 누르면 `검색 중… 5`→`1`이 1초마다 바뀌고 `검색 완료`로 끝난다.
- [ ] 카운트다운 중에 EditText에 글자를 넣을 수 있다.
- [ ] 비교표를 채웠고 코드는 `delay(1000)`으로 되돌렸다.
- [ ] `countDown()`이 `suspend fun`으로 따로 있다.

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 중지와 실패 처리 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 코드를 실행하고 `strings.xml`·`activity_main.xml`에 [다시 시도] 버튼을 추가한다 |
| 10–25분 | `scanJob`을 보관하고 [중지]에서 `cancel()`한다 → 캡처 1 |
| 25–40분 | `connectFake()`를 만든다 |
| 40–52분 | `tryConnect()`에 `try/catch`를 넣고 [검색]·[다시 시도]에서 부른다 → 캡처 2 |
| 52–60분 | 화면을 돌려 관찰하고, 최종 파일과 캡처 2장을 정리해 제출한다 |

### 1. [다시 시도] 버튼 추가하기

[따라하기 8단계](walkthrough.md#8-다시-시도-버튼-추가하기)처럼 `strings.xml`에 `retry`를, `activity_main.xml` 맨 아래에 `retryButton`을 넣는다.
`android:visibility="gone"`으로 두어 처음에는 보이지 않게 한다.

### 2. [중지] 만들기

1. 클래스 안, `binding` 선언 아래에 `private var scanJob: Job? = null`을 둔다.
2. [검색]의 `lifecycleScope.launch {` 앞에 `scanJob = `를 붙이고, [검색]을 누를 때 `stopButton.isEnabled = true`로 켠다.
3. [중지] 리스너에서 코루틴을 취소하고 ProgressBar와 버튼을 되돌린다.

```kotlin
binding.stopButton.setOnClickListener {
    scanJob?.cancel()
    // ProgressBar 숨기기, [검색] 켜기, [중지] 끄기
}
```

- `scanJob`은 아직 [검색]을 안 눌렀으면 `null`이다. 3주차 `?.`를 쓴다.
- [검색] → `검색 중… 3`에서 [중지]를 누르면 숫자가 3에서 멈추고 [검색]이 다시 눌린다. **이 화면을 캡처한다(캡처 1).**

### 3. connectFake() 만들기

`countDown()` 아래에 아래 모양의 함수를 만든다. `Random`은 Alt+Enter 목록에서 `kotlin.random.Random`을 고른다.

```kotlin
private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
    Thread.sleep(2000)
    // Random.nextBoolean()이 true면 throw Exception("연결 실패")
    true
}
```

- `Thread.sleep`은 진짜로 스레드를 막는 일이라 `withContext(Dispatchers.IO)` 안에 둔다. 1일차의 `delay`는 옮길 필요가 없다.
- 이 단계에서는 아직 부르지 않는다. 빌드만 되면 된다.

### 4. tryConnect()와 [다시 시도]

1. `connectFake()` 아래에 `private suspend fun tryConnect()`를 만든다. 안에서 `연결 중…`을 보여 주고 `try { connectFake() … } catch (e: Exception) { … }`로 감싼다.
2. 성공이면 `연결됨`을 보여 주고 4주차 `Intent`로 `ControlActivity`에 장치 이름을 넘긴다.
3. 실패면 `연결 실패`를 보여 주고 `Toast.makeText(this, e.message, …)`와 `retryButton.visibility = View.VISIBLE`.
4. [검색]의 `launch { }` 안은 `countDown()` → `stopButton.isEnabled = false` → `tryConnect()` 순서다.
5. [다시 시도] 리스너는 `lifecycleScope.launch { tryConnect() }`로 연결만 다시 한다.

| 결과 | 예상 화면 | 실제 화면 |
|---|---|---|
| 성공 |  |  |
| 실패 |  |  |
| 실패 뒤 [다시 시도] → 성공 |  |  |

실패 화면(Toast `연결 실패` + [다시 시도] 버튼)을 **캡처한다(캡처 2).** Toast는 2초 만에 사라지므로 뜨자마자 캡처한다.

### 5. 화면 돌려 보기

카운트다운 중에 에뮬레이터 화면을 돌린다. 숫자가 어떻게 되는지 한 문장으로 적는다.
이번 주에는 **관찰만** 하고 고치지 않는다. 이유와 해결은 7주차에 배운다.

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'lifecycleScope'.` | Alt+Enter로 `androidx.lifecycle.lifecycleScope`를 import한다 |
| `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` | `delay`를 부르는 함수에 `suspend`가 빠졌다. `private suspend fun countDown()`으로 쓴다 |
| `Suspend function 'suspend fun countDown(): Unit' should be called only from a coroutine or another suspend function.` | `countDown()`을 `lifecycleScope.launch { }` **밖**(클릭 리스너 바로 안)에서 불렀다. `launch { }` 안으로 옮긴다 |
| `Unresolved reference 'downto'.` | 대소문자를 본다. `downTo`다 |
| `Unresolved reference 'Job'.` 과 `Unresolved reference 'cancel'.` | `kotlinx.coroutines.Job`을 import한다 |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'kotlinx.coroutines.Job?'.` | `scanJob.cancel()`을 `scanJob?.cancel()`로 바꾼다 |
| `Unresolved reference 'Random'.` | Alt+Enter에서 `kotlin.random.Random`을 고른다 |
| `Unresolved reference 'nextBoolean'.` | import가 `java.util.Random`이다. 그 줄을 `import kotlin.random.Random`으로 바꾼다 |
| `Unresolved reference 'handler'.` | 5주차 `onDestroy()`의 `handler.removeCallbacksAndMessages(null)` 블록이 남아 있다. `override fun onDestroy() { … }` 블록 전체를 지운다 |
| `An explicit type is required on a value parameter.` / `Syntax error: Parameters must have type annotation.` | `catch (e)`를 `catch (e: Exception)`으로 쓴다 |
| `Intent(this, …)`를 `launch { }` 안에 썼더니 `None of the following candidates is applicable:` … `constructor(p0: Context!, p1: Class<*>!): Intent` | `launch { }` 안에서는 `this`가 `MainActivity`가 아니다. `Intent`·`Toast`는 `tryConnect()` 같은 클래스의 함수 안에서 쓴다 |
| 빌드는 되는데 [검색]을 누르면 5초 동안 화면이 멈추고 숫자가 안 보인다 | `delay(1000)` 대신 `Thread.sleep(1000)`이 남아 있는지 본다 |
| 빌드는 되는데 `연결 중…`에서 2초 동안 화면이 멈춘다 | `connectFake()`의 `Thread.sleep`이 `withContext(Dispatchers.IO) { }` 안에 있는지 본다 |
| 빌드는 되는데 `연결 중…` 뒤에 앱이 꺼진다. Logcat에 `FATAL EXCEPTION` 과 `java.lang.Exception: 연결 실패` | `connectFake()`를 `try { }` 없이 불렀다. `try/catch`로 감싼다 |
| [중지]를 눌러도 카운트다운이 계속된다 | `scanJob = lifecycleScope.launch {`처럼 대입했는지, [중지]에서 `scanJob?.cancel()`을 부르는지 본다 |
| [중지]가 눌리지 않는다 | XML에 `android:enabled="false"`가 있으므로 [검색]을 누를 때 `binding.stopButton.isEnabled = true`로 켜야 한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 세 가지

1. **`MainActivity.kt`**: `countDown()`, `connectFake()`, `tryConnect()`와 [검색]·[중지]·[다시 시도]가 동작하는 최종 코드
2. **캡처 1**: [중지]로 카운트다운이 멈춘 화면(예: `검색 중… 3`에서 정지, [검색]이 다시 켜진 상태)
3. **캡처 2**: `연결 실패` Toast와 [다시 시도] 버튼이 함께 보이는 화면

1일차 카운트다운과 [중지]까지 동작하면 기본 성공이다. `connectFake()`와 재시도는 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 카운트다운을 10초로 바꾸거나, `검색 중… 3`처럼 숫자만이 아니라 `검색 중… 3초 남음`으로 바꿔 본다.
- 2일차: 장치 이름이 비어 있으면 [검색]을 시작하지 않고 4주차처럼 Toast `장치 이름을 입력하세요`를 띄운다.
- 2일차: `자동 연결` Switch가 꺼져 있으면 성공해도 제어 화면으로 넘어가지 않고 `연결됨`만 보여 준다(`binding.autoSwitch.isChecked`).
- 2일차: [다시 시도]를 몇 번 눌렀는지 `var` 로 세어 `연결 실패 (2번째)`처럼 보여 준다.

추가 과제는 선택 사항이다.
