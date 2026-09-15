# 12주차 예제 — 보드 검색과 연결

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/bleuno/](day1/bleuno) 8개 (`Bleuno.kt`, `BleunoClient.kt`, `BleunoDevice.kt`, `BleunoMessage.kt`, `ConnState.kt`, `FakeBleunoClient.kt`, `PermissionHelper.kt`, `RealBleunoClient.kt`) | `app › kotlin+java › com.example.smartio › bleuno`(새 패키지, New › Package) | **제공 코드**. [bleuno/src](../../../bleuno/src)와 같다. 붙여 넣고 고치지 않는다 |
| 11주차 `ConnState.kt`, `Permissions.kt` | `com.example.smartio` 바로 아래 | 1일차에 **지운다**. `bleuno`의 `ConnState`, `PermissionHelper.required()`를 쓴다 |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `useFake`·`client`·`bluetoothLauncher`, client 받기(24번), [검색] 교체(25~29번), [중지] 교체(30번), `onStop`에 `stopScan()`, `blePermissions()` → `PermissionHelper.required()` |
| [day1/ConnViewModel.kt](day1/ConnViewModel.kt) | `ConnViewModel.kt` | `import com.example.smartio.bleuno.ConnState` 한 줄 추가 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | 주소 목록(31~33번), 0개 안내(34번), [다시 시도]·[해제] 35·36번, collect 대상 교체(37번), 줄 누르면 연결(38번), [제어 화면] 39번, 위치 확인(40~42번). `viewModel`과 9번 삭제 |
| `day2`에 없는 `ConnViewModel.kt` | `ConnViewModel.kt` | 2일차에 **지운다** |
| [day2/ControlActivity.kt](day2/ControlActivity.kt) | `ControlActivity.kt` | 상태 collect(4번) 추가 |
| [day2/activity_main.xml](day2/activity_main.xml) | `app › res › layout › activity_main.xml` | `connectButton` 아래 `controlButton` 추가 |
| [day2/activity_control.xml](day2/activity_control.xml) | `activity_control.xml` | `deviceText` 아래 `stateText` 추가 |
| [day2/strings.xml](day2/strings.xml) | `app › res › values › strings.xml` | `control_screen`, `state_unknown` 추가 |
| `dayN/ContactsReader.kt` | 연락처 읽기 | 11주차 그대로, 바꾸지 않는다 |
| `day1/ControlActivity.kt`, `day1/activity_*.xml`, `day1/strings.xml` | 화면·글자 | 11주차 그대로(2일차에 바꾼다) |
| `dayN/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 11주차 그대로. BLE 권한은 10주차에 넣었다. 내 파일에는 아이콘 등 줄이 더 있어도 된다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`BluetoothGatt`·`StateFlow`·`org.json`은 Android 기본과 4주차 의존성에 들어 있어 `build.gradle.kts`에 더할 것이 없다.
주석 번호는 11주차 1~23에 이어 24~30(1일차), 31~42(2일차)를 붙였다. 번호는 넣은 순서라 파일 안에서는 차례대로 놓이지 않는다. 클래스 변수 `useFake`·`client`·`bluetoothLauncher`에는 번호 없이 `// 12주차 1일차:` 꼬리표를 붙였다.
[bleuno README](../../../bleuno/README.md) 6절의 사용 예는 요약이라 이 예제와 모양이 다르다(`Bleuno.client ?:` 없음 등). 이 예제가 기준이다.

## 1. `name.startsWith("ESP32_BLE")` — 이름으로 보드 고르기

```kotlin
val name = device.name
if (name.startsWith("ESP32_BLE")) {
    devices.add("$name ($address)")
}
```

| `name` | 결과 |
|---|---|
| `ESP32_BLE7C9EBF` (실보드, 칩 ID는 보드마다 다름) | `true` → 목록에 들어감 |
| `ESP32_BLE_FAKE1` (Fake) | `true` → 목록에 들어감 |
| `esp32_ble…` 또는 다른 기기 이름 | `false` → 들어가지 않음 |

- 대소문자까지 같아야 한다. 라이브러리 `RealBleunoClient`도 같은 확인(`nameFilter = "ESP32_BLE"`)을 한다.

## 2. bleuno 패키지와 `Bleuno.client` — 앱 전체가 함께 쓰는 client

```kotlin
private val useFake = true
private lateinit var client: BleunoClient

// onCreate 안
client = Bleuno.client ?: Bleuno.create(this, useFake)
```

| 실행 결과 | 값 |
|---|---|
| 앱을 처음 켰을 때 | `Bleuno.client`가 `null` → `Bleuno.create`가 만들어 `Bleuno.client`에 넣고 돌려준다 |
| 회전해서 `onCreate`가 다시 불렸을 때 | 이미 있는 `Bleuno.client`를 그대로 받는다(연결·상태가 이어진다) |
| `useFake = false` | 실제 보드용 `RealBleunoClient`를 만든다(실기기에서만 보드를 찾는다) |

- `lateinit var`는 `binding`과 같은 "onCreate에서 채우는 변수" 틀이다. 채우는 줄을 빼도 빌드는 되고, 쓰는 순간 `UninitializedPropertyAccessException`으로 멈춘다(예상).
- `Bleuno.client ?:`를 빼면 회전할 때마다 새 client가 만들어져 `준비됨`이 `연결 안 됨`으로 돌아간다(예상).

## 3. 블루투스 켜기 요청 — `StartActivityForResult` 틀

```kotlin
private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        Toast.makeText(this, "블루투스 켜짐. [검색]을 다시 누르세요", Toast.LENGTH_SHORT).show()
    } else {
        Toast.makeText(this, "블루투스를 켜야 검색할 수 있습니다", Toast.LENGTH_SHORT).show()
    }
}

// [검색] 안, 권한 확인 다음
} else if (PermissionHelper.isBluetoothEnabled(this) == false) {
    bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
}
```

| 실행 결과 | 화면 |
|---|---|
| 블루투스가 꺼진 채 [검색] | 시스템의 블루투스 켜기 요청 창(문구는 OS마다 다르다) |
| 요청 창 [허용] | Toast `블루투스 켜짐. [검색]을 다시 누르세요`. 검색은 아직 시작하지 않는다 |
| 요청 창 [거부] | Toast `블루투스를 켜야 검색할 수 있습니다` |

- 10주차 2일차 시연의 `setResult` 결과 받기 틀과 같은 모양이다. 클래스 변수 자리(onCreate 밖)에 둔다.
- 확인 순서는 권한 → 블루투스다. Android 12 이상에서는 요청 창도 `BLUETOOTH_CONNECT` 권한이 있어야 띄울 수 있다.

## 4. `startScan`·`stopScan` — 5초 검색

```kotlin
client.startScan(5000, onFound = { device ->
    val name = device.name
    val address = device.address
    if (name.startsWith("ESP32_BLE")) {
        devices.add("$name ($address)")
        adapter.notifyDataSetChanged()
    }
}, onFinished = {
    binding.scanButton.isEnabled = true
    binding.stopButton.isEnabled = false
    binding.scanProgress.visibility = View.GONE
    val count = devices.size
    binding.stateText.text = "검색 완료 · 장치 수: $count"
})

binding.stopButton.setOnClickListener {
    client.stopScan()
}
```

| 실행 결과 (Fake) | 화면 | Logcat `package:mine tag:BLE` |
|---|---|---|
| [검색] 직후 | `검색 중…`, ProgressBar, [중지] 켜짐 | `startScan(가짜): 5000ms 동안 검색` |
| 1초·2초 뒤 | `ESP32_BLE_FAKE1 (00:11:22:33:44:01)` → `ESP32_BLE_FAKE2 (00:11:22:33:44:02)` | `onScanResult(가짜): ESP32_BLE_FAKE1` … `FAKE2` |
| 5초 뒤 | `검색 완료 · 장치 수: 2`, [검색] 켜짐 | `scan timeout(가짜) (5000ms)` → `stopScan(가짜)` |
| 1.5초쯤 [중지] | 곧바로 `검색 완료 · 장치 수: 1` | `stopScan(가짜)` |
| 검색 중 홈으로 나가기(`onStop`의 `stopScan()`) | 돌아오면 [검색] 켜짐 | `stopScan(가짜)`, `scan timeout` 줄 없음 |

- 첫 값은 **밀리초**다. `5`로 쓰면 5ms 만에 끝나 늘 0개다.
- `onFound`·`onFinished`는 메인 스레드에서 불린다. `runOnUiThread` 없이 View를 바꾼다.
- `stopScan()`은 `onFinished`를 한 번 부른다. [중지]에서 버튼을 따로 되돌리지 않는다.
- `devices`는 글자 목록이라 `device`(이름·주소·신호 세기를 묶은 `BleunoDevice`)를 그대로 넣으면 `Argument type mismatch` 오류가 난다.
- 실보드(`useFake = false`, 실기기): 목록 `ESP32_BLE7C9EBF (84:F7:03:…)`, Logcat `onScanResult: ESP32_BLE7C9EBF 84:F7:03:xx:xx:xx rssi=-48`, `stopScan: 찾은 기기 1개`.

## 5. `connect`와 `connectionState` — 7주차 collect 틀 그대로

```kotlin
val addresses = mutableListOf<String>()     // devices와 같은 순서

binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    val address = addresses.get(position)
    client.stopScan()
    client.connect(address)
}

lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        client.connectionState.collect { state ->
            binding.stateText.text = state
            // 모두 끄고 when (state)로 켤 것만 켠다. READY면 [해제]·[제어 화면]
        }
    }
}
```

| 실행 결과 (Fake, FAKE1 줄 누르기) | 화면 | Logcat `tag:BLE` |
|---|---|---|
| 누른 직후 | `연결 중`, ProgressBar, [검색]·[중지]·[해제]·[제어 화면] 꺼짐 | `connectGatt(가짜): 00:11:22:33:44:01` |
| 1초 뒤 | `서비스 확인 중` | `onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중` |
| 다시 1초 뒤 | `준비됨`, [해제]·[제어 화면] 켜짐 | `onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨` |
| [해제] | `연결 안 됨`, [검색] 켜짐 | `disconnect(가짜) → 연결 안 됨` |
| `준비됨`에서 회전 | `준비됨`과 버튼 유지, 목록만 비워짐 | — |

- **BLE 연결은 목록 줄 탭**이다. [연결] 버튼은 4주차 "이름만 들고 제어 화면으로 이동" 그대로다.
- `준비됨` 동안 10초마다 `onCharacteristicChanged(가짜): {"event":"input",…}`가 찍힌다. 14주차용 입력 이벤트라 12주차 앱은 받지 않는다.
- 상태 값은 `ConnState`의 `연결 안 됨`·`연결 중`·`서비스 확인 중`·`준비됨`·`끊김`이다. `끊김`은 사용자가 [해제]하지 않았는데 끊긴 경우(실보드 전원 끔 등)다.

## 6. 제어 화면에서 같은 연결 보기 — `Bleuno.client?.`

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        Bleuno.client?.connectionState?.collect { state ->
            binding.stateText.text = "상태: $state"
        }
    }
}
```

| 실행 결과 | 제어 화면 상단 |
|---|---|
| `준비됨`에서 [제어 화면] | `장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)` / `상태: 준비됨` |
| 연결하지 않고 [연결]로 이동 | `상태: 연결 안 됨` |
| 실보드 전원을 끔(준비됨 상태) | 몇 초 뒤 `상태: 끊김`(예상) |

- 연결 객체는 Intent로 넘기지 않는다. `object Bleuno`의 `client`를 두 화면이 같이 쓴다.
- `Bleuno.client`는 `BleunoClient?`라서 `?.`가 필요하다. 빼면 `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'com.example.smartio.bleuno.BleunoClient?'.` 오류가 난다.
- `collect`를 틀 밖에서 부르면 `Suspend function 'suspend fun collect(collector: FlowCollector<String>): Nothing' should be called only from a coroutine or another suspend function.` 오류가 난다.

## 7. 0개 안내와 위치 서비스 확인

```kotlin
if (count == 0) {
    binding.stateText.text = "장치를 찾지 못했습니다 — [다시 시도]를 누르세요"
    binding.retryButton.visibility = View.VISIBLE
} else {
    binding.stateText.text = "검색 완료 · 장치 수: $count"
}
```

```kotlin
private fun isLocationOff(): Boolean {
    if (Build.VERSION.SDK_INT <= 30) {
        if (PermissionHelper.isLocationEnabled(this) == false) {
            return true
        }
    }
    return false
}
```

| 실행 결과 | 화면 |
|---|---|
| [검색] 직후 1초 안에 [중지] (Fake) | `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`, [다시 시도] 보임 |
| [다시 시도] | `performClick()`으로 [검색]을 누른 것과 같다. `검색 중…` |
| Android 11 이하 실기기, 위치 꺼짐, [검색] | 검색하지 않고 AlertDialog `위치 서비스가 꺼져 있습니다` → [설정으로]는 위치 설정 화면(예상) |
| 에뮬레이터 API 33 이상 | `isLocationOff()`가 늘 `false`. 안내창이 뜨지 않는다 |

- [검색]의 확인 순서는 권한 → 블루투스 → 위치 → 검색이다. 창은 늘 클릭 리스너에서 띄우고, 5초 뒤 불리는 `onFinished`에서는 글자·버튼만 바꾼다.
- 실기기에서 [검색]·[다시 시도]를 30초에 5번 넘게 누르면 Android가 잠시 검색 결과를 주지 않아 0개가 반복될 수 있다(예상).

## 8. 2일차 완성 — 검색, 연결, 두 화면

[day2](day2) 파일과 [day1/bleuno](day1/bleuno)를 모두 넣고 실행한 흐름:

```text
[검색] ─┬─ 권한 없음 ▶ 권한 창 (10주차)
        ├─ 블루투스 꺼짐 ▶ 켜기 요청 창
        ├─ 위치 꺼짐(Android 11 이하) ▶ 위치 안내창
        └─ 검색 5초 ─ onFound ▶ 목록 "이름 (주소)" ─ onFinished ▶ 검색 완료 · 장치 수 / 0개면 [다시 시도]
목록 줄 누르기 ▶ stopScan ▶ connect(주소)
  연결 중 ▶ 서비스 확인 중 ▶ 준비됨 ─ [제어 화면] ▶ 상태: 준비됨
                                    └ [해제] ▶ 연결 안 됨
화면을 떠나면(onStop) ▶ stopScan
```

실보드 연결 때 Logcat `tag:BLE`에 남는 콜백 사슬([bleuno README](../../../bleuno/README.md) 8절):

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

## 공식 참고 자료

- [Bluetooth Low Energy 개요 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [BLE 기기 찾기 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/find-ble-devices)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
