# 13주차 따라하기 — 보드에 명령 보내고 응답 받기

12주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
12주차 프로젝트가 없거나 실행되지 않으면 강의자에게 12주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에 고치는 파일은 제어 화면 쪽뿐이다. `ControlActivity.kt`·`activity_control.xml`·`strings.xml`(1·2일차)과 `colors.xml`(2일차)이다.
`MainActivity.kt`, `activity_main.xml`, `AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml`, `bleuno` 패키지 8개는 12주차 그대로 둔다. 전체 내용은 [부록 A](#부록-a--바꾸지-않는-파일-전체)와 [부록 B](#부록-b--제공-bleuno-파일-전체)에 있다.

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
- 1일차에는 번호 검사가 없어 `9`도 그대로 나간다. `9` 같은 번호는 **Fake에서만** 해 본다. 보드는 번호를 검사하지 않아 실보드에서는 어떻게 될지 알 수 없다(2일차에 앱이 막는다).

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
- 화면을 돌리면 로그가 비워진 뒤 `on 3`과 응답이 한 번 더 찍힐 수 있다. Switch 켜짐 상태가 되살아나며 리스너가 한 번 더 불리기 때문이다(3주차 회전). 캡처는 돌리지 않은 세로 화면에서 찍는다.

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

아래 파일은 12주차 2일차에 만든 그대로이며 이번 주에는 1·2일차 모두 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.

- `MainActivity.kt`, `activity_main.xml`, `AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml` — [부록 A](#부록-a--바꾸지-않는-파일-전체), [examples/day1](examples/day1)
- `bleuno` 패키지 8개 — [부록 B](#부록-b--제공-bleuno-파일-전체), [bleuno/src](../../bleuno/src)

`AndroidManifest.xml`에 더할 권한은 없다. 명령 보내기(write)와 응답 받기(notify)는 10주차에 넣은 `BLUETOOTH_CONNECT`(Android 12 이상) 권한 안에 들어 있다.

## 2일차

### 8. colors.xml에 로그 색 두 개 넣기

1. `app › res › values › colors.xml`을 연다. 새 프로젝트를 만들 때 생긴 파일이라 `black`·`white` 두 줄이 있다. 파일이 없으면 `values`를 오른쪽 클릭 → **New › Values Resource File** → 이름 `colors`로 만든다.
2. `white` 줄 아래(마지막 `</resources>` 바로 위)에 두 줄을 넣는다.

```xml
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
```

전체는 아래와 같다. 같은 코드가 [examples/day2/colors.xml](examples/day2/colors.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

3. 실행한다. 화면은 1일차와 같다. 색은 11단계에서 쓴다.

- `#AARRGGBB`: 앞 두 자리 `FF`는 불투명, 뒤 여섯 자리가 빨강·초록·파랑이다. `log_ok`는 초록, `log_error`는 빨강이다.
- 4주차 `strings.xml` → `@string/`·`R.string`과 같은 관계로, `colors.xml`에 붙인 이름은 코드에서 `R.color.log_error`로 부른다.

### 9. 허용되지 않는 번호 막기

1. `ControlActivity.kt`의 `// 2.` LED Switch 리스너에서 빈 칸 가지와 `} else if (isChecked) {` 사이에 가지 하나를 넣는다. 리스너 윗부분은 아래와 같다.

```kotlin
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isAllowedIndex(pin.toInt()) == false) {
                // 11. 허용되지 않는 번호면 보드에 보내지 않고 Toast로 알린다. 번호 확인은 12번 함수가 한다(13주차 2일차).
                Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
```

2. `isAllowedIndex`가 빨간색이다. 아직 함수가 없기 때문이다. `onStop()`을 닫는 `}` **아래**, 클래스를 닫는 마지막 `}` **위**에 한 줄을 비우고 함수를 넣는다.

```kotlin
    // 12. 보드에 보내도 되는 번호면 true, 아니면 false(13주차 2일차).
    //     수업 보드의 LED 번호는 0~3이고, -1은 "전체"라는 약속이다(7번 [전체 끄기]). 입력 칸은 inputType이 number라 -를 적을 수 없다.
    //     펌웨어는 번호 범위를 확인하지 않아서 이 밖의 번호를 보내면 보드가 어떻게 될지 모른다. 그래서 보내기 전에 앱이 막는다.
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

3. 실행하고 [제어 화면]에 들어가 `9` → Switch 켜기를 한다. Toast `허용되지 않는 번호`가 뜨고 로그에는 아무 줄도 생기지 않으면 성공이다. Logcat `tag:BLE`에도 `writeCharacteristic` 줄이 없다. 앱이 보내기 전에 막았다는 증거다.
4. `3`으로 바꿔 Switch를 켜고 끄면 1일차처럼 명령과 응답이 쌓인다.
5. 다시 `9`를 넣고 Switch를 눌러 Toast가 떠 있는 동안 **캡처한다.** 입력 칸 `9`, Toast `허용되지 않는 번호`, 로그에 `on 9`가 없는 화면이 제출 캡처 2다. Toast는 2초 만에 사라지니 뜨자마자 찍는다.

- 사슬 순서는 **빈 칸 → 허용 번호 → 켜기/끄기**다. 빈 칸 검사가 먼저 걸러 주므로 `pin.toInt()`가 빈 글자에서 불리지 않는다.
- `listOf(0, 1, 2, 3).contains(index)`: 오늘 문법. 목록 안에 `index`가 있으면 `true`다. 괄호 안에는 목록과 같은 종류(숫자)를 넣는다. `contains(pin)`처럼 글자를 넣으면 `Type inference failed. …` 오류가 난다.
- `: Boolean`과 `return true`/`return false`: 10주차 `hasBlePermissions()`처럼 참/거짓 하나를 돌려주는 함수다. `if`를 두 번 써서 `0`~`3`이거나 `-1`이면 `true`, 둘 다 아니면 마지막 줄의 `false`가 된다.
- `== false`는 12주차처럼 "아니면"이다. 허용 번호가 **아니면** Toast 가지로 간다.
- 검사에 걸리면 Switch 모양만 바뀌고 명령·로그는 없다. 빈 칸 Toast와 같은 동작이다.

### 10. 준비됨일 때만 누르고, 보낸 직후 300ms 쉬기

1. `activity_control.xml`에서 `ledSwitch`와 `allOffButton` 블록의 `android:layout_marginTop="16dp"` 아래에 각각 `android:enabled="false"` 한 줄을 넣는다.

```xml
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/led" />
```

```xml
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/all_off" />
```

   이대로 실행하면 두 버튼이 늘 회색이다. 2번에서 코드로 켠다.

2. `ControlActivity.kt`의 `// 4.` collect 안, `binding.stateText.text = "상태: $state"` **아래**에 `// 13.` 줄들을 넣는다. 블록 전체는 아래와 같다. 예제 파일에는 `// (확장)`이 붙은 `pwmSeekBar` 줄이 두 개 더 있다. 그 두 줄은 SeekBar를 만드는 12단계에서 넣는다.

```kotlin
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                    // 13. 먼저 모두 끄고, 준비됨일 때만 LED Switch·[전체 끄기]를 켠다. MainActivity 8번과 같은 방법이다(13주차 2일차).
                    //     준비되지 않았을 때 보낸 명령은 라이브러리가 버리므로 아예 누르지 못하게 한다.
                    binding.ledSwitch.isEnabled = false
                    binding.allOffButton.isEnabled = false
                    if (state == ConnState.READY) {
                        binding.ledSwitch.isEnabled = true
                        binding.allOffButton.isEnabled = true
                    }
                }
            }
        }
```

| 빨간 글자 | 가져올 import |
|---|---|
| `ConnState` | `com.example.smartio.bleuno.ConnState` |

3. 실행해 확인한다.
   - 목록 줄 탭 → `준비됨` → [제어 화면]: `상태: 준비됨`이 되자마자 Switch와 [전체 끄기]가 켜진다.
   - [뒤로] → [해제] → [연결]로 들어오기: `상태: 연결 안 됨`, Switch와 [전체 끄기]가 회색이라 눌리지 않는다. 1일차에 이 길로 들어와 Switch를 켜면 Logcat에 `send(가짜): 준비되지 않아 무시함` 경고가 찍혔는데, 이제는 누를 수 없어 경고도 없다.

4. 클래스 끝, `isAllowedIndex()` 함수 **아래**에 한 줄을 비우고 `pauseButtons()` 함수를 넣는다. 예제 파일의 `// (확장)` 줄 두 개는 이번에도 12단계에서 넣는다.

```kotlin
    // 15. 명령을 보낸 직후 300ms 동안 LED Switch·[전체 끄기]를 꺼 두어 연달아 누르지 못하게 한다(13주차 2일차).
    //     5주차 isEnabled로 버튼 막기에 6주차 코루틴 delay를 썼다. 300ms 뒤에도 준비됨일 때만 다시 켠다(그사이 끊겼으면 13번이 끈 채로 둔다).
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

| 빨간 글자 | 가져올 import |
|---|---|
| `delay` | `kotlinx.coroutines.delay` |

`lifecycleScope`와 `launch`는 12주차 `// 4.`에서 이미 import했다.

5. `send`를 부르는 세 곳에서 `append` 줄 **아래**에 `// 14.` 주석과 `pauseButtons()`를 넣는다.

켜기(`// 5.` 가지):

```kotlin
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다. 끄고 켜는 일은 15번 함수가 한다(13주차 2일차).
                pauseButtons()
```

끄기(`// 6.` 가지):

```kotlin
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
                pauseButtons()
```

[전체 끄기](`// 7.` 리스너):

```kotlin
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
            // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
            pauseButtons()
```

6. 실행하고 `3` → Switch를 켠다. 누른 순간 Switch와 [전체 끄기]가 잠깐(0.3초) 회색이 되었다가 다시 켜진다. 300ms는 짧아 잘 안 보이면 `delay(300)`을 잠시 `delay(3000)`으로 바꿔 3초 동안 회색인 것을 확인하고, **`delay(300)`으로 되돌린다.**

- XML의 `android:enabled="false"`: 5주차 `stopButton`, 12주차 `controlButton`처럼 "꺼진 채로 시작"이다. client가 없거나 첫 상태가 오기 전에도 누를 수 없다.
- `// 13.`: 12주차 연결 화면(`MainActivity` 8번)과 같은 방법으로 먼저 모두 끄고, `준비됨`일 때만 켠다. 제어 화면은 "준비됨이냐 아니냐"만 보면 되므로 7주차 `when` 대신 `if` 하나로 썼다. [뒤로]는 늘 켜 둔다.
- `pauseButtons()`: 5주차 `isEnabled`로 끄고, 6주차 `lifecycleScope.launch { delay() }`로 기다렸다가 켠다. 화면이 닫히면 이 코루틴도 함께 취소된다.
- `Bleuno.client?.isReady == true`: `isReady`는 상태가 `준비됨`이면 `true`다. client가 없으면 `?.`의 결과가 `null`이고 `null == true`는 `false`라 켜지 않는다. 7주차 `scanJob?.isActive == true`와 같은 모양이다. 300ms 사이에 끊겼으면 13번이 끈 상태를 그대로 둔다.
- `delay(300)`을 `launch { }` 밖에 쓰면 6주차에 본 `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` 오류가 난다.

### 11. 오류 응답을 AlertDialog와 색으로 알리기

1. `onStart()`의 `if (result != null) {` 안, `binding.logText.append("응답: $json\n")` **아래**에 `// 16.` 가지를 넣는다. `onMessage` 안쪽은 아래와 같다.

```kotlin
            val result = BleunoMessage.result(json)
            if (result != null) {
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
```

2. 빨간 글자를 Alt+Enter → Import로 가져온다. `AlertDialog`는 목록에 두 개가 뜨면 **`androidx.appcompat.app.AlertDialog`**를 고른다(10주차와 같다).

| 빨간 글자 | 가져올 import |
|---|---|
| `ContextCompat` | `androidx.core.content.ContextCompat` |
| `AlertDialog` | `androidx.appcompat.app.AlertDialog` |

3. 실행하고 `3` → Switch 켜기. 응답 `ok`가 오는 순간 로그 글자 전체가 **초록색**이 된다.
4. 오류 응답을 일부러 만들어 본다. `// 5.` 가지의 `send` 줄에서 `"on $index"`를 `"on$index"`(띄어쓰기 없음)로 **한 곳만** 바꾸고 실행한다. 로그 줄 `append("on $index\n")`은 바꾸지 않는다.
5. [제어 화면]에 들어온 직후 `3` → Switch 켜기를 한다.
   - 로그: `on 3` 다음 `응답: {"result":"fail","ms":"unknown command"}`, 로그 글자 전체가 **빨간색**
   - AlertDialog: 제목 `보드가 오류를 알렸습니다`, 내용 `응답: fail · unknown command`, [확인]
   - Logcat `tag:BLE`: `writeCharacteristic(가짜): "on3"` → `onCharacteristicChanged(가짜): {"result":"fail","ms":"unknown command"}`
6. [확인] → [전체 끄기]를 누르면 `ok` 응답이 와서 로그가 다시 초록색이 된다.
7. `"on$index"`를 **`"on $index"`로 되돌리고** 한 번 더 실행해 `ok`로 끝나는지 본다.

- `result != "ok"`: `err`(명령은 맞지만 값이 틀림)와 `fail`(모르는 명령) 모두 이 가지로 온다.
- `BleunoMessage.message(json) ?: ""`: `"ms"` 설명 값을 꺼낸다. `String?`이라 3주차 `?:`로 없을 때 빈 글자를 넣는다. 로그에는 JSON 원문이 이미 있으므로 창에는 사람이 읽기 쉬운 `응답: fail · unknown command`를 보여 준다.
- `ContextCompat.getColor(this, R.color.log_error)`: `colors.xml`에 이름 붙인 색의 실제 값을 꺼낸다. `setTextColor`는 로그 칸 **전체** 글자색을 바꾼다. 한 줄만 색을 바꾸는 방법은 다루지 않는다.
- AlertDialog는 10주차와 같은 모양이다. 이 중괄호는 람다지만 `object :` 익명 객체 안이 아니라서 `this`가 그대로 `ControlActivity`다.
- 응답은 `onStart`~`onStop` 사이에만 받으므로 창을 띄울 때 화면이 보이고 있다. 12주차 "창은 화면이 보이는 동안만 띄운다"와 맞는다.
- 앱 로그에는 `on 3`인데 실제로 보낸 글자는 `"on3"`이었다. **명령이 이상하면 Logcat `writeCharacteristic` 줄에서 보낸 글자를 확인한다.**

### 12. (확장) SeekBar로 LED 0 밝기 조절하기

시간이 남으면 한다. 하지 않으면 이 단계를 건너뛰고 13단계로 간다.

1. `strings.xml`의 `all_off` 줄 아래에 한 줄을 넣는다.

```xml
    <string name="pwm_title">LED 0 밝기</string>
```

2. `activity_control.xml`에서 `allOffButton` 블록을 닫는 `/>` **아래**, `명령 로그` 제목 `TextView` **위**에 한 줄을 비우고 가로 줄을 넣는다.

```xml
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
```

3. `ControlActivity.kt`의 `// 7.` [전체 끄기] 리스너를 닫는 `}` **아래**(onCreate를 닫는 `}` 바로 위)에 한 줄을 비우고 넣는다.

```kotlin
        // 17. (확장) SeekBar로 LED 0의 밝기(0~255)를 정한다. 손을 뗄 때 "pwm 0 값" 명령을 한 번 보낸다(13주차 2일차).
        //     object : SeekBar.OnSeekBarChangeListener { … }는 10주차 BroadcastReceiver와 같은 익명 객체 틀이다. 함수 세 개를 모두 적어야 한다.
        binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // 끌고 있는 동안에는 보내지 않는다. 움직일 때마다 보내면 명령이 너무 많이 쌓인다.
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                // 손을 댈 때는 할 일이 없다.
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                val value = binding.pwmSeekBar.progress
                Bleuno.client?.send("pwm 0 $value")
                binding.logText.append("pwm 0 $value\n")
                pauseButtons()
            }
        })
```

| 빨간 글자 | 가져올 import |
|---|---|
| `SeekBar` | `android.widget.SeekBar` |

4. SeekBar도 `준비됨`일 때만 켜지고 보낸 직후 꺼지게 `// (확장)` 줄을 두 곳에 두 줄씩 더한다. `// 13.` collect 블록은 아래처럼 된다.

```kotlin
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                    // 13. 먼저 모두 끄고, 준비됨일 때만 LED Switch·[전체 끄기]를 켠다. MainActivity 8번과 같은 방법이다(13주차 2일차).
                    //     준비되지 않았을 때 보낸 명령은 라이브러리가 버리므로 아예 누르지 못하게 한다.
                    binding.ledSwitch.isEnabled = false
                    binding.allOffButton.isEnabled = false
                    binding.pwmSeekBar.isEnabled = false // (확장) 17번 SeekBar도 같이 끈다.
                    if (state == ConnState.READY) {
                        binding.ledSwitch.isEnabled = true
                        binding.allOffButton.isEnabled = true
                        binding.pwmSeekBar.isEnabled = true // (확장)
                    }
                }
            }
        }
```

`// 15.` `pauseButtons()` 함수는 아래처럼 된다.

```kotlin
    private fun pauseButtons() {
        binding.ledSwitch.isEnabled = false
        binding.allOffButton.isEnabled = false
        binding.pwmSeekBar.isEnabled = false // (확장)
        lifecycleScope.launch {
            delay(300)
            if (Bleuno.client?.isReady == true) {
                binding.ledSwitch.isEnabled = true
                binding.allOffButton.isEnabled = true
                binding.pwmSeekBar.isEnabled = true // (확장)
            }
        }
    }
```

5. 실행하고 `준비됨` 제어 화면에서 `LED 0 밝기` 막대를 가운데쯤 끌었다가 놓는다. 놓는 순간 로그에 `pwm 0 127`(값은 위치에 따라 다름) 다음 `응답: {"result":"ok","ms":"pwm set"}`이 쌓인다. 실보드면 0번 LED(GPIO4)의 밝기가 바뀐다.

- `object : SeekBar.OnSeekBarChangeListener { … }`: 10주차 `object : BroadcastReceiver() { override fun onReceive … }`와 같은 익명 객체 틀이다. 할 일이 세 개(끄는 중·손 댐·손 뗌)인 리스너라 `setOnCheckedChangeListener { }`처럼 중괄호 하나로 쓸 수 없고, 함수 세 개를 **모두** 적는다.
- 끄는 동안(`onProgressChanged`)마다 보내면 write 큐에 명령이 수십 개 쌓인다. 손을 뗄 때(`onStopTrackingTouch`) 한 번만 보낸다.
- `binding.pwmSeekBar.progress`: 막대의 지금 값이다. XML `android:max="255"`라 `0`~`255`만 나온다.
- 명령은 `pwm 0 값`으로 LED 0번에 고정했다. 규약 표의 `pwm N V`다.

완성한 `ControlActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/ControlActivity.kt](examples/day2/ControlActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.os.Bundle
import android.widget.SeekBar
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.bleuno.Bleuno
import com.example.smartio.bleuno.BleunoMessage
import com.example.smartio.bleuno.ConnState
import com.example.smartio.databinding.ActivityControlBinding
import kotlinx.coroutines.delay
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
            } else if (isAllowedIndex(pin.toInt()) == false) {
                // 11. 허용되지 않는 번호면 보드에 보내지 않고 Toast로 알린다. 번호 확인은 12번 함수가 한다(13주차 2일차).
                Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다. 끄고 켜는 일은 15번 함수가 한다(13주차 2일차).
                pauseButtons()
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
                pauseButtons()
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
                    // 13. 먼저 모두 끄고, 준비됨일 때만 LED Switch·[전체 끄기]를 켠다. MainActivity 8번과 같은 방법이다(13주차 2일차).
                    //     준비되지 않았을 때 보낸 명령은 라이브러리가 버리므로 아예 누르지 못하게 한다.
                    binding.ledSwitch.isEnabled = false
                    binding.allOffButton.isEnabled = false
                    binding.pwmSeekBar.isEnabled = false // (확장) 17번 SeekBar도 같이 끈다.
                    if (state == ConnState.READY) {
                        binding.ledSwitch.isEnabled = true
                        binding.allOffButton.isEnabled = true
                        binding.pwmSeekBar.isEnabled = true // (확장)
                    }
                }
            }
        }

        // 7. [전체 끄기] 버튼: 번호 자리에 -1을 보내면 보드의 LED가 모두 꺼진다(13주차 1일차).
        binding.allOffButton.setOnClickListener {
            Bleuno.client?.send("off -1")
            binding.logText.append("off -1\n")
            // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
            pauseButtons()
        }

        // 17. (확장) SeekBar로 LED 0의 밝기(0~255)를 정한다. 손을 뗄 때 "pwm 0 값" 명령을 한 번 보낸다(13주차 2일차).
        //     object : SeekBar.OnSeekBarChangeListener { … }는 10주차 BroadcastReceiver와 같은 익명 객체 틀이다. 함수 세 개를 모두 적어야 한다.
        binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // 끌고 있는 동안에는 보내지 않는다. 움직일 때마다 보내면 명령이 너무 많이 쌓인다.
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                // 손을 댈 때는 할 일이 없다.
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                val value = binding.pwmSeekBar.progress
                Bleuno.client?.send("pwm 0 $value")
                binding.logText.append("pwm 0 $value\n")
                pauseButtons()
            }
        })
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

    // 10. 화면이 안 보이게 되면 응답 받기를 푼다(null). onStart의 등록과 반드시 짝을 맞춘다(13주차 1일차).
    //     10주차 배터리 Receiver의 등록·해제와 같은 규칙이다. 풀지 않으면 보이지 않는 화면의 로그를 계속 고치려 한다.
    override fun onStop() {
        super.onStop()
        Bleuno.client?.onMessage(null)
    }

    // 12. 보드에 보내도 되는 번호면 true, 아니면 false(13주차 2일차).
    //     수업 보드의 LED 번호는 0~3이고, -1은 "전체"라는 약속이다(7번 [전체 끄기]). 입력 칸은 inputType이 number라 -를 적을 수 없다.
    //     펌웨어는 번호 범위를 확인하지 않아서 이 밖의 번호를 보내면 보드가 어떻게 될지 모른다. 그래서 보내기 전에 앱이 막는다.
    private fun isAllowedIndex(index: Int): Boolean {
        if (listOf(0, 1, 2, 3).contains(index)) {
            return true
        }
        if (index == -1) {
            return true
        }
        return false
    }

    // 15. 명령을 보낸 직후 300ms 동안 LED Switch·[전체 끄기]를 꺼 두어 연달아 누르지 못하게 한다(13주차 2일차).
    //     5주차 isEnabled로 버튼 막기에 6주차 코루틴 delay를 썼다. 300ms 뒤에도 준비됨일 때만 다시 켠다(그사이 끊겼으면 13번이 끈 채로 둔다).
    private fun pauseButtons() {
        binding.ledSwitch.isEnabled = false
        binding.allOffButton.isEnabled = false
        binding.pwmSeekBar.isEnabled = false // (확장)
        lifecycleScope.launch {
            delay(300)
            if (Bleuno.client?.isReady == true) {
                binding.ledSwitch.isEnabled = true
                binding.allOffButton.isEnabled = true
                binding.pwmSeekBar.isEnabled = true // (확장)
            }
        }
    }
}
```

`activity_control.xml` 전체 — [examples/day2/activity_control.xml](examples/day2/activity_control.xml)

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

    <Button
        android:id="@+id/backButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="24dp"
        android:text="@string/back" />

</LinearLayout>
```

`strings.xml` 전체 — [examples/day2/strings.xml](examples/day2/strings.xml)

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
</resources>
```

확장을 하지 않았다면 내 파일에는 `activity_control.xml`의 `LinearLayout` 덩어리, `strings.xml`의 `pwm_title`, `ControlActivity.kt`의 `import android.widget.SeekBar`·`// 17.` 덩어리·`// (확장)`이 붙은 네 줄이 없다. 나머지는 위와 같아야 한다.
1일차 코드와 무엇이 다른지 한눈에 보려면 Android Studio에서 두 파일을 골라 오른쪽 클릭 › **Compare Files**를 쓴다.

### 13. 제출하기

1. 11단계에서 바꾼 `"on$index"`가 `"on $index"`로 되돌려져 있는지 확인하고 한 번 실행한다.
2. 제출물은 다섯 가지다.
   1. `ControlActivity.kt`
   2. `activity_control.xml`
   3. 캡처 1: 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 보이는 세로 제어 화면(6단계)
   4. 캡처 2: 입력 칸 `9`, Toast `허용되지 않는 번호`, 로그에 `on 9`가 없는 제어 화면(9단계)
   5. 사진: 번호 3 LED가 켜진 보드(6단계, 보드가 없으면 생략)

- 캡처 2를 1일차 코드로 찍으면 로그에 `on 9`가 생긴다. 2일차 검사를 넣은 뒤 찍는다.
- 캡처와 사진에 계정 이름·알림 내용이 보이지 않게 한다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
명령이 안 먹으면 Logcat `tag:BLE`에서 `writeCharacteristic` 줄(보낸 글자)과 `onCharacteristicChanged` 줄(받은 대답)을 차례로 본다. 보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다.

## 부록 A — 바꾸지 않는 파일 전체

아래 파일은 12주차 `examples/day2`와 글자 단위로 같다. 이번 주 1·2일차 모두 바꾸지 않는다. 같은 코드가 [examples/day1](examples/day1)과 [examples/day2](examples/day2)에 있다.

`MainActivity.kt` — [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)(400행). 12주차 [따라하기](../week12_ble_gatt/walkthrough.md)에서 완성한 연결 화면 그대로라 여기에는 다시 싣지 않는다. 실보드로 바꿀 때 고치는 85행 `private val useFake = true` 한 줄 말고는 손대지 않는다. 내 파일과 비교할 때는 예제 파일을 연다.

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

12주차에 붙여 넣은 8개 파일이다. 모두 `app › kotlin+java › com.example.smartio › bleuno`에 있고 고치지 않는다.
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
