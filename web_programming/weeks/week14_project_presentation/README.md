# 14주차 — 최종 프로젝트 발표

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation

## 이번 주 질문

> 3~13주에 한 주씩 쌓아 온 내 사이트를, 공개 주소 하나로 **3분 안에** 남에게 보여 줄 수 있을까? 그리고 그 설명을 저장소 첫 화면에 한 장으로 남길 수 있을까?

9주차에는 세 페이지짜리 사이트를 2분 동안 보여 주었다. 그 뒤 10주차에 방명록 목록 추가·삭제가, 11주차에 새로고침해도 남는 저장이,
12주차에 JSON 파일에서 읽어 오는 프로젝트 카드가 늘었고, 13주차에 네 페이지를 점검하고 `README.md` 최종판을 썼다.
이번 주에 보여 주는 것은 그 `my-web` 한 저장소다. 1일차에는 마지막 손질을 하고 3분 리허설을 하며, 2일차 90분이 발표다.

## 학습 목표

1. 공개 주소 → 페이지 이동 → 버튼 → 폼 빈값 안내 → 목록 추가·삭제 → 새로고침 유지 → JSON 카드 → **Commits** 탭 순서로 3분 발표를 한다.
2. 발표 순서를 `examples/demo_outline.md`의 8줄 표로 미리 정하고, 그 순서를 홈 화면의 목록으로도 적어 둔다.
3. 내 정보 표에 채점자가 열 **공개 주소**를 한 줄 적는다.
4. 13주차 `README.md` 최종판에 이번 주 commit 한 줄을 더해 레포트를 마무리한다.
5. 공개 주소가 열리지 않을 때 쓰는 대체 절차(시크릿 창 → 로컬 시연)를 말할 수 있다.
6. 구술 질문 한 문항("이 버튼을 누르면 어느 함수가 실행됩니까?")에 답한다.

## 이번 주 결과물

```text
[발표 3분] https://student01.github.io/my-web/
           홈 → 네 페이지 → 다크 모드 → 폼 빈값 안내 → 목록 추가·삭제
           → 새로고침 유지 → JSON 카드 → Commits 탭

[레포트]   https://github.com/student01/my-web 의 첫 화면에 보이는 README.md
           제목·공개 주소 / 기능 5개 / 캡처 3장 / 사용 기술·git log / 어려움과 해결 3줄
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.
이번 주는 주차별 실습 점수 대상이 아니라 **2차 과제 20점**(발표 12 + 레포트 8)이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 발표 순서와 3분 규칙, 채점표 20점, 3분 시연 흐름 표 8줄, 공개 주소가 안 열릴 때, 좋은 시작·피할 시작 | 홈에 할 수 있는 것 목록 → 내 정보에 공개 주소 → README 마무리 → push → 조교 1:1 확인 → 3분 리허설 | 저장소 첫 화면의 README |
| 2일차 | 오늘 순서와 준비, 채점표와 구술 1문항, 공개 주소가 안 열리면 | **발표 3분 × 인원** — 공개 주소에서 여덟 가지를 순서대로 보여 준다 | 발표와 제출 |

1일차는 `설명·함께 따라하기 30분 + 실습 60분`이다.
**2일차는 90분 전체가 발표다.** 앞 30분에 안내 5분과 1~8번 발표(5–29분)가 들어가고, 뒤 60분에 나머지 발표와 총평이 들어간다.

## 준비

- 13주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 네 페이지(`index.html`·`about.html`·`guestbook.html`·`projects.html`)와 `styles.css`·`app.js`·`about.js`·`guestbook.js`·`projects.js`·`data/projects.json`·`images/`·`screenshots/`
- 빠진 파일이 있으면 [따라하기의 이번 주에 고치지 않는 파일](walkthrough.md#이번-주에-고치지-않는-파일)에서 그대로 가져온다
- 과제 안내와 채점 기준을 미리 읽는다: [2차 과제 안내](project_brief.md) · [채점표](rubric.md) · [3분 시연 흐름 표](examples/demo_outline.md)
- **확인과 캡처는 공개 주소에서 한다.** 방명록 목록은 내 PC에서 파일을 더블클릭해 연 화면과 공개 주소가 서로 다른 곳에 저장된다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 최종 발표 | final presentation | 期末展示 |
| 시연 | demo | 演示 |
| 시연 흐름 표 | demo outline | 演示流程表 |
| 레포트 | report (README) | 报告 |
| 채점표 | rubric | 评分表 |
| 공개 주소 | public URL (GitHub Pages) | 公开网址 |
| 구술 질문 | oral question | 口头提问 |
| 시크릿 창 | incognito window | 无痕窗口 |

## 이번 주 범위

| 명령·용어 | 이번 주에 알아둘 뜻 |
|---|---|
| 3분 시연 | 공개 주소에서 여덟 가지를 순서대로 보여 주는 것. 코드 파일은 띄우지 않는다 |
| `examples/demo_outline.md` | 시간 · 화면·동작 · 말할 것 세 칸으로 된 8줄 표. 발표 순서를 미리 적어 두는 종이다 |
| `<h2>`·`<ol>`·`<li>` | 홈에 "이 사이트에서 할 수 있는 것" 다섯 줄을 넣을 때 쓴다. 3주차에 배운 태그다 |
| `<tr>`·`<td>` | 내 정보 표에 "공개 주소" 한 행을 더할 때 쓴다. 3주차에 배운 태그다 |
| GitHub **Commits** 탭 | 저장소에 쌓인 commit 목록. 발표 마지막 25초에 보여 준다 |
| `git log --oneline` | 내 PC에서 같은 목록을 보는 명령. README 마지막 절에 옮겨 적는다 |
| 시크릿 창 | 로그인하지 않은 상태로 여는 브라우저 창. 채점자가 보는 화면과 같다 |
| 공개 주소 | `https://<아이디>.github.io/my-web/`. 발표·채점·캡처가 모두 이 주소에서 이루어진다 |
| `screenshots/` | 캡처를 넣는 폴더. 13주차에 세 장으로 늘렸다 |
| README 최종판 | 제목·공개 주소 / 페이지 / 기능 / 화면 / 사용 기술 / 어려움과 해결 / 만든 과정. 이것이 레포트다 |
| 장애 대체 | 공개 주소가 안 열릴 때 시크릿 창 → 로컬 시연 순서로 같은 배점을 받는 절차 |
| 구술 질문 | 발표 중 한 문항. 예: "이 버튼을 누르면 어느 함수가 실행됩니까?" |

새 태그·새 API는 이번 주에 없다. 3~13주에 쓴 것만 쓴다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week14_project_presentation/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [2차 과제 안내](project_brief.md) · [채점표 20점](rubric.md)
- [3분 시연 흐름 표](examples/demo_outline.md)
- [예제 설명](examples/README.md)
- README 최종판 예: [examples/day1/README.md](examples/day1/README.md)
- 캡처 3장 예: [home.png](examples/day1/screenshots/home.png) · [guestbook.png](examples/day1/screenshots/guestbook.png) · [projects.png](examples/day1/screenshots/projects.png)
- 발표에서 보여 줄 파일: [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [guestbook.html](examples/day1/guestbook.html) · [projects.html](examples/day1/projects.html) · [styles.css](examples/day1/styles.css) · [app.js](examples/day1/app.js) · [about.js](examples/day1/about.js) · [guestbook.js](examples/day1/guestbook.js) · [projects.js](examples/day1/projects.js) · [data/projects.json](examples/day1/data/projects.json)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation

## 완료 기준

- [ ] `https://<아이디>.github.io/my-web/`이 시크릿 창에서 열리고 nav로 네 페이지를 오갈 수 있다.
- [ ] 홈에 "이 사이트에서 할 수 있는 것" 다섯 줄이 보이고, 그 순서가 내 발표 순서와 같다.
- [ ] 내 정보 표에 **공개 주소** 행이 있다.
- [ ] 방명록에서 글을 남기고 지울 수 있고, 새로고침해도 남아 있다.
- [ ] 프로젝트 페이지에 카드 세 장이 보인다.
- [ ] 저장소 첫 화면에 README 최종판과 캡처 3장이 보인다.
- [ ] 저장소 첫 화면을 **캡처 1장**으로 제출했다.
- [ ] 2일차에 3분 발표를 했다.

## 다음 수업 연결

15주차는 기말 개인 실기다. 범위는 2~13주이고, 오늘 발표한 `my-web`이 아니라 **새 저장소의 시험용 폴더**에서 혼자 만든다.
1일차에 리허설을 하며 저장소를 만들고 Pages를 켜고, 2일차 60분이 본시험이다. 구현 15점 + 시연 5점이며 시연은 제출한 공개 주소를 채점자가 직접 여는 것으로 본다.
13주차 2일차에 공개한 리허설 starter와 채점표를 다시 읽어 온다.

## 공식 참고 자료

- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기본 쓰기 및 서식 지정 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [리포지토리의 커밋 기록 보기 — GitHub Docs](https://docs.github.com/ko/repositories/viewing-activity-and-data-for-your-repository/viewing-a-summary-of-repository-activity)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [ol 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/ol)
- [table 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/table)
