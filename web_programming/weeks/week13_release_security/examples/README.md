# 13주차 예제 — 점검을 마친 네 페이지와 README 최종판

`day1/`·`day2/`는 그날 수업이 끝났을 때의 **`my-web` 폴더 전체**다. 그 주에 고치지 않은 파일도 함께 들어 있다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

이번 주에 바뀌는 파일은 **세 개뿐**이다. `about.html`·`about.js`·`projects.js`.
나머지는 12주차 파일 그대로이며 `styles.css`에는 한 줄도 더하지 않는다.

`projects.html`은 `fetch`를 쓰므로 파일을 더블클릭해 열면 카드가 보이지 않는다. 공개 주소에서 확인한다(12주차와 같다).

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/about.html](day1/about.html) | [2단계](../walkthrough.md#2-abouthtml에-입학-연도-폼-넣기) — `script` 줄과 입학 연도 폼이 늘어난다 | `about.html` |
| [day1/about.js](day1/about.js) | [3단계](../walkthrough.md#3-aboutjs로-몇-년차인지-계산하기) — 이번 주에 새로 만드는 파일 | `about.js` |
| [security-demo.html](security-demo.html) · [security-demo.js](security-demo.js) | [4단계](../walkthrough.md#4-글자로-넣기와-html로-넣기-비교하기) — **시연용**. `my-web`에 넣지 않는다 | (넣지 않는다) |
| [day1/guestbook.js](day1/guestbook.js) | [5단계](../walkthrough.md#5-방명록에-b안녕b-남겨-보기) — 눈으로 확인만 하고 고치지 않는다 | `guestbook.js` |
| [day1/projects.js](day1/projects.js) | [7단계](../walkthrough.md#7-카드-링크-글자-고치기-projectsjs) — 링크 글자 한 줄이 바뀐다 | `projects.js` |
| [day2/README.md](day2/README.md) | [11단계](../walkthrough.md#11-readmemd-최종판-쓰기) — 9주차 1차판을 지우고 다시 쓴다 | `README.md` |
| [day2/screenshots/home.png](day2/screenshots/home.png) · [guestbook.png](day2/screenshots/guestbook.png) · [projects.png](day2/screenshots/projects.png) | [10단계](../walkthrough.md#10-화면-캡처-세-장-넣기) | `screenshots/` 세 장 |
| [day1/index.html](day1/index.html) · [guestbook.html](day1/guestbook.html) · [projects.html](day1/projects.html) · [app.js](day1/app.js) · [styles.css](day1/styles.css) · [data/projects.json](day1/data/projects.json) | 이번 주에 고치지 않는다 (12주차와 같다) | 같은 이름의 파일 |

## 1. 시연용 예제 — security-demo

같은 입력을 두 가지 방법으로 넣어 차이를 본다. 이 두 파일은 수업 시연용이며 `my-web`에 넣지 않는다.

```js
textButton.addEventListener('click', function () {
  output.textContent = input.value;
});

htmlButton.addEventListener('click', function () {
  output.innerHTML = input.value;
});
```

입력 칸에는 `<b>안녕</b>`이 미리 적혀 있다. 두 버튼을 차례로 누르면 결과 자리가 이렇게 바뀐다.

```text
[textContent로 넣기]  결과 → <b>안녕</b>      (글자 그대로. 상자 안에 태그가 보인다)
[innerHTML로 넣기]    결과 → 안녕            (굵은 글씨. 태그가 HTML로 실행되었다)
```

- 두 줄의 차이는 단어 하나뿐인데 결과가 다르다.
- 내가 적은 글이면 괜찮지만, 다른 사람이 적은 글을 `innerHTML`로 넣으면 그 사람이 적은 HTML이 내 페이지에서 실행된다.
- 그래서 입력한 글을 보여 줄 때는 `textContent`를 쓴다. `innerHTML`은 `innerHTML = ''`처럼 **비울 때만** 쓴다.

## 2. 1일차 완성 — 입학 연도 폼과 점검

`day1/about.html`에는 표 아래에 폼 하나가 늘어났다. `head`에는 `<script src="about.js" defer></script>` 한 줄이 붙었다.

```html
<h2>몇 년차일까요?</h2>
<form id="year-form">
  <p>
    <label for="year">입학 연도</label>
    <input id="year" type="text">
    <button type="submit">계산하기</button>
  </p>
</form>
<p class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</p>
```

`day1/about.js`는 18줄이고 이름 붙인 함수 정의는 없다. 제출 리스너 하나가 전부다.

```js
const text = yearInput.value.trim();
const year = Number(text);
if (text === '' || isNaN(year)) {
  yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';
  yearInput.focus();
  return;
}
const thisYear = new Date().getFullYear();
const years = thisYear - year + 1;
```

공개 주소에서 `/my-web/about.html`을 열고 `2023`을 적어 **계산하기**를 누르면 이렇게 보인다(올해가 2026년일 때).

```text
몇 년차일까요?
입학 연도 [2023] [계산하기]
┌──────────────────────────────────────────┐
│ 2023년에 입학했으니 올해 4년차입니다.       │
└──────────────────────────────────────────┘
```

`이천이십삼`처럼 숫자가 아닌 글자를 적으면 `입학 연도를 숫자로 적어 주세요.`가 같은 자리에 보인다.

`day1/projects.js`는 19행 한 줄만 바뀌었다.

| 주차 | 코드 | 카드 세 장의 링크 글자 |
|---|---|---|
| 12주차 | `link.textContent = '페이지 열기';` | 페이지 열기 · 페이지 열기 · 페이지 열기 |
| 13주차 | ``link.textContent = `${projects[i].title} 열기`;`` | 자기소개 페이지 열기 · 내 정보 표 열기 · 방명록 열기 |

## 3. 2일차 완성 — README 최종판

`day2/`는 `day1/`에 `README.md` 최종판과 `screenshots/` 그림 세 장이 더해진 것이다. **HTML·CSS·JS는 day1과 완전히 같다.**

`day2/README.md`가 쓰는 마크다운은 네 가지뿐이다.

| 기호 | 쓰임 | 예 |
|---|---|---|
| `#` | 제목 | `## 공개 주소` |
| `-` | 목록 한 줄 | `- 홈의 버튼을 누르면 …` |
| 대괄호 + 소괄호 | 링크 | `[공개 주소](https://student01.github.io/my-web/)` |
| 링크 앞에 `!` | 그림 | 대괄호에 `홈 화면`, 소괄호에 `screenshots/home.png` |

절 구성은 아래와 같다. 9주차 1차판에 **화면 3장·사용 기술·어려움과 해결·만든 과정**이 더해졌다.

```text
# my-web — student01의 웹 연습장
## 공개 주소        → https://student01.github.io/my-web/
## 페이지           → 네 페이지와 한 줄 설명
## 기능             → 다섯 줄
## 화면             → screenshots 그림 세 장
## 사용 기술        → HTML · CSS · JavaScript · GitHub Pages
## 어려움과 해결    → 세 줄
## 만든 과정        → git log --oneline 다섯 줄
```

## 4. day1과 day2의 차이

| 파일 | day1 | day2 |
|---|---|---|
| `about.html` · `about.js` | 이번 주에 만든 상태 | day1과 같다 |
| `projects.js` | 링크 글자를 고친 상태 | day1과 같다 |
| `README.md` | 9주차 1차판(29줄) | **최종판(51줄)** |
| `screenshots/` | `home.png` · `guestbook.png` (9주차에 찍은 것) | 세 장 모두 13주차 화면으로 새로 찍었다 |
| `index.html` · `guestbook.html` · `projects.html` · `app.js` · `guestbook.js` · `styles.css` · `data/projects.json` | 12주차와 같다 | day1과 같다 |

9주차 캡처를 그대로 두지 않는 이유는 그때 nav가 세 페이지였기 때문이다. 최종판 README의 설명과 화면이 어긋난다.

## 공식 참고 자료

- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Element.innerHTML — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/innerHTML)
- [label 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/label)
- [기본 작성 및 서식 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
