# 주차별 강의 자료

## 운영 기준

- 15주, 주 2회 × 90분
- 매 수업: 설명·시연 30분 + 직접 해결 실습 60분
- 주당 합계: 설명·시연 60분 + 실습 120분
- 저장소는 `my-web` 하나다. 1주차는 연습용 폴더 `week01`에서 로컬 Git만 다루고, 2주차에 만든 `my-web`에 15주까지 페이지를 쌓는다. 공개 주소는 `https://<아이디>.github.io/my-web/`이다.
- 매주 시작점은 전주 `examples/day2` 완성본(그 시점의 `my-web` 전체 파일)이다. 자기 코드로 이어 가도 되고, 막히면 전주 완성본을 받아 이어 간다.
- **매주 캡처 1장으로 끝난다.** 그 캡처가 README "완료 기준"의 화면이고 주차별 실습 점수의 근거다. 산출물이 보고서·표여서는 안 된다.
- 주차별 실습 점수는 1~7주·10~13주 캡처로 산정한다(2주차는 고정본의 캡처 4장). 8·9·14·15주는 실습 점수 대상이 아니다.
- 고정 평가 주: 8주 중간 개인 실기, 9주 1차 과제 발표, 14주 최종 프로젝트 발표, 15주 기말 개인 실기.
- 기본 문제를 먼저 완성하고 남는 시간에 확장 문제를 수행한다.

시험과 발표 주차는 대학 일정과 분반 인원에 따라 실제 평가 시간이 달라질 수 있다. 공개 자료에는 평가 구조와 연습 절차만 두며, 학기별 실제 문항·정답·학생 정보는 별도 비공개 공간에서 관리한다.

## 실습 루틴 (3주차부터 매 실습)

공용 실습실 PC라 수업이 끝나면 파일이 남지 않는 환경을 전제한다. 아래 루틴은 3주차부터 각 주 `lab.md` 시간표의 처음과 끝에 그대로 들어 있다.

**시작 0–5분**

| 상황 | 하는 일 |
|---|---|
| 지난 시간과 같은 PC | `git pull` |
| 다른 PC에서 처음 | `git clone https://github.com/<아이디>/my-web.git` |

**끝 55–60분**

1. `git add .` → `git commit -m "…"` → `git push`
2. Pages 주소를 새로고침해 반영을 확인하고 캡처한다
3. 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거한다

**Pages 반영 지연 규칙** — 각 주 `lab.md` "막혔을 때" 표의 첫 줄에 둔다.
- **11주차부터 확인·캡처는 공개 URL에서만 한다.** `localStorage`는 `file://`과 공개 주소가 서로 다른 저장소를 쓰므로 "새로고침해도 남는다"가 로컬 화면으로는 재현되지 않는다. 12주차 `fetch`도 같은 이유로 공개 URL이 기준이다.

- 공개 페이지 반영이 1~3분 늦는다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정하고, 다음 수업 시작 5분에 Pages 확인을 허용한다.

**clone이 로그인 문제로 막히면** 조교에게 전주 `examples/day2`를 받아 그 폴더에서 작업하고, 끝 루틴에서 `git remote add origin <URL>`을 한 뒤 push한다.

## 주차 폴더 구성

각 폴더는 같은 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 첫 줄에 실습 페이지 링크. 이번 주 질문 · 학습 목표 · 결과물(캡처 예) / 2일 수업 흐름 · 준비 / **이번 주 용어**(한국어 · English · 中文) · 이번 주 범위 / 수업 자료(덱 주소) / 완료 기준(캡처 1장) · 다음 수업 연결 · 공식 참고 자료 |
| `slides.md` | Marp 원고. `---`가 슬라이드 구분자. 일차마다 설명 30분을 `N일차 · A–B분 — 제목` 구간으로 나누고 일차 끝에 설명 합계를 적는다. 슬라이드 한 장은 비어 있지 않은 줄 16줄 이하, 태그·명령·속성·GitHub 화면 이름은 영문 원어를 그대로 쓴다 |
| `walkthrough.md` | 처음부터 그대로 따라 하는 단계(할 일 → 예상 결과). 명령 앞에 "현재 폴더"를 적는다. 전체 코드 블록은 `examples/` 파일과 글자 단위로 같다 |
| `lab.md` | 실습 페이지 링크, 일차별 60분 시간표(`A–B분` 표기, 3주차부터 0–5 시작 루틴·55–60 끝 루틴, 마지막 구간이 60분에서 끝난다), 단계별 문제와 힌트, 막혔을 때 표(첫 줄 Pages 지연 규칙, 나머지는 실제로 재현한 오류 문구), 제출물(캡처 1장), 먼저 끝났다면 |
| `examples/README.md` | 예제 파일 ↔ `my-web` 안 위치 ↔ 따라하기 단계 표, 개념별 최소 코드와 실행 결과 |
| `examples/dayN/` | 그날 수업이 끝났을 때의 **`my-web` 전체 파일**(그 주에 바뀌지 않은 파일도 포함) |

`examples/dayN/`의 규칙은 다음과 같다.

- 파일 하나는 60줄 이하로 두고, 학생이 직접 타이핑할 수 있는 크기를 넘지 않는다.
- 클래식 `<script src="app.js" defer>`만 쓴다. CDN·라이브러리·`type="module"`은 쓰지 않는다.
- 페이지마다 자기 `.js` 파일 하나를 연결한다.
- 모든 `dayN/index.html`은 브라우저 Console 오류 0으로 열린다.

시험·과제 주차는 같은 파일 세트에 다음을 더한다. 이 네 주차도 `README.md`·`slides.md`·`walkthrough.md`·`lab.md`는 똑같이 두며, `lab.md`에는 1일차 리허설 시간표와 2일차 시험·발표 운영 시간표 2개를 둔다.

| 주차 | 추가 파일 |
|---:|---|
| 8 | `exam_structure.md`, `rubric.md`, `examples/rehearsal_starter/`, `examples/rehearsal_solution/` |
| 9 | `project_brief.md`, `rubric.md` |
| 14 | `project_brief.md`, `rubric.md`, `examples/demo_outline.md` |
| 15 | `rubric.md`, `examples/rehearsal_starter/`, `examples/rehearsal_solution/` |

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
| 8 | 중간 개인 실기 | `my-web/exam/` 공개 URL · 저장소 URL · 마지막 commit SHA · 완성 화면 캡처 | [`week08_midterm`](week08_midterm/) |
| 9 | 1차 과제 발표와 브랜치 복습 | 2분 시연과 저장소 `README.md` 1차판 | [`week09_architecture_project`](week09_architecture_project/) |
| 10 | 배열 데이터를 목록으로 그리기 | 항목 3개를 쌓고 1개를 지운 뒤 "2개"가 표시된 방명록 | [`week10_supabase_data`](week10_supabase_data/) |
| 11 | 객체와 localStorage | 새로고침해도 남는 방명록 3개와 Application › Local Storage의 `guestbook` 키 | [`week11_auth_rls`](week11_auth_rls/) |
| 12 | fetch로 JSON 불러오기 | JSON에서 읽은 카드 3개와 Network 탭의 `projects.json` 200 | [`week12_persistent_crud`](week12_persistent_crud/) |
| 13 | 보안·접근성·릴리스 점검 | 태그를 입력해도 글자 그대로 보이고 Console 오류가 0인 375px 화면 | [`week13_release_security`](week13_release_security/) |
| 14 | 최종 프로젝트 발표 | 3분 시연과 README 최종판 | [`week14_project_presentation`](week14_project_presentation/) |
| 15 | 기말 개인 실기 | 본시험 공개 URL · 저장소 URL · 마지막 commit SHA | [`week15_final_exam`](week15_final_exam/) |

폴더 이름은 이미 배포된 슬라이드 주소(`.../webprg/decks/<폴더명>/`)를 깨뜨리지 않기 위해 그대로 둔다. 주차의 실제 주제는 위 표의 제목을 따른다.

## 자료 작성 원칙

- **학생 기준선**: 프로그래밍 경험이 거의 없는 대학생이다. 1주차에 URL·요청과 응답·HTML/CSS/JS의 역할·DevTools와 로컬 `git init → add → commit`, 2주차에 GitHub 저장소 `my-web`·push·Pages·브랜치와 merge까지 배웠다. 그 밖의 것은 모른다고 전제한다.
- **기준 자료 우선순위**: (1) 강의자 판서와 Git·GitHub 슬라이드 → (2) 수업계획서의 15주 헤드라인과 평가 배점 → (3) MDN 입문 순서(HTML → CSS → JavaScript → DOM → 폼 → 저장 → fetch). 순서·용어·API는 이 셋과 같게 쓴다.
- **한 주 새 개념은 3~5개**다. 앞 주에서 배운 것만 전제하고 난이도가 한 주에 두 단계 뛰지 않는다. "오늘 문법 5분"이나 복붙 틀로 처리하는 항목은 개념 수에서 빼되 슬라이드 1장으로 제한한다. Git 루틴(pull·add·commit·push)은 3주차부터 복습이므로 개념 수에 넣지 않는다.
- **매주 캡처 1장으로 보여 줄 웹페이지·동작 하나로 끝난다.** 1일차 중간 화면은 `lab.md`에 "확인용"으로만 둔다.
- `slides.md`에는 설명 30분 분량의 핵심만 두고 긴 설명은 강의 대본(비공개)으로 분리한다.
- 예제는 한 번에 한 개념만 보여 주는 최소 코드로 만든다.
- `lab.md`에는 정답 전체 대신 완료 조건과 단계별 힌트를 둔다. "막혔을 때" 항목은 실제로 재현해 본 Console·터미널 문구를 그대로 적는다.
- **표준 API·표준 용어만 쓴다**: `document.querySelector`, `textContent`, `addEventListener`, `classList`, `createElement`/`append`, `localStorage`, `JSON`, `fetch`/`await`. 클릭·제출 리스너 안에서 화면을 직접 바꾼다. 목록을 다시 그리는 함수 이름은 `showList()`로 통일한다.
- **학기 범위 밖**: ES Module(`type="module"`·`import`/`export`), 번들러, npm, Node 서버, 서버 DB·로그인, 화살표 함수, `map`·`filter`·`forEach`, 클래스, 구조 분해, spread, `git rebase`. 필요하면 "이 과목 범위 밖" 한 줄로만 말한다.
- 표준 입문 교재에 없는 설계 틀과 용어는 들여오지 않는다. 금지 목록은 강의자 설계 문서가 관리하며, 주차 검사 스크립트가 공개·비공개 문서를 모두 검사한다.
- **문법·API는 한 주에 몰아넣지 않고 쓰는 주에 5분**으로 도입한다.

| 문법·API | 처음 쓰는 주 | 형태 |
|---|---|---|
| `<script src="app.js" defer>`, `console.log`, Console 오류 줄(파일:줄) 읽기 | 5주 1일차 | 정식 항목 |
| `let`·`const`, 숫자·문자열, 템플릿 문자열 `` `${}` `` | 5주 1일차 | 정식 항목 |
| `if / else`, 비교 `===`·`>=`, `function` 정의·호출·`return` | 5주 2일차 | 정식 항목 |
| `document.querySelector('#greeting').textContent = …` | 5주 2일차 | 복붙 틀 1줄("6주에 배운다") |
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

- **개인정보**: 예시 아이디는 `student01`, 이메일은 `student01@example.com`, 저장소는 `my-web`, 공개 주소는 `https://student01.github.io/my-web/`이다. 공개 저장소·캡처·예제에 실명·학번·전화번호·실제 이메일을 넣지 않는다.
- 시험 폴더에는 문제 구조·starter·채점표만 두고 학기별 실제 문제와 정답은 별도 비공개 공간에서 관리한다.

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
