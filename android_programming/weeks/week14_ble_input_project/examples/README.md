# 14주차 예제 — 안전한 명령 전송과 입력 수신·재연결

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
`day1/`은 1일차 완성본(허용 번호 검사·버튼 막기·오류 표시), `day2/`는 2일차 완성본이며 이 과목의 **최종 완성 앱**이다. 1일차 시작점은 13주차 `../../week13_ble_output/examples/day1`이고, 2일차 시작점은 이 폴더의 `day1`이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다. 15주차 과제 조건은 [13주차 과제 안내](../../week13_ble_output/project_brief.md)에 있다.
아래 "실행 결과" 표와 멈춤 증상은 Android 14 에뮬레이터에서 Fake로 실행해 확인했다. 실보드에서만 볼 수 있는 결과(9절 표의 실보드 줄, 11절 Logcat)는 확인하지 못한 **예상**이다. 오류 문구(`Unresolved reference …` 등)는 빌드로 확인한 원문이다.

## 1일차 파일과 넣을 위치 (`day1/`)

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 1일차 변경 |
|---|---|---|
| [day1/ControlActivity.kt](day1/ControlActivity.kt) | `app › kotlin+java › com.example.smartio › ControlActivity.kt` | import 4개(`ConnState`·`delay`·`ContextCompat`·`AlertDialog`, 확장은 `SeekBar`), 허용 번호 가지(11번), `isAllowedIndex()`(12번), collect에서 버튼 켜고 끄기(13번), `send` 뒤 `pauseButtons()`(14번), `pauseButtons()`(15번), 오류 표시(16번), (확장) `SeekBar` 리스너(17번) |
| [day1/activity_control.xml](day1/activity_control.xml) | `app › res › layout › activity_control.xml` | `ledSwitch`·`allOffButton`에 `android:enabled="false"`, (확장) `pwmSeekBar` 가로 줄 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | (확장) `pwm_title` 추가 |
| [day1/colors.xml](day1/colors.xml) | `app › res › values › colors.xml` | `log_ok`(초록)·`log_error`(빨강) 두 줄 추가 |
| `day1/MainActivity.kt`, `day1/activity_main.xml`, `day1/ContactsReader.kt` | 연결 화면·연락처 읽기 | 13주차 그대로, 1일차에는 바꾸지 않는다 |

## 2일차 파일과 넣을 위치 (`day2/`)

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 2일차 변경 |
|---|---|---|
| [day2/ControlActivity.kt](day2/ControlActivity.kt) | `ControlActivity.kt` | import 6개(`ArrayAdapter`·`Job`·`isActive`·`SimpleDateFormat`·`Date`·`Locale`), 클래스 안 `history`·`historyAdapter`·`inputJob`, 어댑터 연결(18번), [온습도 받기 시작]·[중지] 버튼(19·20번), 받은 JSON 가르기(21~23번), `addHistory`(24번), `stopInput`과 부르는 곳(25~27번), 이력 줄 누르기(28번), 끊김 Toast(29·30번) |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | import 3개(`FakeBleunoClient`·`Job`·`delay`), 클래스 안 `lastAddress`·`connectTimeoutJob`, 주소 기억·저장(43번), [재연결] 숨기기·보이기·Toast(44~46번), [재연결] 리스너(47번), 주소 꺼내기(48번), 연결 시간 제한(49~52번), (시험용) [끊김 시험] 버튼(53~55번) |
| [day2/activity_control.xml](day2/activity_control.xml) | `activity_control.xml` | `logText` 아래에 [온습도 받기 시작]·[중지] 가로 줄, 제목 `입력 이력`, `inputList`(ListView) |
| [day2/activity_main.xml](day2/activity_main.xml) | `activity_main.xml` | `retryButton` 아래에 [재연결]·[끊김 시험] 가로 줄(둘 다 처음엔 숨김) |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | `input_start`·`input_history_title`·`reconnect`·`lost_test` 추가. [중지]는 기존 `stop`을 다시 쓴다 |
| `day2/colors.xml`, `day2/ContactsReader.kt` | 색·연락처 읽기 | 1일차 그대로, 2일차에 바꾸지 않는다 |
| [day2/bleuno/](day2/bleuno) 9개 | `app › kotlin+java › com.example.smartio › bleuno` | 12주차에 넣은 제공 코드 그대로. [bleuno/src](../../../bleuno/src)와 같다 |
| `day2/AndroidManifest.xml`, `day2/res/values/themes.xml` | Manifest·테마 | 12주차 그대로. `dht11` 보내기와 재연결은 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 들어 있다 |

`.kt` 파일 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
새로 쓴 `ContextCompat`·`AlertDialog`·`ArrayAdapter`·`Job`·`SimpleDateFormat`은 4주차 의존성과 Android 기본 API에 들어 있어 `build.gradle.kts`에 더할 것이 없다.
주석 번호는 13주차까지에 이어 1일차가 `ControlActivity.kt` 11~17번, 2일차가 `ControlActivity.kt` 18~30번과 `MainActivity.kt` 43~55번이다. 번호는 수업에서 넣는 순서라 한 덩어리 안에서는 차례대로 놓이지만 파일 전체로는 흩어진다(12·15·17번, 24·25·30번, 46·50·51번은 파일 끝 함수). 같은 한 줄 `startConnectTimeout()`은 두 곳에 같은 49번을 달았다.
`day1`에서 `day2`로 넘어갈 때 **바꾼 줄은 하나뿐**이다: `ControlActivity.kt` 9번 응답 처리의 `if (result != null) {`가 `} else if (result != null) {`(195행)가 되었다. 나머지는 모두 줄을 더했다.

**(시험용) 표시**: [끊김 시험] 버튼은 보드 없이 가짜 보드로 "끊김"을 만들어 보는 시험용이다(53~55번 주석 첫머리 `(시험용)`). 넣지 않으려면 `activity_main.xml`의 `lostTestButton`, `strings.xml`의 `lost_test`, `import com.example.smartio.bleuno.FakeBleunoClient`, 53·54·55번 줄을 넣지 않는다.

## 1. `isAllowedIndex()` — 보내도 되는 번호만 보내기 (1일차)

```kotlin
binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
    val pin = binding.pinEdit.text.toString()
    if (pin.isEmpty()) {
        Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
    } else if (isAllowedIndex(pin.toInt()) == false) {
        Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
    } else if (isChecked) {
```

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

| 실행 결과 (Fake, `준비됨` 제어 화면) | 화면 | Logcat `tag:BLE` |
|---|---|---|
| `3` → Switch 켜기 | 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}` | `writeCharacteristic(가짜): "on 3"` |
| `9` → Switch 켜기 | Toast `허용되지 않는 번호`, 로그에 새 줄 없음 | `writeCharacteristic` 줄 없음 |
| 빈 칸 → Switch 켜기 | Toast `LED 번호를 입력하세요`, 로그에 새 줄 없음 | `writeCharacteristic` 줄 없음 |
| [전체 끄기] | 로그에 `off -1`과 `응답: {"result":"ok","ms":"led(s) off"}` | `writeCharacteristic(가짜): "off -1"` |

- 사슬 순서는 **빈 칸 → 허용 번호 → 켜기/끄기**다. 빈 칸 검사가 먼저 걸러 주므로 `pin.toInt()`가 빈 글자에서 불리지 않는다. 순서를 바꾸면 빌드는 되지만 빈 칸에서 앱이 멈춘다(Logcat `java.lang.NumberFormatException: For input string: ""`).
- `-1`(전체)도 약속된 번호라 허용한다. 입력 칸은 `inputType`이 `number`라 `-`를 적을 수 없어 [전체 끄기]만 `-1`을 보낸다.
- `: Boolean`과 `return true`/`return false`는 10주차 `hasBlePermissions()`와 같은 모양이다. 클래스 끝에 둔다.
- `contains(pin)`처럼 **글자**를 넣으면 `Type inference failed. The value of the type parameter 'T' should be mentioned in input types (argument types, receiver type, or expected type). Try to specify it explicitly.`가 난다. 숫자 목록에는 `pin.toInt()`를 넣는다.
- `== false`를 빠뜨리면 조건이 뒤집혀 `0`~`3`이 막히고 `9`가 나간다. 빌드는 된다.
- 펌웨어는 번호 범위를 확인하지 않는다. 그래서 보내기 전에 앱이 막는다. `4`처럼 약속된 범위 밖이면서 보드에 LED가 없는 번호는 앱이 막는 것과 보드가 못 하는 것이 다르다.

## 2. `enabled="false"`·collect·`pauseButtons()` — 못 누를 때는 못 누르게 (1일차)

```xml
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/led" />
```

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

| 실행 결과 (Fake) | LED Switch·[전체 끄기] |
|---|---|
| 목록 줄 탭 → `준비됨` → [제어 화면] | `상태: 준비됨`이 되는 순간 켜진다 |
| [뒤로] → [해제] → [연결]로 제어 화면 들어오기 | 회색이라 눌리지 않는다. 13주차에 이 길로 들어와 Switch를 켜면 Logcat에 `send(가짜): 준비되지 않아 무시함`이 찍혔다 |
| `delay(300)`을 잠시 `delay(3000)`으로 바꾸고 `3` → Switch 켜기 직후 | 3초 동안 회색 |
| 그 3초 뒤 | 다시 켜진다 |

- XML `android:enabled="false"`는 5주차 `stopButton`, 12주차 `controlButton`처럼 "꺼진 채로 시작"이다. client가 없거나 첫 상태가 오기 전에도 누를 수 없다.
- collect 안에서 **먼저 모두 끄고, `준비됨`이면 켠다.** 12주차 연결 화면(`MainActivity` 8번)과 같은 방법이다. 제어 화면은 "준비됨이냐 아니냐"만 보면 되므로 7주차 `when` 대신 `if` 하나로 썼다. [뒤로]는 늘 켜 둔다.
- `pauseButtons()`는 `send`를 부르는 세 곳(켜기·끄기·[전체 끄기])의 `append` 줄 아래에서 부른다. 5주차 `isEnabled`로 끄고, 6주차 `lifecycleScope.launch { delay() }`로 기다렸다가 켠다.
- `Bleuno.client?.isReady == true`: client가 없으면 `?.`의 결과가 `null`이고 `null == true`는 `false`라 켜지 않는다. 7주차 `scanJob?.isActive == true`와 같은 모양이다. 300ms 사이에 끊겼으면 collect가 끈 상태를 그대로 둔다.
- `delay(300)`을 `launch { }` 밖에 쓰면 `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.`이 난다.

## 3. `colors.xml`·`R.color`와 AlertDialog — 오류를 눈에 보이게 (1일차)

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

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

| 실행 결과 (Fake, `3` → Switch 켜기) | 로그 | 창 | Logcat `tag:BLE` |
|---|---|---|---|
| 그대로 보내기 | `on 3` / `응답: {"result":"ok","ms":"led(s) on"}`, 글자 초록 | 없음 | `writeCharacteristic(가짜): "on 3"` |
| `send("on$index")`로 한 곳만 바꿔 보내기 | `on 3` / `응답: {"result":"fail","ms":"unknown command"}`, 글자 빨강 | `보드가 오류를 알렸습니다` / `응답: fail · unknown command` | `writeCharacteristic(가짜): "on3"` |
| [확인] → [전체 끄기] | `off -1`과 `ok` 응답, 글자 초록으로 되돌아옴 | 없음 | `writeCharacteristic(가짜): "off -1"` |

- `#AARRGGBB`에서 앞 두 자리 `FF`는 불투명, 뒤 여섯 자리가 빨강·초록·파랑이다. `colors.xml`은 새 프로젝트에 이미 있고 `black`·`white` 두 줄 아래에 두 줄만 더한다.
- 4주차 `strings.xml` → `@string/`·`R.string`과 같은 관계로, `colors.xml`에 붙인 이름은 코드에서 `R.color.log_error`로 부른다. 두 색 줄을 넣지 않으면 `Unresolved reference 'log_error'.`가 난다.
- `setTextColor`는 로그 칸 **전체** 글자색을 바꾼다. 한 줄만 색을 바꾸는 방법은 다루지 않는다.
- `result != "ok"`: `err`(명령은 맞지만 값이 틀림)와 `fail`(모르는 명령) 모두 이 가지로 온다.
- `BleunoMessage.message(json) ?: ""`로 `"ms"` 설명을 꺼낸다. `String?`이라 3주차 `?:`로 없을 때 빈 글자를 넣는다. 로그에 JSON 원문이 이미 있으므로 창에는 읽기 쉬운 `응답: fail · unknown command`를 보여 준다.
- `AlertDialog`는 Alt+Enter 목록에서 `androidx.appcompat.app.AlertDialog`를 고른다(10주차와 같다). 응답은 `onStart`~`onStop` 사이에만 오므로 창을 띄울 때 화면이 보이고 있다.
- 앱 로그에는 `on 3`이지만 **실제로 보낸 글자**는 Logcat의 `"on3"`이다. 명령이 이상하면 Logcat `writeCharacteristic` 줄을 믿는다.
- 확인이 끝나면 `"on $index"`로 **반드시 되돌린다.**

## 4. `split(" ")`, `[0]`, `[1]` — 이력 한 줄을 시각과 값으로 나누기 (2일차)

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

## 5. `BleunoMessage.event`·`value` — 받은 JSON 가르기 (2일차)

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

| 받은 JSON | `event` | `value` | `result` | 들어가는 곳 |
|---|---|---|---|---|
| `{"event":"input","index":0,"value":1}` (가짜 보드가 10초마다) | `"input"` | `"1"` | `null` | 입력 이력 `12:00:10 입력=1` |
| `{"result":"ok","value":"[24.5,40.0]"}` (`dht11` 응답) | `null` | `"[24.5,40.0]"` | `"ok"` | 입력 이력 `12:00:03 [24.5,40.0]` |
| `{"result":"ok","ms":"led(s) on"}` | `null` | `null` | `"ok"` | 명령 로그 `응답: {…}` (초록) |
| `{"result":"fail","ms":"unknown command"}` | `null` | `null` | `"fail"` | 명령 로그(빨강) + AlertDialog |

- 입력 이벤트에도 `"value"`가 있으므로 `event` 검사를 **먼저** 한다. 순서를 바꾸면 빌드는 되지만 이벤트가 `12:00:10 1`처럼 숫자 한 줄로 들어간다.
- 세 helper는 키가 없으면 `null`을 돌려주는 `String?`이다. `addHistory(BleunoMessage.value(json))`처럼 바로 넘기면 `Argument type mismatch: actual type is 'kotlin.String?', but 'kotlin.String' was expected.` 위에서 `if (value != null)`로 확인한 변수 `value`를 넘긴다.
- 실제 보드는 펌웨어에 입력 이벤트를 더하기 전까지 이벤트를 보내지 않는다. 실보드에서는 `dht11` 응답으로 입력을 받는다.

## 6. `while (isActive)` — 3초마다 `dht11` 보내고 멈추기 (2일차)

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

## 7. 입력 이력 `ListView` — 시각을 붙여 쌓기 (2일차)

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

## 8. 끊김과 [재연결] — 마지막 주소를 저장해 두기 (2일차)

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

## 9. 연결 시간 제한 — 10초 안에 준비됨이 아니면 (2일차)

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

## 10. (시험용) [끊김 시험] — 보드 없이 끊김 만들기 (2일차)

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

## 11. 최종 앱 흐름

[day2](day2) 파일을 모두 넣고 실행한 흐름:

```text
[권한 확인] ▶ [검색] ▶ 목록 줄 탭 ─ 주소 저장, 10초 시간 제한 시작
   ├─ 10초 안에 준비됨 ▶ [제어 화면]
   │     LED Switch ▶ 허용 번호 확인 ▶ send("on 3") ▶ 명령 로그(초록) + 300ms 버튼 막기
   │     허용되지 않는 번호 ▶ Toast만, 명령 없음
   │     오류 응답 ▶ 명령 로그(빨강) + 창 "보드가 오류를 알렸습니다"
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
- [색 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/more-resources#Color)
- [대화상자 — Android Developers](https://developer.android.com/develop/ui/views/components/dialogs)
- [키-값 데이터 저장(SharedPreferences) — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [코루틴 취소와 시간 제한 — Kotlin](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [split — Kotlin 표준 라이브러리](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/split.html)
