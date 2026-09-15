# 11주차 따라하기 — 장치 목록과 마지막 장치 저장

10주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
10주차 프로젝트가 없거나 실행되지 않으면 강의자에게 10주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에 고치는 파일은 `MainActivity.kt`, `activity_main.xml`, `strings.xml`(1·2일차)과 `AndroidManifest.xml`(2일차)이고, 2일차에 `ContactsReader.kt`를 새로 붙여 넣는다.
`ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `Permissions.kt`, `activity_control.xml`은 10주차 그대로 둔다. 전체 내용은 [9단계](#9-바꾸지-않는-파일-확인하기)에 있다.

## 1일차

### 1. 10주차 프로젝트 열고 실행하기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 연결 화면에 아래가 보이면 시작할 수 있다. 배터리 숫자는 에뮬레이터 설정에 따라 다르다.

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
연결 안 됨
[연결]
[권한 확인]
배터리 100% · 충전 중
```

3. [검색]을 한 번 눌러 `연결 중… 5` → … → `준비됨` 또는 `끊김`까지 7주차처럼 바뀌는지 본다. [권한 확인]도 10주차처럼 동작하면 된다.

### 2. 목록 자리 만들기

1. `app › res › values › strings.xml`의 `check_permission` 줄 **아래**(`</resources>` 바로 위)에 한 줄을 넣는다.

```xml
    <string name="device_list_title">검색된 장치</string>
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
    <string name="check_permission">권한 확인</string>
    <string name="device_list_title">검색된 장치</string>
</resources>
```

2. `app › res › layout › activity_main.xml`에서 상태 글자 `stateText` TextView **아래**, `connectButton` 버튼 **위**에 제목 TextView와 ListView를 넣는다.

```xml
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

3. 실행한다. `연결 안 됨` 아래에 `검색된 장치` 제목이 보이면 성공이다. 목록은 아직 비어 있어서 줄이 하나도 없고, 그 빈자리만큼 [연결]·[권한 확인]·배터리 문구가 아래로 내려간다.

- `ListView`: 여러 줄을 세로로 쌓아 보여 주는 View다. 스스로 글자를 갖고 있지 않고, 3단계에서 끼울 **어댑터**에게서 줄을 받아 그린다.
- `android:layout_height="0dp"` + `android:layout_weight="1"`: 남는 세로 공간을 목록이 모두 차지한다. 4주차 제어 화면의 `logText`와 같은 방법이다. `wrap_content`로 두면 이름이 늘 때마다 아래 버튼이 화면 밖으로 밀린다.
- `id` 이름 `deviceList`는 다음 단계 Kotlin 코드의 `binding.deviceList`와 글자까지 같아야 한다.

### 3. 목록과 어댑터 만들기

1. `MainActivity.kt`를 열고 `onCreate` 안, `// 2.` 자동 연결 Switch 블록(`binding.autoSwitch.setOnCheckedChangeListener`)의 닫는 `}` **아래**, `// 3.` [검색] 블록 **위**에 한 줄을 비우고 아래 줄들을 넣는다.

```kotlin
        // 15. 검색된 장치 이름을 담는 목록. 처음에는 비어 있고 add로 하나씩 늘린다(11주차 1일차).
        val devices = mutableListOf<String>()

        // 16. 어댑터: 목록(devices)의 이름을 한 줄짜리 기본 모양(simple_list_item_1)으로 ListView에 넣어 준다(11주차 1일차).
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
        binding.deviceList.adapter = adapter
```

2. 빨간 `ArrayAdapter`에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 `android.widget.ArrayAdapter`를 가져온다.
3. 실행한다. 화면은 2단계와 같다. 목록 `devices`가 비어 있어서 ListView에 보일 줄이 없다. 빌드만 되면 된다.

- `mutableListOf<String>()`: 늘리고 비울 수 있는 빈 목록을 만든다. `<String>`은 "글자만 담는다"는 표시다.
- `ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)`: 목록(`devices`)과 ListView(화면) 사이를 잇는 어댑터다. 세 값은 화면(`this`), 한 줄의 모양, 목록이다.
- `android.R.layout.simple_list_item_1`: 우리 앱의 `R`이 아니라 **Android가 미리 준비한** 한 줄짜리 글자 모양이다. 그래서 앞에 `android.`이 붙는다.
- `binding.deviceList.adapter = adapter`: ListView에 어댑터를 끼운다. 이제 ListView는 "몇 줄인가, 몇 번 줄에 무엇을 쓰나"를 어댑터에게 묻는다.
- 두 `val`은 반드시 [검색] 블록보다 **위**, `onCreate` **안**에 둔다. 4·6·7단계의 리스너들이 5주차 "람다 안에서 바깥 변수 쓰기"로 이 둘을 쓰는데, 선언한 줄보다 위에서는 쓸 수 없다.

### 4. [검색]에서 1초마다 이름 넣기

1. 클래스 안, `permissionLauncher` 블록을 닫는 `}` **아래**에 한 줄을 비우고 변수를 넣는다. `onCreate` **밖**이다.

```kotlin
    // 11주차 1일차: [검색]이 시작한 "목록에 이름 추가" 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같은 모양).
    private var deviceJob: Job? = null
```

`Job`이 빨간색이면 Alt+Enter로 `kotlinx.coroutines.Job`을 가져온다.

2. `// 3.` [검색] 블록 안, `viewModel.startScan()` 줄 **아래**에 `// 17.` 부분을 넣는다. 블록 전체는 아래와 같다.

```kotlin
        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
            // 17. 목록을 비우고, 1초마다 가짜 장치 이름을 하나씩 추가한다(11주차 1일차).
            //     목록을 바꾼 뒤에는 notifyDataSetChanged()로 어댑터에 알려야 화면의 ListView가 다시 그려진다.
            devices.clear()
            adapter.notifyDataSetChanged()
            deviceJob = lifecycleScope.launch {
                for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
                    delay(1000)
                    devices.add(name)
                    adapter.notifyDataSetChanged()
                    val count = devices.size
                    Log.d("Scan", "추가: $name, 장치 수: $count")
                }
            }
        }
```

3. 빨간 글자를 차례로 Alt+Enter → Import로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `delay` | `kotlinx.coroutines.delay` |
| `Log` | `android.util.Log` |

`lifecycleScope`와 `launch`는 7주차 `collect` 틀에서 이미 import했다.

4. 실행하고 [검색]을 누른다.

| 시간 | 상태 글자 | 목록 |
|---|---|---|
| 누른 직후 | `연결 중… 5` | 비어 있음 |
| 1초 뒤 | `연결 중… 4` | `ESP32_BLE_A` |
| 2초 뒤 | `연결 중… 3` | `ESP32_BLE_A`, `ESP32_BLE_B` |
| 3초 뒤 | `연결 중… 2` | `ESP32_BLE_A`, `ESP32_BLE_B`, `ESP32_BLE_C` |
| 5초 뒤부터 | `서비스 확인 중` → `준비됨` 또는 `끊김` | 세 줄 그대로 |

5. Logcat 창의 필터에 `package:mine tag:Scan`을 넣는다. [검색] 한 번에 아래 세 줄이 찍힌다.

```text
추가: ESP32_BLE_A, 장치 수: 1
추가: ESP32_BLE_B, 장치 수: 2
추가: ESP32_BLE_C, 장치 수: 3
```

6. `끊김`이 되면 [검색]을 다시 눌러 본다(`준비됨`이면 [해제]를 누른 뒤 [검색]). 목록이 비워졌다가 A·B·C가 다시 1초마다 들어가면 성공이다.

- `devices.clear()`: 목록을 모두 비운다. 이것이 없으면 두 번째 [검색]에서 `A B C A B C`로 쌓인다.
- `for (name in arrayOf(…))`: 10주차 `for (permission in blePermissions())`처럼 묶음 안의 이름을 하나씩 꺼내 반복한다.
- `devices.add(name)`: 목록 끝에 이름 하나를 넣는다.
- `adapter.notifyDataSetChanged()`: 어댑터에게 "목록이 바뀌었다"고 알린다. 알림을 받아야 ListView가 다시 그려진다.
- `val count = devices.size`: 목록에 든 개수다. `"장치 수: $count"`처럼 `$count` 뒤에 공백이나 기호를 둔다. `"장치 $count개"`로 쓰면 Kotlin이 `count개`까지 변수 이름으로 읽어 빌드 오류가 난다.
- 목록을 채우는 코루틴은 6주차처럼 화면의 `lifecycleScope.launch`에서 돈다. 상태 카운트다운은 7주차 그대로 ViewModel에서 따로 돈다.

### 5. notifyDataSetChanged를 빼 보기

한 곳만 바꾸고 실행한 뒤 반드시 되돌린다.

1. `for` **안**에 있는 `adapter.notifyDataSetChanged()` 한 줄을 지운다. `devices.clear()` 바로 아래의 것은 그대로 둔다. 빌드는 된다.
2. 실행하고 [검색]을 누른 뒤 목록과 Logcat `tag:Scan`을 함께 본다. Android 14 에뮬레이터에서는 이렇게 보인다. Logcat에는 `장치 수: 1`~`3`이 그대로 찍히는데 목록은 늘지 않고 비어 있다. 상태가 `준비됨`이 되는 순간(약 7~8초 뒤) 세 줄이 한꺼번에 나타나고, `끊김`으로 끝나면 끝까지 비어 있다. 내 화면에서 어느 쪽이 보였는지 적는다.
3. 관찰한 결과를 [실습지](lab.md#3-검색에서-이름-넣기와-중지)의 표에 적고, 지운 줄을 되돌린다.

목록(데이터)이 바뀌어도 화면은 알림을 받아야 바뀐다. 이번 주 목록 코드에서 가장 자주 빠뜨리는 한 줄이다.

### 6. [중지]에서 이름 넣기 멈추기

`// 4.` [중지] 블록 안, `viewModel.stopScan()` 줄 **아래**에 `// 18.` 두 줄을 넣는다. 블록 전체는 아래와 같다.

```kotlin
        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            // 18. 목록에 이름을 넣던 코루틴도 함께 멈춘다. 이미 들어간 이름은 목록에 남는다(11주차 1일차).
            deviceJob?.cancel()
        }
```

실행하고 [검색]을 누른 뒤 `ESP32_BLE_B`가 들어온 직후 [중지]를 누른다. 상태는 `연결 안 됨`이 되고, 목록에는 A·B가 남고 C는 들어오지 않으면 성공이다.

- 6주차 `scanJob?.cancel()`과 같은 모양이다. 아직 [검색]을 안 눌렀으면 `deviceJob`이 `null`이라 `?.`로 부른다.
- 취소는 "앞으로 넣을 이름"만 멈춘다. 이미 넣은 이름은 목록에 남는다.

### 7. 목록의 한 줄 누르기

1. `onCreate` 안, `// 12.` [권한 확인] 블록(`binding.permissionButton.setOnClickListener`)의 닫는 `}` **아래**, `onCreate`를 닫는 `}` **위**에 리스너를 넣는다.

```kotlin
        // 19. 목록의 한 줄을 누르면: 누른 줄 번호(position)의 이름을 어댑터에서 꺼내 장치 이름 칸에 넣는다(11주차 1일차).
        //     1번 [연결]은 이 칸의 이름을 들고 제어 화면으로 가므로 1번 코드는 바꾸지 않는다.
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
        }
```

19번은 `onCreate` 안에 들어가므로 완성 파일에서는 `// 10.`(`onStart`)·`// 11.`(`onStop`)보다 **위**에 있다. 번호 순서대로 찾지 말고 위치 설명을 따른다.

2. 실행하고 아래 순서로 눌러 본다.

| 조작 | 화면 |
|---|---|
| [검색] → 3초 기다리기 → `ESP32_BLE_B` 누르기 | 장치 이름 칸에 `ESP32_BLE_B`, Toast `선택: ESP32_BLE_B` |
| 이어서 [연결] | 제어 화면 상단 `장치: ESP32_BLE_B` |
| 제어 화면 [뒤로] | 연결 화면. 목록 세 줄이 그대로 있다 |

- `{ _, _, position, _ -> }`: 한 줄을 누르면 값 네 개(목록 View, 누른 줄 View, **줄 번호**, id)가 넘어온다. 줄 번호 `position`만 쓰고 나머지는 4주차 `{ _, isChecked -> }`처럼 `_`로 둔다. `position`은 0부터 센다(A=0, B=1, C=2).
- `adapter.getItem(position) ?: ""`: 어댑터에게 그 줄의 이름을 달라고 한다. `String?`가 오므로 4주차 `getStringExtra("name") ?: ""`와 같이 `?: ""`를 붙인다.
- `binding.deviceNameEdit.setText(name)`: EditText에 글자를 넣을 때는 `setText`를 쓴다. TextView처럼 `binding.deviceNameEdit.text = name`으로 쓰면 빌드 오류가 난다.
- 1번 [연결] 코드는 4주차 그대로 장치 이름 칸을 읽는다. 그래서 1번은 고치지 않아도 고른 이름이 제어 화면으로 간다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

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
import android.util.Log
import android.view.View
import android.widget.ArrayAdapter
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
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
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

    // 11주차 1일차: [검색]이 시작한 "목록에 이름 추가" 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같은 모양).
    private var deviceJob: Job? = null

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

        // 15. 검색된 장치 이름을 담는 목록. 처음에는 비어 있고 add로 하나씩 늘린다(11주차 1일차).
        val devices = mutableListOf<String>()

        // 16. 어댑터: 목록(devices)의 이름을 한 줄짜리 기본 모양(simple_list_item_1)으로 ListView에 넣어 준다(11주차 1일차).
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
        binding.deviceList.adapter = adapter

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
            // 17. 목록을 비우고, 1초마다 가짜 장치 이름을 하나씩 추가한다(11주차 1일차).
            //     목록을 바꾼 뒤에는 notifyDataSetChanged()로 어댑터에 알려야 화면의 ListView가 다시 그려진다.
            devices.clear()
            adapter.notifyDataSetChanged()
            deviceJob = lifecycleScope.launch {
                for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
                    delay(1000)
                    devices.add(name)
                    adapter.notifyDataSetChanged()
                    val count = devices.size
                    Log.d("Scan", "추가: $name, 장치 수: $count")
                }
            }
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            // 18. 목록에 이름을 넣던 코루틴도 함께 멈춘다. 이미 들어간 이름은 목록에 남는다(11주차 1일차).
            deviceJob?.cancel()
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

        // 19. 목록의 한 줄을 누르면: 누른 줄 번호(position)의 이름을 어댑터에서 꺼내 장치 이름 칸에 넣는다(11주차 1일차).
        //     1번 [연결]은 이 칸의 이름을 들고 제어 화면으로 가므로 1번 코드는 바꾸지 않는다.
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
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

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
10주차까지의 코드(주석 1~14)가 내 코드와 조금 달라도 동작이 같으면 그대로 둔다.

### 8. 캡처하고 화면 돌려 보기

1. [검색]을 누르고 3초 넘게 기다려 `검색된 장치` 아래 `ESP32_BLE_A`·`ESP32_BLE_B`·`ESP32_BLE_C` 세 줄이 모두 보이는 **세로 화면**을 캡처한다. 한 줄을 눌러 장치 이름 칸에 이름이 들어간 상태면 더 좋다. **이 화면이 제출 캡처 1이다.**
2. 캡처한 뒤 에뮬레이터 화면을 돌려 본다. 상태 글자와 카운트다운은 7주차 ViewModel 덕분에 이어지지만 **목록은 비워진다.** `devices`가 화면(Activity) 안에 있어서 새 화면이 빈 목록으로 다시 만들기 때문이다. 코드가 틀린 것이 아니다. 캡처는 돌리기 전에 한다.

- 연결 화면은 스크롤이 없다. 폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있고, 목록은 높이가 0이 되어 보이지 않는다. 확인할 항목이 안 보이면 세로로 되돌려 확인한다.
- 프로젝트는 2일차에 그대로 이어서 쓴다.

### 9. 바꾸지 않는 파일 확인하기

아래 파일은 10주차에 만든 그대로이며 이번 주 1일차에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.
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

`Permissions.kt` — [examples/day1/Permissions.kt](examples/day1/Permissions.kt)

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). 10주차 2일차 그대로다. 2일차 15단계에서 한 줄을 더한다. 내 파일에는 아이콘 등의 줄이 더 있다.

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

### 10. 마지막 장치 글자와 [연락처 보기] 버튼 자리 만들기

오늘 쓸 글자 하나와 버튼 하나를 XML에 먼저 모두 넣는다. [연락처 보기]는 15~19단계에서 연결하므로 그 전에는 눌러도 아무 일이 없다.

1. `strings.xml`의 `device_list_title` 줄 **아래**에 두 줄을 넣는다.

```xml
    <string name="last_device_none">마지막 장치: 없음</string>
    <string name="show_contacts">연락처 보기</string>
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
    <string name="device_list_title">검색된 장치</string>
    <string name="last_device_none">마지막 장치: 없음</string>
    <string name="show_contacts">연락처 보기</string>
</resources>
```

2. `activity_main.xml`에서 맨 위 앱 제목 TextView(`@string/app_name`) **아래**, `deviceNameEdit` **위**에 TextView를 넣는다.

```xml
    <TextView
        android:id="@+id/lastDeviceText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/last_device_none"
        android:textSize="16sp" />
```

3. 같은 파일에서 `permissionButton` **아래**, `batteryText` **위**에 버튼을 넣는다. 배터리 문구는 계속 맨 아래에 남는다.

```xml
    <Button
        android:id="@+id/contactsButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/show_contacts" />
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

4. 실행한다. 앱 제목 바로 아래에 `마지막 장치: 없음`, [권한 확인] 아래에 [연락처 보기]가 보이면 성공이다.

### 11. [연결]에서 장치 이름 저장하기

`// 1.` [연결] 블록의 `else {` 안, `val intent = Intent(this, ControlActivity::class.java)` 줄 **위**에 `// 20.` 세 줄을 넣는다. 블록 전체는 아래와 같다.

```kotlin
        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                // 20. 연결하는 장치 이름을 앱 전용 저장소 "smartio"에 "last"라는 이름표로 저장한다(11주차 2일차).
                //     edit()로 고치기 시작 → putString으로 값 넣기 → apply()로 저장. 앱을 껐다 켜도 남는다.
                getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
            }
        }
```

새로 import할 것은 없다. 실행하고 [검색] → `ESP32_BLE_B` 누르기 → [연결]을 한다. 제어 화면에 `장치: ESP32_BLE_B`가 보이면 된다. 화면에 달라진 것은 없지만 이 순간 이름이 저장되었다.

- `getSharedPreferences("smartio", MODE_PRIVATE)`: 이 앱만 읽고 쓰는 `smartio`라는 이름의 작은 저장소를 연다. 처음이면 새로 만든다.
- `.edit()` → `.putString("last", name)` → `.apply()`: 고치기 시작하고, `last`라는 이름표(키)에 장치 이름(값)을 넣고, 저장을 확정한다. `apply()`를 빠뜨리면 저장되지 않는다.
- `MODE_PRIVATE`: "이 앱 전용"이라는 뜻이다. Activity 안에서는 10주차 `RESULT_OK`처럼 이름만 쓴다.
- `else` 안에 두었으므로 이름이 비어 있을 때는 저장하지 않는다. 목록에서 고른 이름이든 직접 입력한 이름이든 [연결]로 넘어갈 때 저장된다.
- Android Studio가 `edit()`에 노란 밑줄로 다른 쓰는 법을 제안할 수 있다. 빌드를 막지 않으므로 그대로 둔다.

### 12. 앱이 시작할 때 꺼내 보여 주기

1. `onCreate` 안, `// 19.` 목록 클릭 블록(`binding.deviceList.setOnItemClickListener`)의 닫는 `}` **아래**, `onCreate`를 닫는 `}` **위**에 `// 21.` 부분을 넣는다.

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
```

2. 실행한다. 11단계에서 `ESP32_BLE_B`로 [연결]했다면 앱이 켜지자마자 제목 아래에 `마지막 장치: ESP32_BLE_B`가 보인다. 이어서 아래를 차례로 해 본다.

| 조작 | 제목 아래 글자 |
|---|---|
| [검색] → `ESP32_BLE_C` 누르기 → [연결] → 제어 화면 [뒤로] | 아직 `마지막 장치: ESP32_BLE_B` |
| 화면 돌리기(안 보이면 세로로 되돌려 확인) | `마지막 장치: ESP32_BLE_C` |
| 앱을 완전히 끄고 다시 실행 | `마지막 장치: ESP32_BLE_C` |
| 장치 이름 칸에 `MyBoard` 입력 → [연결] → 앱을 끄고 다시 실행 | `마지막 장치: MyBoard` |

앱을 완전히 끄려면 에뮬레이터 화면 아래의 최근 앱 화면에서 SmartIO를 위로 밀어 없애거나, Android Studio의 ■ Stop을 누른다. 다시 실행은 앱 아이콘이나 `Run ▶`으로 한다.

- `prefs.getString("last", "")`: `last` 이름표의 값을 꺼낸다. 저장한 적이 없으면 두 번째 값 `""`가 온다.
- `?: ""`: `getString`은 `String?`를 돌려준다. 4주차 `getStringExtra(…) ?: ""`와 같이 붙여 `lastName`을 확실한 글자로 만든다. 빼면 `lastName.isEmpty()`에서 빌드 오류가 난다.
- 저장소 이름 `"smartio"`와 이름표 `"last"`는 11단계와 **글자까지 같아야** 한다. 다르면 빌드는 되지만 늘 `없음`이다.
- 읽는 곳이 `onCreate` 한 곳뿐이다. [뒤로]로 돌아올 때는 `onCreate`가 다시 불리지 않아서(3주차 생명주기) 글자가 그대로다. 회전하거나 앱을 다시 켜면 `onCreate`가 불려 새 값이 보인다.
- 3주차 `onSaveInstanceState`는 회전할 때만 값을 넘겼다. SharedPreferences는 앱을 껐다 켜도 남는다. 앱을 **삭제**하면 저장소도 함께 지워져 `없음`으로 돌아간다.

### 13. 캡처 2 찍기

목록에서 이름을 골라 [연결]한 뒤 앱을 완전히 끄고 다시 실행한다. 첫 화면에서 제목 아래 `마지막 장치: ESP32_BLE_…`가 보이고, 목록은 비어 있고, 상태가 `연결 안 됨`인 화면을 캡처한다. **이 화면이 제출 캡처 2다.**

### 14. 실기기 준비하기

Android 폰이 있으면 이 단계로 캡처 3을 만든다. 없으면 15단계로 간다. 메뉴 이름과 위치는 제조사와 Android 버전에 따라 조금 다르다.

1. 폰의 설정 › 휴대전화 정보(또는 디바이스 정보) › 소프트웨어 정보에서 **빌드 번호**를 7번 누른다. "개발자 모드를 켰습니다" 같은 안내가 뜬다.
2. 설정 › **개발자 옵션**에서 **USB 디버깅**을 켠다.
3. 데이터가 오가는 USB 케이블로 PC에 연결한다. 충전만 되는 케이블은 인식되지 않는다.
4. 폰에 "USB 디버깅을 허용하시겠습니까?" 창이 뜨면 **허용**을 누른다.
5. Android Studio 위쪽 기기 목록에서 에뮬레이터 대신 내 폰 이름을 고르고 `Run ▶`을 누른다.
6. 폰에서 SmartIO가 실행되면 빠른 설정에서 **블루투스**와 **위치**를 켠다.
7. 앱에서 [권한 확인]을 누르고 권한 창에서 허용한다. Toast `권한 OK`가 보이면 12주차 BLE 수업 준비가 끝났다.

| 확인 | 실기기에서 보여야 할 것 |
|---|---|
| 앱 실행 | 연결 화면이 뜨고 위쪽 상태 표시줄에 폰의 시계·배터리가 보인다 |
| 마지막 장치 | `마지막 장치: 없음`. 폰에는 앱이 새로 설치되어 에뮬레이터에 저장한 값이 없다 |
| [검색] | 1일차와 같이 가짜 이름 세 줄 |
| [권한 확인] | Android 12 이상은 "근처 기기", 11 이하는 "위치" 권한 창 → Toast `권한 OK` |

기기 목록에 폰이 안 보이면 케이블을 바꾸고, 폰의 허용 창을 놓치지 않았는지 보고, USB 디버깅을 껐다 켠 뒤 케이블을 다시 꽂는다.

**실기기에서 앱이 뜬 화면(가능하면 Toast `권한 OK`가 함께 보이게)이 제출 캡처 3이다.** 폰의 화면 캡처 기능으로 찍는다. 알림 내용이 보이지 않게 한다.

### 15. 연락처 권한 선언하기

실기기가 없으면 15~19단계로 캡처 3을 만든다. 실기기로 캡처 3을 찍은 학생은 해 보지 않아도 된다.

`app › manifests › AndroidManifest.xml`에서 `ACCESS_FINE_LOCATION` 선언 **아래**, `<application` **위**에 두 줄을 넣는다.

```xml
    <!-- 11주차 2일차: 연락처 앱의 데이터(ContentProvider)를 읽는 권한. 실행 중에도 허락받아야 한다. -->
    <uses-permission android:name="android.permission.READ_CONTACTS" />
```

전체는 아래와 같다. 같은 코드가 [examples/day2/AndroidManifest.xml](examples/day2/AndroidManifest.xml)에 있다.

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

실행한다. 화면은 그대로다. 연락처는 다른 앱(연락처 앱)의 데이터라서 10주차 BLE 권한처럼 선언하고, 실행 중에도 허락받아야 한다.

### 16. ContactsReader.kt 붙여 넣기

1. Project 창에서 `app › kotlin+java › com.example.smartio`를 오른쪽 클릭 → **New › Kotlin Class/File**을 고른다.
2. 이름에 `ContactsReader`를 쓰고 목록에서 **Object**를 고른 뒤 Enter.
3. 생긴 파일의 내용을 모두 지우고 아래 제공 코드를 붙여 넣는다. 같은 코드가 [examples/day2/ContactsReader.kt](examples/day2/ContactsReader.kt)에 있다.

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

실행한다. 화면은 그대로다. 빌드만 되면 된다.

- `object ContactsReader`: 7주차 `object ConnState`처럼 만들지 않고 이름으로 바로 부르는 묶음이다. `ContactsReader.names(contentResolver)`로 부른다.
- `ContactsContract.Contacts.CONTENT_URI`: 연락처 창구의 주소다. 값은 `content://com.android.contacts/contacts`이다. `content://`는 "ContentProvider에게 묻는 주소", `com.android.contacts`는 연락처 앱의 창구 이름, `/contacts`는 그 안의 표 이름이다.
- `resolver.query(주소, 가져올 칸, 조건, 조건 값, 정렬)`: 연락처 표에서 "표시 이름" 칸만, 조건 없이(`null`) 모두, 이름순으로 달라는 요청이다.
- `while (cursor.moveToNext())`: `while`은 괄호 안이 참인 동안 반복한다. `cursor`를 한 줄씩 옮기다가 더 읽을 줄이 없으면 끝난다.
- `cursor.close()`: 다 읽었으면 반드시 닫는다.
- `List<String>`: 돌려주는 목록의 종류다. 안에서는 `mutableListOf`로 만들어 채우고, 밖에는 읽기용 목록으로 돌려준다. 7주차 `MutableStateFlow`와 `StateFlow`의 짝과 같다.

### 17. showContacts() 만들기

`MainActivity.kt`에서 `// 14.` `showPermissionDialog()` 함수를 닫는 `}` **아래**, 클래스의 마지막 `}` **위**에 함수를 넣는다.

```kotlin
    // 23. ContactsReader로 연락처 이름을 읽어 AlertDialog 목록으로 보여 준다(11주차 2일차).
    //     0건이면 목록 대신 안내 문구를 보여 준다. 0건은 실패가 아니다(에뮬레이터는 처음에 연락처가 없다).
    private fun showContacts() {
        val names = ContactsReader.names(contentResolver)
        if (names.isEmpty()) {
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setMessage("연락처가 0건입니다. 연락처 앱에서 한 명을 추가한 뒤 다시 눌러 보세요.")
                .setPositiveButton("확인", null)
                .show()
        } else {
            // setItems는 배열을 받으므로 toTypedArray()로 목록(List)을 배열(Array)로 바꿔 넘긴다.
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setItems(names.toTypedArray(), null)
                .setPositiveButton("닫기", null)
                .show()
        }
    }
```

새로 import할 것은 없다(`AlertDialog`는 10주차에 import했다). 실행한다. 화면은 그대로다. 빌드만 되면 된다.

- `contentResolver`: Activity가 가진 "다른 앱의 창구에 요청하는 도구"다. 이것을 `ContactsReader.names`에 넘긴다.
- `names.isEmpty()`: 4주차에 글자에 쓴 `isEmpty()`를 목록에도 쓴다. 연락처가 한 명도 없으면 참이다.
- `.setItems(names.toTypedArray(), null)`: 대화상자에 목록을 보여 준다. `setItems`는 배열을 받아서 `toTypedArray()`로 목록을 10주차 `arrayOf`와 같은 배열로 바꾼다. 줄을 눌렀을 때 할 일이 없어서 `null`이다.
- 0건은 실패가 아니다. 에뮬레이터는 처음에 연락처가 없다.

### 18. contactsLauncher 만들기

클래스 안, `deviceJob` 줄 **아래**에 한 줄을 비우고 요청 틀을 넣는다. `onCreate` **밖**이다.

```kotlin
    // 11주차 2일차: 연락처 권한 요청 틀. 10주차 permissionLauncher와 같은 모양으로 클래스 안(onCreate 밖)에 둔다.
    // 결과는 읽지 않고(_) 지금 READ_CONTACTS가 허용됐는지 다시 확인한다. 허용이면 23번 함수로 연락처를 보여 준다.
    private val contactsLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
            showContacts()
        } else {
            AlertDialog.Builder(this)
                .setTitle("연락처 권한 없음")
                .setMessage("연락처를 읽으려면 권한이 필요합니다. 거절해도 앱의 다른 기능은 그대로 쓸 수 있습니다.")
                .setPositiveButton("확인", null)
                .show()
        }
    }
```

`Manifest`가 빨간색이면 Alt+Enter 목록에서 **`android.Manifest`**를 고른다. `java.util.jar.Manifest`를 고르면 `Manifest.permission`에 빨간 줄이 남는다.

실행한다. 화면은 그대로다. 빌드만 되면 된다.

- 10주차 `permissionLauncher`와 같은 틀이다. 권한이 하나뿐이라 `arrayOf(…)`에 `READ_CONTACTS` 하나만 넣어 요청한다(19단계).
- 결과 묶음은 읽지 않고(`_`) `checkSelfPermission`으로 지금 허용됐는지 다시 본다. 허용이면 17단계 `showContacts()`, 아니면 [확인]만 있는 안내 대화상자다.
- 연락처는 선택 기능이라 거절해도 설정 화면으로 보내지 않는다.

### 19. [연락처 보기] 버튼에 연결하기

1. `onCreate` 안, `// 21.` 마지막 장치 표시 블록의 `if … else` 닫는 `}` **아래**, `onCreate`를 닫는 `}` **위**에 리스너를 넣는다.

```kotlin
        // 22. [연락처 보기] 버튼: READ_CONTACTS가 이미 허용이면 바로 보여 주고, 아니면 요청 창을 띄운다(11주차 2일차, 시연·선택 실습).
        binding.contactsButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                showContacts()
            } else {
                contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))
            }
        }
```

2. 실행하고 [연락처 보기]를 누른다. 권한 창의 문구와 버튼 이름은 OS 버전과 언어 설정에 따라 조금 다르다.

| 조작 | 화면 |
|---|---|
| 처음 [연락처 보기] | 시스템 권한 창: Smart I/O Controller가 연락처에 액세스하도록 허용할지 묻는다 |
| 권한 창 [허용] (연락처 0명) | 대화상자 `연락처` / `연락처가 0건입니다. 연락처 앱에서 한 명을 추가한 뒤 다시 눌러 보세요.` / [확인] |
| 에뮬레이터 Contacts 앱에서 두 명 추가 → 앱으로 돌아와 [연락처 보기] | 권한 창 없이 곧바로 대화상자 `연락처`에 이름순 두 줄과 [닫기] |
| 권한 창 [허용 안함] | 대화상자 `연락처 권한 없음`과 [확인] |

에뮬레이터에 연락처를 넣으려면 앱 목록에서 **Contacts**를 열고 **+**(새 연락처) → 이름만 입력 → 저장한다.
이미 허용해서 거절 화면을 보고 싶으면 설정 › 앱 › Smart I/O Controller › 권한 › 연락처 › 허용 안함으로 바꾼다. 허용했던 권한을 끄면 시스템이 앱을 종료하므로 다시 실행하면 처음 화면으로 시작한다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.net.Uri
import android.os.BatteryManager
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View
import android.widget.ArrayAdapter
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
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
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

    // 11주차 1일차: [검색]이 시작한 "목록에 이름 추가" 코루틴. [중지]에서 취소하려고 보관한다(6주차 scanJob과 같은 모양).
    private var deviceJob: Job? = null

    // 11주차 2일차: 연락처 권한 요청 틀. 10주차 permissionLauncher와 같은 모양으로 클래스 안(onCreate 밖)에 둔다.
    // 결과는 읽지 않고(_) 지금 READ_CONTACTS가 허용됐는지 다시 확인한다. 허용이면 23번 함수로 연락처를 보여 준다.
    private val contactsLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
            showContacts()
        } else {
            AlertDialog.Builder(this)
                .setTitle("연락처 권한 없음")
                .setMessage("연락처를 읽으려면 권한이 필요합니다. 거절해도 앱의 다른 기능은 그대로 쓸 수 있습니다.")
                .setPositiveButton("확인", null)
                .show()
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
                // 20. 연결하는 장치 이름을 앱 전용 저장소 "smartio"에 "last"라는 이름표로 저장한다(11주차 2일차).
                //     edit()로 고치기 시작 → putString으로 값 넣기 → apply()로 저장. 앱을 껐다 켜도 남는다.
                getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
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

        // 15. 검색된 장치 이름을 담는 목록. 처음에는 비어 있고 add로 하나씩 늘린다(11주차 1일차).
        val devices = mutableListOf<String>()

        // 16. 어댑터: 목록(devices)의 이름을 한 줄짜리 기본 모양(simple_list_item_1)으로 ListView에 넣어 준다(11주차 1일차).
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
        binding.deviceList.adapter = adapter

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
            // 17. 목록을 비우고, 1초마다 가짜 장치 이름을 하나씩 추가한다(11주차 1일차).
            //     목록을 바꾼 뒤에는 notifyDataSetChanged()로 어댑터에 알려야 화면의 ListView가 다시 그려진다.
            devices.clear()
            adapter.notifyDataSetChanged()
            deviceJob = lifecycleScope.launch {
                for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
                    delay(1000)
                    devices.add(name)
                    adapter.notifyDataSetChanged()
                    val count = devices.size
                    Log.d("Scan", "추가: $name, 장치 수: $count")
                }
            }
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            // 18. 목록에 이름을 넣던 코루틴도 함께 멈춘다. 이미 들어간 이름은 목록에 남는다(11주차 1일차).
            deviceJob?.cancel()
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

        // 19. 목록의 한 줄을 누르면: 누른 줄 번호(position)의 이름을 어댑터에서 꺼내 장치 이름 칸에 넣는다(11주차 1일차).
        //     1번 [연결]은 이 칸의 이름을 들고 제어 화면으로 가므로 1번 코드는 바꾸지 않는다.
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
        }

        // 21. 앱이 시작되면(onCreate) 저장해 둔 마지막 장치 이름을 꺼내 보여 준다(11주차 2일차).
        //     저장한 적이 없으면 기본값 ""이 온다. getString은 String?를 돌려주므로 ?: ""로 null을 막는다.
        val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
        val lastName = prefs.getString("last", "") ?: ""
        if (lastName.isEmpty()) {
            binding.lastDeviceText.text = "마지막 장치: 없음"
        } else {
            binding.lastDeviceText.text = "마지막 장치: $lastName"
        }

        // 22. [연락처 보기] 버튼: READ_CONTACTS가 이미 허용이면 바로 보여 주고, 아니면 요청 창을 띄운다(11주차 2일차, 시연·선택 실습).
        binding.contactsButton.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                showContacts()
            } else {
                contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))
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

    // 23. ContactsReader로 연락처 이름을 읽어 AlertDialog 목록으로 보여 준다(11주차 2일차).
    //     0건이면 목록 대신 안내 문구를 보여 준다. 0건은 실패가 아니다(에뮬레이터는 처음에 연락처가 없다).
    private fun showContacts() {
        val names = ContactsReader.names(contentResolver)
        if (names.isEmpty()) {
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setMessage("연락처가 0건입니다. 연락처 앱에서 한 명을 추가한 뒤 다시 눌러 보세요.")
                .setPositiveButton("확인", null)
                .show()
        } else {
            // setItems는 배열을 받으므로 toTypedArray()로 목록(List)을 배열(Array)로 바꿔 넘긴다.
            AlertDialog.Builder(this)
                .setTitle("연락처")
                .setItems(names.toTypedArray(), null)
                .setPositiveButton("닫기", null)
                .show()
        }
    }
}
```

### 20. 캡처 3과 제출하기

실기기가 없는 학생은 아래 가운데 하나를 **캡처 3**으로 찍는다.

1. 연락처 이름 목록이 보이는 `연락처` 대화상자(가장 좋다)
2. `연락처가 0건입니다. …` 대화상자
3. `연락처 권한 없음` 대화상자

제출물은 네 가지다.

1. `MainActivity.kt`
2. 캡처 1: 목록에 장치 이름 세 줄이 쌓인 연결 화면(1일차 8단계)
3. 캡처 2: 앱을 껐다 켠 뒤 `마지막 장치: …`가 보이는 화면(13단계)
4. 캡처 3: 실기기에서 앱이 실행된 화면(14단계). 실기기가 없으면 위의 연락처 대화상자

캡처에 계정 이름·알림 내용·실제 연락처 번호 같은 개인정보가 보이지 않게 한다. 실제 폰의 연락처 목록을 찍을 때는 이름이 보이지 않게 가리거나 에뮬레이터에서 찍는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
