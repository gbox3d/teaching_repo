# 12주차 따라하기 — 보드 검색과 연결

11주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
11주차 프로젝트가 없거나 실행되지 않으면 강의자에게 11주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에는 제공 라이브러리 `bleuno` 패키지(파일 8개)를 새로 붙여 넣고, `MainActivity.kt`(1·2일차), `ConnViewModel.kt`(1일차 import 한 줄), `ControlActivity.kt`·`activity_main.xml`·`activity_control.xml`·`strings.xml`(2일차)을 고친다.
11주차 `ConnState.kt`·`Permissions.kt`는 1일차에, `ConnViewModel.kt`는 2일차에 지운다. `AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml`은 11주차 그대로 둔다. 전체 내용은 [10단계](#10-바꾸지-않는-파일-확인하기)와 [부록](#부록--제공-bleuno-파일-전체)에 있다.

에뮬레이터는 API 33 이상 이미지를 쓴다. 보드 없이 가짜 클라이언트(Fake)로 끝까지 할 수 있고, 실보드는 실기기에서만 연결된다.
bleuno [README 6절](../../bleuno/README.md#6-사용-예--검색--연결--상태-표시--명령--응답)의 사용 예는 요약이다. 이 따라하기와 `examples/day2`가 기준이다.

## 1일차

### 1. 11주차 프로젝트 열고 실행하기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 연결 화면에 아래가 보이면 시작할 수 있다. `마지막 장치`와 배터리 숫자는 내 기기에 따라 다르다.

```text
Smart I/O Controller
마지막 장치: 없음
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
연결 안 됨
검색된 장치
[연결]
[권한 확인]
[연락처 보기]
배터리 100% · 충전 중
```

3. [검색]을 한 번 눌러 11주차처럼 `연결 중… 5`와 함께 목록에 `ESP32_BLE_A`·`B`·`C`가 1초마다 들어오는지 본다. 이 가짜 이름을 오늘 진짜 검색으로 바꾼다.
4. Logcat 창의 필터에 `package:mine tag:BLE`를 넣어 둔다. 지금은 아무 줄도 없다.

### 2. bleuno 패키지 넣기

1. 제공 파일 8개를 받는다. [bleuno/src](../../bleuno/src) 폴더(또는 [examples/day1/bleuno](examples/day1/bleuno))의 `Bleuno.kt`, `BleunoClient.kt`, `BleunoDevice.kt`, `BleunoMessage.kt`, `ConnState.kt`, `FakeBleunoClient.kt`, `PermissionHelper.kt`, `RealBleunoClient.kt`다. 내용은 [부록](#부록--제공-bleuno-파일-전체)에도 있다.
2. Project 창에서 `app › kotlin+java › com.example.smartio`를 오른쪽 클릭 → **New › Package**를 고른다.
3. 이름 칸이 `com.example.smartio.bleuno`가 되게 끝에 `bleuno`를 쓰고 Enter.
4. 파일 탐색기(맥은 Finder)에서 받은 8개 파일을 모두 골라 복사(Ctrl+C, 맥 ⌘+C)하고, Android Studio Project 창의 `bleuno` 패키지를 한 번 누른 뒤 붙여 넣는다(Ctrl+V, 맥 ⌘+V). 복사 확인 창이 뜨면 [OK].
5. `bleuno` 아래에 8개 파일이 보이고, 아무 파일이나 열어 첫 줄이 `package com.example.smartio.bleuno`인지 본다.
6. 실행한다. 화면과 동작은 1단계와 같다. 빌드만 되면 된다.

- 라이브러리는 `com.example.smartio.bleuno`라는 **다른 패키지**에 있다. 그래서 `MainActivity.kt`에서 쓰려면 import가 필요하다.
- 앱 코드는 `BleunoClient`(할 수 있는 일 목록)만 보고 쓴다. 실제 보드용 `RealBleunoClient`와 연습용 `FakeBleunoClient`가 같은 일을 하므로 한 줄(`useFake`)만 바꿔 오갈 수 있다.
- `RealBleunoClient.kt` 안에 특강에서 본 `BluetoothGatt` 콜백이 모두 들어 있다. 이번 학기에는 열어서 읽기만 하고 고치지 않는다.

### 3. 11주차 ConnState.kt·Permissions.kt 지우기

11주차 두 파일은 라이브러리에 같은 일을 하는 것이 들어 있어 지운다.

1. Project 창에서 `com.example.smartio` 바로 아래의 `ConnState.kt`(bleuno 안의 것이 **아니다**)를 오른쪽 클릭 → **Delete** → [OK]. 사용하는 곳이 있다는 창이 뜨면 그대로 지운다.
2. `MainActivity.kt`의 7번 `when` 안 `ConnState`가 빨간색이 된다. 빨간 `ConnState`에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter) → **Import** → `com.example.smartio.bleuno.ConnState`를 고른다.
3. `ConnViewModel.kt`를 열어 같은 방법으로 import한다. `import androidx.lifecycle.viewModelScope` 아래에 한 줄이 생긴다.

```kotlin
import com.example.smartio.bleuno.ConnState
```

4. 같은 방법으로 `com.example.smartio` 바로 아래의 `Permissions.kt`를 지운다.
5. `MainActivity.kt`에서 빨간색이 된 `blePermissions()` **두 곳**을 `PermissionHelper.required()`로 바꾸고, 빨간 `PermissionHelper`에 Alt+Enter → `com.example.smartio.bleuno.PermissionHelper`를 import한다.
   - `// 12.` [권한 확인] 블록 안의 한 줄

```kotlin
                permissionLauncher.launch(PermissionHelper.required())
```

   - `// 13.` `hasBlePermissions()` 함수의 `for` 줄. 주석은 아래처럼 바꿔도 되고 그대로 둬도 된다.

```kotlin
    // 13. PermissionHelper.required()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    //     12주차 1일차: 10주차 blePermissions()를 bleuno 패키지의 PermissionHelper.required()로 바꿨다. 돌려주는 권한 목록은 같다.
    private fun hasBlePermissions(): Boolean {
        for (permission in PermissionHelper.required()) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        return true
    }
```

6. 실행한다. 11주차와 똑같이 [검색] → 카운트다운과 A·B·C 목록, [권한 확인] → `권한 OK`가 되면 성공이다.

- bleuno의 `ConnState`는 11주차 파일과 이름·값(`연결 안 됨`·`연결 중`·`서비스 확인 중`·`준비됨`·`끊김`)이 같다. 그래서 import만 바꾸면 된다. 11주차 `ConnState.kt` 주석에 "12주차에는 이 파일 대신 import만 바꾼다"라고 적어 두었던 일이다.
- `PermissionHelper.required()`는 10주차 `blePermissions()`와 같은 권한 목록(Android 12 이상 `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT`, 그 이하 `ACCESS_FINE_LOCATION`)을 돌려준다.
- 한 곳만 바꾸고 빌드하면 `Unresolved reference 'blePermissions'.` 오류가 남는다. 그 위에 `Method 'iterator()' is ambiguous…`와 긴 목록이 먼저 보여도 아래의 `Unresolved reference` 줄을 먼저 읽는다.

완성한 `ConnViewModel.kt` 전체는 아래와 같다. import 한 줄 말고는 11주차 그대로다. 같은 코드가 [examples/day1/ConnViewModel.kt](examples/day1/ConnViewModel.kt)에 있다.

```kotlin
package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.smartio.bleuno.ConnState
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

### 4. client 받기

1. `MainActivity.kt`의 클래스 안, `contactsLauncher` 블록을 닫는 `}` **아래**에 한 줄을 비우고 두 변수를 넣는다. `onCreate` **밖**이다.

```kotlin
    // 12주차 1일차: true면 보드 없이 연습하는 가짜 클라이언트, false면 실제 보드에 연결하는 클라이언트를 만든다.
    // 실기기와 보드가 있으면 이 한 줄만 false로 바꾼다. 나머지 코드는 그대로 둔다.
    private val useFake = true

    // 12주차 1일차: 보드와 이야기하는 클라이언트. onCreate에서 받아 온다(24번). lateinit은 binding과 같은 틀이다.
    private lateinit var client: BleunoClient
```

2. `onCreate` 안, insets 블록(`ViewCompat.setOnApplyWindowInsetsListener`)을 닫는 `}` **아래**, `// 1.` [연결] 블록 **위**에 한 줄을 비우고 넣는다.

```kotlin
        // 24. 앱 전체가 함께 쓰는 클라이언트를 받는다(12주차 1일차).
        //     이미 만들어 둔 것이 있으면(회전해서 onCreate가 다시 불린 경우) 그것을 그대로 쓰고, 없을 때만 Bleuno.create로 만든다.
        client = Bleuno.client ?: Bleuno.create(this, useFake)
```

3. 빨간 글자를 차례로 Alt+Enter → Import로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `BleunoClient` | `com.example.smartio.bleuno.BleunoClient` |
| `Bleuno` | `com.example.smartio.bleuno.Bleuno` |

4. 실행한다. 화면은 그대로다. 빌드만 되면 된다.

- `private val useFake = true`: 보드 없이 연습하는 가짜 클라이언트를 쓰겠다는 스위치다. 실기기와 보드가 있으면 이 한 줄만 `false`로 바꾼다.
- `private lateinit var client: BleunoClient`: 4주차 `binding`처럼 `onCreate`에서 채우는 변수다. `lateinit`은 "나중에 채운다"는 약속이라, 채우는 줄(24번)을 빠뜨려도 빌드는 되고 쓰는 순간 앱이 멈춘다.
- `Bleuno.client ?: Bleuno.create(this, useFake)`: `Bleuno.client`는 앱 전체가 함께 쓰는 client를 보관하는 칸이고 처음에는 `null`이다. 3주차 `?:`로 "있으면 그것, 없으면 만들기"를 한 줄에 쓴다. `create`는 만든 것을 `Bleuno.client`에 넣은 뒤 돌려준다.
- 회전하면 `onCreate`가 다시 불린다. 그때 새로 만들지 않고 이미 만든 client를 그대로 쓰므로, 2일차에 연결한 상태가 회전해도 이어진다.

### 5. 블루투스 켜기 요청 틀 만들기

1. 4단계에서 넣은 `client` 줄 **아래**에 한 줄을 비우고 요청 틀을 넣는다. `onCreate` **밖**이다.

```kotlin
    // 12주차 1일차: 블루투스 켜기 요청 창을 띄우고 결과를 받는 틀. 10주차에 본 setResult 결과 받기 틀(StartActivityForResult)과 같다.
    // 사용자가 요청 창에서 [허용]을 누르면 resultCode가 RESULT_OK로 돌아온다.
    private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == RESULT_OK) {
            Toast.makeText(this, "블루투스 켜짐. [검색]을 다시 누르세요", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "블루투스를 켜야 검색할 수 있습니다", Toast.LENGTH_SHORT).show()
        }
    }
```

2. 새로 import할 것은 없다(`ActivityResultContracts`·`Toast`는 10주차부터 있다). 실행한다. 화면은 그대로다.

- 10주차 2일차에 시연한 `setResult` 결과 받기 틀(`StartActivityForResult`)과 같은 모양이다. 10주차 `permissionLauncher`처럼 화면이 시작되기 전에 만들어야 하므로 클래스 변수 자리에 둔다.
- 사용자가 요청 창에서 [허용]을 누르면 `result.resultCode`가 `RESULT_OK`로 돌아온다. 이번에는 `result.data`는 쓰지 않는다.
- 요청 창은 6단계 [검색]에서 띄운다.

### 6. [검색]과 [중지] 바꾸기

1. `// 3.` [검색] 블록을 **통째로** 아래 코드로 바꾼다. 11주차의 `viewModel.startScan()`과 `// 17.` 코루틴(`deviceJob = lifecycleScope.launch { … }`)은 모두 지워진다.

```kotlin
        // 3. [검색] 버튼: 권한과 블루투스를 확인한 뒤 5초 동안 보드를 검색한다(12주차 1일차에 가짜 검색을 교체).
        binding.scanButton.setOnClickListener {
            // 25. 권한이 없으면 10주차 흐름대로 요청 창을 띄우고, 블루투스가 꺼져 있으면 켜 달라고 요청한다(12주차 1일차).
            //     블루투스 켜기 요청 창도 권한이 있어야 띄울 수 있으므로 권한을 먼저 확인한다.
            if (hasBlePermissions() == false) {
                permissionLauncher.launch(PermissionHelper.required())
            } else if (PermissionHelper.isBluetoothEnabled(this) == false) {
                bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
            } else {
                // 26. 목록을 비우고, 버튼과 ProgressBar를 "검색 중" 모양으로 바꾼다(12주차 1일차).
                //     검색할 때마다 목록을 새로 채우므로 [검색]을 여러 번 눌러도 같은 이름이 두 번 들어가지 않는다.
                devices.clear()
                adapter.notifyDataSetChanged()
                binding.scanButton.isEnabled = false
                binding.stopButton.isEnabled = true
                binding.scanProgress.visibility = View.VISIBLE
                binding.stateText.text = "검색 중…"
                // 27. 5초 동안 검색한다. 보드를 찾을 때마다 onFound { }가, 검색이 끝나면 onFinished { }가 불린다(12주차 1일차).
                //     둘 다 메인 스레드에서 불리므로 안에서 View를 바로 바꿔도 된다. 한 번 검색하는 동안 같은 보드는 한 번만 알려 준다.
                client.startScan(5000, onFound = { device ->
                    val name = device.name
                    val address = device.address
                    // 28. 이름이 "ESP32_BLE"로 시작하는 보드만 목록에 "이름 (주소)"로 넣는다(12주차 1일차).
                    //     라이브러리도 같은 기준으로 거르지만, 앱에서 startsWith로 한 번 더 확인한다.
                    if (name.startsWith("ESP32_BLE")) {
                        devices.add("$name ($address)")
                        adapter.notifyDataSetChanged()
                        val count = devices.size
                        Log.d("Scan", "찾음: $name ($address), 장치 수: $count")
                    }
                }, onFinished = {
                    // 29. 검색이 끝나면(5초가 지났거나 [중지]) 버튼과 ProgressBar를 되돌리고 찾은 개수를 보여 준다(12주차 1일차).
                    binding.scanButton.isEnabled = true
                    binding.stopButton.isEnabled = false
                    binding.scanProgress.visibility = View.GONE
                    val count = devices.size
                    binding.stateText.text = "검색 완료 · 장치 수: $count"
                })
            }
        }
```

2. `// 4.` [중지] 블록도 통째로 바꾼다. `viewModel.stopScan()`과 `// 18.` `deviceJob?.cancel()`이 지워진다.

```kotlin
        // 4. [중지] 버튼: 검색을 바로 멈춘다(12주차 1일차에 가짜 검색 취소를 교체).
        binding.stopButton.setOnClickListener {
            // 30. 검색을 멈춘다. 이때도 onFinished가 한 번 불려 29번이 버튼·ProgressBar를 되돌린다(12주차 1일차).
            client.stopScan()
        }
```

3. 클래스 변수 자리의 `// 11주차 1일차: …` 주석과 `private var deviceJob: Job? = null` 두 줄을 지운다. 파일 위쪽에서 회색이 된 `import kotlinx.coroutines.Job`, `import kotlinx.coroutines.delay`도 지운다.
4. 빨간 `BluetoothAdapter`에 Alt+Enter → `android.bluetooth.BluetoothAdapter`를 import한다. `View`·`Log`·`Intent`는 앞 주차에 이미 import했다.
5. 실행하고 [검색]을 누른다. Logcat 필터는 `package:mine tag:BLE`다.

| 상황 | 화면 |
|---|---|
| 권한이 아직 없을 때 [검색] | 시스템 권한 창("근처 기기", 문구는 OS마다 다름) → [허용] → Toast `권한 OK`. 검색은 아직 시작하지 않는다 → [검색]을 다시 누른다 |
| 블루투스가 꺼져 있을 때 [검색] | 블루투스 켜기 요청 창 → [허용] → Toast `블루투스 켜짐. [검색]을 다시 누르세요` / [거부] → Toast `블루투스를 켜야 검색할 수 있습니다` |
| 권한·블루투스 OK에서 [검색] | 상태 `검색 중…`, ProgressBar, [검색] 꺼짐·[중지] 켜짐. 1초 뒤 `ESP32_BLE_FAKE1 (00:11:22:33:44:01)`, 2초 뒤 `ESP32_BLE_FAKE2 (00:11:22:33:44:02)` |
| 5초 뒤 | ProgressBar 사라짐, [검색] 켜짐·[중지] 꺼짐, `검색 완료 · 장치 수: 2` |
| [검색] 뒤 1.5초쯤 [중지] | 곧바로 `검색 완료 · 장치 수: 1`(FAKE1만 남음) |
| 목록에서 FAKE2 줄 누르기 | 장치 이름 칸 `ESP32_BLE_FAKE2 (00:11:22:33:44:02)`, Toast `선택: …`(11주차 19번 그대로. 연결은 2일차) |

Logcat `tag:BLE`에는 아래 순서로 찍힌다. [중지]를 누르면 `scan timeout` 줄 없이 `stopScan(가짜)`가 찍힌다.

```text
startScan(가짜): 5000ms 동안 검색
onScanResult(가짜): ESP32_BLE_FAKE1
onScanResult(가짜): ESP32_BLE_FAKE2
scan timeout(가짜) (5000ms)
stopScan(가짜)
```

블루투스 켜기 요청 창을 보려면 에뮬레이터 화면 위에서 아래로 끌어 빠른 설정을 열고 블루투스를 끈 뒤 [검색]을 누른다.

- **확인 순서 25번**: `if / else if / else`는 1주차 `if/else`에 조건을 이어 붙인 모양이다. 위에서부터 처음 맞는 한 곳만 실행한다. 권한 → 블루투스 순서인 까닭은 Android 12 이상에서 블루투스 켜기 요청 창도 권한이 있어야 띄울 수 있기 때문이다. `== false`는 "아니면"이라는 뜻이다.
- **26번**: 5주차 `isEnabled`·`visibility`와 같은 "검색 중" 모양이다. 검색할 때마다 `devices.clear()`로 비우므로 같은 이름이 두 번 들어가지 않는다.
- **27번** `client.startScan(5000, onFound = { device -> … }, onFinished = { … })`: 첫 값은 **밀리초**라서 `5000`이 5초다. `onFound =`·`onFinished =`는 두 람다 가운데 어느 칸에 넣는지 붙인 이름표다. `{ device -> }`는 10주차 `{ result -> }`처럼 넘어오는 값에 이름을 붙인 것이다.
- `onFound`·`onFinished`는 라이브러리가 메인 스레드에서 부른다. 그래서 5주차 `runOnUiThread` 없이 안에서 View를 바로 바꾼다.
- **28번**: `device.name`·`device.address`는 `BleunoDevice`(이름·주소·신호 세기를 묶어 둔 `data class`)의 값이다. `name.startsWith("ESP32_BLE")`는 이름이 `ESP32_BLE`로 시작하면 `true`다. 라이브러리 안(`RealBleunoClient.kt`)에도 같은 확인이 있지만 앱에서 한 번 더 본다. `devices`는 글자 목록이라 `"$name ($address)"`로 글자를 만들어 넣는다.
- **30번**: [중지]에서 버튼을 되돌리는 코드를 쓰지 않는다. `stopScan()`이 `onFinished`를 한 번 부르므로 29번이 되돌린다.

### 7. 화면을 떠나면 검색 멈추기

1. `// 11.` `onStop()` 함수에서 `unregisterReceiver(batteryReceiver)` **아래**에 `client.stopScan()`을 넣는다. 주석 한 줄도 함께 넣는다. 함수 전체는 아래와 같다.

```kotlin
    // 11. 화면이 안 보이게 되면 등록을 푼다. onStart의 등록과 반드시 짝을 맞춘다(10주차 1일차).
    //     12주차 1일차: 검색도 여기서 멈춘다. 화면이 안 보이는 동안 검색이 끝나 onFinished(29번)가 보이지 않는 화면을 고치는 일을 막는다.
    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
        client.stopScan()
    }
```

2. 실행하고 [검색]을 누른 뒤 1초쯤 뒤에 홈으로 나간다. Logcat `tag:BLE`에 `stopScan(가짜)`가 찍히고 `scan timeout(가짜)` 줄은 없어야 한다.
3. 앱으로 돌아오면 [검색]이 켜져 있고 목록에는 떠나기 전에 찾은 줄만 남아 있다. [검색]을 다시 누르면 정상으로 새 검색이 된다.

- 10주차 "`onStart`에서 등록 ↔ `onStop`에서 해제" 짝 규칙과 같다. 시작한 검색은 화면이 안 보이게 될 때 멈춘다.
- 이 줄이 없으면 화면이 안 보이는 동안 검색이 끝나 29번이 보이지 않는 화면을 고치게 된다.
- `onStart`에서 검색을 다시 시작하지는 않는다. 검색은 [검색]을 누를 때만 시작한다.

완성한 `MainActivity.kt` 전체는 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다(352줄). 파일을 열어 내 코드와 위에서부터 한 블록씩 비교한다. 이번 단계까지 넣은 곳은 import 5줄(`BluetoothAdapter`·`Bleuno`·`BleunoClient`·`ConnState`·`PermissionHelper`), 클래스 변수 3개, 24번, 3·4번 블록, 11번 `onStop`, 12·13번의 `PermissionHelper.required()`다.

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
11주차까지의 코드(주석 1~23)가 내 코드와 조금 달라도 동작이 같으면 그대로 둔다. 1일차에는 상태가 늘 `연결 안 됨`이라 [다시 시도]·[해제]는 누를 일이 없다. 2일차에 정리한다.

### 8. startsWith 글자 바꿔 보기

한 곳만 바꾸고 실행한 뒤 반드시 되돌린다.

1. 28번의 `name.startsWith("ESP32_BLE")`에서 괄호 안 글자를 `"ESP32_BLE_FAKE2"`로 바꾸고 [검색]을 누른다. 목록에 `ESP32_BLE_FAKE2` 줄만 들어가고 `검색 완료 · 장치 수: 1`이 된다.
2. `"esp32_ble"`(소문자)로 바꾸고 [검색]을 누른다. 대소문자가 달라 목록에 아무것도 들어가지 않고 `검색 완료 · 장치 수: 0`이 된다.
3. 관찰한 결과를 [실습지](lab.md#4-화면을-떠나면-검색-멈추기와-startswith-바꿔-보기)의 표에 적고 `"ESP32_BLE"`로 되돌린다.

Logcat `tag:BLE`의 `onScanResult(가짜)` 줄은 세 경우 모두 두 번 찍힌다. 라이브러리는 보드를 찾아 알려 주고, 목록에 넣을지는 앱의 `startsWith`가 정한다.

### 9. 캡처하고 실제 보드로 바꿔 보기

1. [검색]을 누르고 2초 넘게 기다려 `검색된 장치` 아래 `ESP32_BLE_FAKE1 (00:11:22:33:44:01)`·`ESP32_BLE_FAKE2 (00:11:22:33:44:02)`가 보이는 **세로 화면**을 캡처한다. **이 화면이 제출 캡처 1이다.** 캡처한 뒤 화면을 돌리면 11주차처럼 목록이 비워진다.
2. 실기기와 보드가 있으면 보드에 전원을 넣고 LED가 **파랑 깜빡임**인지 본다. 빨강이면 부팅 중이니 잠깐 기다린다.
3. `private val useFake = true`를 `false`로 바꾸고, Android Studio 위쪽 기기 목록에서 내 폰을 골라 `Run ▶`.
4. [검색] → (권한·블루투스 확인) → 목록에 `ESP32_BLE7C9EBF (84:F7:03:…)`처럼 `ESP32_BLE` + 칩 ID 줄이 보이면 성공이다. 칩 ID와 주소는 보드마다 다르다. 실보드 줄이 보이는 캡처를 캡처 1로 내도 된다.

실보드일 때 Logcat `tag:BLE`에는 아래 모양으로 찍힌다.

```text
startScan: 5000ms 동안 "ESP32_BLE"로 시작하는 기기 검색
onScanResult: ESP32_BLE7C9EBF 84:F7:03:xx:xx:xx rssi=-48
scan timeout (5000ms)
stopScan: 찾은 기기 1개
```

- 에뮬레이터에서 `useFake = false`로 실행하면 주변에 보드가 없어 늘 0개다. 에뮬레이터로 돌아갈 때는 `true`로 되돌린다.
- 보드가 목록에 안 뜨면 파랑 깜빡임인지(다른 폰이 이미 연결하면 광고를 멈춘다), 블루투스가 켜져 있는지, Android 11 이하면 위치가 켜져 있는지 본다.
- 프로젝트는 2일차에 그대로 이어서 쓴다.

### 10. 바꾸지 않는 파일 확인하기

아래 파일은 11주차에 만든 그대로이며 이번 주 1일차에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.
같은 코드가 [examples/day1](examples/day1)에 있다. `AndroidManifest.xml`, `ContactsReader.kt`, `themes.xml`은 2일차에도 바꾸지 않는다.

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). BLE를 쓰는 선언(`bluetooth_le`)과 권한(`BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT`, Android 11 이하용 세 줄)은 10주차 2일차에 이미 넣었다. 있는지만 확인한다.

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

`ControlActivity.kt` — [examples/day1/ControlActivity.kt](examples/day1/ControlActivity.kt). 2일차 14단계에서 고친다.

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

`activity_main.xml` — [examples/day1/activity_main.xml](examples/day1/activity_main.xml). 2일차 11단계에서 고친다.

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

`activity_control.xml` — [examples/day1/activity_control.xml](examples/day1/activity_control.xml). 2일차 11단계에서 고친다.

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

`strings.xml` — [examples/day1/strings.xml](examples/day1/strings.xml). 2일차 11단계에서 고친다.

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

### 11. [제어 화면] 버튼과 상태 글자 자리 만들기

오늘 쓸 글자 두 개, 버튼 하나, TextView 하나를 XML에 먼저 모두 넣는다.

1. `strings.xml`의 `show_contacts` 줄 **아래**에 두 줄을 넣는다.

```xml
    <string name="show_contacts">연락처 보기</string>
    <string name="control_screen">제어 화면</string>
    <string name="state_unknown">상태: ?</string>
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
    <string name="control_screen">제어 화면</string>
    <string name="state_unknown">상태: ?</string>
</resources>
```

2. `activity_main.xml`에서 `connectButton` 버튼 **아래**, `retryButton` 버튼 **위**에 버튼을 넣는다.

```xml
    <Button
        android:id="@+id/controlButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:enabled="false"
        android:text="@string/control_screen" />
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

3. `activity_control.xml`에서 `deviceText` TextView **아래**, `pinEdit` **위**에 TextView를 넣는다.

```xml
    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_unknown"
        android:textSize="18sp" />
```

전체는 아래와 같다. 같은 코드가 [examples/day2/activity_control.xml](examples/day2/activity_control.xml)에 있다.

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

4. 실행한다. 연결 화면의 [연결] 아래에 **꺼진** [제어 화면]이 보이고, 장치 이름을 넣고 [연결]로 간 제어 화면의 `장치: …` 아래에 `상태: ?`가 보이면 된다.

- `android:enabled="false"`: 처음에는 꺼진 채 시작한다(4주차 `stopButton`과 같다). `준비됨`이 되면 코드가 켠다.
- 제어 화면 TextView의 id도 `stateText`다. 레이아웃 파일이 달라 binding도 따로 만들어지므로(`ActivityControlBinding`) 연결 화면의 `stateText`와 겹치지 않는다.

### 12. 상태를 client에서 받고 ConnViewModel 지우기

7주차부터 연결 상태는 `ConnViewModel`이 가짜 카운트다운으로 만들었다. 오늘부터는 라이브러리가 진짜 연결 상태를 만들어 주므로 `client.connectionState`를 받고 ViewModel은 지운다.

1. `MainActivity.kt`의 `// 7.` 상태 collect 블록을 통째로 아래 코드로 바꾼다. 바뀌는 곳은 다섯 군데다. 주석 `37.` 한 줄 추가, `viewModel.state.collect` → `client.connectionState.collect`, 8번 아래 `controlButton` 끄기 한 줄, `CONNECTING` 가지의 `stopButton` 켜기 줄을 주석 두 줄로, `READY` 가지에 `controlButton` 켜기.

```kotlin
        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        //    37. 7주차 viewModel.state 대신 보드와의 실제 연결 상태 client.connectionState를 받는다. 틀은 그대로다(12주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                client.connectionState.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.controlButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            // 연결 중에는 버튼을 모두 꺼 둔다. [중지]는 이제 검색 멈춤이라 켜지 않는다(12주차 2일차).
                            // 보드가 응답하지 않으면 한참(보통 30초쯤) 뒤 "끊김"이 되어 [검색]·[다시 시도]가 다시 켜진다.
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                            // 준비됨일 때만 [제어 화면]을 누를 수 있다(12주차 2일차).
                            binding.controlButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }
```

2. 바로 아래의 `// 9.` 남은 초 collect 블록을 **통째로** 지운다. 지울 블록은 아래와 같다.

```kotlin
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
```

3. `// 5.` [다시 시도] 블록과 `// 6.` [해제] 블록을 아래처럼 바꾼다.

```kotlin
        // 5. [다시 시도] 버튼: [검색]을 한 번 더 누른 것과 같다(12주차 2일차에 가짜 연결 재시도를 교체).
        binding.retryButton.setOnClickListener {
            // 35. performClick()은 코드로 버튼을 누른다. 3번 [검색]이 권한·블루투스 확인부터 그대로 다시 실행된다(12주차 2일차).
            binding.scanButton.performClick()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            // 36. 보드와의 연결을 끊는다. 끊기면 connectionState가 "연결 안 됨"이 되어 7번이 화면을 고친다(12주차 2일차).
            client.disconnect()
        }
```

4. 클래스 변수 자리 맨 위의 `// 7주차 1일차: …` 주석과 `private val viewModel: ConnViewModel by viewModels()` 두 줄을 지운다. 파일 위쪽에서 회색이 된 `import androidx.activity.viewModels`도 지운다.
5. Project 창에서 `ConnViewModel.kt`를 오른쪽 클릭 → **Delete** → [OK].
6. 실행한다. 앱 시작 화면은 상태 `연결 안 됨`, [검색]만 켜짐, [제어 화면] 꺼짐이다. [검색]은 1일차처럼 FAKE1·FAKE2를 찾는다. 목록 줄을 눌러도 아직 연결하지 않는다(13단계).

- 틀(`lifecycleScope.launch` · `repeatOnLifecycle(Lifecycle.State.STARTED)` · `collect`)과 `when` 다섯 가지는 7주차 그대로다. 받는 대상만 `client.connectionState`로 바뀌었다. 값은 bleuno `ConnState`의 문자열 다섯 개라서 `stateText`에 그대로 들어간다.
- `CONNECTING`: 7주차에는 [중지]로 카운트다운을 멈출 수 있었지만 12주차 [중지]는 검색 멈춤이다. 그래서 연결 중에는 7번이 켜는 버튼([검색]·[중지]·[해제]·[제어 화면])이 모두 꺼지고 ProgressBar만 돈다. 7번이 건드리지 않는 [연결]·[권한 확인]·[연락처 보기]는 그대로 켜져 있다. 보드가 응답하지 않으면 한참(보통 30초쯤) 뒤 `끊김`이 된다.
- `READY`: [해제]와 [제어 화면]을 켠다. `준비됨`이 아닐 때는 8번에서 끈 그대로다.
- `// 35.` `performClick()`은 코드로 버튼을 누른다. [다시 시도]를 누르면 [검색]을 누른 것과 똑같이 권한·블루투스 확인부터 다시 한다.
- `// 36.` `client.disconnect()`: 연결을 끊는다. 끊기면 `connectionState`가 `연결 안 됨`이 되어 7번이 화면을 고친다.
- `viewModel`에 빨간 줄이 남아 있으면 5·6·7·9번 가운데 아직 안 바꾼 곳이 있다.

### 13. 목록 줄을 누르면 연결하기

1. `onCreate` 안, `// 16.` 어댑터 블록(`binding.deviceList.adapter = adapter`) **아래**, `// 3.` [검색] 블록 **위**에 한 줄을 비우고 주소 목록을 만든다.

```kotlin
        // 31. 찾은 보드의 주소를 목록 줄과 같은 순서로 담는다. 줄을 누르면 같은 번호의 주소로 연결한다(12주차 2일차).
        val addresses = mutableListOf<String>()
```

2. [검색] 블록의 `// 26.` 부분, `adapter.notifyDataSetChanged()` 줄 **아래**에 `// 32.` 세 줄을 넣는다.

```kotlin
                devices.clear()
                adapter.notifyDataSetChanged()
                // 32. 주소 목록도 함께 비우고, 앞에서 보였을 수 있는 [다시 시도]를 숨긴다(12주차 2일차).
                addresses.clear()
                binding.retryButton.visibility = View.GONE
```

3. `onFound` 안, `devices.add("$name ($address)")` 줄 **아래**에 `// 33.` 두 줄을 넣는다.

```kotlin
                    if (name.startsWith("ESP32_BLE")) {
                        devices.add("$name ($address)")
                        // 33. 같은 순서로 주소도 넣는다. devices의 0번 줄 ↔ addresses의 0번 주소(12주차 2일차).
                        addresses.add(address)
```

4. `// 19.` 목록 누르기 블록의 `Toast.makeText(this, "선택: $name", …)` 줄 **아래**에 `// 38.` 부분을 넣는다. 블록 위의 `// 19.` 주석 두 줄은 11주차 그대로 두고, 그 아래 리스너 전체는 아래와 같다.

```kotlin
        binding.deviceList.setOnItemClickListener { _, _, position, _ ->
            val name = adapter.getItem(position) ?: ""
            binding.deviceNameEdit.setText(name)
            Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
            // 38. 누른 줄과 같은 번호의 주소를 꺼내 연결을 시작한다. 검색 중이면 먼저 검색을 멈춘다(12주차 2일차).
            //     get(번호)는 add로 넣은 순서대로 꺼낸다. 번호는 0부터 센다.
            val address = addresses.get(position)
            client.stopScan()
            client.connect(address)
        }
```

5. 새로 import할 것은 없다. 실행하고 Logcat 필터를 `package:mine tag:BLE`로 둔 뒤 [검색] → `ESP32_BLE_FAKE1` 줄을 누른다.

| 시간 | 연결 화면 |
|---|---|
| 누른 직후 | Toast `선택: ESP32_BLE_FAKE1 (00:11:22:33:44:01)`, 상태 `연결 중`, ProgressBar, [검색]·[중지]·[해제]·[제어 화면] 꺼짐 |
| 1초 뒤 | `서비스 확인 중`, [검색]·[중지]·[해제]·[제어 화면] 꺼짐 |
| 다시 1초 뒤 | `준비됨`, ProgressBar 사라짐, [해제]·[제어 화면] 켜짐, [검색] 꺼짐 |
| [해제] | `연결 안 됨`, [검색] 켜짐, [해제]·[제어 화면] 꺼짐 |

Logcat `tag:BLE`에는 아래 세 줄이 찍힌다. [해제]를 누르면 `disconnect(가짜) → 연결 안 됨`이 찍힌다.

```text
connectGatt(가짜): 00:11:22:33:44:01
onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중
onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨
```

`준비됨` 동안 10초마다 `onCharacteristicChanged(가짜): {"event":"input","index":0,"value":1}` 줄이 찍힌다. 14주차에 쓰는 입력 이벤트라 지금은 무시해도 된다.

- **BLE 연결은 목록 줄 탭이다.** [연결] 버튼은 4주차에 만든 "장치 이름만 들고 제어 화면으로 이동" 버튼 그대로라서 눌러도 보드와 연결하지 않는다.
- `devices`(목록에 보이는 글자)와 `addresses`(연결에 쓸 주소)를 **같은 순서의 목록 두 개**로 둔다. `devices`의 0번 줄과 `addresses`의 0번 주소가 같은 보드다. `addresses`도 `devices`처럼 [검색] 블록보다 위에 만들어야 리스너 안에서 쓸 수 있다.
- `addresses.get(position)`: 11주차 `adapter.getItem(position)`처럼 번호로 꺼낸다. 번호는 0부터 센다.
- `client.stopScan()`을 먼저 부른다. 특강 콜백 사슬도 "검색 멈춤 → 연결" 순서다. 검색 중에 누르면 `검색 완료 · 장치 수: N`이 잠깐 보인 뒤 `연결 중`으로 바뀐다.
- 11주차 세 줄(이름 칸 채우기·Toast)은 그대로 둔다. 장치 이름 칸의 글자는 14단계 [제어 화면]이 제어 화면으로 넘긴다.

### 14. [제어 화면]으로 같은 연결 보기

1. `MainActivity.kt`의 `// 19.` 목록 누르기 블록을 닫는 `}` **아래**, `// 21.` 마지막 장치 블록 **위**에 한 줄을 비우고 리스너를 넣는다.

```kotlin
        // 39. [제어 화면] 버튼: 준비됨일 때만 켜진다(7번). 장치 이름 칸의 이름을 들고 제어 화면으로 간다(12주차 2일차).
        //     연결은 Bleuno.client에 들어 있으므로 제어 화면에서도 같은 연결을 이어 쓴다.
        binding.controlButton.setOnClickListener {
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        }
```

2. `ControlActivity.kt`를 열고 `onCreate` 안, `// 3.` [뒤로] 블록을 닫는 `}` **아래**에 한 줄을 비우고 넣는다.

```kotlin
        // 4. 연결 화면이 만든 클라이언트를 Bleuno.client로 꺼내 연결 상태를 상단에 보여 준다(12주차 2일차).
        //    MainActivity 7번과 같은 collect 틀이다. client가 없으면(null) ?.에서 멈추고 "상태: ?"가 그대로 남는다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                }
            }
        }
```

3. `ControlActivity.kt`의 빨간 글자를 차례로 Alt+Enter → Import로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `lifecycleScope` | `androidx.lifecycle.lifecycleScope` |
| `launch` | `kotlinx.coroutines.launch` |
| `repeatOnLifecycle` | `androidx.lifecycle.repeatOnLifecycle` |
| `Lifecycle` | `androidx.lifecycle.Lifecycle` |
| `Bleuno` | `com.example.smartio.bleuno.Bleuno` |

4. 실행하고 [검색] → FAKE1 줄 누르기 → `준비됨` → [제어 화면]을 누른다. 제어 화면 상단에 `장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)`, 그 아래 `상태: 준비됨`이 보이면 성공이다.
5. [뒤로]로 돌아와 `준비됨`에서 에뮬레이터 화면을 돌린다. 상태 `준비됨`과 버튼 모양이 그대로이고, 장치 이름 칸 글자도 남는다. 목록만 11주차처럼 비워진다.

- `// 39.`는 4주차 [연결]과 같은 Intent 코드다. **연결 객체는 Intent로 넘기지 않는다.** 대신 `object Bleuno { var client }`에 하나 두고 두 화면이 같이 쓴다. 제어 화면으로 넘어가도 연결은 끊기지 않는다.
- 제어 화면 `// 4.`는 MainActivity 7번과 같은 collect 틀이다. `Bleuno.client`는 `BleunoClient?`(아직 안 만들었으면 `null`)라서 3주차 `?.`로 부른다. `!!`는 쓰지 않는다. client가 없으면 `?.`에서 멈추고 `상태: ?`가 그대로 남는다.
- 회전해도 `준비됨`이 이어지는 까닭은 4단계 `Bleuno.client ?:` 덕분이다. 새 화면의 `onCreate`가 이미 만든 client를 받고, collect가 마지막 상태를 바로 다시 받는다.

완성한 `ControlActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/ControlActivity.kt](examples/day2/ControlActivity.kt)에 있다.

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

        // 4. 연결 화면이 만든 클라이언트를 Bleuno.client로 꺼내 연결 상태를 상단에 보여 준다(12주차 2일차).
        //    MainActivity 7번과 같은 collect 틀이다. client가 없으면(null) ?.에서 멈추고 "상태: ?"가 그대로 남는다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                Bleuno.client?.connectionState?.collect { state ->
                    binding.stateText.text = "상태: $state"
                }
            }
        }
    }
}
```

### 15. 0개 안내와 위치 서비스 확인

1. [검색] 블록의 `onFinished` 안에서 `binding.stateText.text = "검색 완료 · 장치 수: $count"` **한 줄**을 `// 34.` `if … else`로 바꾼다. `onFinished` 부분 전체는 아래와 같다.

```kotlin
                }, onFinished = {
                    // 29. 검색이 끝나면(5초가 지났거나 [중지]) 버튼과 ProgressBar를 되돌리고 찾은 개수를 보여 준다(12주차 1일차).
                    binding.scanButton.isEnabled = true
                    binding.stopButton.isEnabled = false
                    binding.scanProgress.visibility = View.GONE
                    val count = devices.size
                    // 34. 하나도 못 찾았으면 안내하고 [다시 시도]를 보여 준다(12주차 2일차).
                    if (count == 0) {
                        binding.stateText.text = "장치를 찾지 못했습니다 — [다시 시도]를 누르세요"
                        binding.retryButton.visibility = View.VISIBLE
                    } else {
                        binding.stateText.text = "검색 완료 · 장치 수: $count"
                    }
                })
```

2. 실행하고 [검색]을 누른 직후 1초 안에 [중지]를 누른다. `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`와 [다시 시도] 버튼이 보인다. [다시 시도]를 누르면 `검색 중…`이 되고 [다시 시도]는 숨겨진다.
3. 클래스의 마지막 `}` **위**, `// 23.` `showContacts()` 함수 **아래**에 한 줄을 비우고 두 함수를 넣는다.

```kotlin
    // 40. 위치 서비스가 꺼져 있을 때 보여 주는 AlertDialog. [설정으로]를 누르면 위치 설정 화면을 연다(12주차 2일차).
    //     14번과 같은 모양이다. [검색]을 눌렀을 때(41번) 부르므로 늘 화면이 보이는 동안 뜬다.
    private fun showLocationDialog() {
        AlertDialog.Builder(this)
            .setTitle("위치 서비스가 꺼져 있습니다")
            .setMessage("Android 11 이하에서는 위치 서비스를 켜야 보드가 검색됩니다. 위치를 켠 뒤 [검색]을 다시 누르세요.")
            .setPositiveButton("설정으로") { _, _ ->
                val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
    }

    // 42. Android 11(API 30) 이하이면서 위치 서비스가 꺼져 있으면 true, 아니면 false(12주차 2일차).
    //     Android 12 이상은 위치 서비스와 상관없이 검색되므로 늘 false다. 13번 hasBlePermissions()처럼 true/false를 돌려준다.
    private fun isLocationOff(): Boolean {
        if (Build.VERSION.SDK_INT <= 30) {
            if (PermissionHelper.isLocationEnabled(this) == false) {
                return true
            }
        }
        return false
    }
```

4. 빨간 `Build`에 Alt+Enter → `android.os.Build`를 import한다(`Settings`·`AlertDialog`는 10주차에 import했다).
5. [검색] 블록의 25번 사슬에서 블루투스 가지(`bluetoothLauncher.launch(…)`) **아래**, `} else {` **위**에 `else if` 가지를 넣는다. 사슬 전체는 아래와 같다.

```kotlin
            if (hasBlePermissions() == false) {
                permissionLauncher.launch(PermissionHelper.required())
            } else if (PermissionHelper.isBluetoothEnabled(this) == false) {
                bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
            } else if (isLocationOff()) {
                // 41. Android 11(API 30) 이하에서 위치 서비스가 꺼져 있으면 검색해도 0개가 나온다. 검색하지 않고 안내창(40번)을 띄운다(12주차 2일차).
                //     권한 → 블루투스 → 위치 순서로 확인하고, 셋 다 통과해야 아래 else에서 검색한다. 위치 확인은 42번 함수가 한다.
                showLocationDialog()
            } else {
```

6. 실행한다. 에뮬레이터(API 33 이상)에서는 1일차와 똑같이 검색된다. Android 11 이하 실기기에서 위치를 끄고 [검색]을 누르면 검색하지 않고 곧바로 `위치 서비스가 꺼져 있습니다` 창이 뜨고, [설정으로]를 누르면 위치 설정 화면이 열린다.

- `// 34.` 0개는 앱 오류가 아니다. 보드가 꺼졌거나, 다른 폰에 이미 연결되어 광고를 멈췄거나, 너무 멀면 0개가 된다. 화면 문구의 `[다시 시도]`는 버튼 글자와 같다.
- `// 42.` `isLocationOff()`: Android 11(API 30) 이하에서는 위치 서비스가 꺼져 있으면 검색 결과가 0개다. Android 12 이상은 위치와 상관없이 검색되므로 늘 `false`다. `Build.VERSION.SDK_INT`는 10주차 `Permissions.kt`에서 본 기기 버전 숫자다. 13번 `hasBlePermissions()`처럼 참/거짓을 돌려주는 함수로 만들어 `else if` 조건에 바로 쓴다.
- `// 40.` `showLocationDialog()`: 10주차 14번 `showPermissionDialog()`와 같은 모양이다. `Settings.ACTION_LOCATION_SOURCE_SETTINGS`는 위치 설정 화면을 여는 암시적 Intent다.
- `// 41.` 확인 순서는 권한 → 블루투스 → 위치다. 안내창은 [검색]을 누른 순간(클릭 리스너)에만 띄운다. 5초 뒤에 불리는 `onFinished`에서 창을 띄우면 그사이 화면이 돌거나 닫혔을 때 사라진 화면에 창을 띄우게 된다. `onFinished` 안에서는 글자와 버튼만 바꾼다.

완성한 `MainActivity.kt` 전체는 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다(400줄). 파일을 열어 내 코드와 위에서부터 한 블록씩 비교한다. 2일차에 바뀐 곳은 import(`Build` 추가, `viewModels` 삭제), `viewModel` 선언 삭제, 31~39번, 5·6·7번, 9번 삭제, 40·41·42번이다.
1일차 코드와 무엇이 다른지 한눈에 보려면 Android Studio에서 두 파일을 골라 오른쪽 클릭 › **Compare Files**를 쓴다.

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
`AndroidManifest.xml`, `ContactsReader.kt`, `res/values/themes.xml`, `bleuno` 패키지 8개는 1일차와 같다([10단계](#10-바꾸지-않는-파일-확인하기), [부록](#부록--제공-bleuno-파일-전체)).

### 16. 캡처 2·보드 사진과 제출하기

1. [검색] → 줄 누르기 → `준비됨`이 된 연결 화면과 Logcat `package:mine tag:BLE`의 연결 줄이 함께 보이게 캡처한다. Android Studio의 기기 화면 창(Running Devices)과 Logcat 창을 나란히 두면 한 장에 담긴다. 어려우면 두 장으로 나눈다. **이 화면이 제출 캡처 2다.**
   - Fake: 13단계의 `(가짜)` 세 줄이 보이게 찍는다.
   - 실보드: 아래 줄들 가운데 `onConnectionStateChange` → `onMtuChanged` → `onServicesDiscovered`가 순서대로 보이게 찍는다.

```text
connectGatt(84:F7:03:xx:xx:xx, autoConnect=false)
onConnectionStateChange: status=0 newState=2
STATE_CONNECTED → requestMtu(185)
onMtuChanged: mtu=185 status=0 → discoverServices()
onServicesDiscovered: status=0
characteristic 확보: f6aa83ca-de53-46b4-bdea-28a7cb57942e
writeDescriptor(CCCD, ENABLE_NOTIFICATION_VALUE)
onDescriptorWrite: status=0 → 준비됨
```

2. 실보드와 연결했으면 파랑 깜빡임이 멈추고 LED가 모두 꺼진 보드를 사진으로 찍는다. [해제]를 누르면 Logcat에 `STATE_DISCONNECTED → gatt.close()`가 찍히고 보드가 다시 파랑 깜빡임으로 돌아간다. 보드·실기기가 없으면 사진은 생략한다.
3. 제출물은 다섯 가지다.
   1. `MainActivity.kt`
   2. `ControlActivity.kt`
   3. 캡처 1: 목록에 `ESP32_BLE…` 줄이 보이는 세로 연결 화면(9단계)
   4. 캡처 2: `준비됨` 화면과 Logcat `tag:BLE` 연결 줄(이 단계)
   5. 사진: 연결된 보드(보드가 없으면 생략)

- 실보드가 `연결 중`에서 오래 멈추면 보드 전원과 거리를 본다. 보드가 응답하지 않으면 보통 30초쯤 뒤 `끊김`이 되고 [검색]·[다시 시도]가 켜진다.
- 보드 하나에는 폰 하나만 연결된다. 옆 사람 보드와 이름(칩 ID)을 헷갈리지 않게 한다.
- 캡처와 사진에 계정 이름·알림 내용이 보이지 않게 한다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 예외 이름과 메시지를 읽는다.
보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다. Logcat `tag:BLE`의 마지막 줄이 어디까지 갔는지가 단서다.

## 부록 — 제공 bleuno 파일 전체

2단계에서 붙여 넣는 8개 파일이다. 모두 `app › kotlin+java › com.example.smartio › bleuno`에 둔다. 고치지 않는다.
같은 파일이 [bleuno/src](../../bleuno/src)와 [examples/day1/bleuno](examples/day1/bleuno)에 있다. 쓰는 방법은 [bleuno README](../../bleuno/README.md) 5절에 있다.

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
