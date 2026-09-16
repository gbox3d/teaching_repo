# 13주차 — 보안·접근성·릴리스 점검

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

## 이번 주 질문

> 지금까지 만든 네 페이지를, **다른 사람이 써도 안전하고 누구나 읽을 수 있게** 다듬어 내놓을 수 있을까?

12주차까지 `my-web`에는 네 페이지가 생겼다. 홈·내 정보·방명록·프로젝트다.
이번 주에는 새 기능을 거의 만들지 않는다. 대신 **입력한 글을 어떻게 화면에 넣는지**(`textContent`),
**그림과 입력 칸에 글이 붙어 있는지**(`alt`·`label for`), **링크가 다 열리는지**를 점검하고 고친다.
마지막에는 저장소 `README.md`를 최종판으로 다시 쓰고 화면 캡처 세 장을 넣는다. 이것이 14주차 발표에 그대로 쓰인다.

1일차에 `about.html`에 작은 폼 하나를 더 만든다. 입학 연도를 적으면 몇 년차인지 계산해 주는 폼이다.

## 학습 목표

1. `about.html`에 입학 연도 폼을 만들고 `about.js`에서 `Number()`·`isNaN()`·`new Date().getFullYear()`로 **n년차**를 계산해 보여 준다.
2. 같은 글자를 `textContent`로 넣을 때와 `innerHTML`로 넣을 때의 차이를 보고, 방명록이 `textContent`로 넣고 있는지 확인한다.
3. 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일이 없는지 본다.
4. 그림의 `alt`, 입력 칸의 `label for`, 링크·버튼 **글자**를 점검해 고친다.
5. 링크 404 → Console 오류 → 기기 모드 375px 순서로 점검하고, `README.md` 최종판과 `screenshots/` 3장을 정리한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/guestbook.html   (F12 기기 모드 375px)

         방명록
         홈
         내 정보
         방명록
         프로젝트
         남긴 글
         ┌─────────────────────────────────────┐
         │ · student02: <b>안녕</b> (2026. 9. 16.) [삭제] │
         └─────────────────────────────────────┘
         1개
         [전체 지우기]
         F12 › Console — 빨간 줄 없음
         ← 주소창이 함께 보이게 찍는다
```

`<b>안녕</b>`이 **굵은 글씨가 아니라 글자 그대로** 보이는 것이 이번 주 캡처의 핵심이다.
`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 오늘 문법 5분(`Number`·`isNaN`·`getFullYear`), `textContent`와 `innerHTML`, 개인정보 규칙, `alt`·`label for`, 점검 순서 | `about.html` 폼과 `about.js` → `<b>안녕</b>` 확인 → `alt`·`label`·링크 글자 수정 → 링크·Console·375 점검 | 확인용 캡처 |
| 2일차 | README 마크다운 네 가지, `screenshots/`, `git log --oneline` 붙이기, Pages source 두 방식, 14주차 발표 흐름 | `README.md` 최종판 → 저장소 첫 화면 확인 → 3분 리허설 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 12주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 이번 주에 새로 만드는 파일은 `about.js` 하나다. `screenshots/`에는 그림 세 장이 들어간다
- 브라우저 개발자 도구의 **Console** 탭과 **기기 모드**(**F12** → 왼쪽 위 휴대전화 아이콘 → 폭 **375**)
- 본인 GitHub Pages 공개 주소. **확인과 캡처는 이 주소에서만 한다**
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 글자로 넣기 | textContent | 按文字插入 |
| HTML로 넣기 | innerHTML | 按 HTML 插入 |
| 대체 글 | alt | 替代文字 |
| 이름표 연결 | label for | 标签关联 |
| 접근성 | accessibility | 无障碍 |
| 개인정보 | personal information | 个人信息 |
| 내놓기 전 점검 | release check | 发布前检查 |
| 화면 캡처 | screenshot | 屏幕截图 |

## 이번 주 범위

| 태그·API | 이번 주에 알아둘 뜻 |
|---|---|
| `element.textContent = 값` | 값을 **글자 그대로** 넣는다. `<b>안녕</b>`을 넣으면 화면에도 `<b>안녕</b>`이 보인다 |
| `element.innerHTML = 값` | 값을 **HTML로 해석해서** 넣는다. `<b>안녕</b>`을 넣으면 굵은 `안녕`이 된다 |
| `innerHTML = ''` | 목록을 **비울 때만** 쓴다(10주차). 입력한 글을 넣는 자리에는 쓰지 않는다 |
| `Number(글자)` | 글자를 숫자로 바꾼다. 숫자로 바꿀 수 없으면 `NaN`이 된다 |
| `isNaN(값)` | 그 값이 `NaN`이면 `true`. 숫자가 아닌 입력을 거를 때 쓴다 |
| `new Date().getFullYear()` | 오늘 날짜에서 **연도**만 꺼낸다. 2026년이면 `2026` |
| `img alt="…"` | 그림이 안 보일 때 대신 읽히는 글. 비워 두지 않는다 |
| `label for="year"` · `input id="year"` | 이름표와 입력 칸을 잇는다. 두 글자가 같아야 하며, 이름표를 누르면 커서가 입력 칸으로 간다 |
| 링크·버튼 글자 | 그 글자만 읽어도 어디로 가는지 알 수 있게 적는다. `여기를 누르세요`는 쓰지 않는다 |
| 개인정보 | 실명·학번·전화번호·실제 이메일·비밀번호. 공개 저장소와 캡처에 넣지 않는다 |
| README 마크다운 | 제목 `#`, 목록 `-`, 링크 `[보이는 글](https://주소)`, 그림(링크 앞에 `!`) 네 가지만 쓴다 |
| `git log --oneline` | 지금까지의 commit을 한 줄씩 본다. README "만든 과정"에 그대로 붙인다 |
| Pages source | 공개할 파일이 어느 브랜치에 있는지 정한다. 수업 표준은 `main` · `/(root)`다 |

허용 목록 기반 정리(sanitize), CSP, 자동 점검 도구 점수, 서버 권한 설정은 이번 주에 다루지 않는다.
`innerHTML`로 입력한 글을 넣는 방법도 가르치지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week13_release_security/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 시연용 예제: [security-demo.html](examples/security-demo.html) · [security-demo.js](examples/security-demo.js)
- 1일차 완성 코드: [about.html](examples/day1/about.html) · [about.js](examples/day1/about.js) · [projects.js](examples/day1/projects.js) · [guestbook.js](examples/day1/guestbook.js)
- 2일차 완성 코드: [README.md](examples/day2/README.md) · [screenshots/home.png](examples/day2/screenshots/home.png) · [guestbook.png](examples/day2/screenshots/guestbook.png) · [projects.png](examples/day2/screenshots/projects.png)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

## 완료 기준

- [ ] 공개 주소 `/my-web/about.html`에서 입학 연도를 적고 **계산하기**를 누르면 `…년차입니다.`가 보인다.
- [ ] 숫자가 아닌 글자를 적으면 `입학 연도를 숫자로 적어 주세요.`가 보인다.
- [ ] 방명록에 `<b>안녕</b>`을 남기면 목록에 **글자 그대로** 보인다.
- [ ] 네 페이지의 nav 링크가 모두 열리고, 각 페이지 Console에 빨간 줄이 없다.
- [ ] 기기 모드 **375px**에서 네 페이지가 가로로 밀리지 않는다.
- [ ] 저장소 `README.md` 최종판이 GitHub 첫 화면에 보이고 `screenshots/` 그림 세 장이 깨지지 않는다.
- [ ] 375px 공개 주소에서 `<b>안녕</b>`이 글자 그대로 보이는 화면을 캡처 1장으로 제출한다.

## 다음 수업 연결

이제 `my-web`은 내놓을 수 있는 상태가 되었다. 14주차에는 이 공개 주소를 그대로 열어 **3분 시연**을 한다.
페이지 이동 → 다크 모드 → 폼 빈값 안내 → 방명록 추가·삭제 → 새로고침해도 남는 목록 → JSON 카드 순서이며,
레포트는 이번 주에 쓴 `README.md` 최종판이다. 15주차 기말 리허설 자료는 2일차에 공개한다.

## 공식 참고 자료

- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [Element.innerHTML — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/innerHTML)
- [img 요소의 alt — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/img)
- [label 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/label)
- [Number() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Number/Number)
- [isNaN() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/isNaN)
- [Date.prototype.getFullYear() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/getFullYear)
- [기본 작성 및 서식 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [리포지토리 README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Pages 사이트에 대한 게시 원본 구성 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
