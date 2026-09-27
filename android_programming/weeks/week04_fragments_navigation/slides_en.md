---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 4
footer: SmartIO Kickoff · ViewBinding · EditText · Switch · Second Screen
---

# Starting SmartIO: ViewBinding, Input Widgets, a Second Screen

The last 3 weeks were `StudentCard`.
From today until the end of the term, we build **Smart I/O Controller**.

```text
[Connect screen]             [Control screen]
Device name: ESP32_BLE_1 →   Device: ESP32_BLE_1
Auto-connect (O)             Pin: 3   LED (O)
      [Connect]              Command log
                              on 3
                              off 3
```

---

# Day 1 — Building the Connect Screen

`30 min explanation & demo → 60 min lab`

1. New project `SmartIO` and ViewBinding
2. Text goes in `strings.xml`
3. Read input with `EditText`, toggle with `Switch`

---

## Day 1 · 0–5 min — Today's Syntax: Building Strings and Checking Empty Values

```kotlin
val pin = "3"
val command = "on $pin"        // "on 3"  (same $variable syntax as Week 1)
val number = pin.toInt()       // 3      (text → number)
val name = ""
name.isEmpty()                 // true   (no characters at all)
```

- `"on $pin"`: this is how we build the command string sent to the board in Week 13.
- `.toInt()`: crashes on non-numeric text, so use it **after checking for empty input**.
- `isEmpty()`: use it to check whether an input field is blank.

---

## Day 1 · 5–15 min ① — New Project SmartIO

1. **File › New › New Project** → **Empty Views Activity**
2. Name: `SmartIO` · Package: `com.example.smartio` · Language: **Kotlin**
3. Click **Finish** → after sync finishes, **Run ▶** → `Hello World!`

| Week 2 | Today |
|---|---|
| `StudentCard` | `SmartIO` (app name Smart I/O Controller) |
| `findViewById` | **ViewBinding** `binding.xxx` |

Leave `StudentCard` closed. From today we only use `SmartIO`.

---

## Day 1 · 5–15 min ② — Turning On ViewBinding

Add this inside `android { }` in `build.gradle.kts (Module :app)`, then **Sync Now**

```kotlin
    buildFeatures {
        viewBinding = true
    }
```

- Once on, each layout gets its own class: `activity_main.xml` → `ActivityMainBinding`
- In `dependencies { }`, paste the four lines for Weeks 5–7 from [Walkthrough Step 3](walkthrough.md#3-viewbinding-켜기와-의존성-넣기).
  You can skip them this week since we don't use them yet. If Sync fails, remove the four lines and Sync again.

---

## Day 1 · 5–15 min ③ — Calling Views with binding

```kotlin
private lateinit var binding: ActivityMainBinding      // template

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()
    binding = ActivityMainBinding.inflate(layoutInflater)   // template
    setContentView(binding.root)                             // template
    ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets -> … }

    binding.connectButton.setOnClickListener { … }          // no findViewById
}
```

- `@+id/connectButton` → `binding.connectButton`. A different spelling shows a red underline.
- `lateinit var binding` marks "filled in later." Keep these three lines as is.

---

## Day 1 · 15–20 min — strings.xml and the Hardcoded String Warning

```xml
<!-- res/values/strings.xml -->
<string name="app_name">Smart I/O Controller</string>
<string name="connect">Connect</string>
```

```xml
<Button android:text="@string/connect" … />
```

- Writing text directly in XML triggers the yellow `Hardcoded string` warning (you saw this in Week 2).
- Collect text in `strings.xml` and refer to it as `@string/name`.
- Sentences you build in code (`"Connect: $name"`) can stay as is.

---

## Day 1 · 20–27 min ① — EditText: Reading Input

```xml
<EditText android:id="@+id/deviceNameEdit"
    android:hint="@string/device_name_hint" android:inputType="text" … />
```

```kotlin
val name = binding.deviceNameEdit.text.toString()
if (name.isEmpty()) {
    Toast.makeText(this, "Enter a device name", Toast.LENGTH_SHORT).show()
} else {
    Toast.makeText(this, "Connect: $name", Toast.LENGTH_SHORT).show()
}
```

- `hint` is the faint guide text shown when the field is empty.
- `.text` is a text box object; add `.toString()` to get a String.

---

## Day 1 · 20–27 min ② — Switch: On and Off

```xml
<Switch
    android:id="@+id/autoSwitch"
    android:text="@string/auto_connect" … />
```

```kotlin
binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
    if (isChecked) {
        Toast.makeText(this, "Auto-connect on", Toast.LENGTH_SHORT).show()
    }
}
```

- Two names before the arrow: the first is the switch itself (unused, so `_`); the second, `isChecked`, is whether it's on.
- `{ }` runs both when turning it on and off. Use `isChecked` to tell them apart.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--연결-화면-만들기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Create `SmartIO` and turn on ViewBinding.
2. Place a title, a device name `EditText`, an auto-connect `Switch`, and a [Connect] button.
3. [Connect]: Toast `Enter a device name` if empty, otherwise `Connect: name`.
4. Toast `Auto-connect on` when the Switch turns on. Do the "turn off" case **yourself**.

**Explanation total: 5+10+5+7+3 = 30 min**

If you get stuck, check `viewBinding = true` and Sync, then the spelling after `binding.`.

---

# Day 2 — Passing the Name to a Second Screen

`30 min explanation & demo → 60 min lab`

1. Creating `ControlActivity` and the Manifest
2. Passing the name with `Intent`/`putExtra`, returning with `finish()`
3. Control screen: pin number · LED Switch · command log

---

## Day 2 · 0–5 min — Today's Syntax: Missing Extras · else if

```kotlin
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "Device: $name"
```

- `getStringExtra("name")` might return nothing, so it's `String?` (Week 3).
- `?: ""` — use an empty string if it's missing. We never use `!!`.
- The key `"name"` used with `putExtra("name", …)` and when reading it back must match.

```kotlin
if (pin.isEmpty()) { … } else if (isChecked) { … } else { … }
```

- `else if`: chains another condition. You can also nest `if/else` inside `if`.

---

## Day 2 · 5–20 min ① — Creating a Second Activity

Right-click `com.example.smartio` in the Project panel
**New › Activity › Empty Views Activity**

| Field | Value |
|---|---|
| Activity Name | `ControlActivity` |
| Layout Name | `activity_control` (automatic) |
| Launcher Activity | **leave unchecked** |

Three files are created: `ControlActivity.kt` · `activity_control.xml` · one line in the Manifest

---

## Day 2 · 5–20 min ② — The Line Added to the Manifest

`app › manifests › AndroidManifest.xml`

```xml
<activity
    android:name=".ControlActivity"
    android:exported="false" />
```

- An Activity must be **registered** in the Manifest before it can be opened. The wizard adds this automatically.
- If you create an Activity file by hand, add this line yourself.
- `exported="false"`: other apps cannot open this screen.

---

## Day 2 · 5–20 min ③ — Moving with Intent and Passing a Value

```kotlin
val intent = Intent(this, ControlActivity::class.java)
intent.putExtra("name", name)
startActivity(intent)
```

| Line | Meaning |
|---|---|
| `Intent(this, ControlActivity::class.java)` | "from here to ControlActivity" — an explicit Intent |
| `putExtra("name", name)` | puts a value under the key `"name"` |
| `startActivity(intent)` | opens the next screen |

If `Intent` turns red, **Alt+Enter** to import `android.content.Intent`.

---

## Day 2 · 5–20 min ④ — Receiving the Value and finish()

```kotlin
// ControlActivity.kt
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "Device: $name"

binding.backButton.setOnClickListener {
    finish()          // close this screen, go back to the previous one
}
```

```text
MainActivity ──startActivity──▶ ControlActivity
MainActivity ◀───finish()────── ControlActivity
```

The system Back button (◀) does the same thing as `finish()`.

---

## Day 2 · 20–25 min — Activity and Fragment

```text
Activity (one screen)           Activity
┌──────────────┐               ┌──────────────┐
│              │               │ Fragment A   │  ← a piece of the screen
│  Views       │               ├──────────────┤
│              │               │ Fragment B   │  ← can be swapped in and out
└──────────────┘               └──────────────┘
```

- A Fragment is **a piece of a screen inside an Activity**. One Activity can hold several, or swap between them.
- This term's SmartIO uses two Activities. We demo Fragments in Week 9.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--제어-화면과-명령-로그-60분) · [Walkthrough](walkthrough.md#2일차)

1. Create `ControlActivity` and show `Device: name` at the top, passed from [Connect].
2. Place a pin number `EditText` (`inputType="number"`), an LED `Switch`, and a log `TextView`.
3. `append` `on 3` to the log when the Switch turns on, `off 3` when it turns off. Toast if the pin is empty.
4. [Back] calls `finish()`. Submit 2 screenshots.

**Explanation total: 5+15+5+5 = 30 min**

---

## What to Submit

Submit these four items once, at the end of Day 2.

1. **`MainActivity.kt`**
2. **`ControlActivity.kt`**
3. **Screenshot 1**: the connect screen with a device name typed in
4. **Screenshot 2**: the control screen showing that name at the top, with `on 3` / `off 3` in the log

---

## Next Week Preview

Right now, pressing [Connect] jumps to the control screen **instantly**.

A real device scan takes about 5 seconds. What happens if the screen freezes during those 5 seconds?

In Week 5 you'll learn about the **main thread and background work**, and build a [Scan] button.
