---
marp: true
theme: default
paginate: true
header: "Web programming · Week 12"
footer: "fetch · Promise · async/await"
---

# Fetch with Promises and async/await

Start with a timer to see which lines run first.
Read a to-do from JSONPlaceholder, then fetch the current temperature for Seoul and Busan.

Each session has 60 minutes of lecture and demos and 30 minutes of practice. [Examples](examples/README.md)

---

## Day 1 · 0–5 min · Open the timer example

[Example 01](examples/day1/ex01/index.html) · [Code](examples/day1/ex01/app.js)

Before pressing the button, predict the order of the three lines. Then start the timer and watch which ones appear before it finishes.

This example runs in the browser. The public APIs used later accept requests without a key.

---

## Day 1 · 5–15 min · While the timer is running

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

## Day 1 · 15–30 min · Receive a Promise result

| State | Meaning |
|---|---|
| pending | Still waiting for an outcome |
| fulfilled | The operation succeeded with a value |
| rejected | The operation failed with a reason |

When the timer in example 01 calls `resolve`, the pending Promise fulfills. The function registered with `.then()` receives the value. A `.catch()` handler can handle rejection.

---

## Day 1 · 30–40 min · From response to title

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

The first callback receives the HTTP response. Returning the Promise from `response.json()` passes the parsed to-do object to the next callback.

---

## Day 1 · 40–55 min · Await the same request

[Example 03](examples/day1/ex03/index.html) · [Code](examples/day1/ex03/app.js)

```js
const response = await fetch(url);
if (!response.ok) throw new Error('HTTP ' + response.status);
const todo = await response.json();
output.textContent = todo.title;
```

`await` pauses this `async` function before its next line. The browser can handle input in the meantime. Calling an `async` function returns a Promise.

---

## Day 1 · 55–60 min · Practice

| Practice time | Activity |
|---|---|
| 0–8 min | Predict and verify the timer output in example 01 |
| 8–18 min | Use **Send Request** and compare the title in example 02 |
| 18–30 min | Rewrite a copy of example 02 using `try/catch` and two `await` expressions. Run it, then check example 03 |

What value reaches the next callback when the `return` in `return response.json()` is removed? Write down your prediction. [Practice sheet](lab.md)

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

For an optional preview, open the [guestbook](examples/day2/web-week12/guestbook.html) and enter your publishable key and book id. [Connection check, help and list requests](examples/day2/web-week12/requests.http) · [Settings](examples/day2/web-week12/README.md)
