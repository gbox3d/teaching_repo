[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# 8주차 — 중간 개인 실기

이번 주는 새 내용을 배우지 않는다. 1~7주 실습 제출을 한 문제씩으로 정리한 **문제 은행**으로 연습하고(1일차), 같은 문제를 값만 바꾼 **중간 실기**를 본다(2일차).
은행 문제는 그 주에 배운 것만 쓰게 만들었다. 다른 주의 내용(HTML 뼈대·CSS·이미 있는 버튼 등)은 시작 파일에 다 들어 있고, 문제끼리 이어지지 않는다.
해답은 공개하지 않는다. 문제마다 해답 대신 **확인할 것**이 있다. 화면과 F12 로 그 항목을 하나씩 맞춰 보면 스스로 맞았는지 안다.

## 이번 주 질문

> 1~7주 실습에서 한 번씩 만든 것을, 값이 바뀐 문제지만 보고 **혼자 60분 안에** 다시 만들어 공개 주소까지 올릴 수 있을까?

답은 코드를 외우는 것이 아니다. 문제 문장을 읽는 순서와, 맞았는지 스스로 확인하는 방법이다.
시험 문제는 은행 문제와 문장·할 일·확인하는 방법이 같고 **값만 다르다**. 1일차에 은행 문제로 "읽기 → 받기 → 서버로 열기 → 할 일 → 확인할 것 맞추기"를 손에 익히면, 2일차에는 바뀐 값으로 같은 순서를 밟는다.

## 학습 목표

1. 은행 문제 하나를 읽고 "시작 파일"·"할 일"·"확인할 것"·"이 문제의 값"이 각각 무엇을 말하는지 구분한다. 시험에서는 "이 문제의 값" 표의 값만 바뀐다.
2. 문제 폴더를 **Raw** 로 받아 `node server.mjs` 로 열고, "확인할 것"을 화면·F12(Console·Network·Elements)·기기 모드로 하나씩 맞춘다. 해답 없이 맞았는지 스스로 판단한다.
3. 이번 주 새 저장소 `web-week08` 을 1일차에 만들어 Pages 를 켜고, 연습한 문제 폴더를 공개 주소에서 다시 확인한다.
4. 2일차에 받은 `exam` 폴더를 저장소 맨 위에 넣고, 시작과 끝에 한 번씩 올리며 60분 안에 문제 넷을 푼다. 한 문제에 5분 넘게 막히면 다음 문제로 간다.
5. 제출 세 가지(공개 주소 `…/web-week08/exam/`·저장소 주소·GitHub **Commits** 탭 캡처)를 낸다.

## 이번 주 결과물

```text
[제출 1] 공개 주소     https://student01.github.io/web-week08/exam/
[제출 2] 저장소 주소   https://github.com/student01/web-week08
[제출 3] 캡처 1장      GitHub Commits 탭 ─ 맨 위 commit(중간 실기 끝)의 번호와 시각이 보이게
```

- 제출은 2일차 시험이 끝날 때 이 세 가지다. 이번 주는 주차별 실습 점수 대상이 아니라 **중간 실기 20점(안)** 으로 본다. 기준은 [채점표](rubric.md)에 있다.
- 1일차에 올린 연습 폴더(`https://student01.github.io/web-week08/w05_greeting_card/` 등)는 확인용이다. 점수에 들어가지 않는다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 이번 주는 문제 은행과 시험(같은 문제·값만 바뀜·해답 비공개·확인할 것) → 문제 하나 읽는 법([w05_greeting_card](examples/w05_greeting_card/)) → 확인하는 법(서버로 열기, F12 Console·Network·Elements, 기기 모드) → 오늘 순서와 저장소 만들기·Pages | 은행에서 영역이 다른 문제 셋 고르기 → 문제마다 받기 → 서버로 열기 → 할 일 → "확인할 것" 맞추기 → 새 저장소 `web-week08` 만들어 올리기 · Pages 켜기 → 공개 주소에서 다시 확인 | 연습 폴더 공개 주소(확인용) |
| 2일차 | 시험 규칙(볼 수 있는 것·범위·막히면 넘어가기·시간표) → `exam` 폴더 받기·저장소 맨 위에 넣기·목차 열기·시작 올리기 → 영역·배점·채점 → 끝내기 전(마지막 올리기·공개 주소·Commits 탭 캡처) | **중간 실기 60분** — `exam` 폴더의 문제 넷(A HTML · B CSS · C JavaScript·DOM · D 폼) → 마지막 올리기 → Commits 탭 캡처 | 제출 세 가지 |

각 수업은 `설명 30분 + 실습 60분` 이다. 2일차 60분은 연습이 아니라 **평가 시간**이다. 분 단위 시간표는 [실습지](lab.md)에 있다.

## 준비

- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). `node -v` 로 확인한다. [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더 맨 위에 받아 `node server.mjs` 로 띄운다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 연다. 다만 F12 › Network 의 Status 번호(`200`·`404`)는 서버로 연 주소나 공개 주소에서만 보인다
- GitHub 로그인. 1일차 끝에 새 저장소 `web-week08` 을 만들고, 2일차에는 그 저장소에 `exam` 폴더를 넣는다
- 1~7주 실습지. 은행 문제마다 제목 아래 줄의 출처 링크가 그 주 실습지의 제출 절이다. 시험 중에도 교재 사이트·본인 저장소·MDN 은 볼 수 있다
- 채점 기준을 미리 읽는다: [채점표](rubric.md) · [시험 구조](exam_structure.md)
- 화면 캡처 단축키: Windows **Win+Shift+S**, macOS **⌘+Shift+4**
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 중간 실기 | midterm practical exam | 期中实操考试 |
| 문제 은행 | problem bank | 题库 |
| 시작 파일 | starter files | 起始文件 |
| 할 일 | tasks | 任务 |
| 확인할 것 | checks | 检查项 |
| 이 문제의 값 | values of this problem | 本题的值 |
| 영역 | section (A~D) | 考查部分 |
| 시험 폴더 · 목차 | exam folder · index page | 考试文件夹 · 目录 |
| 커밋 기록(Commits 탭) | commit history | 提交记录 |
| 채점표 | rubric | 评分表 |

## 이번 주 범위

시험은 1~7주 실습 제출에서만 낸다. 은행 문제는 일곱 개다. 2일차에는 영역마다 한 문제씩, 모두 네 문제가 값만 바뀌어 나온다.

| 영역 (배점) | 출처 주 | 은행 문제 | 권장 |
|---|---|---|---:|
| A HTML (4점) | [1주차 실습 제출](../week01_web_git/lab.md#제출--캡처-두-장) | [w01_link_fix](examples/w01_link_fix/) 세 파일 연결 고치기 | 8분 |
| A HTML (4점) | [2주차 실습 제출](../week02_github_pages/lab.md#제출--캡처-네-장) | [w02_about_page](examples/w02_about_page/) 새 페이지와 상대 링크 | 10분 |
| A HTML (4점) | [3주차 실습 제출](../week03_semantic_html/lab.md#제출--캡처-한-장) | [w03_guestbook_form](examples/w03_guestbook_form/) 신청 폼 페이지 | 10분 |
| B CSS (4점) | [4주차 실습 제출](../week04_responsive_css/lab.md#제출--캡처-한-장) | [w04_responsive_css](examples/w04_responsive_css/) 반응형 메뉴와 카드 | 12분 |
| C JavaScript·DOM (5점) | [5주차 실습 제출](../week05_javascript_data/lab.md#제출--캡처-한-장) | [w05_greeting_card](examples/w05_greeting_card/) 인사 카드 | 12분 |
| C JavaScript·DOM (5점) | [6주차 실습 제출](../week06_dom_crud/lab.md#제출--캡처-한-장) | [w06_dark_mode](examples/w06_dark_mode/) 문구 바꾸기·다크 모드·클릭 횟수 | 12분 |
| D 폼 (3점) | [7주차 실습 제출](../week07_async_modules/lab.md#제출--캡처-한-장) | [w07_form_result](examples/w07_form_result/) 폼 제출을 한 줄로, 빈값 안내 | 11분 |

나머지 4점은 제출·공개 3점과 Console 오류 없음 1점이다. 합계 20점(안)이고, 영역마다 무엇을 보는지는 [채점표](rubric.md)에 있다.
문제 이름을 누르면 문제 문장(시작 파일·할 일·확인할 것·이 문제의 값·받기와 올리기)과 시작 파일이 보인다. 은행 전체 목록은 [examples/README.md](examples/README.md)다.

**범위 밖**: 배열로 목록 그리기(10주), `localStorage`(11주), `fetch`·JSON(12주), ES Module(`import`·`export`), 외부 라이브러리·CDN.
범위 밖 기능을 넣어도 가점은 없다. 그 때문에 요구 동작이 멈추면 그 영역에서 감점한다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week08_midterm/index.html
- [순서대로 따라하기](walkthrough.md) — 1일차 연습 절차, 2일차 시험 절차
- [실습과 시험 안내](lab.md)
- [시험 구조](exam_structure.md) · [채점표 20점(안)](rubric.md)
- [문제 은행 목록](examples/README.md) — 1~7주 문제 일곱 개
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 15주 기말 은행(1~14주 누적, 이번 주 일곱 문제 포함): [15주차 문제 은행](../week15_final_exam/examples/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

## 완료 기준

- [ ] 1일차: 새 저장소 `web-week08` 에 연습한 문제 폴더가 올라가 있고 **Settings › Pages** 가 켜져 있다.
- [ ] 1일차: 영역이 다른 문제 셋을 풀어 "확인할 것"을 스스로 맞춰 봤고, 맞추지 못한 항목이 무엇인지 안다.
- [ ] 2일차: 시험을 시작하자마자 `exam` 폴더를 저장소 맨 위에 넣어 한 번 올렸다(`중간 실기 시작`).
- [ ] 2일차: 마지막으로 올렸고(`중간 실기 끝`), `https://<아이디>.github.io/web-week08/exam/` 에서 목차와 문제마다 페이지가 열린다.
- [ ] 2일차: 제출 세 가지(공개 주소·저장소 주소·Commits 탭 캡처)를 냈다.

## 다음 수업 연결

[9주차](../week09_architecture_project/README.md)는 **1차 과제 발표**다. 지금까지 만든 내 사이트를 공개 주소로 2분 동안 보여 주고, 그 사이트를 소개하는 `README.md` 1차판(제목·공개 주소·페이지·기능·화면 그림·배운 것)을 저장소 첫 화면에 쓴다.
그 README 는 15주 은행의 [w09_readme_links](../week15_final_exam/examples/w09_readme_links/) 문제가 된다.
15주 기말 실기도 이번 주와 같은 방식이다. 기말 은행은 1~14주 누적이라 이번 주 일곱 문제도 들어 있고, 다시 나오면 8주와 다른 값으로 나온다.
이번 주 `web-week08` 저장소는 채점이 끝날 때까지 지우거나 이름을 바꾸지 않는다.

## 공식 참고 자료

- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [GitHub Pages 사이트에 대한 게시 원본 구성 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Git에서 GitHub 자격 증명 캐싱 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/caching-your-github-credentials-in-git)
- [Console 개요 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console?hl=ko)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
- [CSS 보기 및 변경 — Chrome DevTools](https://developer.chrome.com/docs/devtools/css?hl=ko)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode)
- [첫 HTML 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [CSS 미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
