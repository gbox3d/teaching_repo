# 3주차 — 시맨틱 HTML과 form

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

## 이번 주 질문

> 2주차에 공개한 `my-web`을 홈·내 정보·방명록 세 페이지로 늘리고, 이름과 메시지를 적는 입력 칸까지 만들 수 있을까?

2주차에는 `my-web`을 GitHub에 올리고 공개 주소를 만들었다. 페이지는 카드 한 장이었다.
이번 주에는 그 `index.html`을 자기소개 페이지로 다시 쓰고, `about.html`을 내 정보 표로 바꾸고, `guestbook.html`을 새로 만든다.
이번 주는 HTML만 쓴다. `styles.css`와 `app.js`는 폴더에 그대로 두고 연결만 뺀다. 꾸미기는 4주차, 동작은 5주차다.

## 학습 목표

1. `header`·`nav`·`main`·`footer`로 문서 뼈대를 나눈다.
2. `h1`~`h3`로 제목 단계를 만들고 `p`·`strong`으로 문단을 쓴다.
3. `a href`에 상대 경로를 적어 세 페이지를 오가고, `img src`·`alt`로 `images/profile.png`를 넣는다.
4. `ul`·`ol`·`li`로 목록을, `table`·`tr`·`th`·`td`로 2열 표를 만든다.
5. `form`·`label for`·`input type="text"`·`input type="email"`·`textarea`·`button type="submit"`으로 입력 칸을 만든다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/guestbook.html
         메뉴에 홈 · 내 정보 · 방명록 세 링크
         이름 · 이메일 · 메시지 입력 칸과 [남기기] 버튼
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 시작·끝 루틴, `header`·`nav`·`main`·`footer`, 제목과 문단, 링크와 그림, 목록 | `index.html`을 자기소개 페이지로 다시 쓰기 → 그림·링크·취미 목록 | 확인용 화면 |
| 2일차 | `table`, `form`과 `label`·`input`·`textarea`, `button type="submit"`, `guestbook` 브랜치 | `about.html` 표 → `guestbook.html` 폼 → nav 통일 → merge → push | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 2주차에 만든 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 수업용 그림 [examples/day1/images/profile.png](examples/day1/images/profile.png)를 내려받아 `my-web/images/`에 넣는다 ([따라하기 4단계](walkthrough.md#4-프로필-그림과-nav-링크-넣기))
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 시맨틱 태그 | semantic element | 语义化标签 |
| 머리말 · 꼬리말 | header · footer | 页眉 · 页脚 |
| 길잡이 메뉴 | nav (navigation) | 导航 |
| 제목 단계 | heading (h1–h3) | 标题层级 |
| 상대 경로 | relative path | 相对路径 |
| 대체 텍스트 | alt text | 替代文本 |
| 목록 · 표 | list · table | 列表 · 表格 |
| 입력 양식 · 이름표 | form · label | 表单 · 标签 |

## 이번 주 범위

| 태그·명령 | 이번 주에 알아둘 뜻 |
|---|---|
| `<header>` | 페이지 맨 위의 소개 영역. 제목과 메뉴를 담는다 |
| `<nav>` | 페이지를 오가는 링크 묶음. `header` 안에 둔다 |
| `<main>` | 그 페이지의 본문. 한 페이지에 하나 |
| `<footer>` | 페이지 맨 아래의 마무리 줄 |
| `<h1>` · `<h2>` · `<h3>` | 제목 단계. `h1`은 페이지에 하나, 그 아래 묶음이 `h2`, 그 안이 `h3` |
| `<p>` · `<strong>` | 문단 / 문단 안에서 중요한 말 |
| `<a href="about.html">` | 같은 폴더의 파일로 이동한다(상대 경로). 파일 이름만 적는다 |
| `<img src="images/profile.png" alt="…">` | 그림을 넣는다. `alt`는 그림이 안 보일 때 대신 읽히는 글 |
| `width="160"` | 그림 너비를 픽셀로 정한다. 4주차에 CSS로 옮긴다 |
| `<ul>` · `<ol>` · `<li>` | 순서 없는 목록 / 순서 있는 목록 / 목록 한 줄 |
| `<table>` · `<tr>` · `<th>` · `<td>` | 표 / 표의 한 줄 / 제목 칸 / 내용 칸 |
| `<form>` | 입력 칸을 묶는 영역 |
| `<label for="name">` | 입력 칸의 이름표. `for`와 `input`의 `id`가 같아야 이름표를 눌러 커서가 들어간다 |
| `<input type="text">` · `<input type="email">` | 한 줄 입력 칸 / 이메일용 입력 칸 |
| `<textarea rows="4">` | 여러 줄 입력 칸 |
| `<button type="submit">` | form을 제출하는 버튼 |
| `git switch -c guestbook` | 브랜치를 만들면서 바로 옮겨 간다. 2주차 `git branch` + `git switch`를 한 줄로 |

`section`·`article`·`div`, `aria-*` 속성, `required` 같은 입력 검사, CSS·JavaScript 연결은 이번 주에 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week03_semantic_html/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [styles.css](examples/day1/styles.css) · [app.js](examples/day1/app.js) · [images/profile.png](examples/day1/images/profile.png)
- 2일차 완성 코드: [index.html](examples/day2/index.html) · [about.html](examples/day2/about.html) · [guestbook.html](examples/day2/guestbook.html)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`이 열린다.
- [ ] 세 페이지 어디서나 메뉴의 `홈`·`내 정보`·`방명록`으로 오갈 수 있다.
- [ ] `index.html`에 프로필 그림(`alt` 포함)과 취미 목록이 보인다.
- [ ] `about.html`에 2열 4행 표가 보인다.
- [ ] `guestbook.html`에 이름·이메일·메시지 입력 칸과 **남기기** 버튼이 보인다.
- [ ] 주소창이 함께 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

이번 주에 만든 것은 꾸미지 않은 화면이다. 4주차에는 `styles.css`를 비우고 다시 써서 세 페이지에 연결하고,
색·박스·`display: flex`·`@media`로 이 세 페이지를 꾸민다. 오늘 만든 `header`·`nav`·`main`·`footer`·`ul`·`table`이
그대로 4주차 CSS의 대상이 된다. 결과는 같은 공개 주소 `https://<아이디>.github.io/my-web/`에서 확인한다.

## 공식 참고 자료

- [HTML 기초 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Your_first_website/Creating_the_content)
- [HTML 문서와 웹사이트 구조 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)
- [HTML 텍스트 기초 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/Headings_and_paragraphs)
- [하이퍼링크 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/Creating_links)
- [HTML 이미지 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_images)
- [HTML 표 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [첫 HTML 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
