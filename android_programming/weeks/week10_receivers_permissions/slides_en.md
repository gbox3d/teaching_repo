---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 10
footer: BroadcastReceiver and Runtime Permissions
---

# BroadcastReceiver and Runtime Permissions

Last week's comparison table only named **BroadcastReceiver**. This week you build one yourself.
You'll also get the **permission** needed before week 12's BLE scanning.

```text
Battery 80% · Charging       Permission needed
                              [Cancel] [Go to Settings]
```

---

# Day 1 — Receiving Battery Broadcasts

`30 min explanation & demo → 60 min lab`

1. Build a Receiver that listens for broadcasts, using the `object : BroadcastReceiver()` template.
2. Register it in `onStart` and unregister it in `onStop`.
3. Pull the battery value out of the broadcast and show it on screen.

---

## Day 1 · 0–5 min — Today's Syntax: the Receiver Template and !=

```kotlin
private val batteryReceiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // runs every time a broadcast arrives
    }
}
```

- `object : BroadcastReceiver() { … }` is a template that creates **one unnamed Receiver** and stores it in a variable. Copy it as a whole.
- The `?` in `Context?` and `Intent?` is week 3's null safety. Either can be empty.
- One more thing: `!=` means **not equal**. It's the opposite of `==`.
- `if (plugged != 0) "Charging" else "Not charging"` has the same shape as week 1's one-line `if … else`.

---

## Day 1 · 5–15 min ① — Broadcasts and Receivers

```text
System: "the battery changed"  ── Intent(ACTION_BATTERY_CHANGED) ──▶
   IntentFilter(Intent.ACTION_BATTERY_CHANGED)   ← pick out only this broadcast
      └▶ batteryReceiver.onReceive(context, intent) runs
```

- A **broadcast** is an `Intent` the system or an app sends to announce "this happened."
- A **Receiver** is the component that receives it. It has no screen.
- You choose which broadcasts to receive with an `IntentFilter`.
- Today we register it in code. It is not written in the manifest.

---

## Day 1 · 5–15 min ② — Register in onStart, Unregister in onStop

```kotlin
override fun onStart() {
    super.onStart()
    ContextCompat.registerReceiver(this, batteryReceiver,
        IntentFilter(Intent.ACTION_BATTERY_CHANGED), ContextCompat.RECEIVER_NOT_EXPORTED)
}
override fun onStop() {
    super.onStop()
    unregisterReceiver(batteryReceiver)
}
```

- Put both functions **outside** `onCreate()`, directly inside the class — the same spot as week 3's lifecycle callbacks.
- `RECEIVER_NOT_EXPORTED`: broadcasts from other apps are not received. System broadcasts still are.
- If `ContextCompat` or `IntentFilter` shows up in red, import it with Alt+Enter (⌥+Enter on Mac).

---

## Day 1 · 5–15 min ③ — Register and Unregister Come in Pairs

```text
onStart ─ register (registerReceiver) ───▶ onReceive fires when a broadcast arrives
onStop  ─ unregister (unregisterReceiver) ─▶ no longer received
Home / rotate / [Connect] to another screen ─▶ onStop … back again ─▶ onStart registers again
```

- Broadcasts are received only **while the screen is visible**. There's no need to update text on a screen no one can see.
- The app still builds if you skip the unregister — so you have to check the pairing by eye.
- `ACTION_BATTERY_CHANGED` sends its **last value once**, the moment you register. The number appears right when the app opens.

---

## Day 1 · 15–25 min ① — Reading the Battery Value Out of the Intent

```kotlin
val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
if (level == -1) {
    return
}
val percent = level * 100 / scale
val charging = if (plugged != 0) "Charging" else "Not charging"
binding.batteryText.text = "Battery $percent% · $charging"
```

- `getIntExtra(name, default)` is the integer version of week 4's `getStringExtra`. If there's no value, you get the default.
- Since `intent` is an `Intent?`, we add `?.` and `?:`. Drop `?: -1` and `level * 100` is a build error.
- The `%` in `$percent%` is just a plain character tacked on.

---

## Day 1 · 15–25 min ② — Changing the Battery in the Emulator

| Name | Meaning | Emulator's starting value |
|---|---|---|
| `EXTRA_LEVEL` | remaining charge | 100 |
| `EXTRA_SCALE` | value at full charge (usually 100) | 100 |
| `EXTRA_PLUGGED` | 0 if unplugged, nonzero if plugged in | nonzero (AC charger) |

Demo: emulator toolbar **⋯** › **Battery**

- Set Charge level to 80 → `Battery 80% · Charging`
- Set Charger connection to `None` → `Battery 80% · Not charging`
- Go to Home, change the slider, then come back → the new value shows the moment you return

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--배터리-상태-받기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Add `batteryText` (`Battery ?`) to the bottom of the connection screen.
2. Copy the `batteryReceiver` template and fill in `onReceive`.
3. Register in `onStart`, unregister in `onStop`.
4. Change the Battery value to something like 80 and take a screenshot in **portrait**.

**Explanation total: 5+10+10+5 = 30 min**

If `override fun onStart()` shows a red underline, check whether it's **below** `onCreate`'s closing `}`.

---

# Day 2 — Requesting Permission and Handling a Denial

`30 min explanation & demo → 60 min lab`

1. The five steps of runtime permission, plus the manifest declaration.
2. Show the request dialog and receive the result.
3. On denial, show an `AlertDialog` and open Settings.

---

## Day 2 · 0–8 min ① — The Five Steps of Runtime Permission

| Step | What it does | This week's code |
|---|---|---|
| ① Declare | State "this app uses this permission" | `uses-permission` in `AndroidManifest.xml` |
| ② Check | See if it's already granted | `hasBlePermissions()` |
| ③ Explain | Tell the user why it's needed | `AlertDialog` after a denial |
| ④ Request | Show the system permission dialog | `permissionLauncher.launch(…)` |
| ⑤ Result | Update the screen for grant/deny | the request template's `{ _ -> … }` |

- Declaring it in the manifest alone is not enough. The user must approve it **at runtime**.
- Don't ask the moment the app opens — ask when the user taps [Check Permission].

---

## Day 2 · 0–8 min ② — The Manifest Declaration Differs by Version

```xml
<uses-permission
    android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation"
    tools:targetApi="s" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission
    android:name="android.permission.ACCESS_FINE_LOCATION"
    android:maxSdkVersion="30" />
```

- Android 12 (API 31) and above: `BLUETOOTH_SCAN`/`BLUETOOTH_CONNECT`. Android 11 and below: `ACCESS_FINE_LOCATION`.
- `maxSdkVersion="30"`: a declaration used only at API level 30 and below. `BLUETOOTH` and `BLUETOOTH_ADMIN` follow the same pattern (full list in the walkthrough).
- Using `tools:` requires an `xmlns:tools` line on the `<manifest>` tag. New projects usually already have it — **just check**, and add it only if it's missing (adding it twice is a build error).

---

## Day 2 · 8–15 min ① — Picking the Right Permission per Version (a Provided Function)

**Three new shapes today** — this is a file you receive and paste in, so you only need to be able to read it.
① a file with only a function ② `arrayOf(…)` ③ `return a value`

```kotlin
fun blePermissions(): Array<String> {
    if (Build.VERSION.SDK_INT >= 31) {
        return arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        return arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
```

- ① A **file** holding only a function, no class. New › Kotlin Class/File › **File**, name it `Permissions`. Paste it in.
- ② `Array<String>` / `arrayOf(…)`: an array bundling several pieces of text. List syntax comes in week 11.
- ③ `return a value`: the same shape as week 7's `return`, with a value attached. `Build.VERSION.SDK_INT` is the device's Android version number.

---

## Day 2 · 8–15 min ② — Showing the Request Dialog and Getting the Result

```kotlin
private val permissionLauncher =
    registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (hasBlePermissions()) {
            Toast.makeText(this, "Permission OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
    }
```

- Create the request template in the **class-variable spot** (outside `onCreate`). Creating it inside a button freezes the app the instant it's tapped.
- From a button, show the dialog with `permissionLauncher.launch(blePermissions())`.
- `{ _ -> }`: the incoming result isn't read (`_`) — we just **check permissions again** right away.

---

## Day 2 · 8–15 min ③ — Checking One by One with checkSelfPermission

```kotlin
private fun hasBlePermissions(): Boolean {
    for (permission in blePermissions()) {
        if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
            return false
        }
    }
    return true
}
```

- `for (permission in blePermissions())` is the "one at a time through a collection" pattern from week 6's `for (i in 5 downTo 1)`. Copy this line rather than memorizing it.
- If even one permission isn't granted, `return false`; if all pass, `true`.
- The [Check Permission] button (before requesting) and the request template (after requesting) both check through this same function.

---

## Day 2 · 15–23 min ① — On Denial, an AlertDialog

```kotlin
private fun showPermissionDialog() {
    AlertDialog.Builder(this)
        .setTitle("Permission needed")
        .setMessage("Scanning for and connecting to devices requires this permission. Please allow it under Settings › Permissions.")
        .setPositiveButton("Go to Settings") { _, _ ->
            val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
            startActivity(intent)
        }
        .setNegativeButton("Cancel", null)
        .show()
}
```

- Pick **`androidx.appcompat.app.AlertDialog`** from the Alt+Enter list.
- `{ _, _ -> }`: as with week 4's `{ _, isChecked -> }`, unused values are left as `_`.

---

## Day 2 · 15–23 min ② — Opening the Settings Screen with an Implicit Intent

| | Week 4's explicit Intent | Today's implicit Intent |
|---|---|---|
| Code | `Intent(this, ControlActivity::class.java)` | `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))` |
| What you specify | the screen (class) to open | an action (ACTION) + a target (address) |
| Who finds the screen | you decide | the system finds a matching screen |

- `$packageName` is this app's package name (`com.example.smartio`).
- The address must start with `package:`. Leave it off and the app crashes the instant [Go to Settings] is tapped.
- Granting it in Settings and coming back doesn't update the text by itself. Tap [Check Permission] again.

---

## Day 2 · 23–27 min ① — Demo: Getting a Result Back from Another Screen

```kotlin
// MainActivity class-variable spot: same shape as the permission request template
private val controlLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        val message = result.data?.getStringExtra("message") ?: ""
        Toast.makeText(this, "Returned value: $message", Toast.LENGTH_SHORT).show()
    }
}
```

- Replace the [Connect] listener's `startActivity(intent)` with `controlLauncher.launch(intent)`.
- `result.data?.getStringExtra(…) ?: ""` combines week 3's `?.`/`?:` with week 4's `getStringExtra`.
- This is a **demo only** today. It doesn't go into the finished app.

---

## Day 2 · 23–27 min ② — Demo: Returning a Result with setResult

```kotlin
// ControlActivity's [Back] button
binding.backButton.setOnClickListener {
    val result = Intent()
    result.putExtra("message", "Closed the control screen")
    setResult(RESULT_OK, result)
    finish()
}
```

- Closing with [Back] shows the Toast `Returned value: Closed the control screen` on the connection screen.
- Closing with the back gesture skips `setResult`, so no Toast appears.
- In week 12 you'll use this same template to receive the result of a "turn on Bluetooth" request.

---

## Day 2 · 27–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--권한-요청과-거절-안내-60분) · [Walkthrough](walkthrough.md#2일차)

1. Add the [Check Permission] button, the manifest permission declarations, and `Permissions.kt`.
2. Write `hasBlePermissions()` and `showPermissionDialog()`.
3. Add the `permissionLauncher` request template and the [Check Permission] listener.
4. Take screenshots of the denial dialog and the Settings app-info screen.

**Explanation total: 8+7+8+4+3 = 30 min**

If the permission dialog never appears and the AlertDialog shows immediately, check `uses-permission` in the manifest first.

---

## What to Submit

Submit once, at the end of Day 2.

1. **`MainActivity.kt`, `AndroidManifest.xml`**
2. **Screenshot 1**: the connection screen (portrait) after changing the Battery value, showing something like `Battery 80% · Charging`
3. **Screenshot 2**: the `Permission needed` dialog shown after denying the permission
4. **Screenshot 3**: the `Smart I/O Controller` app-info screen opened via [Go to Settings]

---

## Next Week Preview

In week 11 you add a **list of device names** to the connection screen, and **save** the last device connected.

For `Last device: …` to survive turning the app off and back on, where would you need to write it down?

Before week 12's BLE class, connect a physical device and get its permission through this week's flow.
