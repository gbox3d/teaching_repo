# 12주차 실습 — 보드 검색과 연결

이번 주에는 11주차 `SmartIO`의 가짜 검색을 제공 라이브러리 bleuno의 검색으로 바꾸고, 2일차에는 목록 줄을 눌러 연결한 뒤 두 화면에서 연결 상태를 본다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 한 곳씩 바꿔 가며 화면과 Logcat `tag:BLE`가 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. 보드가 없는 학생은 `useFake = true`(Fake) 그대로 끝까지 할 수 있다.

## 1일차 — Fake로 보드 검색하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 11주차 `SmartIO`를 실행하고 `bleuno` 패키지에 제공 파일 8개를 붙여 넣는다. 11주차 `ConnState.kt`·`Permissions.kt`를 지우고 import와 이름을 고친다 |
| 10–20분 | `useFake`·`client`·`bluetoothLauncher`를 만들고 `onCreate`에서 client를 받는다 |
| 20–40분 | [검색]을 권한 → 블루투스 → `startScan` 순서로 바꾸고 [중지]는 `stopScan()`으로 바꾼다. 관찰표를 채운다 |
| 40–50분 | `onStop`에서 검색을 멈추고, `startsWith` 글자를 바꿔 본 뒤 되돌린다 |
| 50–60분 | 캡처 1을 찍는다. 보드와 실기기가 있으면 `useFake = false`로 실제 보드 이름을 확인한다 |

### 1. bleuno 넣고 11주차 파일 정리하기

1. `com.example.smartio` 아래에 **New › Package**로 `bleuno` 패키지를 만들고 [bleuno/src](../../bleuno/src)의 8개 파일을 붙여 넣는다. 방법은 [따라하기 2단계](walkthrough.md#2-bleuno-패키지-넣기)에 있다.
2. 11주차 `ConnState.kt`를 지운다. 빨간색이 된 `ConnState`(`MainActivity.kt`, `ConnViewModel.kt`)에 **Alt+Enter**(맥 ⌥+Enter)로 `com.example.smartio.bleuno.ConnState`를 import한다.
3. 11주차 `Permissions.kt`를 지운다. `blePermissions()`를 부르던 두 곳을 `PermissionHelper.required()`로 바꾸고 import한다.
4. 실행해 11주차와 똑같이 [검색] → `연결 중… 5` → 목록 A·B·C가 되면 다음으로 간다.

- 두 파일을 지운 뒤 빌드 창의 빨간 줄이 어느 파일 몇 번째 줄인지 먼저 읽는다. [막혔을 때](#막혔을-때)에 문구가 있다.
- `bleuno`의 `ConnState`는 11주차 파일과 이름·값이 같다. 그래서 import만 바꾸면 7번 `when`은 그대로 동작한다.

### 2. client와 블루투스 켜기 요청 틀

1. 클래스 변수 자리, `contactsLauncher` 블록 **아래**에 아래 모양을 채운다. `onCreate` **밖**이다.

```kotlin
private val useFake = true
private lateinit var client: BleunoClient
private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    // result.resultCode가 RESULT_OK면 Toast "블루투스 켜짐. [검색]을 다시 누르세요"
    // 아니면 Toast "블루투스를 켜야 검색할 수 있습니다"
}
```

2. `onCreate` 안, insets 블록 **아래**·`// 1.` [연결] 블록 **위**에서 client를 받는다.

```kotlin
// Bleuno.client가 이미 있으면 그것을, 없으면 Bleuno.create(this, useFake)로 만든 것을 client에 넣는다 (3주차 ?:)
```

- `Bleuno`, `BleunoClient`가 빨간색이면 Alt+Enter로 `com.example.smartio.bleuno`의 것을 import한다.
- 실행하면 화면은 1번과 같다. 빌드만 되면 된다.
- `Bleuno.client ?:`를 붙이는 까닭을 "회전"이라는 낱말을 넣어 한 문장으로 적는다.

### 3. [검색]·[중지] 바꾸기

1. `// 3.` [검색] 리스너의 **몸체 전체**(11주차 `viewModel.startScan()`과 17번 코루틴)를 지우고 아래 모양을 채운다.

```kotlin
if (hasBlePermissions() == false) {
    // 10주차처럼 권한 요청 창: permissionLauncher.launch(PermissionHelper.required())
} else if (PermissionHelper.isBluetoothEnabled(this) == false) {
    // 블루투스 켜기 요청 창: bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
} else {
    // devices 비우고 알리기, [검색] 끄기·[중지] 켜기, ProgressBar 보이기, 상태 "검색 중…"
    client.startScan(5000, onFound = { device ->
        // device.name이 "ESP32_BLE"로 시작하면 "이름 (주소)"를 devices에 넣고 알리기
        // Log.d("Scan", "찾음: 이름 (주소), 장치 수: N")
    }, onFinished = {
        // [검색] 켜기·[중지] 끄기, ProgressBar 숨기기, 상태 "검색 완료 · 장치 수: N"
    })
}
```

2. `// 4.` [중지] 리스너의 몸체(11주차 `viewModel.stopScan()`과 18번)를 `client.stopScan()` 한 줄로 바꾼다.
3. 쓰지 않게 된 `private var deviceJob: Job? = null`과 회색이 된 `import kotlinx.coroutines.Job`·`import kotlinx.coroutines.delay`를 지운다.
4. `BluetoothAdapter`가 빨간색이면 Alt+Enter로 `android.bluetooth.BluetoothAdapter`를 import한다.
5. 실행하고 Logcat 필터를 `package:mine tag:BLE`로 둔 뒤 표를 채운다.

| 조작 | 예상 화면 | 실제 화면 | Logcat `tag:BLE` 마지막 줄 |
|---|---|---|---|
| (처음) [검색] → 권한 창 [허용] |  |  |  |
| [검색] 후 5초 기다리기 |  |  |  |
| [검색] 후 1.5초쯤 [중지] |  |  |  |
| 빠른 설정에서 블루투스를 끄고 [검색] → 요청 창 [허용] |  |  |  |
| 이어서 [검색]을 두 번 연달아(끝난 뒤 다시) 누르기 |  |  |  |

- 권한을 허용하거나 블루투스를 켠 직후에는 검색이 자동으로 시작되지 않는다. 왜 그런지 3번 코드의 `if / else if / else`로 설명해 본다.
- [중지]에서 버튼을 되돌리는 코드를 쓰지 않았는데 [검색]이 다시 켜지는 까닭을 `onFinished`로 한 문장 적는다.
- 막히면 [1일차 완성 코드](examples/day1/MainActivity.kt)와 한 줄씩 비교한다.

### 4. 화면을 떠나면 검색 멈추기와 startsWith 바꿔 보기

1. `// 11.` `onStop()`의 `unregisterReceiver(batteryReceiver)` **아래**에 `client.stopScan()`을 넣는다.
2. [검색]을 누르고 1초쯤 뒤 홈 버튼을 누른다. Logcat `tag:BLE`에 `stopScan(가짜)`가 찍히고 `scan timeout(가짜)` 줄이 없으면 된다. 앱으로 돌아와 [검색]을 다시 누른다.
3. 28번의 `name.startsWith("ESP32_BLE")`에서 괄호 안 글자만 바꿔 실행하고 표를 채운 뒤 **되돌린다**.

| 괄호 안 글자 | 목록에 들어간 줄 | 상태 글자 |
|---|---|---|
| `"ESP32_BLE"` |  |  |
| `"ESP32_BLE_FAKE2"` |  |  |
| `"esp32_ble"` |  |  |

- 실보드 이름은 `ESP32_BLE7C9EBF`처럼 `ESP32_BLE` 바로 뒤에 칩 ID가 붙는다. 괄호 안을 `"ESP32_BLE_"`(밑줄까지)로 쓰면 실보드가 목록에 들어갈지 적어 본다.

### 5. 실제 보드로 바꿔 보기 (보드와 실기기가 있으면)

1. 보드에 전원을 넣고 LED가 **파랑 깜빡임**인지 본다(빨강이면 부팅 중이니 잠깐 기다린다).
2. `private val useFake = true`를 `false`로 바꾸고, Android Studio 기기 목록에서 **실기기**를 골라 `Run ▶`.
3. [검색] → 권한·블루투스 확인 → 목록에 `ESP32_BLE` + 칩 ID 줄이 보이면 성공이다. Logcat `tag:BLE`의 `onScanResult:` 줄도 본다.

| 항목 | 내 보드 |
|---|---|
| 목록에 보인 이름 |  |
| `onScanResult:` 줄의 `rssi=` 값(보드 가까이 / 1m 떨어져서) |  |

- 에뮬레이터에서 `useFake = false`로 실행하면 주변에 보드가 없어 늘 0개다. 에뮬레이터로 돌아갈 때는 `true`로 되돌린다.
- 다른 폰이 이미 그 보드에 연결되어 있으면 보드가 광고를 멈춰 목록에 보이지 않는다.

### 6. 오늘 확인할 것

- [ ] `bleuno` 패키지에 8개 파일이 있고, 11주차 `ConnState.kt`·`Permissions.kt`는 지웠다.
- [ ] [검색]을 누르면 `검색 중…`과 ProgressBar가 보이고, Fake면 1초·2초 뒤 `ESP32_BLE_FAKE1`·`ESP32_BLE_FAKE2`가 한 줄씩 들어온 뒤 `검색 완료 · 장치 수: 2`가 된다.
- [ ] [중지]를 누르면 곧바로 검색이 끝나고 [검색]이 다시 켜진다.
- [ ] 검색 중에 홈으로 나가면 Logcat에 `stopScan(가짜)`가 찍힌다.
- [ ] 목록에 `ESP32_BLE…` 줄이 보이는 **세로** 연결 화면을 캡처했다(캡처 1).

화면을 돌리면 11주차처럼 목록이 비워진다. 캡처는 돌리기 전에 세로에서 한다.
프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 연결하고 두 화면에서 상태 보기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 코드를 실행하고 `strings.xml`·`activity_main.xml`·`activity_control.xml`에 [제어 화면] 버튼과 상태 글자 자리를 만든다 |
| 10–25분 | 7번 collect가 `client.connectionState`를 받게 바꾸고, [다시 시도]·[해제]를 client로 바꾼 뒤 `ConnViewModel.kt`를 지운다 |
| 25–40분 | 주소 목록을 만들고 목록 줄을 누르면 `connect`한다. [제어 화면]과 제어 화면 상태 표시를 만든다 |
| 40–50분 | 검색 결과 0개 안내와 위치 서비스 확인을 넣는다 |
| 50–60분 | 캡처 2와 보드 사진을 찍고 `MainActivity.kt`·`ControlActivity.kt`와 함께 제출한다 |

### 1. 자리 만들기

1. `strings.xml`의 `show_contacts` 아래에 `control_screen`(`제어 화면`)과 `state_unknown`(`상태: ?`)을 넣는다.
2. `activity_main.xml`에서 `connectButton` **아래**·`retryButton` **위**에 id가 `controlButton`인 버튼(글자 `@string/control_screen`, 위 간격 `8dp`, `android:enabled="false"`)을 넣는다.
3. `activity_control.xml`에서 `deviceText` **아래**·`pinEdit` **위**에 id가 `stateText`인 TextView(글자 `@string/state_unknown`, `18sp`, 위 간격 `8dp`)를 넣는다.
4. 실행해 [연결] 아래에 꺼진 [제어 화면]이 보이고, [연결]로 간 제어 화면에 `상태: ?`가 보이면 다음으로 간다.

막히면 [따라하기 11단계](walkthrough.md#11-제어-화면-버튼과-상태-글자-자리-만들기)를 본다.

### 2. 상태를 client에서 받기

1. `// 7.` collect 틀에서 `viewModel.state.collect`를 `client.connectionState.collect`로 바꾼다.
2. 8번 "먼저 모두 끄고"에 `binding.controlButton.isEnabled = false`를 더하고, `READY` 가지에 `binding.controlButton.isEnabled = true`를 더한다.
3. `CONNECTING` 가지의 `binding.stopButton.isEnabled = true` 한 줄을 지운다([중지]는 이제 검색 멈춤이다).
4. `// 9.` 남은 초 collect 블록 전체를 지운다.
5. `// 5.` [다시 시도] 몸체를 `binding.scanButton.performClick()`으로, `// 6.` [해제] 몸체를 `client.disconnect()`로 바꾼다.
6. `private val viewModel: ConnViewModel by viewModels()`와 그 주석, 회색이 된 `import androidx.activity.viewModels`를 지우고, Project 창에서 `ConnViewModel.kt`를 지운다.
7. 실행해 1일차처럼 검색이 되면 아래 표를 코드(7번 `when`)만 보고 채운다. 연결은 3번에서 확인한다.

| 상태 | 켜지는 버튼 | ProgressBar | [다시 시도] |
|---|---|---|---|
| `연결 안 됨` |  |  |  |
| `연결 중` |  |  |  |
| `서비스 확인 중` |  |  |  |
| `준비됨` |  |  |  |
| `끊김` |  |  |  |

- 틀(`lifecycleScope.launch` · `repeatOnLifecycle` · `collect`)은 7주차 그대로다. 바뀌는 것은 받는 대상뿐이다.
- `viewModel`에 빨간 줄이 남아 있으면 5·6·7·9번 가운데 아직 안 바꾼 곳이 있다.

### 3. 목록 줄 누르기 → 연결, 그리고 [제어 화면]

1. `// 16.` 어댑터 블록 **아래**·`// 3.` [검색] 블록 **위**에 `val addresses = mutableListOf<String>()`을 만든다.
2. [검색]의 `adapter.notifyDataSetChanged()`(26번) 아래에서 `addresses`도 비우고 `retryButton`을 숨긴다. `onFound`의 `devices.add(…)` 아래에서 `addresses.add(address)`를 한다.
3. `// 19.` 목록 누르기 리스너 끝에 아래 모양을 채운다. 11주차 세 줄(이름 칸·Toast)은 그대로 둔다.

```kotlin
// addresses에서 position 번호의 주소를 꺼낸다 (get, 번호는 0부터)
// 검색 중일 수 있으니 먼저 client.stopScan()
// client.connect(주소)
```

4. `// 19.` 리스너 **아래**에 [제어 화면] 리스너를 만든다. 4주차 [연결]처럼 `Intent`에 장치 이름 칸의 글자를 `putExtra("name", …)`로 담아 `ControlActivity`를 연다.
5. `ControlActivity.kt`의 `// 3.` [뒤로] 블록 **아래**에 MainActivity 7번과 같은 틀로 `Bleuno.client?.connectionState?.collect { state -> }`를 만들고 안에서 `binding.stateText.text = "상태: $state"`. `Lifecycle`·`lifecycleScope`·`repeatOnLifecycle`·`Bleuno`·`launch`는 Alt+Enter로 import한다.
6. 실행하고 [검색] 뒤 표를 채운다. Logcat 필터는 `package:mine tag:BLE`.

| 조작 | 연결 화면 상태 글자와 켜진 버튼 | Logcat `tag:BLE` 새 줄 |
|---|---|---|
| `ESP32_BLE_FAKE1` 줄 누르기 |  |  |
| 1초 뒤 |  |  |
| 다시 1초 뒤 |  |  |
| [제어 화면] 누르기 → 제어 화면 상단 |  |  |
| [뒤로] → `준비됨`에서 화면 돌리기 |  |  |
| [해제] 누르기 |  |  |

- **BLE 연결은 목록 줄 탭이다.** [연결]은 4주차에 만든 "이름만 들고 이동" 버튼 그대로라서 눌러도 보드와 연결하지 않는다.
- `준비됨` 뒤 10초마다 `onCharacteristicChanged(가짜): {"event":"input",…}` 줄이 찍힌다. 14주차에 쓰는 입력 이벤트라 지금은 무시한다.
- 회전한 뒤에도 `준비됨`이 남는 까닭을 `Bleuno.client ?:`로 한 문장 적는다.

### 4. 0개 안내와 위치 서비스 확인

1. `onFinished`의 `binding.stateText.text = "검색 완료 · 장치 수: $count"` 한 줄을 `if (count == 0) { … } else { … }`로 바꾼다. 0개면 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`와 `retryButton` 보이기, 아니면 원래 문구.
2. 클래스 끝(`showContacts()` 아래)에 10주차 `showPermissionDialog()`와 같은 모양으로 `showLocationDialog()`를 만든다. 제목 `위치 서비스가 꺼져 있습니다`, [설정으로]는 `Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)`를 연다.
3. 그 아래에 `hasBlePermissions()`처럼 참/거짓을 돌려주는 `isLocationOff()`를 만든다. `Build.VERSION.SDK_INT <= 30`이면서 `PermissionHelper.isLocationEnabled(this) == false`이면 `true`. `Build`는 `android.os.Build`를 import한다.
4. [검색]의 블루투스 가지 **아래**·`else` **위**에 `else if (isLocationOff()) { showLocationDialog() }`를 넣는다.

| 조작 | 예상 화면 | 실제 화면 |
|---|---|---|
| [검색] 직후 1초 안에 [중지] |  |  |
| 이어서 [다시 시도] |  |  |
| (Android 11 이하 실기기) 위치를 끄고 [검색] |  |  |

- 에뮬레이터(API 33 이상)에서는 `isLocationOff()`가 늘 `false`라 안내창을 볼 수 없다. 코드로만 확인해도 된다.
- 안내창을 `onFinished` 안이 아니라 [검색] 리스너에서 띄우는 까닭을 "5초 뒤"와 "화면"이라는 낱말로 한 문장 적는다.

### 5. 캡처 2와 보드 사진

1. 목록 줄을 눌러 `준비됨`이 된 연결 화면과 Logcat `package:mine tag:BLE`의 연결 줄이 함께 보이게 **캡처한다(캡처 2).** Android Studio의 기기 화면 창과 Logcat 창을 나란히 두면 한 장에 담긴다. 어려우면 두 장으로 나눈다.
   - 실보드: `onConnectionStateChange` → `onMtuChanged` → `onServicesDiscovered` 줄이 순서대로 보이게
   - Fake: `connectGatt(가짜)` → `onConnectionStateChange(가짜)` → `onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨` 세 줄이 보이게
2. 실보드와 연결했으면 파랑 깜빡임이 멈추고 LED가 꺼진 보드를 **사진으로 찍는다.** 연결 전 파랑 깜빡임 사진과 나란히 두면 더 좋다. [해제]를 누르면 보드가 다시 파랑 깜빡임으로 돌아가는지도 본다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 줄이다. 파일 이름 뒤의 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 기기에서 조금 다르게 보일 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'Bleuno'.` (`ConnState`·`PermissionHelper`도 같은 모양) | 라이브러리는 다른 패키지(`com.example.smartio.bleuno`)라 import가 필요하다. 빨간 글자에 Alt+Enter(맥 ⌥+Enter) → Import |
| `Unresolved reference 'blePermissions'.` (바로 위에 `Method 'iterator()' is ambiguous for this expression.`과 후보 목록이 먼저 보일 수 있다) | 위의 `iterator()` 목록은 이 오류의 여파다. `Permissions.kt`를 지웠는데 부르는 곳을 안 바꿨다. `blePermissions()`를 `PermissionHelper.required()`로 바꾼다 |
| `Argument type mismatch: actual type is 'com.example.smartio.bleuno.BleunoDevice', but 'kotlin.String' was expected.` | `devices.add(device)`로 썼다. `devices`는 글자만 담는 목록이다. `device.name`·`device.address`로 꺼내 `"$name ($address)"`를 넣는다 |
| `Suspend function 'suspend fun collect(collector: FlowCollector<String>): Nothing' should be called only from a coroutine or another suspend function.` | `collect`를 틀 밖에서 불렀다. MainActivity 7번처럼 `lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { … } }` 안에 둔다 |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'com.example.smartio.bleuno.BleunoClient?'.` | 제어 화면에서 `Bleuno.client.connectionState`로 썼다. `Bleuno.client?.connectionState?.collect`로 `?.`를 쓴다. `!!`는 쓰지 않는다 |
| `Unresolved reference 'stateText'.` (`ControlActivity.kt`에 표시된다) | 고칠 곳은 `activity_control.xml`이다. `android:id="@+id/stateText"` TextView가 있는지, 철자가 같은지 본다 |
| (예상) 권한·블루투스가 켜진 상태에서 [검색]을 누르거나, 홈·회전·[연결]로 화면을 떠나는 순간(검색하지 않았어도) 앱이 멈춘다. 2일차 코드라면 앱을 켜자마자 멈춘다. Logcat에 `kotlin.UninitializedPropertyAccessException: lateinit property client has not been initialized` | `onCreate`의 `client = Bleuno.client ?: Bleuno.create(this, useFake)` 줄이 빠졌다. `lateinit`은 채우는 줄이 없어도 빌드가 된다. 화면을 떠날 때 멈추는 것은 `onStop`의 `client.stopScan()`이 채워지지 않은 `client`를 쓰기 때문이다 |
| (예상) [검색]을 누르면 ProgressBar가 한순간 보였다 사라지고 `검색 완료 · 장치 수: 0`(2일차 코드면 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`). Logcat에 `startScan(가짜): 5ms 동안 검색` | `startScan`의 첫 값은 밀리초다. `5`가 아니라 `5000`(5초)으로 쓴다 |
| (예상) [검색]·[권한 확인]을 눌러도 시스템 권한 창이 뜨지 않고 곧바로 `권한이 필요합니다`. 앱 권한 화면에 "근처 기기"가 없다 | `AndroidManifest.xml`에 10주차에 넣은 `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT` 선언이 있는지 본다 |
| (예상) `준비됨`에서 화면을 돌리면 `연결 안 됨`으로 돌아가고 [제어 화면]이 꺼진다. 실보드면 그 뒤 [검색]해도 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요` | `client = Bleuno.create(this, useFake)`처럼 `Bleuno.client ?:`가 빠졌다. bleuno README 6절 사용 예를 그대로 복사했을 때도 이렇다. `client = Bleuno.client ?: Bleuno.create(this, useFake)`로 쓴다 |
| (예상) 실기기에서 [검색]·[다시 시도]를 연달아 여러 번(30초에 5번 넘게) 눌렀더니 보드가 파랑 깜빡임인데도 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`가 반복된다 | Android가 짧은 시간에 너무 많은 검색을 잠시 막는다. 30초쯤 기다린 뒤 [검색]을 한 번만 누른다. Fake에는 해당하지 않는다 |
| (예상) 에뮬레이터에서 `useFake = false`로 실행했더니 늘 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`. Logcat에 `stopScan: 찾은 기기 0개` | 에뮬레이터 주변에는 보드가 없다. 실기기로 실행하거나 `useFake = true`로 되돌린다 |
| 실보드가 목록에 안 뜬다 | 보드 LED가 파랑 깜빡임인지(다른 폰에 연결되면 광고를 멈춘다), 블루투스가 켜져 있는지, Android 11 이하면 위치가 켜져 있는지, 28번 괄호 안이 `"ESP32_BLE"`인지 본다 |
| 화면을 돌리니 목록이 비워졌다 | 코드 잘못이 아니다. `devices`가 화면 안에 있어 새 화면이 빈 목록으로 시작한다(11주차와 같다). 연결 상태는 이어진다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.
앱이 보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다. Fake에서 되면 보드·기기 쪽을, Fake에서도 안 되면 내 코드를 본다.

## 제출 — 코드 두 개, 캡처 2장, 사진 1장

1. **`MainActivity.kt`**, **`ControlActivity.kt`**: 2일차 최종 코드
2. **캡처 1**: [검색] 뒤 `검색된 장치` 아래에 `ESP32_BLE…` 줄(Fake면 `ESP32_BLE_FAKE1`·`ESP32_BLE_FAKE2`)이 보이는 세로 연결 화면
3. **캡처 2**: `준비됨` 연결 화면과 Logcat `package:mine tag:BLE`의 연결 줄(실보드는 `onConnectionStateChange` → `onMtuChanged` → `onServicesDiscovered`, Fake는 `(가짜)` 세 줄). 두 장으로 나눠도 된다
4. **사진**: 연결 뒤 파랑 깜빡임이 멈추고 LED가 꺼진 보드. 보드·실기기가 없으면 생략하고 캡처 2를 Fake로 찍는다

채점은 [README 완료 기준](README.md#완료-기준)의 항목을 이 제출물로 확인한다. 실습지의 관찰표(1일차 3·4번, 2일차 3·4번 표), 상태별 버튼 표, "내 보드" 표는 스스로 점검하는 것이라 제출하지 않고 채점하지 않는다.
1일차 검색 목록(캡처 1)과 2일차 `준비됨`(캡처 2)까지 동작하면 기본 성공이다. 0개 안내·위치 확인과 실보드 연결은 예제와 도움을 받아 마무리해도 된다.
캡처와 사진에 계정·알림 내용이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 목록 줄에 신호 세기도 붙인다. `onFound` 안에서 `val rssi = device.rssi`를 꺼내 `ESP32_BLE_FAKE1 (00:11:22:33:44:01) 신호 -50`처럼 보여 준다. 실보드면 보드에서 멀어질수록 값이 어떻게 바뀌는지 본다.
- 1일차: 검색 시간을 10초로 늘린다. Logcat `tag:BLE`의 `startScan` 줄에서 바뀐 값을 확인한다.
- 2일차: 제어 화면에 [해제] 버튼을 하나 더 두고, 누르면 `Bleuno.client?.disconnect()` 뒤 `finish()`로 연결 화면에 돌아가게 한다. 돌아온 연결 화면의 상태 글자를 본다.
- 2일차: `준비됨`일 때 목록 줄을 누르면 다시 연결하지 않고 Toast `이미 연결되어 있습니다. [해제]를 먼저 누르세요`를 띄운다(`client.isReady`).

추가 과제는 선택 사항이다.
