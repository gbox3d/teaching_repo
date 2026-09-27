---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 9
footer: Comparing App Components and Project 1 Presentations
---

# Comparing App Components and Project 1 Presentations

Every screen you built in weeks 2–7 was an **Activity**.
On Day 1, we look at the other components an app is made of besides Activity.
On Day 2, you present **Project 1**, built on top of what you made through week 7.

```text
Day 1: comparing components · Service demo · Fragment demo · project briefing → rehearsal
Day 2: presentations (3 min per person = 2 min demo + 1 min code Q&A)
```

---

# Day 1 — Comparing App Components and the Project Briefing

`30 min explanation & demo → 60 min Project 1 rehearsal`

1. Compare Activity, Service, BroadcastReceiver, and ContentProvider in one table.
2. Use `LogService` to confirm "a Service also runs on the main thread."
3. A demo of swapping Fragments, and a look at a Notification.
4. Project 1 grading and presentation slots.

---

## Day 1 · 0–8 min ① — The Four Components an App Is Made Of

| Component | What it is | When to use it | Screen | Example |
|---|---|---|---|---|
| Activity | One screen the user sees | Tapping and taking input | Yes | SmartIO's connection screen |
| Service | Does work with no screen | Work that must continue after you leave the screen | No | Playing music |
| BroadcastReceiver | Receives system-sent announcements | Battery/charging state changes | No | Showing battery level |
| ContentProvider | A window that exposes data to other apps | Reading contacts or photos | No | The Contacts app |

- All four are **entry points into the app** that Android itself can call directly.
- That's why they're declared in `AndroidManifest.xml` (a BroadcastReceiver can also be registered in code).

---

## Day 1 · 0–8 min ② — When We Meet Each One in This Course

| Component | This course | Our code |
|---|---|---|
| Activity | Every week, weeks 2–7 | `MainActivity`, `ControlActivity` |
| Service | **Demo today** | `LogService` |
| BroadcastReceiver | Week 10 | Receiving battery changes |
| ContentProvider | Week 11 comparison + demo | Reading contact names |

- In week 4 you saw the line `<activity android:name=".ControlActivity" …>` in the manifest.
- Today a `<service android:name=".LogService" …>` line joins it.
- Project 1 and the exams are built with Activity. Today's Service and Fragment are **look-only**.

---

## Day 1 · 8–15 min ① — Three Kinds of Service

| Kind | Who starts it | When it ends | Visible to the user? |
|---|---|---|---|
| started | A screen calls `startService(intent)` | when `stopService` is called, or it stops itself | not guaranteed |
| bound | A screen binds to it with `bindService` | when every bound screen unbinds | tied to the bound screen |
| foreground | started + shows a notification | until it stops | **a notification is always shown** |

- Today's demo is a single **started** Service. Just know the names for bound and foreground.
- A music app keeping a notification up while it plays is a foreground Service.

---

## Day 1 · 8–15 min ② — LogService: a Component with No Screen

```kotlin
class LogService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        return START_NOT_STICKY
    }
    override fun onDestroy() { … Log.d("Service", "onDestroy") }   // shortened
    override fun onBind(intent: Intent?): IBinder? { … return null }
}
```

- `onStartCommand`: called **every time** `startService` is called.
- `onDestroy`: called once, when it stops. `onBind`: today it's just a **template** returning `null`.

---

## Day 1 · 8–15 min ③ — Start/Stop and Registering It in the Manifest

```kotlin
binding.serviceStartButton.setOnClickListener {
    val intent = Intent(this, LogService::class.java)
    startService(intent)
}
```

```xml
<service
    android:name=".LogService"
    android:exported="false" />
```

- The same shape as week 4's `Intent(this, ControlActivity::class.java)` → `startActivity(intent)`.
- [Stop Service] uses the same two lines, with `stopService(intent)` in place of `startService`.
- The app still **builds** without the `<service>` line — it just doesn't start the Service when tapped.

---

## Day 1 · 8–15 min ④ — Demo: A Service Also Runs on the Main Thread

Logcat filter: `package:mine tag:Service`

| Button pressed | Screen | Logcat |
|---|---|---|
| [Start Service] | unchanged | `onStartCommand thread=main` |
| [Start Service] again | unchanged | one more `onStartCommand thread=main` |
| [Stop Service] | unchanged | `onDestroy` |

- `thread=main`: the same **main thread** you saw back in week 5.
- A Service is not "a thread running in the background." Call `Thread.sleep` inside `onStartCommand` and the screen freezes too.
- Long-running work inside a Service is still moved off to a thread or coroutine, just like weeks 5–6.

---

## Day 1 · 15–20 min ① — Fragment: A Piece of Screen Inside an Activity

```text
┌ MainActivity ────────────────────┐
│ [First piece] [Second piece]      │  ← stays in place
│ ┌ FragmentContainerView ───────┐ │
│ │  FirstFragment goes here      │ │  ← only this spot
│ │  (or SecondFragment)          │ │     gets swapped
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

- A Fragment is a piece of screen with its **own layout** (`fragment_first.xml`).
- Instead of an Activity's `setContentView`, `onCreateView` returns the fragment's screen.
- It is not declared in the manifest. This is the real thing previewed back in week 4, Day 2.

---

## Day 1 · 15–20 min ② — The Empty Slot and the Three Lines That Swap It

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/fragmentContainer"
```

```kotlin
binding.secondButton.setOnClickListener {
    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(R.id.fragmentContainer, SecondFragment())
    transaction.commit()
}
```

- Start a swap → put a fragment in the slot → **commit** it. Skip `commit()` and nothing changes.
- Demo: each tap logs `SecondFragment onCreateView` under Logcat tag `Fragment`.

---

## Day 1 · 20–24 min — Notification: Alerting Outside the Screen

```text
Pulling down the status bar shows
┌──────────────────────────────────┐
│ Smart I/O Controller             │
│ Connection lost                  │
└──────────────────────────────────┘
```

- A Notification alerts a user who isn't currently looking at the app's screen.
- A foreground Service **must** show a notification (row three of the Service table).
- Since Android 13, showing a notification requires the user's **permission**.
- Permission requests are covered on week 10, Day 2. Today you only see the shape — no code.

---

## Day 1 · 24–30 min ① — Project 1: Choose One of Two

| | (a) SmartIO simulator | (b) Free-choice app (weeks 5–7 scope) |
|---|---|---|
| Flow | device name → scan countdown → simulated connect success/failure with retry → control-screen command log | a flow you design yourself |
| Add | **one feature of your own** | call the provided `fakeRequest()` at least once, and add a **[Retry]** button |
| Starting point | your `SmartIO` project through week 7 | a new project |

Option (b) is available only in sections your instructor allows by announcement.

The scoring criteria are the same: **normal flow / failure & retry / survives rotation / code walkthrough (individual Q&A)**

Full requirements: [project brief](project_brief.md) · [rubric](rubric.md)

---

## Day 1 · 24–30 min ② — Grading and Presentation Slots

| Presentation, 5 pts | Report, 5 pts |
|---|---|
| Normal flow 1.5 · failure & retry 1 · survives rotation 1 · code walkthrough 1.5 | How to run it & file list 1 · screenshots with code locations 2 · your own feature explained 1 · a record of a bug you fixed 1 |

Each presentation is **3 minutes**. First, check whether everyone fits inside the 60-minute slot.

```text
presentation time = ceil(N / E) × 3 min ≤ 60 min     N = presenters, E = graders listening at once
e.g. N = 38, E = 2 → 19 × 3 = 57 min → fits in Day 2's 60 minutes
e.g. N = 26, E = 1 → 26 × 3 = 78 min → the first 13 present during today's 20–60 min lab instead
```

---

## Day 1 · 24–30 min ③ — Try It Yourself

[Day 1 lab](lab.md#1일차--1차-과제-리허설-60분) · [Walkthrough](walkthrough.md#1일차)

1. Check your slot on the presentation order sheet, and confirm your app shows all four scoring criteria.
2. Take a screenshot **now** of a screen showing both the failure message and [Retry].
3. Pair up and time each other running the **2-minute demo** twice.
4. Find the file and line you'll point to for the code question, and finish your report.

**Explanation total: 8+7+5+4+6 = 30 min**

If you chose (b), see the walkthrough's `fakeRequest()` step. You can also try the Service and Fragment demos again in the walkthrough (ungraded).

---

# Day 2 — Project 1 Presentations

`30 min briefing & check → 60 min presentations`

1. Today's running order.
2. The rubric, once more.
3. A preview of the code-question style.
4. Pre-presentation checklist → presentations begin.

---

## Day 2 · 0–5 min — Today's Running Order

| Step | Task | Time |
|---|---|---|
| 1 | While the person before you presents, have your app open on the first screen | while waiting |
| 2 | Demo: normal flow → failure & retry → rotation | 2 min |
| 3 | Answer one grader question, pointing to a line of code | 1 min |
| 4 | Hand off to the next person | within the 3 min |

- When 2 minutes are up, the demo stops and you move to the question. A scene you couldn't show can be covered with a report screenshot instead, but that item scores at most half credit (exceptions apply for a logged technical issue, or a failure state that never triggered).
- Where you present (front screen / your seat) and the order follow your section's announcement. Discuss any reordering with the instructor first.

---

## Day 2 · 5–12 min — The Rubric, Once More: Presentation 5 + Report 5

| Presentation item | Points | What earns full credit |
|---|---|---|
| Normal flow | 1.5 | Runs start to finish with nothing stuck. For (a), through your own feature too. |
| Failure & retry | 1 | Failure message → [Retry] → success |
| Survives rotation | 1 | Text and buttons stay correct when rotated mid-run or on a failure screen |
| Code walkthrough | 1.5 | Point to the file and line, answer in one sentence |

| Report item | Points |
|---|---|
| How to run it and file list | 1 |
| Screenshots of each scoring criterion, with code locations | 2 |
| Explanation of your own feature (for (b), where `fakeRequest()` is called) | 1 |
| A record of a bug you fixed | 1 |

---

## Day 2 · 12–20 min — What the Code Questions Look Like

| Example question | What to point to |
|---|---|
| Why does state survive rotation? | the `by viewModels()` line and `viewModelScope.launch` |
| Why doesn't the app crash on failure? | `try { … } catch (e: Exception) { … }` |
| Where does [Retry] get shown? | the `when` or `if` inside `collect { }` |
| Why does tapping [Scan] twice only start one scan? | `if (scanJob?.isActive == true) {` |
| Which line is your own feature? | the file and line you changed |

Answer in this order: **open the file → point to the line → one sentence.**

"It just works that way" earns no points. Point to a line.

---

## Day 2 · 20–27 min — Pre-Presentation Checklist

- [ ] After your last edit, you **saved and ran it again** with Run ▶
- [ ] Auto-rotate is on in the emulator's quick settings, and the rotate button actually turns the app
- [ ] The app is on its first screen (`Not connected` or `Waiting`)
- [ ] You know how many tries it takes to trigger a failure, and have a **failure screenshot** ready in case it doesn't show up live
- [ ] The file you'll use for the code question is already open in an editor tab
- [ ] You've submitted your report, or know how to

Take 7 minutes now to run through this yourself. Raise your hand if your emulator won't start.

---

## Day 2 · 27–30 min — Presentations Begin

[Day 2 lab](lab.md#2일차--1차-과제-발표-60분) · [Walkthrough](walkthrough.md#2일차)

1. The first three presenters keep their apps open and wait for their turn.
2. Once you've presented, watch the others and make sure your report was submitted.
3. Raise your hand if equipment freezes. The TA logs the time and moves you later in the order.

**Explanation total: 5+7+8+7+3 = 30 min**

---

## Next Week Preview

We build the third row of today's table ourselves: **BroadcastReceiver**.

- Changing the emulator's battery will make SmartIO's `Battery 80% · Charging` update to match.
- Using BLE in week 12 requires the user's **permission**. We build that flow on week 10, Day 2.
