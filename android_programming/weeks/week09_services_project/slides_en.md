---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 9
footer: Comparing App Components · Service and Fragment
---

# App Components Compared: Service and Fragment

Every screen you built in weeks 2–7 was an **Activity**.
On Day 1 you add a **Service**, a component with no screen, and start and stop it yourself.
On Day 2 you build **Fragments** and swap one slot of the screen.

```text
Day 1: four components compared · three kinds of Service · starting and stopping LogService
Day 2: swapping Fragments · Notification demo and preview
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

- SmartIO never uses a Service, all semester: it connects only while you are looking at the screen.
- "Anything without a screen is a Service" is wrong. The test is **must it continue after you leave?**
- Even inside a Service, long work still moves to a thread or coroutine.

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

# Day 2 — Swapping Fragments

`30 min explanation & demo → 60 min lab`

1. See that a Fragment is a piece of a screen inside an Activity.
2. Make an empty slot with `FragmentContainerView`.
3. Return the fragment's own view from `onCreateView`.
4. Swap pieces with the three lines `beginTransaction()` → `replace()` → `commit()`.

---

## Day 2 · 0–6 min ① — Fragment: a Piece of a Screen Inside an Activity

```text
┌ MainActivity ────────────────────┐
│ [First piece] [Second piece]     │  ← stays put
│ ┌ FragmentContainerView ───────┐ │
│ │  This is FirstFragment        │ │  ← only this slot
│ │  (or SecondFragment)          │ │     gets swapped
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

- A Fragment is a piece of a screen with **its own layout** (`fragment_first.xml`).
- The button row belongs to the Activity, so it stays; only the piece in the slot changes.
- Week 4 Day 2 promised "a piece of a screen inside an Activity." Today you build it.

---

## Day 2 · 0–6 min ② — What Activity and Fragment Each Do

| | Activity | Fragment |
|---|---|---|
| Manifest | declared with `<activity>` | not declared |
| Choosing the view | `setContentView` in `onCreate` | `onCreateView` returns a View |
| Can it stand alone? | yes, it is an entry point | no, it must be put inside an Activity |
| How you change it | `startActivity` for a new screen | `replace` for just that slot |

- Today's app has **one** Activity and **two** pieces.
- A whole new screen is an Activity; swapping one slot is a Fragment.
- SmartIO keeps its two Activities all semester, so today's practice uses a new project.

---

## Day 2 · 6–14 min ① — The Empty Slot: FragmentContainerView

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/fragmentContainer"
    android:layout_width="match_parent"
    android:layout_height="0dp"
    android:layout_weight="1" />
```

- This is the **empty slot** a piece goes into. At first it holds nothing.
- `layout_height="0dp"` + `layout_weight="1"`: it takes all the height left under the button row (week 2).
- The code calls this `id` as `R.id.fragmentContainer`. A typo shows up as an error in Kotlin.
- Run it with only the slot in place and you see the button row with nothing under it.

---

## Day 2 · 6–14 min ② — The Fragment Class and onCreateView

```kotlin
class FirstFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "FirstFragment onCreateView")
        return inflater.inflate(R.layout.fragment_first, container, false)
    }
}
```

- `inflater.inflate(…)` turns the layout file into a View and returns it. That is the `setContentView` spot.
- The import is `androidx.fragment.app.Fragment`. Do not pick `android.app.Fragment` (the old one).
- `SecondFragment` differs from this only in the layout name and the log text.

---

## Day 2 · 14–22 min ① — The Three Lines That Swap a Piece

```kotlin
binding.secondButton.setOnClickListener {
    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(R.id.fragmentContainer, SecondFragment())
    transaction.commit()
}
```

```kotlin
if (savedInstanceState == null) {
    … put FirstFragment() in with the same three lines
}
```

- Begin → put the piece in the slot → **commit**. Without `commit()` nothing changes.
- The first insertion goes inside `if (savedInstanceState == null)`.
- After a rotation the system restores the piece you were looking at (week 3), so you do not insert it again.

---

## Day 2 · 14–22 min ② — Demo: Only the Piece Changes

Logcat filter: `package:mine tag:Fragment`

| Action | Screen | Logcat |
|---|---|---|
| App starts | button row + `This is FirstFragment` | `FirstFragment onCreateView` |
| [Second piece] | button row unchanged, text becomes `This is SecondFragment` | `SecondFragment onCreateView` |
| The same button twice | the text is the same | one line each time you tap |
| Rotate after swapping | the piece you were on stays | one line for that piece |

- Tapping the same button twice builds a new piece and inserts it, so two lines appear.
- Back closes the app instead of returning to the previous piece. A back stack for pieces must be added on purpose.

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
- Runtime permissions are week 10 Day 2, so today this is **a demo only, not part of the lab**.

---

## Day 2 · 27–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--fragment-바꿔-끼우기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Create a new project `FragmentDemo` (package `com.example.fragmentdemo`). Keep it apart from SmartIO.
2. Add two buttons and a `FragmentContainerView` slot, then create the two fragment layouts.
3. Write `FirstFragment` and `SecondFragment`, each returning its own layout from `onCreateView`.
4. Add the first insertion and the three swap lines for both buttons, then take **two screenshots**.

```text
This is FirstFragment      →   This is SecondFragment
```

**Explanation total: 6+8+8+5+3 = 30 min**

---

## What to Submit

Take one screenshot on Day 1 and two on Day 2.

1. **Day 1, one screenshot**: Logcat filtered by `tag:Service`, showing two `onStartCommand thread=main` lines and one `onDestroy` line
2. **Day 2, two screenshots**: the `This is FirstFragment` screen and the `This is SecondFragment` screen (the button row must stay in the same place)

Follow the class announcement for file names, where to submit, and the deadline. Check that no personal information shows in the screenshots.

---

## Next Week Preview

You build row three of Day 1's table, a **BroadcastReceiver**, yourself.

- Change the battery in the emulator and make SmartIO's `Battery 80% · Charging` follow it.
- Using BLE in week 12 needs the user's **permission**. You build that flow in week 10 Day 2.
- The notification permission you saw today is the same kind of runtime permission. Week 10 starts from the week 7 result.
