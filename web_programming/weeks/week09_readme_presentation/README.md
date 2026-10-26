[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project)

# 9주차 — 1차 과제 발표와 README

이번 주는 1차 과제 주다. 3~7주에 만든 사이트(7주차 완성본)를 이번 주 새 저장소 `web-week09` 에 넣고, 그 사이트를 소개하는 `README.md` 1차판을 쓴다. 2일차에 공개 주소를 열어 2분 동안 발표한다.
README 는 **마크다운**으로 쓴다. 비교 예제 3개(`.md` 파일)로 제목 `#`·목록 `-`·링크 `[보이는 글](주소)` 를 하나씩 보고, 1일차 끝에 그 세 가지로 README 1차판을 조립한다.
결과는 **VS Code 미리 보기**와 **GitHub 저장소 화면**에서 원문과 렌더된 모양을 나란히 놓고 본다. 사이트의 HTML·CSS·JavaScript 는 7주차 그대로 두고 고치지 않는다.

## 이번 주 질문

> 3~7주에 만든 내 사이트를 처음 보는 사람에게 2분 안에 보여 주고, 저장소 첫 화면 한 장으로 소개하려면 무엇을 알아야 하나?

답은 세 가지 원리다.
마크다운은 **줄 맨 앞의 기호**가 모양을 정한다. `#` 는 제목(개수가 늘수록 작아진다), `-` 는 목록 한 줄이고, 기호 뒤에 **띄어쓰기 한 칸**이 있어야 한다. 기호가 없는 줄은 원문에서 줄을 바꿔도 한 문단으로 이어진다.
링크는 `[보이는 글](주소)` 다. 소괄호에는 인터넷 주소나 **같은 저장소 안의 파일 이름**을 쓴다. 저장소 맨 위의 `README.md` 는 GitHub 저장소 첫 화면, 파일 목록 아래에 렌더되어 보인다.
지금 방명록에 남긴 글은 **화면**에만 있어서 새로고침하면 사라진다. 데이터가 갈 수 있는 곳은 화면·브라우저 저장소·인터넷 서버 DB 셋이다. 발표는 공개 주소에서 동작하는 화면을 정해 둔 순서로 2분 안에 보여 준다.

## 학습 목표

1. 마크다운 원문과 렌더된 모양을 VS Code 미리 보기(원문 옆)와 GitHub 저장소 화면(**Preview**·**Code**)에서 나란히 비교한다.
2. `#`·`##` 로 제목을 쓰고, `#` 뒤에 띄어쓰기가 없으면 제목이 아니라 글자로 보인다는 것을 확인한다.
3. `- ` 로 목록을 쓰고, 기호 없이 줄만 바꾼 줄은 한 문단으로 이어진다는 것을 확인한다.
4. `[보이는 글](주소)` 로 인터넷 주소와 같은 저장소 안의 파일(`index.html`·`screenshots/home.png`)을 링크해 README 1차판 다섯 항목을 쓴다.
5. 방명록 글이 새로고침하면 사라지는 까닭을 "데이터가 가는 세 곳"으로 말하고, 공개 주소 → 세 페이지 → 버튼·폼 → README·Commits 탭 순서로 2분 발표를 한다.

## 이번 주 결과물

```text
[캡처 1]   https://github.com/student01/web-week09
           저장소 첫 화면 ─ 파일 목록 아래에 README.md 가 렌더되어 보인다
           큰 제목 한 줄 ─ 내 사이트 이름
           작은 제목 다섯 ─ 공개 주소 · 페이지 · 기능 · 화면 · 이번에 배운 것

[발표 2분] https://student01.github.io/web-week09/
           홈 → 내 정보 → 방명록 → 버튼 한 번 → 폼 한 번 → README·Commits 탭
```

- 이번 주는 주차별 실습 점수 대상이 아니라 **1차 과제 10점**(발표 5 + 레포트 5)이다. 레포트는 따로 내는 문서가 아니라 저장소 첫 화면의 `README.md` 한 장이다.
- `web-week09/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다(확인용).
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 2분 발표 형식 → 데이터가 가는 세 곳 → ex01 제목 → ex02 목록 → ex03 링크 → 조립표 | 새 폴더 `web-week09` 에 7주차 완성본 넣기 → `ex/` 에 세 파일 저장 → 값 바꿔 보기 → 화면 두 장 캡처 → README 1차판 조립 → 짝과 2분 연습 → 새 저장소 만들어 올리기 · Pages 켜기 | 캡처 1(저장소 첫 화면) |
| 2일차 | 오늘 순서와 탭 세 개 → 채점표 10점 → 2분 시연 한 번 보기 → 공개 주소가 안 열리면 → 발표 시작 | **발표 2분 × 인원** → 총평과 10주차 예고 → README 를 고쳤으면 push | 발표 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 이번 주는 2일차 60분이 발표(평가)라서 비교 예제와 조립을 모두 1일차에 한다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 7주차 완성본. 내 `web-week07` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [7주차 `examples/day2/web-week07/`](../week07_async_modules/examples/day2/web-week07/) 파일을 **Raw** 로 받는다. 8주차 시험 저장소 `web-week08` 은 이번 과제와 관계가 없다
- VS Code(마크다운 미리 보기가 들어 있어 따로 설치하지 않는다), Chrome, Git (`git --version` 으로 확인)
- Node.js LTS(선택). [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md))
- 화면 캡처 단축키: Windows **Win+Shift+S**, macOS **⌘+Shift+4**
- 과제 안내와 채점 기준을 미리 읽는다: [1차 과제 안내](project_brief.md) · [채점표 10점](rubric.md)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 마크다운 | Markdown | Markdown 标记语言 |
| 제목 | heading | 标题 |
| 목록 | list | 列表 |
| 링크 | link | 链接 |
| 렌더(기호를 읽어 모양으로 그려 보이기) | render | 渲染 |
| 미리 보기 | preview | 预览 |
| 저장소 설명 파일 | README | 说明文件 |
| 발표·시연 | presentation · demo | 演示 |

## 이번 주 비교 예제

1일차 ex01~ex03 은 마크다운 파일(`.md`)이다. JavaScript 가 없어서 고르기 페이지와 `.js` 파일이 없다. VS Code 에서 파일을 열고 미리 보기를 옆에 띄워(**Ctrl+K** 다음 **V**, macOS **⌘+K** 다음 **V**) 원문과 렌더된 모양을 비교한다. 올린 뒤에는 GitHub 저장소 화면에서 같은 파일을 연다. 2일차는 발표라서 비교 예제가 없다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_heading.md](examples/day1/ex01_heading.md) | 같은 글자 `공개 주소` 앞에 1. `#` 하나 / 2. `##` 둘 / 3. `#` 뒤 띄어쓰기 없음 | 줄 맨 앞 `#` 개수가 제목의 크기를 정한다. `#` 뒤에 띄어쓰기 한 칸이 있어야 제목이다 | 10행 `##` 를 `###` 로, 14행 `#공개 주소` 에 띄어쓰기 한 칸 |
| [ex02_list.md](examples/day1/ex02_list.md) | 1. `- ` 세 줄 / 2. 기호 없는 세 줄 / 3. `-` 뒤 띄어쓰기 없음 | `- ` 로 시작하는 줄이 목록 한 줄이 된다. 기호 없는 줄은 줄을 바꿔도 한 문단으로 이어진다 | 2번 세 줄 사이에 빈 줄, 3번 `-` 뒤에 띄어쓰기 |
| [ex03_link.md](examples/day1/ex03_link.md) | 1. 인터넷 주소 / 2. 같은 폴더의 파일 / 3. 2번에서 `]` 와 `(` 사이만 띄움 | 대괄호는 보이는 글, 소괄호는 누르면 가는 곳이다. 같은 저장소 안의 파일은 이름(경로)만 쓴다 | 6행 주소를 내 공개 주소로, 10행 소괄호를 `ex02_list.md` 로, 14행 띄어쓰기 지우기 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week09_architecture_project/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [1차 과제 안내](project_brief.md) · [채점표 10점](rubric.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(ex01~ex03 의 `.md`), 2일차 `day2/`(완성본 `web-week09/`)
- 2일차 끝의 `web-week09`(1일차 끝과 같다): [README.md](examples/day2/web-week09/README.md) · [index.html](examples/day2/web-week09/index.html) · [about.html](examples/day2/web-week09/about.html) · [guestbook.html](examples/day2/web-week09/guestbook.html) · [styles.css](examples/day2/web-week09/styles.css) · [app.js](examples/day2/web-week09/app.js) · [guestbook.js](examples/day2/web-week09/guestbook.js) · [images/profile.png](examples/day2/web-week09/images/profile.png) · [screenshots/home.png](examples/day2/web-week09/screenshots/home.png) · [screenshots/guestbook.png](examples/day2/web-week09/screenshots/guestbook.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 데이터가 가는 세 곳 중 ③ 인터넷 서버 DB: [선택 특강 — Supabase 로 만드는 서버 방명록](../../specials/supabase_guestbook/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

## 완료 기준

- [ ] 새 저장소 `web-week09` 를 만들어 Pages 를 켰고, `ex/` 에 비교 예제 세 파일이 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] 저장소 맨 위에 `README.md` 1차판(큰 제목 한 줄과 작은 제목 다섯 항목)과 `screenshots/` 캡처 두 장(동작한 뒤의 화면)이 있다.
- [ ] `https://github.com/student01/web-week09` 첫 화면의 파일 목록 아래에 README 가 렌더되어 보이고, 공개 주소·세 페이지·캡처 두 장 링크를 누르면 모두 열린다.
- [ ] 공개 주소 `https://student01.github.io/web-week09/` 에서 nav 로 세 페이지를 오가고, 버튼과 폼(빈값 안내까지)이 동작한다.
- [ ] 저장소 첫 화면 캡처 1장을 제출했고, 2일차에 2분 발표를 했다.

## 다음 수업 연결

지금 방명록은 두 번째 글을 남기면 앞 글이 사라지고, 새로고침하면 모두 사라진다(세 곳 중 ① 화면).
10주차에는 새 저장소 `web-week10` 을 이번 주 `web-week09` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week09/`](examples/day2/web-week09/)), 글을 배열에 **쌓아** 목록으로 그리고 지운다. 11주차에는 그 목록을 ② 브라우저 저장소에 남겨 새로고침해도 보이게 한다.
오늘 쓴 README 는 13주차에 최종판으로 다시 쓰고, 14주차 최종 발표의 레포트가 된다. README 1차판 쓰기는 15주차 기말 [문제 은행](../week15_final_exam/examples/README.md)에도 [w09_readme_links](../week15_final_exam/examples/w09_readme_links/README.md) 문제로 들어 있다.

## 공식 참고 자료

- [리포지토리 README 파일에 관하여 — GitHub 문서](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기본 쓰기 및 서식 지정 구문 — GitHub 문서](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [파일 보기 및 이해 — GitHub 문서](https://docs.github.com/ko/repositories/working-with-files/using-files/viewing-and-understanding-files)
- [GitHub Pages 사이트 만들기 — GitHub 문서](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Markdown and Visual Studio Code — VS Code 문서(영문)](https://code.visualstudio.com/docs/languages/markdown)
- [Markdown Reference — CommonMark(영문)](https://commonmark.org/help/)
- [Web Storage API — MDN](https://developer.mozilla.org/ko/docs/Web/API/Web_Storage_API) (세 곳 중 ② 브라우저 저장소, 11주차)
- [웹의 동작 방식 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works)
