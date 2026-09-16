# 7주차 — 폼 입력 읽기와 결과 표시

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

## 이번 주 질문

> 3주차에 만든 방명록 폼의 **[남기기]** 버튼은 눌러도 주소창만 바뀌고 아무 일도 일어나지 않았다. 입력한 이름과 메시지를 읽어 화면에 띄우려면 무엇이 더 필요할까?

6주차에는 **버튼을 클릭했을 때** 화면을 바꿨다. 이번 주에는 **폼을 제출했을 때** 화면을 바꾼다.
`addEventListener`는 그대로 쓰고 `'click'` 대신 `'submit'`을 쓰며, 입력 칸의 값을 읽는 `input.value`와
브라우저가 원래 하려던 일(페이지 새로고침)을 멈추는 `event.preventDefault()`를 배운다.
1일차에는 이름을 읽어 한 줄로 표시하고, 2일차에는 이름·메시지 두 칸을 모두 검사해 안내 문구까지 다듬는다.

## 학습 목표

1. `addEventListener('submit', function (event) { })`로 폼 제출을 받아 내 코드를 실행한다.
2. `event.preventDefault()`로 제출할 때 페이지가 새로고침되지 않게 막는다.
3. `input.value`·`textarea.value`와 `trim()`으로 입력 칸의 값을 읽는다.
4. 읽은 값을 템플릿 문자열로 만들어 `#last`에 `textContent`로 표시하고, `form.reset()`으로 폼을 비운다.
5. 이름·메시지가 비어 있으면 안내 문구를 띄우고 `focus()`로 커서를 옮긴 뒤 `return`으로 멈춘다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/guestbook.html
         이름 student01 · 메시지 안녕하세요 를 넣고 [남기기]를 누른 화면

         마지막으로 남긴 글
         student01: 안녕하세요        ← 카드 한 줄에 이렇게 보인다
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.
빈값 안내 문구(`이름을 입력하세요.`)는 실습 중에 눈으로 확인하는 것이고, 제출 캡처에는 없어도 된다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 3주차 폼 다시 보기, `submit`과 `preventDefault`, `value`와 `trim`, 결과 표시·빈값 안내·`focus`·`reset`, 8주차 중간 실기 공개 | `guestbook.js` 연결 → 제출 값 읽기 → `#last`에 한 줄 표시 → 이름 빈값 안내 → `reset` → 리허설 starter 열어 보기 | 확인용 캡처 |
| 2일차 | GitHub 웹에서 `README.md` 만들고 `git pull`, SSH 키 한 장(선택), 두 칸 검사와 안내 문구 지우기, 다음 입력 준비, 리허설·본시험 안내 | README 받아오기 → 메시지 빈값 안내 → 안내 문구 지우기 → 리허설 문항 하나 → push·캡처 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 6주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 3주차에 만든 `guestbook.html`의 폼(이름·이메일·메시지 칸과 **[남기기]** 버튼). 이번 주에 그 폼이 동작한다
- 브라우저 개발자 도구의 **Console** 탭 (**F12** 또는 우클릭 › 검사)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 폼 제출 | submit | 提交 |
| 원래 동작 막기 | preventDefault | 阻止默认行为 |
| 입력 값 | value | 输入值 |
| 앞뒤 공백 지우기 | trim | 去除首尾空格 |
| 안내 문구 | notice | 提示文字 |
| 커서 옮기기 | focus | 聚焦 |
| 폼 비우기 | reset | 重置表单 |
| 저장소 설명 파일 | README | 说明文件 |

## 이번 주 범위

| 태그·명령·API | 이번 주에 알아둘 뜻 |
|---|---|
| `<form id="guestbook-form">` | 입력 칸들을 묶는 상자. `id`를 붙여야 JavaScript가 찾을 수 있다 |
| `submit` 이벤트 | **[남기기]**를 누르거나 입력 칸에서 Enter를 쳤을 때 폼에서 일어나는 일 |
| `addEventListener('submit', function (event) { })` | 폼이 제출될 때 실행할 코드를 맡겨 둔다. 6주차 `'click'`과 같은 모양이다 |
| `event` | 방금 일어난 일에 대한 정보가 담긴 상자. 리스너 괄호 안에 이름을 적어 받는다 |
| `event.preventDefault()` | 브라우저가 원래 하려던 일(주소 끝에 `?`를 붙이고 새로고침)을 멈춘다 |
| `nameInput.value` | 입력 칸에 **지금 적혀 있는 글자**. `textarea`도 같다 |
| `.trim()` | 글자 앞뒤의 공백을 떼어 낸 값을 돌려준다. 공백만 친 칸을 빈칸으로 볼 때 쓴다 |
| `if (name === '') { … return; }` | 값이 비었으면 안내만 하고 **거기서 멈춘다**. `return`이 없으면 아랫줄이 그대로 실행된다 |
| `nameInput.focus()` | 그 입력 칸으로 커서를 옮긴다. 학생이 어디를 고쳐야 할지 바로 보인다 |
| `form.reset()` | 폼의 입력 칸을 모두 비운다. 제출이 끝난 뒤 다음 입력을 받을 준비다 |
| `'input'` 이벤트 | 입력 칸의 글자가 바뀔 때마다 일어난다. 2일차에 안내 문구를 지우는 데 쓴다 |
| GitHub 웹 편집 → `git pull` | GitHub 화면에서 파일을 만들면 내 PC에는 없다. `git pull`로 받아 온다 (2주차 부록 복습) |

새로고침해도 남는 목록(10·11주차), 서버에서 글을 받아 오는 `fetch`(12주차), ES Module(`import`/`export`)은 이번 주에 다루지 않는다.
ES Module과 번들러는 이 과목 범위 밖이다. `innerHTML`로 입력 글을 넣는 방법도 쓰지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week07_async_modules/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [guestbook.html](examples/day1/guestbook.html) · [guestbook.js](examples/day1/guestbook.js) · [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [app.js](examples/day1/app.js) · [styles.css](examples/day1/styles.css)
- 2일차 완성 코드: [guestbook.js](examples/day2/guestbook.js) · [README.md](examples/day2/README.md)
- 8주차 중간 실기 자료(1일차에 공개): [채점표](../week08_midterm/rubric.md) · [시험 구조](../week08_midterm/exam_structure.md) · [리허설 starter](../week08_midterm/examples/rehearsal_starter)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`이 열린다.
- [ ] 이름과 메시지를 넣고 **[남기기]**를 누르면 페이지가 새로고침되지 않는다.
- [ ] **마지막으로 남긴 글** 아래 카드에 `이름: 메시지`가 한 줄로 보인다.
- [ ] 누른 뒤 입력 칸이 비워지고 커서가 이름 칸에 있다.
- [ ] 이름을 비우고 누르면 `이름을 입력하세요.`가 보이고 글은 표시되지 않는다(2일차에는 메시지 칸도 같다).
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 결과가 보이는 화면을 주소창과 함께 캡처 1장으로 제출한다.

## 다음 수업 연결

이번 주로 8주차 중간 실기 범위(2~7주차 — Pages·HTML·CSS·DOM·폼)가 모두 채워졌다.
8주차 1일차는 시험과 같은 모양의 **리허설**이고, 2일차가 **본시험**이다. 본시험은 새 저장소를 만들지 않고 `my-web/exam/` 폴더에서 작업한다.
채점표와 리허설 starter는 이번 주 1일차에 공개하므로 미리 읽고 와도 된다.

지금은 두 번째로 글을 남기면 앞 글이 사라진다. 글을 **쌓아** 목록으로 보여 주는 것은 10주차,
새로고침해도 남게 하는 것은 11주차다.

## 공식 참고 자료

- [첫 번째 폼 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
- [HTMLFormElement: submit 이벤트 — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/submit_event)
- [Event.preventDefault() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Event/preventDefault)
- [HTMLInputElement — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLInputElement)
- [String.prototype.trim() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/String/trim)
- [HTMLElement.focus() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLElement/focus)
- [HTMLFormElement.reset() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/reset)
- [리포지토리에서 새 파일 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/working-with-files/managing-files/creating-new-files)
- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [새 SSH 키 생성 및 ssh-agent에 추가 — GitHub Docs](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) (선택)
