[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

# 11주차 예제 — 비교 예제 7개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex01 ~ ex03     객체와 점 표기, 배열 안의 객체, 객체를 목록 한 줄로 (.js 파일)
  day2/   index.html      고르기 페이지 — ex04 의 저장하기 버튼도 여기 있다
          ex04 ~ ex07     저장 칸, JSON, || 또는, removeItem (.js 파일)
          web-week11/     2일차 끝의 web-week11 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **F12 › Console**, 그리고 2일차에 처음 쓰는 **F12 › Application** 탭에서 본다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 저장 칸(`localStorage`)은 ex04 의 주제라서 1일차 예제에는 없다. 뒤 예제가 앞 예제의 줄을 빌려 쓸 때는 줄 끝 주석에 출처(`// setItem 은 ex04`)를 적었다.
만들기는 마지막 하나, [`day2/web-week11/`](day2/web-week11/) 뿐이다.

1일차는 세 예제가 같은 화면을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day1/index.html](day1/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex01 줄만 켜져 있다. 6주차 1일차와 같은 방법이다.
2일차 네 예제도 결과를 Console 과 Application 탭에서만 본다. 그래서 같은 방법으로 고르기 페이지 [day2/index.html](day2/index.html) 하나로 연다. 맨 아래 `<script src>` 네 줄 중 하나만 켠다. 처음에는 ex04 줄만 켜져 있다. ex04 가 쓰는 **저장하기** 버튼은 그 페이지의 "ex04 가 쓰는 자리"에 있다. 내 `ex/` 에서는 2일차 `index.html` 이 1일차 것을 덮어쓴다(1일차 `.js` 세 개는 그대로 남는다).
2일차 예제의 저장 칸 키는 `ex04-memo` 처럼 예제 번호로 시작한다. 같은 주소의 저장 칸은 함께 쓰므로, 완성본의 `guestbook` 키와 섞이지 않게 하려는 것이다.
내려받아 이번 주 저장소 `web-week11` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)와 [2일차](../walkthrough.md#2일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/index.html](day1/index.html) | 제목과 안내 두 줄, "ex03 이 쓰는 자리"(제목 두 개와 빈 목록 두 개). Console 은 켜 둔 `script` 줄의 예제 것만 찍힌다 | JS 를 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day1/ex01_object.js](day1/ex01_object.js) | Console 1번 객체 한 묶음(값 바로 앞의 ▶ 로 펼치면 이름표 셋과 값이 한 줄씩 보인다. 순서는 코드와 다를 수 있고, `[[Prototype]]` 줄이 보이면 그것은 내가 적은 이름표가 아니다), 2번 `하늘`, 3번 `2026. 11. 11.`, 4번 `undefined`, 5번 `바다` | 객체 `{ }` 는 이름표가 붙은 값 묶음이다. 점 뒤에 이름표를 쓰면 그 값 하나가 나온다. 없는 이름표는 빨간 줄 없이 `undefined` 다. `{ name: name }` 의 왼쪽은 이름표, 오른쪽은 변수다 | 4행 `'하늘'` 뒤 쉼표 지우기 → 빨간 줄, 1~5번 모두 안 찍힌다. 14행 `name: name` 을 `name: 'name'` 으로 → 5번 `name` |
| [day1/ex02_array_objects.js](day1/ex02_array_objects.js) | Console 1번 글자 두 개짜리 배열, 2번 `하늘: 안녕하세요`, 3번 객체 두 개짜리 배열 `[{…}, {…}]`, 4번 `하늘`, 5번 오늘 날짜 | 글자 한 덩어리에서는 이름만 꺼낼 수 없다. 배열 안의 객체는 대괄호로 몇 번째 묶음인지, 점으로 무슨 값인지 고른다. `new Date().toLocaleDateString()` 은 오늘 날짜를 글자로 만드는 틀이다 | 17행 쉼표 뒤를 `items.name[0]` 으로 → 빨간 줄. 12행 `.toLocaleDateString()` 지우기 → 5번이 긴 날짜·시각 값 |
| [day1/ex03_list_line.js](day1/ex03_list_line.js) | 1번 목록 `[object Object]` 두 줄, 2번 목록 `하늘: 안녕하세요 (2026. 11. 11.)` · `바다: 잘 봤습니다 (2026. 11. 11.)`. 빨간 줄 없음 | 글자 자리에 객체를 통째로 넣으면 `[object Object]` 가 된다. 점 표기로 값을 하나씩 꺼내 백틱 문장(5주차 템플릿 문자열)에 넣는다 | 16행 `items[i].nmae` → `undefined: 안녕하세요 (…)`. 16행 백틱을 작은따옴표로 → `${…}` 가 글자 그대로 |
| [day2/index.html](day2/index.html) | 제목과 안내 두 줄, "ex04 가 쓰는 자리"(**저장하기** 버튼 하나). Console 과 저장 칸에는 켜 둔 `script` 줄의 예제 것만 생긴다 | 1일차와 같다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다. 버튼은 ex04 줄을 켰을 때만 일을 한다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day2/ex04_storage.js](day2/ex04_storage.js) | 처음 Console 1번 `(처음 값)`, 2번 `null`. **저장하기** → 새로고침하면 1번 `(처음 값)`, 2번 `안녕하세요`. Application 표에 `ex04-memo` 한 줄 | 변수는 열 때마다 처음 값으로 다시 시작한다. `setItem(키, 값)` 으로 저장 칸에 적은 글자는 새로고침해도 `getItem(키)` 로 꺼낼 수 있다. 적은 적 없는 키는 `null` | 저장한 뒤 8행 `getItem` 의 키를 `'ex04-Memo'` 로 → 2번 `null`, 표에는 `ex04-memo` 그대로. 12행 값에 `['하늘', '바다']` → 2번 `하늘,바다`(글자) |
| [day2/ex05_json.js](day2/ex05_json.js) | Console 1번 `[object Object],[object Object]`, 2번 `[{"name":"하늘","message":"안녕하세요"},{"name":"바다","message":"잘 봤습니다"}]`, 3번 `하늘 / 개수 : 2` | 저장 칸은 글자만 받는다. 배열을 그대로 넣으면 내용이 사라진다. `JSON.stringify` 로 바꾼 글자는 내용이 남고, `JSON.parse` 로 다시 배열이 된다 | 22행 주석 풀기 → `is not valid JSON` 빨간 줄. 13행을 6행 위로 → 2번에 하나만, 3번 개수 1 |
| [day2/ex06_or.js](day2/ex06_or.js) | Console 1번 `이름과 메시지를 모두 입력하세요.`, 2번 `null`, 3번 빈 배열과 `개수 : 0` | `\|\|` 는 "또는"이다. if 안에서는 둘 중 하나라도 참이면 참이다. 값 자리에서는 앞이 없으면(`null`) 뒤 값을 쓴다. 그래서 처음 여는 사람도 빈 배열로 시작한다 | 5행 `message` 를 채우기 → 1번 `둘 다 채웠다.`. 23행 주석 풀기 → `null` 의 `length` 빨간 줄 |
| [day2/ex07_remove.js](day2/ex07_remove.js) | Console 1번 `0 개 / 저장 칸 : ["하늘","바다"]`, 2번 `0 개 / 저장 칸 : null`, 3번 `다른 키`. Application 표의 ex07 키는 `ex07-other` 만 남는다 | 배열 변수와 저장 칸은 따로다. `items = []` 는 배열만 비운다. `removeItem(키)` 은 저장 칸에서 그 키 하나만 지운다 | 13행을 주석으로 → 2번 저장 칸이 그대로. 13행 키를 `'ex07-other'` 로 → 3번 `null` |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex06_or.js](day2/ex06_or.js) 에서 인용:

```js
// 2. 적은 적 없는 키를 꺼내 되살리면 null 이다(getItem 은 ex04, JSON.parse 는 ex05)
const saved = JSON.parse(localStorage.getItem('ex06-none'));
console.log('2. || 없이 :', saved);

// 3. 값 자리의 || — 앞이 null 이면 뒤의 빈 배열 [] 을 쓴다
const items = JSON.parse(localStorage.getItem('ex06-none')) || [];
console.log('3. || [] 를 붙이면 :', items, '/ 개수 :', items.length);
```

2번과 3번은 꺼내는 줄이 똑같다. 다른 것은 줄 끝의 `|| []` 하나다. 완성본의 되살리는 줄 `let items = JSON.parse(localStorage.getItem('guestbook')) || [];` 가 3번과 같은 모양이다.

## `day2/web-week11/` — 2일차 끝의 web-week11

[`day2/web-week11/`](day2/web-week11/) 는 2일차 끝의 `web-week11` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 12주차 새 저장소 `web-week12` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week11/` 파일 | 내 `web-week11` 의 위치 | 따라하기 단계 |
|---|---|---|
| [guestbook.html](day2/web-week11/guestbook.html) | `guestbook.html` | [2일차 8·13단계](../walkthrough.md#2일차) — `#empty` 줄이 없어지고 `#count` 의 처음 글자가 안내 문장이 된다. 그 아래에 **[전체 지우기]** 버튼 줄이 늘어난다 |
| [guestbook.js](day2/web-week11/guestbook.js) | `guestbook.js` | [2일차 8~13단계](../walkthrough.md#2일차) — 10주차 파일을 조립표 순서로 고친다. 한 줄이 객체가 되고, `saveList()`·되살리는 줄·전체 지우기가 들어온다. 이 파일과 글자 단위로 같아진다 |
| [index.html](day2/web-week11/index.html) · [about.html](day2/web-week11/about.html) · [app.js](day2/web-week11/app.js) · [styles.css](day2/web-week11/styles.css) | 같은 이름 | 10주차 그대로. 이번 주에 열지 않는다. `index.html` 의 `id="count"` 는 클릭 횟수 자리라서 방명록의 `#count` 와 이름만 같고 서로 영향이 없다 |
| [README.md](day2/web-week11/README.md) · [screenshots/](day2/web-week11/screenshots/) | 같은 이름 | 9주차 1차 과제 때 만든 저장소 소개와 캡처 두 장. 9주차 그대로다(10주차에도 바꾸지 않았다). 저장소 `README.md` 는 13주차에 최종판으로 다시 쓴다 |
| [images/profile.png](day2/web-week11/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
