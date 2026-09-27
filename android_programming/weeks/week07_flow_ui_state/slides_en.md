---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 7
footer: ViewModel and StateFlow · State That Survives Rotation
---

# ViewModel and StateFlow: State That Survives Rotation

In week 6, the countdown disappeared the moment you **rotated** the screen.
This week we put state somewhere that outlives the screen, and the screen **collects** that state to show it.

```text
Connecting… 3    ──rotate──▶    Connecting… 3 → 2 → 1
[Scan] [Stop] [Disconnect]      [Scan] [Stop] [Disconnect]
```

---

# Day 1 — Moving Coroutines and State into a ViewModel

`30 min explanation & demo → 60 min lab`

1. Read up on `class` and properties.
2. See what disappears when you rotate the screen.
3. Move the coroutine into `ConnViewModel` and get it with `by viewModels()`.

---

## Day 1 · 0–5 min — Today's Syntax: class and Properties

```kotlin
class Counter {
    var count = 0                      // property: a value the object holds
    fun plus() { count = count + 1 }   // function: something the object does
}

fun main() {
    val a = Counter()                  // build one object from the class (the blueprint)
    a.plus()
    println(a.count)                   // 1
}
```

- A `class` is a blueprint; `Counter()` is an **object** built from that blueprint.
- Use a dot (`.`) to reach a value or function inside an object. `binding.stateText.text` has the same shape.
- The `ConnViewModel` we build today is also just a class.

---

## Day 1 · 5–15 min ① — A Countdown That Disappears on Rotation

Demo: in your finished week 6 app, tap [Scan] → rotate while it shows `Scanning… 3`.

```text
Before rotation          After rotation
Scanning… 3              Waiting
[Scan] [Stop]            [Scan] [Stop]
                         (the number is gone, and no connection is attempted)
```

- Week 3: rotating triggers `onDestroy` → `onCreate`. **The Activity is re-created.**
- The week 6 coroutine running in `lifecycleScope` is cancelled along with the old screen.
- `onSaveInstanceState` keeps a single number, but it cannot resume **a coroutine that was already running**.

---

## Day 1 · 5–15 min ② — A ViewModel That Outlives the Screen

```text
Screen A (portrait) ── onDestroy ─┐   Screen B (landscape) ── onCreate ── …
                                   │
ConnViewModel ═════════════════════╪═══════════════════════ (stays alive)
  scanJob: Scanning… 3 → 2 → 1 → Connecting… → Connected
```

- A **ViewModel** survives rotation and hands the new screen **the same object** back.
- It is cleared only when the app is closed with the back gesture (◁).
- So we move the countdown coroutine and the last message into the **ViewModel**.
- The ViewModel doesn't know about the screen (`binding`). It only holds the message; putting it on screen is the Activity's job.

---

## Day 1 · 15–25 min ① — ConnViewModel and viewModelScope

```kotlin
class ConnViewModel : ViewModel() {
    private var scanJob: Job? = null        // variable moved over from week 6's MainActivity

    fun startScan() {
        scanJob = viewModelScope.launch {   // viewModelScope instead of lifecycleScope
            for (i in 5 downTo 1) {
                show("Scanning… $i")         // show(…) instead of a binding line
                delay(1000)
            }
            tryConnect()
        }
    }
}
```

- `viewModelScope` is a coroutine scope **tied to the ViewModel**. It keeps running even when the screen is re-created.

---

## Day 1 · 15–25 min ② — Getting It with by viewModels()

```kotlin
// Inside the MainActivity class, below binding
private val viewModel: ConnViewModel by viewModels()
```

```kotlin
binding.scanButton.setOnClickListener {
    // the four button/ProgressBar lines stay the same as week 6
    viewModel.startScan()
}
```

- Don't create it **directly** with `ConnViewModel()`. That would create a new object every time you rotate.
- `by viewModels()` returns **the existing** ViewModel for this screen, if there is one.
- `viewModelScope` is only available inside a class that extends `: ViewModel()`.
- If `viewModels` shows up in red, press Alt+Enter (⌥+Enter on Mac) → `androidx.activity.viewModels`.

---

## Day 1 · 15–25 min ③ — Notifying the Screen, and Reading It Back After Rotation

```kotlin
// ConnViewModel: keep the last message, and notify a registered screen if any
private fun show(text: String) {
    resultText = text
    listener?.invoke(text)
}
```

```kotlin
// MainActivity onCreate: register, then read back the remaining message
viewModel.listener = { text -> showState(text) }
binding.stateText.text = viewModel.resultText
// onDestroy: viewModel.listener = null
```

- `showState(text)` is a `MainActivity` function that holds the text/button/Intent/Toast lines that used to sit inside week 6's `tryConnect()`.
- `listener` is a variable (a slot) that holds "code that takes one piece of text"; it's `null` when empty. On rotation, the old screen clears it in `onDestroy`, and the new screen registers it again in `onCreate`.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--viewmodel로-옮기기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Rotate your week 6 project to confirm the problem.
2. Create `ConnViewModel.kt` and move the countdown, `connectFake()`, and `tryConnect()` into it.
3. Get it with `by viewModels()`, and add register/unregister/read-back.
4. Rotate the screen and note in your observation table **what survives** and **what doesn't**.

**Explanation total: 5+10+10+5 = 30 min**

Today only the text carries over; the button and ProgressBar reset to their starting look. We fix that tomorrow.

---

# Day 2 — Collecting State with StateFlow

`30 min explanation & demo → 60 min lab`

1. The `object ConnState` constant group and `when`.
2. Store state with `MutableStateFlow`/`StateFlow`.
3. Collect inside the standard block and update text and buttons together.

---

## Day 2 · 0–5 min — Today's Syntax: object Constant Groups and when

```kotlin
object ConnState {
    const val CONNECTING = "Connecting"
    const val READY = "Ready"
    // five in total, also DISCONNECTED, DISCOVERING, LOST
}
```

```kotlin
when (state) {
    ConnState.CONNECTING -> { binding.stopButton.isEnabled = true }
    ConnState.READY -> { binding.disconnectButton.isEnabled = true }
}
```

- `object` is a single group you call directly by name; `const val` is a constant that never changes. Get a name wrong and it shows up as a **build error**.
- `when (state)` runs only the one branch whose value matches. It's a shorter way to write `if … else if …`.

---

## Day 2 · 5–13 min — MutableStateFlow and StateFlow

```kotlin
// Inside ConnViewModel
private val _state = MutableStateFlow(ConnState.DISCONNECTED)   // writable side: private only
val state: StateFlow<String> = _state                           // readable side: exposed to the screen

fun disconnect() {
    _state.value = ConnState.DISCONNECTED    // change the value only inside a ViewModel function
}
```

- A `StateFlow` is a box that always holds **exactly one current value**. When the value changes, it notifies whoever is collecting it.
- `<String>` marks the value inside the box as text.
- This one box now does both jobs from Day 1: `resultText` (storing) and `listener` (notifying).
- Trying to change it from the screen with `viewModel.state.value = …` gives `'val' cannot be reassigned.`

---

## Day 2 · 13–23 min ① — The Standard Block: Collect Only While Visible

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            binding.stateText.text = state   // ← you only fill in inside these braces
        }
    }
}
```

| Line | Meaning |
|---|---|
| `lifecycleScope.launch` | Starts a coroutine, as in week 6. Needed because `collect` is a suspend function too. |
| `repeatOnLifecycle(STARTED)` | Starts the block when the screen is visible, stops it when it isn't, and starts it again when it reappears. |
| `collect { state -> }` | Runs the code inside the braces every time the state changes. |

---

## Day 2 · 13–23 min ② — Collecting Starts from the Last Value

```text
[Scan]        ─▶ _state = Connecting,  _seconds = 5, 4, 3 …
Rotate        ─▶ old screen onStop: collecting stops → onDestroy
                 new screen appears: collecting restarts → immediately "Connecting" + 3
Home → back   ─▶ the same way, the last value is collected again
```

- This block replaces the register (onCreate), unregister (onDestroy), and read-back you did **by hand** on Day 1.
- With two values to collect (`state`, `seconds`), write the block **twice**. Put the `seconds` block **below** the `state` block.
- Calling `collect` directly in `onCreate` without the block is a build error. Put it inside the block instead:
  `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.`
  (You'll see `<Int>` when collecting `seconds`, and `<String>` when collecting `state`.)

---

## Day 2 · 23–27 min — Buttons per State: Turn Everything Off First, Then Turn On Only What's Needed

```kotlin
binding.scanButton.isEnabled = false
binding.stopButton.isEnabled = false
binding.disconnectButton.isEnabled = false
binding.retryButton.visibility = View.GONE
binding.scanProgress.visibility = View.GONE
when (state) {
    ConnState.READY -> {
        binding.disconnectButton.isEnabled = true
    }
    // DISCONNECTED, CONNECTING, DISCOVERING, and LOST follow the same pattern
}
```

- Turning everything off first means a button enabled by the previous state never **lingers**.
- [Connect] stays enabled at all times, as in week 4. Don't put `startActivity` or a Toast inside `collect` (it would run again on every re-collect).

---

## Day 2 · 27–30 min ① — Project 1 Preview

- **Week 9, Day 2 presentation**: presentation 5 + report 5
- Topic: SmartIO simulator —
  device name → scan countdown → simulated connect success/failure with retry → control-screen command log + **one feature of your own**
- Scoring criteria: normal flow / failure & retry / **survives rotation** / code walkthrough (individual Q&A)
- This week's screen is the skeleton of the project. Full instructions and how to submit will come with the week 9 materials and class announcements.

---

## Day 2 · 27–30 min ② — Try It Yourself

[Day 2 lab](lab.md#2일차--stateflow로-상태-받기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Create `ConnState.kt` and a [Disconnect] button.
2. Replace `ConnViewModel`'s `resultText`/`listener` with `_state`/`_seconds`.
3. Add the two blocks to `MainActivity` and fill in each `collect { }`.
4. Take screenshots: a landscape screen rotated while showing `Connecting… 3`, and a `Ready` screen with only [Disconnect] enabled.

**Explanation total: 5+8+10+4+3 = 30 min**

---

## What to Submit

Submit once, at the end of Day 2.

1. **`ConnState.kt`, `ConnViewModel.kt`, `MainActivity.kt`**
2. **Screenshot 1**: landscape screen rotated while showing `Connecting… 3` (only [Stop] enabled, ProgressBar visible)
3. **Screenshot 2**: `Ready` screen. Of the row [Scan] / [Stop] / [Disconnect], **only [Disconnect]** is enabled.

---

## Next Week Preview

Week 8 is the **midterm (individual hands-on exam)**. It covers weeks 2–7.

Day 1 rehearsal: on a similar screen, [Start] → a 5-second countdown → a completion message, [Cancel] to stop, and **state that survives rotation (ViewModel + StateFlow)**.

Try writing this week's two blocks and the `when` again, without looking at the example.
