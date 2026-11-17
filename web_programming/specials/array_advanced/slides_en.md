---
marp: true
theme: default
paginate: true
header: "Web Programming · Advanced Arrays"
footer: "Original array · Return value · Callback · Object reference"
---

# Advanced Arrays

Compare insertion, deletion, iteration, selection, transformation, and accumulation.

- Read the original array and return value separately.
- Inspect arguments and return values of function callbacks.
- Examine empty arrays and shared object references.
- Supplementary lesson, excluded from the regular Week 11 assignment.

[Lab](lab.md) · [Walkthrough](walkthrough.md)

---

## Preparation and shared CSS

Prerequisites: arrays, objects, functions, and DOM events. No arrow syntax needed.
Run from the repository root.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

Open http://localhost:8111/specials/array_advanced/examples/01_insert_delete/

An internet connection is required to load [W3.CSS from the CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css).
Keep the examples and the additional web_programming/shared/examples.css in their relative locations.

---

## Five examples and a shared student array

Example 01 uses fruit. Examples 02–05 use these students.

```js
const students = [
  { name: '하늘', score: 80 },
  { name: '바다', score: 60 },
  { name: '노을', score: 90 }
];
```

01 Insert/delete → 02 Iterate → 03 filter → 04 map → 05 reduce
Predict before running; compare the original, return value, and view.
Arrays stay in memory only. Reloading restores the initial state.

---

## 01: Mutation and return values

[Insertion/deletion source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/01_insert_delete/app.js)

| Method | Original array | Return value |
|---|---|---|
| push(value) | Append | New length |
| unshift(value) | Prepend | New length |
| pop() | Remove last item | Removed value |
| shift() | Remove first item | Removed value |

Reset before each experiment. The initial array is 사과, 바나나, 포도.
Pushing 귤 produces four items and returns the number 4.

---

## 01: splice and empty arrays

Reset before testing each line.

```js
fruits.splice(1, 0, '귤'); // Insert at index 1; returns []
fruits.splice(1, 1);      // Remove at index 1; returns ['바나나']
```

- splice returns an array of removed items.
- pop or shift on an empty array returns undefined.
- This UI accepts insertion indexes 0–length and deletion indexes 0–length-1.
- The example does not cover every index rule supported by JavaScript splice.

---

## 02: for...of and forEach

[Iteration source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/02_iteration/app.js)

```js
for (const student of students) {
  console.log(student.name);
}
const result = students.forEach(function (student) {
  console.log(student.name);
}); // result is undefined
```

The runnable example creates li elements instead of logging to the Console.
for...of is a loop. forEach calls a callback and does not return a new array.

---

## 03: filter selects matching items

[filter source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/03_filter/app.js)

```js
const selected = students.filter(function (student) {
  return student.score >= minimum;
});
```

- student is the current object. A true result includes it in the new array.
- Minimum 70: 하늘 and 노을, two students
- Minimum 60: all three / minimum 100: an empty array [], zero students
- No student is removed from the original array.

---

## 04: map builds an array from callback results

[map source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/04_map/app.js)

```js
const adjusted = students.map(function (student) {
  return { name: student.name, score: student.score + bonus };
});
```

A bonus of 5 produces scores 85, 65, and 95.
Repeating the action starts from 80, 60, and 90; the bonus does not accumulate.
The callback returns a new object. It does not assign to the original student's score.

---

## A new array is not a deep copy

| Example | New array | Objects inside |
|---|---|---|
| filter | Yes | Shared with selected original objects |
| Current map code | Yes | New objects created by the callback |

Changing an object field in a filter result also changes the original object.
A map callback can also share or modify original objects if written that way.
These examples preserve originals by reading fields or creating new objects.
A new array alone does not establish that its objects were deeply copied.

---

## 05: The reduce accumulator

[reduce source](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/05_reduce/app.js)

```js
const total = students.reduce(function (accumulator, current) {
  return accumulator + current.score;
}, 0);
```

| Call | accumulator | current.score | Return value |
|---|---|---|---|
| 1 | 0 | 80 | 80 |
| 2 | 80 | 60 | 140 |
| 3 | 140 | 90 | 230 |

---

## 05: Initial value and empty input

- The first accumulator is the initial value 0 supplied as the last argument.
- Each returned value becomes the accumulator on the next call.
- The final returned value, 230, is the result of reduce.
- Empty array with initial value 0: result 0, zero callback calls

Select the empty-array checkbox and calculate again.
The table is built from actual steps.push calls inside the callback; it now has no rows.
Calling reduce on an empty array without an initial value throws an error.

---

## Compare original arrays and return values

| Operation | Original in this example | Return value |
|---|---|---|
| push/unshift/pop/shift/splice | Changed | Length, removed value, or array |
| forEach | Preserved | undefined |
| filter | Preserved | New array of selected items |
| map | Preserved | Array containing new objects |
| reduce | Preserved | Numeric sum |

A callback that assigns to original objects can change the preservation behavior.

---

## Change inputs and compare

1. Insert/delete: reset each time; record array state and return value.
2. Iterate: compare both lists and their return-value descriptions.
3. filter: test minimum scores 70, 60, 100, and the boundary at 80.
4. map: repeat bonus 5, then compare bonuses 10, 0, and -5.
5. reduce: compare the sum and callback count for normal and empty input.

One delivery example: 60-minute explanation/demo + 30-minute practice.
This is not a limit on the lesson's total duration, sessions, or material.
[Lab](lab.md) · [Example guide](examples/README.md)

---

## Explanations and experiment records

- Why push returns a length rather than the changed array
- Why an insertion-only splice returns []
- How forEach results differ from map results
- Shared filter references versus new map objects
- The role of the initial value in an empty-array reduce

Record example/input → prediction → observation → reason for any difference.
Keep useful screenshots and code. This is separate from the Week 11 submission.
