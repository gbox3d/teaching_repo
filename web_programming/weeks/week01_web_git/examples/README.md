# 1주차 예제 — 세 파일로 만든 작은 페이지

1일차와 2일차의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
파일은 브라우저로 **더블클릭해서** 연다(`file://` 주소). 이번 주에는 서버를 켜지 않는다.
`student01`은 예시 별칭이다. 본인 수업용 별칭으로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [2단계](../walkthrough.md#2-세-파일-만들기)에서 만들고, [5단계](../walkthrough.md#5-내-소개로-고치고-저장하기)에서 이 파일과 같아진다 | `week01/index.html` |
| [day1/styles.css](day1/styles.css) | [2단계](../walkthrough.md#2-세-파일-만들기) — 그대로 붙여 넣는다 | `week01/styles.css` |
| [day1/app.js](day1/app.js) | [2단계](../walkthrough.md#2-세-파일-만들기) — 붙여 넣고 읽기만 한다 | `week01/app.js` |
| [day2/index.html](day2/index.html) | [13~15단계](../walkthrough.md#13-commit-1--제목-만들기) — commit 세 개를 마치면 이 파일이 된다 | `week01-practice/index.html` |
| [day2/styles.css](day2/styles.css) · [day2/app.js](day2/app.js) | [15단계](../walkthrough.md#15-commit-3--스타일과-스크립트-연결) — 1일차 폴더에서 복사해 넣는다 | `week01-practice/styles.css` · `app.js` |

## 1. 1일차 완성 — 내 소개 페이지

`day1/` 세 파일을 한 폴더에 두고 `index.html`을 더블클릭하면 카드 한 장이 열린다.

```text
Week 01 · HTML · CSS · JavaScript
안녕하세요, student01입니다
웹프로그래밍 수업에서 만든 첫 페이지입니다.
[눌러 보기] 클릭 횟수: 0
```

- `index.html`: 제목 `<h1>`, 소개 문단 `<p>`, 버튼과 `<p id="status">`. 머리에서 `styles.css`·`app.js`를 연결한다.
- `styles.css`: 카드 모양, 배경색, 버튼 색.
- `app.js`: 버튼을 누를 때마다 `클릭 횟수`를 1씩 올리고, Console에 `week01 ready`를 남긴다.

`<h1>`과 소개 문단은 본인 소개로 바꾼다. 나머지는 그대로 두어도 된다.

## 2. 2일차 완성 — 연습 페이지와 commit 세 개

`day2/`는 `week01-practice` 폴더의 **마지막 모습**이다. `styles.css`와 `app.js`는 day1과 같은 파일이다.

| commit | 메시지 | `index.html`에 생기는 것 |
|---|---|---|
| 1 | `제목 만들기` | 뼈대와 제목 `<h1>` |
| 2 | `소개 문단과 링크 추가` | 소개 `<p>`, 교재 사이트 `<a>`, 버튼, `<p id="status">` |
| 3 | `스타일과 스크립트 연결` | 머리의 `<link>`·`<script>` 두 줄 (+ 새 파일 `styles.css`·`app.js`) |

commit 2까지는 글자만 보이고 버튼을 눌러도 아무 일이 없다.
commit 3에서 두 파일을 연결하면 카드 모양이 생기고 버튼이 동작한다. 세 파일이 각각 무엇을 맡는지 눈으로 확인할 수 있다.

## 3. `app.js`는 읽기만 한다

```js
countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});
```

"버튼을 누르면 숫자를 1 올리고 화면 글자를 바꾼다"는 뜻이다. 이번 주에는 이 파일을 고치지 않는다.
JavaScript 문법은 뒤 주차에서 배운다.

## 공식 참고 자료

- [첫 번째 웹사이트 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Your_first_website)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
