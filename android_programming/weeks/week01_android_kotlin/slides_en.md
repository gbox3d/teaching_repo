---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 1
footer: Kotlin Basics Practice
---

# First Steps in Kotlin: Print Your Student ID and Name

This week's goal is to **print your student ID, your name, and one pass/fail line**.

```text
Student ID: 20260001
Name: Hong Gildong
Result: Pass
```

The ID and name above are examples for practice.

---

# Day 1 — Type Text and Run It

`30 min explanation & demo → 60 min lab`

1. See what this course builds over 15 weeks.
2. Open Kotlin Playground in your browser.
3. Print text with `println`.
4. Replace the example with your student ID and name.

---

## Day 1 · 0–5 min ① — Course Overview: 15 Weeks

| Week | What we do |
|---|---|
| 1 | First steps in Kotlin — print text in the browser |
| 2–3 | First app `StudentCard` — my info screen, buttons, screen rotation |
| 4–7 | `Smart I/O Controller` screens — input fields, a second screen, an app that keeps responding while waiting |
| 8 | Midterm (hands-on) |
| 9 | Project 1 presentations |
| 10–11 | Battery display, permission requests, lists, saving |
| 12–14 | Turn on board LEDs and read temperature/humidity over Bluetooth, Project 2 presentations |
| 15 | Final exam (hands-on) |

Every week ends with a **screenshot of a screen you built**.

---

## Day 1 · 0–5 min ② — Course Overview: The App We Build

```text
[Phone app: Smart I/O Controller]          [Board: ESP32]
Status: Ready                              4 LEDs, temp/humidity sensor
[Scan] [Connect] [Disconnect]  Bluetooth
LED 0 [ON]   LED 1 [OFF]       <------>    an LED turns on
Temp 24.5  Humidity 40.0                   sensor values are sent back
Log: on 0 -> {"result":"ok"}
```

- Press a button in the phone app and an **LED on the board turns on**; sensor values **appear** in the app.
- You finish and present this app in week 14. The board itself is shown in class.
- Today we take the first step: **printing one line of text**.

---

## Day 1 · 0–5 min ③ — Course Overview: Grading

| Item | Weight | Based on |
|---|---|---|
| Weekly labs | 20% | The **screenshot** you submit at the end of each lab (weeks 1–7, 10–13) |
| Midterm | 20% | Week 8, hands-on at the computer |
| Project 1 | 10% | Week 9 presentation |
| Project 2 | 20% | Week 14 presentation (app connected to the board) |
| Final exam | 20% | Week 15 hands-on + demo |

The remaining share follows the syllabus.
Each week's screenshot counts directly, so **submit each week's work in that week.**

---

## Day 1 · 5–10 min — Open the Playground

Open [Kotlin Playground](https://play.kotlinlang.org/) in your browser.

1. Type the code shown by your instructor in the code editor.
2. Press **Run (▶)**.
3. Check the text in the output area.

After editing the text, **press Run again** to update the output.
Use the lab PCs. A TA checks personal-laptop installs at the end of the Day 2 lab.

---

## Day 1 · 10–20 min ① — Starting Code and First Output

Type this code and run it.

```kotlin
fun main() {
    println("Hello")
}
```

- `fun main()` is where the program starts. Use this starting code for now.
- Write the code to run between `{` and `}`.
- `println(...)` prints what is inside the parentheses, then starts a new line.

---

## Day 1 · 10–20 min ② — Put Text in Double Quotes

```kotlin
fun main() {
    println("Hello")
    println("Nice to meet you")
}
```

```text
Hello
Nice to meet you
```

Put text inside `" "`. Match each opening parenthesis and quote with a closing one.
A missing closing quote gives the error `Expecting '"'.`

---

## Day 1 · 20–27 min — Use Your Student ID and Name

```kotlin
fun main() {
    println("Student ID: 20260001")
    println("Name: Hong Gildong")
}
```

1. Replace `20260001` with your student ID.
2. Replace `Hong Gildong` with your name.
3. Run the code and check that both lines appear.

Start by changing **only the text inside the double quotes**.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--글자-두-줄-출력하기-60분) · [Walkthrough](walkthrough.md#1일차)

**Explanation total: 5+5+10+7+3 = 30 min**

Take your time during the following 60-minute lab.

1. Run the example code.
2. Change it to your student ID and name, then run it again.
3. Save your code as `Hello.kt`.

If you get stuck, check for missing quotes, parentheses, or braces together.

---

# Day 2 — Add Some Kotlin Basics

`30 min explanation & demo → 60 min lab`

Today's result is **student ID and name on two lines + one pass/fail line**.

- `val`: give a value a name
- `String` and `Int`: distinguish text from whole numbers
- `$`: put a stored value into a sentence
- `var`: a variable that can be assigned a new value later
- `if/else`: choose a value depending on a condition
- `fun`: give a piece of work a name and call it

---

## Day 2 · 0–5 min — Give Values Names with val

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "Hong Gildong"

    println(studentId)
    println(name)
}
```

Use `val name = value` to store a value. `=` assigns the value on its right.

`println(name)` prints the value stored in `name`: `Hong Gildong`.

---

## Day 2 · 5–13 min ① — Text and Whole Numbers

```kotlin
val studentId = "20260001"  // String: text
val score = 85              // Int: a whole number
```

- Text inside double quotes is a **string (`String`)**.
- `85` is a **whole number**. Its type is `Int`.
- Kotlin infers the type from the value; you can omit the type here.
- A student ID identifies a person. Store it as text, inside double quotes.

Text after `//` is a **comment**. It is not executed.

---

## Day 2 · 5–13 min ② — Put Values into Text with $

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "Hong Gildong"

    println("Student ID: $studentId")
    println("Name: $name")
}
```

Inside double quotes, `$name` inserts the value stored in `name`.

This is a **string template**. Without `$`, the word `name` itself is printed.

---

## Day 2 · 13–18 min — val and var

```kotlin
fun main() {
    var greeting = "Hello"
    println(greeting)
    greeting = "Nice to meet you"
    println(greeting)
}
```

- `val`: you cannot assign a different value after its initial assignment.
  Doing so gives the error `'val' cannot be reassigned.`
- `var`: you can assign a new value, as in `greeting = "Nice to meet you"`.

You can still edit the name in `val name = "Hong Gildong"` and **run it again**.

---

## Day 2 · 18–23 min — if/else: A Value That Depends on a Condition

```kotlin
val score = 85
val result = if (score >= 60) "Pass" else "Fail"
println("Result: $result")
```

```text
Result: Pass
```

- `if (condition) value1 else value2`: `value1` if the condition holds, otherwise `value2`.
- `score >= 60` is the condition "is score 60 or more?".
- Change `score` to `50` and run: you get `Result: Fail`.
- Leaving out `else` is an error. Write both branches.

---

## Day 2 · 23–27 min — fun: Name a Piece of Work and Call It

```kotlin
fun intro(name: String) {
    println("Name: $name")
}

fun main() {
    intro("Hong Gildong")
    intro("Kim Cheolsu")
}
```

- `fun intro(name: String) { ... }` **defines** a function called `intro`. Write it outside `main`.
- `name: String` means "take one piece of text and call it `name`".
- **Calling** `intro("Hong Gildong")` runs the code inside `{ }`.
- `main` is also a function. When you press Run, `main` is called first.

---

## Day 2 · 27–30 min — Today's Finished Code and Lab Handoff

[Day 2 lab](lab.md#2일차--변수와-if-fun으로-자기소개-완성하기-60분) · [Walkthrough](walkthrough.md#2일차) · **Explanation total: 5+8+5+5+4+3 = 30 min**

```kotlin
fun intro(name: String) {
    println("Name: $name")
}

fun main() {
    val studentId = "20260001"
    val name = "Hong Gildong"
    val score = 85

    println("Student ID: $studentId")
    intro(name)

    val result = if (score >= 60) "Pass" else "Fail"
    println("Result: $result")
}
```

---

## What to Submit

Submit these two items once, at the end of Day 2.

1. **Your finished Kotlin code, `StudentCard.kt`**
2. **One screenshot showing the three printed lines: ID, name, result**

```text
Student ID: 20260001
Name: Hong Gildong
Result: Pass
```

Check that your student ID and name are correct, and you are done.

---

## Next Week Preview

Next week you build your **first app** in Android Studio.
The same ID and name go on the **phone screen** instead of the console.

- Android Studio is installed on the lab PCs.
- To install it on your own laptop, have a TA check it in the last 15 minutes of today's lab.

`println("Name: $name")` becomes `nameText.text = "Name: $name"` next week.
