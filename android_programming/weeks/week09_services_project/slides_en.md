---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 9
footer: Service: Work Without a Screen
---

# Service: Work Without a Screen

Every screen you built in weeks 2–7 was an **Activity**.
On Day 1 you add a **Service**, a component with no screen, and start and stop it yourself.
On Day 2 the Service counts once a second and your screen **receives** that number.

```text
Day 1: four components compared · three kinds of Service · starting and stopping LogService
Day 2: keeping the value in an object and a MutableStateFlow · counting in the Service · receiving it
```

---

# Day 1 — Comparing App Components and Service

`30 min explanation & demo → 60 min lab`

1. Compare Activity, Service, BroadcastReceiver, and ContentProvider in one table.
2. Read the three kinds of Service and the `LogService` code.
3. Use `startService`/`stopService` and register `<service>` in the manifest.
4. Confirm in Logcat that "a Service also runs on the main thread."

---

## Day 1 · 0–8 min ① — The Four Components an App Is Made Of

| Component | What it is | When to use it | Screen | Example |
|---|---|---|---|---|
| Activity | One screen the user sees | Tapping and taking input | Yes | SmartIO's connection screen |
| Service | Does work with no screen | Work that must continue after you leave the screen | No | Playing music |
| BroadcastReceiver | Receives system-sent announcements | Battery/charging state changes | No | Showing battery level |
| ContentProvider | A window that exposes data to other apps | Reading contacts or photos | No | The Contacts app |

- Only one of the four has a screen: Activity.
- All four are **entry points into the app** that Android itself can call directly.
- That's why they're declared in `AndroidManifest.xml` (a BroadcastReceiver can also be registered in code).

---

## Day 1 · 0–8 min ② — When We Meet Each One in This Course

| Component | This course | Our code |
|---|---|---|
| Activity | Every week, weeks 2–7 | `MainActivity`, `ControlActivity` |
| Service | **Today, Day 1** | `LogService` |
| BroadcastReceiver | Week 10 | Receiving battery changes |
| ContentProvider | Week 11 comparison + demo | Reading contact names |

- In week 4 you saw the line `<activity android:name=".ControlActivity" …>` in the manifest.
- Today a `<service android:name=".LogService" …>` line joins it.
- Today's Service is not part of the SmartIO main line. Week 10 starts again from the week 7 result.

---

## Day 1 · 8–14 min ① — Three Kinds of Service

| Kind | Who starts it | When it ends | Visible to the user? |
|---|---|---|---|
| started | A screen calls `startService(intent)` | when `stopService` is called, or it stops itself | not guaranteed |
| bound | A screen binds to it with `bindService` | when every bound screen unbinds | tied to the bound screen |
| foreground | started + shows a notification | until it stops | **a notification is always shown** |

- You build a single **started** Service today. Just know the names for bound and foreground.
- A music app keeping a notification up while it plays is a foreground Service.
- Because the user knows about it, the system does not stop a foreground Service easily.

---

## Day 1 · 8–14 min ② — LogService: a Component with No Screen

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

- You inherit from `Service()` just like week 7's `ConnViewModel : ViewModel()`. There is no layout file.
- `onStartCommand`: called **every time** `startService` is called.
- `onDestroy`: called once, when it stops. `onBind`: today it's just a **template** returning `null`.

---

## Day 1 · 14–20 min ① — Start/Stop and Registering It in the Manifest

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

## Day 1 · 14–20 min ② — Demo: A Service Also Runs on the Main Thread

Logcat filter: `package:mine tag:Service`

| Button pressed | Screen | Logcat |
|---|---|---|
| [Start Service] | unchanged | `onStartCommand thread=main` |
| [Start Service] again | unchanged | one more `onStartCommand thread=main` |
| [Stop Service] | unchanged | `onDestroy` |

- `thread=main`: the same **main thread** you saw in week 5.
- A Service is not "a thread running in the background." `Thread.sleep` in `onStartCommand` freezes the screen.
- Long work inside a Service also goes to a thread or coroutine, exactly as in weeks 5 and 6.

---

## Day 1 · 20–26 min ① — The Four Components in One Table Again

| Component | Manifest tag | Who starts it | Do we build one? |
|---|---|---|---|
| Activity | `<activity>` | the user opening the app, or `startActivity` | every week from week 2 |
| Service | `<service>` | a screen calling `startService`/`bindService` | today, Day 1 |
| BroadcastReceiver | `<receiver>` or code registration | the system, when it sends an announcement | week 10, Day 1 |
| ContentProvider | `<provider>` | another app asking for data | week 11, we only read one |

- They sit in different manifest tags, and **who calls them** differs.
- Only Activity owns a screen through `setContentView`. The other three have no screen.
- Android calls each one differently: Service through `onCreate`/`onDestroy`, BroadcastReceiver through `onReceive` once, ContentProvider through `onCreate` (the week 3 idea).

---

## Day 1 · 20–26 min ② — When to Use a Service, and When Not To

| What you want to do | What we use in this course |
|---|---|
| Waiting while the screen is visible (countdown, fake connect) | week 6 coroutines + week 7 ViewModel |
| State that must survive rotation | week 7 ViewModel and StateFlow |
| Work that continues after you leave the screen (music, a long upload) | a Service |
| Long work the user must keep seeing | a foreground Service (notification required) |

- The Service you add this week is practice. From week 10 the main SmartIO line restarts from the week 7 build.
- "Anything without a screen is a Service" is wrong. The test is **must it continue after you leave?**
- Even inside a Service, long work still moves to a thread or coroutine. Tomorrow you do exactly that.

---

## Day 1 · 26–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--smartio에-logservice-넣기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Create `LogService.kt` and write the three functions (`onStartCommand`, `onDestroy`, `onBind`).
2. Add the three `<service>` lines inside `<application>`. Miss this and your Logcat stays empty.
3. Add [Start Service] and [Stop Service] buttons that call `startService`/`stopService`.
4. Set the Logcat filter to `package:mine tag:Service`, fill in the table, and take **one screenshot**.

```text
onStartCommand thread=main   ← two lines if you tap twice
onDestroy                    ← [Stop Service]
```

**Explanation total: 8+6+6+6+4 = 30 min**

---

# Day 2 — Showing the Service's Count on the Screen

`30 min explanation & demo → 60 min lab`

1. See that the Service and the screen are different objects, so the value needs a place of its own.
2. Put week 7's `MutableStateFlow` into `object ServiceState`.
3. Count up once a second inside the Service with a coroutine.
4. Receive it on the screen with week 7's `repeatOnLifecycle` frame.

---

## Day 2 · 0–6 min ① — Day 1's Service Only Reached Logcat

| What you tapped on Day 1 | Screen | Logcat |
|---|---|---|
| [Start Service] | unchanged | `onStartCommand thread=main` |
| [Stop Service] | unchanged | `onDestroy` |

- **From the screen alone** you could not tell whether the Service was running. You had to open Logcat.
- Today the Service counts once a second, and the screen writes that number after the `Count:` label.
- As Day 1 said, long work inside a Service goes to a coroutine. Today you write that coroutine.
- You delete none of the Day 1 code: you create one new file and add to four more.

---

## Day 2 · 0–6 min ② — The Service and the Screen Are Different Objects

```text
LogService  ──▶  ServiceState.tick  ──▶  MainActivity
+1 every second   object: one per app    collects it and writes it on screen
```

| If you try this | What happens |
|---|---|
| The Service writes into a `MainActivity` property | the Service does not know that screen object |
| Getting a value back through `startService(intent)` | an Intent only goes **out**; nothing comes back |
| Keeping one place both of them can see | today's way |

- Android creates the Service and the Activity **as two separate objects**.
- So passing a value needs a place both of them know. You build that place on the next slide.

---

## Day 2 · 6–14 min ① — A Place to Keep the Value: object and MutableStateFlow

```kotlin
import kotlinx.coroutines.flow.MutableStateFlow

object ServiceState {
    val tick = MutableStateFlow(0)
}
```

- An `object` exists once per app. Week 7 Day 2's `ConnState` was an object too.
- `MutableStateFlow(0)` is week 7's **box holding one current value**, and it starts at 0.
- In week 7 you hid the writing side (`_state`) and exposed only the reading side (`state`).
- Today the side that raises the value is `LogService`, **outside** this file, so one line stays open.
- Wrap it in a `StateFlow` as in week 7 and `LogService.kt` reports `'val' cannot be reassigned.`

---

## Day 2 · 6–14 min ② — The Service Counts Every Second with a Coroutine

```kotlin
    private val scope = CoroutineScope(Dispatchers.Default)
    private var tickJob: Job? = null
```

```kotlin
        tickJob = scope.launch {
            while (isActive) {
                delay(1000)
                ServiceState.tick.value++
            }
        }
```

- A Service has nothing like week 7's `viewModelScope`, so you **make the coroutine's place yourself**. `Dispatchers.Default` is not the main thread.
- `delay(1000)` is the week 6 function. `while (isActive)` repeats resting one second and raising the value by 1.
- Tapping [Start Service] again must not start a second coroutine, so `if (tickJob?.isActive == true)` returns right away while it counts.

---

## Day 2 · 14–22 min ① — Receiving on the Screen: repeatOnLifecycle

```kotlin
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                ServiceState.tick.collect { tick ->
                    binding.serviceTickText.text = "Count: $tick"
                }
            }
        }
```

- The week 7 Day 2 frame, unchanged; **only what you receive** moves from `viewModel.state` to `ServiceState.tick`.
- Put it inside `onCreate()`, after block 11. Add no imports at all to `MainActivity.kt`.
- You receive only while the screen is visible (`STARTED`): not while you are on the control screen.
- The number goes into `serviceTickText` in `activity_main.xml`, and its first text sits in `strings.xml`.

---

## Day 2 · 14–22 min ② — Demo: The Count Continues After Switching Screens

| Action | What to look for on screen |
|---|---|
| [Start Service] | the number after `Count:` should change about once a second |
| [Start Service] again | the number should carry on; no second coroutine starts |
| type a name, [Connect] → control screen → [Back] | the number on return should be larger than when you left |
| Rotate the screen | the last value should appear again (the week 7 restore frame) |
| [Stop Service] | `onDestroy` puts it back to 0, so `Count: 0` should appear |

- While you are on the control screen the screen stops receiving, but the Service keeps counting. On return it takes the last value at once.
- Work continuing after you leave the screen is the reason to use a Service. The Day 1 test becomes visible here.
- Drop `tickJob?.cancel()` from `onDestroy` and it still builds. See for yourself in the lab what follows.

---

## Day 2 · 22–27 min — Notification: Telling the User Off-Screen

```text
Pull down the status bar and you see
┌──────────────────────────────────┐
│ Smart I/O Controller             │
│ The connection was lost          │
└──────────────────────────────────┘
```

- A notification tells a user who is not looking at your app's screen.
- Row three of Day 1's Service table: a foreground Service **must** show a notification.
- From Android 13 on, posting a notification needs the user's **permission**.
- Without the permission, calling `notify` posts nothing. Check with `areNotificationsEnabled()` and Logcat.
- Runtime permissions are week 10 Day 2, so today this is **a demo only, not part of the lab**.

---

## Day 2 · 27–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--service가-센-숫자를-화면에-보여-주기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Create `ServiceState.kt` as an **Object** with the single line `val tick = MutableStateFlow(0)`.
2. Add `scope` and `tickJob` to `LogService.kt` and raise `ServiceState.tick` once a second.
3. In `onDestroy`, cancel the counting coroutine and put the value back to 0.
4. Add the `serviceTickText` spot to `activity_main.xml` and its first text to `strings.xml`.
5. Write one more week 7 collect frame in `MainActivity.kt`, then take **two screenshots**.

```text
Count: 0  →  after [Start Service], a number that is not 0
            →  after leaving for the control screen and back, a larger number
```

**Explanation total: 6+8+8+5+3 = 30 min**

---

## What to Submit

Take one screenshot on Day 1 and two on Day 2.

1. **Day 1, one screenshot**: Logcat filtered by `tag:Service`, showing two `onStartCommand thread=main` lines and one `onDestroy` line
2. **Day 2, two screenshots**: ① the number after `Count:` is not 0 ② the number carried on after a trip to the control screen and back

Follow the class announcement for file names, where to submit, and the deadline. Check that no personal information shows in the screenshots.

---

## Next Week Preview

You build row three of Day 1's table, a **BroadcastReceiver**, and ask for a **runtime permission**.

- Change the battery in the emulator and make SmartIO's `배터리 80% · 충전 중` follow it.
- Like today's notification permission, week 10 Day 2 asks the user right before the app needs it.
- In week 12, **BLE** (Bluetooth Low Energy) reports the board's state through the collect frame you wrote today.
- Week 10 starts from the week 7 result. The Service you added today ends with week 9.
