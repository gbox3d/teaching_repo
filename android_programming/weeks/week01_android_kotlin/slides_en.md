---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 1
footer: Kotlin + XML Views · Smart I/O Controller
---

# Android Execution Structure and Kotlin Diagnostics

## This Week's Question

Can you explain the app's entry point, screen, and logs as one execution flow?

---

# Day 1 — Until the App Runs

`30 min lecture & demo → 60 min lab`

---

## Day 1 · 0–4 min — Start from the Result

Leave execution evidence in three layers.

| Layer | Question | Evidence |
|---|---|---|
| Target | Where did it run? | Device / emulator name |
| UI | What is visible? | Screen and status text |
| Runtime | Which code ran? | Logcat tag |

> "The screen appeared" alone does not tell you which code actually ran.

---

## Day 1 · 4–9 min — Project Map

```text
app/
├─ src/main/AndroidManifest.xml   app & component declarations
├─ src/main/java/.../MainActivity.kt
├─ src/main/res/layout/activity_main.xml
└─ src/main/res/values/strings.xml
```

Follow the chain: `Kotlin code → resource ID → XML View`.

---

## Day 1 · 9–15 min — Startup Flow

```text
Launcher icon
      │ Intent
      ▼
launcher Activity in AndroidManifest
      │ onCreate()
      ▼
setContentView(...) ──▶ XML inflate ──▶ View tree
```

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
}
```

---

## Day 1 · 15–21 min — Run Target and Failure Layers

| Symptom | Check first |
|---|---|
| No run target | Device Manager / USB connection |
| Build fails | First cause in Build Output |
| Install fails | Selected device and storage space |
| Crashes while running | Exception and `Caused by` in Logcat |
| Screen shows something else | Installed app, Activity, layout |

Narrow down the failing layer before changing many lines at once.

---

## Day 1 · 21–27 min — Logcat Is Execution Evidence

```kotlin
private const val TAG = "DeviceInfo"

Log.d(TAG, "onCreate: screen ready")
```

Filter by:

- the running app's process
- your own unique `TAG`
- read the first exception cause, not just the error level

Never log personal data or tokens.

---

## Day 1 · 27–30 min — Handoff to Lab

Lab order:

1. Predict the result before running.
2. Record the target, screen, and log of a normal run.
3. Reproduce one safe error.
4. Narrow the fix using the first cause line.

**Day 1 lecture total: 4+5+6+6+6+3 = 30 min**

---

# Day 2 — Building Screen State with Kotlin

`30 min lecture & demo → 60 min lab`

---

## Day 2 · 0–5 min — Values and Mutability

```kotlin
val model: String = Build.MODEL       // never reassigned
var refreshCount: Int = 0             // state that is meant to change

fun label(name: String, value: String) = "$name: $value"
```

Default to `val`. Choose `var` only when change is required.

---

## Day 2 · 5–10 min — Data Structures and String Formatting

```kotlin
data class DeviceSummary(
    val manufacturer: String,
    val model: String,
    val apiLevel: Int,
)

val summaryText = getString(
    R.string.device_summary_format,
    summary.manufacturer,
    summary.model,
    summary.apiLevel,
)
```

Separate raw data from the localizable display format.

---

## Day 2 · 10–16 min — Nullable Is a Possible State

```kotlin
fun normalizeBuildValue(raw: String?, unknownSentinel: String): String? =
    raw?.trim()?.takeIf {
        it.isNotEmpty() && !it.equals(unknownSentinel, ignoreCase = true)
    }
```

| Input | Result |
|---|---|
| `" Pixel "` | `Pixel` |
| `"   "` | `null` |
| `null` | `null` |
| `"unknown"` | `null` |

`!!` does not remove uncertainty — it defers it to an exception.

---

## Day 2 · 16–22 min — Connecting XML Views and Kotlin

```xml
<TextView
    android:id="@+id/deviceSummary"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:text="@string/device_unknown" />
```

```kotlin
findViewById<TextView>(R.id.deviceSummary).text = getString(
    R.string.device_summary_format,
    summary.manufacturer,
    summary.model,
    summary.apiLevel,
)
```

Keep fallback text and display formats in `strings.xml`.

---

## Day 2 · 22–27 min — Input → Process → Display

```text
Build values / test inputs
          │
          ▼
 normalizeBuildValue(), DeviceSummary
          │
          ▼
       TextView.text
```

Do not test only your device's "normal" values.

- Normal: real manufacturer & model
- Boundary: blank string
- Possible failure: nullable input

---

## Day 2 · 27–30 min — Handoff to Lab

Completion criteria:

- `Device Info` runs.
- The refresh count matches on screen and in the logs.
- `null`, blank, and `Build.UNKNOWN` are shown as the "unknown" fallback resource.
- You can explain the handling without using `!!`.

**Day 2 lecture total: 5+5+6+6+5+3 = 30 min**

---

## Compared with Compose — Not in This Week's Scope

Compose declares UI with Kotlin functions. This course uses **Kotlin + XML Views** so we can explicitly observe Android's View tree, XML resources, and Activity wiring. Compose syntax is neither implemented nor assessed.

---

## Next Week

We split one info text into multiple Views, styles, dimensions, and string resources, and handle screen sizes, rotation, and accessibility.
