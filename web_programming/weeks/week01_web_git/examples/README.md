# 1주차 예제 — 세 파일로 만든 작은 페이지

1일차 제공본과 2일차 완성 기준 파일이다. 각 차시는 강의·시연 60분과 개별 실습 30분이며, [실습지](../lab.md)의 필수 수정만 수행한다. 전체 코드를 타이핑하지 않는다.
파일은 브라우저로 **더블클릭해서** 연다(`file://` 주소). 이번 주에는 서버를 켜지 않는다.
`student01`은 예시 별칭이다. 본인 수업용 별칭으로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [2단계](../walkthrough.md#2-세-파일-만들기)에서 복사하고, [5단계](../walkthrough.md#5-내-소개로-고치고-저장하기)에서 제목·소개를 변경한다 | `week01/index.html` |
| [day1/styles.css](day1/styles.css) | [2단계](../walkthrough.md#2-세-파일-만들기)에서 복사하고 5단계에서 `body` 배경색 한 곳을 변경한다 | `week01/styles.css` |
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

`<h1>`과 소개 문단은 본인 소개로, `styles.css`의 `body` 배경색은 다른 값으로 바꾼다. 이 세 곳이 1일차 필수 수정이다. CSS의 나머지 부분과 `app.js`는 제공 코드다.

`.card`의 `box-sizing: border-box`는 지정한 너비 안에 안쪽 여백을 포함해 좁은 화면에서도 카드가 넘치지 않게 한다. 이 줄은 제공 상태로 두며 박스 모델은 4주차에 배운다. CSS 파일명 오류와 Elements·Console 관찰은 강의자 시연, 직접 재현은 선택이다.

## 2. 2일차 완성 — 연습 페이지와 commit 세 개

`day2/`는 `week01-practice` 폴더의 마지막 모습이다. 저장소의 `styles.css`와 `app.js`는 day1과 같다. 학생은 1일차에 색을 변경한 자신의 CSS와 제공 JS를 복사한다. HTML 조각을 제공받아 붙여 넣되 세 단계의 Git 기록은 직접 남긴다.

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

## 다음 주로 넘길 파일

`week01`의 소개 페이지와 `week01-practice`의 세 commit을 보관한다. 2주차에는 새 `my-web` 저장소에서 제공 파일을 GitHub에 올린다. 기존 `.git` 폴더를 복사하지 않고 새 저장소의 로컬 작성자 설정을 다시 확인한다.

## 공식 참고 자료

- [첫 번째 웹사이트 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Your_first_website)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
