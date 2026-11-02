[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_readme_presentation)

# 9주차 예제 — 비교 예제 11개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01 ~ ex11     제목 · 목록 · 링크 · 강조 · 그림 · 소스 코드 · 표 · 인용·구분선 · SVG 그림 · SVG 도표 · Mermaid
  day2/   web-week09/     2일차 끝의 web-week09 — 7주차 완성본에 README 1차판, 캡처 두 장, 도표를 더한 조립
```

`exNN_*` 파일은 **파일 하나 = 개념 하나**다. 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
이번 주 예제는 마크다운 파일(`.md`)이다. 결과는 **렌더된 모양**에서 본다. VS Code 에서 파일을 열고 미리 보기를 옆에 띄우거나(**Ctrl+K** 다음 **V**, macOS **⌘+K** 다음 **V**), 올린 뒤 GitHub 저장소 화면에서 파일을 연다(**Preview** 는 렌더된 모양, **Code** 는 원문).
맨 위 `<!-- … -->` 두 줄은 HTML 주석이다. 원문에는 있지만 렌더된 모양에는 보이지 않는다(5·7주차 고르기 페이지의 주석과 같다).
**다른 파일의 개념은 섞지 않는다.** 형제 사이는 빈 줄로 나눴다.
만들기는 마지막 하나, [`day2/web-week09/`](day2/web-week09/) 뿐이다. 2일차는 발표라서 파일이 바뀌지 않으므로 2일차 끝의 `web-week09` 는 1일차 끝과 같다.
내려받아 이번 주 저장소 `web-week09` 의 `ex/` 폴더에 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 파일 | 열면 보이는 것(렌더된 모양) | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01_heading.md](day1/ex01_heading.md) | 같은 글자 `공개 주소` 가 1번 아래 큰 제목, 2번 아래 한 단계 작은 제목, 3번 아래 보통 글자 `#공개 주소` | 줄 맨 앞의 `#` 개수가 제목의 크기를 정한다. `#` 뒤에 띄어쓰기 한 칸이 있어야 제목이다 | 10행 `##` → `###`. 14행 `#공개 주소` → `# 공개 주소` |
| [day1/ex02_list.md](day1/ex02_list.md) | 1번 점 목록 세 줄, 2번 `홈 내 정보 방명록` 한 줄, 3번 `-홈 -내 정보 -방명록` 한 줄, 4번 번호 목록, 5번 안쪽 목록, 6번 점검표(하나는 체크됨) | `- `·`1. ` 로 시작하는 줄이 목록 한 줄이 된다. 기호 없는 줄은 한 문단으로 이어진다. 앞에 두 칸을 두면 안쪽 목록이다 | 2번(12~14행) 사이에 빈 줄. 4번 숫자 바꾸기. 6번 `[ ]` ↔ `[x]` |
| [day1/ex03_link.md](day1/ex03_link.md) | 1·2번은 누를 수 있는 링크, 3번은 `[ex01 제목 예제] (ex01_heading.md)` 글자 그대로 | 대괄호는 보이는 글, 소괄호는 누르면 가는 곳이다. `]` 와 `(` 사이를 띄우면 링크가 아니다 | 14행 띄어쓰기 지우기. 10행 소괄호를 `ex02_list.md` 로 |
| [day1/ex04_emphasis.md](day1/ex04_emphasis.md) | 1번 굵게, 2번 기울임, 3번 취소선, 4번 `**[남기기]**를` 별이 글자로 남음, 5번 굵은 `[남기기]` | 같은 기호로 앞뒤를 감싼다. 닫는 별 앞이 문장 부호이고 뒤에 글자가 바로 붙으면 닫히지 않는다 | 6행 닫는 별 지우기. 4번 대괄호 지우기 |
| [day1/ex05_image.md](day1/ex05_image.md) + [images/profile.png](day1/images/profile.png) | 1번 그림(400×400), 2번 글자 링크, 3번 깨진 표시와 대괄호 글자, 4번 작은 그림(폭 120) | `!` 가 링크를 그림으로 바꾼다. 대괄호 글자는 3주차 `alt` 와 같다. 크기를 정하려면 `<img>` 를 쓴다 | 6행 `!` 지우기. 18행 `width` |
| [day1/ex06_code.md](day1/ex06_code.md) | 1번 문장 안의 코드, 2번 한 색 코드 상자, 3번 색이 입혀진 코드 상자, 4번 `#`·`-` 가 글자 그대로인 상자 | 짧은 코드는 백틱 하나, 여러 줄은 백틱 세 개 줄 사이. 여는 줄의 언어 이름이 색을 정한다 | 언어 이름 `js` → `html`. 닫는 줄 지우기 |
| [day1/ex07_table.md](day1/ex07_table.md) | 1번 표, 2번 `\|` 가 글자로 이어진 문단, 3번 칸마다 정렬이 다른 표 | 머리글 아래 구분 줄이 있어야 표다. `:` 자리가 정렬을 정한다 | 2번에 구분 줄 넣기. 1번에 줄 더하기 |
| [day1/ex08_quote_rule.md](day1/ex08_quote_rule.md) | 1번 인용, 2번 글과 가로줄, 3번 `방명록` 큰 제목(가로줄 없음) | `>` 는 인용이다. `---` 는 위가 빈 줄이면 가로줄, 글 바로 아래면 그 글을 제목으로 만든다 | 3번 사이에 빈 줄 |
| [day1/ex09_svg.md](day1/ex09_svg.md) + [ex09_shapes.svg](day1/ex09_shapes.svg) | 1번 사각형·선·글자 그림. 2번은 GitHub 에서 빈자리 | SVG 는 도형 하나가 태그 하나인 글자 파일이다. 문서에는 파일로 넣는다. GitHub 은 문서 안의 `<svg>` 를 지운다 | `.svg` 의 `fill`·`width`·`y` |
| [day1/ex10_diagram.md](day1/ex10_diagram.md) + [ex10_site_map.svg](day1/ex10_site_map.svg) | 상자 셋(홈·내 정보·방명록)과 선 셋의 사이트 구조 도표 | ex09 의 사각형·선·글자만으로 도표가 된다. 자리는 숫자로 직접 정한다 | 상자 글자. 상자 `x` |
| [day1/ex11_mermaid.md](day1/ex11_mermaid.md) | GitHub 에서 1번은 도표, 2번은 글자 그대로. VS Code 기본 미리 보기에서는 1번도 코드로 보일 수 있다 | 연결만 적으면 GitHub 이 자리를 잡아 그린다 | 연결 줄 바꾸기 |

### 파일 안의 모양

형제 번호는 원문과 렌더된 모양에 모두 보이는 `1번 — …` 줄에 있다. [ex07_table.md](day1/ex07_table.md) 에서 인용:

```markdown
1번 — 첫 줄이 머리글, 둘째 줄이 구분 줄:

| 페이지 | 파일 |
|---|---|
| 홈 | index.html |
| 방명록 | guestbook.html |

2번 — 1번에서 구분 줄만 뺐다:

| 페이지 | 파일 |
| 홈 | index.html |
| 방명록 | guestbook.html |
```

1번과 2번은 글자가 똑같다. 다른 것은 구분 줄 하나다.

## `day2/web-week09/` — 2일차 끝의 web-week09

[`day2/web-week09/`](day2/web-week09/) 는 2일차 끝의 `web-week09` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 10주차 새 저장소 `web-week10` 의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week09/` 파일 | 내 `web-week09` 의 위치 | 따라하기 단계 |
|---|---|---|
| [README.md](day2/web-week09/README.md) | `README.md` | [1일차 7단계](../walkthrough.md#7-readme-1차판-조립하기) — 이번 주 조립. 사이트 이름·소개·기능·배운 것 문장은 내 것으로 쓰고, 공개 주소 줄은 내 `https://<아이디>.github.io/web-week09/` 로 쓴다 |
| [screenshots/home.png](day2/web-week09/screenshots/home.png) · [screenshots/guestbook.png](day2/web-week09/screenshots/guestbook.png) | `screenshots/` | [1일차 5단계](../walkthrough.md#5-화면-두-장-캡처와-도표-파일) — 내 화면을 직접 찍어 넣는다(동작한 뒤의 화면) |
| [index.html](day2/web-week09/index.html) · [styles.css](day2/web-week09/styles.css) · [app.js](day2/web-week09/app.js) | 같은 이름 | 7주차 그대로. 이번 주에 고치지 않는다 |
| [about.html](day2/web-week09/about.html) · [guestbook.html](day2/web-week09/guestbook.html) · [guestbook.js](day2/web-week09/guestbook.js) | 같은 이름 | 7주차 그대로. 방명록 글은 화면에만 있다 |
| [images/profile.png](day2/web-week09/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
| [images/site-map.svg](day2/web-week09/images/site-map.svg) | `images/site-map.svg` | [1일차 5단계](../walkthrough.md#5-화면-두-장-캡처와-도표-파일) — ex10 의 SVG 에서 맨 위 주석을 지운 것. 10~14주 완성본이 그대로 이어받는다 |
