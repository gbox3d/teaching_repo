---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 7주차"
footer: "CSS 응용"
---

# CSS 응용

카드와 메뉴를 배치하고 방명록의 글을 최신순 피드로 보여 준다.

- 1일차: W3.CSS 클래스 조합, 카드·메뉴, 타임라인
- 2일차: 방명록에 피드 적용, 모바일에서 작성자·시각·본문 확인
- 매일 **강의·시연 60분 + 실습 30분**

폼 JS는 제공 코드를 읽고 실행한다. 입력 처리 흐름은 후속 수업에서도 사용한다.

---

# 1일차 W3.CSS 기본 화면

| 강의 시간 | 내용 |
|---|---|
| 0–10분 | CDN과 CSS 클래스 |
| 10–25분 | ex01 연결 전후 |
| 25–40분 | ex02 입력창과 버튼 |
| 40–47분 | ex03 카드와 모바일 메뉴 |
| 47–55분 | ex03b 타임라인과 글 사이 여백 |
| 55–60분 | 클래스·id와 실행 확인 |

이어서 30분 실습. 다운로드와 Git 준비는 수업 전에 마친다. 첫 10분의 앞 5분은 파일·서버 확인, 마지막 5분은 실습 안내에 쓴다.

---

## 1일차 0–10분 CDN으로 CSS 연결

W3.CSS는 미리 작성된 스타일을 클래스 이름으로 제공한다.

```html
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

- `<head>`에 버전이 고정된 CDN 주소를 연결한다.
- Network에서 Disable cache → 새로고침 → `w3.min.css`의 200 확인.
- 인터넷 연결이 필요하다. 라이브러리 사본은 저장소에 넣지 않는다.

[cdnjs W3.CSS](https://cdnjs.com/libraries/w3-css)

---

## 1일차 10–25분 ex01 연결 전후

[연결 전 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/before.html) · [연결 후 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/index.html) · [같은 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/app.js)

```html
<button id="button" class="w3-button w3-teal">클릭</button>
```

두 HTML의 버튼은 같은 클래스를 갖는다. CDN이 연결된 화면에 스타일이 적용된다.

1. 두 화면에서 버튼을 눌러 클릭 횟수를 확인한다.
2. 강의자가 연결 후 파일의 `w3-teal`을 `w3-blue`로 바꾼다. 학생 변경은 선택이다.
3. 색상과 클릭 동작을 함께 확인한다.

---

## 1일차 25–40분 ex02 입력창과 버튼

[HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex02/index.html) · [제공 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex02/app.js)

```html
<input id="name" class="w3-input w3-border" type="text">
<button class="w3-button w3-teal" type="submit">미리보기</button>
```

- `w3-input`: 입력창, `w3-border`: 테두리
- `w3-button`: 버튼, `w3-teal`: 색상
- 이름·메시지 입력 → 미리보기. 입력 칸의 글자는 유지된다.

버튼 색상 한 곳을 바꾸고 같은 결과가 표시되는지 확인한다.

---

## 1일차 40–47분 ex03 카드와 모바일 메뉴

[HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex03/index.html) · [설명](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex03/README.md)

| 클래스 | 적용 |
|---|---|
| `w3-container`, `w3-padding` | 내용 여백 |
| `w3-content`, `w3-card` | 내용 폭과 카드 모양 |
| `w3-bar`, `w3-bar-item`, `w3-button` | 메뉴와 항목 |
| `w3-mobile` | 600px 이하에서 항목을 세로 배치 |

375px와 1280px에서 메뉴를 비교한다. 두 카드는 항상 위아래로 놓인다. 입력 미리보기 JS는 ex02와 같다.

---

## 1일차 47–55분 글을 읽는 타임라인

[ex03b 타임라인 예제](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input/examples/day1/ex03b_list)

1. 아바타 옆에서 작성자와 시각을 찾고, 바로 아래 본문을 읽는다. 구분선을 경계로 다음 글이 시작된다.
2. 375px와 1280px에서 같은 글을 비교한다. 좁아지면 본문이 줄바꿈되고 작성자 정보는 해당 글에 붙어 있어야 한다.
3. `.post`의 `padding-block`을 `0.5rem`에서 `1rem`으로 바꾸고 글 사이 간격을 비교한다.

**55–60분 확인** · 배치를 바꾸는 `class`와 제공 JS가 찾는 `id`를 각각 한 곳 짚는다.

---

# 1일차 실습 30분

| 시간 | 할 일 |
|---|---|
| 0–5분 | ex01 CDN 연결 전후와 클릭 동작 |
| 5–10분 | ex02 버튼 색상 또는 입력 테두리 변경 |
| 10–15분 | ex03 메뉴·카드 변경 |
| 15–25분 | ex03b 글 사이 여백 변경, 375px·1280px 비교 |
| 25–30분 | CDN 응답 200과 Console 확인 |

[실습지](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/lab.md) · [따라하기](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/walkthrough.md)

넓은 화면과 좁은 화면에서 같은 글을 읽어 보고 줄바꿈 위치를 비교한다.

---

# 2일차 기존 방명록 화면 변환

| 강의 시간 | 내용 |
|---|---|
| 0–10분 | ex04 기존 방명록 실행 |
| 10–20분 | 제공 JS 처리 흐름 읽기 |
| 20–30분 | ex05 입력 폼 스타일 변환 |
| 30–40분 | 카드와 메뉴 변환 |
| 40–50분 | 같은 JS와 class·id 확인 |
| 50–60분 | 동작과 모바일 화면 검증 |

이어서 30분 실습. 변환 전 `guestbook.html`에서 시작한다. 첫 10분의 앞 5분은 준비 확인, 마지막 10분의 끝 5분은 실습·다음 수업 안내에 쓴다.

---

## 2일차 0–10분 ex04 동작하는 방명록

[변환 전 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/index.html) · [제공 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/app.js)

기존 CSS로 만든 화면에서 먼저 동작을 확인한다.

1. 이름을 비우고 제출: 안내, 목록 추가 없음.
2. 이름·메시지를 입력하고 제출: 목록에 한 항목 추가.
3. 다시 제출: 새 글이 맨 위에 보이고 앞 글은 그 아래에 남는다.
4. 제출 뒤 입력은 비고 이름 칸에 커서가 온다.

이 동작을 유지하면서 HTML의 연결과 클래스를 바꾼다.

---

## 2일차 10–20분 제공 JS 읽기

| 코드 | 화면 동작 |
|---|---|
| `submit` · `preventDefault()` | 제출을 받고 페이지 다시 열기 방지 |
| `.value.trim()` | 입력값 읽기, 앞뒤 공백 제거 |
| 빈값 검사 · `return` | 안내 후 목록 추가 전에 종료 |
| `textContent` · `prepend` | 작성자와 본문을 글자로 표시하고 새 글을 맨 위에 삽입 |
| `reset()` · `focus()` | 초기값 복원, 이름 칸으로 커서 이동 |
| `input` · `clearNotice` | 다시 입력하면 안내 제거 |

후속 수업에서 사용할 흐름이다. JS는 제공 코드를 유지한다.

---

## 2일차 20–30분 ex05 입력 폼 변환

[변환 후 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex05/index.html)

기존 `styles.css` 링크를 W3.CSS CDN으로 바꾼다.

| 대상 | 적용 클래스 |
|---|---|
| 이름·이메일·메시지 칸 | `w3-input w3-border` |
| 제출 버튼 | `w3-button w3-teal` |
| 안내 자리 `#notice` | `w3-text-red` |
| 목록 `#list` | `w3-ul example-output feed-list` 적용 |

`id`와 `guestbook.js` 연결은 유지한다. 이메일은 선택 입력이며 현재 JS는 읽지 않는다. 입력한 이메일 형식이 틀리면 브라우저가 제출을 막는다.

---

## 2일차 30–40분 카드와 메뉴 변환

메뉴를 header 바로 뒤로 옮긴다. 폼·안내와 목록을 각각 section으로 묶는다.

| 대상 | 적용 클래스 |
|---|---|
| 메뉴 | `w3-bar w3-white w3-card` |
| 메뉴 항목 | `w3-bar-item w3-button w3-mobile` |
| main | `w3-content w3-padding` |
| 두 section | `w3-container w3-card w3-white w3-margin-top` |

제목·버튼 색상 한 곳을 바꾼다. 나머지 매핑은 [따라하기](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/walkthrough.md)에 있다.

---

## 2일차 40–50분 같은 JS와 id 유지

[ex04 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/app.js) · [ex05 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex05/app.js) · [완성본 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.js)

VS Code에서 Select for Compare → Compare with Selected.
세 파일의 코드는 같다.

```text
JS가 찾는 id
guestbook-form · name · message · notice · list
```

스타일 클래스 변경 뒤에도 같은 요소를 찾는다. 홈·소개 페이지는 기존 CSS를 사용한다. `shared/examples.css`에서 `.post`의 Grid가 아바타와 글을 두 열에 배치한다. `.post-body`는 작성자가 넣은 줄바꿈을 보존한다.

---

## 2일차 50–60분 실행 검증

| 확인 | 기대 결과 |
|---|---|
| 빈 이름 또는 메시지 | 안내, 목록 추가 없음 |
| 글 두 건 등록 | 새 글이 맨 위, 작성자·시각·본문 표시, 입력 초기화 |
| 375px 화면 | 메뉴 세로 배치, 입력창 가로 넘침 없음 |
| Network · Console | CDN 200, 예제 코드 오류 없음 |

새로고침하면 목록이 사라진다. 저장 기능은 11주차에 다룬다.

강의 합계: **10 + 10 + 10 + 10 + 10 + 10 = 60분**

---

# 2일차 실습 30분

`guestbook.before.html`을 복사한 `guestbook.html`에서 작업한다.
완성본은 `guestbook.reference.html`로 보관해 대조한다.

| 시간 | 할 일 |
|---|---|
| 0–5분 | 기존 CSS 링크를 지정 CDN으로 교체 |
| 5–18분 | 매핑표로 클래스 적용, 색상 한 곳 변경 |
| 18–25분 | 빈값·두 건 등록·375px 확인 |
| 25–30분 | 실행 화면 캡처 |

[시작 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.before.html) · [대조 HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.html) · [실습지](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/lab.md)

---

## 제출 실행 화면 한 장

375px 화면에서 다음 항목이 보이게 캡처한다.

- 주소와 W3.CSS 방명록
- `student02`의 새 글이 `student01`의 글 위에 보이는 피드
- 변경한 버튼 또는 제목 색상

빈값 안내는 실습 중 확인한다. 별도 비교표나 코드 전문은 제출하지 않는다.
실명·학번·실제 이메일은 사용하지 않는다.

수업 뒤 push와 Pages 게시를 마치고 공개 주소에서 확인한다.

---

## 다음 수업과 참고 자료

- 8주차: [중간 실기 문제 은행](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm/examples). 분반 안내에서 출제 범위를 확인한다.
- 9주차: 시험 답안 대신 완성한 `web-week07` 웹 파일을 그대로 이어 쓴다.
- 10주차: 배열로 목록 관리. 11주차: 폼 한 건 저장·복원. 전체 저장 방명록은 제공 시연본이다.

[W3.CSS 입력창](https://www.w3schools.com/w3css/w3css_input.asp) · [컨테이너](https://www.w3schools.com/w3css/w3css_containers.asp) · [메뉴](https://www.w3schools.com/w3css/w3css_navigation.asp) · [cdnjs](https://cdnjs.com/libraries/w3-css)
