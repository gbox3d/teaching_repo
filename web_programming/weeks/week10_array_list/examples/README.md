[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data)

# 10주차 예제 — 비교 예제 7개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   index.html      고르기 페이지 — 맨 아래 script 줄 하나만 켠다
          ex01 ~ ex04     배열, for, 목록 한 줄 만들기, 누를 때마다 쌓기 (.js 파일)
  day2/   ex05 ~ ex07     비우고 다시 그리기, showList, 삭제 버튼 틀 (.html + .js 한 쌍)
          web-week10/     2일차 끝의 web-week10 — 비교 예제에서 본 줄을 모은 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **F12 › Console**, **F12 › Elements** 에서 본다. Console 아래 입력 칸에 `items` 를 치면 지금 배열이 보인다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 파일의 개념은 섞지 않는다.** 목록을 비우고 다시 그리는 것은 ex05 의 주제라서 1일차 예제에는 없다. 삭제 버튼은 ex07 에만 있다.
만들기는 마지막 하나, [`day2/web-week10/`](day2/web-week10/) 뿐이다.

1일차는 네 예제가 같은 화면(글 칸과 **더하기** 버튼, 빈 목록, 개수 자리)을 쓴다. 그래서 코드를 `.js` 파일로 떼어 두고 고르기 페이지 [day1/index.html](day1/index.html) 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 네 줄 중 **하나만** 주석 밖에 둔다(VS Code 에서 줄에 커서를 두고 **Ctrl+/**, macOS **⌘+/**). 처음에는 ex01 줄만 켜져 있다. ex01·ex02 는 Console 에만 찍고 화면 자리는 쓰지 않는다.
2일차 예제는 화면이 서로 다르다. 그래서 예제마다 `.html` 과 `.js` 를 한 쌍으로 둔다. `.html` 을 연다. 두 파일이 같은 폴더에 있어야 한다.
내려받아 이번 주 저장소 `web-week10` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 내 저장소에서는 날짜 폴더 없이 `ex/` 한 곳에 모은다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/index.html](day1/index.html) | 제목과 안내 두 줄, "예제가 쓰는 자리"(글 칸·**더하기** 버튼·빈 목록·`0개`). Console 은 켜 둔 `script` 줄의 예제 것만 찍힌다 | JS 를 파일로 떼어 HTML 이 `<script src>` 로 불러온다. 어느 파일을 불러올지는 `script` 줄 하나로 정해진다 | 켜 둔 줄을 바꿔 가며 새로고침 |
| [day1/ex01_array.js](day1/ex01_array.js) | Console 1번 `0`, 2번 `3` 과 배열, 3번 `student01: 안녕하세요`, 4번 `student03: 반갑습니다`, 5번 `undefined`, 6번 `2` 와 배열 | 배열은 값을 순서대로 담는다. `push` 는 맨 뒤에 더한다. 번호는 0 부터라서 마지막 번호는 개수보다 하나 작고, 없는 번호는 `undefined` 다. 6번처럼 대괄호 안에 쉼표로 나눠 적으면 처음부터 값이 든 배열이다(ex02·ex05·ex07 이 이 모양으로 시작한다) | 8행 앞에 `//` → 2번 `2`, 4번 `undefined`. 12행 `items[0]` 을 `items[1]` 로. 16행 배열에 `, 'student03'` → 6번 `3`. Console 입력 칸에 `items` |
| [day1/ex02_for.js](day1/ex02_for.js) | Console 1번 세 줄(번호 0·1·2), 2번 네 줄(번호 0~3) | `for` 는 `i` 를 0 부터 하나씩 올리며 `items[i]` 를 꺼낸다. 끝을 숫자 `3` 으로 적으면 넷째를 빠뜨리고, `items.length` 로 적으면 끝까지 간다 | 5행 앞에 `//` → 둘 다 세 줄. 14행 `<` 를 `<=` 로. `let i` 를 `const i` 로 → 빨간 줄 |
| [day1/ex03_create_li.js](day1/ex03_create_li.js) | 화면 목록에 `2. 만들고 붙인 줄`·`3. 나중에 붙인 줄` 두 줄. Console 1~3번 | `createElement` 로 만든 요소는 `append` 로 붙여야 화면과 Elements 에 나타난다. `append` 는 맨 뒤에 붙인다 | 맨 끝에 `list.append(li1);` → 1번 줄이 맨 아래에. 7행 `'li'` 를 `'<li>'` 로 → 빨간 줄 |
| [day1/ex04_push_add.js](day1/ex04_push_add.js) | **더하기**를 누를 때마다 목록에 칸의 글이 한 줄 쌓이고 `1개`·`2개`·`3개`. Console 1~3번이 한 묶음씩 | 누를 때 배열에 넣고(`push`) 화면에도 붙인다(`append`). 둘은 따로라서 하나를 빼면 어긋난다. 개수는 화면의 줄이 아니라 `items.length` 로 쓴다 | 12행(`push`) 앞에 `//` → 줄은 쌓이는데 `0개`. 16행(`append`) 앞에 `//` → 줄 없이 `3개`. 18행 백틱을 작은따옴표로 |
| [day2/ex05_redraw.html](day2/ex05_redraw.html) + [ex05_redraw.js](day2/ex05_redraw.js) | 버튼 둘과 빈 목록. 1번을 누를 때마다 세 줄씩 늘고(3·6·9줄), 2번은 몇 번을 눌러도 세 줄 | 다시 그릴 때는 `list.innerHTML = ''` 로 먼저 비우고 배열 전체를 처음부터 그린다. 이 수업에서 `innerHTML` 은 비우기에만 쓴다 | 19행 앞에 `//` → 2번도 늘어난다. 5행 배열에 한 줄 더 → 2번이 네 줄 |
| [day2/ex06_show_list.html](day2/ex06_show_list.html) + [ex06_show_list.js](day2/ex06_show_list.js) | 열자마자 빈 목록, `아직 남긴 글이 없습니다.`, `0개`. **더하기**를 누르면 안내가 사라지고 줄과 개수가 는다 | 목록·안내 문장·개수를 모두 배열에서 다시 만드는 함수 `showList()` 하나를 둔다. 열 때 한 번, 배열을 바꿀 때마다 부른다 | 8행 배열에 값 하나 + 26행 앞에 `//` → 배열은 1개인데 화면은 `0개`. 32행 앞에 `//` → 눌러도 화면 그대로 |
| [day2/ex07_delete_button.html](day2/ex07_delete_button.html) + [ex07_delete_button.js](day2/ex07_delete_button.js) | 세 줄마다 **[삭제]**, `3개`. 가운데를 누르면 두 줄과 `2개`. Console 에 `그린 뒤 items :` | 삭제 버튼 틀(14~20행)을 그대로 옮겨 쓴다. 누르면 `splice(i, 1)` 로 배열에서 하나 빼고 `showList()` 로 다시 그린다. `showList()` 가 다시 그릴 때 버튼마다 번호를 새로 붙인다 | 17행 `splice(i, 1)` 의 `1` 을 `2` 로 → 두 줄이 지워진다. 18행 앞에 `//` → 화면은 그대로, 배열만 준다 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 `console.log` 앞 글자에 있다. [ex02_for.js](day1/ex02_for.js) 에서 인용:

```js
// 1. 끝을 숫자 3 으로 적었다 — 넷째 값을 빠뜨린다
for (let i = 0; i < 3; i++) {
    console.log('1.', i, items[i]);
}

// 2. 끝을 items.length 로 적었다 — 몇 개가 들어 있든 끝까지 간다
for (let i = 0; i < items.length; i++) {
    console.log('2.', i, items[i]);
}
```

1번과 2번은 안쪽 줄이 앞 번호(`'1.'`·`'2.'`)만 다르다. `for` 줄에서 다른 것은 끝 조건 `i < 3` 과 `i < items.length` 하나다. 배열에 값이 넷이므로 1번은 세 줄, 2번은 네 줄이 찍힌다.

## `day2/web-week10/` — 2일차 끝의 web-week10

[`day2/web-week10/`](day2/web-week10/) 는 2일차 끝의 `web-week10` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 11주차 새 저장소 `web-week11` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week10/` 파일 | 내 `web-week10` 의 위치 | 따라하기 단계 |
|---|---|---|
| [guestbook.html](day2/web-week10/guestbook.html) | `guestbook.html` | [2일차 8단계](../walkthrough.md#2일차) — `<div id="notice">` 아래 두 줄이 `<h3>남긴 글</h3>`·`#list`·`#empty`·`#count` 네 줄로 바뀐다 |
| [guestbook.js](day2/web-week10/guestbook.js) | `guestbook.js` | [2일차 9~12단계](../walkthrough.md#2일차) — 찾아 두기 세 줄과 `let items = []`, `showList()` 와 삭제 버튼 틀, submit 안 두 줄, 맨 끝 `showList();`. 나머지는 9주차와 같다(submit 안의 빈 줄만 뺐다. 남아 있어도 동작은 같다) |
| [index.html](day2/web-week10/index.html) | `index.html` | 9주차 그대로. 이번 주에 열지 않는다 |
| [about.html](day2/web-week10/about.html) | `about.html` | 9주차 그대로 |
| [styles.css](day2/web-week10/styles.css) | `styles.css` | 9주차 그대로. 목록과 **[삭제]** 에 따로 규칙을 주지 않았다 |
| [app.js](day2/web-week10/app.js) | `app.js` | 9주차 그대로(6주차 인사·다크 모드) |
| [README.md](day2/web-week10/README.md) · [screenshots/](day2/web-week10/screenshots/) | `README.md` · `screenshots/` | 9주차에 쓴 README 1차판과 화면 두 장 그대로 |
| [images/profile.png](day2/web-week10/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
