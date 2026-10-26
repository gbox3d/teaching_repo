[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

# 11주차 — 객체와 localStorage

이번 주도 부품을 하나씩 본다. 비교 예제 7개를 열어 값을 바꿔 보고, 마지막에 이번 주 새 저장소 `web-week11` 의 `guestbook.html`·`guestbook.js` 를 그 부품으로 조립한다.
10주차 방명록은 한 줄이 `하늘: 안녕하세요` 같은 **글자 한 덩어리**였고, 새로고침하면 목록이 사라졌다. 이번 주에는 한 줄을 이름·메시지·날짜 **객체**로 바꾸고, 목록을 브라우저의 **저장 칸**(`localStorage`)에 남겨 새로고침해도 남게 한다.
결과는 화면과 **F12 › Console**, 그리고 이번 주에 처음 쓰는 **F12 › Application** 탭에서 본다. **이번 주부터 확인·캡처는 공개 주소에서만 한다.** 내 PC 에서 연 화면과 공개 주소는 저장 칸이 따로다.

## 이번 주 질문

> 방명록 한 줄에 이름·메시지·날짜를 함께 담고, 새로고침해도 목록이 남게 하려면 무엇을 알아야 하나?

답은 세 가지 원리다.
**객체** `{ }` 는 이름표가 붙은 값 묶음이다. 배열 안의 객체는 대괄호로 **몇 번째**인지, 점으로 **무슨 값**인지 골라 `items[i].name` 처럼 꺼낸다.
변수는 새로고침하면 처음으로 돌아가고, **저장 칸**(`localStorage`)에 적은 것은 남는다. 저장 칸은 **글자만** 받으므로 배열은 `JSON.stringify` 로 글자로 바꿔 넣고, 꺼낸 뒤 `JSON.parse` 로 되살린다.
처음 여는 사람의 저장 칸은 비어 있어 `null` 이 나온다. 그래서 되살리는 줄 끝에 `|| []` 를 붙이고, 전체 지우기는 배열과 저장 칸을 **둘 다** 비운다.

## 학습 목표

1. `{ name: …, message: …, date: … }` 객체를 만들고 `item.name` 처럼 **점 표기**로 값을 꺼낸다. 없는 이름표는 빨간 줄 없이 `undefined` 라는 것을 확인한다.
2. 배열 안의 객체에서 `items[i].name` 으로 "몇 번째 글의 어떤 값"을 읽고, 목록 한 줄을 `` `${items[i].name}: ${items[i].message} (${items[i].date})` `` 로 쓴다. 객체를 그대로 넣으면 `[object Object]` 가 된다.
3. `localStorage.setItem / getItem` 으로 글자를 저장하고 꺼낸다. **Application › Local Storage** 에서 키와 값을 본다.
4. `JSON.stringify` 로 배열을 글자로 바꿔 저장하고, `JSON.parse(localStorage.getItem('guestbook')) || []` 로 페이지를 열 때 되살린다. `||` 의 두 쓰임(if 안·값 자리)을 말한다.
5. `localStorage.removeItem` 과 `items = []` 로 전체 지우기를 만들고, 둘 중 하나만 하면 무엇이 남는지 말한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-week11/guestbook.html
         글 3개를 남기고 새로고침한 뒤, F12 › Application › Local Storage 를 함께 연 화면

         남긴 글
         · 하늘: 안녕하세요 (2026. 11. 11.)      [삭제]
         · 바다: 잘 봤습니다 (2026. 11. 11.)     [삭제]
         · 노을: 반갑습니다 (2026. 11. 11.)      [삭제]
         3개                                     ← 새로고침해도 그대로
         Key: guestbook  Value: [{"name":"하늘","message":"안녕하세요",…}]
         ← 주소창이 함께 보이게 찍는다
```

- 제출은 이 캡처 **한 장**이다. 날짜는 글을 남긴 날이고, 모양은 브라우저 언어 설정에 따라 다르다.
- `web-week11/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다. 기록물·표는 없다.
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | 고르기 페이지 쓰는 법 → ex01 객체와 점 표기 → ex02 배열 안의 객체와 날짜 틀 → ex03 객체를 목록 한 줄로 | 새 폴더 `web-week11` 에 지난주 완성본 넣기 → `ex/` 에 네 파일 저장 → 값 바꿔 보기 → 새 저장소 만들어 올리기 · Pages 켜기 | `ex/` 비교 예제(확인용) |
| 2일차 | ex04 저장 칸과 Application 탭 → ex05 JSON → ex06 `\|\|` 또는 → ex07 removeItem → 내 목록은 내 브라우저에만 → 조립표 | `ex/` 에 다섯 파일 저장(고르기 페이지는 1일차 것을 덮어쓴다) → 값 바꿔 보기 → `guestbook.html`·`guestbook.js` 조립 → push → 공개 주소에서 확인 → 캡처 | 캡처 1 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 지난주 완성본. 내 `web-week10` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [10주차 `examples/day2/web-week10/`](../week10_supabase_data/examples/day2/web-week10/) 파일을 **Raw** 로 받는다
- VS Code, Chrome(DevTools), Git (`git --version` 으로 확인)
- Node.js LTS(선택). 5주차에 받은 [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md)). 서버로 연 주소(`http://localhost:8000/`)도 공개 주소와 저장 칸이 다르다
- 개발자 도구의 **Console** 탭과 이번 주 2일차에 처음 쓰는 **Application** 탭 위치(**F12**, 또는 오른쪽 클릭 › **검사**)
- 10주차 [비교 예제](../week10_supabase_data/examples/README.md)의 배열·`for`·`showList()` 를 기억해 둔다. 이번 주는 그 배열에 담는 값을 글자에서 객체로 바꾼다
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 객체 | object | 对象 |
| 속성(이름표) | property | 属性 |
| 점 표기 | dot notation | 点表示法 |
| 브라우저 저장 칸 | localStorage | 本地存储 |
| 키 | key | 键 |
| 글자로 바꾸기 | JSON.stringify | 转成 JSON 字符串 |
| 글자를 되살리기 | JSON.parse | 解析 JSON |
| 또는 | logical OR (`\|\|`) | 逻辑或 |

## 이번 주 비교 예제

1일차 ex01~ex03 은 같은 화면을 쓰므로 코드만 `.js` 파일에 두고, 고르기 페이지 [day1/index.html](examples/day1/index.html) 맨 아래 `<script src>` 세 줄 중 하나만 켜서 연다. 2일차 ex04~ex07 도 결과를 Console 과 Application 탭에서만 보므로 같은 방법이다. 고르기 페이지 [day2/index.html](examples/day2/index.html) 의 `<script src>` 네 줄 중 하나만 켠다. ex04 의 **저장하기** 버튼은 그 페이지의 "ex04 가 쓰는 자리"에 있다. 내 `ex/` 에서는 2일차 `index.html` 이 1일차 것을 덮어쓴다. Console 의 번호가 코드의 형제 번호와 같다.
2일차 예제는 저장 칸 키 이름을 `ex04-memo` 처럼 예제 번호로 시작하게 했다. 같은 주소의 저장 칸은 함께 쓰므로 완성본의 `guestbook` 키와 섞이지 않게 하려는 것이다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_object.js](examples/day1/ex01_object.js) | 1. 객체 통째로 / 2·3. 점 표기로 값 하나 / 4. 없는 이름표 / 5. 값 자리에 변수 | 객체는 이름표가 붙은 값 묶음이다. 점 뒤에 이름표를 쓰면 그 값이 나오고, 없는 이름표는 `undefined` 다 | 객체 안 쉼표 하나 지우기 → 파일 전체가 실행되지 않는다. `name: name` 의 오른쪽에 따옴표 |
| [ex02_array_objects.js](examples/day1/ex02_array_objects.js) | 1·2. 글자를 쌓은 배열 / 3·4·5. 객체를 쌓은 배열 | 대괄호로 몇 번째 묶음인지, 점으로 무슨 값인지 고른다. `new Date().toLocaleDateString()` 은 날짜 글자 틀이다 | 17행 쉼표 뒤의 `items[0].name` 을 `items.name[0]` 으로 → 빨간 줄. `.toLocaleDateString()` 지우기 |
| [ex03_list_line.js](examples/day1/ex03_list_line.js) | 1. 객체를 그대로 넣은 줄 / 2. 점 표기로 꺼내 넣은 줄 | 글자 자리에 객체를 넣으면 `[object Object]` 가 되고 빨간 줄은 없다. 점 표기로 값을 꺼내 템플릿 문자열에 넣는다 | `items[i].nmae` → `undefined: …`. 백틱을 작은따옴표로 |
| [ex04_storage.js](examples/day2/ex04_storage.js) | 1. 변수 `memo` / 2. 저장 칸 `ex04-memo` | 변수는 열 때마다 처음 값으로 시작하고, `setItem` 으로 적은 글자는 새로고침해도 `getItem` 으로 꺼낼 수 있다. 적은 적 없는 키는 `null` | 꺼내는 쪽(`getItem`) 키 철자 바꾸기 → `null`, 표에는 `ex04-memo` 그대로. 값 자리에 배열 → 글자 `하늘,바다` |
| [ex05_json.js](examples/day2/ex05_json.js) | 1. 배열을 그대로 저장 / 2. `JSON.stringify` 해서 저장 / 3. `JSON.parse` 로 되살리기 | 저장 칸은 글자만 받는다. 배열은 JSON 글자로 바꿔 넣고, 꺼낸 글자는 다시 배열로 되살린다 | 4번 주석 풀기 → `is not valid JSON` 빨간 줄. `stringify` 줄을 둘째 `push` 위로 → 하나만 저장된다 |
| [ex06_or.js](examples/day2/ex06_or.js) | 1. if 안의 `\|\|` / 2. `\|\|` 없이 되살리기 / 3. `\|\| []` 붙여 되살리기 | `\|\|` 는 "또는"이다. if 안에서는 둘 중 하나라도 참이면 참, 값 자리에서는 앞이 없으면(`null`) 뒤 값을 쓴다 | 4·5행 두 값 바꾸기. 4번 주석 풀기 → `null` 의 `length` 빨간 줄 |
| [ex07_remove.js](examples/day2/ex07_remove.js) | 1. `items = []` / 2. `removeItem` / 3. 다른 키 | 배열 변수와 저장 칸은 따로다. 배열만 비우면 저장 칸은 그대로다. `removeItem` 은 그 키 하나만 지운다 | `removeItem` 줄을 주석으로 → 저장 칸이 남는다 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week11_auth_rls/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(고르기 페이지 `index.html`, ex01~ex03 의 `.js`), 2일차 `day2/`(고르기 페이지 `index.html`, ex04~ex07 의 `.js`, 조립 `web-week11/`)
- 2일차 끝의 `web-week11`(조립 결과): [guestbook.html](examples/day2/web-week11/guestbook.html) · [guestbook.js](examples/day2/web-week11/guestbook.js) · [index.html](examples/day2/web-week11/index.html) · [about.html](examples/day2/web-week11/about.html) · [app.js](examples/day2/web-week11/app.js) · [styles.css](examples/day2/web-week11/styles.css) · [README.md](examples/day2/web-week11/README.md)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

## 완료 기준

- [ ] 새 저장소 `web-week11` 을 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] 공개 주소 `https://student01.github.io/web-week11/guestbook.html` 에서 글을 남기면 목록 한 줄에 `하늘: 안녕하세요 (2026. 11. 11.)` 처럼 이름·메시지·날짜가 함께 보인다.
- [ ] 새로고침해도 목록과 개수가 그대로 남는다. 줄 하나를 **[삭제]** 한 뒤 새로고침해도 그 줄이 돌아오지 않는다.
- [ ] **F12 › Application › Local Storage** 에 `guestbook` 키가 있고 값이 `[{"name":…}]` 모양이다.
- [ ] **[전체 지우기]** 를 누르면 목록이 비고 `아직 남긴 글이 없습니다.` 가 보이며, 새로고침해도 비어 있다. F12 Console 에 `Uncaught` 로 시작하는 빨간 줄이 없다(`favicon.ico` 404 한 줄은 세지 않는다).
- [ ] 글 3개를 남기고 새로고침한 뒤 Application 탭을 함께 연 화면과 주소창이 보이는 캡처 1장을 제출한다.

## 다음 수업 연결

이제 목록은 **내 브라우저 안**에 남는다. 다만 그 글은 나만 볼 수 있고, 다른 PC 에서 열면 비어 있다.
12주차에는 새 저장소 `web-week12` 를 오늘 `web-week11` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week11/`](examples/day2/web-week11/)), JSON 파일 `data/projects.json` 을 `fetch` 로 불러와 카드로 그린다.
JSON 파일의 글자 모양은 이번 주 Application 탭에서 본 `[{"name":…}]` 과 같다. 확인과 캡처는 12주차에도 공개 주소에서 한다.

## 공식 참고 자료

- [객체로 작업하기 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Working_with_objects)
- [속성 접근자 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Property_accessors)
- [Date.prototype.toLocaleDateString() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [Storage.setItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/setItem)
- [Storage.getItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/getItem)
- [Storage.removeItem() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Storage/removeItem)
- [JSON.stringify() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [JSON.parse() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- [논리 OR (||) — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Logical_OR)
- [로컬 저장소 보기 및 수정 — Chrome DevTools](https://developer.chrome.com/docs/devtools/storage/localstorage?hl=ko)
