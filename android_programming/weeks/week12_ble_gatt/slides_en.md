---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 12
footer: BLE Basics · Scan and Connect with the Bleuno Client
---

# BLE Basics: Scan and Connect with the Bleuno Client

In week 11, **[검색]** (Scan) added fake names to the list.
This week, we use the provided **bleuno** library to **scan for and connect to** a real board.

```text
검색된 장치                            준비됨
ESP32_BLE_FAKE1 (00:11:22:33:44:01)    [해제] [제어 화면]
ESP32_BLE_FAKE2 (00:11:22:33:44:02)    제어 화면: 상태: 준비됨
```

Even without a board, you can practice the same way with `useFake = true`.

---

# Day 1 — Scanning for the Board

`30 min explanation & demo → 60 min lab`

1. Filter board names with `name.startsWith("ESP32_BLE")`
2. Phone and board roles, GATT, and the bleuno board's UUIDs
3. A prompt to turn Bluetooth on if it's off
4. Replace week 11's fake scan with `Bleuno.create` and `startScan`/`stopScan`

---

## Day 1 · 0–5 min — Today's Syntax: name.startsWith("ESP32_BLE")

```kotlin
val name = "ESP32_BLE7C9EBF"
if (name.startsWith("ESP32_BLE")) {
    println("수업 보드: $name")
}
```

| `name` | `name.startsWith("ESP32_BLE")` |
|---|---|
| `ESP32_BLE7C9EBF` (real board) | `true` |
| `ESP32_BLE_FAKE1` (Fake) | `true` |
| `Galaxy Buds` | `false` |

- Returns `true` if the string **starts with** the text in parentheses. Case must match exactly.
- Board names are `ESP32_BLE` + a chip ID, so the ending differs per board.

---

## Day 1 · 5–13 min ① — Phone and Board: Two Role Axes

| Role axis | Android phone | ESP32-C3 board |
|---|---|---|
| central / peripheral | central: scans and starts the connection | peripheral: advertises and waits |
| GATT client / server | client: finds, reads, and writes values | server: holds services and values |

- The two axes travel together, but they are **not the same thing** — one is about who starts the connection, the other about who holds the values.
- In this course, the phone is central and client; the board is peripheral and server.

---

## Day 1 · 5–13 min ② — From Advertising to Ready

```text
Board: advertising (blue blinking)
   ↓ Scan result — phone receives the name and address
Connect                              → 연결 중
   ↓ Connected (board LED turns off)
Discover services                    → 서비스 확인 중
   ↓ Find the needed service/characteristic
Turn on notifications                → 준비됨
```

- Being connected does **not** mean you can send commands right away. The board reaches `준비됨` (Ready) only after services are discovered.
- The text on the right is the library's `ConnState` string — the same five values you built in week 7.

---

## Day 1 · 5–13 min ③ — The GATT Hierarchy and the bleuno Board

```text
Board ESP32_BLE7C9EBF (GATT server)
└─ Service         c6f8b088-2af8-4388-8364-ca2a907bdeb8
   └─ Characteristic f6aa83ca-de53-46b4-bdea-28a7cb57942e  read · write · notify
      └─ CCCD      00002902-0000-1000-8000-00805f9b34fb  enables notifications
```

- A **service** is a group of characteristics; a **characteristic** is where the actual values travel.
- A **UUID** is their label. Use only these exact values, not UUIDs from other tutorials.
- Commands (`on 3`) and responses (JSON) travel through this characteristic starting in week 13.
- Full table: [bleuno README](../../bleuno/README.md), sections 1–2

---

## Day 1 · 13–20 min ① — When Bluetooth Is Off

```kotlin
// Class-level property (outside onCreate)
private val bluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        Toast.makeText(this, "블루투스 켜짐. [검색]을 다시 누르세요", Toast.LENGTH_SHORT).show()
    } else {
        Toast.makeText(this, "블루투스를 켜야 검색할 수 있습니다", Toast.LENGTH_SHORT).show()
    }
}
// When launching it
bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
```

- This has the **same shape** as the `setResult` result-receiving pattern from the week 10 demo. All you read is `resultCode`.
- `PermissionHelper.isBluetoothEnabled(this)` tells you whether Bluetooth is already on.

---

## Day 1 · 13–20 min ② — Check Order: Permission → Bluetooth → Scan

```kotlin
binding.scanButton.setOnClickListener {
    if (hasBlePermissions() == false) {
        permissionLauncher.launch(PermissionHelper.required())
    } else if (PermissionHelper.isBluetoothEnabled(this) == false) {
        bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))
    } else {
        // Scan happens here
    }
}
```

- This chains `else if` onto week 1's `if/else`. Only the **first matching branch**, from the top, runs.
- On Android 12+, even the enable-Bluetooth prompt needs permission first, so we **check permission first**.
- Scanning does not start automatically right after granting permission or turning Bluetooth on. Tap **[검색]** (Scan) again.

---

## Day 1 · 20–27 min ① — Adding the Provided bleuno Library

1. In `com.example.smartio`: **New › Package** › `bleuno` → paste in the 8 files from `src/`
2. Delete week 11's `ConnState.kt` and `Permissions.kt` → import `ConnState`, use `PermissionHelper.required()`

```kotlin
private val useFake = true                    // false if you have a board
private lateinit var client: BleunoClient     // same pattern as binding

// Inside onCreate, below the insets block
client = Bleuno.client ?: Bleuno.create(this, useFake)
```

- `Bleuno.client` is one client shared by the whole app. It starts out `null`.
- Thanks to `?:`, even if rotation calls `onCreate` again, it reuses the **one already created**.

---

## Day 1 · 20–27 min ② — Replacing Week 11's Fake Scan with startScan

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

- `5000` is milliseconds (5 seconds). `onFound =` and `onFinished =` are labels marking **which parameter** each lambda fills.
- Both are called on the main thread, so you can update views directly inside them (no `runOnUiThread` needed).

---

## Day 1 · 20–27 min ③ — [중지] (Stop) and onStop

```kotlin
binding.stopButton.setOnClickListener {
    client.stopScan()          // onFinished is called once
}

override fun onStop() {
    super.onStop()
    unregisterReceiver(batteryReceiver)
    client.stopScan()          // Stop scanning when leaving the screen too
}
```

- You don't write separate code in [중지] (Stop) to restore the buttons — `onFinished` handles it.
- Week 10's pairing rule: **stop whatever you started when the screen is no longer visible.**
- Fake results: `ESP32_BLE_FAKE1` after 1s, `ESP32_BLE_FAKE2` after 2s, `검색 완료 · 장치 수: 2` after 5s

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--fake로-보드-검색하기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Add the `bleuno` package and clean up week 11's `ConnState.kt` and `Permissions.kt`.
2. Create `useFake`, `client`, and `bluetoothLauncher`, and get the client in `onCreate`.
3. Wire [검색] (Scan) to permission → Bluetooth → `startScan`; wire [중지] (Stop) and `onStop` to `stopScan()`.
4. Take a portrait screenshot with `ESP32_BLE…` in the list. Use `useFake = false` if you have a board.

**Explanation total: 5+8+7+7+3 = 30 min**

Watch the `startScan(가짜)` and `onScanResult(가짜)` lines together with the Logcat filter `package:mine tag:BLE`.

---

# Day 2 — Connecting and Viewing State on Both Screens

`30 min explanation & demo → 60 min lab`

1. Read the connection callback chain through Logcat `tag:BLE`
2. Tap a list row → `client.connect(address)`, receive state with the week 7 collect pattern
3. Share one connection with the control screen through `object Bleuno`
4. Handling zero results, Bluetooth off, and location services off

---

## Day 2 · 0–8 min ① — The Special-Lecture Callback Chain at a Glance

```text
startScan → (5s) stopScan
connectGatt(address, autoConnect=false)                            연결 중
 └▶ onConnectionStateChange(STATE_CONNECTED) → requestMtu(185)    서비스 확인 중
     └▶ onMtuChanged → discoverServices()
         └▶ onServicesDiscovered → find characteristic
             └▶ Enable notifications (write CCCD) → onDescriptorWrite   준비됨
STATE_DISCONNECTED → gatt.close()                                연결 안 됨 / 끊김
```

- The callbacks you wrote by hand in the special lecture are **still there, unchanged**, inside `RealBleunoClient.kt`.
- We call just one line, `connect`, and read the result as the **state text** on the right.

---

## Day 2 · 0–8 min ② — Reading It Through Logcat tag:BLE

```text
connectGatt(84:F7:03:xx:xx:xx, autoConnect=false)
onConnectionStateChange: status=0 newState=2
STATE_CONNECTED → requestMtu(185)
onMtuChanged: mtu=185 status=0 → discoverServices()
onServicesDiscovered: status=0
characteristic 확보: f6aa83ca-de53-46b4-bdea-28a7cb57942e
onDescriptorWrite: status=0 → 준비됨
```

- Filter: `package:mine tag:BLE`. The last line printed tells you **how far the process got**.
- Fake mode prints three lines tagged `(가짜)`: `connectGatt(가짜)` → `onConnectionStateChange(가짜)` → `onServicesDiscovered(가짜) … 준비됨`
- After `준비됨`, a line `onCharacteristicChanged(가짜): {"event":"input",…}` prints every 10 seconds. That's for week 14 — ignore it for now.

---

## Day 2 · 8–18 min ① — Tap a List Row → connect(address)

```kotlin
val addresses = mutableListOf<String>()      // same order as devices

devices.add("$name ($address)")              // inside onFound
addresses.add(address)

binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    // … the 3 lines from week 11 (name field, Toast), unchanged
    val address = addresses.get(position)
    client.stopScan()
    client.connect(address)
}
```

- Keep the visible text (`devices`) and the address used to connect (`addresses`) at the **same index**.
- **A BLE connection starts by tapping a list row.** [연결] (Connect) is still the "carry just the name over" button you built in week 4.

---

## Day 2 · 8–18 min ② — client.connectionState in the Week 7 collect Pattern

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        client.connectionState.collect { state ->    // week 7: viewModel.state.collect
            binding.stateText.text = state
            // … turn everything off first, then use when (state) to turn on only what matches
        }
    }
}
```

- The pattern is unchanged from week 7 — only **what you collect** changes. The values are the five `ConnState` strings.
- The library now produces the state, so delete `ConnViewModel.kt` and step 9 (the remaining-seconds collect).
- The screen shows `연결 중` → `서비스 확인 중` → `준비됨` in order. There's no countdown number.

---

## Day 2 · 8–18 min ③ — Buttons per State: [제어 화면] When Ready

| State | What's enabled |
|---|---|
| `연결 안 됨` | [검색] |
| `연결 중` | Only the ProgressBar ([검색]·[중지]·[해제]·[제어 화면] off) |
| `서비스 확인 중` | Only the ProgressBar |
| `준비됨` | [해제], **[제어 화면]** |
| `끊김` | [검색], [다시 시도] |

```kotlin
ConnState.READY -> {
    binding.disconnectButton.isEnabled = true
    binding.controlButton.isEnabled = true
}
```

- [중지] (Stop), which used to turn on during week 7's `CONNECTING`, now means **stop scanning**, so it's not enabled here.

---

## Day 2 · 8–18 min ④ — Sharing One Connection with object Bleuno

```kotlin
// End of ControlActivity onCreate
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        Bleuno.client?.connectionState?.collect { state ->
            binding.stateText.text = "상태: $state"
        }
    }
}
```

- `object Bleuno { var client }` holds one client that **both screens share**. A connection can't be passed through an Intent.
- `Bleuno.client` is `BleunoClient?`, so call it with week 3's `?.`. Don't use `!!`.
- Rotating the screen while `준비됨` keeps the state (`Bleuno.client ?:`). Only the list clears, as in week 11.

---

## Day 2 · 18–25 min ① — [다시 시도] (Retry) at Zero Results

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

- [다시 시도] (Retry) is one line: `binding.scanButton.performClick()`. It presses [검색] (Scan) in code.
- Zero results is not an app bug. Check whether the board LED is **blinking blue** (it won't be if the board is already connected to another phone).
- To see this in Fake mode, tap [중지] (Stop) within 1 second of [검색] (Scan).

---

## Day 2 · 18–25 min ② — Location Services (Android 11 and Below) and the Check Chain

```kotlin
if (hasBlePermissions() == false) {
    permissionLauncher.launch(PermissionHelper.required())       // permission
} else if (PermissionHelper.isBluetoothEnabled(this) == false) {
    bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))   // Bluetooth
} else if (isLocationOff()) {
    showLocationDialog()                                          // location (API 30 and below)
} else {
    // scan
}
```

- `isLocationOff()`: returns `true` when `Build.VERSION.SDK_INT <= 30` and location is off (same shape as function 13).
- The dialog follows the shape of week 10's `showPermissionDialog()`, plus `Settings.ACTION_LOCATION_SOURCE_SETTINGS`.
- Only show the dialog **from the click listener**. In `onFinished`, called 5 seconds later, just change the text.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--연결하고-두-화면에서-상태-보기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Add the [제어 화면] (Control Screen) button and a state-text spot on the control screen.
2. Change collect step 7 to `client.connectionState` and delete `ConnViewModel.kt`.
3. Address list → tap a row → `connect` → [제어 화면] enabled when `준비됨` → control screen shows `상태: 준비됨`.
4. Add the zero-result message and location check, then capture the `준비됨` screen + Logcat `tag:BLE`.

**Explanation total: 8+10+7+5 = 30 min**

If it stays on `연결 중` for a long time, check the board's power and distance. A real board usually becomes `끊김` after about 30 seconds.

---

## What to Submit

Submit once, at the end of Day 2.

1. **`MainActivity.kt`**, **`ControlActivity.kt`**
2. **Screenshot 1**: portrait connection screen with an `ESP32_BLE…` row visible after [검색] (Scan)
3. **Screenshot 2**: the `준비됨` screen and the connection lines in Logcat `package:mine tag:BLE`
4. **Photo**: the board once its blue blinking stops after connecting (skip if you have no board/device; use Fake for screenshot 2)

---

## Next Week Preview

Right now, the control screen's LED switch **only writes** `on 3` to the log.

In week 13, you'll send a real command to the board with `Bleuno.client?.send("on 3")`,

and receive the board's reply `{"result":"ok","ms":"led(s) on"}` through `onMessage { }` to add to the log.
