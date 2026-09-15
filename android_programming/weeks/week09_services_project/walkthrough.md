# 9주차 따라하기 — Service·Fragment 시연 다시 해 보기와 1차 과제 준비

이번 주 따라하기는 세 갈래다. 1일차 실습 60분은 [1차 과제 리허설](lab.md#1일차--1차-과제-리허설-60분)이므로, 아래 단계는 필요한 것만 골라서 한다.
각 단계의 결과가 화면이나 Logcat에 보이면 다음 단계로 넘어간다.

| 부분 | 누가 하나 | 시작점 | 채점 |
|---|---|---|---|
| A. `LogService` (1~7단계) | 1일차 Service 시연을 내 손으로 다시 해 보고 싶은 사람 | 7주차까지 만든 `SmartIO`. 없으면 7주차 완성본(`examples/day2`) | 하지 않는다 |
| B. `FragmentDemo` (8~12단계) | 1일차 Fragment 시연을 다시 해 보고 싶은 사람 | 새 프로젝트 | 하지 않는다 |
| C. `fakeRequest()` (13~18단계) | 1차 과제 (b)를 고른 사람 | 새 프로젝트 `Project1`(연습) → 내 앱에 옮기기 | 1차 과제에서 |
| 2일차 (19~21단계) | 모두 | 내 과제 앱 | 발표 |

A에서 넣은 [서비스 시작]·[서비스 중지]는 과제 제출본에 남아 있어도 감점하지 않는다. 10주차는 7주차 완성본을 이어서 쓰므로 지워도 되고 남겨도 된다.
과제 앱을 망가뜨릴까 걱정되면 A는 발표가 끝난 뒤에 한다.

## 1일차

### 1. SmartIO 열고 실행하기 (A)

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

이번 A에서 고치는 파일은 `LogService.kt`(새 파일), `AndroidManifest.xml`, `strings.xml`, `activity_main.xml`, `MainActivity.kt` 다섯 개다.
`ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`은 7주차 그대로 둔다. 전체 내용은 [7단계](#7-바꾸지-않는-파일-확인하기)에 있다.

### 2. LogService.kt 만들기

1. Project 창에서 `app › kotlin+java › com.example.smartio` 폴더를 **오른쪽 클릭** → **New › Kotlin Class/File**을 고른다.
2. 목록에서 **Class**를 고르고 이름에 `LogService`를 넣은 뒤 Enter를 누른다.
3. 생긴 파일의 내용을 모두 지우고 아래 코드로 바꾼다. 같은 코드가 [examples/service_demo/LogService.kt](examples/service_demo/LogService.kt)에 있다.

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

전체는 아래와 같다. 같은 코드가 [examples/service_demo/AndroidManifest.xml](examples/service_demo/AndroidManifest.xml)에 있다. 내 파일에는 아이콘 등의 줄이 더 있어도 된다.

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

전체는 아래와 같다. 같은 코드가 [examples/service_demo/strings.xml](examples/service_demo/strings.xml)에 있다.

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

전체는 아래와 같다. 같은 코드가 [examples/service_demo/activity_main.xml](examples/service_demo/activity_main.xml)에 있다.

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

폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있다. 이 화면은 가로에서 [서비스 시작]·[서비스 중지] 줄이 잘리거나 화면 밖으로 밀리고, `연결 중…`·`끊김`일 때는 [연결]·[다시 시도] 아래쪽도 잘린다. A 단계는 세로로 하고, 확인할 항목이 안 보이면 세로로 되돌려 확인한다.
발표용 과제본에서는 이 [서비스 시작]·[서비스 중지] 줄을 지워도 된다.

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

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/service_demo/MainActivity.kt](examples/service_demo/MainActivity.kt)에 있다.

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

### 6. Logcat으로 스레드 이름 보기

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

### 7. 바꾸지 않는 파일 확인하기

아래 파일은 7주차에 만든 그대로이며 이번 주에는 손대지 않는다. 같은 코드가 [examples/service_demo](examples/service_demo)에 있다.

`ConnState.kt` — [examples/service_demo/ConnState.kt](examples/service_demo/ConnState.kt)

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

`ConnViewModel.kt` — [examples/service_demo/ConnViewModel.kt](examples/service_demo/ConnViewModel.kt)

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

`ControlActivity.kt` — [examples/service_demo/ControlActivity.kt](examples/service_demo/ControlActivity.kt)

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

`activity_control.xml` — [examples/service_demo/activity_control.xml](examples/service_demo/activity_control.xml)

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

`res/values/themes.xml` — [examples/service_demo/res/values/themes.xml](examples/service_demo/res/values/themes.xml). 프로젝트를 만들 때 생긴 그대로다.

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

### 8. FragmentDemo 새 프로젝트 만들기 (B)

B는 SmartIO와 섞지 않고 작은 새 프로젝트로 한다.

1. **File › New › New Project** → **Phone and Tablet**에서 **Empty Views Activity** → **Next**.
2. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `FragmentDemo` |
| Package name | `com.example.fragmentdemo` |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |

3. 4주차 3단계처럼 `Gradle Scripts › build.gradle.kts (Module :app)`을 열어 `buildFeatures { viewBinding = true }`와 의존성 네 줄을 넣고 **Sync Now**를 누른다.
   Fragment는 `appcompat` 라이브러리에 함께 들어 있어서 따로 넣지 않는다. 검증에 쓴 전체 파일은 [examples/fragment_demo/build.gradle.kts](examples/fragment_demo/build.gradle.kts)이며 아래와 같다.

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

1. `app › res › values › strings.xml` 전체를 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/strings.xml](examples/fragment_demo/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Fragment Demo</string>
    <string name="first">첫 번째 조각</string>
    <string name="second">두 번째 조각</string>
    <string name="first_text">여기는 FirstFragment</string>
    <string name="second_text">여기는 SecondFragment</string>
</resources>
```

2. `app › res › layout › activity_main.xml`을 열고 오른쪽 위 **Code** 보기에서 전체를 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/activity_main.xml](examples/fragment_demo/activity_main.xml)에 있다.

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
3. **Code** 보기에서 전체를 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/fragment_first.xml](examples/fragment_demo/fragment_first.xml)에 있다.

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

4. 같은 방법으로 `fragment_second`를 만들고 전체를 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/fragment_second.xml](examples/fragment_demo/fragment_second.xml)에 있다.

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
2. 내용을 모두 지우고 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/FirstFragment.kt](examples/fragment_demo/FirstFragment.kt)에 있다.

```kotlin
package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 1일차: Activity 안에 끼우는 화면 조각. 자기 layout(fragment_first.xml)을 가진다.
class FirstFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 1일차).
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

3. 같은 방법으로 `SecondFragment`를 만들고 아래로 바꾼다. 같은 코드가 [examples/fragment_demo/SecondFragment.kt](examples/fragment_demo/SecondFragment.kt)에 있다.

```kotlin
package com.example.fragmentdemo

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

// 9주차 1일차: 두 번째 화면 조각. FirstFragment와 모양이 같고 layout만 다르다(fragment_second.xml).
class SecondFragment : Fragment() {

    // 1. 조각의 화면을 만들 때 불린다. layout 파일을 View로 만들어 돌려준다(9주차 1일차).
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
        // 1. 앱을 처음 켰을 때만 빈 자리에 FirstFragment를 끼운다(9주차 1일차).
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
        // 2. [첫 번째 조각] 버튼: 빈 자리의 조각을 FirstFragment로 바꾼다. 화면(Activity)은 그대로다(9주차 1일차).
        binding.firstButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 3. [두 번째 조각] 버튼: 빈 자리의 조각을 SecondFragment로 바꾼다. commit()을 빼면 아무것도 바뀌지 않는다(9주차 1일차).
        binding.secondButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, SecondFragment())
            transaction.commit()
        }
```

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/fragment_demo/MainActivity.kt](examples/fragment_demo/MainActivity.kt)에 있다.

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

        // 1. 앱을 처음 켰을 때만 빈 자리에 FirstFragment를 끼운다(9주차 1일차).
        //    회전 뒤에는 savedInstanceState가 null이 아니고, 보고 있던 조각을 시스템이 되살려 준다(3주차 복원과 같은 원리).
        //    바꾸기는 세 줄이다: 바꾸기 시작(beginTransaction) → 자리에 조각 넣기(replace) → 확정(commit).
        if (savedInstanceState == null) {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 2. [첫 번째 조각] 버튼: 빈 자리의 조각을 FirstFragment로 바꾼다. 화면(Activity)은 그대로다(9주차 1일차).
        binding.firstButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }

        // 3. [두 번째 조각] 버튼: 빈 자리의 조각을 SecondFragment로 바꾼다. commit()을 빼면 아무것도 바뀌지 않는다(9주차 1일차).
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

`AndroidManifest.xml` — [examples/fragment_demo/AndroidManifest.xml](examples/fragment_demo/AndroidManifest.xml)

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

`res/values/themes.xml` — [examples/fragment_demo/res/values/themes.xml](examples/fragment_demo/res/values/themes.xml)

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

### 13. (b) 새 프로젝트 Project1 만들기

C는 1차 과제 (b)를 고른 사람이 제공 함수 `fakeRequest()`를 부르는 모양을 먼저 작은 앱으로 만들어 보는 단계다. 다 되면 18단계 끝의 안내대로 내 앱에 옮긴다.

1. **File › New › New Project** → **Empty Views Activity** → Name `Project1`, Package name `com.example.project1`, Language `Kotlin` → **Finish**.
2. 8단계 3번처럼 `build.gradle.kts (Module :app)`에 ViewBinding과 의존성 네 줄을 넣고 **Sync Now**를 누른다. 검증에 쓴 전체 파일은 [examples/fake_request/build.gradle.kts](examples/fake_request/build.gradle.kts)이며 아래와 같다.

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.project1"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.project1"
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

3. 실행해서 `Hello World!`가 보이면 다음으로 간다.

### 14. FakeRequest.kt 넣기

1. `app › kotlin+java › com.example.project1`을 **오른쪽 클릭** → **New › Kotlin Class/File** → 이번에는 **File**을 고르고 이름 `FakeRequest` → Enter.
2. 내용을 모두 지우고 아래로 바꾼다. 같은 코드가 [examples/fake_request/FakeRequest.kt](examples/fake_request/FakeRequest.kt)에 있다.

```kotlin
package com.example.project1

import kotlinx.coroutines.delay
import kotlin.random.Random

// 9주차 1차 과제 제공 코드: 이 파일을 그대로 프로젝트에 복사한다. package 줄만 자기 프로젝트에 맞춘다.

// 1. 요청을 보낸 척한다. 1초 기다린 뒤 절반은 실패(throw)하고, 나머지는 "성공"을 돌려준다(9주차 1일차).
//    delay를 쓰는 suspend 함수이므로 코루틴 안에서만 부를 수 있다. 회전해도 결과를 남기려면 viewModelScope.launch { } 안에서 부른다.
//    실패하면 앱이 꺼지지 않도록 부르는 쪽에서 try/catch로 감싼다.
suspend fun fakeRequest(): String {
    delay(1000)
    if (Random.nextBoolean()) {
        throw Exception("요청 실패")
    }
    return "성공"
}
```

- 이 파일은 **제공 코드**다. 내 앱에 넣을 때는 첫 줄 `package`만 내 것으로 바꾸고 함수 안은 고치지 않는다.
- `suspend fun fakeRequest(): String`: 1초 기다린 뒤 절반은 `Exception("요청 실패")`를 던지고, 나머지는 `"성공"`을 돌려준다. `: String`은 글자 하나를 돌려준다는 표시, `return "성공"`은 그 글자를 돌려주고 함수를 끝낸다.
- 클래스 밖에 있는 함수라 같은 package의 어느 파일에서나 `fakeRequest()`로 부른다.
- 6주차 `connectFake()`와 달리 `withContext(Dispatchers.IO)`가 없다. `delay`는 스레드를 막지 않으므로 옮길 필요가 없다.
- `Random`이 빨간색이면 Alt+Enter에서 **`kotlin.random.Random`**을 고른다(6주차와 같다).

### 15. strings.xml과 activity_main.xml 바꾸기

1. `strings.xml` 전체를 아래로 바꾼다. 같은 코드가 [examples/fake_request/strings.xml](examples/fake_request/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Project1</string>
    <string name="state_idle">대기 중</string>
    <string name="request">요청</string>
    <string name="retry">다시 시도</string>
</resources>
```

2. `activity_main.xml` 전체를 아래로 바꾼다. 같은 코드가 [examples/fake_request/activity_main.xml](examples/fake_request/activity_main.xml)에 있다.

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
        android:id="@+id/resultText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/state_idle"
        android:textSize="18sp" />

    <Button
        android:id="@+id/requestButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/request" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

</LinearLayout>
```

- `resultText`는 결과 문구, `retryButton`은 처음에 숨겨 둔 [다시 시도]다(6주차 `retryButton`과 같은 모양).
- 실행하면 `Project1`, `대기 중`, [요청]이 보인다. 아직 [요청]은 아무 일도 하지 않는다.

### 16. RequestViewModel 만들기

1. `com.example.project1`을 **오른쪽 클릭** → **New › Kotlin Class/File** → **Class** → 이름 `RequestViewModel` → Enter.
2. 내용을 모두 지우고 아래로 바꾼다. 같은 코드가 [examples/fake_request/RequestViewModel.kt](examples/fake_request/RequestViewModel.kt)에 있다.

```kotlin
package com.example.project1

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// 9주차 1차 과제 예시: fakeRequest()를 부르는 ViewModel. 7주차 ConnViewModel과 같은 모양이라 회전해도 결과가 남는다.
class RequestViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 결과 문구와 실패 여부.
    //    바꾸는 쪽(_result, _failed)은 안에만 두고, 화면에는 읽기 전용(result, failed)만 보여 준다(7주차 2일차).
    private val _result = MutableStateFlow("대기 중")
    val result: StateFlow<String> = _result
    private val _failed = MutableStateFlow(false)
    val failed: StateFlow<Boolean> = _failed

    // 2. [요청]·[다시 시도]가 시작한 코루틴(7주차 1일차).
    private var requestJob: Job? = null

    // 3. [요청]·[다시 시도]: fakeRequest()를 부르고 결과를 _result·_failed에 넣는다(9주차 1일차).
    //    viewModelScope 코루틴은 회전해도 끊기지 않는다. 요청 중에 회전해도 1초 뒤 결과가 새 화면에 나온다.
    fun request() {
        // 이미 요청 중이면 새로 시작하지 않는다(7주차 1일차).
        if (requestJob?.isActive == true) {
            return
        }
        requestJob = viewModelScope.launch {
            _failed.value = false
            _result.value = "요청 중…"
            try {
                val text = fakeRequest()
                _result.value = "결과: $text"
            } catch (e: Exception) {
                // 4. 실패하면 실패 문구를 넣고 [다시 시도]가 보이게 한다(6주차 2일차).
                _result.value = "요청 실패"
                _failed.value = true
            }
        }
    }
}
```

| 빨간 글자 | 가져올 import |
|---|---|
| `ViewModel` | `androidx.lifecycle.ViewModel` |
| `viewModelScope` | `androidx.lifecycle.viewModelScope` |
| `Job` | `kotlinx.coroutines.Job` |
| `MutableStateFlow`, `StateFlow` | `kotlinx.coroutines.flow.MutableStateFlow`, `kotlinx.coroutines.flow.StateFlow` |
| `launch` | `kotlinx.coroutines.launch` |

- 7주차 `ConnViewModel`과 같은 모양이다. `_result`·`_failed`는 안에서만 바꾸고, 화면에는 `result`·`failed`만 보여 준다.
- `fakeRequest()`를 `viewModelScope.launch { }` **안**, `try { }` **안**에서 부른다. 코루틴 밖이면 빌드가 안 되고, `try` 밖이면 실패할 때 앱이 꺼진다.
- `if (requestJob?.isActive == true) { return }`: 요청 중에 [요청]을 또 눌러도 새 요청을 만들지 않는다(7주차 `startScan()`과 같다).
- 실패 문구는 `e.message` 대신 고정 글자 `"요청 실패"`를 넣는다. `e.message`는 `String?`이라 `MutableStateFlow<String>`에 바로 넣을 수 없다.

### 17. MainActivity에서 부르고 받기

`MainActivity.kt` 전체를 아래로 바꾼다. 4주차 ViewBinding 틀, 7주차 `by viewModels()`와 틀 두 개로 되어 있다. 같은 코드가 [examples/fake_request/MainActivity.kt](examples/fake_request/MainActivity.kt)에 있다.

```kotlin
package com.example.project1

import android.os.Bundle
import android.view.View
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.project1.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: RequestViewModel by viewModels()

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

        // 1. [요청] 버튼: 요청은 ViewModel이 보낸다. 화면은 부탁만 한다(9주차 1일차).
        binding.requestButton.setOnClickListener {
            viewModel.request()
        }

        // 2. [다시 시도] 버튼: 실패한 요청을 한 번 더 보낸다. [요청]과 같은 함수를 부른다(9주차 1일차).
        binding.retryButton.setOnClickListener {
            viewModel.request()
        }

        // 3. 결과 문구를 받아 화면에 보여 준다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.result.collect { result ->
                    binding.resultText.text = result
                }
            }
        }

        // 4. 실패 여부를 받아 [다시 시도]를 보이거나 숨긴다. 3번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.failed.collect { failed ->
                    if (failed) {
                        binding.retryButton.visibility = View.VISIBLE
                    } else {
                        binding.retryButton.visibility = View.GONE
                    }
                }
            }
        }
    }
}
```

| 빨간 글자 | 가져올 import |
|---|---|
| `ActivityMainBinding` | `com.example.project1.databinding.ActivityMainBinding` |
| `viewModels` | `androidx.activity.viewModels` |
| `Lifecycle`, `lifecycleScope`, `repeatOnLifecycle` | `androidx.lifecycle.Lifecycle`, `androidx.lifecycle.lifecycleScope`, `androidx.lifecycle.repeatOnLifecycle` |
| `launch` | `kotlinx.coroutines.launch` |
| `View` | `android.view.View` |

- [요청]과 [다시 시도]는 같은 `viewModel.request()`를 부른다. 화면은 부탁만 하고, 결과는 `collect { }`에서 받는다.
- 틀 두 개는 7주차 2일차와 같다. 우리 코드는 `collect { }` 안만 채운다.

### 18. 실행해서 채점 축 세 가지 확인하기

실행하고 [요청]을 여러 번 눌러 본다.

| 조작 | `resultText` | [다시 시도] |
|---|---|---|
| 앱 시작 | `대기 중` | 숨김 |
| [요청] 직후 | `요청 중…` | 숨김 |
| 1초 뒤 성공 | `결과: 성공` | 숨김 |
| 1초 뒤 실패 | `요청 실패` | **보임** |
| [다시 시도] | `요청 중…` → 1초 뒤 성공 또는 실패 | 숨김 → 결과대로 |
| `요청 중…`일 때 [요청] 한 번 더 | 바뀌지 않는다(새 요청 없음) | 숨김 |
| `요청 중…`에서 회전 | 가로 화면에서도 `요청 중…`, 1초 안에 결과가 새 화면에 나온다 | 결과대로 |
| `요청 실패`에서 회전 | 가로 화면에서도 `요청 실패` | **보임** 유지 |

- 정상 흐름(`결과: 성공`), 실패·재시도(`요청 실패` + [다시 시도] → 성공), 회전 유지가 모두 보이면 (b)의 화면 쪽 조건을 이해한 것이다.
- 50% 확률이라 성공과 실패를 둘 다 보려면 몇 번 눌러야 한다. 이 앱은 Logcat에 로그를 남기지 않는다.

Manifest와 테마는 프로젝트를 만들 때 생긴 그대로다. 검증에 쓴 파일은 아래와 같다.

`AndroidManifest.xml` — [examples/fake_request/AndroidManifest.xml](examples/fake_request/AndroidManifest.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:label="@string/app_name"
        android:theme="@style/Theme.Project1">

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

`res/values/themes.xml` — [examples/fake_request/res/values/themes.xml](examples/fake_request/res/values/themes.xml)

```xml
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Base.Theme.Project1" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your light theme here. -->
        <!-- <item name="colorPrimary">@color/my_light_primary</item> -->
    </style>

    <style name="Theme.Project1" parent="Base.Theme.Project1" />
</resources>
```

**내 앱에 옮기기**

1. `FakeRequest.kt`를 내 앱의 package 폴더에 같은 방법(14단계)으로 만들고, 첫 줄만 내 package로 둔다.
2. 내 앱에 ViewModel이 없으면 7주차 1일차처럼 `class … : ViewModel()`을 하나 만들고 16단계 모양으로 `request()`를 넣는다. 이미 있으면 그 ViewModel에 넣는다.
3. 버튼에서 `viewModel.request()`를 부르고, 17단계의 틀 두 개로 결과 문구와 [다시 시도]를 받는다.
4. 18단계 표와 같은 장면이 내 앱에서도 나오는지 확인하고, [리허설 1번](lab.md#1-채점-축-점검표-채우기) 점검표에 적는다.

## 2일차

### 19. 발표 전에 저장하고 다시 실행하기

1. 과제 앱을 열고 **저장**(Ctrl+S, 맥 ⌘+S) → `Run ▶`으로 다시 실행한다. 다시 실행하지 않은 코드는 확인되지 않은 코드다.
2. 에뮬레이터 화면 위쪽을 내려 빠른 설정에서 **자동 회전**을 켠다. 도구 막대의 회전 버튼으로 앱이 실제로 도는지 한 번 본다.
3. 앱을 첫 화면(`연결 안 됨` 또는 `대기 중`)에 둔다.
4. 코드 설명에 쓸 파일(ViewModel, `MainActivity.kt`, 본인 기능 파일)을 편집기 탭에 열어 둔다.

### 20. 2분 시연 한 번 해 보기

순서를 기다리는 동안 소리 없이 한 바퀴만 돌려 본다. 발표에서는 같은 순서로 한다.

```text
0:00–0:15  앱 이름, 고른 주제 (a)/(b), 본인 기능 한 문장
0:15–1:00  정상 흐름
1:00–1:30  실패 → [다시 시도] → 성공
1:30–1:50  진행 중이나 실패 화면에서 회전
1:50–2:00  마무리 한 문장
```

- 실패가 세 번 눌러도 나오지 않으면 레포트에 넣은 실패 캡처를 보여 주고 넘어간다.
- 한 바퀴 돌린 뒤에는 앱을 다시 첫 화면에 둔다. (a)는 [해제]를 누르면 `연결 안 됨`으로 돌아간다.

### 21. 발표하고 레포트 제출하기

1. 차례가 되면 2분 시연 → 평가자 질문 한 개에 **파일 열기 → 줄 가리키기 → 한 문장**으로 답한다.
2. 발표를 마치면 앱을 닫고 자리를 넘긴다.
3. 레포트 PDF와 `app/src/main` 압축 파일이 제출 칸에 올라갔는지 확인한다([과제 안내의 레포트](project_brief.md#레포트)).

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
이번 주 예제에서 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 꺼졌다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
