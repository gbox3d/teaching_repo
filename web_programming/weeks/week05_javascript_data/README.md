# 5주차 — JavaScript 데이터와 함수

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

## 이번 주 질문

> 3주차에 연결을 뺐던 `app.js`를 되살려, 변수와 함수로 만든 인사말을 `index.html`에 띄울 수 있을까?

4주차에는 `styles.css`로 세 페이지를 꾸몄다. 화면은 달라졌지만 페이지는 아직 아무 값도 만들지 않는다.
이번 주에는 `index.html`에 `<script src="app.js" defer></script>` 한 줄을 되살리고 `app.js`를 비운 뒤 새로 쓴다.
1일차에는 **화면을 건드리지 않고 Console에만 값을 찍는다.** 2일차에 `if`와 함수로 인사말을 만들어 화면 한 줄에 띄운다.

## 학습 목표

1. `<script src="app.js" defer></script>`로 JS 파일을 연결하고 `console.log`로 값을 Console에 찍는다.
2. Console의 빨간 오류 줄에서 `app.js:6` 같은 **파일 이름과 줄 번호**를 읽어 고친다.
3. `const`·`let`에 문자열과 숫자를 담고, 템플릿 문자열 `` `${}` ``로 문장을 만든다.
4. `if / else`와 비교 연산 `>=`·`===`로 두 문장 중 하나를 고른다.
5. `function`으로 하는 일에 이름을 붙이고, `return`한 값을 화면 한 줄에 띄운다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/my-web/
         카드 한 줄 ─ 안녕하세요, student01님! 좋은 아침입니다.
         F12 Console ─ 10
                       안녕하세요, student01님! 좋은 아침입니다.
         ← 주소창과 Console이 한 화면에 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 제출은 이 캡처 **한 장**이다.
12시가 지난 시간에 열면 `좋은 오후입니다.`가 나온다. 둘 다 정답이다.
2일차를 끝내지 못했다면 1일차 Console 캡처(여섯 줄)로 인정한다. JavaScript를 처음 쓰는 주여서 두는 완화다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `script` 줄 되살리기, `console.log`와 Console 오류 줄, `let`·`const`, 템플릿 문자열 | `app.js`를 비우고 값 만들기 → Console 확인 → 오타 내고 고치기 | 확인용 Console 화면 |
| 2일차 | `git revert HEAD`, `if / else`와 비교, `function`·`return`, 화면 한 줄 틀 | `if`로 인사 고르기 → 함수 두 개 → `#greeting`에 표시 → revert | 캡처 1 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 4주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 브라우저 개발자 도구를 여는 키 **F12**(또는 우클릭 › 검사)와 **Console** 탭 위치
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 변수 | variable | 变量 |
| 상수 | const (constant) | 常量 |
| 문자열 · 숫자 | string · number | 字符串 · 数字 |
| 템플릿 문자열 | template literal | 模板字符串 |
| 조건문 | if / else | 条件语句 |
| 비교 연산자 | comparison operator | 比较运算符 |
| 함수 | function | 函数 |
| 돌려주기 | return | 返回 |

## 이번 주 범위

| 태그·명령·API | 이번 주에 알아둘 뜻 |
|---|---|
| `<script src="app.js" defer></script>` | `index.html`이 `app.js`를 불러온다. `defer`는 HTML을 다 읽은 뒤 실행하라는 뜻 |
| `console.log(값)` | 괄호 안의 값을 **Console 탭**에 찍는다. 화면은 바뀌지 않는다 |
| `app.js:6` | Console 오류 줄 오른쪽에 보이는 파일 이름과 줄 번호. 고칠 자리를 알려 준다 |
| `const name = 'student01';` | 값에 이름을 붙인다. `const`는 다시 넣지 않는 값 |
| `let hour = 9;` | 나중에 다른 값을 다시 넣을 값. `hour = 15;`처럼 이름만 적고 다시 넣는다 |
| `'글자'` · `9` | 따옴표 안은 문자열, 따옴표 없는 것은 숫자. `'9'`와 `9`는 다르다 |
| `` `안녕하세요, ${name}님!` `` | 백틱으로 감싼 문장. `${이름}` 자리에 변수 값이 들어간다 |
| `if (조건) { } else { }` | 조건이 맞으면 위, 아니면 아래 중괄호 안을 실행한다 |
| `>=` · `<=` · `===` | 크거나 같다 / 작거나 같다 / 값이 같다. `=` 하나는 "넣는다" |
| `new Date().getHours()` | 지금 시각을 0~23 숫자로 준다. 이번 주는 **복붙 틀 한 줄** |
| `function greet(name) { … }` | 하는 일에 이름을 붙인다. 정의만으로는 실행되지 않는다 |
| `greet('student01')` | 이름 뒤에 괄호를 붙여야 그때 실행된다(호출) |
| `return 값` | 함수가 돌려주는 값. `return`이 없으면 결과는 `undefined` |
| `document.querySelector('#greeting').textContent = message;` | `id="greeting"`인 자리의 글자를 바꾼다. **복붙 틀 한 줄**이며 뜻은 6주차에 배운다 |
| `git revert HEAD` | 마지막 commit을 되돌리는 commit을 새로 만든다. 기록은 둘 다 남는다 |

배열·반복문(10주차), 버튼 클릭 같은 이벤트(6주차), 입력 칸 값 읽기(7주차)는 이번 주에 다루지 않는다.
화살표 함수(`() =>`), `map`·`filter`, 클래스는 이 과목에서 쓰지 않는다. 2주차 `app.js`에 있던 `() =>`는 틀로만 본 것이다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week05_javascript_data/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [index.html](examples/day1/index.html) · [app.js](examples/day1/app.js) · [about.html](examples/day1/about.html) · [guestbook.html](examples/day1/guestbook.html) · [styles.css](examples/day1/styles.css)
- 2일차 완성 코드: [index.html](examples/day2/index.html) · [app.js](examples/day2/app.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

## 완료 기준

- [ ] 공개 주소 `https://<아이디>.github.io/my-web/`을 열면 카드 한 줄에 인사말이 보인다.
- [ ] 인사말에 본인 아이디와 오전·오후 인사가 함께 들어 있다.
- [ ] F12 Console에 오류(빨간 줄)가 없고 `console.log`로 찍은 값이 보인다.
- [ ] `app.js`에 `const`·`let`·템플릿 문자열·`if / else`·함수 두 개가 있다.
- [ ] 주소창과 Console이 함께 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

오늘은 페이지를 열 때 **한 번** 실행되는 코드를 썼다. 6주차에는 버튼을 눌렀을 때 실행되는 코드를 쓴다.
`document.querySelector`와 `textContent`가 정식 항목이 되고, 오늘 만든 `#greeting`과 `greet(name)`·`hello(hour)`를
그대로 이어받아 "인사 바꾸기" 버튼과 클릭 횟수, 다크 모드를 만든다. 결과는 같은 공개 주소에서 확인한다.

## 공식 참고 자료

- [JavaScript 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)
- [변수에 필요한 정보 저장하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Variables)
- [문자열 다루기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Strings)
- [조건문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Conditionals)
- [함수 — 코드 재사용하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Functions)
- [나만의 함수 만들기(return 포함) — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Build_your_own_function)
- [console.log() — MDN](https://developer.mozilla.org/ko/docs/Web/API/console/log_static)
- [git revert — Git 공식 문서](https://git-scm.com/docs/git-revert)
