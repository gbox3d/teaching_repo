---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 12주차
footer: BLE 기초 · Bleuno 클라이언트로 검색·연결
---

# BLE 기초: Bleuno 클라이언트로 검색·연결

11주차 [검색]은 가짜 이름을 목록에 넣었습니다.
이번 주에는 제공 라이브러리 **bleuno**로 진짜 보드를 **찾고, 연결**합니다.

```text
검색된 장치                            준비됨
ESP32_BLE_FAKE1 (00:11:22:33:44:01)    [해제] [제어 화면]
ESP32_BLE_FAKE2 (00:11:22:33:44:02)    제어 화면: 상태: 준비됨
```

보드가 없어도 `useFake = true`로 똑같이 연습합니다.

---

# 1일차 — 보드 검색하기

`30분 설명·시연 → 60분 실습`

1. `name.startsWith("ESP32_BLE")`로 보드 이름 거르기
2. 폰과 보드의 역할, GATT와 bleuno 보드의 UUID
3. 블루투스가 꺼져 있으면 켜기 요청 창
4. `Bleuno.create`와 `startScan`·`stopScan`으로 11주차 가짜 검색 바꾸기

---

## 1일차 · 0–5분 — 오늘 문법: name.startsWith("ESP32_BLE")

```kotlin
val name = "ESP32_BLE7C9EBF"
if (name.startsWith("ESP32_BLE")) {
    println("수업 보드: $name")
}
```

| `name` | `name.startsWith("ESP32_BLE")` |
|---|---|
| `ESP32_BLE7C9EBF` (실보드) | `true` |
| `ESP32_BLE_FAKE1` (Fake) | `true` |
| `Galaxy Buds` | `false` |

- 글자가 괄호 안 글자로 **시작하면** `true`입니다. 대소문자까지 같아야 합니다.
- 보드 이름은 `ESP32_BLE` + 칩 ID라서 보드마다 뒤가 다릅니다.

---

## 1일차 · 5–13분 ① — 폰과 보드: 두 역할 축

| 역할 축 | Android 폰 | ESP32-C3 보드 |
|---|---|---|
| central / peripheral | central: 검색하고 연결을 건다 | peripheral: 광고하며 기다린다 |
| GATT client / server | client: 값을 찾아 읽고 쓴다 | server: service와 값을 가진다 |

- 두 축은 함께 다니지만 **같은 말이 아닙니다.** 연결을 거는 역할과 값을 가진 역할입니다.
- 이 수업에서는 폰이 central이면서 client, 보드가 peripheral이면서 server입니다.

---

## 1일차 · 5–13분 ② — 광고에서 준비됨까지

```text
보드: 광고 (파랑 깜빡임)
   ↓ 검색 결과 — 폰이 이름·주소를 받는다
연결 (connect)                       → 연결 중
   ↓ 연결됨 (보드 LED 꺼짐)
서비스 찾기 (discover services)       → 서비스 확인 중
   ↓ 필요한 service·characteristic 확인
알림 켜기                            → 준비됨
```

- 연결됐다고 곧바로 명령을 보낼 수 있는 것이 **아닙니다.** 서비스를 찾아야 `준비됨`입니다.
- 오른쪽 글자가 라이브러리의 `ConnState` 문자열입니다. 7주차에 만든 다섯 가지와 같습니다.

---

## 1일차 · 5–13분 ③ — GATT 계층과 bleuno 보드

```text
보드 ESP32_BLE7C9EBF (GATT server)
└─ Service         c6f8b088-2af8-4388-8364-ca2a907bdeb8
   └─ Characteristic f6aa83ca-de53-46b4-bdea-28a7cb57942e  읽기·쓰기·알림
      └─ CCCD      00002902-0000-1000-8000-00805f9b34fb  알림 켜기 설정
```

- **service**는 characteristic의 묶음, **characteristic**은 실제 값이 오가는 칸입니다.
- **UUID**는 이것들의 이름표입니다. 인터넷 예제의 UUID가 아니라 이 값만 씁니다.
- 명령(`on 3`)과 응답(JSON)은 13주차에 이 characteristic으로 주고받습니다.
- 전체 표: [bleuno README](../../bleuno/README.md) 1·2절

---

## 1일차 · 13–20분 ① — 블루투스가 꺼져 있으면

```kotlin
// 클래스 변수 자리 (onCreate 밖)
private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        Toast.makeText(this, "블루투스 켜짐. [검색]을 다시 누르세요", Toast.LENGTH_SHORT).show()
    } else {
        Toast.makeText(this, "블루투스를 켜야 검색할 수 있습니다", Toast.LENGTH_SHORT).show()
    }
}
// 띄울 때
bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
```

- 10주차 시연의 `setResult` 결과 받기 틀과 **같은 모양**입니다. 받는 것은 `resultCode`뿐입니다.
- 켜져 있는지는 `PermissionHelper.isBluetoothEnabled(this)`가 알려 줍니다.

---

## 1일차 · 13–20분 ② — 확인 순서: 권한 → 블루투스 → 검색

```kotlin
binding.scanButton.setOnClickListener {
    if (hasBlePermissions() == false) {
        permissionLauncher.launch(PermissionHelper.required())
    } else if (PermissionHelper.isBluetoothEnabled(this) == false) {
        bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
    } else {
        // 여기서 검색한다
    }
}
```

- 1주차 `if/else`에 `else if`를 이어 붙였습니다. 위에서부터 **처음 맞는 것 하나**만 실행됩니다.
- Android 12+에서는 켜기 요청 창도 권한이 있어야 뜨므로 **권한을 먼저** 봅니다.
- 허용·켜기 직후에는 검색이 자동으로 시작되지 않습니다. [검색]을 한 번 더 누릅니다.

---

## 1일차 · 20–27분 ① — 제공 라이브러리 bleuno 넣기

1. `com.example.smartio`에서 **New › Package** › `bleuno` → `src/` 파일 8개 붙여 넣기
2. 11주차 `ConnState.kt`·`Permissions.kt` 지우기 → `ConnState` import, `PermissionHelper.required()`

```kotlin
private val useFake = true                    // 보드가 있으면 false
private lateinit var client: BleunoClient     // binding과 같은 틀

// onCreate 안, insets 블록 아래
client = Bleuno.client ?: Bleuno.create(this, useFake)
```

- `Bleuno.client`는 앱 전체가 함께 쓰는 client 한 개입니다. 처음에는 `null`입니다.
- `?:` 덕분에 회전해서 `onCreate`가 다시 불려도 **이미 만든 것**을 씁니다.

---

## 1일차 · 20–27분 ② — 11주차 가짜 검색을 startScan으로

```kotlin
client.startScan(5000, onFound = { device ->
    val name = device.name
    val address = device.address
    if (name.startsWith("ESP32_BLE")) {
        devices.add("$name ($address)")
        adapter.notifyDataSetChanged()
    }
}, onFinished = {
    val count = devices.size
    binding.stateText.text = "검색 완료 · 장치 수: $count"
})
```

- `5000`은 밀리초(5초). `onFound =`·`onFinished =`는 **어느 칸의 람다인지** 붙인 이름표입니다.
- 둘 다 메인 스레드에서 불리므로 안에서 View를 바로 바꿉니다(`runOnUiThread` 필요 없음).

---

## 1일차 · 20–27분 ③ — [중지]와 onStop

```kotlin
binding.stopButton.setOnClickListener {
    client.stopScan()          // onFinished가 한 번 불린다
}

override fun onStop() {
    super.onStop()
    unregisterReceiver(batteryReceiver)
    client.stopScan()          // 화면을 떠나면 검색도 멈춘다
}
```

- [중지]에서 버튼을 되돌리는 코드를 따로 쓰지 않습니다. `onFinished`가 처리합니다.
- 10주차 짝 규칙: **시작한 일은 화면이 안 보일 때 멈춥니다.**
- Fake 결과: 1초 뒤 `ESP32_BLE_FAKE1`, 2초 뒤 `ESP32_BLE_FAKE2`, 5초 뒤 `검색 완료 · 장치 수: 2`

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--fake로-보드-검색하기-60분) · [따라하기](walkthrough.md#1일차)

1. `bleuno` 패키지를 넣고 11주차 `ConnState.kt`·`Permissions.kt`를 정리합니다.
2. `useFake`·`client`·`bluetoothLauncher`를 만들고 `onCreate`에서 client를 받습니다.
3. [검색]을 권한 → 블루투스 → `startScan`으로, [중지]와 `onStop`은 `stopScan()`으로.
4. 목록에 `ESP32_BLE…`가 뜬 세로 화면을 캡처합니다. 보드가 있으면 `useFake = false`.

**설명 합계: 5+8+7+7+3 = 30분**

Logcat 필터 `package:mine tag:BLE`로 `startScan(가짜)`·`onScanResult(가짜)` 줄을 함께 봅니다.

---

# 2일차 — 연결하고 두 화면에서 상태 보기

`30분 설명·시연 → 60분 실습`

1. 연결 콜백 사슬을 Logcat `tag:BLE`로 읽기
2. 목록 줄 누르기 → `client.connect(address)`, 7주차 collect 틀로 상태 받기
3. `object Bleuno`로 제어 화면과 같은 연결 쓰기
4. 0개·블루투스 꺼짐·위치 서비스 꺼짐일 때 안내

---

## 2일차 · 0–8분 ① — 특강 콜백 사슬 한눈에

```text
startScan → (5초) stopScan
connectGatt(주소, autoConnect=false)                              연결 중
 └▶ onConnectionStateChange(STATE_CONNECTED) → requestMtu(185)   서비스 확인 중
     └▶ onMtuChanged → discoverServices()
         └▶ onServicesDiscovered → characteristic 찾기
             └▶ 알림 켜기(CCCD 쓰기) → onDescriptorWrite        준비됨
STATE_DISCONNECTED → gatt.close()                              연결 안 됨 / 끊김
```

- 특강에서 직접 쓴 콜백들이 `RealBleunoClient.kt` 안에 **그대로** 들어 있습니다.
- 우리는 `connect` 한 줄만 부르고, 결과는 오른쪽 **상태 글자**로 받습니다.

---

## 2일차 · 0–8분 ② — Logcat tag:BLE로 읽기

```text
connectGatt(84:F7:03:xx:xx:xx, autoConnect=false)
onConnectionStateChange: status=0 newState=2
STATE_CONNECTED → requestMtu(185)
onMtuChanged: mtu=185 status=0 → discoverServices()
onServicesDiscovered: status=0
characteristic 확보: f6aa83ca-de53-46b4-bdea-28a7cb57942e
onDescriptorWrite: status=0 → 준비됨
```

- 필터 `package:mine tag:BLE`. 마지막으로 찍힌 줄이 **어디까지 갔는지** 알려 줍니다.
- Fake는 `(가짜)`가 붙은 세 줄: `connectGatt(가짜)` → `onConnectionStateChange(가짜)` → `onServicesDiscovered(가짜) … 준비됨`
- 준비됨 뒤 10초마다 찍히는 `onCharacteristicChanged(가짜): {"event":"input",…}`는 14주차용이라 지금은 무시합니다.

---

## 2일차 · 8–18분 ① — 목록 줄 누르기 → connect(address)

```kotlin
val addresses = mutableListOf<String>()      // devices와 같은 순서로

devices.add("$name ($address)")              // onFound 안
addresses.add(address)

binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    // … 11주차 세 줄(이름 칸·Toast) 그대로
    val address = addresses.get(position)
    client.stopScan()
    client.connect(address)
}
```

- 보이는 글자(`devices`)와 연결에 쓸 주소(`addresses`)를 **같은 번호**로 둡니다.
- **BLE 연결은 목록 줄 탭**입니다. [연결]은 4주차에 만든 "이름만 들고 이동" 버튼 그대로입니다.

---

## 2일차 · 8–18분 ② — 7주차 collect 틀에 client.connectionState

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        client.connectionState.collect { state ->    // 7주차: viewModel.state.collect
            binding.stateText.text = state
            // … 먼저 모두 끄고, when (state)로 상태에 맞는 것만 켠다
        }
    }
}
```

- 틀은 7주차 그대로, **받는 대상만** 바뀝니다. 값은 `ConnState` 문자열 다섯 가지입니다.
- 상태를 라이브러리가 만들어 주므로 `ConnViewModel.kt`와 9번(남은 초 collect)은 지웁니다.
- 화면에는 `연결 중` → `서비스 확인 중` → `준비됨`이 그대로 보입니다. 카운트다운 숫자는 없습니다.

---

## 2일차 · 8–18분 ③ — 상태별 버튼: 준비됨이면 [제어 화면]

| 상태 | 켜지는 것 |
|---|---|
| `연결 안 됨` | [검색] |
| `연결 중` | ProgressBar만 ([검색]·[중지]·[해제]·[제어 화면] 꺼짐) |
| `서비스 확인 중` | ProgressBar만 |
| `준비됨` | [해제], **[제어 화면]** |
| `끊김` | [검색], [다시 시도] |

```kotlin
ConnState.READY -> {
    binding.disconnectButton.isEnabled = true
    binding.controlButton.isEnabled = true
}
```

- 7주차 `CONNECTING`에서 켜던 [중지]는 이제 **검색 멈춤**이라 켜지 않습니다.

---

## 2일차 · 8–18분 ④ — object Bleuno로 두 화면이 같은 연결을

```kotlin
// ControlActivity onCreate 끝
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        Bleuno.client?.connectionState?.collect { state ->
            binding.stateText.text = "상태: $state"
        }
    }
}
```

- `object Bleuno { var client }`에 client 하나를 두고 **두 화면이 같이** 씁니다. 연결은 Intent로 넘길 수 없습니다.
- `Bleuno.client`는 `BleunoClient?`라서 3주차 `?.`로 부릅니다. `!!`는 쓰지 않습니다.
- `준비됨`에서 화면을 돌려도 상태가 이어집니다(`Bleuno.client ?:`). 목록만 11주차처럼 비워집니다.

---

## 2일차 · 18–25분 ① — 0개일 때 [다시 시도]

```kotlin
}, onFinished = {
    val count = devices.size
    if (count == 0) {
        binding.stateText.text = "장치를 찾지 못했습니다 — [다시 시도]를 누르세요"
        binding.retryButton.visibility = View.VISIBLE
    } else {
        binding.stateText.text = "검색 완료 · 장치 수: $count"
    }
})
```

- [다시 시도]는 `binding.scanButton.performClick()` 한 줄입니다. 코드로 [검색]을 누릅니다.
- 0개는 앱 오류가 아닙니다. 보드 LED가 **파랑 깜빡임**인지(다른 폰에 연결되면 안 보임) 확인합니다.
- Fake로 보려면 [검색] 직후 1초 안에 [중지]를 누릅니다.

---

## 2일차 · 18–25분 ② — 위치 서비스(Android 11 이하)와 확인 사슬

```kotlin
if (hasBlePermissions() == false) {
    permissionLauncher.launch(PermissionHelper.required())       // 권한
} else if (PermissionHelper.isBluetoothEnabled(this) == false) {
    bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))   // 블루투스
} else if (isLocationOff()) {
    showLocationDialog()                                          // 위치(API 30 이하)
} else {
    // 검색
}
```

- `isLocationOff()`: `Build.VERSION.SDK_INT <= 30`이면서 위치가 꺼졌으면 `true`(13번 함수와 같은 모양).
- 안내창은 10주차 `showPermissionDialog()` 모양 + `Settings.ACTION_LOCATION_SOURCE_SETTINGS`.
- 창은 **클릭 리스너에서만** 띄웁니다. 5초 뒤 불리는 `onFinished`에서는 글자만 바꿉니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--연결하고-두-화면에서-상태-보기-60분) · [따라하기](walkthrough.md#2일차)

1. [제어 화면] 버튼과 제어 화면 상태 글자 자리를 만듭니다.
2. 7번 collect를 `client.connectionState`로 바꾸고 `ConnViewModel.kt`를 지웁니다.
3. 주소 목록 → 줄 누르면 `connect` → `준비됨`이면 [제어 화면] → 제어 화면 `상태: 준비됨`.
4. 0개 안내·위치 확인을 넣고, `준비됨` 화면 + Logcat `tag:BLE`를 캡처합니다.

**설명 합계: 8+10+7+5 = 30분**

`연결 중`에서 오래 멈추면 보드 전원·거리를 봅니다. 실보드는 보통 30초쯤 뒤 `끊김`이 됩니다.

---

## 제출하기

2일차가 끝나면 한 번 제출합니다.

1. **`MainActivity.kt`**, **`ControlActivity.kt`**
2. **캡처 1**: [검색] 뒤 목록에 `ESP32_BLE…` 줄이 보이는 세로 연결 화면
3. **캡처 2**: `준비됨` 화면과 Logcat `package:mine tag:BLE`의 연결 줄
4. **사진**: 연결 뒤 파랑 깜빡임이 멈춘 보드(보드·실기기가 없으면 생략, 캡처 2를 Fake로)

---

## 다음 주 미리 보기

지금 제어 화면의 LED Switch는 로그에 `on 3`을 **적기만** 합니다.

13주차에는 `Bleuno.client?.send("on 3")`으로 보드에 진짜 명령을 보내고,

보드가 돌려주는 `{"result":"ok","ms":"led(s) on"}`을 `onMessage { }`로 받아 로그에 쌓습니다.
