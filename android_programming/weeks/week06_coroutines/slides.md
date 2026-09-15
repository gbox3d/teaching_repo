---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 6주차
footer: 코루틴 · delay·취소·오류 처리
---

# 코루틴: delay·취소·오류 처리

5주차에는 `Handler`로 **5초 뒤에** "검색 완료"를 띄웠습니다.
이번 주에는 **1초마다 숫자를 줄이면서** 기다리고, 멈추고, 실패를 받아냅니다.

```text
검색 중… 3          연결 실패
[검색] [중지]        [검색] [중지]
                     [다시 시도]
```

---

# 1일차 — 카운트다운을 코루틴으로

`30분 설명·시연 → 60분 실습`

1. `for (i in 5 downTo 1)`로 다섯 번 반복하기
2. `lifecycleScope.launch { }` 안에서 `delay(1000)`으로 1초씩 기다리기
3. `suspend fun`으로 카운트다운을 함수 하나로 묶기

---

## 1일차 · 0–5분 — 오늘 문법: for (i in 5 downTo 1)

```kotlin
for (i in 5 downTo 1) {
    println("검색 중… $i")
}
```

```text
검색 중… 5
검색 중… 4
검색 중… 3
검색 중… 2
검색 중… 1
```

- `i`가 5, 4, 3, 2, 1로 바뀌며 중괄호 안이 **다섯 번** 실행됩니다.
- 올라가게 세려면 `for (i in 1..5)`입니다. 오늘은 `downTo`만 씁니다.

---

## 1일차 · 5–17분 ① — Handler 옆에 코루틴 놓기

```kotlin
handler.postDelayed(finishScan, 5000)   // 5주차: 5초 뒤에 한 번
```

```kotlin
// 6주차: 1초마다 한 번씩, 다섯 번
lifecycleScope.launch {
    for (i in 5 downTo 1) {
        binding.stateText.text = "검색 중… $i"
        delay(1000)
    }
    binding.stateText.text = "검색 완료"
}
```

- `launch { }` 안은 **코루틴**입니다. `delay(1000)`은 1초 기다립니다.
- 위에서 아래로 그냥 읽히는데, 화면은 멈추지 않습니다.

---

## 1일차 · 5–17분 ② — delay는 기다리고, sleep은 막는다

| | `Thread.sleep(1000)` | `delay(1000)` |
|---|---|---|
| 1초 동안 화면 | **멈춘다** (5주차) | 그대로 움직인다 |
| 숫자 `5 → 1` | 안 보이다가 마지막에 한 번 | 1초마다 바뀐다 |
| EditText 입력 | 안 된다 | 된다 |
| 쓸 수 있는 곳 | 어디서나 | `launch { }` 안 |

시연: `delay(1000)`을 `Thread.sleep(1000)`으로 바꾸고 [검색]을 누른 뒤 EditText를 눌러 봅니다.

`delay`는 기다리는 동안 메인 스레드를 **붙잡지 않습니다.** 그래서 화면이 움직입니다.

---

## 1일차 · 17–25분 ① — suspend fun은 멈췄다 이어지는 함수

```text
[검색] 클릭 ─▶ launch ─▶ "검색 중… 5" ─ delay ─ 멈춤 ┐
                                                     │ 1초 동안 화면은 자유
   ┌──────────────────────────────────────────────────┘
   └▶ "검색 중… 4" ─ delay ─ 멈춤 ┐  …  ─▶ "검색 완료"
```

- `delay`처럼 **멈췄다 이어지는** 함수에는 `suspend`가 붙어 있습니다.
- `suspend fun`은 코루틴 안이나 다른 `suspend fun` 안에서만 부를 수 있습니다.
- `suspend`는 "다른 스레드에서 돈다"는 뜻이 **아닙니다.** 그냥 멈출 수 있다는 표시입니다.

---

## 1일차 · 17–25분 ② — countDown()으로 묶기

```kotlin
private suspend fun countDown() {
    for (i in 5 downTo 1) {
        binding.stateText.text = "검색 중… $i"
        delay(1000)
    }
}
```

- 안에서 `delay`를 쓰니 `suspend`를 붙입니다. 빼면 빨간 줄이 생깁니다.
- `onCreate()` **바깥**, 클래스의 마지막 `}` 바로 위에 둡니다.
- `launch { }` 안은 `countDown()` 한 줄과 그 뒤의 `검색 완료` 두 줄만 남습니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--코루틴-카운트다운-60분) · [따라하기](walkthrough.md#1일차)

1. 5주차 [검색]의 Handler 코드를 지우고 `lifecycleScope.launch { }`로 바꿉니다.
2. `for … downTo`와 `delay(1000)`으로 `검색 중… 5`부터 `1`까지 보여 줍니다.
3. `Thread.sleep`으로 바꿔 화면이 멈추는 것을 보고 되돌린 뒤, `countDown()`으로 묶습니다.

**설명 합계: 5+12+8+5 = 30분**

`delay`가 빨간색이면 `launch { }` **안**에 있는지, `suspend`가 붙었는지 확인합니다.

---

# 2일차 — 중지와 실패 처리

`30분 설명·시연 → 60분 실습`

1. `Job.cancel()`로 [중지] 버튼 살리기
2. `withContext(Dispatchers.IO)`로 진짜 막히는 일 옮기기
3. 절반은 실패하는 `connectFake()`를 `try/catch`로 받고 [다시 시도] 보이기

---

## 2일차 · 0–5분 — 오늘 문법: try/catch와 throw

```kotlin
try {
    connectFake()
    binding.stateText.text = "연결됨"
} catch (e: Exception) {
    binding.stateText.text = "연결 실패"
}
```

```kotlin
throw Exception("연결 실패")
```

- `try` 안에서 오류가 나면 앱이 꺼지는 대신 **`catch` 안**으로 건너뜁니다.
- `throw`는 오류를 일부러 냅니다. 괄호 안 글자가 `e.message`로 전달됩니다.
- 오류가 안 나면 `catch`는 실행되지 않습니다.

---

## 2일차 · 5–13분 — Job으로 [중지] 만들기

```kotlin
private var scanJob: Job? = null      // 클래스 안, onCreate() 바깥

scanJob = lifecycleScope.launch {     // [검색] 안
    countDown()
}
```

```kotlin
binding.stopButton.setOnClickListener {
    scanJob?.cancel()
}
```

- `launch`는 시작한 코루틴을 **`Job`**으로 돌려줍니다. 변수에 보관합니다.
- 아직 [검색]을 안 눌렀으면 `null`이므로 3주차의 `?.`로 부릅니다.
- `cancel()`하면 `delay`에서 멈춰 있던 코루틴이 그 자리에서 끝납니다.

---

## 2일차 · 13–21분 — withContext(Dispatchers.IO)는 진짜 막히는 일만

| 하는 일 | 어디서 | 이유 |
|---|---|---|
| `binding.stateText.text = …` | 그냥 `launch { }` 안 | View는 메인 스레드에서만 |
| `delay(1000)` | 그냥 `launch { }` 안 | 붙잡지 않으니 옮길 필요 없음 |
| `Thread.sleep`, 파일 읽기, 네트워크 | `withContext(Dispatchers.IO) { }` | 메인 스레드를 **진짜 막는** 일 |

```kotlin
val ok = withContext(Dispatchers.IO) {
    Thread.sleep(2000)   // 여기는 다른 스레드
    true                 // 마지막 줄이 결과가 된다
}
```

`withContext`가 끝나면 다시 메인 스레드로 돌아옵니다. 5주차 `runOnUiThread`가 필요 없습니다.

---

## 2일차 · 21–27분 ① — connectFake(): 절반은 실패하는 가짜 연결

```kotlin
private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
    Thread.sleep(2000)
    if (Random.nextBoolean()) {
        throw Exception("연결 실패")
    }
    true
}
```

- 2초 걸리고, `Random.nextBoolean()`이 `true`면 오류를 던집니다.
- `: Boolean`은 참/거짓 하나를 돌려준다는 표시, `fun … = …`은 `=` 오른쪽 결과를 그대로 돌려주는 짧은 모양(중괄호 대신)입니다.
- 12주차에 진짜 BLE 연결로 바뀌어도 **부르는 쪽 코드는 같습니다.**
- `Random`은 Alt+Enter에서 **`kotlin.random.Random`**을 고릅니다. `java.util.Random`을 고르면 빌드가 안 됩니다.

---

## 2일차 · 21–27분 ② — try/catch로 받아서 [다시 시도] 보이기

```kotlin
private suspend fun tryConnect() {
    try {
        connectFake()
        binding.stateText.text = "연결됨"
        // 4주차처럼 Intent로 제어 화면 이동
    } catch (e: Exception) {
        binding.stateText.text = "연결 실패"
        Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
        binding.retryButton.visibility = View.VISIBLE
    }
}
```

- 성공: `연결됨` → 제어 화면. 실패: Toast `연결 실패` + [다시 시도] 버튼.
- `suspend fun`으로 만들면 `this`가 그대로 `MainActivity`라 `Intent`·`Toast`를 쓸 수 있습니다.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--중지와-실패-처리-60분) · [따라하기](walkthrough.md#2일차)

1. `scanJob`을 보관하고 [중지]에서 `cancel()`합니다.
2. `connectFake()`를 만들고 카운트다운 뒤에 `tryConnect()`로 부릅니다.
3. 실패하면 Toast와 [다시 시도], 성공하면 제어 화면으로 넘어가게 합니다.

**설명 합계: 5+8+8+6+3 = 30분**

`try` 없이 `throw`가 나면 앱이 그냥 꺼집니다. 꺼지면 `try/catch`부터 확인합니다.

---

## 제출하기

2일차가 끝나면 세 가지를 한 번 제출합니다.

1. **`MainActivity.kt`**: `countDown()`, `connectFake()`, `tryConnect()`가 있는 최종 코드
2. **캡처 1**: [중지]를 눌러 카운트다운이 멈춘 화면 (예: `검색 중… 3`)
3. **캡처 2**: `연결 실패` Toast와 [다시 시도] 버튼이 보이는 화면

---

## 다음 주 미리 보기

카운트다운 중에 화면을 **돌려** 보세요.

숫자는 어떻게 되었나요? `lifecycleScope`는 누구와 함께 사라질까요?

7주차에는 화면보다 오래 사는 **ViewModel**에 코루틴과 상태를 옮깁니다.
