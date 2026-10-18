[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# 8주차 — 중간 개인 실기

이번 주는 새 내용을 배우지 않는다. 1~7주 실습에서 **실제로 제출한 것**을 한 문제씩으로 정리한 **문제 은행**으로 연습하고(1일차), 같은 문제를 값만 바꾼 **중간 실기**를 본다(2일차).
은행 문제는 수업에서 한 실습을 그대로 다시 하는 수준이다. 문제마다 **힌트**가 있고, 해답 대신 **확인할 것**이 있다. 화면과 F12 로 그 항목을 하나씩 맞춰 보면 스스로 맞았는지 안다.

## 이번 주 질문

> 수업에서 한 번씩 해 본 것을, 값이 바뀐 문제지만 보고 **혼자 시간 안에** 다시 만들 수 있을까?

답은 코드를 외우는 것이 아니다. 문제 문장을 읽는 순서와, 맞았는지 스스로 확인하는 방법이다.
시험 문제는 은행 문제와 문장·할 일·확인하는 방법이 같고 **값만 다르다**. 1일차에 은행 문제로 "읽기 → 받기 → 열기 → 할 일 → 확인할 것 맞추기"를 손에 익히면, 2일차에는 바뀐 값으로 같은 순서를 밟는다.

## 학습 목표

1. 은행 문제 하나를 읽고 "시작 파일"·"할 일"·"확인할 것"·"힌트"·"이 문제의 값"이 각각 무엇을 말하는지 구분한다. 시험에서는 "이 문제의 값" 표의 값만 바뀐다.
2. 문제 폴더를 **Raw** 로 받아 열고(두 번 눌러 열기 또는 `node server.mjs`), "확인할 것"을 화면·F12(Console·Network·Elements)로 하나씩 맞춘다. 해답 없이 맞았는지 스스로 판단한다.
3. 수업에서 나간 범위의 은행 문제를 모두 한 번씩 풀어 둔다. 어디서 막혔는지 알고 시험에 간다.
4. 2일차에 분반 공지가 정한 형식대로 답안(코드·실행 화면 캡처·자기 말로 쓴 짧은 설명)을 시간 안에 낸다.

## 이번 주 결과물

```text
1일차  은행 문제를 푼 폴더들 — 연습용, 점수 없음
       (저장소에 올려 두면 공개 주소 https://student01.github.io/web-week08/w04_box_style/ 로 다시 볼 수 있다)
2일차  중간 실기 답안 — 코드 + 실행 화면 캡처 + 설명 1~2문장. 내는 곳과 형식은 분반 공지
```

- 이번 주는 주차별 실습 점수 대상이 아니라 **중간 실기 20점**으로 본다. 기준은 [채점표](rubric.md)에 있다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 이번 주는 문제 은행과 시험(같은 문제·값만 바뀜·해답 비공개·확인할 것·힌트) → 문제 하나 읽는 법([w04_box_style](examples/w04_box_style/)) → 확인하는 법(열기, F12 Console·Network·Elements) → 오늘 순서 | 수업에서 나간 범위의 은행 문제를 차례로 풀기 → 문제마다 받기 → 열기 → 할 일 → "확인할 것" 맞추기 → 올리기(선택) | 연습 폴더 |
| 2일차 | 시험 규칙(분반 공지: 시간·문항 수·볼 수 있는 것·제출 방법) → 문제 읽는 순서 다시 보기 → 답안에 넣을 것(코드·캡처·설명) | **중간 실기** — 공지한 시간 안에 은행 문제를 값만 바꾼 문제를 풀고 답안을 낸다 | 제출 |

각 수업은 `설명 30분 + 실습 60분` 이다. 2일차 실습 시간 중 공지한 시간이 **평가 시간**이다. 분 단위 순서는 [실습지](lab.md)에 있다.

## 준비

- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). `node -v` 로 확인한다. [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더 맨 위에 받아 `node server.mjs` 로 띄운다([사용 안내](../../tools/static-server/README.md)). Node 가 없는 PC 는 파일을 두 번 눌러 연다. 다만 F12 › Network 의 Status 번호(`200`·`404`)는 서버로 연 주소나 공개 주소에서만 보인다
- GitHub 로그인. w02 문제와 올리기에 쓴다. 저장소는 이번 주 `web-week08` 하나다
- 1~7주 실습지. 은행 문제마다 제목 아래 줄의 출처 링크가 그 주 실습지의 제출 절이다. 시험 중에 볼 수 있는 것은 분반 공지를 따른다
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
| 힌트 | hint | 提示 |
| 이 문제의 값 | values of this problem | 本题的值 |
| 영역 | section (A~D) | 考查部分 |
| 채점표 | rubric | 评分表 |

## 이번 주 범위

시험은 1~7주 실습 제출에서만 낸다. 은행 문제는 일곱 개다. 범위는 1~7주 가운데 **수업에서 나간 주차까지**다. 아직 배우지 않은 주의 문제(예: JavaScript 를 아직 안 했으면 w06·w07)는 시험에 내지 않는다. 어디까지인지는 분반 공지에 적는다.

| 영역 | 출처 주 | 은행 문제 | 수업에서 한 것 | 권장 |
|---|---|---|---|---:|
| A HTML | [1주차 실습 제출](../week01_web_git/lab.md#제출--캡처-두-장) | [w01_first_page](examples/w01_first_page/) 첫 페이지 만들기 | h1·p·ul 을 쓴 첫 페이지, 두 번 눌러 열기와 서버로 열기 | 8분 |
| A HTML | [2주차 실습 제출](../week02_github_pages/lab.md#제출--캡처-네-장) | [w02_push_repo](examples/w02_push_repo/) 고치고 올리기 | 파일 고친 뒤 `add` → `commit` → `push`, GitHub 화면 확인 | 10분 |
| A HTML | [3주차 실습 제출](../week03_semantic_html/lab.md#제출--캡처-한-장) | [w03_second_page](examples/w03_second_page/) 새 페이지와 링크로 오가기 | 두 번째 페이지와 상대 경로 링크 | 10분 |
| B CSS | [4주차 실습 제출](../week04_responsive_css/lab.md#제출--캡처-한-장) | [w04_box_style](examples/w04_box_style/) 상자 꾸미기와 글자 가운데 | 배경색·글자색·테두리·padding, flex column 으로 가운데 | 10분 |
| B CSS | [4주차 실습 제출](../week04_responsive_css/lab.md#제출--캡처-한-장) | [w05_box_position](examples/w05_box_position/) 틀 안의 상자를 지정 위치에 | `justify-content`·`align-items` 로 상단 중앙·하단 우측 같은 위치 | 10분 |
| C JavaScript·DOM | [6주차 실습 제출](../week06_dom_crud/lab.md#제출--캡처-한-장) | [w06_click_text](examples/w06_click_text/) 버튼을 누르면 글자와 횟수가 바뀐다 | `querySelector`·`addEventListener`·`textContent`·`let` 변수 | 10분 |
| D 폼 | [7주차 실습 제출](../week07_async_modules/lab.md#제출--캡처-한-장) | [w07_form_line](examples/w07_form_line/) 입력 칸을 읽어 한 줄로 보여 주기 | `submit`·`preventDefault`·`value`·빈값 안내 | 10분 |

문제 이름을 누르면 문제 문장(시작 파일·할 일·확인할 것·힌트·이 문제의 값·받기와 올리기)과 시작 파일이 보인다. 은행 전체 목록은 [examples/README.md](examples/README.md)다.

**범위 밖**: 미디어 쿼리·반응형(수업에서 안 했으면), 배열로 목록 그리기(10주), `localStorage`(11주), `fetch`·JSON(12주), ES Module, 외부 라이브러리·CDN.
범위 밖 기능을 넣어도 가점은 없다. 그 때문에 요구 동작이 멈추면 그 문제에서 감점한다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week08_midterm/index.html
- [순서대로 따라하기](walkthrough.md) — 1일차 연습 절차, 2일차 시험 날 절차
- [실습과 시험 안내](lab.md)
- [시험 구조](exam_structure.md) · [채점표 20점](rubric.md)
- [문제 은행 목록](examples/README.md) — 1~7주 문제 일곱 개
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 15주 기말 은행(1~14주 누적, 이번 주 일곱 문제 포함): [15주차 문제 은행](../week15_final_exam/examples/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

## 완료 기준

- [ ] 1일차: 수업에서 나간 범위의 은행 문제를 풀어 "확인할 것"을 스스로 맞춰 봤고, 맞추지 못한 항목이 무엇인지 안다.
- [ ] 1일차: 저장소 `web-week08` 이 있고(w02 문제에서 올려 봤고) GitHub 로그인이 된다.
- [ ] 2일차: 공지한 시간 안에 문제를 풀고, 코드·실행 화면 캡처·설명을 공지한 곳에 냈다.
- [ ] 2일차: 캡처에 실명·학번·실제 이메일이 보이지 않는다.

## 다음 수업 연결

[9주차](../week09_architecture_project/README.md)는 **1차 과제 발표**다. 지금까지 만든 내 사이트를 공개 주소로 2분 동안 보여 주고, 그 사이트를 소개하는 `README.md` 1차판을 저장소 첫 화면에 쓴다.
15주 기말 실기도 이번 주와 같은 방식이다. 기말 은행은 1~14주 누적이라 이번 주 일곱 문제도 들어 있고, 다시 나오면 8주와 다른 값으로 나온다.

## 공식 참고 자료

- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Git에서 GitHub 자격 증명 캐싱 — GitHub Docs](https://docs.github.com/ko/get-started/git-basics/caching-your-github-credentials-in-git)
- [Console 개요 — Chrome DevTools](https://developer.chrome.com/docs/devtools/console?hl=ko)
- [네트워크 활동 검사 — Chrome DevTools](https://developer.chrome.com/docs/devtools/network?hl=ko)
- [CSS 보기 및 변경 — Chrome DevTools](https://developer.chrome.com/docs/devtools/css?hl=ko)
- [플렉스박스의 기본 개념 — MDN](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- [첫 HTML 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
