[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_readme_presentation)

# 9주차 — 마크다운과 1차 과제 발표

1일차는 **마크다운 기본 기능**을 하루 동안 본다. README 와 수업 노트, GitHub 의 모든 문서가 마크다운이다. 제목·목록·링크에 더해 강조, 그림, 소스 코드, 표, 인용, SVG 도표, Mermaid 까지 비교 예제 11개로 하나씩 보고, 1일차 끝에 3~7주에 만든 사이트(7주차 완성본)를 소개하는 `README.md` 1차판으로 조립한다.
2일차는 1차 과제 발표다. 이번 주 새 저장소 `web-week09` 의 공개 주소를 열어 2분 동안 발표한다.
결과는 **VS Code 미리 보기**와 **GitHub 저장소 화면**에서 원문과 렌더된 모양을 나란히 놓고 본다. 사이트의 HTML·CSS·JavaScript 는 7주차 그대로 두고 고치지 않는다.

## 이번 주 질문

> 내 사이트를 처음 보는 사람에게 저장소 첫 화면 한 장으로 소개하려면 글·표·그림·코드·도표를 어떻게 적어야 하나? 그리고 2분 안에 어떻게 보여 줄까?

답은 네 가지 원리다.
마크다운은 **기호**가 모양을 정한다. 줄 맨 앞의 `#`·`-`·`1.`·`>` 는 그 줄의 역할을, 앞뒤를 감싼 `**`·`` ` `` 는 글자의 모양을 정한다. 기호 하나, 띄어쓰기 한 칸이 틀리면 오류 없이 글자로 남는다.
링크 `[보이는 글](주소)` 앞에 `!` 를 붙이면 그림이다. 여러 줄 코드는 백틱 세 개 줄 사이에 쓰고, 표는 구분 줄 `|---|` 이 있어야 표다.
**SVG** 는 그림을 글자로 적은 파일이다. 사각형·선·글자를 숫자로 놓으면 도표가 되고, 문서에는 그림처럼 넣는다. **Mermaid** 는 연결만 적으면 GitHub 이 그려 준다.
발표는 공개 주소에서 동작하는 화면을 정해 둔 순서로 2분 안에 보여 준다.

## 학습 목표

1. 마크다운 원문과 렌더된 모양을 VS Code 미리 보기와 GitHub 저장소 화면(**Preview**·**Code**)에서 나란히 비교한다.
2. 제목 `#`, 목록 `-`·`1.`·들여쓰기·`- [ ]`, 링크 `[보이는 글](주소)`, 강조 `**`·`*`·`~~`, 인용 `>`, 구분선 `---` 를 쓰고, 기호가 글자로 남을 때 원인을 찾는다.
3. `![대신 읽을 글](경로)` 로 그림을 문서 안에 넣고, 경로가 틀렸을 때 보이는 모양을 안다. 크기를 정할 때는 `<img width>` 를 쓴다.
4. 짧은 코드는 백틱 하나, 여러 줄 코드는 백틱 세 개 줄과 언어 이름으로 쓴다. 표를 `|` 와 구분 줄로 쓰고 `:` 로 정렬한다.
5. SVG 의 `<rect>`·`<line>`·`<text>` 숫자를 고쳐 사이트 구조 도표를 만들어 문서에 넣고, Mermaid 로 같은 연결을 글자로 그려 비교한다.
6. 이 기능들로 README 1차판 다섯 항목을 쓰고, 공개 주소 → 세 페이지 → 버튼·폼 → README·Commits 탭 순서로 2분 발표를 한다.

## 이번 주 결과물

```text
[캡처 1]   https://github.com/student01/web-week09
           저장소 첫 화면 ─ 파일 목록 아래에 README.md 가 렌더되어 보인다
           큰 제목 한 줄 ─ 내 사이트 이름
           작은 제목 다섯 ─ 공개 주소 · 페이지(표와 SVG 도표) · 기능(소스 코드)
                            · 화면(그림 두 장) · 이번에 배운 것

[발표 2분] https://student01.github.io/web-week09/
           홈 → 내 정보 → 방명록 → 버튼 한 번 → 폼 두 번(목록 두 줄) → README·Commits 탭
```

- 이번 주는 주차별 실습 점수 대상이 아니라 **1차 과제 10점**(발표 5 + 레포트 5)이다. 레포트는 따로 내는 문서가 아니라 저장소 첫 화면의 `README.md` 한 장이다.
- `web-week09/ex/` 에 비교 예제를 저장하고 값을 바꾼 것은 push 로 남긴다(확인용).
- `student01` 은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | ex01 제목 → ex02 목록 → ex03 링크 → ex04 강조 → ex05 그림 → ex06 소스 코드 → ex07 표 · ex08 인용·구분선 → ex09·ex10 SVG → ex11 Mermaid → 조립표 | 새 폴더 `web-week09` 에 7주차 완성본 넣기 → `ex/` 에 파일 저장 → 값 바꿔 보기 → 화면 두 장 캡처·도표 파일 → README 1차판 조립 → 새 저장소 만들어 올리기 · Pages 켜기 | 캡처 1(저장소 첫 화면) |
| 2일차 | 오늘 순서와 탭 세 개 → 채점표 10점 → 2분 시연 한 번 보기 → 공개 주소가 안 열리면 → 발표 시작 | **발표 2분 × 인원** → 총평과 10주차 예고 → README 를 고쳤으면 push | 발표 |

각 수업은 `설명·시연 30분 + 실습 60분` 이다. 마크다운은 1일차 하루에 모두 보고, 2일차 60분은 발표(평가)다. 먼저 끝난 학생은 [실습지](lab.md)의 "먼저 끝났다면"을 한다.

## 준비

- 7주차 완성본. 내 `web-week07` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [7주차 `examples/day2/web-week07/`](../week07_form_input/examples/day2/web-week07/) 파일을 **Raw** 로 받는다. 8주차 시험 저장소 `web-week08` 은 이번 과제와 관계가 없다
- VS Code(마크다운 미리 보기가 들어 있어 따로 설치하지 않는다), Chrome, Git (`git --version` 으로 확인)
- Node.js LTS(선택). [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md))
- 화면 캡처 단축키: Windows **Win+Shift+S**, macOS **⌘+Shift+4**
- 과제 안내와 채점 기준을 미리 읽는다: [1차 과제 안내](project_brief.md) · [채점표 10점](rubric.md)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com` 이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 마크다운 | Markdown | Markdown 标记语言 |
| 제목 | heading | 标题 |
| 목록 | list | 列表 |
| 링크 | link | 链接 |
| 렌더(기호를 읽어 모양으로 그려 보이기) | render | 渲染 |
| 미리 보기 | preview | 预览 |
| 저장소 설명 파일 | README | 说明文件 |
| 강조 | emphasis | 强调 |
| 소스 코드 블록 | code block | 代码块 |
| 표 | table | 表格 |
| 인용 | blockquote | 引用 |
| 도표 | diagram | 图表 |
| 발표·시연 | presentation · demo | 演示 |

## 이번 주 비교 예제

1일차 ex01~ex11 은 마크다운 파일(`.md`)이고 ex09·ex10 에는 SVG 파일이 하나씩 따른다. VS Code 에서 파일을 열고 미리 보기를 옆에 띄워(**Ctrl+K** 다음 **V**, macOS **⌘+K** 다음 **V**) 원문과 렌더된 모양을 비교한다. 올린 뒤에는 GitHub 저장소 화면에서 같은 파일을 연다. 2일차는 발표라서 비교 예제가 없다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_heading.md](examples/day1/ex01_heading.md) | 같은 글자 앞에 `#` 하나 / `##` 둘 / `#` 뒤 띄어쓰기 없음 | 줄 맨 앞 `#` 개수가 제목의 크기를 정한다 | 10행 `##` → `###`, 14행 띄어쓰기 |
| [ex02_list.md](examples/day1/ex02_list.md) | `- ` / 기호 없음 / 띄어쓰기 없음 / `1. ` / 들여쓰기 / `- [x]` | 줄 맨 앞 기호가 목록을 만든다. 기호 없는 줄은 한 문단으로 이어진다 | 2번에 빈 줄, 번호 바꾸기, `- [ ]` |
| [ex03_link.md](examples/day1/ex03_link.md) | 인터넷 주소 / 같은 폴더의 파일 / `]` 와 `(` 사이 띄움 | 대괄호는 보이는 글, 소괄호는 누르면 가는 곳 | 14행 띄어쓰기 지우기, 10행 소괄호 |
| [ex04_emphasis.md](examples/day1/ex04_emphasis.md) | `**` / `*` / `~~`, 조사가 붙은 `**[남기기]**를` / 한 칸 띈 것 | 같은 기호로 앞뒤를 감싼다. 문장 부호 뒤에 글자가 붙으면 닫히지 않는다 | 닫는 별 지우기, 대괄호 지우기 |
| [ex05_image.md](examples/day1/ex05_image.md) | `![글](경로)` / `!` 없음 / 경로 틀림 / `<img width>` | `!` 가 링크를 그림으로 바꾼다. 대괄호 글자는 `alt` 다 | `!` 지우기, `width` |
| [ex06_code.md](examples/day1/ex06_code.md) | 백틱 하나 / 세 개 줄 언어 없음 / 언어 `js` / 안의 기호 | 여러 줄 코드는 백틱 세 개 줄 사이에. 언어 이름이 색을 정한다 | 언어 이름, 닫는 줄 지우기 |
| [ex07_table.md](examples/day1/ex07_table.md) | 구분 줄 있음 / 없음 / `:` 정렬 | 구분 줄이 있어야 표다. `:` 자리가 정렬을 정한다 | 구분 줄 넣기, 줄 더하기, `:` 옮기기 |
| [ex08_quote_rule.md](examples/day1/ex08_quote_rule.md) | `>` / 빈 줄 뒤 `---` / 글 바로 아래 `---` | `>` 는 인용, `---` 는 위의 빈 줄에 따라 가로줄이나 제목이 된다 | 3번에 빈 줄 |
| [ex09_svg.md](examples/day1/ex09_svg.md) + [ex09_shapes.svg](examples/day1/ex09_shapes.svg) | SVG 파일을 그림으로 / 문서 안에 바로 `<svg>` | 도형 하나가 태그 하나, 숫자가 자리와 크기다. GitHub 은 문서 안의 `<svg>` 를 지운다 | `fill`·`width`·`y` |
| [ex10_diagram.md](examples/day1/ex10_diagram.md) + [ex10_site_map.svg](examples/day1/ex10_site_map.svg) | 사각형·선·글자로 그린 사이트 구조 | ex09 의 도형만으로 도표가 된다 | 상자 글자, `x` |
| [ex11_mermaid.md](examples/day1/ex11_mermaid.md) | 언어 이름 `mermaid` / `text` | 연결만 적으면 GitHub 이 자리를 잡아 그린다 | 연결 줄 |

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week09_readme_presentation/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [1차 과제 안내](project_brief.md) · [채점표 10점](rubric.md)
- [예제 설명](examples/README.md) — 1일차 `day1/`(ex01~ex11 의 `.md`, SVG 두 개, 그림 `images/profile.png`), 2일차 `day2/`(완성본 `web-week09/`)
- 2일차 끝의 `web-week09`(1일차 끝과 같다): [README.md](examples/day2/web-week09/README.md) · [index.html](examples/day2/web-week09/index.html) · [about.html](examples/day2/web-week09/about.html) · [guestbook.html](examples/day2/web-week09/guestbook.html) · [styles.css](examples/day2/web-week09/styles.css) · [app.js](examples/day2/web-week09/app.js) · [guestbook.js](examples/day2/web-week09/guestbook.js) · [images/profile.png](examples/day2/web-week09/images/profile.png) · [images/site-map.svg](examples/day2/web-week09/images/site-map.svg) · [screenshots/home.png](examples/day2/web-week09/screenshots/home.png) · [screenshots/guestbook.png](examples/day2/web-week09/screenshots/guestbook.png)
- 정적 서버: [server.mjs](../../tools/static-server/server.mjs) · [사용 안내](../../tools/static-server/README.md)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_readme_presentation

## 완료 기준

- [ ] 새 저장소 `web-week09` 를 만들어 Pages 를 켰고, `ex/` 에 비교 예제가 있고, 각 예제에서 값을 하나 이상 바꿔 push 했다.
- [ ] 저장소 맨 위에 `README.md` 1차판(큰 제목 한 줄과 작은 제목 다섯 항목), `screenshots/` 캡처 두 장(동작한 뒤의 화면), `images/site-map.svg` 도표가 있다.
- [ ] `https://github.com/student01/web-week09` 첫 화면의 파일 목록 아래에 README 가 렌더되어 보인다. 표와 코드 블록이 제 모양이고 도표·캡처 두 장이 깨지지 않으며, 공개 주소·세 페이지 링크를 누르면 모두 열린다.
- [ ] 공개 주소 `https://student01.github.io/web-week09/` 에서 nav 로 세 페이지를 오가고, 버튼과 폼(빈값 안내까지)이 동작한다.
- [ ] 저장소 첫 화면 캡처 1장을 제출했고, 2일차에 2분 발표를 했다.

## 다음 수업 연결

지금 방명록은 남긴 글이 목록에 한 줄씩 쌓이지만 화면에만 있다. 한 줄만 지울 수 없고, 새로고침하면 모두 사라진다.
10주차에는 새 저장소 `web-week10` 을 이번 주 `web-week09` 의 파일에서 시작하고(**Code › Download ZIP**, 못 받으면 교재의 이번 주 [`examples/day2/web-week09/`](examples/day2/web-week09/)), 글을 **배열**에 모아 두고 목록을 배열대로 **다시 그려** 줄마다 지운다. 11주차에는 그 목록을 브라우저 저장소에 남겨 새로고침해도 보이게 한다.
오늘 쓴 README 는 13주차에 최종판으로 다시 쓰고, 14주차 최종 발표의 레포트가 된다. README 1차판 쓰기는 15주차 기말 [문제 은행](../week15_final_exam/examples/README.md)에도 [w09_readme_links](../week15_final_exam/examples/w09_readme_links/README.md) 문제로 들어 있다.

## 공식 참고 자료

- [리포지토리 README 파일에 관하여 — GitHub 문서](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기본 쓰기 및 서식 지정 구문 — GitHub 문서](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [표 구성 — GitHub 문서](https://docs.github.com/ko/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables)
- [코드 블록 만들기 및 강조 표시 — GitHub 문서](https://docs.github.com/ko/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks)
- [다이어그램 만들기 — GitHub 문서](https://docs.github.com/ko/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [SVG 튜토리얼 — MDN](https://developer.mozilla.org/ko/docs/Web/SVG/Tutorials)
- [파일 보기 및 이해 — GitHub 문서](https://docs.github.com/ko/repositories/working-with-files/using-files/viewing-and-understanding-files)
- [GitHub Pages 사이트 만들기 — GitHub 문서](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Markdown and Visual Studio Code — VS Code 문서(영문)](https://code.visualstudio.com/docs/languages/markdown)
- [Markdown Reference — CommonMark(영문)](https://commonmark.org/help/)
