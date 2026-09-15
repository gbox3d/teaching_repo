# 10주차 따라하기 — 배터리 방송과 BLE 권한

7주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
7주차 프로젝트가 없거나 실행되지 않으면 강의자에게 7주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에 고치는 파일은 `MainActivity.kt`, `activity_main.xml`, `strings.xml`(1·2일차)과 `AndroidManifest.xml`(2일차)이고, 2일차에 `Permissions.kt`를 새로 붙여 넣는다.
`ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`은 7주차 그대로 둔다. 전체 내용은 [7단계](#7-바꾸지-않는-파일-확인하기)에 있다.

## 1일차

### 1. 7주차 프로젝트 열고 실행하기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 연결 화면에 아래가 보이면 시작할 수 있다. [검색]만 켜져 있고 [중지]·[해제]는 회색이다.

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
연결 안 됨
[연결]
```

3. [검색]을 한 번 눌러 `연결 중… 5` → … → `준비됨` 또는 `끊김`까지 7주차처럼 바뀌는지 본다. 확인했으면 [해제]나 [다시 시도]로 정리하지 않아도 된다.

### 2. 배터리 글자 자리 만들기

1. `app › res › values › strings.xml`의 `disconnect` 줄 **아래**(`</resources>` 바로 위)에 한 줄을 넣는다.

```xml
    <string name="battery_unknown">배터리 ?</string>
```

전체는 아래와 같다. 같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

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
    <string name="disconnect">해제</string>
    <string name="battery_unknown">배터리 ?</string>
</resources>
```

2. `app › res › layout › activity_main.xml`의 `retryButton` **아래**, 마지막 `</LinearLayout>` 바로 위에 TextView를 넣는다.

```xml
    <TextView
        android:id="@+id/batteryText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/battery_unknown"
        android:textSize="16sp" />
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

    <TextView
        android:id="@+id/batteryText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/battery_unknown"
        android:textSize="16sp" />

</LinearLayout>
```

3. 실행한다. [연결] 버튼 아래(화면 맨 아래)에 `배터리 ?`가 보이면 성공이다. 아직 코드가 없으므로 글자는 바뀌지 않는다.

`id` 이름 `batteryText`는 다음 단계 Kotlin 코드의 `binding.batteryText`와 글자까지 같아야 한다.

### 3. batteryReceiver 만들기

1. `MainActivity.kt`를 열고 클래스 안, `private val viewModel: ConnViewModel by viewModels()` 줄 **아래**에 한 줄을 비우고 아래 블록을 넣는다. `onCreate` **밖**이다.

```kotlin
    // 10주차 1일차: 배터리 방송을 받는 Receiver. object : BroadcastReceiver() { … } 틀을 그대로 복사해 쓴다.
    // 방송이 오면 onReceive가 불리고, 함께 온 intent 안의 값(extras)으로 배터리 문구를 만든다.
    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            // 남은 양(level). intent가 null이거나 값이 없으면 -1이 된다.
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            // 가득 찼을 때의 값(scale). 보통 100이다. 없으면 100으로 본다.
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
            // 충전기 연결(plugged). 0이면 빠져 있고, 0이 아니면(AC·USB·무선) 꽂혀 있다.
            val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
            if (level == -1) {
                return
            }
            val percent = level * 100 / scale
            val charging = if (plugged != 0) "충전 중" else "충전 안 함"
            binding.batteryText.text = "배터리 $percent% · $charging"
        }
    }
```

2. 빨간 글자를 차례로 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `BroadcastReceiver` | `android.content.BroadcastReceiver` |
| `Context` | `android.content.Context` |
| `BatteryManager` | `android.os.BatteryManager` |

`Intent`는 4주차에 이미 import했다. 빨간색이면 `android.content.Intent`를 가져온다.

3. 실행한다. 화면은 2단계와 같이 `배터리 ?`다. Receiver를 **만들기만** 하고 아직 등록하지 않아서 방송을 받지 않는다.

- `object : BroadcastReceiver() { … }`: 이름 없는 Receiver 하나를 만들어 `batteryReceiver`에 담는 틀이다. 틀 부분은 그대로 복사하고 `onReceive` 안만 채운다.
- `intent?.getIntExtra(이름, 기본값) ?: 기본값`: `intent`가 `Intent?`(비어 있을 수 있음)라서 3주차의 `?.`와 `?:`를 쓴다. 4주차 `getStringExtra(…) ?: ""`의 정수 판이다.
- `if (plugged != 0) "충전 중" else "충전 안 함"`: `!=`는 "같지 않으면"이다. 1주차 `if … else` 한 줄과 같은 모양이다.
- `level * 100 / scale`: 정수끼리 나누면 소수점 아래는 버린다. `scale`이 100이면 `level` 그대로다.

### 4. onStart에서 등록하고 onStop에서 해제하기

1. `onCreate`를 닫는 `}`(`// 9.` 틀 바로 다음 줄) **아래**, 클래스의 마지막 `}` **위**에 두 함수를 넣는다.

```kotlin
    // 10. 화면이 보이기 시작하면 배터리 방송을 받도록 등록한다. 등록하자마자 마지막 배터리 값이 한 번 온다(10주차 1일차).
    override fun onStart() {
        super.onStart()
        ContextCompat.registerReceiver(
            this,
            batteryReceiver,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
    }

    // 11. 화면이 안 보이게 되면 등록을 푼다. onStart의 등록과 반드시 짝을 맞춘다(10주차 1일차).
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
    }
```

2. 빨간 글자를 Alt+Enter로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `ContextCompat` | `androidx.core.content.ContextCompat` |
| `IntentFilter` | `android.content.IntentFilter` |

3. 실행한다. 아주 잠깐 `배터리 ?`가 보였다가 곧바로 `배터리 100% · 충전 중`으로 바뀌면 성공이다(에뮬레이터 처음 값은 100%, AC charger).

- `onStart`·`onStop`은 3주차 생명주기 콜백이다. `onCreate` 안에 넣으면 빨간 줄이 생긴다. 반드시 `onCreate`를 닫는 `}` 아래에 둔다.
- `IntentFilter(Intent.ACTION_BATTERY_CHANGED)`: 여러 방송 가운데 "배터리가 바뀌었다" 방송만 골라 받는다.
- `RECEIVER_NOT_EXPORTED`: 다른 앱이 보낸 방송은 받지 않는다. 배터리 방송은 시스템이 보내므로 받는다.
- `ACTION_BATTERY_CHANGED`는 등록하자마자 마지막 값이 한 번 전달된다. 그래서 앱을 켜자마자 숫자가 보인다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

    // 10주차 1일차: 배터리 방송을 받는 Receiver. object : BroadcastReceiver() { … } 틀을 그대로 복사해 쓴다.
    // 방송이 오면 onReceive가 불리고, 함께 온 intent 안의 값(extras)으로 배터리 문구를 만든다.
    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            // 남은 양(level). intent가 null이거나 값이 없으면 -1이 된다.
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            // 가득 찼을 때의 값(scale). 보통 100이다. 없으면 100으로 본다.
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
            // 충전기 연결(plugged). 0이면 빠져 있고, 0이 아니면(AC·USB·무선) 꽂혀 있다.
            val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
            if (level == -1) {
                return
            }
            val percent = level * 100 / scale
            val charging = if (plugged != 0) "충전 중" else "충전 안 함"
            binding.batteryText.text = "배터리 $percent% · $charging"
        }
    }

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
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            viewModel.disconnect()
        }

        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            binding.stopButton.isEnabled = true
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }

        // 9. 남은 초를 받아 "연결 중… 3"처럼 붙여 보여 준다. 7번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        //    반드시 7번 틀 아래에 둔다. 7번이 "연결 중"을 먼저 쓰고 9번이 숫자를 붙여야 회전 뒤에도 숫자가 보인다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    if (seconds > 0) {
                        binding.stateText.text = "연결 중… $seconds"
                    }
                }
            }
        }
    }

    // 10. 화면이 보이기 시작하면 배터리 방송을 받도록 등록한다. 등록하자마자 마지막 배터리 값이 한 번 온다(10주차 1일차).
    override fun onStart() {
        super.onStart()
        ContextCompat.registerReceiver(
            this,
            batteryReceiver,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
    }

    // 11. 화면이 안 보이게 되면 등록을 푼다. onStart의 등록과 반드시 짝을 맞춘다(10주차 1일차).
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
7주차 코드(주석 1~9)가 내 코드와 조금 달라도 동작이 같으면 그대로 둔다.

### 5. 에뮬레이터에서 배터리 바꿔 보기

에뮬레이터 창 옆 도구 막대의 **⋯**(Extended controls)를 누르고 왼쪽 목록에서 **Battery**를 고른다.

| 조작 | 연결 화면 맨 아래 |
|---|---|
| Charge level 슬라이더를 80으로 | `배터리 80% · 충전 중` |
| Charger connection을 `None`으로 | `배터리 80% · 충전 안 함` |
| Charger connection을 다시 `AC charger`로 | `배터리 80% · 충전 중` |
| 홈 버튼 → 슬라이더를 50으로 → 앱으로 돌아오기 | 돌아오자마자 `배터리 50% · …` |
| 장치 이름을 넣고 [연결] → 제어 화면에서 [뒤로] | 연결 화면에 돌아오자마자 현재 값 |

홈으로 나가면 `onStop`에서 해제되고, 돌아오면 `onStart`에서 다시 등록되어 마지막 값이 곧바로 온다.
7주차 [검색] → `준비됨` 흐름과 Logcat `tag:Conn` 로그는 그대로다. 이번 주에는 새 로그를 찍지 않는다.

### 6. 캡처하고 보관하기

Charge level을 100이 아닌 값(예: 80)으로 바꾼 뒤 **세로 화면**에서 연결 화면을 캡처한다. Extended controls 창의 Charge level이 함께 보이면 더 좋다. **이 화면이 제출 캡처 1이다.**

- 연결 화면은 스크롤이 없어서 가로로 돌리면 맨 아래 배터리 문구가 잘려 안 보일 수 있다. 캡처는 세로에서 한다.
- 프로젝트는 2일차에 그대로 이어서 쓴다.

### 7. 바꾸지 않는 파일 확인하기

아래 파일은 7주차에 만든 그대로이며 이번 주 1일차에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.
같은 코드가 [examples/day1](examples/day1)에 있다. `AndroidManifest.xml`을 뺀 나머지는 2일차에도 바꾸지 않는다.

`ConnState.kt` — [examples/day1/ConnState.kt](examples/day1/ConnState.kt)

```kotlin
package com.example.smartio

// 1. 연결 상태를 나타내는 한글 문자열 모음. 화면의 TextView에 그대로 넣어 보여 준다(7주차 2일차).
// 12주차 bleuno 라이브러리의 ConnState와 이름·값이 같다. 12주차에는 이 파일 대신 import만 바꾼다.
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 [중지]·[해제]를 누른 뒤
    const val CONNECTING = "연결 중"        // 5초를 세는 중
    const val DISCOVERING = "서비스 확인 중" // 가짜 연결(2초)을 기다리는 중
    const val READY = "준비됨"              // 연결 성공
    const val LOST = "끊김"                 // 연결 실패
}
```

`ConnViewModel.kt` — [examples/day1/ConnViewModel.kt](examples/day1/ConnViewModel.kt)

```kotlin
package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 연결 상태와 카운트다운 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(7주차 2일차).
    private val _state = MutableStateFlow(ConnState.DISCONNECTED)
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null

    // 3. [검색]: 연결 중으로 바꾸고 5초를 센 뒤 가짜 연결을 시도한다. 값은 _state·_seconds에 넣는다(7주차 2일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다(7주차 1일차).
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            _state.value = ConnState.CONNECTING
            for (i in 5 downTo 1) {
                Log.d("Conn", "연결 중… $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            tryConnect()
        }
    }

    // 4. [중지]: 카운트다운 코루틴을 취소하고 연결 안 됨으로 돌린다(7주차 2일차).
    fun stopScan() {
        scanJob?.cancel()
        _seconds.value = 0
        _state.value = ConnState.DISCONNECTED
    }

    // 5. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }

    // 6. [해제]: 연결 안 됨으로 돌린다(7주차 2일차).
    fun disconnect() {
        _state.value = ConnState.DISCONNECTED
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과 상태를 _state에 넣는다.
    private suspend fun tryConnect() {
        _state.value = ConnState.DISCOVERING
        try {
            connectFake()
            _state.value = ConnState.READY
        } catch (e: Exception) {
            _state.value = ConnState.LOST
        }
        Log.d("Conn", _state.value)
    }
}
```

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). `ControlActivity` 줄이 있는지만 본다. 내 파일에는 아이콘 등의 줄이 더 있다. **Receiver는 Manifest에 적지 않는다.** 코드(`onStart`)에서 등록했기 때문이다.

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

### 8. [권한 확인] 버튼 추가하기

1. `strings.xml`의 `battery_unknown` 줄 **아래**에 한 줄을 넣는다.

```xml
    <string name="check_permission">권한 확인</string>
```

전체는 아래와 같다. 같은 코드가 [examples/day2/strings.xml](examples/day2/strings.xml)에 있다.

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
    <string name="disconnect">해제</string>
    <string name="battery_unknown">배터리 ?</string>
    <string name="check_permission">권한 확인</string>
</resources>
```

2. `activity_main.xml`에서 `retryButton` **아래**, `batteryText` **위**에 버튼을 넣는다. 배터리 문구는 계속 맨 아래에 남는다.

```xml
    <Button
        android:id="@+id/permissionButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/check_permission" />
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

    <Button
        android:id="@+id/permissionButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/check_permission" />

    <TextView
        android:id="@+id/batteryText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/battery_unknown"
        android:textSize="16sp" />

</LinearLayout>
```

3. 실행한다. [연결] 아래에 [권한 확인] 버튼, 그 아래에 배터리 문구가 보이면 성공이다. 아직 눌러도 아무 일이 없다.

### 9. Manifest에 권한 선언하기

`app › manifests › AndroidManifest.xml`을 연다.

1. 맨 위 `<manifest>` 태그에 `xmlns:tools="http://schemas.android.com/tools"`가 이미 있는지 먼저 본다. 새 프로젝트 템플릿에는 보통 들어 있으니 있으면 그대로 두고, 없을 때만 `xmlns:android="…"` 다음 줄, 태그를 닫는 `>` 앞에 한 줄 넣는다(아래 전체의 2~3행 모양). 두 번 넣으면 빌드 오류가 난다.
2. `<application` 줄 **위**에 `uses-feature` 하나와 `uses-permission` 다섯 개를 넣는다.
3. `<application>` 안(Activity 두 개)은 그대로 둔다. 내 파일에 아이콘 등의 줄이 더 있거나 `<application>` 태그에 `tools:targetApi="31"` 같은 줄이 있어도 지우지 않는다.

전체는 아래와 같다. 같은 코드가 [examples/day2/AndroidManifest.xml](examples/day2/AndroidManifest.xml)에 있다. 확인에 필요한 줄만 남긴 파일이라 내 파일보다 짧다.

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

4. 실행한다. 화면은 8단계와 같다. 선언은 "이 권한을 쓸 수 있다"는 표시일 뿐이고, 사용자에게 묻는 일은 코드가 한다.

| 선언 | 쓰는 Android 버전 | 실행 중에도 허락받나 |
|---|---|---|
| `BLUETOOTH_SCAN`(`neverForLocation`), `BLUETOOTH_CONNECT` | 12(API 31) 이상 | 받는다 |
| `BLUETOOTH`, `BLUETOOTH_ADMIN`(`maxSdkVersion="30"`) | 11(API 30) 이하 | 받지 않는다 |
| `ACCESS_FINE_LOCATION`(`maxSdkVersion="30"`) | 11(API 30) 이하 | 받는다 |
| `uses-feature` `bluetooth_le` | 모두 | 권한이 아니라 "BLE를 쓰는 앱"이라는 표시 |

- `tools:targetApi="s"`처럼 `tools:`로 시작하는 속성은 1번에서 확인한 `xmlns:tools` 줄이 있어야 쓸 수 있다.
- `neverForLocation`: 검색 결과로 위치를 알아내지 않는다는 표시다. `tools:targetApi="s"`: Android 12용 속성이라고 편집기에 알리는 표시다. 둘 다 외우지 않고 그대로 옮긴다.
- 이 선언은 12주차 `bleuno` 라이브러리를 쓸 때도 그대로 쓴다.

### 10. Permissions.kt 붙여 넣기

버전에 따라 요청할 권한을 고르는 함수는 **받아서 붙여 넣는다**.

1. Project 창 `app › kotlin+java › com.example.smartio`에서 오른쪽 클릭 → **New › Kotlin Class/File**을 누른다.
2. 목록에서 **File**(Class가 아니다)을 고르고 이름에 `Permissions`를 넣는다.
3. 생긴 파일의 내용을 모두 지우고 아래를 넣는다. 같은 코드가 [examples/day2/Permissions.kt](examples/day2/Permissions.kt)에 있다.

```kotlin
package com.example.smartio

import android.Manifest
import android.os.Build

// 1. BLE 장치를 찾고 연결하려면 실행 중에 허락받아야 하는 권한 목록을 돌려준다(10주차 2일차).
//    Android 12(API 31) 이상: BLUETOOTH_SCAN·BLUETOOTH_CONNECT, Android 11 이하: ACCESS_FINE_LOCATION.
//    같은 권한이라도 이름이 Android 버전마다 달라서 기기 버전(SDK_INT)을 보고 고른다.
fun blePermissions(): Array<String> {
    if (Build.VERSION.SDK_INT >= 31) {
        return arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        return arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
```

4. `Manifest`가 빨간색이면 Alt+Enter 목록에서 **`android.Manifest`**를 고른다(`java.util.jar.Manifest`가 아니다). `Build`는 `android.os.Build`다.
5. 실행한다. 화면은 그대로다. 빌드만 되면 된다.

- 클래스 없이 `fun` 하나만 든 파일이다. 같은 package(`com.example.smartio`) 어디서나 `blePermissions()`로 부른다.
- `Array<String>` / `arrayOf(…)`: 권한 이름(글자) 여러 개를 묶은 배열이다. 목록 문법은 11주차에 배운다.
- `return 값`: 7주차 `return`(그냥 끝내기)에 돌려줄 값을 붙인 모양이다. `fun blePermissions(): Array<String>`의 타입과 같은 값을 돌려준다.
- `Build.VERSION.SDK_INT`: 앱이 돌고 있는 기기의 Android 버전 번호다. 31이 Android 12다.

### 11. hasBlePermissions() 만들기

`MainActivity.kt`로 돌아와 `onStop()`의 닫는 `}` **아래**, 클래스의 마지막 `}` **위**에 함수를 넣는다.

```kotlin
    // 13. blePermissions()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    private fun hasBlePermissions(): Boolean {
        for (permission in blePermissions()) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        return true
    }
```

`PackageManager`가 빨간색이면 Alt+Enter로 `android.content.pm.PackageManager`를 가져온다. `ContextCompat`은 1일차에 이미 가져왔다.

실행한다. 화면은 그대로다. 아직 부르는 곳이 없어서 함수 이름이 회색으로 보여도 괜찮다.

- 주석 번호(12·13·14)는 완성 파일에 붙인 이름표라서 따라 넣는 순서와 다르다. 빨간 줄 없이 한 단계씩 실행해 볼 수 있게 **함수부터** 넣는다.
- `for (permission in blePermissions())`: 6주차 `for (i in 5 downTo 1)`이 숫자를 하나씩 바꿨다면, 이것은 묶음 안의 권한 이름을 하나씩 꺼낸다.
- 하나라도 `PERMISSION_GRANTED`(허용됨)가 아니면 그 자리에서 `return false`로 끝난다. 반복을 끝까지 통과하면 `return true`다.

### 12. showPermissionDialog() 만들기

`hasBlePermissions()` **아래**, 클래스의 마지막 `}` **위**에 거절했을 때 보여 줄 대화상자 함수를 넣는다.

```kotlin
    // 14. 거절했을 때 보여 주는 AlertDialog. [설정으로]를 누르면 이 앱의 정보(권한) 화면을 연다(10주차 2일차).
    private fun showPermissionDialog() {
        AlertDialog.Builder(this)
            .setTitle("권한이 필요합니다")
            .setMessage("장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.")
            .setPositiveButton("설정으로") { _, _ ->
                // 암시적 Intent: 무엇을 할지(ACTION)와 대상(package:앱 이름)만 적으면 시스템이 맞는 화면을 찾아 연다.
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
    }
```

빨간 글자를 Alt+Enter로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `AlertDialog` | `androidx.appcompat.app.AlertDialog` (`android.app.AlertDialog`가 아니다) |
| `Settings` | `android.provider.Settings` |
| `Uri` | `android.net.Uri` |

실행한다. 화면은 그대로다. 빌드만 되면 된다.

- `AlertDialog.Builder(this)` 뒤에 `.setTitle`·`.setMessage`·버튼 두 개를 점으로 이어 붙이고 마지막 `.show()`로 띄운다.
- `{ _, _ -> }`: 버튼을 누르면 실행되는 코드다. 넘어오는 값 두 개는 쓰지 않아서 4주차 `{ _, isChecked -> }`처럼 `_`로 둔다.
- `.setNegativeButton("취소", null)`: [취소]는 할 일이 없어서 `null`이다. 누르면 대화상자만 닫힌다.
- 암시적 Intent: 4주차 `Intent(this, ControlActivity::class.java)`는 열 화면을 직접 정했다. 이번에는 할 일(`ACTION_APPLICATION_DETAILS_SETTINGS`)과 대상(`package:com.example.smartio`)만 적고, 시스템이 설정 앱의 알맞은 화면을 연다.

### 13. permissionLauncher 만들기

클래스 안, `batteryReceiver` 블록을 닫는 `}` **아래**에 한 줄을 비우고 요청 틀을 넣는다. `onCreate` **밖**이다.

```kotlin
    // 10주차 2일차: 권한 요청 창을 띄우고 결과를 받는 틀. 화면이 시작되기 전에 만들어 두어야 하므로 클래스 안(onCreate 밖)에 둔다.
    // 사용자가 요청 창에서 고르면 { _ -> … }가 불린다. 넘어오는 결과는 쓰지 않고(_), 13번 함수로 지금 권한을 다시 확인한다.
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (hasBlePermissions()) {
            Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
    }
```

`ActivityResultContracts`가 빨간색이면 Alt+Enter로 `androidx.activity.result.contract.ActivityResultContracts`를 가져온다.

실행한다. 화면은 그대로다. 빌드만 되면 된다.

- `registerForActivityResult(…) { }`: 권한 요청 창을 띄울 준비를 해 두는 **틀**이다. 사용자가 창에서 [허용]이나 [허용 안함]을 고르면 중괄호 안이 실행된다.
- 이 틀은 반드시 클래스 변수 자리에서 만든다. 화면이 시작되기 전에 준비되어 있어야 하기 때문이다.
- `{ _ -> }`: 결과 묶음이 넘어오지만 읽지 않는다. 대신 11단계의 `hasBlePermissions()`로 "지금 허용됐나"를 다시 본다.

### 14. [권한 확인] 버튼에 연결하기

1. `onCreate` 안, `// 9.` 틀(`viewModel.seconds.collect`가 있는 블록)의 닫는 `}` **아래**, `onCreate`를 닫는 `}` **위**에 리스너를 넣는다.

```kotlin
        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            if (hasBlePermissions()) {
                Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
            } else {
                permissionLauncher.launch(blePermissions())
            }
        }
```

12번은 `onCreate` 안에 들어가므로 완성 파일에서는 `// 10.`(`onStart`)·`// 11.`(`onStop`)보다 **위**에 있다. 번호 순서대로 찾지 말고 위치 설명을 따른다.

2. 실행하고 [권한 확인]을 누른다. 권한 창의 문구와 버튼 이름은 OS 버전과 언어 설정에 따라 조금 다르다.

| 조작 | 화면 |
|---|---|
| 처음 [권한 확인] | 시스템 권한 창이 **한 번** 뜬다. Android 12 이상은 "근처 기기"를 찾고 연결하도록 허용할지 묻는다(SCAN·CONNECT가 같은 묶음이라 창이 하나다) |
| 권한 창에서 [허용] (영어 화면은 Allow) | Toast `권한 OK` |
| 그 뒤 다시 [권한 확인] | 창 없이 곧바로 Toast `권한 OK` |
| 권한 창에서 [허용 안함] (영어 화면은 Don't allow) | 대화상자 `권한이 필요합니다`와 [취소]·[설정으로] |
| 대화상자 [취소] | 대화상자만 닫힌다 |
| 대화상자 [설정으로] | 설정 앱의 `Smart I/O Controller` 앱 정보 화면 |
| 설정에서 권한 › 근처 기기 › 허용 → 뒤로 → [권한 확인] | Toast `권한 OK` |

- Android 11 이상에서는 같은 권한을 **두 번 거절**하면 그다음부터 권한 창이 뜨지 않는다. 그때는 [권한 확인]을 누르자마자 대화상자가 뜬다. 창 없이 곧바로 결과가 오고 `hasBlePermissions()`가 `false`이기 때문이다.
- 설정에서 이미 허용한 권한을 **다시 끄면** 시스템이 앱을 종료한다. 앱으로 돌아오면 처음부터 다시 시작해 `연결 안 됨`이 보이는 것이 정상이다.
- Android 11 이하 에뮬레이터에서는 권한 창이 "위치" 권한으로 뜬다. 흐름은 같다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.net.Uri
import android.os.BatteryManager
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

    // 10주차 1일차: 배터리 방송을 받는 Receiver. object : BroadcastReceiver() { … } 틀을 그대로 복사해 쓴다.
    // 방송이 오면 onReceive가 불리고, 함께 온 intent 안의 값(extras)으로 배터리 문구를 만든다.
    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            // 남은 양(level). intent가 null이거나 값이 없으면 -1이 된다.
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            // 가득 찼을 때의 값(scale). 보통 100이다. 없으면 100으로 본다.
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
            // 충전기 연결(plugged). 0이면 빠져 있고, 0이 아니면(AC·USB·무선) 꽂혀 있다.
            val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
            if (level == -1) {
                return
            }
            val percent = level * 100 / scale
            val charging = if (plugged != 0) "충전 중" else "충전 안 함"
            binding.batteryText.text = "배터리 $percent% · $charging"
        }
    }

    // 10주차 2일차: 권한 요청 창을 띄우고 결과를 받는 틀. 화면이 시작되기 전에 만들어 두어야 하므로 클래스 안(onCreate 밖)에 둔다.
    // 사용자가 요청 창에서 고르면 { _ -> … }가 불린다. 넘어오는 결과는 쓰지 않고(_), 13번 함수로 지금 권한을 다시 확인한다.
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (hasBlePermissions()) {
            Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
    }

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
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            viewModel.disconnect()
        }

        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            binding.stopButton.isEnabled = true
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }

        // 9. 남은 초를 받아 "연결 중… 3"처럼 붙여 보여 준다. 7번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        //    반드시 7번 틀 아래에 둔다. 7번이 "연결 중"을 먼저 쓰고 9번이 숫자를 붙여야 회전 뒤에도 숫자가 보인다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    if (seconds > 0) {
                        binding.stateText.text = "연결 중… $seconds"
                    }
                }
            }
        }

        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            if (hasBlePermissions()) {
                Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
            } else {
                permissionLauncher.launch(blePermissions())
            }
        }
    }

    // 10. 화면이 보이기 시작하면 배터리 방송을 받도록 등록한다. 등록하자마자 마지막 배터리 값이 한 번 온다(10주차 1일차).
    override fun onStart() {
        super.onStart()
        ContextCompat.registerReceiver(
            this,
            batteryReceiver,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
    }

    // 11. 화면이 안 보이게 되면 등록을 푼다. onStart의 등록과 반드시 짝을 맞춘다(10주차 1일차).
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
    }

    // 13. blePermissions()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    private fun hasBlePermissions(): Boolean {
        for (permission in blePermissions()) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        return true
    }

    // 14. 거절했을 때 보여 주는 AlertDialog. [설정으로]를 누르면 이 앱의 정보(권한) 화면을 연다(10주차 2일차).
    private fun showPermissionDialog() {
        AlertDialog.Builder(this)
            .setTitle("권한이 필요합니다")
            .setMessage("장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.")
            .setPositiveButton("설정으로") { _, _ ->
                // 암시적 Intent: 무엇을 할지(ACTION)와 대상(package:앱 이름)만 적으면 시스템이 맞는 화면을 찾아 연다.
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
    }
}
```

### 15. 거절 대화상자와 설정 화면 캡처하기

1. 권한 창에서 [허용 안함]을 누른 직후 `권한이 필요합니다` 대화상자가 떠 있는 연결 화면을 캡처한다. **제출 캡처 2다.**
2. 대화상자의 [설정으로]를 누르고, 열린 앱 정보 화면(`Smart I/O Controller`가 보이는 화면)을 캡처한다. 권한 항목까지 들어가 "근처 기기"가 보이면 더 좋다. **제출 캡처 3이다.**

이미 [허용]을 눌러 대화상자를 만들 수 없으면, 설정 › 앱 › Smart I/O Controller › 권한 › 근처 기기 › **허용 안함**으로 되돌린 뒤 앱을 다시 실행하고 [권한 확인]을 누른다.

- 대화상자가 뜬 채로 화면을 돌리면 대화상자는 사라진다. [권한 확인]을 다시 누르면 된다. 캡처는 세로에서 한다.
- 설정 화면에 갔다 오면 `onStop` → `onStart`가 돌아 배터리 문구도 곧바로 새 값으로 바뀐다.

### 16. 제출하기

제출물은 네 가지다.

1. `MainActivity.kt`, `AndroidManifest.xml`
2. 캡처 1: Battery 값을 바꾼 뒤 배터리 문구가 보이는 연결 화면(1일차 6단계)
3. 캡처 2: 권한을 거절한 뒤 뜬 `권한이 필요합니다` 대화상자
4. 캡처 3: [설정으로]로 열린 `Smart I/O Controller` 앱 정보 화면

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
