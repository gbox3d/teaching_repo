---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 1
footer: Kotlin Basics Practice
---

# First Steps in Kotlin: Print Your Student ID and Name

This week's goal is to **print your student ID and name on two lines**.

```text
Student ID: 20260001
Name: Hong Gildong
```

The ID and name above are examples for practice.

---

# Day 1 — Type Text and Run It

`30 min explanation & demo → 60 min lab`

1. Open Kotlin Playground in your browser.
2. Print text with `println`.
3. Replace the example with your student ID and name.

---

## Day 1 · 0–5 min — Open the Playground

Open [Kotlin Playground](https://play.kotlinlang.org/) in your browser.

1. Type the code shown by your instructor in the code editor.
2. Press **Run (▶)**.
3. Check the text in the output area.

After editing the text, **press Run again** to update the output.

---

## Day 1 · 5–15 min ① — Starting Code and First Output

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

## Day 1 · 5–15 min ② — Put Text in Double Quotes

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

---

## Day 1 · 15–25 min — Use Your Student ID and Name

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

## Day 1 · 25–30 min — Try It Yourself

**Explanation total: 5+10+10+5 = 30 min**

Take your time during the following 60-minute lab.

1. Run the example code.
2. Change it to your student ID and name, then run it again.
3. Save your code and output.

If you get stuck, check for missing quotes, parentheses, or braces together.

---

# Day 2 — Add Some Kotlin Basics

`30 min explanation & demo → 60 min lab`

Today's result is still **two lines: your student ID and name**.

- `val`: give a value a name
- `String` and `Int`: distinguish text from whole numbers
- `$`: put a stored value into a sentence
- `var`: a variable that can be assigned a new value later

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

## Day 2 · 5–15 min ① — Text and Whole Numbers

```kotlin
val studentId = "20260001"  // String: text
val age = 20                // Int: a whole number
```

- Text inside double quotes is a **string (`String`)**.
- `20` is a **whole number**. Its type in this example is `Int`.
- Kotlin infers the type from the value; you can omit the type here.
- A student ID identifies a person. Store it as text, inside double quotes.

Text after `//` is a **comment**. It is not executed.

---

## Day 2 · 5–15 min ② — Put Values into Text with $

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "Hong Gildong"

    println("Student ID: $studentId")
    println("Name: $name")
}
```

Inside double quotes, `$name` inserts the value stored in `name`.

This is a **string template**. Replace the example values with your own details.

---

## Day 2 · 15–25 min — val and var

```kotlin
fun main() {
    var greeting = "Hello"
    println(greeting)
    greeting = "Nice to meet you"
    println(greeting)
}
```

- `val`: you cannot assign a different value after its initial assignment.
- `var`: you can assign a new value, as in `greeting = "Nice to meet you"`.

You can still edit the name in `val name = "Hong Gildong"` and **run it again**.

---

## Day 2 · 25–30 min — Today's Finished Code

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "Hong Gildong"

    println("Student ID: $studentId")
    println("Name: $name")
}
```

**Explanation total: 5+10+10+5 = 30 min**

Enter your student ID and name, then run the code to meet this week's goal.

---

## Day 2 Lab — Practice at Your Own Pace · 60 min

1. Type the finished code and run it.
2. Set `studentId` and `name` to your own details.
3. Check the printed ID and name, then save your code.

If time remains, change a greeting with `var`.
Or add these lines inside `main`'s `{ }` and compare their output.

```kotlin
println(1 + 2)       // 3
println("1 + 2")     // 1 + 2
```

Extra practice is optional. Only the student ID and name are required output.

---

## What to Submit

Submit these two items once, at the end of Day 2.

1. **Your finished Kotlin code, `StudentCard.kt`**
2. **One screenshot showing the printed student ID and name**

```text
Student ID: 20260001
Name: Hong Gildong
```

Check that your student ID and name are correct, and you are done.
