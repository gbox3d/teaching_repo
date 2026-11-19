[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_readme_presentation)

# 9주차 마크다운과 1차 과제 발표

1일차는 강의·시연 60분과 README 작성 30분이다. 제목·목록·링크·그림·코드·표를 배운 뒤 제공 시작 틀을 본인 사이트 내용으로 채운다. SVG는 제공 도표의 글자만 고친다. 강조·인용·SVG 좌표 작성·Mermaid는 선택 자료다.

2일차는 안내 5분·발표 75분·피드백 10분이다. 7주차 완성 웹 파일은 고치지 않는다. 이번 주에 추가하는 파일은 README, 화면 캡처 두 장, 사이트 도표다. 배점은 기존 1차 과제 10점(발표 5+README 5)을 유지한다.

## 학습 목표

1. VS Code 미리 보기에서 제목·목록·링크·그림·코드·표의 원문과 결과를 비교한다.
2. 제공 [README 시작 틀](examples/day2/web-week09/README.start.md)의 주소·페이지·기능·화면·배운 내용을 본인 사이트에 맞게 쓴다.
3. 제공 SVG의 글자를 고쳐 도표를 넣고, 이미지와 상대 링크를 확인한다.
4. 홈·소개·방명록과 입력 동작을 2분 안에 시연한다.

## 이번 주 결과물

- 저장소 맨 위 README 1차판: 공개 주소·페이지·기능·화면·이번에 배운 것 다섯 항목
- 버튼을 누른 홈과 두 글을 남긴 방명록의 캡처 두 장, 제공 SVG 글자를 고친 도표
- 저장소 첫 화면 캡처 1장과 2분 시연

## 2일 수업 흐름

| 차시 | 강의·시연 또는 안내 | 학생 활동 |
|---|---|---|
| 1일차 | 60분: 준비 5, 제목·목록·링크 15, 그림·코드·표 20, 제공 SVG 사용 10, 시연 순서 5, 실습 안내 5 | 30분: 제목·주소·표 10, 캡처·코드·기능 두 줄·배운 것 세 줄 10, SVG 글자·미리 보기 5, 확인 5 |
| 2일차 | 안내 5분, 피드백 10분 | 발표 75분. 30명까지 1인 시연 2분+전환 30초 |

파일과 저장소 준비는 수업 전에, 업로드는 1일차 수업 뒤에 한다. 실습 시간에는 localhost 동작과 VS Code 미리 보기를 확인한다. 비교 예제 11개를 모두 수정하는 과제는 없다. 31명 이상 분반의 사전 영상·표본 발표·개인 설명 시간은 [발표 운영](project_brief.md#발표-인원과-운영)에 따른다.

## 준비

- 7주차 완성본. 내 `web-week07` 저장소 GitHub 화면 › **Code › Download ZIP** 으로 받는다. 못 받으면 교재 [7주차 `examples/day2/web-week07/`](../week07_form_input/examples/day2/web-week07/) 파일을 **Raw** 로 받는다. 8주차 시험 저장소 `web-week08` 은 이번 과제와 관계가 없다
- VS Code(마크다운 미리 보기가 들어 있어 따로 설치하지 않는다), Chrome, Git (`git --version` 으로 확인)
- Node.js 24 LTS. [server.mjs](../../tools/static-server/server.mjs) 를 이번 주 폴더에도 둔다([사용 안내](../../tools/static-server/README.md))
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

## 강의자 시연과 선택 예제

강의자 시연·선택 참고용 ex01~ex11 은 마크다운 파일(`.md`)이고 ex09·ex10 에는 SVG 파일이 하나씩 따른다. VS Code 에서 파일을 열고 미리 보기를 옆에 띄워(Ctrl+K 다음 V, macOS ⌘+K 다음 V) 원문과 렌더된 모양을 비교한다. 올린 뒤에는 GitHub 저장소 화면에서 같은 파일을 연다. 2일차는 발표라서 비교 예제가 없다.

| 파일 | 비교하는 것 | 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01_heading.md](examples/day1/ex01_heading.md) | 같은 글자 앞에 `#` 하나 / `##` 둘 / `#` 뒤 띄어쓰기 없음 | 줄 맨 앞 `#` 개수가 제목의 크기를 정한다 | 10행 `##` → `###`, 14행 띄어쓰기 |
| [ex02_list.md](examples/day1/ex02_list.md) | `- ` / 기호 없음 / 띄어쓰기 없음 / `1. ` / 들여쓰기 / `- [x]` | 줄 맨 앞 기호가 목록을 만든다. 기호 없는 줄은 한 문단으로 이어진다 | 2번에 빈 줄, 번호 바꾸기, `- [ ]` |
| [ex03_link.md](examples/day1/ex03_link.md) | 인터넷 주소 / 같은 폴더의 파일 / `]` 와 `(` 사이 띄움 | 대괄호는 보이는 글, 소괄호는 누르면 가는 곳 | 14행 띄어쓰기 지우기, 10행 소괄호 |
| 선택: [ex04_emphasis.md](examples/day1/ex04_emphasis.md) | `**` / `*` / `~~`, 조사가 붙은 `**[남기기]**를` / 한 칸 띈 것 | 같은 기호로 앞뒤를 감싼다. 문장 부호 뒤에 글자가 붙으면 닫히지 않는다 | 닫는 별 지우기, 대괄호 지우기 |
| [ex05_image.md](examples/day1/ex05_image.md) | `![글](경로)` / `!` 없음 / 경로 틀림 / `<img width>` | `!` 가 링크를 그림으로 바꾼다. 대괄호 글자는 `alt` 다 | `!` 지우기, `width` |
| [ex06_code.md](examples/day1/ex06_code.md) | 백틱 하나 / 세 개 줄 언어 없음 / 언어 `js` / 안의 기호 | 여러 줄 코드는 백틱 세 개 줄 사이에. 언어 이름이 색을 정한다 | 언어 이름, 닫는 줄 지우기 |
| [ex07_table.md](examples/day1/ex07_table.md) | 구분 줄 있음 / 없음 / `:` 정렬 | 구분 줄이 있어야 표다. `:` 자리가 정렬을 정한다 | 구분 줄 넣기, 줄 더하기, `:` 옮기기 |
| 선택: [ex08_quote_rule.md](examples/day1/ex08_quote_rule.md) | `>` / 빈 줄 뒤 `---` / 글 바로 아래 `---` | `>` 는 인용, `---` 는 위의 빈 줄에 따라 가로줄이나 제목이 된다 | 3번에 빈 줄 |
| 선택: [ex09_svg.md](examples/day1/ex09_svg.md) + [ex09_shapes.svg](examples/day1/ex09_shapes.svg) | SVG 파일을 그림으로 / 문서 안에 바로 `<svg>` | 도형 하나가 태그 하나, 숫자가 자리와 크기다. GitHub 은 문서 안의 `<svg>` 를 지운다 | `fill`·`width`·`y` |
| [ex10_diagram.md](examples/day1/ex10_diagram.md) + [ex10_site_map.svg](examples/day1/ex10_site_map.svg) | 사각형·선·글자로 그린 사이트 구조 | ex09 의 도형만으로 도표가 된다 | 상자 글자만 필수. `x` 수정은 선택 |
| 선택: [ex11_mermaid.md](examples/day1/ex11_mermaid.md) | 언어 이름 `mermaid` / `text` | 연결만 적으면 GitHub 이 자리를 잡아 그린다 | 연결 줄 |

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

- [ ] 수업 전에 `web-week09` 파일·저장소를 준비했고, 수업 뒤 README와 캡처를 업로드했다. 예제 전체 수정은 필수가 아니다.
- [ ] 저장소 맨 위에 `README.md` 1차판(큰 제목 한 줄과 작은 제목 다섯 항목), `screenshots/` 캡처 두 장(동작한 뒤의 화면), `images/site-map.svg` 도표가 있다.
- [ ] `https://github.com/student01/web-week09` 첫 화면의 파일 목록 아래에 README 가 렌더되어 보인다. 표와 코드 블록이 제 모양이고 도표·캡처 두 장이 깨지지 않으며, 공개 주소·세 페이지 링크를 누르면 모두 열린다.
- [ ] 공개 주소 `https://student01.github.io/web-week09/` 에서 nav 로 세 페이지를 오가고, 버튼과 폼(빈값 안내까지)이 동작한다.
- [ ] 저장소 첫 화면 캡처 1장을 제출했고, 인원별 운영에 따라 2분 현장 시연 또는 사전 영상과 현장 개인 설명을 마쳤다.

## 다음 수업 연결

9주 방명록은 작성자·시각·본문을 최신순으로 보여 준다. 새로고침하면 글이 사라진다.
10주에는 [배열 실습용 시작 폴더](../week10_array_list/examples/day2/web-week10/)에 이번 주 홈·내 정보를 옮긴다. 방명록은 제공된 `guestbook.start.html`에서 시작한다. 글을 문자열 배열에 등록순으로 담아 첫 줄과 `items[0]`를 비교하고 가운데 글을 지운다. 11주차 필수 실습은 폼 한 객체의 저장·복원이며, 전체 저장 방명록은 제공 시연본으로 비교한다.
오늘 쓴 README는 이후 기능을 추가할 때 갱신한다. 레포트는 별도 과제로 안내하며 14주는 REST 수정·삭제 실습이다. README 1차판 쓰기는 15주차 기말 [문제 은행](../week15_final_exam/examples/README.md)에도 [w09_readme_links](../week15_final_exam/examples/w09_readme_links/README.md) 문제로 들어 있다.

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
