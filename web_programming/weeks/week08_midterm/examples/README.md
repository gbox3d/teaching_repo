# 8주차 예제 — 리허설 문제와 해답

이 폴더에는 **1일차 리허설**에 쓰는 파일만 있다. 2일차 본시험 문제와 답안은 여기에 없다.
`rehearsal_starter`는 문제, `rehearsal_solution`은 그 해답이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 해답과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

본시험 starter도 이것과 **같은 구조**다. 폴더 하나에 `index.html`·`styles.css`·`app.js` 세 개이고, 라이브러리와 CDN은 쓰지 않는다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 폴더의 파일 |
|---|---|---|
| [rehearsal_starter/index.html](rehearsal_starter/index.html) | [2단계](../walkthrough.md#2-starter-세-파일-넣기) — 그대로 넣고 시작한다 | `midterm-practice/index.html` |
| [rehearsal_starter/styles.css](rehearsal_starter/styles.css) | [2단계](../walkthrough.md#2-starter-세-파일-넣기) | `midterm-practice/styles.css` |
| [rehearsal_starter/app.js](rehearsal_starter/app.js) | [2단계](../walkthrough.md#2-starter-세-파일-넣기) | `midterm-practice/app.js` |
| [rehearsal_solution/index.html](rehearsal_solution/index.html) | [3단계](../walkthrough.md#3-문제-1-목록과-표-넣기) — 문제 1의 해답 | 맞춰 보기용 |
| [rehearsal_solution/styles.css](rehearsal_solution/styles.css) | [4단계](../walkthrough.md#4-문제-2-카드-색과-nav-가로-배치) — 문제 2의 해답 | 맞춰 보기용 |
| [rehearsal_solution/app.js](rehearsal_solution/app.js) | [5~6단계](../walkthrough.md#5-문제-3-버튼으로-글자와-색-바꾸기) — 문제 3·4의 해답 | 맞춰 보기용 |

해답은 **다 풀어 본 뒤에** 연다. 먼저 열면 어디서 막히는지 알 수 없다.

## 1. 문제 네 개

`rehearsal_starter`를 열면 꾸미지 않은 화면에 빈 자리가 보인다. 주석 아홉 자리(`index.html` 2 · `styles.css` 3 · `app.js` 4)가 문제다.

```text
사진 동아리 소개          ← header > h1
활동  모임  신청          ← header > nav > a 세 개
활동                      ← 문제 1: ul 세 줄 + 2열 3행 table
모임                      ← 문제 3: 버튼 두 개
  아직 누르지 않았습니다.
  [이번 주 모임 보기] [다크 모드]
신청                      ← 문제 4: 이름·신청 이유 + [신청하기]
```

| 문제 | 파일 | 하는 일 | 배운 주 |
|---|---|---|---|
| 1 | `index.html` | `ul`·`li` 세 줄과 2열 3행 `table` 넣기 | 3주 |
| 2 | `styles.css` | `.card` 규칙, `nav`를 `flex`, `@media`에서 세로 | 4주 |
| 3 | `app.js` | 버튼 클릭 → `textContent` 바꾸기 / `classList.toggle('dark')` | 5·6주 |
| 4 | `app.js` | 제출 → `#result`에 표시, 이름이 비면 안내 | 7주 |

## 2. 개념별 최소 코드

목록과 표:

```html
<ul>
  <li>매주 금요일 사진 찍으러 나가기</li>
</ul>
<table>
  <tr><th>항목</th><th>내용</th></tr>
  <tr><td>모이는 곳</td><td>학생회관 2층</td></tr>
</table>
```

class 선택자와 가로 배치, 좁은 화면:

```css
.card { padding: 16px; border: 1px solid #c7d0e8; background: white; }
nav { display: flex; gap: 16px; }
@media (max-width: 600px) { nav { flex-direction: column; } }
```

클릭으로 글자 바꾸기와 class 붙였다 떼기:

```js
noticeButton.addEventListener('click', function () {
  noticeText.textContent = '이번 주 모임: 금요일 오후 5시';
});
```

제출 받기와 빈값 안내:

```js
joinForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
});
```

## 3. 두 폴더의 차이

| 파일 | starter | solution |
|---|---|---|
| `index.html` | `활동` 아래가 주석 두 줄 | `ul` 세 줄과 표 세 줄이 들어 있다 |
| `styles.css` | `.card`·`nav` flex·`@media`가 주석 | 규칙 세 개가 들어 있다. `body.dark`는 두 파일 모두에 미리 있다 |
| `app.js` | 변수 일곱 개와 주석 네 줄 | `click` 두 개와 `submit` 하나가 들어 있다 |

두 폴더 모두 브라우저에서 열었을 때 Console에 빨간 줄이 없다. starter는 `리허설 starter 준비 완료`, solution은 `리허설 해답 준비 완료` 한 줄만 찍힌다.
이 한 줄이 보이면 `app.js`가 연결된 것이다.

## 공식 참고 자료

- [HTML 표 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [CSS 미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
- [Event.preventDefault() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Event/preventDefault)
