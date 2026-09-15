# 6주차 따라하기 — 코루틴 카운트다운과 가짜 연결

5주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
5주차 프로젝트가 없거나 실행되지 않으면 강의자에게 5주차 완성본을 받아 시작한다.

이번 주에 고치는 파일은 `MainActivity.kt`(1·2일차)와 `activity_main.xml`·`strings.xml`(2일차)뿐이다.
`ControlActivity.kt`, `activity_control.xml`, `AndroidManifest.xml`은 4주차에 만든 그대로 둔다. 전체 내용은 [7단계](#7-바꾸지-않는-파일-확인하기)에 있다.

## 1일차

### 1. 5주차 프로젝트 열고 실행하기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 연결 화면에 아래가 보이면 시작할 수 있다.

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지]
대기 중
[연결]
```

3. `app › res › layout › activity_main.xml`은 5주차 2일차에 완성한 그대로다. 아래와 같은지 확인한다. id 이름이 다르면 아래 파일로 바꾼다.
   같은 코드가 [examples/day1/activity_main.xml](examples/day1/activity_main.xml)에 있다.

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

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

</LinearLayout>
```

`stopButton`에 `android:enabled="false"`가 있다. 1일차에는 [중지]를 쓰지 않으므로 처음부터 눌리지 않게 둔다. 2일차에 코드로 켠다.

4. `app › res › values › strings.xml`도 5주차 그대로다. 같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
    <string name="device_unknown">장치: ?</string>
    <string name="pin_hint">핀 번호</string>
    <string name="led">LED</string>
    <string name="log_title">명령 로그</string>
    <string name="back">뒤로</string>
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
</resources>
```

### 2. Handler 코드 지우기

`MainActivity.kt`를 열고 5주차 2일차에 넣었던 `Handler` 관련 코드를 **여섯 군데** 지운다. 위에서 아래 순서다.

1. 클래스 안, `private lateinit var binding` 줄 아래에 있는 **한 줄**: `private val handler = Handler(Looper.getMainLooper())`. 바로 위의 `// 5주차 2일차: …` 주석도 함께 지운다.
2. `onCreate()` 안의 `val finishScan = Runnable {` 로 시작해 `}` 로 끝나는 **7줄짜리 블록 전체**(안에 `검색 완료`, `View.GONE`, Toast가 있는 블록). 위의 `// 3. 검색이 끝났을 때 …` 주석도 지운다.
3. `binding.scanButton.setOnClickListener { … }` **안**의 세 줄: `binding.stopButton.isEnabled = true`, `binding.stateText.text = "검색 중…"`, `handler.postDelayed(finishScan, 5000)`. 나머지 두 줄(`isEnabled = false`, `scanProgress.visibility = View.VISIBLE`)은 남긴다.
4. `binding.stopButton.setOnClickListener {` 로 시작하는 **7줄짜리 블록 전체**(`removeCallbacks`가 있는 블록). 위의 `// 5. [중지] 버튼 …` 주석도 지운다.
5. 5주차에 `onDestroy()`를 넣었다면(`handler.removeCallbacksAndMessages(null)`이 있는 블록) `override fun onDestroy() {` 부터 짝 `}` 까지 **블록 전체**를 지운다. 남겨 두면 `handler`를 찾을 수 없다는 빨간 줄이 난다.
6. 파일 위쪽의 `import android.os.Handler`, `import android.os.Looper` 두 줄. 회색으로 바뀐 import는 지워도 된다.

지우고 나면 [검색] 리스너는 아래 두 줄만 남는다. 4주차에 만든 `connectButton`·`autoSwitch` 코드는 그대로 둔다.

```kotlin
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
        }
```

실행해 화면이 그대로 뜨는지 본다. 아직 [검색]을 누르면 버튼만 회색이 되고 원만 돈다.

### 3. lifecycleScope.launch로 카운트다운 만들기

1. [검색] 리스너의 두 줄 **아래**에 `lifecycleScope.launch { … }`를 넣는다. 전체는 아래와 같다.

```kotlin
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                for (i in 5 downTo 1) {
                    binding.stateText.text = "검색 중… $i"
                    delay(1000)
                }
                binding.stateText.text = "검색 완료"
                binding.scanProgress.visibility = View.GONE
                binding.scanButton.isEnabled = true
            }
        }
```

2. 빨간 글자 세 개를 차례로 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `lifecycleScope` | `androidx.lifecycle.lifecycleScope` |
| `launch` | `kotlinx.coroutines.launch` |
| `delay` | `kotlinx.coroutines.delay` |

`View`는 5주차에 이미 import했다. 빨간색이면 `android.view.View`를 가져온다.

3. 실행하고 [검색]을 누른다. `검색 중… 5`, `검색 중… 4`, … `검색 중… 1`이 1초마다 바뀌고 5초 뒤 `검색 완료`가 되면 성공이다.
   카운트다운 중에 장치 이름 EditText를 눌러 글자를 넣어 본다. 글자가 바로 들어가면 화면이 멈추지 않은 것이다.

- `lifecycleScope.launch { }`: 중괄호 안을 **코루틴**으로 시작한다. 이 화면(`MainActivity`)이 사라지면 함께 사라진다.
- `for (i in 5 downTo 1)`: `i`가 5, 4, 3, 2, 1로 바뀌며 중괄호 안을 다섯 번 실행한다.
- `delay(1000)`: 1초 기다린다. 5주차의 `Thread.sleep`과 달리 기다리는 동안 화면이 움직인다.

### 4. delay를 Thread.sleep으로 바꿔 보기

한 곳만 바꾸고 실행한 뒤 반드시 되돌린다.

1. `delay(1000)`을 `Thread.sleep(1000)`으로 바꾼다. 빌드는 된다.
2. 실행하고 [검색]을 누른다. 5초 동안 숫자가 바뀌지 않고 EditText도 눌리지 않다가, 5초 뒤 `검색 완료`만 보인다.
   중간 숫자는 화면에 그려질 틈이 없었다. 5주차에 본 "메인 스레드가 막힌" 상태다.
3. 관찰한 결과를 [실습지](lab.md#3-delay와-threadsleep-비교하기)의 표에 적고, `delay(1000)`으로 되돌린다.

### 5. countDown()으로 묶기

카운트다운 부분을 함수 하나로 뺀다. 안에서 `delay`를 쓰므로 `fun` 앞에 `suspend`가 붙는다.

1. `onCreate()`의 마지막 `}` **아래**, 클래스의 마지막 `}` **위**에 아래 함수를 넣는다.

```kotlin
    // 5부터 1까지 1초마다 화면에 보여 준다. 안에서 delay를 쓰므로 suspend가 붙는다.
    private suspend fun countDown() {
        for (i in 5 downTo 1) {
            binding.stateText.text = "검색 중… $i"
            delay(1000)
        }
    }
```

2. `launch { }` 안의 `for` 블록을 지우고 `countDown()` 한 줄로 바꾼다.

```kotlin
            lifecycleScope.launch {
                countDown()
                binding.stateText.text = "검색 완료"
                binding.scanProgress.visibility = View.GONE
                binding.scanButton.isEnabled = true
            }
```

3. 실행 결과는 3단계와 같아야 한다. `suspend`를 지워 보면 `delay` 줄에 빨간 줄이 생긴다. 다시 붙인다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
            }
        }

        // 2. 자동 연결 Switch: 켜고 끌 때마다 알린다.
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }

        // 3. [검색] 버튼(6주차 1일차): 코루틴으로 5초 카운트다운을 보여 준다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                countDown()
                binding.stateText.text = "검색 완료"
                binding.scanProgress.visibility = View.GONE
                binding.scanButton.isEnabled = true
            }
        }
    }

    // 5부터 1까지 1초마다 화면에 보여 준다. 안에서 delay를 쓰므로 suspend가 붙는다.
    private suspend fun countDown() {
        for (i in 5 downTo 1) {
            binding.stateText.text = "검색 중… $i"
            delay(1000)
        }
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
4주차 `connectButton`·`autoSwitch` 부분이 내 코드와 조금 달라도 동작이 같으면 그대로 둔다. 주석 번호가 없어도 괜찮다.

### 6. 캡처하고 보관하기

[검색]을 눌러 `검색 중… 3`쯤에서 캡처해 둔다(연습용. 제출 캡처는 2일차 [중지]로 멈춘 화면이다).
프로젝트는 2일차에 그대로 이어서 쓴다.

### 7. 바꾸지 않는 파일 확인하기

아래 파일은 4주차에 만든 그대로이며(5주차에도 바꾸지 않았다) 이번 주에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.
같은 코드가 [examples/day1](examples/day1)에 있다.

`ControlActivity.kt` — [examples/day1/ControlActivity.kt](examples/day1/ControlActivity.kt)

```kotlin
package com.example.smartio

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityControlBinding

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
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "핀 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                binding.logText.append("on $pin\n")
            } else {
                binding.logText.append("off $pin\n")
            }
        }

        // 3. [뒤로] 버튼: 이 화면을 닫고 연결 화면으로 돌아간다.
        binding.backButton.setOnClickListener {
            finish()
        }
    }
}
```

`activity_control.xml` — [examples/day1/activity_control.xml](examples/day1/activity_control.xml)

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

    <EditText
        android:id="@+id/pinEdit"
        android:layout_width="160dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/pin_hint"
        android:inputType="number" />

    <Switch
        android:id="@+id/ledSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/led" />

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). `ControlActivity` 줄이 있는지만 본다. 내 파일에는 아이콘 등의 줄이 더 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

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

## 2일차

### 8. [다시 시도] 버튼 추가하기

1. `strings.xml`의 마지막 `</resources>` 바로 위에 `retry` 한 줄을 추가한다. 전체는 아래와 같다. 같은 코드가 [examples/day2/strings.xml](examples/day2/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
    <string name="device_unknown">장치: ?</string>
    <string name="pin_hint">핀 번호</string>
    <string name="led">LED</string>
    <string name="log_title">명령 로그</string>
    <string name="back">뒤로</string>
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
    <string name="retry">다시 시도</string>
</resources>
```

2. `activity_main.xml`의 마지막 `</LinearLayout>` 바로 위([연결] 버튼 아래)에 버튼을 추가한다. `visibility="gone"`이라 처음에는 보이지 않는다.

```xml
    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />
```

전체는 아래와 같다. 같은 코드가 [examples/day2/activity_main.xml](examples/day2/activity_main.xml)에 있다.

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

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

</LinearLayout>
```

3. 실행한다. 화면은 1일차와 같아 보여야 한다(버튼은 숨어 있다).

### 9. scanJob과 [중지] 만들기

1. `MainActivity.kt`에서 `private lateinit var binding` 줄 **아래**에 변수를 하나 추가한다. 5주차에 `handler`를 두었던 자리다.

```kotlin
    // 6주차 2일차: [검색]이 시작한 코루틴. [중지]에서 취소하려고 보관한다. 아직 없으면 null이다.
    private var scanJob: Job? = null
```

`Job`이 빨간색이면 Alt+Enter로 `kotlinx.coroutines.Job`을 가져온다.

2. [검색]의 `lifecycleScope.launch {` 앞에 `scanJob = `를 붙이고, [중지]를 누를 수 있게 켠다.

```kotlin
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.scanProgress.visibility = View.VISIBLE
            scanJob = lifecycleScope.launch {
                countDown()
                binding.stateText.text = "검색 완료"
                binding.scanProgress.visibility = View.GONE
                binding.scanButton.isEnabled = true
                binding.stopButton.isEnabled = false
            }
        }
```

3. [검색] 블록 아래에 [중지] 블록을 넣는다.

```kotlin
        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            scanJob?.cancel()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
```

4. 실행하고 [검색] → `검색 중… 3`에서 [중지]를 누른다. 숫자가 3에서 멈추고 ProgressBar가 사라지며 [검색]이 다시 눌리면 성공이다. **이 화면이 제출 캡처 1이다.**

- `launch`는 시작한 코루틴을 `Job`으로 돌려준다. 변수에 보관해야 나중에 멈출 수 있다.
- `scanJob?.cancel()`: 아직 [검색]을 안 눌렀으면 `scanJob`이 `null`이다. 3주차의 `?.`로 안전하게 부른다.
- `cancel()`하면 `delay(1000)`에서 멈춰 있던 코루틴이 그 자리에서 끝난다. `검색 완료` 줄은 실행되지 않는다.

### 10. connectFake() 만들기

`countDown()` 아래에 가짜 연결 함수를 넣는다. 2초 걸리고 절반은 실패한다.

```kotlin
    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }
```

빨간 글자를 Alt+Enter로 가져온다. `Random`은 목록에서 **`kotlin.random.Random`**을 고른다(`java.util.Random`이 아니다).

| 빨간 글자 | 가져올 import |
|---|---|
| `withContext` | `kotlinx.coroutines.withContext` |
| `Dispatchers` | `kotlinx.coroutines.Dispatchers` |
| `Random` | `kotlin.random.Random` |

- `withContext(Dispatchers.IO) { }`: 중괄호 안을 다른 스레드에서 실행하고 끝나면 메인 스레드로 돌아온다. `Thread.sleep`처럼 **진짜 막히는** 일만 여기에 넣는다. `delay`는 넣을 필요가 없다.
- `: Boolean`은 이 함수가 참/거짓 하나를 돌려준다는 표시다. `fun … = …`은 `=` 오른쪽의 결과를 그대로 돌려주는 짧은 모양이다(중괄호 본문 대신). 이번 주에는 이 한 함수에서만 쓴다.
- 마지막 줄 `true`가 `withContext { }` 블록의 결과가 되어 `connectFake()`의 반환값이 된다.
- `throw Exception("연결 실패")`: 오류를 일부러 낸다. 12주차에 진짜 BLE 연결로 바꿔도 부르는 쪽은 그대로다.

### 11. tryConnect()와 try/catch

`connectFake()` 아래에 결과를 화면에 보여 주는 함수를 넣는다.

```kotlin
    // 가짜 연결을 시도하고 결과를 화면에 보여 준다.
    private suspend fun tryConnect() {
        binding.stateText.text = "연결 중…"
        try {
            connectFake()
            binding.stateText.text = "연결됨"
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } catch (e: Exception) {
            binding.stateText.text = "연결 실패"
            Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
        }
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
    }
```

- `try { }` 안에서 `connectFake()`가 오류를 던지면 그 아래 줄은 건너뛰고 `catch { }`로 간다. 오류가 없으면 `catch`는 실행되지 않는다.
- `e.message`는 `throw Exception("연결 실패")`에 적은 글자다.
- 이 함수는 `launch { }` 람다가 아니라 클래스의 함수이므로 `this`가 그대로 `MainActivity`다. 4주차처럼 `Intent(this, …)`와 `Toast.makeText(this, …)`를 쓸 수 있다.

### 12. [검색]과 [다시 시도]에서 부르기

1. [검색]의 `launch { }` 안을 아래처럼 바꾼다. 카운트다운이 끝나면 [중지]를 끄고(연결 중에는 멈출 수 없다) `tryConnect()`를 부른다.

```kotlin
        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.retryButton.visibility = View.GONE
            binding.scanProgress.visibility = View.VISIBLE
            scanJob = lifecycleScope.launch {
                countDown()
                binding.stopButton.isEnabled = false
                tryConnect()
            }
        }
```

2. [중지] 블록 아래에 [다시 시도] 블록을 넣는다. 카운트다운 없이 연결만 다시 한다.

```kotlin
        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                tryConnect()
            }
        }
```

3. 실행하고 장치 이름을 넣은 뒤 [검색]을 누른다. 카운트다운 → `연결 중…`(2초) 뒤 둘 중 하나가 된다.

| 결과 | 화면 |
|---|---|
| 성공 | `연결됨` → 제어 화면으로 넘어가고 위에 `장치: 이름`이 보인다 |
| 실패 | `연결 실패`, Toast `연결 실패`, [다시 시도] 버튼이 나타난다. **이 화면이 제출 캡처 2다** |

실패가 안 나오면 [뒤로]로 돌아와 [검색]을 다시 누른다. 절반 확률이므로 몇 번이면 나온다. [다시 시도]는 성공할 때까지 눌러 본다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 6주차 2일차: [검색]이 시작한 코루틴. [중지]에서 취소하려고 보관한다. 아직 없으면 null이다.
    private var scanJob: Job? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
            }
        }

        // 2. 자동 연결 Switch: 켜고 끌 때마다 알린다.
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.retryButton.visibility = View.GONE
            binding.scanProgress.visibility = View.VISIBLE
            scanJob = lifecycleScope.launch {
                countDown()
                binding.stopButton.isEnabled = false
                tryConnect()
            }
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            scanJob?.cancel()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            lifecycleScope.launch {
                tryConnect()
            }
        }
    }

    // 5부터 1까지 1초마다 화면에 보여 준다. 안에서 delay를 쓰므로 suspend가 붙는다.
    private suspend fun countDown() {
        for (i in 5 downTo 1) {
            binding.stateText.text = "검색 중… $i"
            delay(1000)
        }
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과를 화면에 보여 준다.
    private suspend fun tryConnect() {
        binding.stateText.text = "연결 중…"
        try {
            connectFake()
            binding.stateText.text = "연결됨"
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } catch (e: Exception) {
            binding.stateText.text = "연결 실패"
            Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
        }
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
    }
}
```

### 13. 화면 돌려 보기

[검색]을 누르고 카운트다운 중에 에뮬레이터 화면을 돌린다. 숫자가 사라지고 `대기 중`으로 돌아간다.
`lifecycleScope`가 화면과 함께 사라졌기 때문이다. 코드가 틀린 것이 아니다. 이번 주에는 관찰만 하고, 7주차에 해결한다.

### 14. 제출하기

제출물은 세 가지다.

1. `MainActivity.kt`
2. 캡처 1: [중지]로 카운트다운이 멈춘 화면(예: `검색 중… 3`)
3. 캡처 2: `연결 실패` Toast와 [다시 시도] 버튼이 보이는 화면

Toast는 2초 만에 사라지므로 Toast가 뜬 직후 바로 캡처한다. 놓치면 [다시 시도]를 눌러 다시 실패를 기다린다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 꺼졌다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 `Caused by`를 읽는다.
