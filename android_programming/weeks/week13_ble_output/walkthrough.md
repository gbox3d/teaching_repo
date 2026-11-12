# 13주차 따라하기 — 보드에 명령 보내고 응답 받기

12주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
12주차 프로젝트가 없거나 실행되지 않으면 강의자에게 12주차 완성본(`week12_ble_gatt/examples/day2`)을 받아 시작한다.

이번 주에 고치는 파일은 제어 화면 쪽뿐이다. `ControlActivity.kt`·`activity_control.xml`·`strings.xml` 셋이다. 코드를 넣는 것은 1일차뿐이고, 2일차는 과제 계획안 발표다.
`MainActivity.kt`, `activity_main.xml`, `AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml`, `bleuno` 패키지 9개는 12주차 그대로 둔다. 전체 내용은 [부록 A](#부록-a--바꾸지-않는-파일-전체)와 [부록 B](#부록-b--제공-bleuno-파일-전체)에 있다.

에뮬레이터는 12주차와 같은 API 33 이상 이미지를 쓴다. 보드 없이 가짜 클라이언트(Fake)로 끝까지 할 수 있고, 실보드는 실기기에서만 연결된다.
제어 화면에는 **목록 줄 탭 → `준비됨` → [제어 화면]**으로 들어간다. [연결]은 4주차에 만든 "이름만 들고 이동" 버튼이라 연결을 시작하지 않는다. 연결(`준비됨`)이 안 된 채로 제어 화면에 들어오면(목록 줄을 누르지 않았거나 [해제]한 뒤 [연결]로 들어옴) 상태가 `연결 안 됨`이라 명령이 버려진다.

## 1일차

### 1. 12주차 프로젝트 열고 제어 화면까지 들어가기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. Logcat 창의 필터에 `package:mine tag:BLE`를 넣어 둔다.
3. [검색]을 누르고 목록에 `ESP32_BLE_FAKE1 (00:11:22:33:44:01)`이 들어오면 그 줄을 누른다. 상태가 `연결 중` → `서비스 확인 중` → `준비됨`이 되면 [제어 화면]을 누른다.
4. 제어 화면에 아래가 보이면 시작할 수 있다.

```text
장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[핀 번호      ]
LED (○)
명령 로그

[뒤로]
```

5. 입력 칸에 `3`을 넣고 LED Switch를 켠다. 로그에 `on 3`이 쌓이지만 Logcat `tag:BLE`에는 새 줄이 없다. 4주차부터 로그에 **적기만** 했고 보드에는 아무것도 보내지 않았기 때문이다. 오늘 이 줄이 보드에 가게 만든다.
6. `준비됨`인 채로 10초쯤 기다린다. Logcat에 `onCharacteristicChanged(가짜): {"event":"input","index":0,"value":1}` 같은 줄이 10초마다 찍힌다. 가짜 보드가 14주차용 입력 이벤트를 흉내 내는 줄이다. 오늘은 앱에서 이 줄을 걸러 낸다.

지금 내 `ControlActivity.kt`는 [12주차 완성본](../week12_ble_gatt/examples/day2/ControlActivity.kt)과 같아야 한다. 많이 다르면 그 파일로 바꾸고 시작한다.

### 2. 입력 칸 문구와 [전체 끄기] 자리 만들기

1. `app › res › values › strings.xml`을 연다. `pin_hint` 줄의 **값**만 `핀 번호`에서 `LED 번호 (0~3)`으로 바꾼다. 이름 `pin_hint`는 그대로 둔다.

```xml
    <string name="pin_hint">LED 번호 (0~3)</string>
```

2. `state_unknown` 줄 아래(마지막 `</resources>` 바로 위)에 한 줄을 넣는다.

```xml
    <string name="all_off">전체 끄기</string>
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
</resources>
```

3. `app › res › layout › activity_control.xml`을 연다. `pinEdit` 블록의 마지막 줄 `android:inputType="number" />`에서 끝의 ` />`를 떼고, 아래 줄에 `maxLength`를 붙여 블록을 닫는다.

```xml
        android:inputType="number"
        android:maxLength="2" />
```

4. `ledSwitch` 블록을 닫는 `/>` **아래**, `명령 로그` 제목 `TextView` **위**에 한 줄을 비우고 버튼을 넣는다.

```xml
    <Button
        android:id="@+id/allOffButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/all_off" />
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
        android:text="@string/led" />

    <Button
        android:id="@+id/allOffButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/all_off" />

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

    <Button
        android:id="@+id/backButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="24dp"
        android:text="@string/back" />

</LinearLayout>
```

5. 실행하고 [제어 화면]까지 들어간다. 입력 칸 힌트가 `LED 번호 (0~3)`이고 LED Switch 아래에 [전체 끄기]가 보이면 성공이다. 입력 칸에 `123`을 쳐 보면 `12`까지만 들어간다. [전체 끄기]는 아직 눌러도 아무 일이 없다.

- `android:maxLength="2"`: 입력 칸에 두 글자까지만 들어간다. `inputType="number"`는 자릿수를 막지 않아서 아주 긴 숫자를 넣으면 `toInt()`가 숫자로 바꾸지 못하고 앱이 멈춘다. 두 글자로 막아 `0`~`99`만 들어오게 한다.
- `inputType="number"`는 `-`를 적을 수 없다. "전체"를 뜻하는 `-1`은 [전체 끄기]가 보낸다.
- id `pinEdit`와 문자열 이름 `pin_hint`는 4주차 이름 그대로 둔다. 뜻만 이제 **LED 번호**다. Kotlin의 `binding.pinEdit`도 그대로 쓴다.

### 3. Switch를 켜고 끄면 명령 보내기

`ControlActivity.kt`를 열고 `// 2.` LED Switch 리스너에서 세 곳을 바꾼다.

1. 빈 칸일 때 Toast 글자 `핀 번호를 입력하세요`를 `LED 번호를 입력하세요`로 바꾼다.
2. `} else if (isChecked) {` 가지 안의 `binding.logText.append("on $pin\n")` **한 줄**을 `// 5.` 주석과 세 줄로 바꾼다.
3. `} else {` 가지 안의 `binding.logText.append("off $pin\n")` **한 줄**을 `// 6.` 주석과 세 줄로 바꾼다.
4. `// 2.` 주석 아래에 `13주차 1일차:` 설명 줄을 붙인다(주석이 없어도 동작은 같다).

바꾼 리스너 전체는 아래와 같다.

```kotlin
        // 2. LED Switch: 켜면 on, 끄면 off 명령을 로그에 쌓는다.
        //    13주차 1일차: 입력 칸은 이제 핀 번호가 아니라 LED 번호(0~3)다. 로그에 쌓기 전에 보드에도 명령을 보낸다(5·6번).
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
            }
        }
```

`Bleuno`는 12주차 2일차 `// 4.` 상태 표시에서 이미 import했다. 빨간색이면 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 `com.example.smartio.bleuno.Bleuno`를 가져온다.

5. 실행하고 [제어 화면]에 들어가 `3` → Switch 켜기를 한다. 앱 로그에는 `on 3`이 쌓이고, Logcat `tag:BLE`에는 두 줄이 새로 찍힌다.

```text
writeCharacteristic(가짜): "on 3"
onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) on"}
```

   가짜 보드가 약 0.3초 뒤 JSON 한 줄로 대답했다. 그런데 앱 로그에는 응답 줄이 없다. 대답을 받는 코드가 아직 없기 때문이다(4단계).
6. Switch를 끈다. 앱 로그 `off 3`, Logcat `writeCharacteristic(가짜): "off 3"` 다음에 `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) off"}`.

- `val index = pin.toInt()`: 4주차에 배운 글자 → 숫자 바꾸기다. 빈 칸 검사(`pin.isEmpty()`)를 통과한 가지 안에서만 부른다. 빈 글자를 `toInt()`하면 앱이 멈춘다.
- `"on $index"`: bleuno 명령 규약이다. **명령 이름, 띄어쓰기 한 칸, LED 번호.** 끝의 `\n`은 `send`가 붙인다. 로그에 쌓는 글자와 보내는 글자가 같다.
- `Bleuno.client?.send(…)`: 12주차에 연결 화면이 만든 client와 **같은 객체**를 `Bleuno.client`로 꺼냈다. `null`일 수 있어 3주차 `?.`로 부르고, `null`이면 아무것도 보내지 않는다.
- `send`는 명령을 큐에 넣고 차례대로 보낸다. 쓰기가 끝났다는 콜백이 와야 다음 명령이 나간다(실보드 로그는 6단계).
- 이번 주 코드에는 번호 검사가 없어 `9`도 그대로 나간다. `9` 같은 번호는 **Fake에서만** 해 본다. 보드는 번호를 검사하지 않아 실보드에서는 어떻게 될지 알 수 없다(14주차 1일차에 앱이 막는다).

### 4. 응답 받기: onStart에서 등록, onStop에서 해제

1. `onCreate()`를 닫는 `}`(`// 4.` collect 블록 바로 아래 줄) **아래**, 클래스를 닫는 마지막 `}` **위**에 한 줄을 비우고 두 함수를 넣는다. onCreate **안**이 아니다.

```kotlin
    // 8. 화면이 보이기 시작하면 보드가 보내는 응답(JSON 한 줄)을 받도록 등록한다(13주차 1일차).
    //    명령 하나마다 응답이 한 줄씩 온다. { json -> }는 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다.
    override fun onStart() {
        super.onStart()
        Bleuno.client?.onMessage { json ->
            // 9. JSON에서 "result"(ok·err·fail) 값을 꺼내 보고, 명령의 응답이면 받은 JSON 한 줄을 그대로 로그에 남긴다(13주차 1일차).
            //    로그 예: 응답: {"result":"ok","ms":"led(s) on"}. result가 없는 줄은 명령의 응답이 아니다(가짜 보드가 10초마다 보내는 입력 이벤트, 14주차에 다룬다). 로그에 넣지 않는다.
            val result = BleunoMessage.result(json)
            if (result != null) {
                binding.logText.append("응답: $json\n")
            }
        }
    }

    // 10. 화면이 안 보이게 되면 응답 받기를 푼다(null). onStart의 등록과 반드시 짝을 맞춘다(13주차 1일차).
    //     10주차 배터리 Receiver의 등록·해제와 같은 규칙이다. 풀지 않으면 보이지 않는 화면의 로그를 계속 고치려 한다.
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
    }
```

2. 빨간 글자를 Alt+Enter → Import로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `BleunoMessage` | `com.example.smartio.bleuno.BleunoMessage` |

3. 실행하고 [제어 화면]에 들어가 `3` → Switch 켜기를 한다. 로그에 `on 3`, 약 0.3초 뒤 `응답: {"result":"ok","ms":"led(s) on"}`이 쌓이면 성공이다. 로그 칸 폭(240dp) 때문에 JSON 줄은 두 줄로 접혀 보일 수 있다. 글자는 같다.
4. Switch를 끈다. `off 3` 다음에 `응답: {"result":"ok","ms":"led(s) off"}`.
5. `준비됨`인 채로 15초쯤 기다린다. Logcat에는 `{"event":"input",…}` 줄이 찍히지만 앱 로그에는 새 줄이 생기지 않는다.

- `override fun onStart()`·`onStop()`: 3주차 생명주기 콜백을 두는 자리(onCreate 괄호 밖, 클래스 안)다. onCreate 안에 붙여 넣으면 `Modifier 'override' is not applicable to 'local function'.` 오류가 난다.
- `Bleuno.client?.onMessage { json -> }`: 보드가 JSON 한 줄을 보낼 때마다 중괄호 안이 실행되고 그 글자가 `json`으로 넘어온다. 12주차 `{ device -> }`와 같은 "넘어오는 값에 이름 붙이기"다.
- 라이브러리가 이 중괄호를 **메인 스레드**에서 불러 주므로 5주차 `runOnUiThread` 없이 `binding.logText`를 바로 바꾼다.
- `BleunoMessage.result(json)`: JSON에서 `"result"` 값(`ok`·`err`·`fail`)을 꺼낸다. 키가 없으면 `null`이다(`String?`). 가짜 보드의 입력 이벤트 줄에는 `result`가 없어서 `if (result != null)`에서 걸러진다.
- `"응답: $json\n"`: 4주차 문자열 템플릿으로 받은 줄을 그대로 붙였다.
- 10주차 배터리 Receiver처럼 **`onStart`에서 등록하면 `onStop`에서 푼다.** `onMessage(null)`이 푸는 것이다.

### 5. [전체 끄기] 버튼과 홈에 갔다 오기

1. `onCreate()` 안, `// 4.` collect 블록을 닫는 `}` **아래**(onCreate를 닫는 `}` 바로 위)에 한 줄을 비우고 넣는다.

```kotlin
        // 7. [전체 끄기] 버튼: 번호 자리에 -1을 보내면 보드의 LED가 모두 꺼진다(13주차 1일차).
        binding.allOffButton.setOnClickListener {
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
        }
```

2. 실행하고 `3` → Switch 켜기 → [전체 끄기]를 누른다. 로그에 `off -1` 다음 `응답: {"result":"ok","ms":"led(s) off"}`, Logcat에 `writeCharacteristic(가짜): "off -1"`. LED Switch는 켜진 모양 그대로다. [전체 끄기]는 보드에 명령만 보내고 Switch를 건드리지 않는다.
3. 홈 버튼을 눌렀다가 앱으로 돌아와 Switch를 끈다. `off 3` 다음에 응답 줄이 찍히면 된다. 홈으로 나갈 때 `onStop`이 받기를 풀고, 돌아올 때 `onStart`가 다시 등록했다.

- 번호 자리의 `-1`은 bleuno 규약에서 "모든 LED"다. 입력 칸으로는 `-`를 적을 수 없어서 버튼으로 보낸다.
- 리스너이므로 onCreate 안 어디에 두어도 동작은 같다. 예제는 `// 4.` 아래에 두었다.

완성한 `ControlActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/ControlActivity.kt](examples/day1/ControlActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.bleuno.Bleuno
import com.example.smartio.bleuno.BleunoMessage
import com.example.smartio.databinding.ActivityControlBinding
import kotlinx.coroutines.launch

class ControlActivity : AppCompatActivity() {
    // ViewBinding 틀: activity_control.xml → ActivityControlBinding
    private lateinit var binding: ActivityControlBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityControlBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. 연결 화면이 보낸 장치 이름을 꺼내 상단에 보여 준다.
        val name = intent.getStringExtra("name") ?: ""
        binding.deviceText.text = "장치: $name"

        // 2. LED Switch: 켜면 on, 끄면 off 명령을 로그에 쌓는다.
        //    13주차 1일차: 입력 칸은 이제 핀 번호가 아니라 LED 번호(0~3)다. 로그에 쌓기 전에 보드에도 명령을 보낸다(5·6번).
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
            }
        }

        // 3. [뒤로] 버튼: 이 화면을 닫고 연결 화면으로 돌아간다.
        binding.backButton.setOnClickListener {
            finish()
        }

        // 4. 연결 화면이 만든 클라이언트를 Bleuno.client로 꺼내 연결 상태를 상단에 보여 준다(12주차 2일차).
        //    MainActivity 7번과 같은 collect 틀이다. client가 없으면(null) ?.에서 멈추고 "상태: ?"가 그대로 남는다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                }
            }
        }

        // 7. [전체 끄기] 버튼: 번호 자리에 -1을 보내면 보드의 LED가 모두 꺼진다(13주차 1일차).
        binding.allOffButton.setOnClickListener {
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
        }
    }

    // 8. 화면이 보이기 시작하면 보드가 보내는 응답(JSON 한 줄)을 받도록 등록한다(13주차 1일차).
    //    명령 하나마다 응답이 한 줄씩 온다. { json -> }는 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다.
    override fun onStart() {
        super.onStart()
        Bleuno.client?.onMessage { json ->
            // 9. JSON에서 "result"(ok·err·fail) 값을 꺼내 보고, 명령의 응답이면 받은 JSON 한 줄을 그대로 로그에 남긴다(13주차 1일차).
            //    로그 예: 응답: {"result":"ok","ms":"led(s) on"}. result가 없는 줄은 명령의 응답이 아니다(가짜 보드가 10초마다 보내는 입력 이벤트, 14주차에 다룬다). 로그에 넣지 않는다.
            val result = BleunoMessage.result(json)
            if (result != null) {
                binding.logText.append("응답: $json\n")
            }
        }
    }

    // 10. 화면이 안 보이게 되면 응답 받기를 푼다(null). onStart의 등록과 반드시 짝을 맞춘다(13주차 1일차).
    //     10주차 배터리 Receiver의 등록·해제와 같은 규칙이다. 풀지 않으면 보이지 않는 화면의 로그를 계속 고치려 한다.
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다. 주석 번호가 없어도 괜찮다.

### 6. 캡처 1과 실제 보드

1. [뒤로]를 누르고 [제어 화면]으로 다시 들어온다. 새 화면이라 로그가 비어 있다. `3` → Switch 켜기 → 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 보이는 **세로 화면을 캡처한다.** 이 화면이 제출 캡처 1이다.

- 로그 칸(`logText`)에는 스크롤이 없다. 명령 하나에 `on 3` 한 줄과 접힌 JSON 줄이 쌓여, 몇 번 보내면 새 줄이 칸 아래로 밀려 안 보인다. 캡처는 **들어온 직후 첫 조작**에서 찍는다. 넘치면 [뒤로] → [제어 화면]으로 다시 들어온다.
- 화면을 돌리면 Switch 켜짐 상태가 되살아나며 리스너가 한 번 더 불려 `on 3`이 다시 나간다(3주차 회전). 폰 크기 가로 화면에서는 로그 칸이 안 보여, 이때 다시 나간 명령과 응답은 Logcat `tag:BLE`에서만 보인다. 세로로 되돌릴 때 한 번 더 나가고, 그때 비워진 로그에 `on 3`과 응답이 찍힌다. 캡처는 돌리지 않은 세로 화면에서 찍는다.

2. 보드와 실기기가 있으면 실제 보드로 해 본다.
   1. 보드 LED가 파랑 깜빡임인지 본다.
   2. `MainActivity.kt`의 `private val useFake = true`를 `false`로 바꾸고, 기기 목록에서 실기기를 골라 `Run ▶`.
   3. [검색] → `ESP32_BLE…` 줄 누르기 → `준비됨`(보드 LED가 모두 꺼짐) → [제어 화면] → `3` → Switch 켜기.
   4. 번호 3 LED(GPIO0)가 켜지면 성공이다. **이 보드를 사진으로 찍는다.** Logcat `tag:BLE`에는 아래 순서가 찍힌다.

```text
send: 큐에 추가 "on 3" (대기 1개)
writeCharacteristic("on 3") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}
```

- Switch를 빠르게 켰다 껐다 하면 `대기 2개`처럼 큐에 쌓였다가 `onCharacteristicWrite`가 올 때마다 하나씩 나간다. 특강에서 본 "쓰기가 끝나야 다음 쓰기"를 라이브러리가 대신 지킨다.
- 실보드에서는 `0`~`3`만 넣는다.
- 에뮬레이터로 돌아갈 때는 `useFake = true`로 되돌린다.

### 7. 바꾸지 않는 파일 확인하기

아래 파일은 12주차 2일차에 만든 그대로이며 이번 주에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.

- `MainActivity.kt`, `activity_main.xml`, `AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml` — [부록 A](#부록-a--바꾸지-않는-파일-전체), [examples/day1](examples/day1)
- `bleuno` 패키지 9개 — [부록 B](#부록-b--제공-bleuno-파일-전체), [bleuno/src](../../bleuno/src)

`AndroidManifest.xml`에 더할 권한은 없다. 명령 보내기(write)와 응답 받기(notify)는 10주차에 넣은 `BLUETOOTH_CONNECT`(Android 12 이상) 권한 안에 들어 있다.

## 제출하기

1. 6단계까지 한 코드로 한 번 더 실행해 `3` → Switch 켜기가 `응답: {"result":"ok","ms":"led(s) on"}`으로 끝나는지 본다.
2. 제출물은 네 가지다.
   1. `ControlActivity.kt`
   2. `activity_control.xml`
   3. 캡처 1: 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 보이는 세로 제어 화면(6단계)
   4. 사진: 번호 3 LED가 켜진 보드(6단계, 보드가 없으면 생략)

- 로그가 넘쳐 응답 줄이 잘렸으면 [뒤로] → [제어 화면]으로 다시 들어와 첫 조작에서 다시 찍는다.
- 캡처와 사진에 계정 이름·알림 내용이 보이지 않게 한다.
- 2일차에는 코드를 더 넣지 않는다. 지금까지 만든 앱으로 과제 계획안을 발표한다([과제 안내](project_brief.md) · [채점표](rubric.md)).

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
명령이 안 먹으면 Logcat `tag:BLE`에서 `writeCharacteristic` 줄(보낸 글자)과 `onCharacteristicChanged` 줄(받은 대답)을 차례로 본다. 보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다.

## 부록 A — 바꾸지 않는 파일 전체

아래 파일은 12주차 `week12_ble_gatt/examples/day2`와 글자 단위로 같다. 이번 주에는 바꾸지 않는다. 같은 코드가 [examples/day1](examples/day1)에 있다.

`MainActivity.kt` — [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)(405행). 12주차 [따라하기](../week12_ble_gatt/walkthrough.md)에서 완성한 연결 화면 그대로라 여기에는 다시 싣지 않는다. 실보드로 바꿀 때 고치는 88행 `private val useFake = true` 한 줄 말고는 손대지 않는다. 내 파일과 비교할 때는 예제 파일을 연다.

`activity_main.xml` — [examples/day1/activity_main.xml](examples/day1/activity_main.xml)

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). 내 파일에는 아이콘 등의 줄이 더 있다. BLE 권한이 있는지만 본다.

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

`res/values/themes.xml` — [examples/day1/res/values/themes.xml](examples/day1/res/values/themes.xml). 프로젝트를 만들 때 생긴 그대로다. 내 것을 그대로 둔다.

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

12주차에 붙여 넣은 9개 파일이다. 모두 `app › kotlin+java › com.example.smartio › bleuno`에 있고 고치지 않는다.
같은 파일이 [bleuno/src](../../bleuno/src)와 [examples/day1/bleuno](examples/day1/bleuno)에 있다. 이번 주에 쓰는 `send`·`onMessage`는 `BleunoClient.kt`, `result`·`message`는 `BleunoMessage.kt`에 있다.

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

    // PC에서 돌리는 시뮬레이터(android_programming/iot_sim)에 Wi-Fi(TCP)로 연결하는 클라이언트를 만든다.
    // 보드와 블루투스 없이 같은 명령·응답으로 연습한다. 만든 객체는 client에 보관한 뒤 그대로 돌려준다.
    fun createTcp(): BleunoClient {
        val created: BleunoClient = TcpBleunoClient()
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
            onFinished()
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

### TcpBleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONObject
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.IOException
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.net.SocketTimeoutException
import java.util.concurrent.Executors

// PC에서 돌리는 시뮬레이터(android_programming/iot_sim)와 Wi-Fi(TCP)로 이야기하는 클라이언트.
// 보드와 블루투스 없이 RealBleunoClient와 같은 명령·같은 JSON으로 연습한다. 앱 코드는 그대로다.
//   검색: UDP로 "bleuno?"를 뿌리고, 답한 시뮬레이터마다 onFound(이름, "ip:포트"), timeoutMs 뒤 onFinished
//   연결: connect("10.0.2.2:8266") → 연결 중 → 서비스 확인 중 → (첫 줄 hello를 받으면) 준비됨
//         3초 안에 연결되지 않거나, 연결된 뒤 3초 안에 첫 줄이 오지 않으면 "끊김"
//         (연결 3초는 IP 주소 기준이다. 이름을 넣으면 이름을 IP로 바꾸는 시간은 이 3초에 들지 않는다)
//   전송: send → 한 줄 쓰기 → 응답 JSON 한 줄이 onMessage로
//   끊김: 시뮬레이터를 끄거나 화면의 [연결 끊기]를 누르면 "끊김"
// 소켓 일은 Thread에서 하고, 상태 변경과 리스너 호출은 모두 메인 스레드 Handler로 전달한다.
// 모든 단계는 Log.d("TCP", …)로 남기므로 Logcat에서 태그 TCP로 순서를 볼 수 있다.
class TcpBleunoClient : BleunoClient {

    companion object {
        const val TAG = "TCP"
        const val DEFAULT_PORT = 8266              // 명령·응답 TCP 포트 (주소에 포트가 없으면 이 값)
        const val DISCOVERY_PORT = 8267            // 검색용 UDP 포트
        const val DISCOVERY_QUERY = "bleuno?"      // 검색할 때 보내는 글자
        const val EMULATOR_HOST = "10.0.2.2"       // 에뮬레이터에서 보는 PC 주소
        const val CONNECT_TIMEOUT = 3000           // connect 기다리는 시간(ms)
        const val HELLO_TIMEOUT = 3000             // 연결된 뒤 첫 줄(hello)을 기다리는 시간(ms)
        const val RECEIVE_TIMEOUT = 500            // UDP 응답을 한 번에 기다리는 시간(ms)
    }

    // 소켓 스레드에서 온 결과는 항상 이 Handler로 메인 스레드에서 처리한다
    private val mainHandler = Handler(Looper.getMainLooper())
    // 검색 시간 초과 전용 Handler (removeCallbacksAndMessages로 검색 예약만 취소하려고 따로 둔다)
    private val scanHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    // ---- 검색 ----
    @Volatile private var isScanning = false
    @Volatile private var scanSocket: DatagramSocket? = null
    @Volatile private var scanId = 0                 // 검색 회차. startScan·stopScan마다 1 늘린다. 회차가 다른 검색 스레드는 곧 끝난다
    private var onFoundListener: ((BleunoDevice) -> Unit)? = null
    private var onFinishedListener: (() -> Unit)? = null
    private val foundAddresses = HashSet<String>()   // 같은 시뮬레이터를 두 번 알리지 않기 위한 주소 집합

    // ---- 연결 ----
    @Volatile private var socket: Socket? = null     // 지금 회차의 소켓. 메인 스레드에서만 넣고 뺀다
    @Volatile private var writer: BufferedWriter? = null
    @Volatile private var connectId = 0              // 연결 회차. connect()·disconnect()·끊김 처리마다 1 늘린다. 회차가 다른 스레드의 결과는 버린다

    // ---- 전송 ----
    // 명령을 순서대로 하나씩 쓴다. 이 클라이언트는 앱 전체에 하나만 쓴다(Bleuno.client). 그래서 따로 닫지 않는다.
    private val sendExecutor = Executors.newSingleThreadExecutor()

    private var messageListener: ((String) -> Unit)? = null

    // ---------------------------------------------------------------- 검색

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (isScanning) stopScan()
        foundAddresses.clear()
        onFoundListener = onFound
        onFinishedListener = onFinished
        val id = ++scanId
        isScanning = true
        Log.d(TAG, "startScan: ${timeoutMs}ms 동안 UDP $DISCOVERY_PORT 로 \"$DISCOVERY_QUERY\" 검색")
        Thread {
            runDiscovery(id)
        }.start()
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    // 지금 회차의 검색인지 본다. stopScan()이나 새 startScan()이 불렸으면 false다.
    private fun isCurrentScan(id: Int): Boolean {
        return isScanning && id == scanId
    }

    // 검색 스레드. "bleuno?"를 두 곳에 보내고, 멈출 때까지 응답을 받는다.
    private fun runDiscovery(id: Int) {
        var udp: DatagramSocket? = null
        try {
            udp = DatagramSocket()
            udp.broadcast = true
            udp.soTimeout = RECEIVE_TIMEOUT
            scanSocket = udp
            // 소켓을 넣기 전에 stopScan()이 불렸으면 stopScan()은 닫을 소켓이 없었다. 회차를 보고 여기서 끝낸다.
            if (!isCurrentScan(id)) return
            val query = DISCOVERY_QUERY.toByteArray(Charsets.UTF_8)
            // 같은 Wi-Fi의 PC(실기기)와 에뮬레이터를 띄운 PC, 두 곳에 보낸다
            for (host in listOf("255.255.255.255", EMULATOR_HOST)) {
                try {
                    udp.send(DatagramPacket(query, query.size, InetAddress.getByName(host), DISCOVERY_PORT))
                    Log.d(TAG, "UDP 보냄: $host:$DISCOVERY_PORT \"$DISCOVERY_QUERY\"")
                } catch (e: IOException) {
                    Log.w(TAG, "UDP 보내기 실패 ($host): $e")
                }
            }
            val buffer = ByteArray(512)
            while (isCurrentScan(id)) {
                val packet = DatagramPacket(buffer, buffer.size)
                try {
                    udp.receive(packet)
                } catch (e: SocketTimeoutException) {
                    continue   // 500ms 동안 응답이 없었다. 멈출지 확인하고 다시 기다린다
                }
                val text = String(packet.data, packet.offset, packet.length, Charsets.UTF_8)
                val ip = packet.address.hostAddress ?: continue
                Log.d(TAG, "UDP 받음: $ip $text")
                val json = try {
                    JSONObject(text)
                } catch (e: Exception) {
                    Log.w(TAG, "UDP 응답이 JSON이 아님: $text")
                    continue
                }
                val name = json.optString("name", "")
                if (name.isEmpty()) continue
                val port = json.optInt("port", DEFAULT_PORT)
                val found = BleunoDevice(name, "$ip:$port", 0)
                mainHandler.post {
                    if (!isCurrentScan(id)) return@post
                    if (!foundAddresses.add(found.address)) return@post   // 이미 알린 시뮬레이터
                    Log.d(TAG, "onFound: ${found.name} ${found.address}")
                    onFoundListener?.invoke(found)
                }
            }
        } catch (e: IOException) {
            // stopScan()이 소켓을 닫으면 receive가 여기로 풀린다. 검색 중이었다면 끝낸다.
            scanFailed(id, e)
        } catch (e: SecurityException) {
            // INTERNET 권한이 없으면 여기로 온다. 앱을 끝내지 않고 검색만 끝낸다.
            scanFailed(id, e)
        } finally {
            udp?.close()
            if (scanSocket === udp) scanSocket = null
        }
    }

    // 검색 스레드에서 오류가 났다. 지금 회차의 검색이면 메인 스레드에서 검색을 끝낸다.
    private fun scanFailed(id: Int, e: Exception) {
        if (isCurrentScan(id)) {
            Log.w(TAG, "UDP 검색 중 오류: $e")
            mainHandler.post { if (id == scanId) stopScan() }
        }
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanId++              // 회차를 올린다. 검색 스레드는 회차가 바뀐 것을 보고 곧 끝난다
        scanHandler.removeCallbacksAndMessages(null)
        scanSocket?.close()   // 검색 스레드의 receive를 풀어 준다
        Log.d(TAG, "stopScan: 찾은 시뮬레이터 ${foundAddresses.size}개")
        val finished = onFinishedListener
        onFoundListener = null
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    override fun connect(address: String) {
        // 새 회차로 시작하고, 이전 연결이 남아 있으면 정리한다.
        // disconnect()처럼 회차를 먼저 올린다. 그래야 소켓이 닫혀 풀린 지난 연결 스레드가 회차가 바뀐 것을 보고 Log.d만 남긴다.
        val id = ++connectId
        closeSocket()

        // "host:port". 포트가 없으면 8266
        val host = address.substringBefore(":").trim()
        val portText = address.substringAfter(":", "").trim()
        val port = if (portText.isEmpty()) DEFAULT_PORT else (portText.toIntOrNull() ?: -1)
        if (host.isEmpty() || port !in 1..65535) {
            // ":" 앞에 IP가 있어야 하고, 포트는 1~65535 숫자여야 한다. 잘못된 주소로는 연결하지 않고, 다른 실패와 같이 연결 중 → 끊김 순서로 둔다.
            // IP가 빈 채(예: ":8266")로 연결하면 PC가 아니라 이 기기 자신(localhost)에 붙으려 한다. 그래서 여기서 막는다.
            // StateFlow는 같은 값을 두 번 내보내지 않는다. 연결 중을 거쳐야 이미 끊김일 때도 화면이 끊김을 다시 받는다.
            if (host.isEmpty()) {
                Log.w(TAG, "connect: IP가 없음 (\"$address\") → 끊김")
            } else {
                Log.w(TAG, "connect: 포트가 잘못됨 (\"$address\") → 끊김")
            }
            _connectionState.value = ConnState.CONNECTING
            endConnection(id)
            return
        }

        // 소켓은 여기(메인 스레드)서 만들어 보관한 뒤 연결 스레드에 넘긴다.
        // Socket()은 만들기만 하고 네트워크는 쓰지 않는다. 보관해 두었으므로 disconnect()가 언제든 닫을 수 있다.
        val s = Socket()
        socket = s
        _connectionState.value = ConnState.CONNECTING
        Log.d(TAG, "connect: $host:$port (${CONNECT_TIMEOUT}ms 안에 연결)")
        Thread {
            runConnection(id, s, host, port)
        }.start()
    }

    // 연결 스레드. 연결 → 첫 줄(hello) → 준비됨 → 이후 줄마다 onMessage. 끊어지면 끊김.
    private fun runConnection(id: Int, s: Socket, host: String, port: Int) {
        try {
            s.connect(InetSocketAddress(host, port), CONNECT_TIMEOUT)
            Log.d(TAG, "connected: $host:$port → 서비스 확인 중")

            val reader = BufferedReader(InputStreamReader(s.getInputStream(), Charsets.UTF_8))
            val w = BufferedWriter(OutputStreamWriter(s.getOutputStream(), Charsets.UTF_8))
            // writer는 회차가 같을 때만 넣는다. 메인 스레드에서 확인하므로 그사이 disconnect()가 불려도 섞이지 않는다.
            mainHandler.post {
                if (id == connectId) {
                    writer = w
                    _connectionState.value = ConnState.DISCOVERING
                }
            }

            // 첫 줄(hello)은 3초만 기다린다. 다른 포트(예: 화면 주소 :8080)에 붙으면 첫 줄이 오지 않는다.
            s.soTimeout = HELLO_TIMEOUT
            val first = try {
                reader.readLine()
            } catch (e: SocketTimeoutException) {
                Log.w(TAG, "hello 없음: ${HELLO_TIMEOUT}ms 안에 첫 줄이 오지 않았다. 포트가 $DEFAULT_PORT 인지 확인한다 → 끊김")
                endConnection(id)
                return
            }
            if (first == null) {
                Log.d(TAG, "EOF: 첫 줄을 받기 전에 상대가 연결을 닫음")
                endConnection(id)
                return
            }
            // 첫 줄을 받았다. 이제부터는 시간 제한 없이 기다린다.
            // keepAlive는 상대가 소리 없이 사라졌을 때(PC가 잠들거나 Wi-Fi가 바뀜) 그것을 알아내려고 켠다.
            // 기본값으로는 2시간 동안 조용해야 확인을 시작하므로, 그런 끊김은 아주 늦게 안다.
            s.soTimeout = 0
            s.keepAlive = true
            Log.d(TAG, "첫 줄 받음 → 준비됨: $first")
            mainHandler.post { if (id == connectId) _connectionState.value = ConnState.READY }
            // hello 줄은 앱에 전달하지 않는다. 첫 줄이 hello가 아니면 그 줄도 전달한다.
            if (!isHello(first)) deliver(id, first)

            while (true) {
                val line = reader.readLine() ?: break   // null이면 상대가 닫았다(EOF)
                deliver(id, line)
            }
            Log.d(TAG, "EOF: 상대가 연결을 닫음")
            endConnection(id)
        } catch (e: IOException) {
            // 연결 실패(타임아웃·거부), 읽기 중 오류, disconnect()가 소켓을 닫은 경우
            connectionFailed(id, e)
        } catch (e: IllegalArgumentException) {
            // 주소를 만들 수 없는 경우. 앱을 끝내지 않고 끊김으로 둔다.
            connectionFailed(id, e)
        } catch (e: SecurityException) {
            // INTERNET 권한이 없는 경우. 앱을 끝내지 않고 끊김으로 둔다.
            connectionFailed(id, e)
        } finally {
            closeQuietly(s)
        }
    }

    // 연결 스레드에서 오류가 났다. 지난 회차(disconnect()·새 connect()·끊김 처리가 닫은 소켓)면 Log.d만 남기고 상태는 바꾸지 않는다.
    private fun connectionFailed(id: Int, e: Exception) {
        if (id == connectId) {
            Log.w(TAG, "connect/read 오류: $e")
        } else {
            Log.d(TAG, "지난 연결 스레드 끝남: $e")
        }
        endConnection(id)
    }

    // 연결이 끝났다(시뮬레이터 종료·연결 실패·hello 없음·write 오류·잘못된 주소). 지금 회차일 때만 끊김으로 둔다.
    // 끊김으로 둘 때 회차를 올린다. write 오류 뒤 여기서 소켓을 닫으면 읽기 스레드가 풀리는데, 그 결과는 지난 회차라 Log.d만 남는다.
    // disconnect()는 회차를 올리므로, 사용자가 끊은 뒤에는 여기서 아무것도 바꾸지 않는다(연결 안 됨 그대로).
    private fun endConnection(id: Int) {
        mainHandler.post {
            if (id != connectId) return@post
            connectId++   // 이 회차는 끝났다. 소켓을 닫기 전에 올려야 풀린 스레드가 지난 회차로 본다
            Log.d(TAG, "connection ended → 끊김")
            closeSocket()
            _connectionState.value = ConnState.LOST
        }
    }

    // {"event":"hello", …} 줄인지 본다. JSON이 아니면 hello가 아니다.
    private fun isHello(line: String): Boolean {
        return try {
            JSONObject(line).optString("event", "") == "hello"
        } catch (e: Exception) {
            false
        }
    }

    // 지금 회차의 소켓을 닫는다. 연결 스레드의 readLine이 풀려 끝난다. 두 번 불려도 괜찮다. 메인 스레드에서 부른다.
    private fun closeSocket() {
        val s = socket
        socket = null
        writer = null
        if (s != null) closeQuietly(s)
    }

    private fun closeQuietly(s: Socket) {
        try {
            s.close()
        } catch (e: IOException) {
            Log.w(TAG, "socket.close 오류: $e")
        }
    }

    override fun disconnect() {
        connectId++   // 회차를 올린다. 지금 연결 스레드가 보내는 결과(상태·메시지)는 모두 버려진다
        if (socket == null) {
            Log.d(TAG, "disconnect: 연결 없음 → 연결 안 됨")
        } else {
            Log.d(TAG, "disconnect: socket.close() → 연결 안 됨")
            closeSocket()
        }
        _connectionState.value = ConnState.DISCONNECTED
    }

    // 받은 한 줄을 메인 스레드에서 리스너에 전달한다. 지난 회차의 줄은 버린다.
    private fun deliver(id: Int, line: String) {
        Log.d(TAG, "received: $line")
        mainHandler.post {
            if (id == connectId) messageListener?.invoke(line)
        }
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!isReady) {
            Log.w(TAG, "send: 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        val w = writer
        if (w == null) {
            Log.w(TAG, "send: writer 없음 → 무시함 (\"$command\")")
            return
        }
        val id = connectId
        // RealBleunoClient처럼 끝에 언제나 "\n"을 붙인다. 빈 글자도 거르지 않는다(빈 줄 하나를 보낸다).
        val text = command + "\n"
        // 단일 스레드 executor라서 보낸 순서대로 하나씩 쓴다
        sendExecutor.execute {
            try {
                w.write(text)
                w.flush()
                Log.d(TAG, "sent: \"${text.trim()}\"")
            } catch (e: IOException) {
                Log.w(TAG, "write 오류: $e → 끊김")
                endConnection(id)
            }
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }
}
```
