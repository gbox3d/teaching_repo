---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 6
footer: Coroutines · delay, cancel, error handling
---

# Coroutines: delay, Cancellation, Error Handling

In Week 5, `Handler` showed "Scan complete" **5 seconds later**.
This week you count down **once a second**, stop it, and handle failure.

```text
Scanning… 3          Connection failed
[Scan] [Stop]         [Scan] [Stop]
                      [Retry]
```

---

# Day 1 — A Countdown Using Coroutines

`30 min explanation & demo → 60 min lab`

1. Repeat five times with `for (i in 5 downTo 1)`
2. Wait one second at a time with `delay(1000)` inside `lifecycleScope.launch { }`
3. Wrap the countdown in one `suspend fun`

---

## Day 1 · 0–5 min — Today's Syntax: for (i in 5 downTo 1)

```kotlin
for (i in 5 downTo 1) {
    println("Scanning… $i")
}
```

```text
Scanning… 5
Scanning… 4
Scanning… 3
Scanning… 2
Scanning… 1
```

- `i` becomes 5, 4, 3, 2, 1 in turn, running the braces **five times**.
- To count up, use `for (i in 1..5)`. Today we only use `downTo`.

---

## Day 1 · 5–17 min ① — Placing a Coroutine Next to Handler

```kotlin
handler.postDelayed(finishScan, 5000)   // Week 5: once, after 5 seconds
```

```kotlin
// Week 6: once per second, five times
lifecycleScope.launch {
    for (i in 5 downTo 1) {
        binding.stateText.text = "Scanning… $i"
        delay(1000)
    }
    binding.stateText.text = "Scan complete"
}
```

- Everything inside `launch { }` is a **coroutine**. `delay(1000)` waits one second.
- It reads top to bottom like ordinary code, yet the screen never freezes.

---

## Day 1 · 5–17 min ② — delay Waits, sleep Blocks

| | `Thread.sleep(1000)` | `delay(1000)` |
|---|---|---|
| The screen during 1 second | **freezes** (Week 5) | keeps moving |
| The number `5 → 1` | hidden, jumps once at the end | changes every second |
| Typing in an EditText | doesn't work | works |
| Where you can use it | anywhere | inside `launch { }` |

Demo: change `delay(1000)` to `Thread.sleep(1000)`, press [Scan], then try tapping an EditText.

`delay` doesn't **hold onto** the main thread while it waits. That's why the screen keeps moving.

---

## Day 1 · 17–25 min ① — suspend fun: A Function That Pauses and Resumes

```text
[Scan] click ─▶ launch ─▶ "Scanning… 5" ─ delay ─ pauses ┐
                                                     │ the screen is free for 1 second
   ┌──────────────────────────────────────────────────┘
   └▶ "Scanning… 4" ─ delay ─ pauses ┐  …  ─▶ "Scan complete"
```

- Functions that can **pause and resume**, like `delay`, are marked `suspend`.
- A `suspend fun` can only be called from a coroutine or another `suspend fun`.
- `suspend` does **not** mean "runs on another thread." It just means it can pause.

---

## Day 1 · 17–25 min ② — Wrapping It in countDown()

```kotlin
private suspend fun countDown() {
    for (i in 5 downTo 1) {
        binding.stateText.text = "Scanning… $i"
        delay(1000)
    }
}
```

- It uses `delay` inside, so it's marked `suspend`. Remove it and you get a red underline.
- Place it **outside** `onCreate()`, right above the class's closing `}`.
- `launch { }` now holds just one line calling `countDown()`, plus the `Scan complete` line after it.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--코루틴-카운트다운-60분) · [Walkthrough](walkthrough.md#1일차)

1. Delete the Handler code from Week 5's [Scan] and replace it with `lifecycleScope.launch { }`.
2. Use `for … downTo` and `delay(1000)` to show `Scanning… 5` down to `1`.
3. Swap in `Thread.sleep` to see the screen freeze, then revert it and wrap the code in `countDown()`.

**Explanation total: 5+12+8+5 = 30 min**

If `delay` turns red, check whether it's **inside** `launch { }` and whether `suspend` is added.

---

# Day 2 — Handling Stop and Failure

`30 min explanation & demo → 60 min lab`

1. Make [Stop] work with `Job.cancel()`
2. Move truly blocking work to `withContext(Dispatchers.IO)`
3. Catch a `connectFake()` that fails half the time with `try/catch`, and show [Retry]

---

## Day 2 · 0–5 min — Today's Syntax: try/catch and throw

```kotlin
try {
    connectFake()
    binding.stateText.text = "Connected"
} catch (e: Exception) {
    binding.stateText.text = "Connection failed"
}
```

```kotlin
throw Exception("Connection failed")
```

- If an error occurs inside `try`, the app jumps into **`catch`** instead of crashing.
- `throw` raises an error on purpose. The text in the parentheses becomes `e.message`.
- If no error occurs, `catch` never runs.

---

## Day 2 · 5–13 min — Building [Stop] with Job

```kotlin
private var scanJob: Job? = null      // inside the class, outside onCreate()

scanJob = lifecycleScope.launch {     // inside [Scan]
    countDown()
}
```

```kotlin
binding.stopButton.setOnClickListener {
    scanJob?.cancel()
}
```

- `launch` returns the started coroutine as a **`Job`**. We keep it in a variable.
- It's `null` before [Scan] is pressed, so we call it with Week 3's `?.`.
- `cancel()` ends the coroutine right where it's paused at `delay`.

---

## Day 2 · 13–21 min — withContext(Dispatchers.IO) Is Only for Truly Blocking Work

| Task | Where | Why |
|---|---|---|
| `binding.stateText.text = …` | plain `launch { }` | Views can only change on the main thread |
| `delay(1000)` | plain `launch { }` | doesn't hold the thread, no need to move it |
| `Thread.sleep`, file reads, network calls | `withContext(Dispatchers.IO) { }` | work that **truly blocks** the main thread |

```kotlin
val ok = withContext(Dispatchers.IO) {
    Thread.sleep(2000)   // this runs on another thread
    true                 // the last line becomes the result
}
```

`withContext` returns to the main thread when it finishes. Week 5's `runOnUiThread` isn't needed here.

---

## Day 2 · 21–27 min ① — connectFake(): A Fake Connection That Fails Half the Time

```kotlin
private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
    Thread.sleep(2000)
    if (Random.nextBoolean()) {
        throw Exception("Connection failed")
    }
    true
}
```

- Takes 2 seconds, and throws an error if `Random.nextBoolean()` is `true`.
- `: Boolean` means it returns one true/false value; `fun … = …` is shorthand that returns whatever is right of `=` (instead of braces).
- In Week 12 this becomes a real BLE connection, but **the calling code stays the same.**
- For `Random`, pick **`kotlin.random.Random`** from Alt+Enter. Picking `java.util.Random` breaks the build.

---

## Day 2 · 21–27 min ② — Catching It with try/catch and Showing [Retry]

```kotlin
private suspend fun tryConnect() {
    try {
        connectFake()
        binding.stateText.text = "Connected"
        // move to the control screen with Intent, as in Week 4
    } catch (e: Exception) {
        binding.stateText.text = "Connection failed"
        Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
        binding.retryButton.visibility = View.VISIBLE
    }
}
```

- Success: `Connected` → control screen. Failure: Toast `Connection failed` + [Retry] button.
- Making it a `suspend fun` keeps `this` as `MainActivity`, so `Intent` and `Toast` both work.

---

## Day 2 · 27–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--중지와-실패-처리-60분) · [Walkthrough](walkthrough.md#2일차)

1. Keep `scanJob` and call `cancel()` in [Stop].
2. Build `connectFake()` and call it with `tryConnect()` after the countdown.
3. On failure show Toast and [Retry]; on success move to the control screen.

**Explanation total: 5+8+8+6+3 = 30 min**

If `throw` happens outside a `try`, the app simply crashes. If it crashes, check `try/catch` first.

---

## What to Submit

Submit these three items once, at the end of Day 2.

1. **`MainActivity.kt`**: final code with `countDown()`, `connectFake()`, and `tryConnect()`
2. **Screenshot 1**: the countdown stopped after pressing [Stop] (e.g. `Scanning… 3`)
3. **Screenshot 2**: the `Connection failed` Toast and the [Retry] button

---

## Next Week Preview

Try **rotating** the screen during a countdown.

What happens to the number? What disappears along with `lifecycleScope`?

In Week 7 you move coroutines and state into a **ViewModel**, which outlives the screen.
