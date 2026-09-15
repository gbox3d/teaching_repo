# 14주차 따라하기 — 입력 받기·끊김·재연결과 2차 과제 발표

13주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
13주차 프로젝트가 없거나 실행되지 않으면 강의자에게 13주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에 고치는 파일은 다섯 개다. 제어 화면 `ControlActivity.kt`·`activity_control.xml`, 연결 화면 `MainActivity.kt`·`activity_main.xml`, 그리고 `strings.xml`이다.
`AndroidManifest.xml`, `ContactsReader.kt`, `colors.xml`, `res/values/themes.xml`, `bleuno` 패키지 8개는 13주차 그대로 둔다. 전체 내용은 [부록 A](#부록-a--바꾸지-않는-파일-전체)와 [부록 B](#부록-b--제공-bleuno-파일-전체)에 있다.

에뮬레이터는 13주차와 같은 API 33 이상 이미지를 쓴다. 보드 없이 가짜 클라이언트(Fake)로 끝까지 할 수 있고, 실보드는 실기기에서만 연결된다.
제어 화면에는 13주차처럼 **목록 줄 탭 → `준비됨` → [제어 화면]**으로 들어간다.
2일차는 2차 과제 발표라 새 코드가 없다. [2일차](#2일차) 절에는 발표 전 점검과 실보드가 안 될 때 Fake로 바꾸는 순서를 적었다.

## 1일차

### 1. 13주차 프로젝트 열고 입력 이벤트 줄 보기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. Logcat 창의 필터에 `package:mine tag:BLE`를 넣어 둔다.
3. [검색]을 누르고 목록에 `ESP32_BLE_FAKE1 (00:11:22:33:44:01)`이 들어오면 그 줄을 누른다. 상태가 `연결 중` → `서비스 확인 중` → `준비됨`이 되면 [제어 화면]을 누른다.
4. 제어 화면에 아래가 보이면 시작할 수 있다. `LED 0 밝기` 줄은 13주차 확장을 한 사람만 있다.

```text
장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[LED 번호 (0~3)]
LED (○)
[전체 끄기]
LED 0 밝기 ─○──────
명령 로그

[뒤로]
```

5. `준비됨`인 채로 10초쯤 기다린다. Logcat에 아래 줄이 10초마다 찍힌다. `value`는 `1`과 `0`이 번갈아 온다.

```text
onCharacteristicChanged(가짜): {"event":"input","index":0,"value":1}
```

   가짜 보드가 **입력 이벤트**를 흉내 내는 줄이다. 13주차 9번 `if (result != null)`이 이 줄을 걸러서 앱 로그에는 없다. 오늘은 이 줄과 `dht11`(온도·습도) 응답을 **입력 이력** 목록에 쌓는다.
6. `3` → LED Switch 켜기를 해 본다. 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 쌓이면 13주차 그대로다.

지금 내 `ControlActivity.kt`는 [13주차 완성본](../week13_ble_output/examples/day2/ControlActivity.kt), `MainActivity.kt`는 [13주차 완성본 연결 화면](../week13_ble_output/examples/day2/MainActivity.kt)과 같아야 한다. 많이 다르면 그 파일로 바꾸고 시작한다.

### 2. strings.xml에 문자열 네 줄 넣기

1. `app › res › values › strings.xml`을 연다. `pwm_title` 줄 아래(마지막 `</resources>` 바로 위)에 네 줄을 넣는다. 13주차 확장을 하지 않아 `pwm_title`이 없으면 `all_off` 줄 아래에 넣는다.

```xml
    <string name="input_start">온습도 받기 시작</string>
    <string name="input_history_title">입력 이력</string>
    <string name="reconnect">재연결</string>
    <string name="lost_test">끊김 시험</string>
```

전체는 아래와 같다. 같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
    <string name="device_unknown">장치: ?</string>
    <string name="pin_hint">LED 번호 (0~3)</string>
    <string name="led">LED</string>
    <string name="log_title">명령 로그</string>
    <string name="back">뒤로</string>
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
    <string name="retry">다시 시도</string>
    <string name="disconnect">해제</string>
    <string name="battery_unknown">배터리 ?</string>
    <string name="check_permission">권한 확인</string>
    <string name="device_list_title">검색된 장치</string>
    <string name="last_device_none">마지막 장치: 없음</string>
    <string name="show_contacts">연락처 보기</string>
    <string name="control_screen">제어 화면</string>
    <string name="state_unknown">상태: ?</string>
    <string name="all_off">전체 끄기</string>
    <string name="pwm_title">LED 0 밝기</string>
    <string name="input_start">온습도 받기 시작</string>
    <string name="input_history_title">입력 이력</string>
    <string name="reconnect">재연결</string>
    <string name="lost_test">끊김 시험</string>
</resources>
```

2. 실행한다. 화면은 1단계와 같다.

- [중지] 버튼 글자는 5주차부터 있는 `stop`(`중지`)을 다시 쓴다. 새로 만들지 않는다.
- `reconnect`·`lost_test`는 연결 화면(8단계)에서 쓴다. 미리 넣어 두어도 빌드에 문제가 없다.

### 3. 제어 화면에 입력 이력 자리 만들기

1. `app › res › layout › activity_control.xml`을 연다. 명령 로그 칸(`logText`) 블록을 닫는 `/>` **아래**, [뒤로] 버튼(`backButton`) **위**에 한 줄을 비우고 넣는다.

```xml
    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/inputStartButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:enabled="false"
            android:text="@string/input_start" />

        <Button
            android:id="@+id/inputStopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

    </LinearLayout>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/input_history_title"
        android:textSize="16sp" />

    <ListView
        android:id="@+id/inputList"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="2"
        android:layout_marginTop="8dp"
        android:transcriptMode="alwaysScroll" />
```

전체는 아래와 같다. 같은 코드가 [examples/day1/activity_control.xml](examples/day1/activity_control.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center_horizontal"
    android:orientation="vertical">

    <TextView
        android:id="@+id/deviceText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/device_unknown"
        android:textSize="24sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_unknown"
        android:textSize="18sp" />

    <EditText
        android:id="@+id/pinEdit"
        android:layout_width="160dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/pin_hint"
        android:inputType="number"
        android:maxLength="2" />

    <Switch
        android:id="@+id/ledSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/led" />

    <Button
        android:id="@+id/allOffButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/all_off" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:gravity="center_vertical"
        android:orientation="horizontal">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/pwm_title"
            android:textSize="16sp" />

        <SeekBar
            android:id="@+id/pwmSeekBar"
            android:layout_width="160dp"
            android:layout_height="wrap_content"
            android:enabled="false"
            android:max="255" />

    </LinearLayout>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/log_title"
        android:textSize="16sp" />

    <TextView
        android:id="@+id/logText"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="8dp"
        android:textSize="18sp" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/inputStartButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:enabled="false"
            android:text="@string/input_start" />

        <Button
            android:id="@+id/inputStopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

    </LinearLayout>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/input_history_title"
        android:textSize="16sp" />

    <ListView
        android:id="@+id/inputList"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="2"
        android:layout_marginTop="8dp"
        android:transcriptMode="alwaysScroll" />

    <Button
        android:id="@+id/backButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="24dp"
        android:text="@string/back" />

</LinearLayout>
```

2. 실행하고 [제어 화면]까지 들어간다. 명령 로그 칸 아래에 아래 줄이 보이면 성공이다.

```text
명령 로그

[온습도 받기 시작] [중지]     ← 둘 다 회색(눌리지 않음)
입력 이력
                              ← 빈 목록
[뒤로]
```

- 가로 버튼 줄은 12주차 [검색]·[중지]·[해제] 줄과 같은 모양이다. 두 버튼은 13주차 LED Switch처럼 `android:enabled="false"`로 꺼진 채 시작하고, `준비됨`일 때 코드로 켠다(6단계).
- `ListView`는 11주차 `검색된 장치` 목록과 같은 모양이다. `layout_height="0dp"`와 `layout_weight="2"`는 위 명령 로그 칸(`1`)과 남은 높이를 1:2로 나눈다.
- `android:transcriptMode="alwaysScroll"`: 새 줄이 들어오면 목록이 맨 아래로 내려간다. 이번 주에 처음 쓰는 속성이다.

### 4. 입력 이력 목록과 어댑터 준비하기

1. `ControlActivity.kt`를 연다. 클래스 안, `private lateinit var binding: ActivityControlBinding` 줄 **아래**에 한 줄을 비우고 넣는다.

```kotlin
    // 14주차 1일차: 입력 이력 목록(시각과 값 한 줄씩)과 그 목록을 ListView에 보여 주는 어댑터.
    // 응답을 받는 onStart(8번)에서도 써야 하므로 onCreate 밖, 클래스 안에 둔다. 어댑터는 onCreate에서 만든다(18번). lateinit은 binding과 같은 틀이다.
    // 이 목록은 이 화면이 가진 것이라, 회전해서 화면이 새로 만들어지면 빈 목록으로 다시 시작한다(받기도 27번 onStop에서 꺼진다).
    private val history = mutableListOf<String>()
    private lateinit var historyAdapter: ArrayAdapter<String>
```

2. `onCreate()` 안, `// 7.` [전체 끄기] 리스너 **아래**(13주차 확장을 했으면 `// 17.` SeekBar 리스너를 닫는 `})` 아래), onCreate를 닫는 `}` **위**에 한 줄을 비우고 넣는다.

```kotlin
        // 18. 입력 이력 ListView에 어댑터를 붙인다. 11주차 장치 목록(MainActivity 16번)과 같은 틀이다(14주차 1일차).
        historyAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, history)
        binding.inputList.adapter = historyAdapter
```

3. 빨간 글자를 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `ArrayAdapter` | `android.widget.ArrayAdapter` |

4. 실행한다. 화면은 3단계와 같다. 빨간 줄 없이 실행되면 된다. 이력은 5단계부터 쌓인다.

- `mutableListOf<String>()`·`ArrayAdapter(this, android.R.layout.simple_list_item_1, …)`는 11주차 장치 목록과 같은 틀이다.
- 11주차 `devices`는 onCreate **안**의 `val`이었다. 이번 `history`는 onStart(응답을 받는 곳)에서도 써야 해서 클래스 안에 둔다.
- `lateinit var historyAdapter`: `binding`과 같은 "onCreate에서 꼭 넣겠다는 약속"이다. 넣기 전에 쓰면 앱이 멈추므로 2번 두 줄을 빠뜨리지 않는다.

### 5. 받은 JSON 가르기 — 입력 이벤트를 이력에 쌓기

1. 클래스 끝, `// 15.` `pauseButtons()` 함수를 닫는 `}` **아래**(클래스를 닫는 마지막 `}` 위)에 한 줄을 비우고 함수를 넣는다.

```kotlin
    // 24. 받은 글자 앞에 지금 시각을 붙여 입력 이력 맨 아래에 한 줄 넣고, 어댑터에 알려 화면을 고친다(14주차 1일차).
    //     SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())는 지금 시각을 "12:00:03"(시:분:초) 글자로 만드는 틀이다.
    //     activity_control.xml의 inputList에 transcriptMode="alwaysScroll"을 적어 두어서 새 줄이 들어오면 목록이 맨 아래로 내려간다.
    private fun addHistory(text: String) {
        val time = SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
        history.add("$time $text")
        historyAdapter.notifyDataSetChanged()
    }
```

2. `onStart()`의 `// 9.` 응답 처리를 고친다. `val result = BleunoMessage.result(json)` 줄 **아래**에 `// 21.`·`// 22.`·`// 23.` 가지를 넣고, 13주차의 `if (result != null) {`를 `} else if (result != null) {`로 바꾼다. `// 9.` 주석 아래에 `14주차 1일차:` 설명 줄을 붙인다(주석이 없어도 동작은 같다). `// 16.` 아래는 13주차 그대로다.
   바꾼 `onStart()` 전체는 아래와 같다.

```kotlin
    // 8. 화면이 보이기 시작하면 보드가 보내는 응답(JSON 한 줄)을 받도록 등록한다(13주차 1일차).
    //    명령 하나마다 응답이 한 줄씩 온다. { json -> }는 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다.
    override fun onStart() {
        super.onStart()
        Bleuno.client?.onMessage { json ->
            // 9. JSON에서 "result"(ok·err·fail) 값을 꺼내 보고, 명령의 응답이면 받은 JSON 한 줄을 그대로 로그에 남긴다(13주차 1일차).
            //    로그 예: 응답: {"result":"ok","ms":"led(s) on"}. result가 없는 줄은 명령의 응답이 아니다(가짜 보드가 10초마다 보내는 입력 이벤트, 14주차에 다룬다). 로그에 넣지 않는다.
            //    14주차 1일차: 입력 이벤트(22번)와 dht11 응답(23번)은 명령 로그 대신 입력 이력에 넣는다. 그래서 if (result != null) 앞에 else를 붙였다.
            val result = BleunoMessage.result(json)
            // 21. "event"(보드가 먼저 보낸 이벤트 종류)와 "value"(값)도 꺼낸다. 그 키가 없는 줄이면 null이다(14주차 1일차).
            val event = BleunoMessage.event(json)
            val value = BleunoMessage.value(json)
            if (event == "input") {
                // 22. event가 "input"이면 보드가 먼저 보낸 입력 이벤트다(예: {"event":"input","index":0,"value":1}). "입력=값"으로 이력에 넣는다(14주차 1일차).
                //     입력 이벤트에도 "value"가 들어 있으므로 23번보다 먼저 확인한다.
                //     28번이 이력 줄을 띄어쓰기로 나누므로 "입력=1"처럼 띄어쓰기 없이 붙여 적는다.
                addHistory("입력=$value")
            } else if (value != null) {
                // 23. value가 있으면 dht11 응답이다(예: {"result":"ok","value":"[24.5,40.0]"}). 값만 "시각 값" 한 줄로 이력에 넣는다(14주차 1일차).
                addHistory(value)
            } else if (result != null) {
                binding.logText.append("응답: $json\n")
                // 16. result가 "ok"가 아니면(err·fail) 로그 글자를 colors.xml의 빨간색으로 바꾸고, "ms"(설명) 값을 꺼내 AlertDialog로 알린다(13주차 2일차).
                //     ok면 초록색으로 되돌린다. 응답은 onStart~onStop 사이(거의 항상 화면이 보이는 동안)에만 받으므로 여기서 창을 띄운다.
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
            }
        }
    }
```

3. 빨간 글자를 Alt+Enter → Import로 가져온다. `Date`는 목록에 두 개가 뜬다. **`java.util.Date`**를 고른다.

| 빨간 글자 | 가져올 import |
|---|---|
| `SimpleDateFormat` | `java.text.SimpleDateFormat` |
| `Date` | `java.util.Date` (`java.sql.Date`가 아니다) |
| `Locale` | `java.util.Locale` |

4. 실행하고 목록 줄 탭 → `준비됨` → [제어 화면]으로 들어와 **가만히** 둔다. 0~10초 안에 입력 이력에 첫 줄이 들어오고, 그 뒤 10초마다 한 줄씩 늘어난다. 시각은 지금 시각이다.

```text
입력 이력
12:00:10 입력=1
12:00:20 입력=0
12:00:30 입력=1
```

5. `3` → LED Switch 켜기를 한다. 명령 로그에는 13주차처럼 `on 3`과 응답이 쌓이고, 입력 이벤트 줄은 명령 로그에 들어가지 않는다.

- `BleunoMessage.event(json)`·`BleunoMessage.value(json)`: 13주차 `result(json)`처럼 JSON에서 `"event"`·`"value"` 값을 꺼낸다. 키가 없으면 `null`(`String?`)이다.
- 받은 줄은 세 가지로 가른다. `{"event":"input",…}` → 22번(입력 이벤트), `{"result":"ok","value":"[24.5,40.0]"}` → 23번(`dht11` 응답, 6단계에서 보낸다), 그 밖의 `result`가 있는 줄(`on`·`off`·오류) → 13주차 명령 로그.
- **22번을 23번보다 먼저 확인한다.** 입력 이벤트에도 `"value"`가 들어 있어서, 순서를 바꾸면 이벤트가 `12:00:10 1`처럼 숫자 한 줄로 들어간다.
- 23번 가지는 `if (value != null)` 안이라 `value`를 `String`으로 넘길 수 있다. `addHistory(BleunoMessage.value(json))`처럼 꺼내자마자 넘기면 `String?`이라 빌드 오류가 난다(3주차 null 안전성).
- `"입력=$value"`는 띄어쓰기 없이 붙인다. 7단계에서 이력 줄을 띄어쓰기로 나누기 때문이다.
- `SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())`: 지금 시각을 `12:00:03`(시:분:초) 글자로 만드는 **틀**이다. `HH`는 24시간, `mm`은 분, `ss`는 초다.
- `history.add(…)` 뒤에는 11주차처럼 `notifyDataSetChanged()`로 어댑터에 알려야 화면이 바뀐다.

### 6. 온습도 3초마다 받기와 [중지]

1. 클래스 안, 4단계에서 넣은 `historyAdapter` 줄 **아래**에 한 줄을 비우고 넣는다.

```kotlin
    // 14주차 1일차: [온습도 받기 시작]이 시작한 반복 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같다). 아직 없으면 null이다.
    private var inputJob: Job? = null
```

2. `onCreate()` 안, 4단계의 `// 18.` 두 줄 **아래**에 한 줄을 비우고 두 리스너를 넣는다.

```kotlin
        // 19. [온습도 받기 시작] 버튼: 3초마다 "dht11" 명령을 보낸다. 응답은 onStart의 23번이 받아 이력에 넣는다(14주차 1일차).
        //     6주차 카운트다운처럼 lifecycleScope.launch 안에서 delay로 기다린다. while (isActive)는 "취소되지 않았으면 계속 되풀이한다"는 뜻이다.
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

        // 20. [중지] 버튼: 반복 코루틴을 취소하고 버튼을 되돌린다. 25번 함수가 한다(14주차 1일차).
        binding.inputStopButton.setOnClickListener {
            stopInput()
        }
```

3. 클래스 끝, 5단계의 `addHistory()` 함수 **아래**에 한 줄을 비우고 함수를 넣는다. 함수 위의 `// 25.` 설명 주석 두 줄은 예제 파일 261~262행에 있다(주석이 없어도 동작은 같다).

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

4. `onCreate()`의 `// 4.` collect 안, `// 13.`의 `if (state == ConnState.READY) { … }`를 닫는 `}` **아래**에 두 줄을 넣는다. `// (확장)` 줄은 13주차 확장을 한 사람만 있다.

```kotlin
                    if (state == ConnState.READY) {
                        binding.ledSwitch.isEnabled = true
                        binding.allOffButton.isEnabled = true
                        binding.pwmSeekBar.isEnabled = true // (확장)
                    }
                    // 26. 상태가 바뀌면(끊김 등) 온습도 받기를 멈추고, 준비됨일 때만 [온습도 받기 시작]을 켠다. 25번 함수가 한다(14주차 1일차).
                    stopInput()
```

5. `onStop()`의 `Bleuno.client?.onMessage(null)` **아래**에 두 줄을 넣는다.

```kotlin
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
        // 27. 응답을 받지 않는 동안에는 온습도 요청도 보내지 않는다. [중지]를 누른 것과 같다(14주차 1일차).
        stopInput()
    }
```

6. 빨간 글자를 Alt+Enter → Import로 가져온다. `launch`·`delay`는 13주차에 이미 import했다.

| 빨간 글자 | 가져올 import |
|---|---|
| `Job` | `kotlinx.coroutines.Job` |
| `isActive` | `kotlinx.coroutines.isActive` |

7. 실행하고 `준비됨` 제어 화면에 들어온다. [온습도 받기 시작]이 켜져 있고 [중지]는 회색이다.
8. [온습도 받기 시작]을 누른다. [온습도 받기 시작]이 회색, [중지]가 켜지고, 약 0.3초 뒤 첫 줄, 그 뒤 3초마다 한 줄씩 쌓인다. 입력 이벤트 줄도 10초마다 섞여 들어온다.

```text
입력 이력
12:00:03 [24.5,40.0]
12:00:06 [25.0,41.0]
12:00:08 입력=1
12:00:09 [25.5,42.0]
```

   Logcat `tag:BLE`에는 3초마다 두 줄이 찍힌다.

```text
writeCharacteristic(가짜): "dht11"
onCharacteristicChanged(가짜): {"result":"ok","value":"[24.5,40.0]"}
```

9. [중지]를 누른다. `dht11` 줄이 더 늘지 않고(입력 이벤트 줄은 계속 10초마다), [온습도 받기 시작]이 다시 켜진다.
10. [온습도 받기 시작] → 홈 버튼 → 앱으로 돌아오기를 한다. 받기가 꺼져 있다([온습도 받기 시작] 켜짐, [중지] 회색). 이력은 나가기 전 줄 그대로다.

- `inputJob = lifecycleScope.launch { while (isActive) { … delay(3000) } }`: 6주차 `scanJob = lifecycleScope.launch { }`와 같은 모양이다. `while (isActive)`는 "취소되지 않았으면 계속 되풀이한다"는 뜻이다. `while`은 11주차 `ContactsReader`에서 본 "조건이 참인 동안 되풀이"다.
- `inputJob =`을 빠뜨리면 [중지]의 `inputJob?.cancel()`이 아무것도 취소하지 못해 반복이 멈추지 않는다.
- 멈추는 일은 `stopInput()` 하나가 맡고 세 곳에서 부른다. [중지] 버튼(20번), 연결 상태가 바뀔 때(26번), 화면이 안 보이게 될 때(27번). 13주차 "onStart에서 받기 등록 ↔ onStop에서 해제"처럼 **응답을 받지 않는 동안에는 요청도 보내지 않는다.**
- 26번이 collect 안에 있어도 받는 중에 멈추지 않는다. StateFlow는 값이 **바뀔 때만**(그리고 collect를 시작할 때 한 번) 주기 때문이다. `끊김`·`연결 안 됨`이 오면 멈춘다.
- 가짜 보드의 온습도는 `[24.5,40.0]` → `[25.0,41.0]` → `[25.5,42.0]`을 되풀이하며 앱을 끄기 전까지 이어서 센다. 두 번째 받기부터는 첫 값이 `[24.5,40.0]`이 아닐 수 있다.

### 7. 이력 줄을 눌러 시각과 값 나누기 — 오늘 문법 split

1. `onCreate()` 안, 6단계의 `// 20.` [중지] 리스너 **아래**에 한 줄을 비우고 넣는다.

```kotlin
        // 28. 입력 이력의 한 줄을 누르면 그 줄을 띄어쓰기(" ")로 나눠 받은 시각과 값을 Toast로 보여 준다(14주차 1일차).
        //     history[position]은 history.get(position)과 같다(누른 줄 번호로 꺼내기). split(" ")은 글자를 " "가 있는 곳마다 잘라 목록으로 돌려준다.
        //     "12:00:03 [24.5,40.0]" → [0]은 "12:00:03"(시각), [1]은 "[24.5,40.0]"(값). 번호는 0부터 센다. 이력 줄은 늘 "시각 값"이라 [1]까지 있다(24번).
        binding.inputList.setOnItemClickListener { _, _, position, _ ->
            val parts = history[position].split(" ")
            val time = parts[0]
            val value = parts[1]
            Toast.makeText(this, "받은 시각: $time · 값: $value", Toast.LENGTH_SHORT).show()
        }
```

2. 실행하고 이력 줄을 몇 개 쌓은 뒤 한 줄을 누른다.

| 누른 줄 | `split(" ")` 결과 `parts` | Toast |
|---|---|---|
| `12:00:03 [24.5,40.0]` | `[12:00:03, [24.5,40.0]]` | `받은 시각: 12:00:03 · 값: [24.5,40.0]` |
| `12:00:10 입력=1` | `[12:00:10, 입력=1]` | `받은 시각: 12:00:10 · 값: 입력=1` |

- `history[position]`: 누른 줄 번호로 목록에서 꺼낸다. 12주차 `addresses.get(position)`과 같다. 번호는 0부터 센다.
- `split(" ")`: 글자를 띄어쓰기(`" "`)가 있는 곳마다 잘라 목록으로 돌려준다. `[0]`이 첫 칸(시각), `[1]`이 둘째 칸(값)이다.
- 이력 줄은 늘 `시각 값` 모양이고 값에 띄어쓰기가 없어서 `[1]`까지 있다. 없는 칸 `[2]`를 꺼내면 줄을 누르는 순간 앱이 멈춘다.
- Toast 글자에 `"$parts[0]"`처럼 바로 쓰면 `$`가 `parts`까지만 읽고 `[0]`은 그냥 글자로 붙는다. 예제처럼 `val time = parts[0]`에 담아 `$time`으로 쓴다.
- 이 리스너는 onCreate 안이라 `this`가 화면(Activity)이다. Toast를 바로 쓴다.

제어 화면은 끊겼을 때 알리는 Toast(11단계)만 남았다. 먼저 연결 화면을 고친다.

### 8. 연결 화면에 [재연결]·[끊김 시험] 자리 만들기

1. `app › res › layout › activity_main.xml`을 연다. [다시 시도] 버튼(`retryButton`) 블록을 닫는 `/>` **아래**, [권한 확인] 버튼(`permissionButton`) **위**에 한 줄을 비우고 넣는다.

```xml
    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/reconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/reconnect"
            android:visibility="gone" />

        <Button
            android:id="@+id/lostTestButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/lost_test"
            android:visibility="gone" />

    </LinearLayout>
```

전체는 아래와 같다. 같은 코드가 [examples/day1/activity_main.xml](examples/day1/activity_main.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="28sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/lastDeviceText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/last_device_none"
        android:textSize="16sp" />

    <EditText
        android:id="@+id/deviceNameEdit"
        android:layout_width="240dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/device_name_hint"
        android:inputType="text" />

    <Switch
        android:id="@+id/autoSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/auto_connect" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/scanButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/scan" />

        <Button
            android:id="@+id/stopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

        <Button
            android:id="@+id/disconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/disconnect" />

    </LinearLayout>

    <ProgressBar
        android:id="@+id/scanProgress"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:visibility="gone" />

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_idle"
        android:textSize="18sp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/device_list_title"
        android:textSize="16sp" />

    <ListView
        android:id="@+id/deviceList"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="8dp" />

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

    <Button
        android:id="@+id/controlButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:enabled="false"
        android:text="@string/control_screen" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/reconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/reconnect"
            android:visibility="gone" />

        <Button
            android:id="@+id/lostTestButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/lost_test"
            android:visibility="gone" />

    </LinearLayout>

    <Button
        android:id="@+id/permissionButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/check_permission" />

    <Button
        android:id="@+id/contactsButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/show_contacts" />

    <TextView
        android:id="@+id/batteryText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/battery_unknown"
        android:textSize="16sp" />

</LinearLayout>
```

2. 실행한다. 두 버튼 모두 `android:visibility="gone"`이라 화면은 그대로다.

- [재연결]은 [다시 시도]처럼 처음엔 숨겨 두고 `끊김`일 때만 보인다(9단계).
- [끊김 시험]은 숨김 + 꺼짐으로 시작한다. 가짜 보드일 때만 보이게 하는 코드는 10단계에서 넣는다.

### 9. 주소 기억하고 [재연결] 만들기

`MainActivity.kt`를 열고 여섯 곳에 넣는다.

1. 클래스 안, `bluetoothLauncher` 블록을 닫는 `}` **아래**에 한 줄을 비우고 넣는다. 맨 위 `// 14주차 1일차: 마지막으로 연결을 시작한 보드 주소 …` 설명 주석 한 줄은 예제 파일 103행에 있다.

```kotlin
    // 화면이 새로 만들어지면(회전 등) 이 변수는 빈 글자("")로 돌아가므로 onCreate에서 저장소의 값을 다시 꺼내 넣는다(48번).
    private var lastAddress = ""
```

2. `// 19.` 목록 줄 리스너 안, `client.connect(address)` **아래**에 넣는다. 리스너 뒷부분은 아래와 같다.

```kotlin
            // 38. 누른 줄과 같은 번호의 주소를 꺼내 연결을 시작한다. 검색 중이면 먼저 검색을 멈춘다(12주차 2일차).
            //     get(번호)는 add로 넣은 순서대로 꺼낸다. 번호는 0부터 센다.
            val address = addresses.get(position)
            client.stopScan()
            client.connect(address)
            // 43. 연결을 시작한 주소를 기억하고, 앱 전용 저장소 "smartio"에 "lastAddress"라는 이름표로도 저장한다(14주차 1일차).
            //     20번 장치 이름 저장과 같은 틀이다(11주차 2일차). 저장해 두면 화면이 새로 만들어져도 [재연결]이 이 주소를 쓴다(48번).
            lastAddress = address
            getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
```

3. `// 21.` 마지막 장치 이름을 보여 주는 `if … else …` 블록 **아래**에 한 줄을 비우고 넣는다. 아래 블록에서는 `// 48.` 주석의 둘째 줄(예제 파일 330행)을 줄였다.

```kotlin
        // 21. 앱이 시작되면(onCreate) 저장해 둔 마지막 장치 이름을 꺼내 보여 준다(11주차 2일차).
        //     저장한 적이 없으면 기본값 ""이 온다. getString은 String?를 돌려주므로 ?: ""로 null을 막는다.
        val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
        val lastName = prefs.getString("last", "") ?: ""
        if (lastName.isEmpty()) {
            binding.lastDeviceText.text = "마지막 장치: 없음"
        } else {
            binding.lastDeviceText.text = "마지막 장치: $lastName"
        }

        // 48. 43번에서 저장한 마지막 보드 주소를 꺼내 lastAddress에 넣는다. 21번과 같은 틀이다(14주차 1일차).
        lastAddress = prefs.getString("lastAddress", "") ?: ""
```

4. `// 7.` collect 안, "먼저 모두 끄고"의 마지막 줄 `binding.scanProgress.visibility = View.GONE` **아래**에 두 줄, `ConnState.LOST ->` 가지의 `binding.retryButton.visibility = View.VISIBLE` **아래**에 네 줄을 넣는다.

```kotlin
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    // 44. [재연결]은 끊김일 때만 보인다(45번). 먼저 숨긴다(14주차 1일차).
                    binding.reconnectButton.visibility = View.GONE
```

```kotlin
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                            // 45. 사용자가 해제하지 않았는데 끊겼다. [재연결]을 보여 주고 Toast로 알린다(14주차 1일차).
                            //     collect 틀 안에서는 this가 Activity가 아니어서 Toast는 46번 함수로 띄운다. 끊김인 채로 이 화면이 다시 보이면(회전, 제어 화면에서 [뒤로]) 또 뜬다.
                            binding.reconnectButton.visibility = View.VISIBLE
                            showLostToast()
                        }
```

5. 클래스 끝, `// 42.` `isLocationOff()` 함수 **아래**에 한 줄을 비우고 함수를 넣는다.

```kotlin
    // 46. 끊겼다고 알리는 Toast. 7번 collect의 끊김 가지(45번)에서 부른다(14주차 1일차).
    //     collect 틀 안의 this는 Activity가 아니어서 Toast.makeText(this, …)를 바로 쓸 수 없다. 함수로 빼면 this가 Activity다.
    private fun showLostToast() {
        Toast.makeText(this, "연결이 끊겼습니다. [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
    }
```

6. `onCreate()` 안, `// 22.` [연락처 보기] 리스너 **아래**(onCreate를 닫는 `}` 위)에 한 줄을 비우고 넣는다. 시간 제한 줄은 12단계에서 더한다.

```kotlin
        // 47. [재연결] 버튼: 끊김일 때만 보인다(45번). 마지막으로 연결한 주소로 다시 연결한다(14주차 1일차).
        //     주소가 비어 있으면(앱을 설치하고 한 번도 목록을 눌러 연결한 적이 없으면) [검색]부터 하라고 알린다.
        binding.reconnectButton.setOnClickListener {
            if (lastAddress.isEmpty()) {
                Toast.makeText(this, "마지막 주소가 없습니다. [검색]부터 하세요", Toast.LENGTH_SHORT).show()
            } else {
                client.connect(lastAddress)
            }
        }
```

7. 실행한다. 새 import는 없다(`Toast`·`View`는 이미 있다). 목록 줄 탭 → `준비됨` → [제어 화면] → [뒤로]가 13주차처럼 되면 된다. [재연결]은 아직 보이지 않는다. 가짜 보드는 스스로 끊기지 않으니 끊김은 10단계에서 만든다.

- `lastAddress`에만 담으면 화면이 새로 만들어질 때(회전, 제어 화면에 간 동안의 회전) 빈 글자로 돌아간다. 그래서 11주차 SharedPreferences로 저장하고(43번) onCreate에서 다시 꺼낸다(48번). 이름표는 장치 이름 `"last"`와 다른 `"lastAddress"`다.
- 48번의 `?: ""`는 11주차 21번과 같은 이유다. `getString`은 `String?`를 돌려주고 `lastAddress`는 `String`이다.
- 45번에서 `Toast.makeText(this, …)`를 바로 쓰지 않는다. collect 틀 안의 `this`는 화면(Activity)이 아니라 코루틴이라 빌드 오류가 난다. 그래서 Toast를 화면의 함수 `showLostToast()`(46번)로 빼서 부른다. 함수 안의 `this`는 화면이다.
- 끊김이면 [검색]·[다시 시도](처음부터 다시 검색)·[재연결](같은 주소로 바로 연결) 셋 다 쓸 수 있다.

### 10. (시험용) [끊김 시험]으로 보드 없이 끊김 만들기

가짜 보드는 전원을 끌 수 없어서, 보드 전원이 꺼진 것처럼 `끊김`을 만드는 시험용 버튼을 둔다. 실보드는 이 버튼 대신 보드 전원을 끈다.

1. `// 7.` collect 안, 9단계의 `// 44.` 두 줄 **아래**에 두 줄을 넣는다.

```kotlin
                    // 44. [재연결]은 끊김일 때만 보인다(45번). 먼저 숨긴다(14주차 1일차).
                    binding.reconnectButton.visibility = View.GONE
                    // 53. (시험용) [끊김 시험]은 준비됨일 때만 켠다(54번). 먼저 끈다(14주차 1일차).
                    binding.lostTestButton.isEnabled = false
```

2. 같은 collect의 `ConnState.READY ->` 가지, `binding.controlButton.isEnabled = true` **아래**에 두 줄을 넣는다.

```kotlin
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                            // 준비됨일 때만 [제어 화면]을 누를 수 있다(12주차 2일차).
                            binding.controlButton.isEnabled = true
                            // 54. (시험용) 준비됨일 때만 [끊김 시험]을 누를 수 있다(14주차 1일차).
                            binding.lostTestButton.isEnabled = true
                        }
```

3. `onCreate()` 안, 9단계의 `// 47.` [재연결] 리스너 **아래**에 한 줄을 비우고 넣는다.

```kotlin
        // 55. (시험용) [끊김 시험] 버튼: 가짜 보드(useFake = true)일 때만 보인다. 보드 전원을 끈 것처럼 "끊김"을 만든다(14주차 1일차).
        //     simulateLost()는 FakeBleunoClient에만 있어서 as로 "가짜 클라이언트로 보고" 꺼낸 뒤 부른다. 실제 보드는 전원을 꺼서 시험한다.
        if (useFake) {
            binding.lostTestButton.visibility = View.VISIBLE
        }
        binding.lostTestButton.setOnClickListener {
            val fake = client as FakeBleunoClient
            fake.simulateLost()
        }
```

4. 빨간 글자를 Alt+Enter → Import로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `FakeBleunoClient` | `com.example.smartio.bleuno.FakeBleunoClient` |

5. 실행한다. [다시 시도] 자리 아래에 [끊김 시험]이 회색으로 보인다.
6. [검색] → `ESP32_BLE_FAKE1` 줄 탭 → `준비됨`. [끊김 시험]이 켜진다. 누른다.

```text
끊김
검색된 장치
ESP32_BLE_FAKE1 (00:11:22:33:44:01)
ESP32_BLE_FAKE2 (00:11:22:33:44:02)
[연결]
[제어 화면]              ← 회색
[다시 시도]
[재연결] [끊김 시험]      ← [끊김 시험]은 회색
연결이 끊겼습니다. [재연결]을 누르세요     ← Toast
```

   Logcat `tag:BLE`에 `simulateLost(가짜) → 끊김`.
7. [재연결]을 누른다. [재연결]·[다시 시도]가 숨겨지고 `연결 중` → `서비스 확인 중` → `준비됨`. Logcat에 `connectGatt(가짜): 00:11:22:33:44:01`.
8. 다시 [끊김 시험]을 누르고, `끊김`인 채로 화면을 돌린다. Toast가 한 번 더 뜬다. 코드가 틀린 것이 아니다. StateFlow가 새 화면에 마지막 값 `끊김`을 다시 주기 때문이다(7주차). 돌린 뒤 [재연결]을 누르면 저장한 주소로 `준비됨`까지 간다.

- `client as FakeBleunoClient`: `simulateLost()`는 가짜 클라이언트에만 있어서 "가짜 클라이언트로 보고" 꺼낸 뒤 부른다. 복사해 쓰는 **시험용 틀**이며 2차 과제에서 채점하지 않는다.
- `useFake = true`일 때만 보이고(55번), `준비됨`일 때만 켜진다(53·54번). 실보드(`useFake = false`)에서는 보이지 않는다.
- 이 버튼을 넣지 않으려면 `activity_main.xml`의 `lostTestButton`, `strings.xml`의 `lost_test`, `FakeBleunoClient` import, 53·54·55번 줄을 넣지 않는다. 그러면 Fake로는 끊김을 만들 수 없다.

### 11. 제어 화면에서 끊겼을 때 알리기

실보드 시연에서는 보통 제어 화면에서 보드 전원을 끈다. 그때 제어 화면도 알려 주게 한다.

1. `ControlActivity.kt`의 `// 4.` collect 안, 6단계의 `// 26.` `stopInput()` **아래**에 넣는다.

```kotlin
                    // 26. 상태가 바뀌면(끊김 등) 온습도 받기를 멈추고, 준비됨일 때만 [온습도 받기 시작]을 켠다. 25번 함수가 한다(14주차 1일차).
                    stopInput()
                    // 29. 끊겼으면 Toast로 알린다. [재연결]은 연결 화면에 있으므로 [뒤로]로 돌아가라고 안내한다(14주차 1일차).
                    //     collect 틀 안에서는 this가 Activity가 아니어서 Toast는 30번 함수로 띄운다. 끊김인 채로 이 화면이 다시 보이면(회전 등) 또 뜬다.
                    if (state == ConnState.LOST) {
                        showLostToast()
                    }
```

2. 클래스 끝, 6단계의 `stopInput()` 함수 **아래**에 한 줄을 비우고 함수를 넣는다.

```kotlin
    // 30. 제어 화면에서 끊겼다고 알리는 Toast. 29번(collect 안)에서 부른다(14주차 1일차).
    //     연결 화면 46번과 같은 이유로 함수로 뺐다. 함수 안의 this는 Activity라서 Toast.makeText(this, …)를 그대로 쓴다.
    private fun showLostToast() {
        Toast.makeText(this, "연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
    }
```

3. 실행한다. 연결 화면에서 `준비됨` → [끊김 시험]으로 끊은 뒤, [연결] 버튼(4주차, 늘 켜짐)으로 제어 화면에 들어간다. `상태: 끊김`, Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`, LED Switch·[전체 끄기]·[온습도 받기 시작]·[중지]가 모두 회색이면 성공이다.
4. [뒤로]를 누른다. 연결 화면에 돌아오는 순간 연결 화면 Toast `연결이 끊겼습니다. [재연결]을 누르세요`가 뜨고 [재연결]이 보인다.

- [재연결] 버튼은 연결을 시작하는 연결 화면에만 둔다. 제어 화면은 알리고 [뒤로]로 안내만 한다.
- 30번을 함수로 뺀 이유는 연결 화면 46번과 같다. 두 함수는 파일이 달라 이름이 같아도 된다.

완성한 `ControlActivity.kt`(277행)는 [examples/day1/ControlActivity.kt](examples/day1/ControlActivity.kt)에 있다. 파일이 길어 여기에는 다시 싣지 않는다.
내 파일과 비교할 때는 예제 파일을 열고, Android Studio에서 두 파일을 골라 오른쪽 클릭 › **Compare Files**를 쓴다. 이번 주에 넣은 곳은 아래와 같다.

| 주석 번호 | 하는 일 | 예제 파일 줄 |
|---|---|---|
| import | `ArrayAdapter`·`Job`·`isActive`·`SimpleDateFormat`·`Date`·`Locale` | 4, 20, 22, 24~26 |
| 클래스 안 | `history`·`historyAdapter`·`inputJob` | 32~39 |
| 26·29 | collect 안에서 받기 멈추기, 끊김이면 Toast | 104~110 |
| 18 | 입력 이력에 어댑터 붙이기 | 142~144 |
| 19·20 | [온습도 받기 시작]·[중지] | 146~162 |
| 28 | 이력 줄 누르기(`split`) | 164~172 |
| 21·22·23 | 받은 줄 세 갈래로 가르기(바꾼 한 줄은 195행) | 182~195 |
| 27 | `onStop`에서 받기 멈추기 | 219~220 |
| 24 | `addHistory()` | 252~259 |
| 25 | `stopInput()` | 261~270 |
| 30 | `showLostToast()` | 272~276 |

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다. 주석 번호가 없어도 괜찮다. 13주차 확장을 하지 않았다면 `// (확장)`이 붙은 네 줄, `// 17.` 덩어리, `import android.widget.SeekBar`가 없다.

### 12. 연결 시간 제한 10초

1. `MainActivity.kt` 클래스 안, 9단계의 `lastAddress` 줄 **아래**에 한 줄을 비우고 넣는다.

```kotlin
    // 14주차 1일차: 연결 시간 제한 코루틴. 다시 연결할 때 앞의 것을 취소하려고 보관한다(6주차 scanJob과 같다). 아직 없으면 null이다.
    private var connectTimeoutJob: Job? = null
```

2. 클래스 끝, 9단계의 `showLostToast()` 함수 **아래**에 한 줄을 비우고 두 함수를 넣는다.

```kotlin
    // 50. 연결 시간 제한을 건다. 앞에서 건 제한이 남아 있으면 먼저 취소한다(14주차 1일차).
    //     취소하지 않으면 앞 연결의 10초 예약이 새 연결을 끊을 수 있다. 6주차 [중지]의 scanJob?.cancel()과 같은 방법이다.
    private fun startConnectTimeout() {
        connectTimeoutJob?.cancel()
        connectTimeoutJob = lifecycleScope.launch {
            waitConnectTimeout()
        }
    }

    // 51. 10초를 기다린 뒤에도 아직 연결 중·서비스 확인 중이면 "연결 시간이 초과되었습니다"를 알리고 연결을 끊는다(14주차 1일차).
    //     그사이 준비됨·끊김·연결 안 됨이 되었으면 아무것도 하지 않는다. listOf(…).contains(…)는 13주차 오늘 문법이다.
    //     delay를 쓰므로 suspend가 붙는다(6주차 countDown과 같다). 이 함수 안의 this는 Activity라서 Toast에 그대로 쓴다.
    private suspend fun waitConnectTimeout() {
        delay(10000)
        val state = client.connectionState.value
        if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
            Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
            client.disconnect()
            // 실제 보드는 아직 맺어지지 않은 연결을 끊으면 "끊겼다"는 알림이 오지 않는 기기가 있다. 그러면 상태가 "연결 중"에 머물러
            // 7번이 화면을 고치지 않으므로, 여기서 직접 [검색]·[다시 시도]를 쓸 수 있는 모양으로 되돌린다(12주차 34번과 같은 모양).
            // 나중에 알림이 오면 7번이 "연결 안 됨" 모양으로 다시 고친다.
            binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.retryButton.visibility = View.VISIBLE
        }
    }
```

3. 연결을 시작하는 두 곳에서 부른다. `// 19.` 목록 줄 리스너의 `// 43.` 두 줄 **아래**, 그리고 `// 47.` [재연결] 리스너의 `client.connect(lastAddress)` **아래**다. 두 곳 모두 같은 `// 49.` 한 줄이다.

```kotlin
            client.connect(address)
            // 43. 연결을 시작한 주소를 기억하고, 앱 전용 저장소 "smartio"에 "lastAddress"라는 이름표로도 저장한다(14주차 1일차).
            //     20번 장치 이름 저장과 같은 틀이다(11주차 2일차). 저장해 두면 화면이 새로 만들어져도 [재연결]이 이 주소를 쓴다(48번).
            lastAddress = address
            getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
            // 49. 10초 연결 시간 제한을 건다. 시간 제한은 50번 함수가 한다(14주차 1일차).
            startConnectTimeout()
        }
```

```kotlin
        // 47. [재연결] 버튼: 끊김일 때만 보인다(45번). 마지막으로 연결한 주소로 다시 연결한다(14주차 1일차).
        //     주소가 비어 있으면(앱을 설치하고 한 번도 목록을 눌러 연결한 적이 없으면) [검색]부터 하라고 알린다.
        binding.reconnectButton.setOnClickListener {
            if (lastAddress.isEmpty()) {
                Toast.makeText(this, "마지막 주소가 없습니다. [검색]부터 하세요", Toast.LENGTH_SHORT).show()
            } else {
                client.connect(lastAddress)
                // 49. 10초 연결 시간 제한을 건다(14주차 1일차).
                startConnectTimeout()
            }
        }
```

4. `// 48.` `lastAddress = prefs.getString(…)` 줄 **아래**에 한 줄을 비우고 넣는다.

```kotlin
        // 48. 43번에서 저장한 마지막 보드 주소를 꺼내 lastAddress에 넣는다. 21번과 같은 틀이다(14주차 1일차).
        lastAddress = prefs.getString("lastAddress", "") ?: ""

        // 52. 연결 중에 회전하면 화면이 새로 만들어지면서 앞 화면의 10초 예약도 함께 취소된다. 아직 연결 중·서비스 확인 중이면 시간 제한을 다시 건다(14주차 1일차).
        //     새로 거는 것이라 10초를 처음부터 다시 센다. 51번과 같은 listOf(…).contains(…) 검사다.
        if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(client.connectionState.value)) {
            startConnectTimeout()
        }
```

5. `// 7.` collect의 `ConnState.CONNECTING ->` 가지에 설명 줄 하나를 붙인다(주석이라 없어도 동작은 같다).

```kotlin
                        ConnState.CONNECTING -> {
                            // 연결 중에는 버튼을 모두 꺼 둔다. [중지]는 이제 검색 멈춤이라 켜지 않는다(12주차 2일차).
                            // 보드가 응답하지 않으면 한참(보통 30초쯤) 뒤 "끊김"이 되어 [검색]·[다시 시도]가 다시 켜진다.
                            // 14주차 1일차: 이제는 10초가 지나도 준비됨이 아니면 51번이 연결을 끊고 [검색]·[다시 시도]를 되살린다.
                            binding.scanProgress.visibility = View.VISIBLE
                        }
```

6. 빨간 글자를 Alt+Enter → Import로 가져온다. `launch`는 이미 있다.

| 빨간 글자 | 가져올 import |
|---|---|
| `Job` | `kotlinx.coroutines.Job` |
| `delay` | `kotlinx.coroutines.delay` |

7. 실행하고 목록 줄을 누른다. 가짜 보드는 약 2초 만에 `준비됨`이 되므로 10초가 지나도 Toast가 뜨지 않는다. 이것이 정상이다.
8. 시간 초과를 눈으로 확인해 본다. 51번의 `delay(10000)`을 **잠시** `delay(1000)`으로 바꾸고 실행해 목록 줄을 누른다. 약 1초 뒤 아래처럼 된다(예상, 실행 확인 전).

```text
[검색] [중지] [해제]          ← [검색] 켜짐
연결 시간 초과 — [다시 시도]를 누르세요
검색된 장치
ESP32_BLE_FAKE1 (00:11:22:33:44:01)
[연결]
[제어 화면]
[다시 시도]
연결 시간이 초과되었습니다    ← Toast
```

   ProgressBar는 사라진다. 상태 글자가 `연결 안 됨`이고 [다시 시도]가 숨겨진 모양으로 보여도 기능상 문제는 없다. 이 화면을 **캡처해 둔다**(레포트의 시간 초과 칸). 확인했으면 **반드시 `delay(10000)`으로 되돌린다.**

- `startConnectTimeout()` + `suspend fun waitConnectTimeout()`: 6주차 2일차 `scanJob = lifecycleScope.launch { countDown() }`와 `private suspend fun countDown()`의 모양 그대로다. 안에서 `delay`를 부르므로 `suspend`가 붙는다. `delay`의 숫자는 **밀리초**라 `10000`이 10초다.
- `connectTimeoutJob?.cancel()`을 먼저 한다. 앞 연결의 10초 예약이 남아 새 연결을 끊는 일을 막는다(6주차 [중지]와 같은 방법).
- 10초 뒤 상태가 `연결 중`·`서비스 확인 중`일 **때만** 끊는다. 그사이 `준비됨`이나 `끊김`이 되었으면 건드리지 않아야 [재연결]이 보이는 화면을 덮지 않는다. `listOf(…).contains(…)`는 13주차 오늘 문법이다. `client.connectionState.value`는 7주차 `_state.value`와 같은 "지금 값"이다.
- Toast를 `waitConnectTimeout()` 함수 **안**에서 띄운다. 함수 안의 `this`는 화면이라 된다(collect·launch 틀 안이 아니다).
- `client.disconnect()` 뒤 네 줄은 화면을 직접 되돌린다. 실보드는 아직 맺어지지 않은 연결을 끊으면 "끊겼다"는 알림이 오지 않는 기기가 있어, 그러면 상태가 `연결 중`에 머물러 7번 collect가 화면을 고치지 않기 때문이다. 12주차 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`와 같은 모양이다.
- 52번: `연결 중`에 화면을 돌리면 앞 화면의 10초 예약이 화면과 함께 취소된다. 새 화면의 onCreate에서 아직 연결 중이면 시간 제한을 다시 건다(10초를 처음부터 센다).

완성한 `MainActivity.kt`(493행)는 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다. 파일이 길어 여기에는 다시 싣지 않는다.
내 파일과 비교할 때는 예제 파일을 열고 **Compare Files**를 쓴다. 이번 주에 넣은 곳은 아래와 같다.

| 주석 번호 | 하는 일 | 예제 파일 줄 |
|---|---|---|
| import | `FakeBleunoClient`·`Job`·`delay` | 32, 35, 36 |
| 클래스 안 | `lastAddress`·`connectTimeoutJob` | 103~108 |
| 44·53 | collect에서 [재연결] 숨기기, [끊김 시험] 끄기 | 246~249 |
| (설명 줄) | `연결 중` 가지의 14주차 설명 | 257 |
| 54 | `준비됨`이면 [끊김 시험] 켜기 | 267~268 |
| 45 | 끊김이면 [재연결] 보이기와 Toast | 273~276 |
| 43·49 | 목록 줄: 주소 저장, 시간 제한 걸기 | 303~308 |
| 48·52 | onCreate: 주소 꺼내기, 연결 중이면 시간 제한 다시 걸기 | 329~337 |
| 47·49 | [재연결] 리스너 | 348~358 |
| 55 | (시험용) [끊김 시험] | 360~368 |
| 46 | `showLostToast()` | 460~464 |
| 50·51 | `startConnectTimeout()`·`waitConnectTimeout()` | 466~492 |

`private val useFake = true`(88행)는 실보드로 바꿀 때만 `false`로 고친다(15단계).

### 13. 화면 돌리기와 홈에서 확인할 것

아래는 코드가 틀린 것이 아니라 이번 주 코드의 정해진 동작이다. 발표 전에 한 번씩 해 보고 놀라지 않게 한다.

| 조작 | 보이는 것 | 까닭 |
|---|---|---|
| 제어 화면에서 받는 중에 회전 | 입력 이력이 비고, 받기가 꺼진다 | `history`는 그 화면의 목록이다. 회전하면 화면이 새로 만들어지고 27번(onStop)이 받기를 멈춘다 |
| 받는 중 홈 → 앱으로 돌아오기 | 이력은 그대로, 받기는 꺼져 있다 | 27번(onStop) |
| `끊김`인 채로 회전, 제어 화면에서 [뒤로], 홈에서 돌아오기 | 끊김 Toast가 또 뜬다 | StateFlow가 마지막 값을 다시 준다(7주차) |
| `준비됨` → [제어 화면] → 회전 → [뒤로] → [끊김 시험] → [재연결] | `준비됨`까지 간다 | 43번에서 저장한 주소를 새 화면의 48번이 꺼냈다 |
| 가만히 둔 제어 화면에서 첫 `입력=` 줄 | 들어온 뒤 0~10초 사이 아무 때나 | 가짜 보드는 `준비됨`이 된 순간부터 10초마다 보내고, 제어 화면이 보이기 전에 온 것은 버려진다 |

캡처는 **세로 화면**에서 찍는다.

### 14. 캡처 세트와 2~3분 시연 리허설

2차 과제 발표에서 보여 줄 장면을 캡처로도 남긴다. 레포트에 넣는 캡처 세트는 일곱 장이다. 1~6번은 여기서 찍고, 7번은 12단계 8번에서 찍어 둔 것을 쓴다.

| 번호 | 캡처 | 찍는 곳 |
|---|---|---|
| 1 | 권한 안내: [권한 확인] → Toast `권한 OK`, 또는 거절 뒤 AlertDialog `권한이 필요합니다` | 연결 화면 |
| 2 | 장치 목록: `검색된 장치`에 `ESP32_BLE…` 줄 | 연결 화면 |
| 3 | 준비됨: 상태 `준비됨`, [제어 화면] 켜짐 | 연결 화면 |
| 4 | LED on/off: `상태: 준비됨`, 명령 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`(실보드면 LED가 켜진 보드 사진도) | 제어 화면 |
| 5 | 입력 수신: 입력 이력에 `시:분:초 [온도,습도]` 줄 3줄 이상과 켜진 [중지], 또는 `시:분:초 입력=1`/`입력=0` 3줄(Fake, 약 30초) | 제어 화면 |
| 6 | 끊김 + [재연결]: 상태 `끊김`과 [재연결] 버튼(Toast가 함께 찍히면 더 좋다) | 연결 화면 |
| 7 | 시간 초과: Toast `연결 시간이 초과되었습니다`와 [다시 시도] (12단계 8번에서 찍은 것) | 연결 화면 |

이어서 아래 순서로 2~3분 시연을 한 바퀴 해 본다. 시간을 재고, 막힌 곳을 적어 둔다.

```text
0:00  [권한 확인] → 권한 OK
0:10  [검색] → ESP32_BLE_FAKE1 줄 탭 → 연결 중 → 서비스 확인 중 → 준비됨
0:30  [제어 화면] → 3 입력 → LED 켜기·끄기 → on 3 / 응답 줄
0:50  [온습도 받기 시작] → 약 6초 → 이력 3줄 → 이력 줄 하나 탭(Toast) → [중지]
1:20  [뒤로] → [끊김 시험] → 끊김 + Toast + [재연결]
1:40  [재연결] → 준비됨
2:00  [해제] → 연결 안 됨
2:10  마무리 한 문장
```

- 실보드로 시연한다면 1:20 줄이 바뀐다. 제어 화면에서 받는 중에 **보드 전원을 끈다** → `상태: 끊김` + Toast → [뒤로] → 연결 화면 Toast·[재연결] → 보드 전원을 켜고 파랑 깜빡임을 기다린다 → [재연결] → `준비됨`.
- 마지막 [해제] → `연결 안 됨`은 채점표 "연결 흐름" 만점에 들어가는 장면이다. 줄이더라도 빼지 않는다.
- 연결 시간 제한은 시연 시간 안에 보이기 어렵다. 12단계 8번에서 찍은 시간 초과 화면(7번 캡처)을 레포트 표의 시간 초과 칸에 넣고, 질문 시간에 쓴다.
- 자세한 발표 규칙과 채점은 [2차 과제 안내](project_brief.md)와 [채점표](rubric.md)에 있다.

### 15. 실제 보드로 해 보기

보드와 실기기가 있으면 실제 보드로 한 바퀴 해 본다.

1. 보드 LED가 파랑 깜빡임인지 본다.
2. `MainActivity.kt`의 `private val useFake = true`를 `false`로 바꾸고, 기기 목록에서 실기기를 골라 `Run ▶`. [끊김 시험]은 보이지 않는다.
3. [검색] → `ESP32_BLE…` 줄 탭 → `준비됨` → [제어 화면] → [온습도 받기 시작]. 이력에 보드가 잰 온도·습도가 3초마다 쌓인다. Logcat `tag:BLE`에는 한 번 받을 때마다 아래 순서가 찍힌다.

```text
send: 큐에 추가 "dht11" (대기 1개)
writeCharacteristic("dht11") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","value":"[24.5,40.0]"}
```

4. 받는 중에 보드 전원을 끈다. 몇 초 뒤 `상태: 끊김` + Toast, 버튼이 모두 회색이 되고 이력이 더 늘지 않는다. Logcat에는 `onConnectionStateChange: status=… newState=0`과 `STATE_DISCONNECTED → gatt.close()`가 찍힌다.
5. [뒤로] → 보드 전원을 켜고 파랑 깜빡임을 기다린다 → [재연결] → `준비됨`.

- 실보드는 입력 이벤트(`{"event":"input",…}`)를 보내지 않는다. 지금 펌웨어에는 보드가 먼저 보내는 메시지가 없다. 실보드의 입력 수신은 `dht11` 응답으로 보인다.
- 앱 문제인지 보드 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다. Fake에서 되고 실보드에서 안 되면 Logcat `tag:BLE`의 마지막 줄을 조교에게 보여 준다.
- 에뮬레이터로 돌아갈 때는 `useFake = true`로 되돌린다.

### 16. 바꾸지 않는 파일 확인하기

아래 파일은 13주차 2일차에 만든 그대로이며 이번 주에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.

- `AndroidManifest.xml`, `ContactsReader.kt`, `colors.xml`, `res/values/themes.xml` — [부록 A](#부록-a--바꾸지-않는-파일-전체), [examples/day1](examples/day1)
- `bleuno` 패키지 8개 — [부록 B](#부록-b--제공-bleuno-파일-전체), [bleuno/src](../../bleuno/src)

`AndroidManifest.xml`에 더할 권한은 없다. `dht11` 보내기, 응답 받기, 재연결은 10주차에 넣은 `BLUETOOTH_CONNECT`(Android 12 이상) 권한 안에 들어 있다.

## 2일차

2일차는 2차 과제 발표다. 새로 만드는 코드는 없다. 발표 순서와 규칙은 [실습지 2일차](lab.md#2일차--2차-과제-발표-60분)에 있다.

### 17. 발표 전 점검

1. 마지막으로 고친 파일을 모두 저장하고 `Run ▶`으로 **다시 실행**한다.
2. 시연할 방법을 정한다. 보드·실기기로 하면 `useFake = false`, 에뮬레이터로 하면 `useFake = true`다. 바꿨으면 다시 실행한다.
3. 14단계의 시연 순서를 한 번 돌린다. 끝나면 앱을 첫 화면(`연결 안 됨`)에 둔다. `끊김`에서 멈췄으면 [재연결] → [해제]로 돌려놓는다.
4. 코드 설명 질문에 쓸 파일(`ControlActivity.kt`, `MainActivity.kt`)을 편집기 탭에 열어 두고, 편집기 왼쪽 줄 번호가 보이게 한다.
5. Logcat 필터 `package:mine tag:BLE`를 켜 둔다. 장애가 나면 이 창이 증거가 된다.
6. 실기기라면 방해 금지 모드를 켜고 화면 꺼짐 시간을 늘린다. 보드는 파랑 깜빡임인지 본다.

### 18. 실보드가 안 될 때 Fake로 바꾸기

발표 중 보드가 검색되지 않거나 연결이 계속 끊기면 **먼저 손을 든다.** 조교가 시각과 증상을 적은 뒤 아래 순서로 바꾼다.

1. Logcat `tag:BLE`의 마지막 몇 줄을 조교에게 보여 준다(예: `onScanResult` 줄이 없음, `연결 중`에서 멈춤).
2. `MainActivity.kt`의 `private val useFake = false`를 `true`로 바꾼다.
3. 에뮬레이터(또는 같은 실기기)로 `Run ▶`한다. 가짜 클라이언트는 보드 없이 같은 화면 흐름을 낸다.
4. 14단계의 Fake 시연 순서대로 이어서 보인다. 끊김은 [끊김 시험]으로 만든다.

- Fake에서 모두 되면 **앱은 정상이고 장비 쪽 문제**라는 근거가 된다. 조교 기록과 함께 채점표의 장애 규칙으로 본다.
- Fake에서도 안 되면 내 코드 문제다. 장애가 아니다.

### 19. 발표와 제출

1. 차례가 되면 준비한 순서대로 2~3분 시연하고, 평가자의 코드 설명 질문 한 개에 **파일 열기 → 줄 가리키기 → 한 문장**으로 답한다.
2. 발표를 마치면 레포트 PDF와 소스 압축 파일(`app/src/main`)이 제출 칸에 올라갔는지 확인한다. 이름과 마감은 [과제 안내](project_brief.md#레포트)를 따른다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다. `Cannot infer type for this parameter.`처럼 뒤에 따라 나오는 줄은 첫 줄을 고치면 사라지는 경우가 많다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
이력이 안 쌓이면 Logcat `tag:BLE`에서 `writeCharacteristic` 줄(보낸 글자)과 `onCharacteristicChanged` 줄(받은 대답)을 차례로 본다. 보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다.

## 부록 A — 바꾸지 않는 파일 전체

아래 파일은 13주차 `examples/day2`와 글자 단위로 같다. 이번 주에 바꾸지 않는다. 같은 코드가 [examples/day1](examples/day1)에 있다.

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- 10주차 2일차: BLE를 쓰는 앱이라고 알린다. -->
    <uses-feature
        android:name="android.hardware.bluetooth_le"
        android:required="true" />

    <!-- 10주차 2일차: Android 12(API 31) 이상에서 쓰는 BLE 권한. 실행 중에도 허락받아야 한다. -->
    <uses-permission
        android:name="android.permission.BLUETOOTH_SCAN"
        android:usesPermissionFlags="neverForLocation"
        tools:targetApi="s" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

    <!-- 10주차 2일차: Android 11(API 30) 이하에서 쓰는 권한. ACCESS_FINE_LOCATION은 실행 중에도 허락받아야 한다. -->
    <uses-permission
        android:name="android.permission.BLUETOOTH"
        android:maxSdkVersion="30" />
    <uses-permission
        android:name="android.permission.BLUETOOTH_ADMIN"
        android:maxSdkVersion="30" />
    <uses-permission
        android:name="android.permission.ACCESS_FINE_LOCATION"
        android:maxSdkVersion="30" />

    <!-- 11주차 2일차: 연락처 앱의 데이터(ContentProvider)를 읽는 권한. 실행 중에도 허락받아야 한다. -->
    <uses-permission android:name="android.permission.READ_CONTACTS" />

    <application
        android:label="@string/app_name"
        android:theme="@style/Theme.SmartIO">

        <!-- New › Activity로 만들면 이 줄이 자동으로 생긴다. -->
        <activity
            android:name=".ControlActivity"
            android:exported="false" />

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

`ContactsReader.kt` — [examples/day1/ContactsReader.kt](examples/day1/ContactsReader.kt)

```kotlin
package com.example.smartio

import android.content.ContentResolver
import android.provider.ContactsContract

// 1. 연락처 앱이 ContentProvider로 내주는 연락처 이름을 읽어 목록으로 돌려준다(11주차 2일차, 제공 코드).
//    다른 앱의 데이터는 직접 열 수 없고, ContentResolver에 content URI(창구 주소)를 주고 query로 요청한다.
//    READ_CONTACTS 권한이 허용된 뒤에만 부른다. 연락처가 없으면 빈 목록(0건)을 돌려준다. 0건은 실패가 아니다.
object ContactsReader {
    fun names(resolver: ContentResolver): List<String> {
        val names = mutableListOf<String>()

        // 2. query(주소, 가져올 칸, 조건, 조건 값, 정렬): 연락처 목록에서 "표시 이름" 칸만 이름순으로 달라고 요청한다.
        val cursor = resolver.query(
            ContactsContract.Contacts.CONTENT_URI,
            arrayOf(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY),
            null,
            null,
            ContactsContract.Contacts.DISPLAY_NAME_PRIMARY + " ASC"
        )
        // 결과를 못 받으면(null) 빈 목록을 그대로 돌려준다.
        if (cursor == null) {
            return names
        }

        // 3. cursor는 결과 표를 한 줄씩 가리키는 손가락이다. moveToNext()가 다음 줄로 옮기고, 더 없으면 false가 되어 반복이 끝난다.
        val nameColumn = cursor.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY)
        while (cursor.moveToNext()) {
            val name: String? = cursor.getString(nameColumn)
            if (name != null) {
                names.add(name)
            }
        }

        // 4. 다 읽었으면 반드시 닫는다. 닫지 않으면 결과 표가 메모리에 계속 남는다.
        cursor.close()
        return names
    }
}
```

`colors.xml` — [examples/day1/colors.xml](examples/day1/colors.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

`res/values/themes.xml` — [examples/day1/res/values/themes.xml](examples/day1/res/values/themes.xml)

```xml
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Base.Theme.SmartIO" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your light theme here. -->
        <!-- <item name="colorPrimary">@color/my_light_primary</item> -->
    </style>

    <style name="Theme.SmartIO" parent="Base.Theme.SmartIO" />
</resources>
```

## 부록 B — 제공 bleuno 파일 전체

아래 8개 파일은 12주차에 넣은 제공 코드이며 [bleuno/src](../../bleuno/src)와 글자 단위로 같다. 고치지 않는다. 위치는 `app › kotlin+java › com.example.smartio › bleuno`다.

### ConnState.kt

```kotlin
package com.example.smartio.bleuno

// 연결 상태를 나타내는 한글 문자열 모음.
// 화면의 TextView에 그대로 넣어 보여 준다. 7주차 ConnViewModel의 ConnState와 같은 다섯 가지다.
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 사용자가 해제한 뒤
    const val CONNECTING = "연결 중"        // connect()를 부른 뒤 보드와 연결되기 전
    const val DISCOVERING = "서비스 확인 중" // 연결은 되었고 서비스·특성을 찾는 중
    const val READY = "준비됨"              // 명령을 보낼 수 있는 상태
    const val LOST = "끊김"                 // 사용자가 해제하지 않았는데 연결이 끊어짐
}
```

### BleunoDevice.kt

```kotlin
package com.example.smartio.bleuno

// 검색으로 찾은 보드 하나의 정보.
// name: 기기 이름(ESP32_BLE로 시작), address: 연결할 때 쓰는 주소, rssi: 신호 세기(클수록 가까움, 보통 음수)
data class BleunoDevice(val name: String, val address: String, val rssi: Int)
```

### BleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import kotlinx.coroutines.flow.StateFlow

// bleuno 보드와 이야기하는 방법을 정한 인터페이스.
// 실제 보드용 RealBleunoClient와 보드 없이 연습하는 FakeBleunoClient가 이 인터페이스를 똑같이 구현한다.
// 앱 코드는 이 인터페이스만 보고 쓰므로 fake ↔ real을 바꿔도 앱 코드는 그대로다.
interface BleunoClient {

    // 현재 연결 상태. 값은 ConnState의 다섯 문자열 중 하나다. collect { }로 화면에 반영한다.
    val connectionState: StateFlow<String>

    // 지금 명령을 보낼 수 있으면 true (connectionState.value == ConnState.READY)
    val isReady: Boolean

    // 보드를 검색한다. 찾을 때마다 onFound가, timeoutMs가 지나면 onFinished가 메인 스레드에서 불린다.
    fun startScan(timeoutMs: Long = 5000, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit = {})

    // 검색을 바로 멈춘다. 이때도 onFinished가 한 번 불린다.
    fun stopScan()

    // 주소로 연결을 시작한다. 상태가 연결 중 → 서비스 확인 중 → 준비됨 순서로 바뀐다.
    fun connect(address: String)

    // 연결을 끊는다. 끝나면 상태가 "연결 안 됨"이 된다.
    fun disconnect()

    // 명령 한 줄을 보낸다. 끝의 "\n"은 자동으로 붙인다. 큐에 넣고 순서대로 하나씩 보낸다.
    fun send(command: String)

    // 보드가 보낸 응답·이벤트(JSON 한 줄)를 받을 리스너. 메인 스레드에서 불린다. null이면 해제한다.
    fun onMessage(listener: ((String) -> Unit)?)
}
```

### Bleuno.kt

```kotlin
package com.example.smartio.bleuno

import android.content.Context

// 앱 전체가 공유하는 BleunoClient 보관소.
// MainActivity에서 create()로 만들고, ControlActivity에서는 Bleuno.client로 같은 연결을 이어 쓴다.
object Bleuno {

    // 앱 어디서나 같은 객체를 쓴다. create()를 부르기 전에는 null이다.
    var client: BleunoClient? = null

    // fake = true 면 보드 없이 동작하는 FakeBleunoClient, false 면 실제 보드용 RealBleunoClient를 만든다.
    // 만든 객체는 client에 보관한 뒤 그대로 돌려준다.
    fun create(context: Context, fake: Boolean): BleunoClient {
        val created: BleunoClient = if (fake) {
            FakeBleunoClient()
        } else {
            RealBleunoClient(context.applicationContext)
        }
        client = created
        return created
    }
}
```

### PermissionHelper.kt

```kotlin
package com.example.smartio.bleuno

import android.Manifest
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.pm.PackageManager
import android.location.LocationManager
import android.os.Build
import androidx.core.content.ContextCompat

// BLE에 필요한 런타임 권한과 기기 설정을 확인하는 도우미.
// Android 12(API 31)부터는 BLUETOOTH_SCAN·BLUETOOTH_CONNECT, 그 이하는 ACCESS_FINE_LOCATION이 필요하다.
object PermissionHelper {

    // 이 기기의 Android 버전에서 사용자에게 요청해야 하는 권한 목록
    fun required(): Array<String> {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
        } else {
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }

    // required() 중 아직 허용되지 않은 권한만 골라 준다. 비어 있으면 모두 허용된 것이다.
    fun missing(context: Context): Array<String> {
        return required().filter { permission ->
            ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()
    }

    // 필요한 권한이 모두 허용되어 있으면 true
    fun hasAll(context: Context): Boolean = missing(context).isEmpty()

    // 블루투스가 켜져 있으면 true. 블루투스가 없는 기기(일부 에뮬레이터)에서는 false.
    fun isBluetoothEnabled(context: Context): Boolean {
        val manager = context.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager
        val adapter = manager?.adapter ?: return false
        return adapter.isEnabled
    }

    // 위치 서비스가 켜져 있으면 true. Android 11 이하에서 검색 결과가 0개일 때 원인을 찾는 용도다.
    // API 28 미만에는 확인 API가 없으므로 true로 본다.
    fun isLocationEnabled(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.P) return true
        val manager = context.getSystemService(Context.LOCATION_SERVICE) as? LocationManager
        return manager?.isLocationEnabled ?: true
    }
}
```

### BleunoMessage.kt

```kotlin
package com.example.smartio.bleuno

import org.json.JSONException
import org.json.JSONObject

// 보드가 보낸 JSON 한 줄에서 값을 꺼내는 도우미.
// 예: {"result":"ok","ms":"led(s) on"} → result(json) == "ok", message(json) == "led(s) on"
// 잘못된 JSON이면 예외를 던지지 않고 null을 돌려준다.
object BleunoMessage {

    // "result" 값: "ok" | "err" | "fail" | null(없거나 JSON이 아님)
    fun result(json: String): String? = field(json, "result")

    // "ms" 값: 사람이 읽는 메시지 (예: "led(s) on", "unknown command")
    fun message(json: String): String? = field(json, "ms")

    // "value" 값: dht11 응답의 "[24.5,40.0]" 처럼 값이 들어 있는 문자열
    fun value(json: String): String? = field(json, "value")

    // "event" 값: 보드가 먼저 보내는 이벤트 종류 (입력 이벤트 가안: "input")
    fun event(json: String): String? = field(json, "event")

    // result가 "ok"이면 true
    fun isOk(json: String): Boolean = result(json) == "ok"

    // 키 하나를 문자열로 꺼낸다. 키가 없거나 JSON이 아니면 null.
    private fun field(json: String, key: String): String? {
        return try {
            val obj = JSONObject(json)
            if (obj.has(key)) obj.getString(key) else null
        } catch (e: JSONException) {
            null
        }
    }
}
```

### FakeBleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONObject

// 보드 없이 앱을 만들고 시험할 때 쓰는 가짜 클라이언트.
// RealBleunoClient와 같은 순서·같은 JSON으로 답하되, 시간은 모두 메인 스레드 Handler.postDelayed로 흉내 낸다.
//   검색: 1초 뒤 ESP32_BLE_FAKE1, 2초 뒤 ESP32_BLE_FAKE2 발견, timeoutMs 뒤 onFinished
//   연결: connect → 연결 중(1초) → 서비스 확인 중(1초) → 준비됨
//   전송: send → 300ms 뒤 펌웨어와 같은 JSON 응답
//   이벤트: 준비됨 상태에서 10초마다 {"event":"input","index":0,"value":0|1}
//   simulateLost(): 보드 전원이 꺼진 것처럼 "끊김"으로 만든다
class FakeBleunoClient : BleunoClient {

    companion object {
        const val TAG = "BLE"
        const val FOUND_DELAY_1 = 1000L
        const val FOUND_DELAY_2 = 2000L
        const val CONNECT_DELAY = 1000L
        const val DISCOVER_DELAY = 1000L
        const val RESPONSE_DELAY = 300L
        const val INPUT_EVENT_INTERVAL = 10000L
        const val LED_COUNT = 4          // 수업 보드의 LED 개수 (인덱스 0~3)
    }

    private val fakeDevices = listOf(
        BleunoDevice("ESP32_BLE_FAKE1", "00:11:22:33:44:01", -50),
        BleunoDevice("ESP32_BLE_FAKE2", "00:11:22:33:44:02", -70),
    )

    // 용도별로 Handler를 나눠서 removeCallbacksAndMessages(null)로 그 용도의 예약만 취소한다
    private val scanHandler = Handler(Looper.getMainLooper())
    private val connectHandler = Handler(Looper.getMainLooper())
    private val sendHandler = Handler(Looper.getMainLooper())
    private val eventHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    private var isScanning = false
    private var onFinishedListener: (() -> Unit)? = null
    private var messageListener: ((String) -> Unit)? = null

    private var inputValue = 0     // 입력 이벤트의 value, 10초마다 0/1 토글
    private var dhtCount = 0       // dht11 응답 값을 조금씩 바꾸기 위한 횟수

    // ---------------------------------------------------------------- 검색

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (isScanning) stopScan()
        isScanning = true
        onFinishedListener = onFinished
        Log.d(TAG, "startScan(가짜): ${timeoutMs}ms 동안 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[0].name}")
            onFound(fakeDevices[0])
        }, FOUND_DELAY_1)
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[1].name}")
            onFound(fakeDevices[1])
        }, FOUND_DELAY_2)
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout(가짜) (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "stopScan(가짜)")
        val finished = onFinishedListener
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    override fun connect(address: String) {
        connectHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "connectGatt(가짜): $address")
        _connectionState.value = ConnState.CONNECTING
        connectHandler.postDelayed({
            Log.d(TAG, "onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중")
            _connectionState.value = ConnState.DISCOVERING
            connectHandler.postDelayed({
                Log.d(TAG, "onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨")
                _connectionState.value = ConnState.READY
                scheduleInputEvent()
            }, DISCOVER_DELAY)
        }, CONNECT_DELAY)
    }

    override fun disconnect() {
        cancelAll()
        Log.d(TAG, "disconnect(가짜) → 연결 안 됨")
        _connectionState.value = ConnState.DISCONNECTED
    }

    // 보드 전원이 꺼진 상황을 흉내 낸다. 상태가 "끊김"이 된다.
    fun simulateLost() {
        cancelAll()
        Log.d(TAG, "simulateLost(가짜) → 끊김")
        _connectionState.value = ConnState.LOST
    }

    private fun cancelAll() {
        connectHandler.removeCallbacksAndMessages(null)
        sendHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
    }

    // 준비됨 상태인 동안 10초마다 입력 이벤트를 보낸다 (보드 버튼 입력 가안 형식)
    private fun scheduleInputEvent() {
        eventHandler.postDelayed({
            if (!isReady) return@postDelayed
            inputValue = 1 - inputValue
            val json = JSONObject()
            json.put("event", "input")
            json.put("index", 0)
            json.put("value", inputValue)
            deliver(json.toString())
            scheduleInputEvent()
        }, INPUT_EVENT_INTERVAL)
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!isReady) {
            Log.w(TAG, "send(가짜): 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        Log.d(TAG, "writeCharacteristic(가짜): \"$command\"")
        // 펌웨어처럼 "\n"으로 나눈 명령마다 응답 한 줄씩 보낸다
        val lines = command.split("\n").filter { it.isNotBlank() }
        for (line in lines) {
            sendHandler.postDelayed({
                deliver(respond(line.trim()))
            }, RESPONSE_DELAY)
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }

    private fun deliver(json: String) {
        Log.d(TAG, "onCharacteristicChanged(가짜): $json")
        messageListener?.invoke(json)
    }

    // 펌웨어 parseCmd와 같은 규칙으로 응답 JSON을 만든다
    private fun respond(line: String): String {
        val tokens = line.split(Regex("\\s+")).filter { it.isNotEmpty() }
        val res = JSONObject()
        if (tokens.isEmpty()) {
            res.put("result", "fail")
            res.put("ms", "need command")
            return res.toString()
        }
        when (tokens[0]) {
            "on" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) on")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "off" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) off")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "pwm" -> {
                if (tokens.size > 2) {
                    val index = tokens[1].toIntOrNull() ?: 0
                    val value = tokens[2].toIntOrNull() ?: 0
                    if (index < 0) {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    } else if (index >= LED_COUNT) {
                        res.put("result", "err")
                        res.put("ms", "pwm pin index error")
                    } else if (value < 0 || value > 255) {
                        res.put("result", "err")
                        res.put("ms", "pwm value range 0~255")
                    } else {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    }
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index and pwm value")
                }
            }
            "dht11" -> {
                // 매번 조금씩 다른 값을 돌려줘서 이력 목록에서 구분되게 한다: 24.5/40.0 → 25.0/41.0 → 25.5/42.0 → 반복
                val step = dhtCount % 3
                dhtCount++
                val temperature = 24.5 + step * 0.5
                val humidity = 40.0 + step * 1.0
                res.put("result", "ok")
                res.put("value", String.format(java.util.Locale.US, "[%.1f,%.1f]", temperature, humidity))
            }
            "about" -> {
                res.put("result", "ok")
                res.put("os", "cronos-v1")
                res.put("app", "BLEuno")
                res.put("version", "1.0.5_dev")
                res.put("author", "gbox3d")
                res.put("chipid", 1234567890L)
            }
            "blink" -> {
                res.put("result", "ok")
                res.put("ms", "led blink")
            }
            "stopblk" -> {
                res.put("result", "ok")
                res.put("ms", "led stop blink")
            }
            else -> {
                res.put("result", "fail")
                res.put("ms", "unknown command")
            }
        }
        return res.toString()
    }
}
```

### RealBleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import android.annotation.SuppressLint
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.bluetooth.BluetoothStatusCodes
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID

// 실제 bleuno 보드와 BluetoothGatt로 이야기하는 클라이언트.
// 콜백 사슬: startScan → (timeoutMs 뒤) stopScan → connectGatt → onConnectionStateChange(CONNECTED)
//   → requestMtu(185) → onMtuChanged → discoverServices → onServicesDiscovered
//   → setCharacteristicNotification + CCCD 쓰기 → onDescriptorWrite → 준비됨
//   → writeCharacteristic → onCharacteristicWrite(다음 명령) / onCharacteristicChanged(응답)
// 모든 콜백은 Log.d("BLE", …)로 남기므로 Logcat에서 태그 BLE로 순서를 볼 수 있다.
// 권한 검사는 PermissionHelper.hasAll로 하고, 없으면 로그만 남기고 아무것도 하지 않는다(요청은 앱 책임).
@SuppressLint("MissingPermission")
class RealBleunoClient(
    context: Context,
    private val nameFilter: String = "ESP32_BLE",   // 이 문자열로 시작하는 이름의 기기만 onFound에 알린다
) : BleunoClient {

    companion object {
        const val TAG = "BLE"
        val SERVICE_UUID: UUID = UUID.fromString("c6f8b088-2af8-4388-8364-ca2a907bdeb8")
        val CHARACTERISTIC_UUID: UUID = UUID.fromString("f6aa83ca-de53-46b4-bdea-28a7cb57942e")
        val CCCD_UUID: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
        const val MTU = 185
    }

    private val appContext: Context = context.applicationContext
    private val bluetoothManager: BluetoothManager? =
        appContext.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager

    // 콜백은 바인더 스레드에서 오므로, 화면과 리스너에는 항상 이 Handler로 메인 스레드에서 전달한다
    private val mainHandler = Handler(Looper.getMainLooper())
    // 검색 시간 초과 전용 Handler (removeCallbacksAndMessages로 검색 것만 취소하기 위해 분리)
    private val scanHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    // ---- 검색 ----
    private var isScanning = false
    private var onFoundListener: ((BleunoDevice) -> Unit)? = null
    private var onFinishedListener: (() -> Unit)? = null
    private val foundAddresses = HashSet<String>()   // 같은 기기를 두 번 알리지 않기 위한 주소 집합

    // ---- 연결 ----
    private var gatt: BluetoothGatt? = null
    private var characteristic: BluetoothGattCharacteristic? = null
    private var userDisconnect = false               // disconnect()를 사용자가 불렀는지

    // ---- 전송 큐 ----
    private val queue = ArrayDeque<String>()         // 아직 보내지 않은 명령("\n" 포함)
    private var writing = false                      // onCharacteristicWrite를 기다리는 중이면 true

    private var messageListener: ((String) -> Unit)? = null

    // ---------------------------------------------------------------- 검색

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device ?: return
            val name = result.scanRecord?.deviceName ?: device.name ?: return
            if (!name.startsWith(nameFilter)) return
            val found = BleunoDevice(name, device.address, result.rssi)
            mainHandler.post {
                if (!isScanning) return@post
                if (!foundAddresses.add(found.address)) return@post   // 이미 알린 기기
                Log.d(TAG, "onScanResult: ${found.name} ${found.address} rssi=${found.rssi}")
                onFoundListener?.invoke(found)
            }
        }

        override fun onScanFailed(errorCode: Int) {
            Log.w(TAG, "onScanFailed: errorCode=$errorCode")
            mainHandler.post { stopScan() }
        }
    }

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "startScan: 권한이 없어 무시함 (${PermissionHelper.missing(appContext).joinToString()})")
            return
        }
        val scanner = bluetoothManager?.adapter?.bluetoothLeScanner
        if (scanner == null) {
            Log.w(TAG, "startScan: 블루투스가 꺼져 있거나 없음 → onFinished")
            onFinished()
            return
        }
        if (isScanning) stopScan()
        foundAddresses.clear()
        onFoundListener = onFound
        onFinishedListener = onFinished
        isScanning = true
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()
        scanner.startScan(null, settings, scanCallback)
        Log.d(TAG, "startScan: ${timeoutMs}ms 동안 \"$nameFilter\"로 시작하는 기기 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        bluetoothManager?.adapter?.bluetoothLeScanner?.stopScan(scanCallback)
        Log.d(TAG, "stopScan: 찾은 기기 ${foundAddresses.size}개")
        val finished = onFinishedListener
        onFoundListener = null
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    private val gattCallback = object : BluetoothGattCallback() {

        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            Log.d(TAG, "onConnectionStateChange: status=$status newState=$newState")
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.d(TAG, "STATE_CONNECTED → requestMtu($MTU)")
                mainHandler.post { _connectionState.value = ConnState.DISCOVERING }
                val requested = g.requestMtu(MTU)
                Log.d(TAG, "requestMtu($MTU) 호출 결과=$requested")
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.d(TAG, "STATE_DISCONNECTED → gatt.close()")
                g.close()
                mainHandler.post {
                    gatt = null
                    characteristic = null
                    queue.clear()
                    writing = false
                    _connectionState.value = if (userDisconnect) ConnState.DISCONNECTED else ConnState.LOST
                }
            }
        }

        override fun onMtuChanged(g: BluetoothGatt, mtu: Int, status: Int) {
            Log.d(TAG, "onMtuChanged: mtu=$mtu status=$status → discoverServices()")
            // MTU 변경이 실패해도 기본 MTU로 쓸 수 있으므로 서비스 탐색은 그대로 진행한다
            val started = g.discoverServices()
            Log.d(TAG, "discoverServices() 호출 결과=$started")
        }

        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            Log.d(TAG, "onServicesDiscovered: status=$status")
            val service = g.getService(SERVICE_UUID)
            val ch = service?.getCharacteristic(CHARACTERISTIC_UUID)
            if (ch == null) {
                Log.w(TAG, "서비스 또는 특성을 찾지 못함 → disconnect()")
                g.disconnect()
                return
            }
            Log.d(TAG, "characteristic 확보: ${ch.uuid}")
            mainHandler.post { characteristic = ch }
            g.setCharacteristicNotification(ch, true)
            val descriptor = ch.getDescriptor(CCCD_UUID)
            if (descriptor == null) {
                Log.w(TAG, "CCCD descriptor 없음 → disconnect()")
                g.disconnect()
                return
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                g.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE)
            } else {
                @Suppress("DEPRECATION")
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                @Suppress("DEPRECATION")
                g.writeDescriptor(descriptor)
            }
            Log.d(TAG, "writeDescriptor(CCCD, ENABLE_NOTIFICATION_VALUE)")
        }

        override fun onDescriptorWrite(g: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) {
            Log.d(TAG, "onDescriptorWrite: status=$status → 준비됨")
            mainHandler.post { _connectionState.value = ConnState.READY }
        }

        override fun onCharacteristicWrite(g: BluetoothGatt, ch: BluetoothGattCharacteristic, status: Int) {
            Log.d(TAG, "onCharacteristicWrite: status=$status")
            mainHandler.post {
                writing = false
                writeNext()
            }
        }

        // API 33 이상에서 불리는 응답 콜백
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic, value: ByteArray) {
            deliver(value)
        }

        // API 32 이하에서 불리는 응답 콜백
        @Deprecated("Deprecated in Java")
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic) {
            @Suppress("DEPRECATION")
            val value = ch.value ?: return
            deliver(value)
        }
    }

    // 받은 바이트를 UTF-8 문자열로 바꿔 메인 스레드에서 리스너에 전달한다
    private fun deliver(bytes: ByteArray) {
        val text = String(bytes, Charsets.UTF_8)
        Log.d(TAG, "onCharacteristicChanged: $text")
        mainHandler.post { messageListener?.invoke(text) }
    }

    override fun connect(address: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "connect: 권한이 없어 무시함")
            return
        }
        val adapter = bluetoothManager?.adapter
        if (adapter == null) {
            Log.w(TAG, "connect: 블루투스 어댑터 없음")
            return
        }
        val device = try {
            adapter.getRemoteDevice(address)
        } catch (e: IllegalArgumentException) {
            Log.w(TAG, "connect: 잘못된 주소 $address")
            return
        }
        // 이전 연결이 남아 있으면 정리하고 새로 시작한다
        gatt?.close()
        gatt = null
        characteristic = null
        queue.clear()
        writing = false
        userDisconnect = false

        _connectionState.value = ConnState.CONNECTING
        Log.d(TAG, "connectGatt($address, autoConnect=false)")
        val created = device.connectGatt(appContext, false, gattCallback)
        if (created == null) {
            Log.w(TAG, "connectGatt 실패 (블루투스 꺼짐?)")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        gatt = created
    }

    override fun disconnect() {
        userDisconnect = true
        val g = gatt
        if (g == null) {
            Log.d(TAG, "disconnect: 연결 없음 → 연결 안 됨")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        Log.d(TAG, "gatt.disconnect()")
        g.disconnect()   // 결과는 onConnectionStateChange(STATE_DISCONNECTED)에서 처리
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "send: 권한이 없어 무시함")
            return
        }
        if (!isReady) {
            Log.w(TAG, "send: 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        queue.addLast(command + "\n")
        Log.d(TAG, "send: 큐에 추가 \"$command\" (대기 ${queue.size}개)")
        if (!writing) writeNext()
    }

    // 큐의 맨 앞 명령 하나를 보낸다. 다음 것은 onCharacteristicWrite가 온 뒤에 보낸다.
    private fun writeNext() {
        val g = gatt ?: return
        val ch = characteristic ?: return
        val text = queue.removeFirstOrNull() ?: return
        val bytes = text.toByteArray(Charsets.UTF_8)
        writing = true
        val ok = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val code = g.writeCharacteristic(ch, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
            code == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION")
            ch.value = bytes
            @Suppress("DEPRECATION")
            g.writeCharacteristic(ch)
        }
        Log.d(TAG, "writeCharacteristic(\"${text.trim()}\") 호출 결과=$ok")
        if (!ok) {
            // 호출 자체가 실패하면 onCharacteristicWrite가 오지 않으므로 바로 다음 것을 시도한다
            writing = false
            writeNext()
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }
}
```
