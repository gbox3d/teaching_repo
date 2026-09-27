---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 11
footer: Lists and Storage · ListView, SharedPreferences, ContentProvider
---

# Lists and Storage: ListView, SharedPreferences, ContentProvider

In week 10 you received battery broadcasts and requested BLE permission.
This week you add a **list of device names** to the connection screen, and **save** the last device you connected to.

```text
Devices found            Smart I/O Controller
ESP32_BLE_A              Last device: ESP32_BLE_B
ESP32_BLE_B
ESP32_BLE_C
```

---

# Day 1 — Building the Scan List

`30 min explanation & demo → 60 min lab`

1. Build a list with `mutableListOf` and grow it with `add`.
2. Attach an `ArrayAdapter` to a `ListView`, and call `notifyDataSetChanged()` after every change.
3. Pull the tapped row's name out with `setOnItemClickListener`.

---

## Day 1 · 0–5 min — Today's Syntax: mutableListOf, add, size

```kotlin
val devices = mutableListOf<String>()   // an empty list holding text
devices.add("ESP32_BLE_A")
devices.add("ESP32_BLE_B")
val count = devices.size
println("Device count: $count")          // Device count: 2
```

- `mutableListOf`: a list you can grow and clear. `<String>` marks it as "text only."
- `add` appends one item, `clear()` empties it, `size` is the count.
- Careful: `"$count devices"` written as `"장치 $count개"` in Korean is a build error there, because Kotlin reads Hangul right after `$count` as part of the variable name (`count개`). In English this particular trap doesn't occur, but the lesson is the same: don't let extra characters run directly into a `$variable`.

---

## Day 1 · 5–15 min ① — The Adapter Between the List and the ListView

```text
devices (list)          ArrayAdapter                       ListView (screen)
[A, B, C]    ──▶   "how many rows? what's row 0?"   ──▶    ESP32_BLE_A
                    one-row layout simple_list_item_1        ESP32_BLE_B
                                                              ESP32_BLE_C
```

- A **ListView** is a View that stacks rows vertically. It has no text of its own.
- An **adapter** turns each item in the list into a row View and hands it to the ListView.
- The list (data) and the screen are kept separate, and the adapter connects them.

---

## Day 1 · 5–15 min ② — Placing a ListView in XML

```xml
<ListView
    android:id="@+id/deviceList"
    android:layout_width="240dp"
    android:layout_height="0dp"
    android:layout_weight="1"
    android:layout_marginTop="8dp" />
```

- Position: below the status text `stateText`, above [Connect]. Put a title TextView, `Devices found`, right above it.
- `0dp` + `layout_weight="1"`: the list takes up all remaining vertical space (same as week 4's `logText`).
- With `wrap_content` instead, the list grows and pushes the buttons below off screen.

---

## Day 1 · 5–15 min ③ — Building and Attaching an ArrayAdapter

```kotlin
// Inside onCreate, above the [Scan] block
val devices = mutableListOf<String>()
val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
binding.deviceList.adapter = adapter
```

- Three values: the screen (`this`), the shape of one row, and the list.
- `android.R.layout.simple_list_item_1` is a one-row layout **Android provides**, not our app's own `R`.
- The listeners below share `devices` and `adapter`, so this goes **above the listeners**.
- If `ArrayAdapter` shows up in red, Alt+Enter (⌥+Enter on Mac) → `android.widget.ArrayAdapter`.

---

## Day 1 · 15–22 min ① — After Changing the List, Call notifyDataSetChanged()

```kotlin
deviceJob = lifecycleScope.launch {
    for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
        delay(1000)
        devices.add(name)
        adapter.notifyDataSetChanged()
        val count = devices.size
        Log.d("Scan", "added: $name, device count: $count")
    }
}
```

- `add` only changes the list. The ListView redraws only when you **tell it to**.
- `for (name in arrayOf(…))` is the same shape as week 10's `for (permission in blePermissions())`.
- The status countdown (week 7's ViewModel) keeps running separately, unaffected.

---

## Day 1 · 15–22 min ② — What Happens Without the Notify Call

| | with `notifyDataSetChanged()` | without it |
|---|---|---|
| Device count in Logcat `tag:Scan` | 1 → 2 → 3 | 1 → 2 → 3 |
| The list on screen | grows by one row per second | doesn't grow, or jumps all at once later |

Demo: delete just the `notifyDataSetChanged()` line inside the `for` loop and tap [Scan].

- Even with correct data, the screen only updates once it's notified. It's the line most often left out.
- Notify again after `devices.clear()` at the start of [Scan] too. Skip clearing and you get `A B C A B C`.
- [Stop] cancels adding names with `deviceJob?.cancel()`, just like week 6.

---

## Day 1 · 22–27 min — Tapping a Row: setOnItemClickListener

```kotlin
binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    val name = adapter.getItem(position) ?: ""
    binding.deviceNameEdit.setText(name)
    Toast.makeText(this, "Selected: $name", Toast.LENGTH_SHORT).show()
}
```

- Of the four values passed in, only the **row number `position`** is used. Counting starts at 0 (A=0, B=1, C=2).
- `getItem` returns a `String?`, the same shape as week 4's `getStringExtra(…) ?: ""`.
- Putting text into an EditText uses `setText(name)`. `text = name` is a build error.
- Since [Connect] already reads this field, the selected name reaches the control screen **without any change there**.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--장치-목록-만들기-60분) · [Walkthrough](walkthrough.md#1일차)

1. Add a title and `deviceList` to `strings.xml` and `activity_main.xml`.
2. Create `devices` and `adapter` **above** the [Scan] block.
3. Have [Scan] add one name per second, [Stop] cancel it, and a row tap fill in the name field.
4. Take a **portrait** screenshot showing all three device names. Rotating clears the list.

**Explanation total: 5+10+7+5+3 = 30 min**

If you see `Unresolved reference 'devices'.`, check whether lines 15–16 sit above the [Scan] block.

---

# Day 2 — Saving Data, Another App's Data, and a Physical Device

`30 min explanation & demo → 60 min lab`

1. Save and read back the last device with SharedPreferences.
2. ContentProvider is a window into another app's data — a demo reading contacts.
3. Run the app on a physical device before week 12.

---

## Day 2 · 0–10 min ① — SharedPreferences: Storage That Survives Closing the App

| | Week 3's `onSaveInstanceState` | `SharedPreferences` |
|---|---|---|
| Survives | rotation (re-creating the screen) | closing and reopening the app |
| Lost when | the app is fully closed | the app is uninstalled |
| Shape | key-value pairs in a `Bundle` | key-value pairs in a named store |
| Used for, this week | — | the last connected device's name |

- The pattern: store the value `"ESP32_BLE_B"` under the key `"last"`.
- Use it for **small** values like settings or the last selection. Don't put long lists or photos in it.

---

## Day 2 · 0–10 min ② — Saving: edit → putString → apply

```kotlin
// Inside the [Connect] listener's else branch, before building the Intent
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
```

| Piece | Meaning |
|---|---|
| `getSharedPreferences("smartio", MODE_PRIVATE)` | open (or create) a store named `smartio`, private to this app |
| `.edit()` | start editing |
| `.putString("last", name)` | put text under the key `last` |
| `.apply()` | commit the save. Skip it and nothing is saved. |

- Save only when [Connect] **actually proceeds**. Don't save when the name field is empty.

---

## Day 2 · 0–10 min ③ — Reading It Back: getString(key, default) ?: ""

```kotlin
// End of onCreate
val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
val lastName = prefs.getString("last", "") ?: ""
if (lastName.isEmpty()) {
    binding.lastDeviceText.text = "Last device: none"
} else {
    binding.lastDeviceText.text = "Last device: $lastName"
}
```

- If nothing has been saved yet, you get the default `""`. `getString` returns `String?`, so we add `?: ""`.
- `"smartio"` and `"last"` must match **exactly** between saving and reading. A mismatch always gives `none`.
- This is read only in `onCreate`. Coming back with [Back] doesn't refresh it yet.

---

## Day 2 · 10–18 min ① — ContentProvider: A Window into Another App's Data

| | SharedPreferences | ContentProvider |
|---|---|---|
| Whose data | this app's own | another app's (contacts, photos, calendar) |
| Who can read it | this app only | any app that's been granted access |
| Shape | small key-value pairs | a table (rows and columns) |
| How to open it | `getSharedPreferences(…)` | `contentResolver.query(address, …)` |
| Permission needed | none | contacts need `READ_CONTACTS` (week 10's flow) |

- This is the fourth component from week 9's comparison table. Today we only **read**, not build one.
- Files and databases are also storage options, but this semester you only need to know their names.

---

## Day 2 · 10–18 min ② — Anatomy of a content URI

```text
content://    com.android.contacts    /contacts
    │                  │                  │
marks it as a       which app's         the table inside it
window address       window (Contacts)   (the contact list)
```

- In code this is the constant `ContactsContract.Contacts.CONTENT_URI`; its value is the address above.
- Just as a web address starts with `https://`, `content://` means "asking a ContentProvider."
- You can't open the Contacts app's file directly. You hand over an address and **ask** the window for it.

---

## Day 2 · 10–18 min ③ — Demo: ContactsReader.names(contentResolver)

```kotlin
// ContactsReader.kt (provided): address, columns to fetch, condition, condition value, sort order
val cursor = resolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    arrayOf(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY),
    null,
    null,
    ContactsContract.Contacts.DISPLAY_NAME_PRIMARY + " ASC"
)
```

- `cursor` is a finger pointing at the result table, one row at a time. Read it with `while (cursor.moveToNext())`, then `close()`.
- From `MainActivity`, call it with the one line `ContactsReader.names(contentResolver)`.
- Permission follows week 10's flow exactly: declare in the manifest → check → request → handle the result.
- The emulator starts with **zero** contacts. Zero is not a failure.

---

## Day 2 · 18–27 min ① — Preparing a Physical Device: Developer Options and USB Debugging

1. Settings › About phone › Software information, then tap **Build number** seven times.
2. Settings › **Developer options** › turn on **USB debugging**.
3. Connect to your PC with a USB cable that carries data — a charge-only cable won't work.
4. Tap **Allow** on the phone's "Allow USB debugging?" prompt.
5. Pick your phone from the device list at the top of Android Studio and press `Run ▶`.

- Menu names and locations vary a bit by manufacturer and Android version.
- The app installs fresh on the phone. The `Last device` saved on the emulator isn't there.

---

## Day 2 · 18–27 min ② — What to Sort Out Before Week 12

| Check | How | If it fails |
|---|---|---|
| Device recognized | phone's name appears in the device list | try a different cable, check the allow prompt, toggle USB debugging off/on |
| Bluetooth | turn it on in quick settings | week 12's scan won't work |
| Location | turn it on in quick settings | Android 11 and below returns zero scan results |
| Permission | [Check Permission] → Toast `Permission OK` | week 10's denial flow → allow it in Settings |

- Week 12's provided library function `PermissionHelper.hasAll()` does the same check as [Check Permission].
- No physical device? Use the connection screen's minutes 32–52 for reading contacts (Day 2 lab step 5) to produce screenshot 3 instead.

---

## Day 2 · 27–30 min ① — A Look Ahead: RecyclerView

| | ListView (this week) | RecyclerView |
|---|---|---|
| Row shape | `simple_list_item_1`, as is | a row XML you design yourself |
| Adapter | one line, `ArrayAdapter` | you write the adapter class yourself |
| Very long lists | works | lighter, since off-screen row Views are reused |
| This semester | used through weeks 12–14 | introduced only — no lab, not graded |

- Most modern apps use RecyclerView for long lists. The list → adapter → screen structure is the same.

---

## Day 2 · 27–30 min ② — Try It Yourself

[Day 2 lab](lab.md#2일차--마지막-장치-저장과-실기기-준비-60분) · [Walkthrough](walkthrough.md#2일차)

1. Add spots for `lastDeviceText` and `contactsButton`.
2. Save on [Connect], read it back in `onCreate`. Close and reopen the app, then take a screenshot.
3. If you have a physical device, run it over USB debugging and take a screenshot.
4. If not, follow the contacts-reading steps and screenshot the dialog.

**Explanation total: 10+8+9+3 = 30 min**

**Uninstalling** the app clears its storage too. Going back to `none` isn't a bug in your code.

---

## What to Submit

Submit once, at the end of Day 2.

1. **`MainActivity.kt`**
2. **Screenshot 1**: the connection screen (portrait) with all three device names listed after [Scan]
3. **Screenshot 2**: the first screen after fully closing and reopening the app — `Last device: …`, an empty list, `Not connected`
4. **Screenshot 3**: the connection screen running on a physical device, with the status bar visible (or the contacts dialog if unavailable)

---

## Next Week Preview

This week's [Scan] added fake names: `ESP32_BLE_A`, `B`, `C`.

In week 12, the provided library's `client.startScan(…)` finds **real board names**.

The list, adapter, and row-tap code stay the same — only where the names come from changes.
