# 5주차 따라하기 — 검색 버튼과 메인 스레드

4주차에 만든 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 결과가 화면에 보이면 다음 단계로 넘어간다.
막혀서 진행이 안 되면 4주차 완성본(강의자에게 요청)을 받아 시작해도 된다.

이번 주에 고치는 파일은 `activity_main.xml`, `strings.xml`, `MainActivity.kt` 세 개다.
`ControlActivity.kt`, `activity_control.xml`, `AndroidManifest.xml`은 4주차 그대로 두며, 전체 내용은 [부록](#부록--4주차에서-그대로-쓰는-파일)에 있다.

## 1일차

### 1. 프로젝트 열고 실행하기

1. Android Studio에서 4주차 `SmartIO` 프로젝트를 연다. 최근 목록에 없으면 **File › Open**에서 폴더를 고른다.
2. `Run ▶`을 눌러 연결 화면(제목·장치 이름·자동 연결·[연결])이 뜨는지 확인한다.

### 2. 문자열 추가하기

`app › res › values › strings.xml`을 열고 `</resources>` **바로 위**에 세 줄을 추가한다.

```xml
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
```

추가한 뒤 전체는 아래와 같다. 4주차 아홉 줄은 그대로이고 세 줄이 더해졌다.
같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

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

4주차에 문자열 이름을 다르게 지었다면 내 이름을 그대로 두고 세 줄만 추가한다. 4주차 줄을 지우면 `activity_control.xml`이 그 이름을 찾지 못해 빌드가 되지 않는다.

### 3. [검색] 버튼과 상태 글자 배치하기

`app › res › layout › activity_main.xml`을 열고 `Switch`와 [연결] `Button` **사이**에 아래 두 View를 넣는다.

```xml
    <Button
        android:id="@+id/scanButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/scan" />

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_idle"
        android:textSize="18sp" />
```

넣은 뒤 전체는 아래와 같다. 같은 코드가 [examples/day1/activity_main.xml](examples/day1/activity_main.xml)에 있다.

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

    <Button
        android:id="@+id/scanButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/scan" />

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

실행하면 Switch 아래에 [검색] 버튼과 `대기 중` 글자가 보인다. 아직 [검색]을 눌러도 아무 일도 일어나지 않는다.
4주차에 id를 예제(`deviceNameEdit`, `autoSwitch`, `connectButton`)와 다르게 지었다면 내 id를 그대로 두고 두 View만 넣는다. 아래 코드의 `binding.deviceNameEdit`도 내 id로 맞춘다.

### 4. 먼저 잘못된 코드로 멈춤을 관찰하기

`MainActivity.kt`를 열고 `onCreate()`의 **마지막 `}` 바로 위**(4주차 자동 연결 Switch 코드 아래)에 아래 코드를 넣고 실행한다.

```kotlin
        binding.scanButton.setOnClickListener {
            binding.stateText.text = "검색 중…"
            Thread.sleep(5000)
            binding.stateText.text = "검색 완료"
        }
```

[검색]을 누르고 바로 Switch를 켜 본다.

- `검색 중…`은 **보이지 않는다.** 5초 동안 아무것도 바뀌지 않다가 `검색 완료`가 된다.
- 5초 동안 Switch가 움직이지 않는다. 5초가 지나면 그제야 켜진다.
- Logcat(태그 없이 `package:mine`)에 `Skipped 299 frames!  The application may be doing too much work on its main thread.`처럼 남는다(숫자는 실행마다 다르다).

이것이 메인 스레드를 막았을 때 생기는 일이다. 관찰이 끝나면 이 코드를 **지운다.** 5초를 넘기면 시스템이 ANR로 앱을 멈춰 세울 수 있다.

### 5. Thread와 runOnUiThread로 고치기

4단계의 코드를 지운 자리에 아래 코드를 넣는다.

```kotlin
        // 3. [검색] 버튼(5주차 1일차): 새 스레드에서 5초 기다린 뒤 메인 스레드에서 화면을 되돌린다.
        binding.scanButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            binding.scanButton.isEnabled = false
            binding.stateText.text = "검색 중…"
            Thread {
                Thread.sleep(5000)
                runOnUiThread {
                    binding.stateText.text = "검색 완료: $name"
                    binding.scanButton.isEnabled = true
                    Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
                }
            }.start()
        }
```

`Toast`가 빨간색이면 그 글자에 커서를 두고 **Alt+Enter**(맥은 ⌥+Enter) → **Import class**를 고른다. 4주차 코드에 이미 있으면 그대로 된다. `Thread`는 import가 필요 없다.

장치 이름에 `ESP32_BLE`를 입력하고 [검색]을 누른다.

| 때 | 화면 |
|---|---|
| 누른 직후 | [검색]이 회색(비활성)이 되고 `검색 중…`이 **바로** 보인다. Switch·[연결]은 눌린다 |
| 5초 뒤 | `검색 완료: ESP32_BLE`, [검색] 복구, Toast `검색 완료` |

- `Thread { … }.start()`: 중괄호 안의 일을 **새 스레드**에서 한다. 여기서 5초를 기다려도 화면은 멈추지 않는다.
- `runOnUiThread { … }`: 화면을 바꾸는 일을 **메인 스레드**에 넘긴다. 이 안에서만 `binding.…`을 만진다.
- `val name`은 람다 바깥에서 만들었지만 5초 뒤에 실행되는 `runOnUiThread { }` 안에서 그대로 쓸 수 있다(오늘 문법).
- `.start()`를 빠뜨리면 오류 없이 빌드되지만 스레드가 시작되지 않아 `검색 중…`에서 영원히 멈춘다.

### 6. 워커 스레드에서 View를 만지면 (관찰만)

5단계 코드에서 `runOnUiThread {`와 그 짝 `}` 두 줄만 지우고 실행해 [검색]을 누른다. 5초 뒤 앱이 꺼지고 Logcat에 이렇게 남는다.

```text
FATAL EXCEPTION: Thread-2
android.view.ViewRootImpl$CalledFromWrongThreadException: Only the original thread that created a view hierarchy can touch its views. Expected: main Calling: Thread-2
```

View는 메인 스레드만 바꿀 수 있다. 관찰이 끝나면 두 줄을 되살린다(Ctrl+Z 두 번, 맥은 ⌘+Z).

### 7. 1일차 완성 코드

완성한 `MainActivity.kt` 전체는 아래와 같다. 4주차 코드([연결] 버튼, 자동 연결 Switch)는 그대로이고 그 아래 [검색] 블록이 더해졌다.
같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

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

        // 3. [검색] 버튼(5주차 1일차): 새 스레드에서 5초 기다린 뒤 메인 스레드에서 화면을 되돌린다.
        binding.scanButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            binding.scanButton.isEnabled = false
            binding.stateText.text = "검색 중…"
            Thread {
                Thread.sleep(5000)
                runOnUiThread {
                    binding.stateText.text = "검색 완료: $name"
                    binding.scanButton.isEnabled = true
                    Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
                }
            }.start()
        }
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 4주차 코드가 예제와 조금 달라도 [검색] 부분만 같으면 된다.

### 8. 캡처하고 보관하기

`검색 중…`이 보이고 [검색]이 회색인 화면을 캡처한다. 2일차에는 같은 프로젝트를 다시 연다.

## 2일차

### 9. [중지] 버튼과 ProgressBar 배치하기

`activity_main.xml`에서 1일차에 넣은 [검색] `Button` 하나를 아래 코드로 **바꾼다.** [검색] 옆에 [중지]가 놓이고 그 아래 ProgressBar가 숨어 있다.

```xml
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
```

바꾼 뒤 전체는 아래와 같다. 같은 코드가 [examples/day2/activity_main.xml](examples/day2/activity_main.xml)에 있다.

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

실행하면 [검색] [중지]가 나란히 보이고 [중지]는 회색이다. ProgressBar는 `visibility="gone"`이라 보이지 않는다.
버튼 두 개가 옆으로 놓인 것은 2주차처럼 `horizontal` LinearLayout으로 감쌌기 때문이다.

### 10. Handler 만들기

`MainActivity.kt`에서 `private lateinit var binding: ActivityMainBinding` 줄 **아래**에 두 줄을 넣는다. `onCreate()` 바깥, 클래스 안이다.

```kotlin
    // 5주차 2일차: 메인 스레드의 메시지 큐에 "나중에 할 일"을 넣어 주는 Handler
    private val handler = Handler(Looper.getMainLooper())
```

`Handler`가 빨간색이면 Alt+Enter → Import class에서 **`android.os.Handler`** 를 고른다. 목록에 `java.util.logging.Handler`도 나오는데 그것을 고르면 빌드가 되지 않는다.
`Looper`도 같은 방법으로 `android.os.Looper`를 import한다.

### 11. 검색 끝에 할 일에 이름 붙이기

`onCreate()` 안에서 1일차에 넣은 `binding.scanButton.setOnClickListener { … }` 블록을 **통째로 지우고**, 그 자리에 아래 코드를 넣는다.

```kotlin
        // 3. 검색이 끝났을 때 할 일(5주차 2일차). 이름을 붙여 두어야 [중지]에서 취소할 수 있다.
        val finishScan = Runnable {
            binding.stateText.text = "검색 완료"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
            Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
        }
```

`View`가 빨간색이면 Alt+Enter → **`android.view.View`** 를 import한다. `Runnable`은 import가 필요 없다.

- `Runnable { … }`: 나중에 실행할 코드 묶음에 `finishScan`이라는 이름을 붙인 것이다. 아직 실행되지 않는다.
- `visibility = View.GONE`: ProgressBar를 숨기고 자리도 없앤다. `View.VISIBLE`이면 보인다.

### 12. [검색]으로 예약하고 [중지]로 취소하기

11단계 코드 **아래**에 이어서 넣는다.

```kotlin
        // 4. [검색] 버튼: 검색 중 화면으로 바꾸고, 5초 뒤에 finishScan을 실행하도록 예약한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.stateText.text = "검색 중…"
            binding.scanProgress.visibility = View.VISIBLE
            handler.postDelayed(finishScan, 5000)
        }

        // 5. [중지] 버튼: 예약을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            handler.removeCallbacks(finishScan)
            binding.stateText.text = "검색 중지"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
```

실행하고 두 가지를 해 본다.

| 조작 | 화면 |
|---|---|
| [검색] | [검색] 회색, [중지] 활성, 돌아가는 원, `검색 중…` |
| 그대로 5초 | 원이 사라지고 `검색 완료`, Toast `검색 완료`, [검색] 복구 |
| [검색] → 2초 뒤 [중지] | 원이 사라지고 `검색 중지`, [검색] 복구. 5초가 지나도 `검색 완료`가 **뜨지 않는다** |

- `postDelayed(finishScan, 5000)`: 5000ms 뒤에 `finishScan`을 실행하라고 메인 스레드의 큐에 넣는다. `Thread`도 `runOnUiThread`도 필요 없다.
- `removeCallbacks(finishScan)`: 아직 실행되지 않은 `finishScan` 예약을 큐에서 뺀다. **같은 이름**을 넘겨야 취소된다.

### 13. 2일차 완성 코드

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 5주차 2일차: 메인 스레드의 메시지 큐에 "나중에 할 일"을 넣어 주는 Handler
    private val handler = Handler(Looper.getMainLooper())

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

        // 3. 검색이 끝났을 때 할 일(5주차 2일차). 이름을 붙여 두어야 [중지]에서 취소할 수 있다.
        val finishScan = Runnable {
            binding.stateText.text = "검색 완료"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
            Toast.makeText(this, "검색 완료", Toast.LENGTH_SHORT).show()
        }

        // 4. [검색] 버튼: 검색 중 화면으로 바꾸고, 5초 뒤에 finishScan을 실행하도록 예약한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.stateText.text = "검색 중…"
            binding.scanProgress.visibility = View.VISIBLE
            handler.postDelayed(finishScan, 5000)
        }

        // 5. [중지] 버튼: 예약을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            handler.removeCallbacks(finishScan)
            binding.stateText.text = "검색 중지"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
    }
}
```

`import android.os.Handler`, `import android.os.Looper`, `import android.view.View` 세 줄이 새로 생겼다. 다른 것을 import했다면 이 세 줄로 고친다.

### 14. 제출하기

캡처 2장을 만든다.

1. [검색]을 누른 직후: [검색] 회색, [중지] 활성, 돌아가는 원, `검색 중…`
2. 5초 뒤 `검색 완료` Toast가 보이는 화면, 또는 [중지]를 누른 뒤 `검색 중지` 화면

제출물은 `MainActivity.kt`, `activity_main.xml`, 캡처 2장이다.
파일은 Project 창에서 오른쪽 클릭 → **Open In › Finder**(Windows는 **Explorer**)로 찾는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 요청한다.

## 부록 — 4주차에서 그대로 쓰는 파일

이번 주에는 고치지 않는다. 4주차 `examples/day2`와 같은 파일이며, 4주차 완성본을 받아 시작하는 학생은 아래 파일도 함께 넣는다.
`AndroidManifest.xml`은 4주차에 `ControlActivity`를 만들 때 자동으로 등록된 줄이 있는지만 확인한다(아이콘 줄이 빠진 예제용 축약본이므로 내 것을 그대로 두어도 된다).

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml)

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

`res/values/themes.xml` — [examples/day1/res/values/themes.xml](examples/day1/res/values/themes.xml). 프로젝트를 만들 때 생긴 파일이며 예제 빌드용으로 함께 둔다. 내 것을 그대로 둔다.

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
