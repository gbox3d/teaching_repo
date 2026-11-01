# 9주차 따라하기 — LogService 넣기와 Fragment 바꿔 끼우기

이번 주 따라하기는 두 갈래다. 1일차는 7주차까지 만든 `SmartIO`에 `LogService`를 넣어 버튼으로 시작·중지하고, 2일차는 새 연습 프로젝트에서 조각을 바꿔 끼운다.
각 단계의 결과가 화면이나 Logcat에 보이면 다음 단계로 넘어간다.

| 일차 | 만드는 것 | 시작점 | 예제 |
|---|---|---|---|
| 1일차 (1~7단계) | `SmartIO`에 `LogService`와 [서비스 시작]·[서비스 중지] | 7주차까지 만든 `SmartIO`. 없으면 7주차 완성본 | [examples/day1](examples/day1) |
| 2일차 (8~13단계) | 조각 두 개를 바꿔 끼우는 `FragmentDemo` | 새 프로젝트 | [examples/day2](examples/day2) |

1일차에 넣은 `LogService.kt`와 버튼 두 개는 10주차 이후 예제에 들어가지 않는다. 10주차는 7주차 완성본에서 다시 시작하므로 남겨 두어도 되고 확인한 뒤 지워도 된다.
2일차 `FragmentDemo`는 `SmartIO`와 섞지 않는 별도 프로젝트다.

## 1일차

### 1. SmartIO 열고 실행하기

1. Android Studio에서 7주차까지 만든 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 연결 화면에 아래가 보이면 시작할 수 있다. [검색]을 눌러 `연결 중… 5`부터 세는지도 한 번 본다.

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
연결 안 됨
[연결]
```

이번 1일차에 고치는 파일은 `LogService.kt`(새 파일), `AndroidManifest.xml`, `strings.xml`, `activity_main.xml`, `MainActivity.kt` 다섯 개다.
`ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`은 7주차 그대로 둔다. 전체 내용은 [7단계](#7-바꾸지-않는-파일-확인하기)에 있다.

### 2. LogService.kt 만들기

1. Project 창에서 `app › kotlin+java › com.example.smartio` 폴더를 **오른쪽 클릭** → **New › Kotlin Class/File**을 고른다.
2. 목록에서 **Class**를 고르고 이름에 `LogService`를 넣은 뒤 Enter를 누른다.
3. 생긴 파일의 내용을 모두 지우고 아래 코드로 바꾼다. 같은 코드가 [examples/day1/LogService.kt](examples/day1/LogService.kt)에 있다.

```kotlin
package com.example.smartio

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log

// 9주차 1일차: 화면 없이 일을 맡는 started Service. 따로 스레드를 만들지 않으면 메인 스레드에서 돈다.
class LogService : Service() {

    // 1. startService를 부를 때마다 불린다. 어느 스레드에서 도는지 Logcat에 남긴다(9주차 1일차).
    //    Service도 메인 스레드에서 돌므로 여기서 오래 걸리는 일을 하면 화면이 멈춘다. 5주차 Thread.sleep 시연과 같다.
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        // 2. 시스템이 이 Service를 강제로 끝내도 다시 살리지 않는다(9주차 1일차).
        return START_NOT_STICKY
    }

    // 3. stopService로 멈추면 불린다(9주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        Log.d("Service", "onDestroy")
    }

    // 4. 화면과 묶어 쓰는(bound) Service가 아니므로 null을 돌려준다. 빼면 빌드가 안 되는 틀이다(9주차 1일차).
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
```

4. import 네 줄은 코드에 들어 있다. 붙여 넣은 뒤에도 빨간 글자가 있으면 그 글자에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `Service` | `android.app.Service` |
| `Intent` | `android.content.Intent` |
| `IBinder` | `android.os.IBinder` |
| `Log` | `android.util.Log` |

- `class LogService : Service()`: 7주차 `ConnViewModel : ViewModel()`처럼 `Service`를 물려받는다. 화면(layout)이 없다.
- `onStartCommand`: `startService`를 부를 **때마다** 불린다. `Thread.currentThread().name`은 지금 이 코드가 도는 스레드 이름이다.
- `return START_NOT_STICKY`: 시스템이 이 Service를 끝내도 다시 살리지 않는다는 표시다. 이 한 줄은 틀로 쓴다.
- `onBind`: 화면과 묶어 쓰는 Service가 아니므로 `null`을 돌려준다. 빼면 빌드가 안 되는 틀이다.

**New › Service › Service** 메뉴로 만들어도 된다. 그때는 Manifest 줄이 자동으로 생기지만 모양이 조금 달라서 세 곳을 고쳐야 한다.
Manifest의 `android:exported="true"`를 `"false"`로, 클래스의 `onBind(intent: Intent): IBinder`를 `onBind(intent: Intent?): IBinder?`로, 본문의 `TODO(…)`를 `return null`로 바꾼다.
반환형의 `?`를 빼먹으면 `Null cannot be a value of a non-null type 'android.os.IBinder'.` 오류가 난다(3주차 null 안전성).

### 3. Manifest에 service 적기

Service도 Activity처럼 Manifest에 적어야 시작된다. 2단계를 **Kotlin Class/File**로 했다면 직접 적는다.

1. `app › manifests › AndroidManifest.xml`을 연다.
2. `MainActivity`의 `</activity>` **아래**, `</application>` **위**에 아래 네 줄을 넣는다.

```xml
        <!-- 9주차 1일차: Service도 Activity처럼 여기에 적어야 시작된다. exported="false"는 이 앱 안에서만 쓴다는 뜻이다. -->
        <service
            android:name=".LogService"
            android:exported="false" />
```

전체는 아래와 같다. 같은 코드가 [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml)에 있다. 내 파일에는 아이콘 등의 줄이 더 있어도 된다.

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

        <!-- 9주차 1일차: Service도 Activity처럼 여기에 적어야 시작된다. exported="false"는 이 앱 안에서만 쓴다는 뜻이다. -->
        <service
            android:name=".LogService"
            android:exported="false" />

    </application>

</manifest>
```

- `android:name=".LogService"`: 앞의 점은 "이 앱 package 안의" 라는 뜻이다. 4주차 `.ControlActivity`와 같다.
- 실행하면 화면은 1단계와 같다. 아직 Service를 부르는 버튼이 없다.

### 4. 버튼 두 개 추가하기

1. `app › res › values › strings.xml`에서 `disconnect` 줄 **아래**, `</resources>` **위**에 두 줄을 넣는다.

```xml
    <string name="service_start">서비스 시작</string>
    <string name="service_stop">서비스 중지</string>
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
    <string name="service_start">서비스 시작</string>
    <string name="service_stop">서비스 중지</string>
</resources>
```

2. `app › res › layout › activity_main.xml`에서 [다시 시도] 버튼(`retryButton`) 블록 **아래**, 파일 맨 끝 `</LinearLayout>` **위**에 가로 줄 하나를 넣는다.

```xml
    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/serviceStartButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/service_start" />

        <Button
            android:id="@+id/serviceStopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:text="@string/service_stop" />

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

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/serviceStartButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/service_start" />

        <Button
            android:id="@+id/serviceStopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:text="@string/service_stop" />

    </LinearLayout>

</LinearLayout>
```

3. 실행한다. 화면 맨 아래에 [서비스 시작] [서비스 중지]가 보이면 성공이다. 아직 눌러도 아무 일이 없다.

```text
[검색] [중지] [해제]
연결 안 됨
[연결]
[서비스 시작] [서비스 중지]
```

폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있다. 이 화면은 가로에서 [서비스 시작]·[서비스 중지] 줄이 잘리거나 화면 밖으로 밀리고, `연결 중…`·`끊김`일 때는 [연결]·[다시 시도] 아래쪽도 잘린다. 1일차 확인은 세로로 하고, 확인할 항목이 안 보이면 세로로 되돌려 확인한다.
확인이 끝나면 이 가로 줄을 지워도 된다. 10주차는 7주차 완성본에서 다시 시작한다.

### 5. startService·stopService 연결하기

`MainActivity.kt`의 `onCreate()` 안, `// 9.` 남은 초 틀(`viewModel.seconds.collect`가 들어 있는 `lifecycleScope.launch { … }`)이 끝나는 `}` **아래**, `onCreate()`를 닫는 `}` **위**에 두 블록을 넣는다.

```kotlin
        // 10. [서비스 시작] 버튼: LogService를 시작한다. 누를 때마다 onStartCommand가 한 번씩 불린다(9주차 1일차).
        binding.serviceStartButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            startService(intent)
        }

        // 11. [서비스 중지] 버튼: LogService를 멈춘다. 돌고 있을 때만 onDestroy가 불린다(9주차 1일차).
        binding.serviceStopButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            stopService(intent)
        }
```

- 새 import는 없다. `Intent`는 4주차부터 import되어 있고, `LogService`는 같은 package라 import가 필요 없다.
- `LogService`가 빨간색이면 2단계의 클래스 이름 철자를 본다. `serviceStartButton`이 빨간색이면 4단계 XML id 철자를 본다.
- 모양은 4주차 [연결]의 `val intent = Intent(this, ControlActivity::class.java)` → `startActivity(intent)`와 같다. `startActivity` 자리에 `startService`·`stopService`가 들어갔다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
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

        // 10. [서비스 시작] 버튼: LogService를 시작한다. 누를 때마다 onStartCommand가 한 번씩 불린다(9주차 1일차).
        binding.serviceStartButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            startService(intent)
        }

        // 11. [서비스 중지] 버튼: LogService를 멈춘다. 돌고 있을 때만 onDestroy가 불린다(9주차 1일차).
        binding.serviceStopButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            stopService(intent)
        }
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. `// 1.`~`// 9.` 부분이 내 7주차 코드와 조금 달라도 동작이 같으면 그대로 둔다.

### 6. Logcat으로 스레드 이름 보고 캡처하기

1. 앱을 실행한 채로 아래쪽 **Logcat** 창을 열고 필터 칸에 `package:mine tag:Service`를 넣는다.
2. 아래 순서로 누르고 Logcat을 본다.

| 조작 | 화면 | Logcat `package:mine tag:Service` |
|---|---|---|
| [서비스 시작] | 바뀌지 않는다(Service는 화면이 없다) | `onStartCommand thread=main` |
| [서비스 시작] 한 번 더 | 바뀌지 않는다 | `onStartCommand thread=main` 한 줄이 더 찍힌다. 이미 돌고 있어도 누를 때마다 불린다 |
| [서비스 중지] | 바뀌지 않는다 | `onDestroy` |
| 멈춘 상태에서 [서비스 중지] 한 번 더 | 바뀌지 않는다 | 아무것도 찍히지 않는다 |
| [검색] 카운트다운 중 [서비스 시작] | 카운트다운이 끊기지 않는다 | `onStartCommand thread=main` |

- `thread=main`: 5주차에 본 메인 스레드와 같은 스레드다. **Service는 따로 스레드를 만들지 않는다.**
- 카운트다운이 끊기지 않은 것은 `onStartCommand`가 로그 한 줄만 찍고 곧바로 끝나기 때문이다. 여기서 오래 걸리는 일을 하면 5주차 `Thread.sleep` 시연처럼 화면이 멈춘다.
- Service가 돌고 있을 때 뒤로 가기로 앱을 닫으면 잠시 뒤 `onDestroy`가 찍힌다(Android 14 에뮬레이터에서 약 1분 뒤). Android 8 이상은 백그라운드로 간 앱의 Service를 멈춘다. 관찰은 앱을 연 채로 한다.

**캡처**: 표의 첫 세 줄을 채웠으면 Logcat 창을 **캡처 1장** 남긴다. `onStartCommand thread=main` 두 줄, `onDestroy` 한 줄, 스레드 이름이 모두 읽혀야 한다.

캡처에 계정 이름 같은 개인정보가 보이지 않는지 확인한다. 제출물은 [실습지의 제출](lab.md#제출--캡처-3장)에 있다.

### 7. 바꾸지 않는 파일 확인하기

아래 파일은 7주차에 만든 그대로이며 이번 주에는 손대지 않는다. 같은 코드가 [examples/day1](examples/day1)에 있다.

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

`res/values/themes.xml` — [examples/day1/res/values/themes.xml](examples/day1/res/values/themes.xml). 프로젝트를 만들 때 생긴 그대로다.

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

### 8. FragmentDemo 새 프로젝트 만들기

2일차는 `SmartIO`와 섞지 않고 작은 새 프로젝트로 한다. 1일차에 고친 `SmartIO`는 그대로 두고, 여기서 만드는 것은 조각을 바꿔 끼우는 연습용 앱이다.

1. **File › New › New Project** → **Phone and Tablet**에서 **Empty Views Activity** → **Next**.
2. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `FragmentDemo` |
| Package name | `com.example.fragmentdemo` |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |

3. 4주차 3단계처럼 `Gradle Scripts › build.gradle.kts (Module :app)`을 열어 `buildFeatures { viewBinding = true }`와 의존성 네 줄을 넣고 **Sync Now**를 누른다.
   Fragment는 `appcompat` 라이브러리에 함께 들어 있어서 따로 넣지 않는다. 검증에 쓴 전체 파일은 [examples/day2/build.gradle.kts](examples/day2/build.gradle.kts)이며 아래와 같다.

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.fragmentdemo"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.fragmentdemo"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    // ViewBinding을 켠다. 이 블록이 있어야 ActivityMainBinding이 만들어진다.
    buildFeatures {
        viewBinding = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    // 5~7주에 쓸 라이브러리. 지금 미리 넣어 둔다.
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
}
```

4. 실행해서 `Hello World!`가 보이면 다음으로 간다.

### 9. strings.xml과 activity_main.xml

1. `app › res › values › strings.xml` 전체를 아래로 바꾼다. 같은 코드가 [examples/day2/strings.xml](examples/day2/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Fragment Demo</string>
    <string name="first">첫 번째 조각</string>
    <string name="second">두 번째 조각</string>
    <string name="first_text">여기는 FirstFragment</string>
    <string name="second_text">여기는 SecondFragment</string>
</resources>
```

2. `app › res › layout › activity_main.xml`을 열고 오른쪽 위 **Code** 보기에서 전체를 아래로 바꾼다. 같은 코드가 [examples/day2/activity_main.xml](examples/day2/activity_main.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center_horizontal"
    android:orientation="vertical">

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/firstButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/first" />

        <Button
            android:id="@+id/secondButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:text="@string/second" />

    </LinearLayout>

    <!-- 조각(Fragment)을 끼울 빈 자리. 버튼을 누르면 이 안의 조각만 바뀌고 위의 버튼은 그대로다. -->
    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/fragmentContainer"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="16dp" />

</LinearLayout>
```

- `FragmentContainerView`: 조각(Fragment)을 끼울 빈 자리다. 지금은 비어 있다.
- `layout_height="0dp"` + `layout_weight="1"`: 버튼 줄을 뺀 남은 높이를 모두 차지한다(2주차 확장의 `layout_weight`).
- 루트의 `android:id="@+id/main"`은 템플릿의 insets 코드가 쓰므로 그대로 둔다.

3. 실행한다. 위에 [첫 번째 조각] [두 번째 조각]이 보이고 아래는 비어 있으면 성공이다.

### 10. 조각 layout 두 개 만들기

1. `app › res › layout` 폴더를 **오른쪽 클릭** → **New › Layout Resource File**.
2. File name에 `fragment_first`, Root element에 `LinearLayout`을 넣고 **OK**.
3. **Code** 보기에서 전체를 아래로 바꾼다. 같은 코드가 [examples/day2/fragment_first.xml](examples/day2/fragment_first.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/first_text"
        android:textSize="24sp"
        android:textStyle="bold" />

</LinearLayout>
```

4. 같은 방법으로 `fragment_second`를 만들고 전체를 아래로 바꾼다. 같은 코드가 [examples/day2/fragment_second.xml](examples/day2/fragment_second.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/second_text"
        android:textSize="24sp"
        android:textStyle="bold" />

</LinearLayout>
```

두 파일은 글자 `@string/first_text` / `@string/second_text` 한 곳만 다르다.

### 11. FirstFragment·SecondFragment 만들기

1. `app › kotlin+java › com.example.fragmentdemo`를 **오른쪽 클릭** → **New › Kotlin Class/File** → **Class** → 이름 `FirstFragment` → Enter.
2. 내용을 모두 지우고 아래로 바꾼다. 같은 코드가 [examples/day2/FirstFragment.kt](examples/day2/FirstFragment.kt)에 있다.

```kotlin
package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 2일차: Activity 안에 끼우는 화면 조각. 자기 layout(fragment_first.xml)을 가진다.
class FirstFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 2일차).
    //    Activity의 setContentView 대신 이 함수가 화면을 정한다.
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "FirstFragment onCreateView")
        return inflater.inflate(R.layout.fragment_first, container, false)
    }
}
```

3. 같은 방법으로 `SecondFragment`를 만들고 아래로 바꾼다. 같은 코드가 [examples/day2/SecondFragment.kt](examples/day2/SecondFragment.kt)에 있다.

```kotlin
package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 2일차: 두 번째 화면 조각. FirstFragment와 모양이 같고 layout만 다르다(fragment_second.xml).
class SecondFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 2일차).
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "SecondFragment onCreateView")
        return inflater.inflate(R.layout.fragment_second, container, false)
    }
}
```

4. `Fragment`가 빨간색이면 Alt+Enter(맥 ⌥+Enter) 목록에서 **`androidx.fragment.app.Fragment`**를 고른다. `android.app.Fragment`(옛 방식)를 고르지 않는다.

| 빨간 글자 | 가져올 import |
|---|---|
| `Fragment` | `androidx.fragment.app.Fragment` |
| `LayoutInflater`, `View`, `ViewGroup` | `android.view.LayoutInflater`, `android.view.View`, `android.view.ViewGroup` |
| `Log` | `android.util.Log` |

- `onCreateView`: 조각의 화면을 만들 때 불린다. `inflater.inflate(R.layout.fragment_first, container, false)`가 layout 파일을 View로 만들어 돌려준다. Activity의 `setContentView` 자리다.
- **New › Fragment › Fragment (Blank)** 메뉴로 만들면 `ARG_PARAM1`·`newInstance` 같은 줄이 함께 생긴다. 이번에는 쓰지 않으므로 위 코드로 전체를 바꾼다.

### 12. MainActivity에서 조각 끼우고 바꾸기

1. `MainActivity.kt`를 4주차 4단계처럼 ViewBinding 틀로 바꾼다. `class MainActivity : AppCompatActivity() {` 아랫줄에 아래 한 줄을 넣고,

```kotlin
    private lateinit var binding: ActivityMainBinding
```

   `setContentView(R.layout.activity_main)` 한 줄을 지운 자리에 아래 두 줄을 넣은 뒤, `findViewById(R.id.main)`을 `binding.main`으로 바꾼다.

```kotlin
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
```

   `ActivityMainBinding`이 빨간색이면 Alt+Enter → `com.example.fragmentdemo.databinding.ActivityMainBinding`.

2. `onCreate()` 안, insets 블록(`ViewCompat.setOnApplyWindowInsetsListener`)이 끝나는 `}` **아래**에 처음 조각을 끼우는 코드를 넣는다.

```kotlin
        // 1. 앱을 처음 켰을 때만 빈 자리에 FirstFragment를 끼운다(9주차 2일차).
        //    회전 뒤에는 savedInstanceState가 null이 아니고, 보고 있던 조각을 시스템이 되살려 준다(3주차 복원과 같은 원리).
        //    바꾸기는 세 줄이다: 바꾸기 시작(beginTransaction) → 자리에 조각 넣기(replace) → 확정(commit).
        if (savedInstanceState == null) {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }
```

3. 실행한다. 버튼 아래에 `여기는 FirstFragment`가 보이면 성공이다.
4. 그 아래, `onCreate()`를 닫는 `}` **위**에 버튼 두 개의 리스너를 넣는다.

```kotlin
        // 2. [첫 번째 조각] 버튼: 빈 자리의 조각을 FirstFragment로 바꾼다. 화면(Activity)은 그대로다(9주차 2일차).
        binding.firstButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 3. [두 번째 조각] 버튼: 빈 자리의 조각을 SecondFragment로 바꾼다. commit()을 빼면 아무것도 바뀌지 않는다(9주차 2일차).
        binding.secondButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, SecondFragment())
            transaction.commit()
        }
```

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.fragmentdemo

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.fragmentdemo.databinding.ActivityMainBinding

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

        // 1. 앱을 처음 켰을 때만 빈 자리에 FirstFragment를 끼운다(9주차 2일차).
        //    회전 뒤에는 savedInstanceState가 null이 아니고, 보고 있던 조각을 시스템이 되살려 준다(3주차 복원과 같은 원리).
        //    바꾸기는 세 줄이다: 바꾸기 시작(beginTransaction) → 자리에 조각 넣기(replace) → 확정(commit).
        if (savedInstanceState == null) {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 2. [첫 번째 조각] 버튼: 빈 자리의 조각을 FirstFragment로 바꾼다. 화면(Activity)은 그대로다(9주차 2일차).
        binding.firstButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 3. [두 번째 조각] 버튼: 빈 자리의 조각을 SecondFragment로 바꾼다. commit()을 빼면 아무것도 바뀌지 않는다(9주차 2일차).
        binding.secondButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, SecondFragment())
            transaction.commit()
        }
    }
}
```

5. 실행하고 Logcat 필터를 `package:mine tag:Fragment`로 바꾼 뒤 눌러 본다.

| 조작 | 화면 | Logcat `package:mine tag:Fragment` |
|---|---|---|
| 앱 시작 | 위에 [첫 번째 조각] [두 번째 조각], 가운데 `여기는 FirstFragment` | `FirstFragment onCreateView` |
| [두 번째 조각] | 버튼 줄은 그대로, 아래 글자만 `여기는 SecondFragment` | `SecondFragment onCreateView` |
| [첫 번째 조각] | `여기는 FirstFragment` | `FirstFragment onCreateView` |
| 같은 버튼을 두 번 | 글자는 같다 | 누를 때마다 한 줄씩 찍힌다(새 조각을 만들어 끼우기 때문) |
| SecondFragment를 보다가 회전 | 가로 화면에서도 `여기는 SecondFragment` | `SecondFragment onCreateView` 한 줄. `FirstFragment`는 찍히지 않는다 |
| 뒤로 가기 | 앱이 닫힌다 | 조각 단위로 뒤로 가지 않는다 |

- 버튼 줄은 Activity의 것이라 그대로 있고, `FragmentContainerView` 자리의 조각만 바뀐다.
- Manifest와 테마는 프로젝트를 만들 때 생긴 그대로다. Manifest에는 Fragment를 적지 않는다. 검증에 쓴 파일은 아래와 같고, 내 파일에는 아이콘 등의 줄이 더 있다.

`AndroidManifest.xml` — [examples/day2/AndroidManifest.xml](examples/day2/AndroidManifest.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:label="@string/app_name"
        android:theme="@style/Theme.FragmentDemo">

        <!-- Fragment는 Activity가 아니므로 여기에 적지 않는다. Activity 하나만 있다. -->
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

`res/values/themes.xml` — [examples/day2/res/values/themes.xml](examples/day2/res/values/themes.xml)

```xml
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Base.Theme.FragmentDemo" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your light theme here. -->
        <!-- <item name="colorPrimary">@color/my_light_primary</item> -->
    </style>

    <style name="Theme.FragmentDemo" parent="Base.Theme.FragmentDemo" />
</resources>
```

### 13. 조각을 바꿔 보고 캡처 두 장 찍기

1. 앱을 켠 채 [두 번째 조각]과 [첫 번째 조각]을 번갈아 누른다. 위의 버튼 줄은 그대로 있고 아래 글자만 바뀌는 것을 확인한다.
2. `여기는 FirstFragment`가 보이는 화면을 캡처한다.
3. [두 번째 조각]을 누르고 `여기는 SecondFragment`가 보이는 화면을 캡처한다.

| 캡처 | 보여야 하는 것 |
|---|---|
| 1장 | 버튼 줄 [첫 번째 조각] [두 번째 조각]과 그 아래 글자 `여기는 FirstFragment` |
| 2장 | 같은 자리의 같은 버튼 줄과 그 아래 글자 `여기는 SecondFragment` |

- 두 캡처를 나란히 놓고 버튼 줄이 같은 자리에 있는지 본다. 조각만 바뀐 것을 보여 주는 캡처다.
- 에뮬레이터 오른쪽 도구 막대의 카메라 버튼으로 찍어도 되고, PC 화면 캡처로 창째 찍어도 된다.
- 캡처에 계정 이름 같은 개인정보가 보이지 않는지 확인한다. 제출물은 [실습지의 제출](lab.md#제출--캡처-3장)에 있다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
이번 주 예제에서 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 꺼졌다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
