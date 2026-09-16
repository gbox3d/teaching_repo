# 6주차 — DOM·이벤트·브라우저 CRUD

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

## 이번 주 질문

> 5주차에 복붙 틀로 쓴 `document.querySelector('#greeting').textContent = …` 한 줄은 무엇이었을까? 버튼을 눌렀을 때 화면을 바꾸려면 무엇이 더 필요할까?

5주차 코드는 페이지를 열 때 **한 번** 실행됐다. 값을 만들고 함수로 인사말을 조립해 카드 한 줄에 띄웠다.
이번 주에는 그 한 줄을 뜯어 본다. `document`가 무엇인지, `querySelector`가 무엇을 돌려주는지 보고
**버튼을 눌렀을 때** 실행되는 코드를 쓴다. 1일차에는 인사 바꾸기 버튼과 클릭 횟수, 2일차에는 다크 모드 버튼을 만든다.
이번 주 작업은 `dark-mode` 브랜치에서 하고 2일차 끝에 main에 합친다.

## 학습 목표

1. HTML 파일과 브라우저가 만든 DOM이 어떻게 다른지 말하고, DevTools **Elements** 탭에서 내 요소를 찾는다.
2. `document.querySelector('#id')`로 요소 하나를 찾아 `const`에 담고, 못 찾으면 `null`이 된다는 것을 확인한다.
3. `textContent`로 요소 안의 글자를 바꾼다.
4. `addEventListener('click', function () { })`로 버튼을 눌렀을 때 실행되는 코드를 쓰고, `let count`로 클릭 횟수를 센다.
5. `classList.toggle('dark')`와 `body.dark` CSS 규칙으로 다크 모드를 켜고 끄며, 두 버튼이 같은 함수를 쓰게 정리한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/
         배경이 어두운 화면 ─ [인사 바꾸기] [다크 모드]
         카드 한 줄 ─ 반갑습니다. 오늘도 좋은 하루 되세요.
         카드 한 줄 ─ 클릭 3회
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.
클릭 횟수는 몇 번이든 된다. `클릭 0회`가 아니라 **1 이상**이면 눌러 본 것이 보인다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `git switch -c dark-mode`, HTML과 DOM, `querySelector`, `textContent`, `addEventListener('click')`와 `let count` | 버튼 1개와 `<p id="count">` 자리 만들기 → 클릭하면 인사말 교체 → 클릭 횟수 세기 → `null` 오류 두 가지 고치기 → 브랜치에 push | 확인용 브랜치 목록 화면 |
| 2일차 | `merge`와 브랜치 정리, `classList.add / remove / toggle`, `body.dark`, 함수 재사용, 8주차 중간 실기 예고 | 다크 모드 버튼 → 두 버튼이 한 함수를 쓰게 정리 → main에 merge → 375·1280 확인 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 5주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 브라우저 개발자 도구의 **Elements** 탭과 **Console** 탭 위치 (**F12** 또는 우클릭 › 검사)
- 5주차에 만든 `#greeting` 문단과 `greet(name)`·`hello(hour)` 함수. 이번 주에 그대로 이어서 쓴다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 문서 객체 모델 | DOM (Document Object Model) | 文档对象模型 |
| 요소 찾기 | querySelector | 查找元素 |
| 글자 내용 | textContent | 文本内容 |
| 이벤트 | event | 事件 |
| 이벤트 등록 | addEventListener | 注册事件监听 |
| class 목록 | classList | 类名列表 |
| 붙였다 뗐다 하기 | toggle | 切换 |
| 다크 모드 | dark mode | 深色模式 |

## 이번 주 범위

| 태그·명령·API | 이번 주에 알아둘 뜻 |
|---|---|
| DOM | 브라우저가 내 HTML을 읽어 만든 **요소 상자들**. 화면에 보이는 것은 이쪽이다 |
| `document` | 페이지 전체. 브라우저가 미리 만들어 두며 JavaScript는 이것부터 시작한다 |
| `document.querySelector('#greeting')` | `id`가 `greeting`인 요소 **하나**를 찾아 돌려준다. 못 찾으면 `null` |
| `.textContent` | 요소 안의 **글자**. `=` 오른쪽에 두면 읽고, 왼쪽에 두면 바꿔 넣는다 |
| `addEventListener('click', function () { })` | "이 요소를 클릭하면 이 함수를 실행하라"고 브라우저에 미리 맡겨 둔다 |
| `let count = 0;` · `count = count + 1;` | 클릭 횟수를 세는 값. 함수 **밖**에 두어야 값이 쌓인다 |
| `document.body` | `<body>` 요소. 페이지 전체의 색을 바꿀 때 쓴다 |
| `classList.toggle('dark')` | class `dark`가 없으면 붙이고, 있으면 뗀다. `add`는 붙이기만, `remove`는 떼기만 한다 |
| `body.dark { … }` | `<body>`에 class `dark`가 붙었을 때만 적용되는 CSS 규칙 |
| `git switch -c dark-mode` | 브랜치를 만들면서 그 브랜치로 옮겨 간다 (3주차 복습) |
| `git merge dark-mode` | 지금 있는 브랜치(main)에 `dark-mode`의 commit을 합친다 |
| `git branch -d dark-mode` | 합치고 **push까지 끝난** 브랜치를 지운다 |

목록 추가·삭제(10주차), 새로고침해도 남는 저장(11주차), 폼 제출 읽기(7주차)는 이번 주에 다루지 않는다.
`innerHTML`로 글 넣기, 이벤트 위임, 화살표 함수(`() =>`)는 이 과목에서 쓰지 않는다. 2주차 `app.js`의 `() =>`는 틀로만 본 것이다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week06_dom_crud/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [index.html](examples/day1/index.html) · [app.js](examples/day1/app.js) · [styles.css](examples/day1/styles.css) · [about.html](examples/day1/about.html) · [guestbook.html](examples/day1/guestbook.html)
- 2일차 완성 코드: [index.html](examples/day2/index.html) · [app.js](examples/day2/app.js) · [styles.css](examples/day2/styles.css)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/`에 버튼 두 개가 보인다.
- [ ] **다크 모드** 버튼을 누르면 배경과 카드가 어두워지고, 다시 누르면 돌아온다.
- [ ] **인사 바꾸기** 버튼을 누르면 카드의 인사말이 바뀐다.
- [ ] 버튼을 누른 만큼 `클릭 N회`의 숫자가 올라간다(`N`은 1 이상).
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 다크 모드가 켜진 화면을 주소창과 함께 캡처 1장으로 제출한다.

## 다음 수업 연결

이번 주에는 **버튼**을 눌렀을 때 화면을 바꿨다. 7주차에는 **폼을 제출했을 때** 화면을 바꾼다.
3주차에 만들어 두고 "눌러도 주소창만 바뀐다"고 적어 둔 `guestbook.html`의 [남기기] 버튼이 그 자리다.
`addEventListener`는 그대로 쓰고 `'click'` 대신 `'submit'`을, 그리고 입력 칸의 값을 읽는 `input.value`를 배운다.
8주차 중간 실기 범위(2~7주차)는 7주차에 모두 채워진다.

## 공식 참고 자료

- [DOM 소개 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document_Object_Model/Introduction)
- [문서에서 DOM 요소 선택하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/DOM_scripting)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
- [git merge — Git 공식 문서](https://git-scm.com/docs/git-merge)
