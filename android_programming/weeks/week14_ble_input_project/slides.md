---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 14주차
footer: 안전한 명령 전송과 입력 수신·재연결
---

# 안전한 명령 전송과 입력 수신·재연결

13주차에는 보드에 명령을 **보내고** 대답을 받았습니다.
1일차에는 보내도 되는 것만 **막아서 보내고**, 2일차에는 보드에서 **받아 쌓고** 끊기면 **다시 연결**합니다.

```text
1일차                          2일차
허용되지 않는 번호   ← Toast    입력 이력            연결 화면
보드가 오류를 알렸습니다 ← 창    12:00:03 [24.5,40.0] 끊김
명령 로그가 빨강/초록          12:00:10 입력=1       [재연결]
```

두 날 모두 보드가 없어도 가짜 클라이언트(`useFake = true`)로 끝까지 할 수 있습니다.

---

# 1일차 — 막고, 알리고, 색으로 보이기

`30분 설명·시연 → 60분 실습`

1. 허용 번호 검사: `9`는 보내지 않고 Toast
2. `준비됨`일 때만, 보낸 직후 300ms는 버튼 막기
3. `result`가 `ok`가 아니면 AlertDialog와 `colors.xml` 빨간 로그
4. (확장) `SeekBar`로 `pwm 0 V`

---

## 1일차 · 0–6분 ① — 보내기 전에 번호 확인

```kotlin
if (pin.isEmpty()) {
    Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
} else if (isAllowedIndex(pin.toInt()) == false) {
    Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
} else if (isChecked) {
    // 13주차 5번: send("on $index")
```

- 순서: **빈 칸 → 허용 번호 → 켜기/끄기.** 빈 글자를 `toInt()`하면 앱이 멈추므로 빈 칸이 먼저입니다.
- 걸리면 명령도 로그도 없습니다. Logcat에 `writeCharacteristic` 줄이 **안 생기는 것**이 증거입니다.
- `== false`는 12주차처럼 "아니면"입니다.

---

## 1일차 · 0–6분 ② — isAllowedIndex()로 묶기

```kotlin
private fun isAllowedIndex(index: Int): Boolean {
    if (listOf(0, 1, 2, 3).contains(index)) {
        return true
    }
    if (index == -1) {
        return true
    }
    return false
}
```

- 10주차 `hasBlePermissions()`처럼 **참/거짓을 돌려주는** 함수입니다. 클래스 끝에 둡니다.
- `-1`(전체)도 약속된 번호라 허용합니다. 입력 칸은 `-`를 못 적어 [전체 끄기]만 보냅니다.
- `contains(pin)`처럼 **글자**를 넣으면 `Type inference failed …` 오류가 납니다. `pin.toInt()`.

---

## 1일차 · 6–14분 ① — 준비됨일 때만 누를 수 있게

```kotlin
Bleuno.client?.connectionState?.collect { state ->
    binding.stateText.text = "상태: $state"
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    if (state == ConnState.READY) {
        binding.ledSwitch.isEnabled = true
        binding.allOffButton.isEnabled = true
    }
}
```

- 12주차 4번 collect 안에 넣습니다. MainActivity 8번처럼 **먼저 끄고, 준비됨이면 켭니다.**
- XML의 `ledSwitch`·`allOffButton`에 `android:enabled="false"`: 상태가 오기 전에도 꺼져 있게.
- 13주차에 보았던 "`준비되지 않아 무시함`"이 더는 생기지 않습니다.

---

## 1일차 · 6–14분 ② — 보낸 직후 300ms 쉬기

```kotlin
private fun pauseButtons() {
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    lifecycleScope.launch {
        delay(300)
        if (Bleuno.client?.isReady == true) {
            binding.ledSwitch.isEnabled = true
            binding.allOffButton.isEnabled = true
        }
    }
}
```

- 5주차 `isEnabled` + 6주차 `launch { delay() }`. `send` 세 곳 뒤에서 `pauseButtons()`를 부릅니다.
- 300ms 사이 끊겼으면 다시 켜지 않습니다. `?. … == true`는 7주차 `scanJob?.isActive == true` 모양.

---

## 1일차 · 14–22분 ① — colors.xml과 R.color

```xml
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

```kotlin
binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
```

- `app › res › values › colors.xml`은 새 프로젝트에 이미 있습니다. **두 줄만** 더합니다.
- `strings.xml` → `R.string`처럼 `colors.xml` → `R.color`. `#AARRGGBB`, 앞 `FF`는 불투명.
- 로그 칸 **전체** 글자색이 바뀝니다. 한 줄만 바꾸는 방법은 다루지 않습니다.

---

## 1일차 · 14–22분 ② — result가 ok가 아니면 AlertDialog

```kotlin
if (result != "ok") {
    val message = BleunoMessage.message(json) ?: ""
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
    AlertDialog.Builder(this)
        .setTitle("보드가 오류를 알렸습니다")
        .setMessage("응답: $result · $message")
        .setPositiveButton("확인", null)
        .show()
} else {
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_ok))
}
```

- 13주차 `if (result != null)` 안, `append` 아래에 넣습니다. `err`·`fail` 둘 다 이 가지.
- `message`는 `String?`이라 3주차 `?:`. 응답은 `onStart`~`onStop` 사이에만 오므로 창을 띄워도 됩니다.

---

## 1일차 · 14–22분 ③ — 오류를 일부러 만들어 확인하기

정상 흐름에서는 `ok`만 옵니다. **한 곳만** 바꿔 오류 응답을 만들고, 확인한 뒤 되돌립니다.

```kotlin
Bleuno.client?.send("on$index")     // 띄어쓰기를 뺐다 (확인 뒤 "on $index"로 되돌리기)
```

```text
로그   on 3
       응답: {"result":"fail","ms":"unknown command"}      ← 빨간색
창     보드가 오류를 알렸습니다 / 응답: fail · unknown command
Logcat writeCharacteristic(가짜): "on3"
```

- 앱 로그에는 `on 3`이지만 **실제로 보낸 글자**는 Logcat의 `"on3"`입니다.
- 제어 화면에 들어온 직후 첫 조작으로 확인합니다. [전체 끄기]의 `ok`로 다시 초록이 됩니다.

---

## 1일차 · 22–26분 — (확장) SeekBar로 pwm 0 V

```kotlin
binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
    override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) { }
    override fun onStartTrackingTouch(seekBar: SeekBar?) { }
    override fun onStopTrackingTouch(seekBar: SeekBar?) {
        val value = binding.pwmSeekBar.progress
        Bleuno.client?.send("pwm 0 $value")
        binding.logText.append("pwm 0 $value\n")
        pauseButtons()
    }
})
```

- 10주차 `object : BroadcastReceiver()`와 같은 익명 객체 틀. 함수 **세 개**를 모두 적습니다.
- 끄는 동안마다 보내면 큐에 수십 개가 쌓입니다. **손을 뗄 때** 한 번. XML `android:max="255"`.

---

## 1일차 · 26–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--번호-검사와-오류-표시-60분) · [따라하기](walkthrough.md#1일차)

1. `colors.xml` 두 색 → 허용 번호 검사 → 캡처 1(`9`와 Toast)
2. `enabled="false"`와 13번 collect, `pauseButtons()`
3. 16번 오류 표시 → `"on$index"`로 확인하고 캡처 2 → 되돌리기
4. 시간이 남으면 (확장) `SeekBar` 밝기 조절

**설명 합계: 6+8+8+4+4 = 30분**

내일은 보드가 보내는 값을 받습니다. 15주차 최종 제출 조건은 [과제 안내](../week13_ble_output/project_brief.md)에 있습니다.

---

# 2일차 — 입력 받기·끊김·재연결

`30분 설명·시연 → 60분 실습`

1. `split(" ")`·`[0]`·`[1]`와 `BleunoMessage.value/event`
2. `dht11`을 3초마다 보내고 입력 이력에 쌓기
3. `끊김`이면 알리고 [재연결]
4. 10초 안에 `준비됨`이 아니면 시간 초과 안내

---

## 2일차 · 0–5분 ① — 오늘 문법: split(" ")과 [0]·[1]

```kotlin
val line = "12:00:03 [24.5,40.0]"
val parts = line.split(" ")
println(parts[0])
println(parts[1])
```

| 식 | 결과 |
|---|---|
| `line.split(" ")` | `[12:00:03, [24.5,40.0]]` — 띄어쓰기마다 자른 목록 |
| `parts[0]` / `parts[1]` | `12:00:03` / `[24.5,40.0]`. 번호는 **0부터** |
| `parts[2]` | 칸이 없다 → 실행하면 앱이 멈춘다 |

- `parts[0]`은 12주차 `addresses.get(position)`의 `get`과 같은 "번호로 꺼내기"입니다.

---

## 2일차 · 0–5분 ② — 제공 helper로 JSON에서 값 꺼내기

| 받은 JSON | `BleunoMessage.event(json)` | `BleunoMessage.value(json)` |
|---|---|---|
| `{"event":"input","index":0,"value":1}` | `"input"` | `"1"` |
| `{"result":"ok","value":"[24.5,40.0]"}` | `null` | `"[24.5,40.0]"` |
| `{"result":"ok","ms":"led(s) on"}` | `null` | `null` |

- 13주차 `BleunoMessage.result(json)`과 같은 모양입니다. 키가 없으면 `null`.
- JSON은 `split`으로 자르지 않습니다. **제공 helper**로 꺼냅니다.
- 입력 이벤트에도 `"value"`가 있습니다. 그래서 `event`를 **먼저** 봅니다.
- 입력 이벤트는 가짜 보드만 10초마다 보냅니다. 실보드는 `dht11` 응답으로 받습니다.

---

## 2일차 · 5–13분 ① — dht11을 3초마다 보내기

```kotlin
binding.inputStartButton.setOnClickListener {
    binding.inputStartButton.isEnabled = false
    binding.inputStopButton.isEnabled = true
    inputJob = lifecycleScope.launch {
        while (isActive) {
            Bleuno.client?.send("dht11")
            delay(3000)
        }
    }
}
```

- 6주차 `scanJob = lifecycleScope.launch { }` 모양. `while (isActive)` = 취소되지 않았으면 되풀이.
- [중지]·끊김·`onStop`에서 `stopInput()` → `inputJob?.cancel()`. 받지 못하는 동안은 보내지도 않습니다.

---

## 2일차 · 5–13분 ② — 받은 줄을 세 갈래로 가르기

```kotlin
val result = BleunoMessage.result(json)
val event = BleunoMessage.event(json)
val value = BleunoMessage.value(json)
if (event == "input") {
    addHistory("입력=$value")
} else if (value != null) {
    addHistory(value)
} else if (result != null) {
    binding.logText.append("응답: $json\n")
    // … 1일차 오류 색·AlertDialog 그대로
}
```

- 입력 이벤트 → 이력 `입력=1` / `dht11` 응답 → 이력 `[24.5,40.0]` / 명령 응답 → 명령 로그
- 순서를 바꾸면 이벤트가 `12:00:10 1`로 들어갑니다. 빌드는 되니 더 찾기 어렵습니다.

---

## 2일차 · 5–13분 ③ — 시각을 붙여 입력 이력에 쌓기

```kotlin
private fun addHistory(text: String) {
    val time = SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
    history.add("$time $text")
    historyAdapter.notifyDataSetChanged()
}
```

```xml
<ListView
    android:id="@+id/inputList"
    android:transcriptMode="alwaysScroll" />
```

- `SimpleDateFormat(…).format(Date())`: 지금 시각을 `12:00:03`으로 만드는 **틀**. `Date`는 `java.util.Date`.
- 11주차 장치 목록 틀 그대로: `mutableListOf` → `ArrayAdapter` → `add` → `notifyDataSetChanged()`.
- `history`는 onStart에서도 쓰므로 클래스 안에 둡니다. 회전하면 빈 목록으로 다시 시작합니다.

---

## 2일차 · 13–19분 ① — 끊김이면 알리고 [재연결] 보이기

```kotlin
ConnState.LOST -> {
    binding.scanButton.isEnabled = true
    binding.retryButton.visibility = View.VISIBLE
    binding.reconnectButton.visibility = View.VISIBLE
    showLostToast()
}
```

```kotlin
private fun showLostToast() {
    Toast.makeText(this, "연결이 끊겼습니다. [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
}
```

- 12주차 7번 collect의 `LOST` 가지에 두 줄을 더합니다. [재연결]은 끊김일 때만 보입니다.
- collect 틀 안의 `this`는 화면이 아닙니다. Toast는 **화면의 함수**로 빼서 부릅니다.

---

## 2일차 · 13–19분 ② — 주소를 저장해 두고 [재연결]

```kotlin
// 목록 줄을 누를 때(43번): 담고 저장
lastAddress = address
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
// onCreate(48번): 꺼내기
lastAddress = prefs.getString("lastAddress", "") ?: ""
// [재연결] 버튼 리스너(47번): 연결
client.connect(lastAddress)
```

- 목록 줄을 누를 때 저장, onCreate에서 꺼내기, [재연결]에서 연결합니다(11주차 틀).
- 변수에만 두면 회전하면 `""`로 돌아갑니다. 저장해 두면 앱을 껐다 켜도 남습니다.
- 끊김 Toast는 회전·[뒤로]·홈에서 돌아올 때 **또 뜹니다**. StateFlow가 마지막 값을 다시 줍니다.
- 실보드는 전원을 끕니다. Fake는 (시험용) [끊김 시험]: `val fake = client as FakeBleunoClient` → `fake.simulateLost()`
- 제어 화면에서 끊기면 Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`.

---

## 2일차 · 19–25분 ① — 10초 연결 시간 제한 걸기

```kotlin
private fun startConnectTimeout() {
    connectTimeoutJob?.cancel()
    connectTimeoutJob = lifecycleScope.launch {
        waitConnectTimeout()
    }
}
```

- 연결을 시작하는 두 곳(목록 줄 탭, [재연결])에서 부릅니다.
- 6주차 `scanJob = lifecycleScope.launch { countDown() }`와 같은 모양입니다.
- 앞 예약을 먼저 `cancel()`해서 앞 연결의 10초가 새 연결을 끊지 않게 합니다.
- 회전하면 예약이 화면과 함께 사라지므로, onCreate에서 아직 `연결 중`이면 다시 겁니다.

---

## 2일차 · 19–25분 ② — 10초 뒤에도 연결 중이면 안내하고 끊기

```kotlin
private suspend fun waitConnectTimeout() {
    delay(10000)
    val state = client.connectionState.value
    if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
        Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
        client.disconnect()
        binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
        // … ProgressBar 숨기기, [검색] 켜기, [다시 시도] 보이기
    }
}
```

- `연결 중`·`서비스 확인 중`일 **때만**. `끊김`·`준비됨`이 된 화면은 덮지 않습니다.
- 함수 안의 `this`는 화면이라 Toast를 씁니다. `delay`가 있으니 `suspend`, `10000`은 밀리초.
- Fake는 2초 만에 `준비됨` → 확인은 `delay(1000)`으로 잠깐 바꿔 보고 되돌립니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--입력-받기끊김재연결-60분) · [따라하기](walkthrough.md#2일차)

1. 제어 화면: 입력 이력 자리 → 받은 줄 가르기 → [온습도 받기 시작]·[중지]
2. 연결 화면: 주소 저장·[재연결]·(시험용) [끊김 시험] → 제어 화면 끊김 Toast
3. 이력 줄 `split` Toast → 연결 시간 제한(`delay(1000)`으로 확인하고 되돌리기)
4. 캡처 두 장: 입력 이력 2줄, `끊김` + [재연결]

**설명 합계: 5+8+6+6+5 = 30분**

**52분까지 반드시 1·2.** 3이 늦으면 미룹니다. 캡처는 세로 화면에서 찍습니다.

---

## 제출하기

1일차와 2일차에 각각 한 번 냅니다.

1. **1일차**: `ControlActivity.kt`, `activity_control.xml`, 캡처 1(`9`와 `허용되지 않는 번호` Toast), 캡처 2(빨간 로그와 오류 대화상자)
2. **2일차**: `ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`·`activity_main.xml`, 캡처 1(입력 이력 2줄), 캡처 2(`끊김`과 [재연결])

캡처는 세로 화면에서 찍고, 계정 이름·알림 내용이 보이지 않게 합니다.

---

## 다음 주 미리 보기

15주차는 **기말고사(개인 실기)**와 **과제 최종 제출**입니다.

- 공개 starter(화면 / 제공 `bleuno/` / 상수) 위에 세 기능: 권한 확인 흐름, 번호 토글(`send`)과 응답 표시, 연결 시간 제한 안내
- 과제는 13주차에 발표한 계획안대로 완성한 앱 + 캡처 세트 + 레포트를 냅니다([과제 안내](../week13_ble_output/project_brief.md)).
