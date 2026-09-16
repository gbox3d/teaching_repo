# 10주차 — 배열 데이터를 목록으로 그리기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

## 이번 주 질문

> 방명록에 두 번째 글을 남기면 앞 글이 사라진다. 남긴 글을 **쌓아서** 목록으로 보여 주고, 필요 없는 줄을 지울 수 있을까?

7주차에는 제출한 값을 카드 한 줄(`#last`)에 표시했다. 한 줄뿐이라 새 글이 앞 글을 덮어썼다.
이번 주에는 남긴 글을 **배열**에 담고, 배열에 든 만큼 `<li>`를 만들어 목록으로 그린다.
1일차에는 글이 쌓이고 항목 수가 보이게 하고, 2일차에는 목록을 다시 그리는 함수 `showList()`를 만들어 항목마다 **[삭제]** 버튼을 붙인다.

## 학습 목표

1. `let items = []`에 `push`로 값을 쌓고 `items.length`와 `items[i]`로 꺼내 쓴다.
2. `for (let i = 0; i < items.length; i++)`로 배열을 처음부터 끝까지 훑는다.
3. `document.createElement('li')`·`textContent`·`list.append(li)`로 화면에 목록 한 줄을 만들어 붙인다.
4. `list.innerHTML = ''`로 목록을 비운 뒤 배열 전체를 다시 그리는 함수 `showList()`를 쓴다.
5. 삭제 버튼 틀(`createElement('button')`·`splice(i, 1)`·`showList()`)을 붙여 항목 하나를 지우고 항목 수를 함께 갱신한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/guestbook.html
         글 3개를 남긴 뒤 가운데 한 줄의 [삭제]를 누른 화면

         남긴 글
         · student01: 안녕하세요        [삭제]
         · student03: 반갑습니다        [삭제]
         2개                            ← 3개에서 하나를 지워 2개
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 오늘 문법(배열 `push`·`length`·`[i]`·`for`), `createElement`·`append`, 7주 코드에 다섯 줄 더하기, 항목 수와 데이터가 가는 세 곳 | `guestbook.html`에 목록 자리 → 배열에 쌓기 → `<li>` 만들어 붙이기 → `N개` 표시 → 빈 이름 확인 | 확인용 캡처 |
| 2일차 | 지우려면 두 곳을 바꿔야 한다, `showList()`로 다시 그리기, 삭제 버튼 복붙 틀, 지운 뒤 확인 | `showList()`로 교체 → 삭제 버튼 → 항목 수 갱신 → 빈 목록 안내 → push·캡처 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 9주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 7주차에 만든 `guestbook.html`·`guestbook.js`. 이번 주에 고치는 파일은 이 둘뿐이다
- 브라우저 개발자 도구의 **Console** 탭 (**F12** 또는 우클릭 › 검사)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 배열 | array | 数组 |
| 뒤에 더하기 | push | 追加 |
| 개수 | length | 长度 |
| 반복 | for loop | 循环 |
| 요소 만들기 | createElement | 创建元素 |
| 붙이기 | append | 追加到 |
| 목록 항목 | list item (`li`) | 列表项 |
| 하나 빼기 | splice | 删除一项 |

## 이번 주 범위

| 태그·API | 이번 주에 알아둘 뜻 |
|---|---|
| `let items = []` | 값을 여러 개 담아 두는 상자. 처음에는 비어 있다. 값이 바뀌므로 `const`가 아니라 `let`으로 쓴다 |
| `items.push(값)` | 배열 **뒤에** 값을 하나 더한다. 쌓이는 자리는 늘 맨 뒤다 |
| `items.length` | 배열에 든 값의 개수. 항목 수 표시에 그대로 쓴다 |
| `items[i]` | 배열의 `i`번째 값. 번호는 `0`부터 센다 |
| `for (let i = 0; i < items.length; i++)` | `i`를 0부터 하나씩 올리며 배열을 끝까지 훑는다. **몇 번째인지(`i`)가 필요해서** 이 모양을 쓴다 |
| `document.createElement('li')` | 화면에 아직 붙지 않은 새 `<li>`를 만든다 |
| `li.textContent = …` | 만든 요소 안의 글자를 정한다. 7주차에 쓴 것과 같다 |
| `list.append(li)` | 만든 요소를 `<ul id="list">` 안에 **붙인다.** 붙여야 화면에 보인다 |
| `list.innerHTML = ''` | 목록을 통째로 **비운다.** 이 수업에서 `innerHTML`은 비우기에만 쓴다 |
| `showList()` | 목록을 비우고 배열 전체를 처음부터 다시 그리는 함수. 추가·삭제 뒤에 부른다 |
| `items.splice(i, 1)` | 배열의 `i`번째 값 하나를 뺀다. **삭제 버튼 틀** 안에서만 쓴다 |
| `<ul class="card" id="list"></ul>` | 목록이 들어갈 빈 상자. 비어 있는 채로 HTML에 두고 JavaScript가 채운다 |

새로고침해도 목록이 남게 하는 것(`localStorage`)은 11주차, 파일에서 데이터를 불러오는 `fetch`는 12주차다.
`map`·`filter`·`forEach`와 이벤트 위임은 이 과목에서 쓰지 않는다. `innerHTML`로 입력한 글을 넣는 방법도 쓰지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week10_supabase_data/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [guestbook.html](examples/day1/guestbook.html) · [guestbook.js](examples/day1/guestbook.js) · [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [app.js](examples/day1/app.js) · [styles.css](examples/day1/styles.css)
- 2일차 완성 코드: [guestbook.html](examples/day2/guestbook.html) · [guestbook.js](examples/day2/guestbook.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`이 열린다.
- [ ] 이름과 메시지를 넣고 **[남기기]**를 누를 때마다 `남긴 글` 목록에 한 줄씩 **쌓인다**.
- [ ] 목록 아래에 `3개`처럼 항목 수가 보이고, 글을 남길 때마다 숫자가 오른다.
- [ ] 항목마다 **[삭제]** 버튼이 있고, 누르면 그 줄만 사라지며 항목 수가 함께 줄어든다.
- [ ] 목록이 비면 `아직 남긴 글이 없습니다.`가 보인다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 글 3개를 남기고 하나를 지워 `2개`가 보이는 화면을 주소창과 함께 캡처 1장으로 제출한다.

## 다음 수업 연결

이번 주 목록은 **화면에만** 있다. 새로고침하면 `아직 남긴 글이 없습니다.`로 돌아간다.
11주차에는 항목을 `{ 이름, 메시지, 날짜 }` 객체로 바꾸고 `localStorage`에 저장해 **새로고침해도 남게** 한다.
그때부터 확인과 캡처는 공개 주소에서만 한다. 12주차에는 JSON 파일에서 데이터를 불러와 카드로 그린다.

## 공식 참고 자료

- [배열 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array)
- [Array.prototype.push() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/push)
- [Array.prototype.splice() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)
- [for — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/for)
- [Document.createElement() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/createElement)
- [Element.append() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/append)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [ul 요소 — MDN](https://developer.mozilla.org/ko/docs/Web/HTML/Reference/Elements/ul)
