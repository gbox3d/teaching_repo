[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project)

# 9주차 예제 — 비교 예제 3개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01 ~ ex03     마크다운 제목 #, 목록 -, 링크 [보이는 글](주소) (.md 파일)
  day2/   web-week09/     2일차 끝의 web-week09 — 7주차 완성본에 README 1차판과 캡처 두 장을 더한 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
이번 주 예제는 마크다운 파일(`.md`)이다. JavaScript 가 없어서 고르기 페이지와 `.js` 파일이 없다. 결과는 **렌더된 모양**에서 본다. VS Code 에서 파일을 열고 미리 보기를 옆에 띄우거나(**Ctrl+K** 다음 **V**, macOS **⌘+K** 다음 **V**), 올린 뒤 GitHub 저장소 화면에서 파일을 연다(**Preview** 는 렌더된 모양, **Code** 는 원문).
맨 위 `<!-- … -->` 두 줄은 HTML 주석이다. 원문에는 있지만 렌더된 모양에는 보이지 않는다(5·6주차 고르기 페이지의 주석과 같다).
**다른 파일의 개념은 섞지 않는다.** 목록 `-` 는 ex02 의 주제라서 ex01·ex03 에는 없다. 형제 사이는 빈 줄로 나눴다.
만들기는 마지막 하나, [`day2/web-week09/`](day2/web-week09/) 뿐이다. 이번 주는 2일차 60분이 발표라서 비교 예제와 조립을 모두 1일차에 한다. 2일차에는 파일이 바뀌지 않으므로 2일차 끝의 `web-week09` 는 1일차 끝과 같다.
내려받아 이번 주 저장소 `web-week09` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것(렌더된 모양) | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01_heading.md](day1/ex01_heading.md) | 같은 글자 `공개 주소` 가 1번 아래 큰 제목, 2번 아래 한 단계 작은 제목, 3번 아래 보통 글자 `#공개 주소` | 줄 맨 앞의 `#` 개수가 제목의 크기를 정한다(하나가 가장 크다). `#` 뒤에 띄어쓰기 한 칸이 있어야 제목이고, 없으면 `#` 까지 글자로 보인다 | 10행 `##` → `###`(더 작아진다). 14행 `#공개 주소` → `# 공개 주소`(6행과 같은 큰 제목) |
| [day1/ex02_list.md](day1/ex02_list.md) | 1번은 점(•)이 붙은 목록 세 줄, 2번은 `홈 내 정보 방명록` 한 줄, 3번은 `-홈 -내 정보 -방명록` 한 줄 | `- `(하이픈과 띄어쓰기)로 시작하는 줄이 목록 한 줄이 된다. 기호 없는 줄은 원문에서 줄을 바꿔도 한 문단으로 이어진다 | 2번(12~14행) 사이에 빈 줄 → 세 줄(점 없음). 3번(18~20행) `-` 뒤에 띄어쓰기 → 1번과 같아진다 |
| [day1/ex03_link.md](day1/ex03_link.md) | 1번 `MDN 웹 문서`·2번 `ex01 제목 예제` 는 누를 수 있는 링크, 2번과 한 칸만 다른 3번은 `[ex01 제목 예제] (ex01_heading.md)` 글자 그대로 | `[보이는 글](주소)`. 대괄호는 화면에 보이는 글, 소괄호는 누르면 가는 곳이다. 소괄호에는 인터넷 주소나 같은 저장소 안의 파일 이름(경로)을 쓴다. `]` 와 `(` 사이를 띄우면 링크가 아니다 | 6행 주소를 내 공개 주소로. 10행 소괄호를 `ex02_list.md` 로(보이는 글은 그대로인데 갈 곳만 바뀐다). 14행 띄어쓰기 지우기 → 2번과 같은 링크 |

### 파일 안의 모양

형제 번호는 원문과 렌더된 모양에 모두 보이는 `1번 — …` 줄에 있다. [ex02_list.md](day1/ex02_list.md) 에서 인용:

```markdown
1번 — 줄마다 맨 앞에 하이픈(-)과 띄어쓰기 한 칸:

- 홈
- 내 정보
- 방명록

2번 — 기호 없이 줄만 바꿨다:

홈
내 정보
방명록
```

1번과 2번은 글자가 똑같다. 다른 것은 줄 맨 앞의 `- ` 하나다. 형제 사이의 빈 줄은 덩어리(문단·목록)를 나누는 줄이다.
다른 두 파일도 같다. ex01 의 세 줄은 글자 `공개 주소` 가 같고 `#` 개수와 띄어쓰기만 다르다. ex03 의 2번과 3번은 `]` 와 `(` 사이 띄어쓰기 한 칸만 다르다.

## `day2/web-week09/` — 2일차 끝의 web-week09

[`day2/web-week09/`](day2/web-week09/) 는 2일차 끝의 `web-week09` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 10주차 새 저장소 `web-week10` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week09/` 파일 | 내 `web-week09` 의 위치 | 따라하기 단계 |
|---|---|---|
| [README.md](day2/web-week09/README.md) | `README.md` | [1일차 7단계](../walkthrough.md#7-readme-1차판-조립하기) — 이번 주 조립. 사이트 이름·소개·기능·배운 것 문장은 내 것으로 쓰고, 공개 주소 줄은 내 `https://<아이디>.github.io/web-week09/` 로 쓴다 |
| [screenshots/home.png](day2/web-week09/screenshots/home.png) · [screenshots/guestbook.png](day2/web-week09/screenshots/guestbook.png) | `screenshots/` | [1일차 5단계](../walkthrough.md#5-화면-두-장-캡처와-데이터가-가는-세-곳) — 내 화면을 직접 찍어 넣는다(동작한 뒤의 화면) |
| [index.html](day2/web-week09/index.html) · [styles.css](day2/web-week09/styles.css) · [app.js](day2/web-week09/app.js) | 같은 이름 | 7주차 그대로. 이번 주에 고치지 않는다 |
| [about.html](day2/web-week09/about.html) · [guestbook.html](day2/web-week09/guestbook.html) · [guestbook.js](day2/web-week09/guestbook.js) | 같은 이름 | 7주차 그대로. 방명록 글은 화면에만 있다(데이터가 가는 세 곳 ①) |
| [images/profile.png](day2/web-week09/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
