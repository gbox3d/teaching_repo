[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w04_box_style — 상자 꾸미기와 글자 가운데

출처: [4주차 실습 제출](../../../week04_responsive_css/lab.md#제출--캡처-한-장) · 권장 10분 · 중간 B(CSS) · 기말 A(화면(HTML·CSS·README))

6주차 실습(검은 상자·글자색·테두리)과 같은 상자를 다른 값으로 만든다. 상자 안의 세 줄은 가로·세로 모두 가운데에 둔다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | `<style>` 과 본문이 한 파일에 있다. `.box` 안에 `<p>` 세 줄이 있고, `.box` 규칙은 주석 두 줄뿐이다 |

## 할 일

`.box` 규칙 안에 쓴다. HTML 은 고치지 않는다.

1. 할 일 1(모양): 너비 `300px`, 높이 `300px`, 배경색 `black`, 글자색 `lightgreen`, 테두리 두께 `4px`·모양 `solid`·색 `gold`, 안쪽 여백은 네 방향 모두 `8px`.
2. 할 일 2(가운데): 세 줄이 상자의 **가로·세로 모두 가운데**에 오게 한다. `display: flex` 와 `flex-direction: column` 을 쓴다.
3. 저장 → 새로고침 → F12 › Elements 에서 `.box` 를 고르고 Styles 에 쓴 값이 그대로 들어갔는지 본다.

## 확인할 것

- [ ] 배경이 `black`, 글자가 `lightgreen` 색이고, 테두리가 `4px solid gold` 로 보인다.
- [ ] 세 줄 `ID: student01` · `Name: Hong Gildong` · `Course: Web Programming` 이 상자의 가로 가운데, 세로 가운데에 모여 있다. 위쪽 빈 공간과 아래쪽 빈 공간이 같다.
- [ ] F12 › Elements 에서 `.box` 를 고르면 Styles 맨 아래 상자 그림의 padding 네 칸이 `8`, border 네 칸이 `4`, 내용 폭·높이가 `300×300` 이다.
- [ ] F12 › Console 에 빨간 줄이 없다.

## 힌트

- 6주차에 쓴 속성 그대로다. `width`, `height`, `background-color`, `color`, `border: 두께 모양 색`, `padding`.
- 글자를 가운데로 모으는 것은 7주차 배치와 같은 속성이다. `flex-direction: column` 일 때는 `justify-content` 가 세로, `align-items` 가 가로를 맡는다. 둘 다 `center` 로 둔다.
- `text-align: center` 만 쓰면 가로만 가운데가 되고 세로는 위에 붙는다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 상자 너비(px) | `300` |
| 상자 높이(px) | `300` |
| 배경색 | `black` |
| 글자색 | `lightgreen` |
| 테두리 두께(px) | `4` |
| 테두리 선 모양 | `solid` |
| 테두리 색 | `gold` |
| 안쪽 여백(px) | `8` |
| 첫 줄 | `ID: student01` |
| 둘째 줄 | `Name: Hong Gildong` |
| 셋째 줄 | `Course: Web Programming` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w04_box_style/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w04_box_style/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w04_box_style/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
