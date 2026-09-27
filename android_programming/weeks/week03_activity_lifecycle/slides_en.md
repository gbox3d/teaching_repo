---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 3
footer: Activity Lifecycle · Logcat · Save and Restore
---

# Activity Lifecycle and Saving State

At the end of Week 2, you set the number to `3` and rotating the screen turned it back to `0`.
This week you see **why** with Logcat, and make `3` survive a rotation.

```text
Before rotation          After rotation
  3          →→→          3
[-1] [Reset] [+1]     [-1] [Reset] [+1]
```

---

# Day 1 — Watching a Screen's Life with Logcat

`30 min explanation & demo → 60 min lab`

1. Filter Logcat to show only your app's log lines.
2. Add `Log.d` to all 7 lifecycle callbacks.
3. Show a Toast when `+1` is pressed.

---

## Day 1 · 0–8 min ① — Logcat: The Log an App Leaves Behind

```kotlin
Log.d("Life", "onCreate")
```

| Week 1 (Playground) | Week 3 (app) |
|---|---|
| `println("onCreate")` | `Log.d("Life", "onCreate")` |

- `Log.d(tag, text)`: writes one line to the Logcat panel.
- The tag `Life` is a name we chose. It's used to filter the log.
- If `Log` turns red, **Alt+Enter** (⌥+Enter on Mac) → `android.util.Log`

---

## Day 1 · 0–8 min ② — The Logcat Panel and Filters

1. Open **Logcat** in the bottom toolbar (or View › Tool Windows › Logcat).
2. Type `package:mine tag:Life` in the filter box and press Enter.
3. Run the app; you should see one line.

```text
Life   com.example.studentcard   D   onCreate
```

- `package:mine`: only my app · `tag:Life`: only lines tagged `Life`
- If you see nothing, check the filter spelling and the selected device.

---

## Day 1 · 8–20 min ① — The 7 Lifecycle Callbacks

```text
onCreate → onStart → onResume    the screen is visible and touchable
                        │ Home button · another app · rotation
                        ▼
              onPause → onStop → onDestroy
                          │
                 onRestart → onStart → onResume   (coming back)
```

- The system calls these **on its own, when it needs to.** We never call them ourselves.
- 3 when created, 3 when destroyed, plus `onRestart` when coming back = 7 total.
- Don't memorize the names — watch Logcat to see **when** each one fires.

---

## Day 1 · 8–20 min ② — Hooking In with override

```kotlin
override fun onStart() {
    super.onStart()
    Log.d("Life", "onStart")
}
```

- `override fun`: **plugs your own code** into a function the system calls.
- `super.onStart()`: lets the original work happen first. **Remove it and the app crashes.**
- Location: below `onCreate`'s closing `}`, above the class's closing `}`.
- Write the other five the same way, just with different names.

---

## Day 1 · 8–20 min ③ — Rotating the Emulator Screen

| Method | How |
|---|---|
| Button | The rotate buttons in the emulator's **top** toolbar: **Rotate Left** · **Rotate Right** |
| Shortcut | Click the emulator screen once, then **Ctrl+L** · **Ctrl+R** (⌘+L · ⌘+R on Mac) |

- Each press rotates the device 90 degrees. Use the opposite button to go back to portrait.
- If the emulator is a separate window, the toolbar is on the **right**, and the shortcuts are **Ctrl+←** · **Ctrl+→**.

**If the device rotates but the app screen doesn't**, auto-rotate is off on the device.

1. Tap the **rotate icon** that appears in a corner for a few seconds, or
2. Swipe down from the top and turn on **Auto-rotate** in quick settings.

---

## Day 1 · 8–20 min ④ — Rotation Kills A and Creates B

```text
Before rotation   MainActivity A   count = 3
            onPause → onStop → onDestroy        A disappears
After rotation   MainActivity B   count = 0
            onCreate → onStart → onResume       B is born fresh
```

- Rotation doesn't just turn the screen — it **creates a new Activity**.
- B's `onCreate` runs `var count = 0` again, so it becomes `0`.
- Day 2: **save** before A disappears, then **restore** when B is born.

---

## Day 1 · 20–25 min — Toast: A Brief Pop-up Message

```kotlin
Toast.makeText(this, "Current number: $count", Toast.LENGTH_SHORT).show()
```

| Argument | Meaning |
|---|---|
| `this` | Where: this screen (MainActivity) |
| `"Current number: $count"` | What: the text to show |
| `Toast.LENGTH_SHORT` | How long: short (`LENGTH_LONG` is longer) |

- Drop the trailing `.show()` and it's built but never shown.
- If `Toast` turns red, Alt+Enter → `android.widget.Toast`

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--생명주기-로그와-toast-60분) · [Walkthrough](walkthrough.md#1일차)

1. Open the Week 2 project and set the Logcat filter to `package:mine tag:Life`.
2. Add `Log.d` to all 7 callbacks, then record run · Home · return · rotate · Back in the log sheet.
3. Show a Toast when `+1` is pressed.

**Explanation total: 8+12+5+5 = 30 min**

If you get stuck, check the `super` line, `override`, and imports first.

---

# Day 2 — Keep the Number After Rotation

`30 min explanation & demo → 60 min lab`

1. Today's syntax: handling values that can be empty.
2. Save before disappearing: `onSaveInstanceState`.
3. Restore when reborn: `savedInstanceState`.

---

## Day 2 · 0–5 min — Today's Syntax: Null Safety

```kotlin
val bag: Bundle? = null        // ?  : a type that can be empty (null)
bag?.getInt("count")           // ?. : if bag is null, this whole expression is null
bag?.getInt("count") ?: 0      // ?: : use 0 if the left side is null
```

- A type with `?` means the value **might be missing**.
- We never use `!!`. If the value is null, the app crashes.
- `savedInstanceState` in `onCreate(savedInstanceState: Bundle?)` is exactly this type:
  null on first run, and holding your saved values after a rotation.

---

## Day 2 · 5–17 min ① — Moving count Right Inside the Class

```kotlin
class MainActivity : AppCompatActivity() {
    var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
```

- `var count = 0` inside `onCreate` is visible only inside `onCreate`.
- We need it in the save function too, so we move it **right inside the class**.
- Delete the `var count = 0` line inside `onCreate`. Leave the button code as is.

---

## Day 2 · 5–17 min ② — Saving with onSaveInstanceState

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putInt("count", count)
    Log.d("Life", "onSaveInstanceState count=$count")
}
```

- The system calls this before the screen disappears. `outState` is a bag (Bundle) for holding values.
- `putInt("count", count)`: puts the number in, tagged `"count"`.
- `outState: Bundle` has **no** `?`. The bag always arrives.

---

## Day 2 · 5–17 min ③ — Restoring in onCreate

```kotlin
count = savedInstanceState?.getInt("count") ?: 0
countText.text = "$count"
```

| Situation | `savedInstanceState` | `count` |
|---|---|---|
| First run | null | `0` |
| After rotation | the saved bag | `3` |

- The tag `"count"` used when putting a value in must match **exactly** when taking it out.
- Write the restored number back to the screen too.

---

## Day 2 · 17–25 min — Verifying the Restore

1. Run → press `+1` three times → `3`
2. Rotate → `3` is still there **(screenshot 1)**
3. Logcat **(screenshot 2)**

```text
onPause → onStop → onSaveInstanceState count=3 → onDestroy
→ onCreate → onStart → onResume
```

4. Home → return: still `3` (A stayed alive)
5. Back → run again: `0` (a finished app isn't saved — this is expected)

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--회전해도-숫자가-남게-60분) · [Walkthrough](walkthrough.md#2일차)

1. Move `count` right inside the class, and save it in `onSaveInstanceState`.
2. Read it back in `onCreate` with `?.` and `?:`, and write it to the screen.
3. Check `3` → rotate → `3`, and keep 2 screenshots.

**Explanation total: 5+12+8+5 = 30 min**

---

## What to Submit

Submit these three items once, at the end of Day 2.

1. **`MainActivity.kt`**: final code with logs in all 7 callbacks, Toast, and save/restore
2. **Screenshot 1**: the screen still showing `3` after rotating
3. **Screenshot 2**: Logcat showing `onSaveInstanceState count=3` during rotation

---

## Next Week Preview

Starting Week 4, you build a new project: **SmartIO**.

You'll **type in** a device name, **flip a switch** on and off, and move to a **second screen**.

`findViewById` becomes ViewBinding starting Week 4.
