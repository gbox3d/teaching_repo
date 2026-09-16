# 11주차 — 객체와 localStorage

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

## 이번 주 질문

> 방명록에 남긴 글을 **새로고침해도 남게** 할 수 있을까? 그리고 한 줄에 이름·메시지·날짜 **세 값**을 함께 담을 수 있을까?

10주차에는 남긴 글을 배열에 쌓아 목록으로 그리고 항목마다 **[삭제]** 버튼을 붙였다.
다만 값이 `student01: 안녕하세요`라는 **문자열 한 덩어리**였고, 새로고침하면 목록이 사라졌다.
이번 주에는 항목을 `{ 이름, 메시지, 날짜 }` **객체**로 바꾸고, 목록을 브라우저 저장소(`localStorage`)에 저장해 새로고침해도 남게 한다.

**이번 주부터 확인과 캡처는 공개 주소에서만 한다.** 내 PC에서 파일을 직접 연 화면(`file://`)과 공개 주소는 저장되는 칸이 서로 다르다.

## 학습 목표

1. `{ name: …, message: …, date: … }` 객체를 만들고 `item.name`처럼 **점 표기**로 값을 꺼낸다.
2. 배열 안에 객체를 담고 `items[i].name`으로 "몇 번째 글의 어떤 값"을 읽는다.
3. `new Date().toLocaleDateString()` 한 줄로 오늘 날짜를 만들어 항목에 넣는다.
4. `JSON.stringify`로 배열을 문자열로 바꿔 `localStorage.setItem('guestbook', …)`에 저장한다.
5. `JSON.parse(localStorage.getItem('guestbook')) || []`로 페이지를 열 때 목록을 되살리고, `removeItem`으로 전체를 지운다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/guestbook.html
         글 3개를 남기고 새로고침한 뒤, F12 › Application › Local Storage를 함께 연 화면

         남긴 글
         · 하늘: 안녕하세요 (2026. 9. 16.)      [삭제]
         · 바다: 잘 봤습니다 (2026. 9. 16.)     [삭제]
         · 노을: 반갑습니다 (2026. 9. 16.)      [삭제]
         3개                                    ← 새로고침해도 그대로
         Key: guestbook  Value: [{"name":"하늘","message":"안녕하세요",…}]
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 오늘 문법(객체와 점 표기), 배열 안의 객체, 남긴 글을 객체로, 목록 한 줄에 이름·메시지·날짜 | 항목을 객체로 바꾸기 → 날짜 넣기 → 안내 문구 한 줄로 합치기 → Console에서 `items` 펼쳐 보기 | 확인용 캡처 |
| 2일차 | 새로고침하면 왜 사라지나, `JSON.stringify`와 `saveList()`, 열 때 되살리기, Application 탭과 전체 지우기 | `saveList()` → 복원 한 줄 → 전체 지우기 버튼 → 새로고침 확인 → push·캡처 | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 10주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 10주차에 만든 `guestbook.html`·`guestbook.js`. 이번 주에 고치는 파일도 이 둘뿐이다
- 브라우저 개발자 도구의 **Console** 탭과 **Application** 탭 (**F12** 또는 우클릭 › 검사)
- 본인 GitHub Pages 공개 주소. **이번 주 확인과 캡처는 이 주소에서만 한다**
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 객체 | object | 对象 |
| 속성 이름 | property | 属性 |
| 점 표기 | dot notation | 点号访问 |
| 문자열로 바꾸기 | JSON.stringify | 转成字符串 |
| 문자열을 되살리기 | JSON.parse | 解析字符串 |
| 브라우저 저장소 | localStorage | 浏览器本地存储 |
| 저장 키 | key | 键 |
| 저장 칸 지우기 | removeItem | 删除 |

## 이번 주 범위

| 태그·API | 이번 주에 알아둘 뜻 |
|---|---|
| `{ name: '하늘', message: '안녕하세요' }` | **객체**. 이름표가 붙은 값을 한 묶음으로 담는다. `이름: 값` 쌍을 쉼표로 잇는다 |
| `item.name` | **점 표기**. 객체에서 `name`이라는 이름표가 붙은 값을 꺼낸다. 따옴표를 붙이지 않는다 |
| `items[i].name` | 배열의 `i`번째 객체에서 `name` 값을 꺼낸다. "몇 번째 글의 이름"이다 |
| `new Date().toLocaleDateString()` | 오늘 날짜를 `2026. 9. 16.` 모양의 문자열로 만든다. **복붙 틀** 한 줄이다 |
| `localStorage` | 브라우저가 주소마다 하나씩 가지고 있는 작은 저장 칸. **문자열만** 넣을 수 있다 |
| `JSON.stringify(items)` | 배열·객체를 한 줄 문자열로 바꾼다. 저장하기 직전에 쓴다 |
| `JSON.parse(문자열)` | 저장해 둔 문자열을 다시 배열·객체로 되살린다. 읽은 직후에 쓴다 |
| `localStorage.setItem('guestbook', …)` | `guestbook`이라는 **키**에 문자열을 적어 둔다. 키 이름은 바꾸지 않는다 |
| `localStorage.getItem('guestbook')` | 적어 둔 문자열을 꺼낸다. 적어 둔 적이 없으면 `null`이다 |
| `localStorage.removeItem('guestbook')` | 그 키의 저장 칸을 통째로 지운다. **[전체 지우기]** 버튼이 쓴다 |
| `JSON.parse(getItem(…)) \|\| []` | "되살린 값이 없으면 빈 배열로." `\|\|`는 **또는**이다. 복붙 틀 한 줄이다 |
| `saveList()` | 지금 배열을 저장 칸에 적어 두는 함수. 추가한 뒤·삭제한 뒤에 부른다 |
| **F12 › Application › Local Storage** | 저장 칸의 키와 값을 눈으로 보는 탭. 제출 캡처에 이 화면이 함께 들어간다 |

서버에 저장해 다른 사람과 함께 보는 것(데이터베이스·로그인)은 이 과목의 선택 특강이다.
`sessionStorage`·쿠키·`??`는 쓰지 않는다. JSON 파일을 `fetch`로 불러오는 것은 12주차다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week11_auth_rls/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [guestbook.html](examples/day1/guestbook.html) · [guestbook.js](examples/day1/guestbook.js) · [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [app.js](examples/day1/app.js) · [styles.css](examples/day1/styles.css)
- 2일차 완성 코드: [guestbook.html](examples/day2/guestbook.html) · [guestbook.js](examples/day2/guestbook.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/guestbook.html`이 열린다.
- [ ] 글을 남기면 목록에 `하늘: 안녕하세요 (2026. 9. 16.)`처럼 이름·메시지·**날짜**가 함께 보인다.
- [ ] 브라우저를 새로고침해도 목록과 개수가 그대로 남아 있다.
- [ ] **F12 › Application › Local Storage**에 `guestbook` 키가 있고 값이 `[{"name":…}]` 모양이다.
- [ ] **[전체 지우기]**를 누르면 목록이 비고 `아직 남긴 글이 없습니다.`가 보이며, 새로고침해도 비어 있다.
- [ ] F12 Console에 빨간 줄이 없다.
- [ ] 글 3개를 남기고 새로고침한 뒤 Application 탭을 함께 연 화면을 캡처 1장으로 제출한다.

## 다음 수업 연결

이제 목록은 **내 브라우저 안**에 남는다. 다만 그 글은 나만 볼 수 있고, 다른 PC에서 열면 비어 있다.
12주차에는 `data/projects.json` 파일을 만들어 `fetch`로 불러오고, 읽어 온 값을 카드로 그린다.
JSON 파일의 글자 모양은 이번 주 Application 탭에서 본 값과 같다. 확인과 캡처는 12주차에도 공개 주소에서 한다.

## 공식 참고 자료

- [객체로 작업하기 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Working_with_objects)
- [속성 접근자 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Property_accessors)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [Storage.setItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/setItem)
- [Storage.getItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/getItem)
- [Storage.removeItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/removeItem)
- [JSON.stringify() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [JSON.parse() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- [Date.prototype.toLocaleDateString() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString)
