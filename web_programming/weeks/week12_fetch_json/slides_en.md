---
marp: true
theme: default
paginate: true
header: "Web programming · Week 12"
footer: "fetch · Promise · async/await"
---

# Fetch with Promises and async/await

Start with timers to see which lines run first and how `async` functions work.
Read a to-do from JSONPlaceholder, then practice reading responses and handling errors with exchange-rate, tarot card, and public-holiday APIs.

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

GET [https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)

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

GET [https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)

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

## Day 2 · 0–5 min · Request an exchange rate

[Example 04](examples/day2/ex04/index.html) · [Exchange-rate request](examples/day2/ex04/requests.http)

GET [https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW](https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW)

`USD` is the base currency and `KRW` is the target currency.

Click **Send Request** and locate `date` and `rates`.

---

## Day 2 · 5–20 min · Read a nested exchange-rate field

| Response field | Value to display |
|---|---|
| `date` | Reference date |
| `rates.KRW` | Reference rate in Korean won per US dollar |

Find the lines that read both fields and compare them with the response. [Example 04 code](examples/day2/ex04/app.js)

---

## Day 2 · 20–35 min · Compare 200 and 404 responses

[Example 05](examples/day2/ex05/index.html) · [Both requests](examples/day2/ex05/requests.http)

| GET URL | HTTP status | `response.ok` |
|---|---|---|
| [https://tarotapi.dev/api/v1/cards/random?n=1](https://tarotapi.dev/api/v1/cards/random?n=1) | 200 | true |
| [https://tarotapi.dev/api/v1/cards/zzmissing](https://tarotapi.dev/api/v1/cards/zzmissing) | 404 | false |

When the server sends `404`, `fetch()` still fulfills with a Response. Check `response.ok` before reading the body. For `200`, read the name and meaning from `cards[0]`.

---

## Day 2 · 35–45 min · Connection failure and catch

[Example 06 holidays page](examples/day2/ex06/index.html) · [Code](examples/day2/ex06/app.js)

1. With the page open, check **Disable cache** in DevTools Network and select **Offline**.
2. Click **공휴일 조회**. The request rejects before receiving an HTTP response and execution moves to `catch`.
3. Restore **No throttling** and request the same country again.

To handle HTTP errors in `catch`, check `response.ok` and throw an error.

---

## Day 2 · 45–55 min · Render a public-holiday array

| Country | GET URL for 2026 |
|---|---|
| South Korea | [https://nagerholidays.com/api/v4/Holidays/KR/2026](https://nagerholidays.com/api/v4/Holidays/KR/2026) |
| Japan | [https://nagerholidays.com/api/v4/Holidays/JP/2026](https://nagerholidays.com/api/v4/Holidays/JP/2026) |
| United States | [https://nagerholidays.com/api/v4/Holidays/US/2026](https://nagerholidays.com/api/v4/Holidays/US/2026) |

The browser example appends the current year to the URL.

Example 06 loops over the response array and displays `date` and `name` for nationwide public holidays. It replaces the list with the new results and re-enables the request button in `finally`. [Requests by country](examples/day2/ex06/requests.http)

---

## Day 2 · 55–60 min · Practice

| Practice time | Activity |
|---|---|
| 0–8 min | Compare the reference date and rate with the response |
| 8–16 min | Request a random card and an unknown card to compare `200` and `404` |
| 16–30 min | View holidays by country, try Offline, and retry after reconnecting |

Submit the [public-holiday list](examples/day2/ex06/index.html). Capture the list and the GET `200` in Network together. [Practice sheet](lab.md)

---

## Optional practice · Current temperature in three cities

Open a city’s URL. Find the temperature in `current.temperature_2m` and its unit in `current_units.temperature_2m`. Compare them with **기온 조회** for the same city.

**Seoul**\
[https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m)

**Jeonju**\
[https://api.open-meteo.com/v1/forecast?latitude=35.8248&longitude=127.1480&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=35.8248&longitude=127.1480&current=temperature_2m)

**Iksan**\
[https://api.open-meteo.com/v1/forecast?latitude=35.9439&longitude=126.9544&current=temperature_2m](https://api.open-meteo.com/v1/forecast?latitude=35.9439&longitude=126.9544&current=temperature_2m)

[Example 07 weather page](examples/day2/ex07/index.html) · [REST Client requests for all three cities](examples/day2/ex07/requests.http)

---

# Week 12 site and Week 13 guestbook

The [course site home page](examples/day2/web-week12/index.html) displays the weather. Its Guestbook menu saves entries in the browser.

[Read server entries](examples/day2/web-week12/guestbook.html) is a separate optional exercise. Use the public key in the `apikey` header in the [REST Client requests](examples/day2/web-week12/requests.http). The example below uses `student01`.

- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/about](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/about)
- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/help?order=step.asc](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/help?order=step.asc)
- [https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50](https://esoqbcwgzjtwcqszwvin.supabase.co/rest/v1/guestbook?book_id=eq.student01&select=id,name,message,created_at&order=id.desc&limit=50)

In Week 13, create, edit, and delete an entry on the same server. [Site instructions](examples/day2/web-week12/README.md)
