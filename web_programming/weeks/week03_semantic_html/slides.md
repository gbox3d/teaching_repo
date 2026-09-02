---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 3주차"
footer: "시맨틱 HTML과 form"
---

# 3주차
## 시맨틱 HTML과 form

CSS 없이도 의미와 사용 순서가 드러나는 화면을 만든다.

---

## 의미를 먼저 만드는 이유

- 브라우저가 일관된 기본 동작을 제공한다.
- 키보드와 보조기술이 구조를 탐색할 수 있다.
- 검색·읽기 도구가 콘텐츠 관계를 해석한다.
- CSS와 JavaScript를 바꾸어도 구조 계약이 남는다.

**시맨틱 HTML은 태그 이름 맞히기가 아니라 관계를 표현하는 일이다.**

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## 문서 구조와 올바른 동작 요소

---

## 0–5분 · 페이지의 뼈대

```html
<header>사이트 소개</header>
<nav aria-label="주요 메뉴">...</nav>
<main>
  <h1>이 페이지의 제목</h1>
  <section>...</section>
</main>
<footer>문서 정보</footer>
```

landmark는 화면 사각형이 아니라 탐색 가능한 큰 영역이다.

---

## 5–10분 · heading은 문서 목차

```text
h1 캠퍼스 활동
 ├─ h2 이번 주 활동
 │   ├─ h3 사진 산책
 │   └─ h3 알고리즘 모임
 └─ h2 이용 안내
```

- 글자 크기를 위해 level을 고르지 않는다.
- 하위 내용을 열 때 한 단계씩 내려간다.
- 페이지마다 목적이 분명한 `h1`을 둔다.

---

## 10–15분 · section과 article

- `section`: 한 주제로 묶이며 보통 heading이 있는 영역
- `article`: 따로 배포·재사용해도 이해되는 독립 항목
- `div`: 의미 계약 없이 styling·grouping이 필요할 때

모든 `div`를 `section`으로 바꾸는 것은 semantic이 아니다.

---

## 15–20분 · link와 button

| 사용자 기대 | 요소 |
|---|---|
| 다른 URL·문서로 이동 | `<a href="...">` |
| 현재 화면에서 실행·상태 변경 | `<button type="button">` |
| form 제출 | `<button type="submit">` |

CSS 모양이 아니라 **활성화 뒤 일어나는 일**로 선택한다.

---

## 20–25분 · accessible name

사용자는 컨트롤의 이름을 알아야 한다.

```html
<a href="detail.html">사진 산책 자세히 보기</a>
<button type="button">즐겨찾기 추가</button>
```

`자세히`, `클릭`처럼 맥락 밖에서 모호한 이름을 반복하지 않는다.

---

## 25–30분 · 키보드로 구조 시험

1. 주소창부터 `Tab`으로 이동
2. focus 순서와 보이는 이름 말하기
3. link는 `Enter`, button은 `Enter`/`Space`
4. `Shift+Tab`으로 역방향 확인

DOM 순서를 CSS로 뒤집어도 focus 순서는 자동으로 바뀌지 않는다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## form, 네이티브 검증, 데이터 표

---

## 0–5분 · form은 입력 계약

```html
<form action="confirmation.html" method="get">
  ...
  <button type="submit">활동 등록</button>
</form>
```

- `action`: 제출 대상
- `method`: 전달 방식
- `name`: 제출 데이터의 key
- button type을 명시해 의도를 고정한다.

---

## 5–10분 · label은 placeholder가 아니다

```html
<label for="title">활동 이름</label>
<input id="title" name="title" required>
```

- `for`와 `id`를 정확히 연결
- label 클릭 시 input focus 확인
- placeholder는 예시일 뿐 이름을 대체하지 않음

---

## 10–15분 · 목적에 맞는 input type

```html
<input type="email" autocomplete="email">
<input type="date">
<input type="number" min="1" max="20">
```

적절한 type은 모바일 키보드, 브라우저 UI, 기본 검증을 함께 제공한다.

---

## 15–20분 · 네이티브 constraint validation

```html
<input
  name="code"
  required
  minlength="4"
  maxlength="12"
  pattern="[A-Za-z0-9-]+"
>
```

테스트할 입력:

- 빈 값
- 최소보다 1 짧음
- 허용하지 않은 문자
- 최소/최대 경계
- 정상 값

---

## 20–24분 · 관련 입력은 fieldset

```html
<fieldset>
  <legend>연락 방법</legend>
  <label><input type="radio" name="contact" value="email"> 이메일</label>
  <label><input type="radio" name="contact" value="none"> 연락하지 않음</label>
</fieldset>
```

`legend`는 여러 control이 공유하는 질문이다.

---

## 24–27분 · table은 2차원 데이터

```html
<table>
  <caption>이번 주 활동 일정</caption>
  <thead><tr><th scope="col">활동</th>...</tr></thead>
  <tbody>...</tbody>
</table>
```

레이아웃을 맞추기 위한 table은 사용하지 않는다.

---

## 27–30분 · 이미지 대체 텍스트

- 정보 이미지: 맥락에서 필요한 정보를 `alt`로
- 장식 이미지: `alt=""`
- 주변 텍스트와 같은 내용을 장황하게 반복하지 않음
- 파일명이나 “이미지”라는 말만 쓰지 않음

**질문:** 같은 이미지라도 페이지 맥락이 바뀌면 alt가 달라질 수 있는가?

---

## 정리

```text
문서: landmark → heading → 독립 콘텐츠
동작: 이동은 link, 실행은 button
입력: label + type + constraint + 상태 검증
점검: mouse 없이 전체 흐름 수행
```
