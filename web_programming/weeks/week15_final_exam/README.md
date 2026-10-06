[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

# 15주차 — 기말 개인 실기

이번 주는 새로 배우는 것이 없다. 1~14주 실습의 제출을 한 문제씩으로 정리한 **문제 은행**(13문제)을 풀어 보고, 2일차에 그 은행에서 나온 문제로 기말 실기를 본다.
시험 문제는 은행 문제와 문장·할 일·확인하는 방법이 같고, 문제마다 있는 "이 문제의 값" 표의 **값만 바뀐다**. 8주에 나온 문제가 다시 나오면 8주와 다른 값으로 나온다.
해답은 공개하지 않는다. 문제마다 있는 **"확인할 것"이 모두 맞으면 된 것이다.** 확인은 서버로 연 화면과 F12, 그리고 공개 주소에서 한다.

## 이번 주 질문

> 1~14주 실습 제출을 모은 문제 은행으로 연습하고, **값만 바뀐 같은 문제**를 60분 안에 풀어 공개 주소로 제출할 수 있을까?

답은 외워 둔 코드가 아니다. 두 가지 습관이다.
문제 문장에서 **고칠 파일과 자리**를 먼저 찾는다(시작 파일 표와 할 일). 그리고 결과를 **스스로 확인**한다(확인할 것 — 화면, F12, 서버 주소, 공개 주소).
문제마다 그 주에 배운 것만 쓰고 나머지 파일은 다 주어진다. 은행 문제를 "확인할 것"까지 맞춰 두면 시험 문제를 한 번 푼 셈이다.

## 학습 목표

1. 문제 문장의 "시작 파일" 표에서 고칠 파일과 고치지 않을 파일을 가른다. "할 일"을 적힌 차례대로 하고, 그 주에 배운 것만 쓴다.
2. "확인할 것"을 스스로 맞춘다. 화면 글자, F12 › Console(빨간 줄·식 쳐 보기), Network(요청과 200·404), Elements, Application(Local Storage), 기기 모드(폭 375 등)에서 본다.
3. 파일을 요청하는 문제(`fetch`)는 두 번 눌러 연 `file://` 이 아니라 서버(`node server.mjs`)나 공개 주소에서 확인한다. `file://` 에는 요청을 받을 웹 서버가 없어서 브라우저가 요청을 막는다.
4. "이 문제의 값" 표의 값이 바뀌어도 같은 할 일을 한다. 값은 표의 글자 그대로 쓴다. 한 글자만 달라도 확인할 것이 맞지 않는다.
5. 이번 주 저장소 `web-week15` 에 시험 폴더 `exam` 을 넣어 올리고, 공개 주소·저장소 주소·Commits 탭 캡처 세 가지로 낸다. 구술에서는 본인 코드의 한 줄이 하는 일을 말한다.

## 이번 주 결과물

```text
[1일차 · 확인용] https://student01.github.io/web-week15/w12_fetch_cards/   ← 연습한 문제 폴더마다 하나

[2일차 · 제출]   ① https://student01.github.io/web-week15/exam/   ← 목차. 문제 A~E 로 가는 링크 다섯 줄
                 ② https://github.com/student01/web-week15
                 ③ GitHub Commits 탭 캡처 1장 ─ 맨 위 commit 「기말 실기 끝」의 번호와 시각이 보이게
```

- 제출은 2일차의 세 가지다. 1일차에 올린 연습 폴더는 확인용이며 따로 내지 않는다.
- 점수는 2일차 기말 실기의 구현 15점과 시연 5점(URL 재현 3·구술 2), 모두 20점(안)이다. 구술은 내는 것이 아니라 시험 후반에 강의자가 좌석에서 1분 묻는 것이다. 기준은 [채점표](rubric.md)에 있다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습·시험 60분 | 결과 |
|---|---|---|---|
| 1일차 | 이번 주는 문제 은행과 시험 → 문제 하나 읽는 법(시작 파일 · 할 일 · 확인할 것 · 이 문제의 값) → 확인하는 법(서버로 열기, F12 Console·Network·Elements·Application, 기기 모드) → 오늘 순서와 새 저장소 | 은행에서 영역이 다른 세 문제 고르기(9~14주 문제 하나 이상) → 받기 · 서버로 열기 · 할 일 · 확인할 것 → 새 저장소 `web-week15` 에 올리기 · Pages 켜기 | 연습 폴더 셋(확인용) |
| 2일차 | 시험 규칙 → `exam` 폴더 받기 · 맨 위에 넣기 · 시작 올리기 → 영역 · 배점 · 채점(시연 5점 포함) → 끝내기 전 | 기말 실기: 읽기 3분 → 문제 다섯(A~E) 48분 → 마지막 올리기 5분 → 예비 4분. 구술은 시험 후반 30분에 좌석에서 1분(쓴 1분은 마감 때 돌려준다) | 제출 세 가지 |

각 수업은 `설명 30분 + 실습(시험) 60분` 이다. 1일차 연습은 점수에 들어가지 않는다. 시간표와 규칙은 [실습지](lab.md)에 있다.

## 준비

- 14주까지 쓰던 PC 환경: VS Code, Chrome(DevTools), Git(`git --version` 으로 확인), Node.js LTS(`node -v` 로 확인). GitHub 로그인이 되는지 1일차에 확인한다
- 정적 서버 [server.mjs](../../tools/static-server/server.mjs). 1일차 시작 때 이번 주 폴더 `web-week15` 맨 위에 **Raw** 로 받는다([사용 안내](../../tools/static-server/README.md)). `fetch` 문제는 서버나 공개 주소에서만 확인된다. Node 가 없는 PC 는 나머지 문제를 두 번 눌러 열어 확인한다
- [문제 은행 목록](examples/README.md)을 한 번 훑어 온다. 지난 주차 가운데 캡처를 못 냈거나 오래 걸린 주가 어디인지 적어 온다. 1일차에 그 영역부터 푼다
- 이번 주에 만드는 것은 새 저장소 `web-week15` 하나다. 1일차 50–60분에 만들어 Pages 를 켜고, 2일차 시험에 그대로 쓴다. 2일차에는 새로 만들지 않는다
- 시험 중 볼 수 있는 것: 교재 사이트, 본인 저장소, MDN. 그 밖은 강의자 공지를 따른다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 기말 실기 | final practical exam | 期末实操考试 |
| 문제 은행 | problem bank | 题库 |
| 시작 파일 | starter files | 起始文件 |
| 확인할 것 | checks | 检查项 |
| 이 문제의 값 | values for this problem | 本题取值 |
| 영역 | section | 考查领域 |
| 공개 주소 | GitHub Pages URL | 网页公开地址 |
| 커밋 목록(Commits 탭) | commit history | 提交记录 |
| URL 재현 | reproduce at the URL | 按网址复现 |
| 구술 확인 | oral check | 口头提问 |

## 이번 주 범위

범위는 1~14주 누적이다. 시험은 영역 A~E 에서 은행 문제를 하나씩, 모두 다섯 문제를 낸다. 어느 문제가 나오는지는 시험 때 안다.
1~7주 문제는 [8주차 문제 은행](../week08_midterm/examples/README.md)과 같은 폴더를 쓴다. 9~14주 문제는 이번 주 [examples/](examples/README.md)에 있다.

| 영역(배점) | 출처 | 은행 문제 | 그 주에 한 것 |
|---|---|---|---|
| A 화면(HTML·CSS·README) · 3점 | 1주 | [w01_link_fix](../week08_midterm/examples/w01_link_fix/) | `index.html` 의 CSS·JS 연결 줄 고치기 |
| | 2주 | [w02_about_page](../week08_midterm/examples/w02_about_page/) | 새 페이지와 상대 링크로 오가기 |
| | 3주 | [w03_guestbook_form](../week08_midterm/examples/w03_guestbook_form/) | 번호 목록과 이름표 붙은 입력 칸이 있는 폼 페이지 |
| | 4주 | [w04_responsive_css](../week08_midterm/examples/w04_responsive_css/) | 폭·메뉴·카드·좁은 화면의 CSS |
| | 9주 | [w09_readme_links](examples/w09_readme_links/) | README 1차판(제목·목록·링크) |
| | 14주 | [w14_readme_images](examples/w14_readme_images/) | README 최종판과 그림 세 장 |
| B DOM · 3점 | 5주 | [w05_greeting_card](../week08_midterm/examples/w05_greeting_card/) | 함수와 `if` 로 만든 인사를 카드에 쓰기 |
| | 6주 | [w06_dark_mode](../week08_midterm/examples/w06_dark_mode/) | 버튼으로 문구·다크 모드·클릭 횟수 바꾸기 |
| | 13주 | [w13_text_safe](examples/w13_text_safe/) | 입력한 글을 글자 그대로 보이게 |
| C 폼·목록 · 4점 | 7주 | [w07_form_result](../week08_midterm/examples/w07_form_result/) | 폼 제출을 한 줄 결과로, 빈값 안내 |
| | 10주 | [w10_list_delete](examples/w10_list_delete/) | 배열로 목록 그리기, 줄마다 삭제, 개수 |
| D 저장(localStorage) · 2점 | 11주 | [w11_local_storage](examples/w11_local_storage/) | 저장·되살리기·그 키만 지우기 |
| E 불러오기(fetch) · 3점 | 12주 | [w12_fetch_cards](examples/w12_fetch_cards/) | JSON 파일을 불러와 카드로, 실패 안내 |

- 문제끼리 이어지지 않는다. 한 문제에 5분 넘게 막히면 다음 문제로 간다.
- 새 문법·새 API 는 이번 주에 없다. 범위 밖 기능은 가점하지 않는다.
- 같은 결과를 내면 쓰는 방법은 달라도 된다(`var`·`getElementById`·`innerText` 로 써도 확인 결과가 같으면 정답이다).

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week15_final_exam/index.html
- [순서대로 따라하기](walkthrough.md) — 1일차 연습(예: `w12_fetch_cards`)과 2일차 시험 날 절차
- [실습과 제출 안내](lab.md)
- [문제 은행 목록](examples/README.md) — 1~14주 13문제. 1~7주 문제는 [8주차 문제 은행](../week08_midterm/examples/README.md)과 같다
- [채점표](rubric.md)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

## 완료 기준

- [ ] 1일차에 영역이 다른 세 문제(9~14주 문제 하나 이상)를 받아, 문제마다 "확인할 것"을 서버로 연 화면에서 모두 맞췄다.
- [ ] 새 저장소 `web-week15` 를 만들어 Pages 를 켰고, 공개 주소 `https://student01.github.io/web-week15/<문제 id>/` 에서 "확인할 것"을 다시 봤다.
- [ ] 2일차에 받은 `exam` 폴더를 저장소 맨 위에 넣고 시작하자마자 올렸다(`기말 실기 시작`).
- [ ] 마지막으로 올렸고(`기말 실기 끝`), 공개 주소 `https://student01.github.io/web-week15/exam/` 의 목차에서 다섯 문제가 열린다.
- [ ] 시험 후반에 구술 1분을 했다.
- [ ] 제출 세 가지(공개 주소 · 저장소 주소 · Commits 탭 캡처)를 냈다.

## 다음 수업 연결

이번 주로 15주 수업이 끝난다. 다음 주차는 없다.
성적이 나올 때까지 `web-week15` 저장소와 공개 주소를 지우지 않고, 마감 뒤에는 그 저장소에 올리지 않는다. 채점자가 공개 주소를 다시 연다(URL 재현). 점수 공개와 확인 방법은 수업 공지를 따른다.
한 학기 동안 만든 저장소와 공개 주소도 지우지 않는다. 14주차에 쓴 README 최종판이 한 학기 작업의 첫 화면이다. 마지막으로 그 안에 실명·학번·실제 이메일이 남아 있지 않은지 본다.
풀어 보지 못한 은행 문제는 방학에 같은 방법으로 풀어 본다. "이 문제의 값" 표의 값을 스스로 바꿔 다시 풀면 시험과 같은 연습이 된다. 기준은 늘 "확인할 것"이다.

## 공식 참고 자료

- [첫 번째 웹사이트 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Getting_started/Your_first_website)
- [미디어 쿼리 시작하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/CSS_layout/Media_queries)
- [JavaScript 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [첫 번째 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [JSON 다루기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/JSON)
- [Console 개요 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console?hl=ko)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
- [기기 모드로 모바일 기기 시뮬레이션 — Chrome DevTools](https://developer.chrome.com/docs/devtools/device-mode)
- [기본 쓰기 및 서식 지정 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [새 리포지토리 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
