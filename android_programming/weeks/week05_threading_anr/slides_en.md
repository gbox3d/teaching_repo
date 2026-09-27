---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 5
footer: Main Thread and Background Work · Thread · Handler
---

# Main Thread and Background Work: Thread, Handler

We add a **[Scan]** button to the connect screen built in Week 4.
This week's goal is to fake a 5-second scan **without freezing the screen**.

```text
Smart I/O Controller
Device name [ESP32_BLE      ]
Auto-connect              (  )
      [Scan] [Stop]
         ◌
       Scanning…
        [Connect]
```

---

# Day 1 — Keeping the Screen Responsive: Main Thread and Thread

`30 min explanation & demo → 60 min lab`

1. Today's syntax: using outer variables inside a lambda
2. What happens if you put `Thread.sleep(5000)` in [Scan]
3. `Thread { }.start()` and `runOnUiThread { }`

---

## Day 1 · 0–5 min — Today's Syntax: Using Outer Variables Inside a Lambda

```kotlin
var count = 0                          // outside the lambda
plusButton.setOnClickListener {        // the lambda { }
    count = count + 1                  // changes the outer variable (Week 2)
}
```

```kotlin
val name = binding.deviceNameEdit.text.toString()   // outside the lambda
Thread {
    Thread.sleep(5000)
    runOnUiThread { binding.stateText.text = "Scan complete: $name" }
}.start()
```

- Inside `{ }`, you can read and change variables created outside it, as is.
- Even if the lambda runs **5 seconds later**, it still remembers `name`.

---

## Day 1 · 5–15 min ① — Putting Thread.sleep(5000) in [Scan]

```kotlin
binding.scanButton.setOnClickListener {
    binding.stateText.text = "Scanning…"
    Thread.sleep(5000)                 // wait 5 seconds (this is wrong)
    binding.stateText.text = "Scan complete"
}
```

Observations:

- `Scanning…` **never appears** — after 5 seconds it jumps straight to `Scan complete`.
- During that time, the Switch and [Connect] don't respond either.
- Logcat: `Skipped 299 frames! The application may be doing too much work on its main thread.` (the number varies each run)

---

## Day 1 · 5–15 min ② — The Main Thread and Its Message Queue

```text
Touch ─┐
Draw    ┼─▶ Message queue ─▶ the main thread processes them one at a time
Click  ─┘                     │
                    a long task makes everything after it wait
```

- Drawing the screen and handling button clicks are both processed in order, on a single **main thread**.
- `Thread.sleep(5000)` blocks this thread for 5 seconds. That's why the text doesn't change and buttons don't respond.
- `stateText.text = "Scanning…"` only adds a "please redraw" request to the queue — the redraw happens only after the click handler finishes.

---

## Day 1 · 5–15 min ③ — ANR: Application Not Responding

If the main thread can't respond to touch for **more than 5 seconds**, the system stops the app.

```text
ANR in com.example.smartio (com.example.smartio/.MainActivity)
Reason: Input dispatching timed out (... Waited 5002ms for MotionEvent).
```

- ANR = Application Not Responding. An "App isn't responding" dialog may appear.
- One rule: **never do slow, waiting work on the main thread.**
- So who waits the 5 seconds? → a different thread.

---

## Day 1 · 15–25 min ① — Thread { }.start() and runOnUiThread { }

```kotlin
binding.scanButton.isEnabled = false
binding.stateText.text = "Scanning…"
Thread {                               // work to do on a new thread
    Thread.sleep(5000)                 // waiting here doesn't freeze the screen
    runOnUiThread {                    // hand screen changes back to the main thread
        binding.stateText.text = "Scan complete"
        binding.scanButton.isEnabled = true
    }
}.start()                              // forget start() and nothing happens
```

```text
Main:   click → show "Scanning…" → start Thread → (draws/handles clicks freely) → "Scan complete" + button restored
Worker:                waits 5s ──▶ runOnUiThread { … } ──▶ hands back to main ─┘
```

---

## Day 1 · 15–25 min ② — Touching a View from a Worker Thread

```kotlin
Thread {
    Thread.sleep(5000)
    binding.stateText.text = "Scan complete"      // changed without runOnUiThread?
}.start()
```

The app crashes, and Logcat shows this.

```text
FATAL EXCEPTION: Thread-2
android.view.ViewRootImpl$CalledFromWrongThreadException:
Only the original thread that created a view hierarchy can touch its views.
Expected: main Calling: Thread-2
```

- Only the **main thread** may change Views. Wrap worker-thread changes in `runOnUiThread { }`.
- Set `isEnabled = false` so [Scan] can't be pressed again while scanning.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--검색-버튼을-멈추지-않게-만들기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Add a [Scan] button and a status TextView to the connect screen.
2. On press, disable the button and show `Scanning…`.
3. Wait 5 seconds in a `Thread`, then use `runOnUiThread` for `Scan complete`, restoring the button, and a Toast.

**Explanation total: 5+10+10+5 = 30 min**

If you get stuck, check `.start()` and whether View code is inside `runOnUiThread { }`.

---

# Day 2 — Scheduling and Canceling: Handler, postDelayed, ProgressBar

`30 min explanation & demo → 60 min lab`

1. Find `postDelayed` in last year's BLE special-lecture code
2. Schedule work 5 seconds ahead with `Handler(Looper.getMainLooper())`, cancel it with [Stop]
3. Show scanning is in progress with `ProgressBar`

---

## Day 2 · 0–5 min — A Piece of Last Year's Special-Lecture Code: postDelayed

From the instructor's BLE test app (you'll see it again in Week 12) — the part that stops scanning after 5 seconds.

```kotlin
private val mHandlerBleScanTimeout = Handler(Looper.getMainLooper())

bluetoothLeScanner.startScan(mScanCallback)
mHandlerBleScanTimeout.postDelayed({
    bluetoothLeScanner.stopScan(mScanCallback)
    Log.d("MainActivity", "scan timeout")
}, 5000)
```

- "Run this code in 5 seconds" fits in **one call**. No new thread, no `sleep`.
- Today we move this one call into our [Scan] code.

---

## Day 2 · 5–15 min ① — Handler(Looper.getMainLooper()) and postDelayed

```kotlin
private val handler = Handler(Looper.getMainLooper())   // inside the class, outside onCreate
```

```kotlin
handler.postDelayed({
    binding.stateText.text = "Scan complete"      // runs on the main thread
}, 5000)
```

- A `Handler` is a **handle for adding work to the main thread's message queue.**
- `postDelayed(work, milliseconds)`: adds a "run this after 5000ms" entry to the queue.
- The main thread runs it, so `runOnUiThread` isn't needed.
- If `Handler`/`Looper` turns red, Alt+Enter → pick the `android.os` one.
- This form (an unnamed `{ }`) **can't be canceled** → the next slide gives it a name.

---

## Day 2 · 5–15 min ② — A Named Runnable and removeCallbacks

```kotlin
val finishScan = Runnable {            // give the work a name
    binding.stateText.text = "Scan complete"
    binding.scanButton.isEnabled = true
}

handler.postDelayed(finishScan, 5000)  // [Scan]: schedule to run in 5 seconds
handler.removeCallbacks(finishScan)    // [Stop]: cancel that schedule
```

- To cancel, you must pass the **same named** object. A fresh `{ }` in `removeCallbacks { }` won't cancel it.
- `removeCallbacks` only removes work that **hasn't run yet.** Once it has run, there's nothing left to remove.

---

## Day 2 · 15–25 min ① — ProgressBar: The Spinning Circle

```xml
<ProgressBar
    android:id="@+id/scanProgress"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:visibility="gone" />
```

```kotlin
binding.scanProgress.visibility = View.VISIBLE   // show it
binding.scanProgress.visibility = View.GONE      // remove it entirely, no space kept
```

- A default ProgressBar is a **spinning circle** for work with no known duration. No number needed.
- If `View` turns red, Alt+Enter → `android.view.View`.

---

## Day 2 · 15–25 min ② — Screen States While Scanning and Not

| State | [Scan] | [Stop] | ProgressBar | Status text |
|---|---|---|---|---|
| Start | enabled | disabled | `GONE` | `Waiting` |
| [Scan] pressed | disabled | enabled | `VISIBLE` | `Scanning…` |
| `finishScan` after 5s | enabled | disabled | `GONE` | `Scan complete` + Toast |
| [Stop] pressed | enabled | disabled | `GONE` | `Scan stopped` |

- Each state changes **four things** together. Miss one and a button won't respond, or the circle keeps spinning.
- In XML, start [Stop] with `android:enabled="false"` and the ProgressBar with `android:visibility="gone"`.

---

## Day 2 · 25–30 min — A Word on AsyncTask, Then Try It Yourself

[Day 2 lab](lab.md#2일차--handler로-예약하고-중지로-취소하기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Replace Day 1's `Thread` with `handler.postDelayed(finishScan, 5000)`.
2. [Stop] button: `removeCallbacks(finishScan)` + reset the screen.
3. Show the ProgressBar only while scanning.

Older code you may see uses a tool called `AsyncTask`. It's legacy and unused today — starting Week 6 we use **coroutines**.

**Explanation total: 5+10+10+5 = 30 min**

---

## What to Submit

Submit these three items once, at the end of Day 2.

1. **`MainActivity.kt`**
2. **`activity_main.xml`**
3. **Two screenshots**: scanning (button disabled, ProgressBar showing), and either the `Scan complete` Toast or the screen after pressing [Stop]

---

## Next Week Preview

To count down the remaining time as `5, 4, 3, 2, 1` during a scan, you'd need to stack five `postDelayed` calls.

In Week 6, a single `delay(1000)` line with **coroutines** builds the countdown, plus a [Retry] flow for when a fake connection fails.
