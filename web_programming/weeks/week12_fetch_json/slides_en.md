---
marp: true
theme: default
paginate: true
header: "Web programming · Week 12"
footer: "fetch · Promise · async/await"
---

# Fetch with Promises and async/await

Start with timers to see which lines run first and how `async` functions work.
Read a to-do from JSONPlaceholder, then fetch the current temperature for Seoul and Busan.

Each session has 60 minutes of lecture and demos and 30 minutes of practice. [Examples](examples/README.md)

---

## Day 1 · 0–5 min · Open the timer example

[Example 01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

Before pressing the button, predict the order of the three lines. Then start the timer and watch which ones appear before it finishes.

Examples 01 to 01d use only browser timers. The public APIs used later accept requests without a key.

---

## Day 1 · 5–12 min · While the timer is running

1. Click **타이머 시작**. The first line appears.
2. After scheduling the timer, the next line runs right away.
3. About one second later, the callback receives the result and displays the final line.

```js
const timer = new Promise(function (resolve) {
  setTimeout(function () { resolve('3. 타이머 완료'); }, 1000);
});
```

`new Promise(...)` returns the pending Promise immediately. The browser remains free to handle other input.

---

## Day 1 · 12–16 min · A wait function that returns a Promise

[Example 01b](examples/day1/ex01b_wait/index.html) · [Code](examples/day1/ex01b_wait/app.js)

```js
function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}
```

Calling `wait(1000)` returns a pending Promise immediately. About one second later, `resolve()` runs and the Promise fulfills. Examples 01c and 01d use the same function.

---

## Day 1 · 16–20 min · A wait function that returns a Promise

| State | Meaning | In example 01b |
|---|---|---|
| pending | Still waiting for an outcome | Right after calling `wait(1000)` |
| fulfilled | The operation succeeded with a value | After `resolve()`, about one second later |
| rejected | The operation failed with a reason | Not here. See the failing timer in example 01d |

The second `.then()` waits for the Promise from `return wait(1000);`. Optional: remove `return` and see when line 3 appears.

---

## Day 1 · 20–30 min · Async functions and await

[Example 01c](examples/day1/ex01c_async_await/index.html) · [Code](examples/day1/ex01c_async_await/app.js)

```js
button.addEventListener('click', async function () {
  output.textContent = '1. 시작\n';
  await wait(1000);
  output.textContent += '2. 1초 지남\n';
  await wait(1000);
  output.textContent += '3. 2초 지남\n';
});
```

`await` pauses only this `async` function. It continues with the next line once the Promise fulfills. Click **클릭** while you wait and the count still goes up. The order matches the two `.then()` calls in example 01b.

---

## Day 1 · 30–34 min · What an async function returns

[Example 01d](examples/day1/ex01d_async_return/index.html) · [Code](examples/day1/ex01d_async_return/app.js)

```js
async function makeMessage() {
  await wait(1000);
  return '1초 타이머 완료';
}

messageButton.addEventListener('click', async function () {
  const promise = makeMessage();
  console.log(promise);
  output.textContent += '2. 다음 줄 먼저 실행\n';
  const message = await promise;
  output.textContent += `3. 받은 값: ${message}\n`;
});
```

`makeMessage()` returns a Promise before it finishes. Console shows it as pending, and about one second later `await promise` receives the `return` value.

---

## Day 1 · 34–38 min · What an async function returns

| Rule for async functions | Where to see it in example 01d |
|---|---|
| A call returns a Promise right away | The line after `makeMessage()` runs first |
| `return` gives the fulfillment value | The string from `await promise` |
| `throw` gives the rejection reason | `error.message` for **실패 타이머** |
| Use `await` only in `async` functions | `async function` on the click listeners |
| `await` pauses only that function | The click count during the wait in example 01c |

A file loaded with `<script src="app.js" defer>` cannot use `await` outside a function, so the click listener functions are marked `async`.

---

## Day 1 · 38–48 min · From response to title

[Example 02](examples/day1/ex02/index.html) · [REST Client request](examples/day1/ex02/requests.http)

```js
fetch(url)
  .then(function (response) {
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.json();
  })
  .then(function (todo) {
    output.textContent = todo.title;
  });
```

The first callback receives the HTTP response. Returning the Promise from `response.json()` passes the parsed to-do object to the next callback. This is the same shape as `return wait(1000);` in example 01b.

---

## Day 1 · 48–55 min · Await the same request

[Example 03](examples/day1/ex03/index.html) · [Code](examples/day1/ex03/app.js)

```js
const response = await fetch(url);
if (!response.ok) throw new Error('HTTP ' + response.status);
const todo = await response.json();
output.textContent = todo.title;
```

`await fetch(url)` and `await response.json()` take the places of the two `await wait(1000);` lines in example 01c. The browser keeps handling input while it waits.

---

## Day 1 · 55–60 min · Practice

| Practice time | Activity |
|---|---|
| 0–8 min | In a copy of example 01c, add `await wait(1000);` and one output line to show ‘4. 3초 지남’. Check **클릭** while waiting |
| 8–18 min | Use **Send Request** and compare the title in example 02 |
| 18–30 min | Rewrite a copy of example 02 using `try/catch` and two `await` expressions. Run it, then check example 03 |

Optional observations: when line 3 appears after removing `return` in example 01b, and **실패 타이머** in example 01d. [Practice sheet](lab.md)

---

## Day 2 · 0–5 min · Request Seoul weather

[Example 04](examples/day2/ex04/index.html) · [Seoul request](examples/day2/ex04/requests.http)

Send Seoul's latitude and longitude to `GET /v1/forecast`. The parameter `current=temperature_2m` requests current air temperature two metres above ground.

Click **Send Request** and locate `current` and `current_units`.

---

## Day 2 · 5–20 min · Read the temperature and unit

| Response field | Value to display |
|---|---|
| `weather.current.temperature_2m` | Current temperature |
| `weather.current_units.temperature_2m` | Unit of temperature |

Find both fields in the [example 04 code](examples/day2/ex04/app.js) and compare them with the response. The temperature can change between requests.

---

## Day 2 · 20–35 min · Invalid latitude and HTTP responses

[Example 05](examples/day2/ex05/index.html) · [Both requests](examples/day2/ex05/requests.http)

| Latitude | HTTP status | `response.ok` |
|---|---|---|
| Seoul, 37.5665 | 200 | true |
| 999 | 400 | false |

The server sent an HTTP response even for 400, so the Promise from `fetch()` fulfills. Read the status and the error body's `reason` field to find the invalid value.

---

## Day 2 · 35–45 min · Connection failure and catch

[Example 06 weather page](examples/day2/ex06/index.html) · [Code](examples/day2/ex06/app.js)

1. With the page open, set Network in DevTools to **Offline**.
2. Click **기온 조회**. The request rejects before receiving an HTTP response and execution moves to `catch`.
3. Restore **No throttling** and request the same city again.

To handle an HTTP 400 in `catch` as well, check `response.ok` and throw an error.

---

## Day 2 · 45–55 min · Select a city and retry

| City | Latitude | Longitude |
|---|---|---|
| Seoul | 37.5665 | 126.9780 |
| Busan | 35.1796 | 129.0756 |

Example 06 builds a URL with the selected coordinates. It disables the button while the request is pending and re-enables it in `finally`. Choose a city for each request. [Requests for both cities](examples/day2/ex06/requests.http)

---

## Day 2 · 55–60 min · Practice

| Practice time | Activity |
|---|---|
| 0–8 min | Compare Seoul's temperature and unit with the response |
| 8–16 min | Compare the HTTP statuses for Seoul's latitude and 999 |
| 16–30 min | Switch cities, try Offline, restore the network and retry |

Submit the [city weather page](examples/day2/ex06/index.html). Capture the temperature and the GET 200 in Network together. [Practice sheet](lab.md)

---

# Next week · Write a guestbook entry

In week 13, POST JSON to the class Supabase project and read the new entry's id. The starter code includes the list-reading function.

For an optional preview, change `BOOK_ID` in the guestbook folder's `config.example.js` to your assigned book id. The first time you open the [guestbook](examples/day2/web-week12/guestbook.html), a dialog asks for the publishable key. Enter the key you received and this browser keeps it. If you entered it wrong, click **공개 키 지우기** and enter it again. [Connection check, help and list requests](examples/day2/web-week12/requests.http) · [Settings](examples/day2/web-week12/README.md)
