# 8주차 — 중간 개인 실기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

## 이번 주 질문

> 2~7주에 한 주씩 쌓아 온 것을, 문제지를 보고 **혼자 60분 안에** 만들어 공개 주소까지 올릴 수 있을까?

1일차에는 시험과 같은 모양의 **리허설**을 60분 동안 풀어 보고, 새 저장소를 만들어 GitHub Pages로 배포하는 절차까지 끝낸다.
2일차가 본시험이다. 본시험은 새 저장소를 만들지 않고, 이미 쓰고 있는 `my-web` 안에 `exam/` 폴더를 만들어 그 안에서 작업한 뒤 push한다.
저장소도 로그인도 Pages도 이미 살아 있으므로, 시험 시간에는 **만드는 일만** 한다.

## 학습 목표

1. 시험 범위(2~7주)와 채점표 20점의 항목을 읽고 무엇을 준비할지 정한다.
2. 리허설 starter의 문제 네 개(목록·표 / CSS / 버튼 / 폼)를 60분 안에 푼다.
3. 새 저장소를 만들어 Pages로 배포하는 절차를 **시험 전날인 1일차에** 끝낸다.
4. 본시험을 `my-web/exam/` 폴더에서 작업해 `git add → commit → push` 한다.
5. 제출물 네 가지(공개 URL · 저장소 URL · 마지막 commit SHA · 완성 화면 캡처 1장)를 만든다.

## 이번 주 결과물

```text
[제출 1] 공개 URL      https://student01.github.io/my-web/exam/
[제출 2] 저장소 URL    https://github.com/student01/my-web
[제출 3] 마지막 commit 1ea3c2e   ← git log -1 --oneline 의 앞 일곱 글자
[제출 4] 캡처 1장      완성 화면 + 주소창이 함께 보이게
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 이번 주는 주차별 실습 점수 대상이 아니라 **중간 20점**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 시험 범위와 채점표, 제출 형식과 60분 배분, `my-web/exam/` 규칙, 허용 자료·장애 대체 | 리허설 starter 문제 네 개 → 해답과 맞춰 보기 → 새 저장소 `midterm-practice` 만들어 push → Pages 켜기 | 리허설 공개 주소 |
| 2일차 | 시험 절차와 "제출본"의 뜻, 장애 대체, starter를 `exam/`에 복사해 실행 확인 | **본시험 60분** — 문제지를 보고 `my-web/exam/`에 만들어 push | 제출물 네 가지 |

각 수업은 `설명·함께 따라하기 30분 + 60분`이다. 2일차 60분은 연습이 아니라 **평가 시간**이다.

## 준비

- 2~7주에 쓰던 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 1일차에 쓸 리허설 파일: [examples/rehearsal_starter](examples/rehearsal_starter) 세 개를 내려받아 새 폴더에 넣는다
- 채점 기준을 미리 읽는다: [채점표](rubric.md) · [시험 구조](exam_structure.md)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 중간 실기 | midterm practical exam | 期中实操考试 |
| 리허설 | rehearsal | 预演 |
| 시작 코드 | starter | 起始代码 |
| 채점표 | rubric | 评分表 |
| 제출물 | submission | 提交物 |
| commit 식별자 | commit SHA | 提交编号 |
| 시험 작업 폴더 | exam folder | 考试文件夹 |
| 장애 대체 절차 | fallback procedure | 应急替代流程 |

## 이번 주 범위

시험에 나오는 것은 2~7주에 수업에서 쓴 것뿐이다. 아래 표 밖의 것은 쓰지 않아도 되고, 써도 점수가 오르지 않는다.

| 태그·명령·API | 이번 주에 쓰는 자리 | 배운 주 |
|---|---|---|
| `git add .` · `git commit -m` · `git push` | 시험 끝 5분과 리허설 저장소 | 2주 |
| **Settings › Pages** (`main` · `/(root)`) | 1일차 리허설 저장소에서 한 번 | 2주 |
| `header` · `nav` · `main` · `footer` · `h1`~`h3` · `p` | 문제 1의 뼈대 | 3주 |
| `ul` · `li` · `table` · `tr` · `th` · `td` | 문제 1 | 3주 |
| `form` · `label for` · `input` · `button type="submit"` | 문제 4 | 3주 |
| `.class` 선택자 · `color` · `background` · `padding` · `border` | 문제 2 | 4주 |
| `display: flex` · `gap` · `@media (max-width: 600px)` | 문제 2 | 4주 |
| `const` · `let` · 템플릿 문자열 `` `${}` `` · `if` · `function` | 문제 3·4 | 5주 |
| `document.querySelector('#id')` · `textContent` | 문제 3 | 6주 |
| `addEventListener('click', function () { })` · `classList.toggle` | 문제 3 | 6주 |
| `addEventListener('submit', …)` · `event.preventDefault()` · `input.value` · `trim()` · `focus()` | 문제 4 | 7주 |
| `git log -1 --oneline` | 제출할 commit SHA 확인 | 8주 |

**범위 밖**: 배열로 목록 그리기(10주), `localStorage`(11주), `fetch`·JSON(12주), ES Module·`import`/`export`, 외부 라이브러리·CDN.
범위 밖 기능을 넣어도 가점은 없다. 그 때문에 화면이 멈추면 감점이다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week08_midterm/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 시험 안내](lab.md)
- [시험 구조](exam_structure.md) · [채점표 20점](rubric.md)
- [예제 설명](examples/README.md)
- 리허설 문제: [index.html](examples/rehearsal_starter/index.html) · [styles.css](examples/rehearsal_starter/styles.css) · [app.js](examples/rehearsal_starter/app.js)
- 리허설 해답: [index.html](examples/rehearsal_solution/index.html) · [styles.css](examples/rehearsal_solution/styles.css) · [app.js](examples/rehearsal_solution/app.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

## 완료 기준

- [ ] 1일차: 리허설 저장소 `midterm-practice`가 GitHub에 있고 Pages 공개 주소가 열린다.
- [ ] 1일차: 리허설 문제 네 개를 어디까지 풀었는지 스스로 안다(해답과 맞춰 봤다).
- [ ] 2일차: `https://<아이디>.github.io/my-web/exam/`이 열리고 문제지가 요구한 화면이 보인다.
- [ ] 2일차: `my-web` 저장소의 `exam/` 폴더에 `index.html`·`styles.css`·`app.js`가 있다.
- [ ] 2일차: `git log -1 --oneline`의 commit SHA를 적어 제출했다.
- [ ] 2일차: 완성 화면과 주소창이 함께 보이는 캡처 1장을 제출했다.

## 다음 수업 연결

9주차는 **1차 과제 발표**다. 오늘 만든 `exam/` 폴더가 아니라 3~7주에 만든 `my-web` 본체(홈·내 정보·방명록 세 페이지 + CSS + 버튼 + 폼)를 2분 동안 시연하고,
저장소 `README.md`를 레포트로 제출한다. 브랜치 만들기·합치기·지우기도 그때 한 번 더 복습한다.

## 공식 참고 자료

- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub Pages 사이트에 대한 게시 원본 구성 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Git에서 GitHub 자격 증명 캐싱 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/caching-your-github-credentials-in-git)
- [HTML 표 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [첫 HTML 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [CSS 미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
