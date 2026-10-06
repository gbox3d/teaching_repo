# 주차별 강의 자료

## 운영 기준

- 15주, 주 2회 × 90분
- 매 수업: 설명·시연 30분 + 직접 해결 실습 60분
- 주당 합계: 설명·시연 60분 + 실습 120분
- 1주차는 연습용 폴더 `week01`에서 로컬 Git을, 2주차는 GitHub 저장소 `my-web`과 Pages 등록을 배운다. **Git 설명은 2주차까지다.** 3주차는 `my-web`을 이어 쓰고, **4주차부터는 매주 새 저장소 `web-weekNN`을 만들어 올린다**(아래 실습 루틴).
- 매주 시작점은 지난주 완성본이다(4주차부터 `examples/day2/build/`, 그 전은 `examples/day2/`). 자기 코드로 이어 가도 되고, 막히면 교재의 지난주 완성본을 받아 이어 간다.
- **매주 캡처 1장으로 끝난다.** 그 캡처가 README "완료 기준"의 화면이고 주차별 실습 점수의 근거다. 산출물이 보고서·표여서는 안 된다.
- 주차별 실습 점수는 1~7주·10~13주 캡처로 산정한다(2주차는 고정본의 캡처 4장). 8·9·14·15주는 실습 점수 대상이 아니다.
- 고정 평가 주: 8주 중간 개인 실기, 9주 1차 과제 발표, 14주 최종 프로젝트 발표, 15주 기말 개인 실기. 두 실기는 그때까지의 실습 제출로 만든 문제 은행에서 낸다(8주 1~7주, 15주 1~14주 누적).
- 기본 문제를 먼저 완성하고 남는 시간에 확장 문제를 수행한다.

시험과 발표 주차는 대학 일정과 분반 인원에 따라 실제 평가 시간이 달라질 수 있다. 공개 자료에는 평가 구조와 연습 절차만 두며, 학기별 실제 문항·정답·학생 정보는 별도 비공개 공간에서 관리한다.

## 실습 루틴 (3주차부터)

Git 은 **2주차까지만 설명한다**(GitHub Pages 등록까지). 3주차부터는 Git 설명 없이 웹에 집중하고, 아래 올리기 순서만 따른다. 명령의 뜻은 2주차에 배웠다.
**매주 새 저장소를 만든다.** 이름은 `web-week04`, `web-week05` … 이고, 공개 주소는 `https://<아이디>.github.io/web-week05/`이다(3주차까지는 `my-web`).

```text
web-week05/
  index.html  about.html  guestbook.html  styles.css  app.js  images/   ← 이번 주 만들기. 지난주 완성본에서 시작
  ex/                                                                  ← 비교 파일(값을 바꿔 보는 실험)
  server.mjs                                                           ← 정적 서버(5주차부터)
```

**1일차 시작 0–5분** — 새 폴더 `web-weekNN`을 VS Code로 연다. 지난주 완성본을 넣는다: 내 지난주 저장소 GitHub 화면 **Code › Download ZIP**, 또는 교재의 지난주 `examples/day2/build/`. `ex/` 폴더에 오늘 비교 파일(교재 `examples/day1/`)을 **Raw**로 저장한다. 내 저장소의 `ex/`에는 날짜 폴더 없이 그 주 비교 파일을 모두 모은다.

**1일차 끝 50–60분** — GitHub에서 새 저장소 `web-weekNN`을 만든다(Public, README 추가하지 않음). 터미널에서:

```bash
git init
git add .
git commit -m "5주차 1일차"
git branch -M main
git remote add origin https://github.com/<아이디>/web-week05.git
git push -u origin main
```

그다음 저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 공개 주소를 연다.

**2일차 시작 0–5분** — 같은 PC에 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/<아이디>/web-weekNN.git` 뒤 **File › Open Folder**.

**2일차 끝 55–60분** — `git add .` → `git commit -m "…"` → `git push` → 공개 주소 새로고침·캡처.

**공용 PC**는 매 실습 끝에 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거한다.

**Pages 반영 지연 규칙** — 각 주 `lab.md` "막혔을 때" 표의 첫 줄에 둔다.

- 공개 페이지 반영이 1~3분 늦는다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정하고, 다음 수업 시작 5분에 Pages 확인을 허용한다.
- **11주차부터 확인·캡처는 공개 URL에서만 한다.** `localStorage`는 주소(origin)마다 따로 저장되므로 "새로고침해도 남는다"는 캡처하는 그 주소에서 확인한다. 12주차 `fetch`도 공개 URL이 기준이다.
- push 가 거부되거나 로그인 창이 안 뜨면 [2주차 막혔을 때 표](week02_github_pages/lab.md)를 본다.

**정적 서버** — [`../tools/static-server/`](../tools/static-server/README.md)의 `server.mjs` 한 파일을 그 주 폴더에 두고 `node server.mjs` → `http://localhost:8000/`. 5주차 2일차에 처음 설명하고, `fetch`(12주차)처럼 `file://`로 안 되는 기능을 공개 주소와 같은 조건으로 미리 본다. Node가 없는 PC는 파일을 두 번 눌러 열거나 push 뒤 공개 주소로 확인한다.

## 주차 폴더 구성

각 폴더는 같은 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 첫 줄에 실습 페이지 링크. 이번 주 질문 · 학습 목표 · 결과물(캡처 예) / 2일 수업 흐름 · 준비 / **이번 주 용어**(한국어 · English · 中文) · 이번 주 범위 / 수업 자료(덱 주소) / 완료 기준(캡처 1장) · 다음 수업 연결 · 공식 참고 자료 |
| `slides.md` | Marp 원고. `---`가 슬라이드 구분자. 일차마다 설명 30분을 `N일차 · A–B분 — 제목` 구간으로 나누고 일차 끝에 설명 합계를 적는다. 슬라이드 한 장은 비어 있지 않은 줄 16줄 이하, 태그·명령·속성·GitHub 화면 이름은 영문 원어를 그대로 쓴다 |
| `walkthrough.md` | 처음부터 그대로 따라 하는 단계(할 일 → 예상 결과). 명령 앞에 "현재 폴더"를 적는다. 만들기 파일(`build/`, 3주차까지는 `dayN/`)의 전체 코드 블록은 예제 파일과 글자 단위로 같다 |
| `lab.md` | 실습 페이지 링크, 일차별 60분 시간표(`A–B분` 표기, 3주차부터 0–5 시작 루틴·55–60 끝 루틴, 마지막 구간이 60분에서 끝난다), 단계별 문제와 힌트, 막혔을 때 표(첫 줄 Pages 지연 규칙, 나머지는 실제로 재현한 오류 문구), 제출물(캡처 1장), 먼저 끝났다면 |
| `examples/README.md` | 비교 파일 표(열면 보이는 것 · 보여 주는 원리 · 바꿔 볼 값)와 조립표(만들기 파일의 줄이 어느 비교 파일에서 왔나) |
| `examples/day1/` · `examples/day2/` | 그날 쓰는 예제. `examples/` 바로 아래에는 `README.md`와 이 두 폴더만 둔다(8·15주는 문제 은행 — 아래 시험·과제 주차) |

`examples/dayN/`의 규칙은 다음과 같다.

- 4주차부터 `dayN/exNN_*.html`은 **비교 파일**이다. 파일 하나 = 개념 하나이고, 값 하나만 다른 형제를 나란히 둔다. 번호는 한 주 안에서 이어 센다(1일차 ex01부터, 2일차는 그다음 번호부터). `<style>`·`<script>`가 파일 안에 있고, 보조 파일이 필요하면 같은 폴더에 같은 번호로 둔다.
- 만들기는 마지막 하나, `day2/build/`뿐이다. 2일차 끝의 `web-weekNN` 저장소 맨 위 전체이고 다음 주의 시작점이다.
- 3주차까지는 `dayN/`이 그날 수업이 끝났을 때의 **`my-web` 전체 파일**이다(그 주에 바뀌지 않은 파일도 포함).
- 만들기 파일은 하나에 60줄 이하로 두고, 학생이 직접 타이핑할 수 있는 크기를 넘지 않는다. 클래식 `<script src="app.js" defer>`만 쓰고(CDN·라이브러리·`type="module"` 없음), 페이지마다 자기 `.js` 파일 하나를 연결한다.
- 모든 `dayN/index.html`(4주차부터는 `day2/build/index.html`)은 브라우저 Console 오류 0으로 열린다. 비교 파일의 오류는 주석을 풀거나 버튼을 눌러 일부러 낼 때만 난다.

시험·과제 주차는 같은 파일 세트에 다음을 더한다. 이 네 주차도 `README.md`·`slides.md`·`walkthrough.md`·`lab.md`는 똑같이 두며, `lab.md`에는 1일차 시간표(8·15주는 문제 은행 연습, 9·14주는 발표 준비)와 2일차 시험·발표 운영 시간표 2개를 둔다.
8·15주 `examples/`에는 날짜 폴더 대신 은행 목록 `README.md`와 문제 폴더 `wNN_*`를 둔다. 문제 하나는 한 주의 실습 제출이고, 시험은 같은 문제를 값만 바꿔 낸다. 해답은 공개하지 않는다.

| 주차 | 추가 파일 |
|---:|---|
| 8 | `exam_structure.md`, `rubric.md`, `examples/README.md`(1~7주 문제 은행 목록), `examples/w01_*`~`w07_*`(문제 폴더) |
| 9 | `project_brief.md`, `rubric.md` |
| 14 | `project_brief.md`, `rubric.md`, `demo_outline.md` |
| 15 | `rubric.md`, `examples/README.md`(1~14주 누적 문제 은행 목록), `examples/w09_*`~`w14_*`(문제 폴더. 1~7주 문제는 8주 폴더의 것을 함께 쓴다) |

PT 원고는 내용 변경 이력을 추적하기 위해 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다.

## 주차 목록

| 주차 | 주제 | 이번 주 결과물 | 폴더 |
|---:|---|---|---|
| 1 | 웹 실행 구조와 Git 상태 | 연습 폴더 `week01`의 `index.html` 화면과 `git log --oneline` 3줄 | [`week01_web_git`](week01_web_git/) |
| 2 | GitHub와 공개 배포 | `my-web` push · Pages 공개 URL · `about` 브랜치와 merge (캡처 4장) | [`week02_github_pages`](week02_github_pages/) |
| 3 | 시맨틱 HTML과 form | 공개 URL의 `guestbook.html` 폼과 세 페이지 nav | [`week03_semantic_html`](week03_semantic_html/) |
| 4 | CSS와 반응형 UI | 기기 모드 375px에서 nav가 세로로 접히는 꾸민 `index.html` | [`week04_responsive_css`](week04_responsive_css/) |
| 5 | JavaScript 데이터와 함수 | 함수가 만든 인사말이 페이지에 보이고 Console에 값이 찍힌 화면 | [`week05_javascript_data`](week05_javascript_data/) |
| 6 | DOM·이벤트·브라우저 CRUD | [다크 모드]로 배경이 바뀌고 "클릭 N회"가 표시된 `index.html` | [`week06_dom_crud`](week06_dom_crud/) |
| 7 | 폼 입력 읽기와 결과 표시 | 이름·메시지를 넣고 [남기기]를 누르면 아래에 한 줄이 표시되는 `guestbook.html` | [`week07_async_modules`](week07_async_modules/) |
| 8 | 중간 개인 실기 | 1일차 [1~7주 문제 은행](week08_midterm/examples/README.md) 연습, 2일차 중간 실기 — `web-week08/exam/` 공개 주소 · 저장소 주소 · Commits 탭 캡처 | [`week08_midterm`](week08_midterm/) |
| 9 | 1차 과제 발표와 브랜치 복습 | 2분 시연과 저장소 `README.md` 1차판 | [`week09_architecture_project`](week09_architecture_project/) |
| 10 | 배열 데이터를 목록으로 그리기 | 항목 3개를 쌓고 1개를 지운 뒤 "2개"가 표시된 방명록 | [`week10_supabase_data`](week10_supabase_data/) |
| 11 | 객체와 localStorage | 새로고침해도 남는 방명록 3개와 Application › Local Storage의 `guestbook` 키 | [`week11_auth_rls`](week11_auth_rls/) |
| 12 | fetch로 JSON 불러오기 | JSON에서 읽은 카드 3개와 Network 탭의 `projects.json` 200 | [`week12_persistent_crud`](week12_persistent_crud/) |
| 13 | 보안·접근성·릴리스 점검 | 태그를 입력해도 글자 그대로 보이고 Console 오류가 0인 375px 화면 | [`week13_release_security`](week13_release_security/) |
| 14 | 최종 프로젝트 발표 | 3분 시연과 README 최종판 | [`week14_project_presentation`](week14_project_presentation/) |
| 15 | 기말 개인 실기 | 1일차 [1~14주 누적 문제 은행](week15_final_exam/examples/README.md) 연습, 2일차 기말 실기 — `web-week15/exam/` 공개 주소 · 저장소 주소 · Commits 탭 캡처 | [`week15_final_exam`](week15_final_exam/) |

폴더 이름은 이미 배포된 슬라이드 주소(`.../webprg/decks/<폴더명>/`)를 깨뜨리지 않기 위해 그대로 둔다. 주차의 실제 주제는 위 표의 제목을 따른다.

## 자료 작성 원칙

- **학생 기준선**: 프로그래밍 경험이 거의 없는 대학생이다. 1주차에 URL·요청과 응답·HTML/CSS/JS의 역할·DevTools와 로컬 `git init → add → commit`, 2주차에 GitHub 저장소 `my-web`·push·Pages·브랜치와 merge까지 배웠다. 그 밖의 것은 모른다고 전제한다.
- **기준 자료 우선순위**: (1) 강의자 판서와 Git·GitHub 슬라이드 → (2) 수업계획서의 15주 헤드라인과 평가 배점 → (3) MDN 입문 순서(HTML → CSS → JavaScript → DOM → 폼 → 저장 → fetch). 순서·용어·API는 이 셋과 같게 쓴다.
- **한 주 새 개념은 3~5개**다. 앞 주에서 배운 것만 전제하고 난이도가 한 주에 두 단계 뛰지 않는다. "오늘 문법 5분"이나 복붙 틀로 처리하는 항목은 개념 수에서 빼되 슬라이드 1장으로 제한한다. 3주차부터의 올리기 순서(add·commit·push)는 설명하지 않는 루틴이므로 개념 수에 넣지 않는다.
- **매주 캡처 1장으로 보여 줄 웹페이지·동작 하나로 끝난다.** 1일차 중간 화면은 `lab.md`에 "확인용"으로만 둔다.
- `slides.md`에는 설명 30분 분량의 핵심만 두고 긴 설명은 강의 대본(비공개)으로 분리한다.
- 예제는 한 번에 한 개념만 보여 주는 최소 코드로 만든다.
- `lab.md`에는 정답 전체 대신 완료 조건과 단계별 힌트를 둔다. "막혔을 때" 항목은 실제로 재현해 본 Console·터미널 문구를 그대로 적는다.
- **표준 API·표준 용어만 쓴다**: `document.querySelector`, `textContent`, `addEventListener`, `classList`, `createElement`/`append`, `localStorage`, `JSON`, `fetch`/`await`. 클릭·제출 리스너 안에서 화면을 직접 바꾼다. 목록을 다시 그리는 함수 이름은 `showList()`로 통일한다.
- **학기 범위 밖**: 번들러, npm 패키지, 서버 DB·로그인, 화살표 함수, `map`·`filter`·`forEach`, 클래스, 구조 분해, spread, `git rebase`. 필요하면 "이 과목 범위 밖" 한 줄로만 말한다.
- 표준 입문 교재에 없는 설계 틀과 용어는 들여오지 않는다. 금지 목록은 강의자 설계 문서가 관리하며, 주차 검사 스크립트가 공개·비공개 문서를 모두 검사한다.
- **문법·API는 한 주에 몰아넣지 않고 쓰는 주에 5분**으로 도입한다.

| 문법·API | 처음 쓰는 주 | 형태 |
|---|---|---|
| `<script src="app.js" defer>`, `console.log`, Console 오류 줄(파일:줄) 읽기 | 5주 1일차 | 정식 항목 |
| `let`·`const`, 숫자·문자열, 템플릿 문자열 `` `${}` `` | 5주 1일차 | 정식 항목 |
| `if / else`, 비교 `===`·`>=`, `function` 정의·호출·`return` | 5주 2일차 | 정식 항목 |
| `document.querySelector('#greeting').textContent = …` | 5주 2일차 | 정식 항목(ex09) |
| `addEventListener('click', function () { })` | 6주 1일차 | 정식 항목 |
| `classList.add / remove / toggle` | 6주 2일차 | 정식 항목 |
| `addEventListener('submit', function (event) { })`, `event.preventDefault()`, `input.value`, `trim()` | 7주 1일차 | 정식 항목 |
| `focus()`, `form.reset()`, `if` 안의 `return` | 7주 1일차 | 오늘 문법 5분 |
| 배열 `[ ]`·`push`·`length`·`[i]`·고전 `for` | 10주 1일차 | 오늘 문법 5분(정식 도입) |
| `createElement`·`textContent`·`append`, `innerHTML = ''`(비우기 전용) | 10주 1·2일차 | 정식 항목 |
| `splice(i, 1)` | 10주 2일차 | 복붙 틀(삭제 버튼 틀 안) |
| 객체 `{ name: …, message: …, date: … }`, 점 표기 | 11주 1일차 | 오늘 문법 5분 |
| `JSON.stringify` / `JSON.parse`, `localStorage.setItem / getItem / removeItem` | 11주 2일차 | 정식 항목 |
| `async function`·`await fetch(url)`·`await response.json()` | 12주 1일차 | 복붙 틀 |
| `try / catch`, `response.ok` | 12주 2일차 | 정식 항목 |
| `Number()`, `isNaN()`, `new Date().getFullYear()` | 13주 1일차 | 오늘 문법 5분 |

- **개인정보**: 예시 아이디는 `student01`, 이메일은 `student01@example.com`, 저장소는 3주차까지 `my-web`, 4주차부터 `web-week04`·`web-week05`…, 공개 주소는 `https://student01.github.io/web-week05/`이다. 공개 저장소·캡처·예제에 실명·학번·전화번호·실제 이메일을 넣지 않는다.
- 시험 주(8·15주) 폴더에는 문제 은행(문제 문장·시작 파일)과 채점표만 두고, 시험에 내는 값과 해답은 별도 비공개 공간에서 관리한다.

## README "이번 주 용어" 표

모든 주차 README의 "이번 주 용어" 절에 한국어 · English · 中文 3열 표를 5~8행 둔다. 그 주에 처음 나오는 말만 넣고, 다음 주부터는 새로 나온 말로 갈아 끼운다. 본문에서도 태그·명령·속성·GitHub 화면 이름은 영문 원어를 그대로 쓴다.

```markdown
## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 요소 | element | 元素 |
| 속성 | attribute | 属性 |
| 선택자 | selector | 选择器 |
| 이벤트 | event | 事件 |
| 저장소 | repository | 仓库 |
| 올리기 | push | 推送 |
```

실제 예는 [2주차 README](week02_github_pages/README.md#이번-주-용어)에 있다.

## 실습 페이지 링크 규칙

- `README.md` 첫 줄, `lab.md` 본문, `slides.md`의 실습 인계 슬라이드에 절대 주소를 넣는다.
  `https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/<폴더명>`
- `README.md`에는 덱 주소도 적는다.
  `https://gbox3d.github.io/teaching_repo/webprg/decks/<폴더명>/index.html`
- `slides.md`에서 `lab.md`·`walkthrough.md`로 가는 링크는 상대 링크로 쓴다. 사이트 빌드가 GitHub blob 주소로 바꿔 준다.

## 공식 참고 자료

- [MDN 웹 개발 학습하기](https://developer.mozilla.org/ko/docs/Learn_web_development)
- [MDN HTML](https://developer.mozilla.org/ko/docs/Web/HTML) · [MDN CSS](https://developer.mozilla.org/ko/docs/Web/CSS) · [MDN JavaScript](https://developer.mozilla.org/ko/docs/Web/JavaScript)
- [GitHub Pages 문서](https://docs.github.com/ko/pages)
- [Git 공식 문서](https://git-scm.com/doc)
