# 14주차 예제 — 입력 받기·끊김·재연결 (최종 완성 앱)

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)의 **최종 완성본**이다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
시작점은 13주차 `examples/day2`이고, 1일차에 입력 받기·끊김·재연결·연결 시간 제한을 더했다. 2일차는 2차 과제 발표라 예제가 없다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다. 2차 과제 조건은 [과제 안내](../project_brief.md)에 있다.
아래 "실행 결과" 표와 멈춤 증상은 Android 14 에뮬레이터에서 Fake로 실행해 확인했다. 실보드에서만 볼 수 있는 결과(6절 표의 실보드 줄, 8절 Logcat)는 확인하지 못한 **예상**이다. 오류 문구(`Unresolved reference …` 등)는 빌드로 확인한 원문이다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/ControlActivity.kt](day1/ControlActivity.kt) | `app › kotlin+java › com.example.smartio › ControlActivity.kt` | import 6개(`ArrayAdapter`·`Job`·`isActive`·`SimpleDateFormat`·`Date`·`Locale`), 클래스 안 `history`·`historyAdapter`·`inputJob`, 어댑터 연결(18번), [온습도 받기 시작]·[중지] 버튼(19·20번), 받은 JSON 가르기(21~23번), `addHistory`(24번), `stopInput`과 부르는 곳(25~27번), 이력 줄 누르기(28번), 끊김 Toast(29·30번) |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `MainActivity.kt` | import 3개(`FakeBleunoClient`·`Job`·`delay`), 클래스 안 `lastAddress`·`connectTimeoutJob`, 주소 기억·저장(43번), [재연결] 숨기기·보이기·Toast(44~46번), [재연결] 리스너(47번), 주소 꺼내기(48번), 연결 시간 제한(49~52번), (시험용) [끊김 시험] 버튼(53~55번) |
| [day1/activity_control.xml](day1/activity_control.xml) | `app › res › layout › activity_control.xml` | `logText` 아래에 [온습도 받기 시작]·[중지] 가로 줄, 제목 `입력 이력`, `inputList`(ListView) |
| [day1/activity_main.xml](day1/activity_main.xml) | `activity_main.xml` | `retryButton` 아래에 [재연결]·[끊김 시험] 가로 줄(둘 다 처음엔 숨김) |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `input_start`·`input_history_title`·`reconnect`·`lost_test` 추가. [중지]는 기존 `stop`을 다시 쓴다 |
| `day1/ContactsReader.kt`, [day1/colors.xml](day1/colors.xml) | 연락처 읽기·색 | 13주차 그대로, 바꾸지 않는다 |
| [day1/bleuno/](day1/bleuno) 8개 | `app › kotlin+java › com.example.smartio › bleuno` | 12주차에 넣은 제공 코드 그대로. [bleuno/src](../../../bleuno/src)와 같다 |
| `day1/AndroidManifest.xml`, `day1/res/values/themes.xml` | Manifest·테마 | 12주차 그대로. `dht11` 보내기와 재연결은 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 들어 있다 |

`.kt` 파일 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
새로 쓴 `ArrayAdapter`·`Job`·`SimpleDateFormat`은 4주차 의존성과 Android 기본 API에 들어 있어 `build.gradle.kts`에 더할 것이 없다.
주석 번호는 13주차까지에 이어 `ControlActivity.kt` 18~30번, `MainActivity.kt` 43~55번이다. 번호는 수업에서 넣는 순서라 한 덩어리 안에서는 차례대로 놓이지만 파일 전체로는 흩어진다(24·25·30번, 46·50·51번은 파일 끝 함수). 같은 한 줄 `startConnectTimeout()`은 두 곳에 같은 49번을 달았다.
13주차 코드에서 **바꾼 줄은 하나뿐**이다: `ControlActivity.kt` 9번 응답 처리의 `if (result != null) {`가 `} else if (result != null) {`(195행)가 되었다. 나머지는 모두 줄을 더했다.

**(시험용) 표시**: [끊김 시험] 버튼은 보드 없이 가짜 보드로 "끊김"을 만들어 보는 시험용이다(53~55번 주석 첫머리 `(시험용)`). 넣지 않으려면 `activity_main.xml`의 `lostTestButton`, `strings.xml`의 `lost_test`, `import com.example.smartio.bleuno.FakeBleunoClient`, 53·54·55번 줄을 넣지 않는다.

## 1. `split(" ")`, `[0]`, `[1]` — 이력 한 줄을 시각과 값으로 나누기

```kotlin
binding.inputList.setOnItemClickListener { _, _, position, _ ->
    val parts = history[position].split(" ")
    val time = parts[0]
    val value = parts[1]
    Toast.makeText(this, "받은 시각: $time · 값: $value", Toast.LENGTH_SHORT).show()
}
```

| 누른 줄 `history[position]` | `split(" ")` 결과 `parts` | Toast |
|---|---|---|
| `12:00:03 [24.5,40.0]` | `[12:00:03, [24.5,40.0]]` | `받은 시각: 12:00:03 · 값: [24.5,40.0]` |
| `12:00:10 입력=1` | `[12:00:10, 입력=1]` | `받은 시각: 12:00:10 · 값: 입력=1` |

- `history[position]`은 12주차 `addresses.get(position)`과 같다. 대괄호 안 번호는 0부터 센다.
- `split(" ")`은 띄어쓰기가 있는 곳마다 글자를 잘라 목록으로 돌려준다. 이력 줄은 늘 `시각 값` 모양이라(24번) `[0]`과 `[1]`이 있다. 그래서 입력 이벤트도 `입력=1`처럼 띄어쓰기 없이 적었다(22번).
- `[position]`을 빠뜨리고 `history.split(" ")`이라 쓰면 `Unresolved reference 'split'.`이 난다. 목록 전체에는 `split`이 없다. 아래 두 줄에 따라 나오는 `Cannot infer type for this parameter. Please specify it explicitly.`는 첫 오류를 고치면 사라진다.
- 문자열 안에 `"받은 시각: $parts[0]"`처럼 바로 쓰면 빌드는 되지만 `$`가 `parts`까지만 읽어서 Toast가 `받은 시각: [12:00:03, [24.5,40.0]][0]`이 된다. 한 번 `val time`에 담아 `$time`으로 쓴다.
- 없는 칸 `parts[2]`도 빌드는 되지만, 줄을 누르는 순간 앱이 멈춘다(Logcat `java.lang.IndexOutOfBoundsException`).

## 2. `BleunoMessage.event`·`value` — 받은 JSON 가르기

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
    // … 13주차 오류 색·AlertDialog 그대로
}
```

| 받은 JSON | `event` | `value` | `result` | 들어가는 곳 |
|---|---|---|---|---|
| `{"event":"input","index":0,"value":1}` (가짜 보드가 10초마다) | `"input"` | `"1"` | `null` | 입력 이력 `12:00:10 입력=1` |
| `{"result":"ok","value":"[24.5,40.0]"}` (`dht11` 응답) | `null` | `"[24.5,40.0]"` | `"ok"` | 입력 이력 `12:00:03 [24.5,40.0]` |
| `{"result":"ok","ms":"led(s) on"}` | `null` | `null` | `"ok"` | 명령 로그 `응답: {…}` (초록) |
| `{"result":"fail","ms":"unknown command"}` | `null` | `null` | `"fail"` | 명령 로그(빨강) + AlertDialog |

- 입력 이벤트에도 `"value"`가 있으므로 `event` 검사를 **먼저** 한다. 순서를 바꾸면 빌드는 되지만 이벤트가 `12:00:10 1`처럼 숫자 한 줄로 들어간다.
- 세 helper는 키가 없으면 `null`을 돌려주는 `String?`이다. `addHistory(BleunoMessage.value(json))`처럼 바로 넘기면 `Argument type mismatch: actual type is 'kotlin.String?', but 'kotlin.String' was expected.` 위에서 `if (value != null)`로 확인한 변수 `value`를 넘긴다.
- 실제 보드는 펌웨어에 입력 이벤트를 더하기 전까지 이벤트를 보내지 않는다. 실보드에서는 `dht11` 응답으로 입력을 받는다.

## 3. `while (isActive)` — 3초마다 `dht11` 보내고 멈추기

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

```kotlin
private fun stopInput() {
    inputJob?.cancel()
    binding.inputStartButton.isEnabled = false
    binding.inputStopButton.isEnabled = false
    if (Bleuno.client?.isReady == true) {
        binding.inputStartButton.isEnabled = true
    }
}
```

| 실행 결과 (Fake, `준비됨` 제어 화면) | 버튼 | 입력 이력 |
|---|---|---|
| [온습도 받기 시작] | [온습도 받기 시작] 꺼짐, [중지] 켜짐 | 약 0.3초 뒤 `12:00:03 [24.5,40.0]`, 이어서 3초마다 `[25.0,41.0]`, `[25.5,42.0]`, `[24.5,40.0]`… |
| [중지] | [온습도 받기 시작] 켜짐, [중지] 꺼짐 | `dht11` 줄이 멈춘다(입력 이벤트 줄은 계속 10초마다) |
| 받는 중 홈 → 앱으로 돌아옴 | [온습도 받기 시작] 켜짐, [중지] 꺼짐 | 나가기 전 줄 그대로 |
| 받는 중 회전(가로에서 안 보이면 세로로 되돌려 확인, 숫자 키보드가 뜨면 닫는다) | [온습도 받기 시작] 켜짐, [중지] 꺼짐 | 빈 목록으로 다시 시작 |

- `stopInput()`은 [중지] 버튼(20번), 연결 상태가 바뀔 때(26번, collect 안), `onStop`(27번) 세 곳에서 부른다. 응답을 받지 않는 동안에는 요청도 보내지 않는다.
- `isActive`는 따로 import한다. 빠뜨리면 `Unresolved reference 'isActive'.` — 빨간 글자에서 Alt+Enter → Import.
- `inputJob =`을 빠뜨리면 빌드는 되지만 [중지]를 눌러도 반복이 멈추지 않는다. 6주차 `scanJob = lifecycleScope.launch`와 같은 이유다.
- Logcat `package:mine tag:BLE`: `writeCharacteristic(가짜): "dht11"` → `onCharacteristicChanged(가짜): {"result":"ok","value":"[24.5,40.0]"}`가 3초마다 찍힌다.

## 4. 입력 이력 `ListView` — 시각을 붙여 쌓기

```kotlin
private val history = mutableListOf<String>()
private lateinit var historyAdapter: ArrayAdapter<String>
```

```kotlin
historyAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, history)
binding.inputList.adapter = historyAdapter
```

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
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="2"
        android:layout_marginTop="8dp"
        android:transcriptMode="alwaysScroll" />
```

- `SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())`는 지금 시각을 `12:00:03`(시:분:초) 글자로 만드는 틀이다. `Date`는 `java.util.Date`를 import한다.
- `transcriptMode="alwaysScroll"`이라 새 줄이 들어오면 목록이 맨 아래로 내려간다. `layout_weight="2"`는 위 명령 로그(`1`)와 남은 높이를 1:2로 나눈다.
- 11주차 장치 목록과 같은 틀이다. `add` 뒤에 `notifyDataSetChanged()`를 빠뜨리면 목록이 늘지 않는다.
- XML id와 Kotlin 이름이 다르면 `Unresolved reference 'inputList'.`가 Kotlin 파일에 뜬다. 고칠 곳은 XML id다.

## 5. 끊김과 [재연결] — 마지막 주소를 저장해 두기

```kotlin
// 목록 줄을 누를 때(43번)
lastAddress = address
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
```

```kotlin
// onCreate(48번)
lastAddress = prefs.getString("lastAddress", "") ?: ""
```

```kotlin
// 7번 collect(44·45번)
binding.reconnectButton.visibility = View.GONE
when (state) {
    // …
    ConnState.LOST -> {
        binding.scanButton.isEnabled = true
        binding.retryButton.visibility = View.VISIBLE
        binding.reconnectButton.visibility = View.VISIBLE
        showLostToast()
    }
}
```

```kotlin
// [재연결] 버튼(47번)
binding.reconnectButton.setOnClickListener {
    if (lastAddress.isEmpty()) {
        Toast.makeText(this, "마지막 주소가 없습니다. [검색]부터 하세요", Toast.LENGTH_SHORT).show()
    } else {
        client.connect(lastAddress)
        startConnectTimeout()
    }
}
```

| 실행 결과 | 화면 |
|---|---|
| 연결 화면 `준비됨`에서 [끊김 시험] (실보드는 보드 전원 끄기) | 상태 `끊김`, Toast `연결이 끊겼습니다. [재연결]을 누르세요`, [검색] 켜짐, [다시 시도]·[재연결] 보임 |
| 제어 화면에 있는 동안 끊김 (실보드 전원 끄기) | `상태: 끊김`, Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`, 버튼 모두 꺼짐 → [뒤로]를 누르면 연결 화면에 [재연결] |
| [재연결] | [재연결]·[다시 시도] 숨겨짐, `연결 중` → `서비스 확인 중` → `준비됨` |
| 끊김에서 회전하거나 제어 화면에서 [뒤로]로 돌아온 뒤 [재연결] | 끊김 Toast가 한 번 더 뜨고, [재연결]은 저장해 둔 주소로 연결한다 |

- 주소를 `var`에만 두면 화면이 새로 만들어질 때(회전, 제어 화면에 간 동안의 회전) 빈 글자로 돌아간다. 11주차 SharedPreferences로 저장하고 onCreate에서 다시 꺼낸다.
- `getString`은 `String?`를 돌려준다. `?: ""`를 빠뜨리면 `Assignment type mismatch: actual type is 'kotlin.String?', but 'kotlin.String' was expected.`
- collect 틀 안에서 `Toast.makeText(this, …)`를 바로 쓰면 `None of the following candidates is applicable:`와 `Unresolved reference 'show'.`가 난다. 그 틀 안의 `this`는 Activity가 아니다. Toast를 Activity의 함수(`showLostToast()`)로 빼서 부른다.
- 끊김 Toast는 끊김인 채로 화면이 다시 보일 때마다(회전, [뒤로], 홈에서 돌아옴) 또 뜬다. StateFlow가 마지막 값을 다시 주기 때문이며 정상 동작이다.

## 6. 연결 시간 제한 — 10초 안에 준비됨이 아니면

```kotlin
private fun startConnectTimeout() {
    connectTimeoutJob?.cancel()
    connectTimeoutJob = lifecycleScope.launch {
        waitConnectTimeout()
    }
}

private suspend fun waitConnectTimeout() {
    delay(10000)
    val state = client.connectionState.value
    if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
        Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
        client.disconnect()
        binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
        binding.retryButton.visibility = View.VISIBLE
    }
}
```

```kotlin
// onCreate(52번): 연결 중에 회전했으면 시간 제한을 다시 건다
if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(client.connectionState.value)) {
    startConnectTimeout()
}
```

| 실행 결과 | 화면 |
|---|---|
| Fake 목록 줄 누르기 | 약 2초 만에 `준비됨`. 10초가 지나도 Toast 없음 |
| (확인용) 51번 `delay(10000)`을 잠시 `delay(1000)`으로 바꾸고 목록 줄 누르기 | 약 1초 뒤 상태 `연결 시간 초과 — [다시 시도]를 누르세요`, [검색] 켜짐, [다시 시도] 보임. Toast `연결 시간이 초과되었습니다`는 `선택: …` Toast 다음(누르고 약 2초)에 뜬다. 확인한 뒤 되돌린다 |
| 실보드 전원을 끈 뒤 목록에 남은 줄 누르기 | 10초 뒤 같은 Toast와 화면. 기기에 따라 잠시 뒤 `연결 안 됨`으로 바뀐다 |
| `연결 중`에 회전 | 52번이 시간 제한을 다시 건다(10초를 처음부터 센다) |

- 조건을 "연결 중·서비스 확인 중일 때만"으로 쓴다. 그사이 `준비됨`이나 `끊김`이 되었다면 건드리지 않아야 [재연결]이 보이는 화면을 덮지 않는다.
- 아직 맺어지지 않은 연결을 끊으면 "끊겼다"는 알림이 오지 않는 기기가 있다. 그러면 상태가 `연결 중`에 머물러 7번이 화면을 고치지 않으므로, `disconnect()` 뒤에 화면을 직접 되돌린다.
- 앞 연결의 예약이 남아 새 연결을 끊지 않도록 `connectTimeoutJob?.cancel()`을 먼저 한다.
- `suspend`를 빠뜨리면 `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.`
- `delay`의 숫자는 밀리초다. `delay(10)`이라 적으면 0.01초 만에 시간 초과가 되어 준비됨까지 가지 못한다.

## 7. (시험용) [끊김 시험] — 보드 없이 끊김 만들기

```kotlin
if (useFake) {
    binding.lostTestButton.visibility = View.VISIBLE
}
binding.lostTestButton.setOnClickListener {
    val fake = client as FakeBleunoClient
    fake.simulateLost()
}
```

- `useFake = true`일 때만 보이고, `준비됨`일 때만 켜진다(53·54번). 실보드는 이 버튼 대신 보드 전원을 꺼서 시험한다.
- `simulateLost()`는 가짜 클라이언트에만 있어서 `as FakeBleunoClient`로 "가짜 클라이언트로 보고" 꺼낸 뒤 부른다. 이 한 줄은 복사해 쓰는 시험용 틀이며 채점하지 않는다.
- Logcat `tag:BLE`: `simulateLost(가짜) → 끊김`.

## 8. 최종 앱 흐름

[day1](day1) 파일을 모두 넣고 실행한 흐름:

```text
[권한 확인] ▶ [검색] ▶ 목록 줄 탭 ─ 주소 저장, 10초 시간 제한 시작
   ├─ 10초 안에 준비됨 ▶ [제어 화면]
   │     LED Switch ▶ send("on 3") ▶ 명령 로그
   │     [온습도 받기 시작] ▶ 3초마다 send("dht11") ▶ 입력 이력 "시각 [온도,습도]"
   │     (가짜 보드) 10초마다 입력 이벤트 ▶ 입력 이력 "시각 입력=1"
   │     이력 줄 탭 ▶ split(" ") ▶ Toast "받은 시각: … · 값: …"
   │     끊김 ▶ 받기 멈춤 + Toast "[뒤로] → [재연결]"
   │  [뒤로] ▶ 연결 화면
   └─ 10초가 지나도 연결 중 ▶ Toast "연결 시간이 초과되었습니다" ▶ [다시 시도]
끊김 ▶ Toast + [재연결] ▶ 저장한 주소로 connect ▶ 준비됨
```

실보드에서 온습도를 한 번 받을 때 Logcat `tag:BLE`에 남는 줄([bleuno README](../../../bleuno/README.md)):

```text
send: 큐에 추가 "dht11" (대기 1개)
writeCharacteristic("dht11") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","value":"[24.5,40.0]"}
```

## 공식 참고 자료

- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [키-값 데이터 저장(SharedPreferences) — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [코루틴 취소와 시간 제한 — Kotlin](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [split — Kotlin 표준 라이브러리](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/split.html)
