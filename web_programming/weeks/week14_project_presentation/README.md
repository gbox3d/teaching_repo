[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 — 최종 프로젝트 발표

이번 주에는 새 문법이 없다. 3~13주에 한 주씩 쌓은 사이트를 새 저장소 `web-week14` 에 담아, 2일차에 공개 주소 하나로 **3분** 동안 보여 준다.
1일차에는 발표 준비에 필요한 비교 예제 3개를 열어 값을 바꿔 보고, 지난주 완성본에 홈의 발표 순서 목록과 내 정보 표의 공개 주소 한 줄을 조립한다. README 최종판은 세 곳만 고친다.
2일차 90분은 모두 발표다. 결과는 공개 주소와 저장소 첫 화면(README)에서 본다.

## 이번 주 질문

> 3~13주에 한 주씩 쌓아 온 내 사이트를, 공개 주소 하나로 **3분 안에** 남에게 보여 줄 수 있을까? 그리고 그 설명을 저장소 첫 화면에 한 장으로 남길 수 있을까?

답은 세 가지 원리다.
발표 순서는 미리 정해 두고 그대로 한다. 차례가 뜻을 가지는 목록은 번호 목록 `<ol>` 로 쓴다. 홈에 적어 두면 발표 중에 다음 할 일이 화면에 보인다.
발표는 공개 주소가 기본이다. 안 열리면 내 PC 에서 `node server.mjs` 로 연다. 두 번 눌러 연 `file://` 페이지에서는 `fetch` 가 파일을 읽지 못해 프로젝트 카드가 나오지 않는다.
새로고침해도 남는 글은 브라우저의 저장 칸(`localStorage`, 11주)에 있다. 저장 칸은 **주소 앞부분마다 따로이고 시크릿 창도 따로**다(`http://localhost:8000` 과 `https://student01.github.io` 는 다른 칸이고, 시크릿 창은 일반 창과 다른 칸이며 닫으면 비워진다). 그래서 방명록 글은 발표 직전에 발표할 바로 그 창에서 남긴다.

## 학습 목표

1. [3분 시연 흐름 표](demo_outline.md)의 여덟 줄(공개 주소 → 네 페이지 → 버튼 → 폼 빈값 안내 → 목록 추가·삭제 → 새로고침 → JSON 카드 → Commits 탭과 README) 순서로 3분 발표를 한다.
2. 차례가 뜻을 가지는 목록은 `<ol>`, 아닌 목록은 `<ul>` 로 쓴다. 번호는 브라우저가 줄 순서대로 붙인다는 것을 확인하고, 홈에 발표 순서 다섯 줄을 `<ol class="card">` 로 넣는다.
3. 같은 페이지를 `node server.mjs` 로 열 때와 두 번 눌러 열 때 `fetch` 결과가 다르다는 것을 확인하고, 공개 주소가 안 열릴 때 로컬 시연을 서버로 한다.
4. 새로고침해도 남는 값은 저장 칸(`localStorage`)에 있고, 저장 칸이 주소 앞부분마다 따로이며 시크릿 창도 따로라는 것을 확인한다.
5. README 최종판의 공개 주소와 홈 설명을 고치고 만든 과정에 14주차 한 줄을 더해(9~14주차 여섯 줄), 저장소 첫 화면에서 그림 세 장이 보이는지 확인한다.
6. 구술 한 문항("이 버튼을 누르면 어느 함수가 실행됩니까?")에 내 코드로 답한다.

## 이번 주 결과물

```text
[발표 3분] https://student01.github.io/web-week14/
           홈 → 네 페이지 → 다크 모드 → 폼 빈값 안내 → 목록 추가·삭제
           → 새로고침 → JSON 카드 → Commits 탭과 README

[캡처 1]   https://github.com/student01/web-week14
           저장소 첫 화면 ─ 파일 목록 아래에 README 최종판과 그림 세 장이 함께 보이게
```

- 이번 주는 주차별 실습 점수 대상이 아니다. **2차 과제 20점**(발표 12 + 레포트 8)이고 기준은 [채점표](rubric.md)에 있다.
- 레포트는 저장소의 `README.md` 한 장이다. 별도 보고서 파일은 내지 않는다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 발표 순서와 3분 규칙 → 채점표 20점 → ex01 시연 순서를 번호 목록으로 → ex02 로컬 시연은 서버로 → ex03 저장은 주소·창마다 따로 → 좋은 시작·피할 시작 → 조립표 | 새 폴더 `web-week14` 에 지난주 완성본 넣기 → `ex/` 에 여섯 파일 → 값 바꿔 보기 → 홈 목록·공개 주소 행·README 조립 → 새 저장소 올리기·Pages 켜기 → 공개 주소 확인·그림 다시 찍기 → 조교 확인·3분 리허설 → push | 캡처 1 |
| 2일차 | 안내 5분 — 오늘 차례, 탭 세 개, 채점표와 구술 한 문항, 공개 주소가 안 열릴 때 | 발표 3분 × 인원 → 총평과 15주차 예고 | 발표 3분 |

1일차는 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.
**2일차는 설명과 실습으로 나누지 않고 90분 전체가 발표다.** 21명 기준으로 0–5분 안내, 5–68분 발표, 68–80분 총평과 15주차 예고, 80–90분은 지연 여유다. 실제 차례와 시각은 수업 공지를 따른다.

## 준비

- 지난주 완성본. 내 `web-week13` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [13주차 `examples/day2/web-week13/`](../week13_release_security/examples/day2/web-week13/) 파일을 **Raw** 로 받는다. `README.md` 와 `screenshots/` 도 함께 넣는다. 그 `README.md` 가 이번 주 레포트다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS. 지난주 폴더의 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). 공개 주소가 안 열릴 때 로컬 시연을 이것으로 한다
- 과제 안내와 채점 기준: [2차 과제 안내](project_brief.md) · [채점표](rubric.md) · [3분 시연 흐름 표](demo_outline.md). 시연 흐름 표는 종이에 옮겨 적어 둔다
- **확인과 캡처는 공개 주소에서 한다.** 두 번 눌러 연 화면은 방명록이 다른 저장 칸을 쓰고, 프로젝트 카드가 나오지 않는다(ex02·ex03)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 최종 발표 | final presentation | 期末展示 |
| 시연 | demo | 演示 |
| 시연 흐름 표 | demo outline | 演示流程表 |
| 번호 목록 | ordered list (`ol`) | 有序列表 |
| 점 목록 | unordered list (`ul`) | 无序列表 |
| 로컬 시연 | local demo (`localhost`) | 本地演示 |
| 시크릿 창 | incognito window | 无痕窗口 |
| 구술 질문 | oral question | 口头提问 |

## 이번 주 비교 예제

비교 예제는 1일차에만 있다. 2일차는 발표만 한다. 세 예제는 화면이 서로 달라서 고르기 페이지 없이 파일마다 따로 연다. ex01 은 `.html` 하나, ex02·ex03 은 `.html` 과 `.js` 한 쌍이고, ex02 에는 읽어 올 `.json` 이 하나 더 있다. Console 의 번호가 코드의 형제 번호와 같다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_order_list.html](examples/day1/ex01_order_list.html) | 같은 다섯 줄을 1. `<ol>` 번호 목록 / 2. `<ul>` 점 목록에 | 번호는 파일에 쓰지 않는다. 브라우저가 줄 순서대로 붙인다. 발표 순서처럼 차례가 뜻을 가지면 `<ol>` | 1번의 두 줄 순서 바꾸기, `ol` 을 `ul` 로, `</ol>` 지우기 |
| [ex02_server.html](examples/day1/ex02_server.html) + [.js](examples/day1/ex02_server.js) + [.json](examples/day1/ex02_message.json) | 같은 페이지를 1. `node server.mjs` 로 연다 / 2. 두 번 눌러 연다 | 12주 ex05 복습. `fetch` 는 서버(`http://`)나 공개 주소(`https://`)로 연 페이지에서만 파일을 읽는다. 로컬 시연은 서버로 한다 | 서버로 열기 → 두 번 눌러 열기, 읽을 파일 이름을 틀리게 |
| [ex03_storage.html](examples/day1/ex03_storage.html) + [.js](examples/day1/ex03_storage.js) | 1. 변수에 담은 수 / 2. 저장 칸(`localStorage`)에 넣은 수 | 11주 ex04 복습 + 주소·창 비교. 새로고침하면 변수는 처음으로 돌아가고 저장 칸의 값은 남는다. 저장 칸은 주소 앞부분마다 따로이고 시크릿 창도 따로다. 같은 아이디의 `github.io` 주소(`web-week13`·`web-week14`)는 저장 칸을 함께 쓴다(11주) | 새로고침, 열 때 꺼내는 줄 빼기, 서버 주소·새 시크릿 창으로 열기 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week14_project_presentation/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [2차 과제 안내](project_brief.md) · [채점표 20점](rubric.md) · [3분 시연 흐름 표](demo_outline.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(ex01~ex03), 2일차 `day2/`(완성본 `web-week14/` 만)
- 2일차 끝의 `web-week14`(조립 결과): [index.html](examples/day2/web-week14/index.html) · [about.html](examples/day2/web-week14/about.html) · [README.md](examples/day2/web-week14/README.md) · 그림 [home.png](examples/day2/web-week14/screenshots/home.png) · [guestbook.png](examples/day2/web-week14/screenshots/guestbook.png) · [projects.png](examples/day2/web-week14/screenshots/projects.png)
- 13주차 그대로인 파일: [styles.css](examples/day2/web-week14/styles.css) · [app.js](examples/day2/web-week14/app.js) · [about.js](examples/day2/web-week14/about.js) · [guestbook.html](examples/day2/web-week14/guestbook.html) · [guestbook.js](examples/day2/web-week14/guestbook.js) · [projects.html](examples/day2/web-week14/projects.html) · [projects.js](examples/day2/web-week14/projects.js) · [data/projects.json](examples/day2/web-week14/data/projects.json)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation

## 완료 기준

- [ ] 새 저장소 `web-week14` 를 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 봤다.
- [ ] 공개 주소 `https://student01.github.io/web-week14/` 가 **새 시크릿 창**에서 열리고 nav 로 네 페이지를 오간다.
- [ ] 홈의 `클릭 0회` 카드 아래에 `이 사이트에서 할 수 있는 것` 번호 목록 다섯 줄이 있고, 그 순서가 내 발표 순서와 같다.
- [ ] 내 정보 표 맨 아래에 **공개 주소** 행이 있고, 주소가 내 `web-week14` 공개 주소다.
- [ ] 저장소 첫 화면에 README 최종판과 그림 세 장이 보이고, README 의 공개 주소 링크를 누르면 내 사이트가 열린다. `## 만든 과정` 은 9주차부터 14주차까지 주차마다 한 줄(여섯 줄)이다.
- [ ] 저장소 첫 화면(README 최종판과 그림 세 장)을 캡처 1장으로 제출했다.
- [ ] 2일차 발표 직전에 발표할 창에서 방명록 글 두세 줄을 남기고 3분 발표를 했다.

## 다음 수업 연결

15주차는 기말 개인 실기다. 범위는 1~14주 누적이고, 새 저장소 `web-week15` 에서 혼자 푼다.
1일차에는 1~14주 실습 제출로 만든 [문제 은행](../week15_final_exam/examples/README.md)으로 연습하고 저장소를 만들어 Pages 를 켠다. 2일차 60분이 기말 실기이며, 은행 문제를 영역마다 하나씩 값만 바꿔 낸다.
구현 15점 + 시연 5점이다. 시연은 제출한 공개 주소를 채점자가 직접 여는 것과 구술 한 문항으로 본다.
이번 주에 마무리한 README 최종판도 은행에 [w14_readme_images](../week15_final_exam/examples/w14_readme_images/README.md) 문제로 들어 있다. 은행 목록과 [채점표](../week15_final_exam/rubric.md)를 미리 읽어 온다.

## 공식 참고 자료

- [ol 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/ol)
- [ul 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/ul)
- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [CORS 오류: Cross origin requests are only supported for HTTP — MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [로컬 저장소 보기와 수정 — Chrome DevTools](https://developer.chrome.com/docs/devtools/storage/localstorage?hl=ko)
- [시크릿 모드로 탐색하기 — Chrome 고객센터](https://support.google.com/chrome/answer/95464?hl=ko)
- [Console 개요 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console?hl=ko)
- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
