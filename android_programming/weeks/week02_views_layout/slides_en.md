---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 2
footer: First Android App · LinearLayout and findViewById
---

# First Android App: My Info Screen and a Counter

In Week 1 you printed your student ID and name to the **console**.
This week you show them on the **app screen**, and change a number with buttons.

```text
My Info
Student ID: 20260001
Name: Hong Gildong
Major: Computer Engineering

3
[-1] [Reset] [+1]
```

---

# Day 1 — Show My Info on the App Screen

`30 min explanation & demo → 60 min lab`

1. Open the project you made in Week 1 and run it on the emulator.
2. Stack text top to bottom with LinearLayout.
3. Show student ID, name, and major with TextView.

---

## Day 1 · 0–5 min — Open Last Week's Project

You already made the `StudentCard` project in Week 1. Today you add a **screen** to it — no new project.

1. Pick `StudentCard` from the recent projects on the welcome screen.
2. Not on the list? **File › Open** → the `StudentCard` folder you made in Week 1.
3. Wait for the progress bar at the bottom (Gradle sync) to finish.
4. Pick a device and press **Run ▶** → check `Hello World!`.

No project? Make one again following the create-project step in the [Week 1 walkthrough](../week01_android_kotlin/walkthrough.md#5-새-프로젝트-만들기) (**Empty Views Activity**, Name `StudentCard`).

---

## Day 1 · 5–15 min ① — Three Folders in the Project Panel

In the left **Project** panel (with `Android` view selected at the top), expand `app` to see three folders.

| Folder | What's inside |
|---|---|
| `manifests` | The app info file `AndroidManifest.xml` — we don't open this yet |
| `kotlin+java` | Kotlin code. `MainActivity.kt` is here |
| `res` | Resources like screens and images. `layout › activity_main.xml` is here |

This week we open only **two** files: one in `kotlin+java`, one in `res`.
For the rest, just note the name and move on.

---

## Day 1 · 5–15 min ② — Two Files That Build the Screen

| File | What it does |
|---|---|
| `res/layout/activity_main.xml` | Describes **what** goes on the screen and **how** |
| `MainActivity.kt` | Describes **what to do** when the app starts |

```kotlin
setContentView(R.layout.activity_main)
```

This means "use `activity_main.xml` as this screen." On Day 1 we only edit the XML.

---

## Day 1 · 5–15 min ③ — LinearLayout Stacks Things in Order

```text
vertical                    horizontal

My Info                    [-1] [Reset] [+1]
Student ID: 20260001
Name: Hong Gildong
Major: Computer Engineering
```

- Children are placed one at a time, **in the order you add them**.
- `android:orientation`: `vertical` goes top to bottom, `horizontal` goes side to side.
- `android:gravity="center"`: centers the content inside.

---

## Day 1 · 15–25 min ① — Reading One TextView

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginTop="8dp"
    android:text="Student ID: 20260001"
    android:textSize="20sp" />
```

- `wrap_content`: sized to exactly fit the text (`match_parent` fills the parent)
- `android:text`: the text shown on screen
- Use `sp` for text size and `dp` for spacing.

---

## Day 1 · 15–25 min ② — Finishing the My Info Screen

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <!-- Four TextViews: My Info · Student ID · Name · Major -->

</LinearLayout>
```

- **Do not delete** `android:id="@+id/main"`. `MainActivity.kt` uses it.
- Copy the student ID TextView, paste it, and change only `android:text`.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--linearlayout으로-내-정보-화면-만들기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Open the `StudentCard` project and run `Hello World!`.
2. Turn `activity_main.xml` into a LinearLayout.
3. Show your own student ID, name, and major, then take a screenshot.

**Explanation total: 5+10+10+5 = 30 min**

If you get stuck, check `android:id="@+id/main"`, your quotes, and matching `/>` first.

---

# Day 2 — Change the Screen with Code

`30 min explanation & demo → 60 min lab`

1. Tag a View with `android:id`.
2. Find a View with `findViewById` and change its text.
3. Count a number up on every button press.

---

## Day 2 · 0–5 min — An id Is a View's Name Tag

```xml
<TextView
    android:id="@+id/nameText"
    android:text="Name: ?"
    ... />
```

```kotlin
R.id.nameText
```

- In XML, `@+id/nameText` tags the View.
- In Kotlin, `R.id.nameText` points to the same View.
- Even one wrong character means it won't be found.

---

## Day 2 · 5–15 min ① — A Template We Don't Need to Read Yet

```kotlin
class MainActivity : AppCompatActivity() {                  // template
    override fun onCreate(savedInstanceState: Bundle?) {    // template: runs when the app starts
        super.onCreate(savedInstanceState)                  // template
        enableEdgeToEdge()                                  // template
        setContentView(R.layout.activity_main)              // connects the layout file
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            ...                                             // template (insets block)
        }
        // ← put today's code here
    }
}
```

- **Don't delete or change** the lines the template created. You'll learn what they mean starting Week 3.
- Our spot is inside `onCreate()`, **below** the `insets` block.

---

## Day 2 · 5–15 min ② — Find and Change with findViewById

```kotlin
val name = "Hong Gildong"
val nameText = findViewById<TextView>(R.id.nameText)
nameText.text = "Name: $name"
```

| Week 1 (console) | Week 2 (app screen) |
|---|---|
| `println("Name: $name")` | `nameText.text = "Name: $name"` |

`findViewById<TextView>`: "find the **TextView** whose id is `nameText`."

---

## Day 2 · 5–15 min ③ — Code That Runs on a Button Press

```kotlin
val plusButton = findViewById<Button>(R.id.plusButton)

plusButton.setOnClickListener {
    // this code runs every time the button is pressed
}
```

- The code inside `{ }` runs **each time you press it**, not when the app starts.
- If `TextView` or `Button` turns red, press **Alt+Enter** (⌥+Enter on Mac) to import it.

---

## Day 2 · 15–25 min ① — Placing the Number and Buttons

```xml
<TextView
    android:id="@+id/countText"
    android:text="0"
    android:textSize="40sp"
    ... />

<LinearLayout android:orientation="horizontal" ...>
    <Button android:id="@+id/minusButton" android:text="-1" ... />
    <Button android:id="@+id/resetButton" android:text="Reset" ... />
    <Button android:id="@+id/plusButton" android:text="+1" ... />
</LinearLayout>
```

- Place one number TextView and a **horizontal** LinearLayout wrapping three buttons below the info.
- Paste the full XML from [Walkthrough Step 9](walkthrough.md#9-숫자와-버튼-배치하기).

---

## Day 2 · 15–25 min ② — Counting with var

```kotlin
var count = 0
val countText = findViewById<TextView>(R.id.countText)

plusButton.setOnClickListener {
    count = count + 1
    countText.text = "$count"
}
```

- The value changes on every press, so it's `var`, not `val`.
- The screen needs text, so we set `"$count"`, not `count`.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--버튼으로-숫자-세기-60분) · [Walkthrough](walkthrough.md#2일차)

1. Give the name TextView an id and change its text with code.
2. Make the `+1` button increase the number by 1.
3. Finish `-1` and `Reset` **yourself**, using the `+1` code as a guide.

**Explanation total: 5+10+10+5 = 30 min**

---

## What to Submit

Submit these three items once, at the end of Day 2.

1. **`activity_main.xml`**
2. **`MainActivity.kt`**
3. **One screenshot**: showing your student ID, name, major, and the number `3`

---

## Extension — Equal Button Widths with layout_weight

```xml
<Button
    android:id="@+id/minusButton"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:layout_weight="1"
    android:text="-1" />
```

- Change the `layout_width` of the horizontal LinearLayout wrapping the buttons to `match_parent`.
- Give all three buttons `layout_width="0dp"` + `layout_weight="1"` → the leftover width splits **1:1:1**.
- Weight decides the width, so leave `layout_width` at `0dp`.
- Optional, for students who finish early. See [If you finish early](lab.md#먼저-끝났다면) in the lab sheet.

---

## Next Week Preview

Set the number to `3`, then **rotate** the emulator screen.

What happened to the number? Why?

In Week 3 you'll learn about the **Activity lifecycle** — why the screen gets rebuilt.
