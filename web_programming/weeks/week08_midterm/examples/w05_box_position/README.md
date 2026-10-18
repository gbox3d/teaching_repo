[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w05_box_position — 틀 안의 상자를 지정 위치에

출처: [4주차 실습 제출](../../../week04_responsive_css/lab.md#제출--캡처-한-장) · 권장 10분 · 중간 B(CSS) · 기말 A(화면(HTML·CSS·README))

7주차 실습(상자를 상단 중앙·상단 우측·하단 우측에 놓기)과 같은 일을 다른 위치로 한다. 회색 틀 세 개 안에 작은 상자가 하나씩 있다. 각 상자를 적힌 위치로 옮긴다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 틀(`.frame`) 세 개와 그 안의 상자(`.item`)가 있다. `.frame` 에는 이미 `display: flex` 가 있고, 위치를 정할 `.p1`·`.p2`·`.p3` 규칙은 비어 있다 |

## 할 일

`.p1`·`.p2`·`.p3` 규칙 안에만 쓴다. HTML 과 `.frame`·`.item` 규칙은 고치지 않는다. `position` 이나 `margin` 숫자는 쓰지 않는다.

1. 1번 틀(`.p1`): 상자를 **상단 중앙** 에 둔다.
2. 2번 틀(`.p2`): 상자를 **하단 우측** 에 둔다.
3. 3번 틀(`.p3`): 상자를 **정중앙** 에 둔다.
4. 저장 → 새로고침 → 틀마다 상자가 그 자리에 있는지 본다.

## 확인할 것

- [ ] 1번 틀의 상자가 상단 중앙, 2번 틀의 상자가 하단 우측, 3번 틀의 상자가 정중앙 에 있다. 틀의 가장자리와 상자의 가장자리가 그 방향에서 딱 붙어 있고, 가운데는 양쪽 빈 공간이 같다.
- [ ] F12 › Elements 에서 각 틀을 고르면 Styles 에 `justify-content` 와 `align-items` 두 줄만 더 있다. `position`·`margin` 은 없다.
- [ ] 세 상자의 크기(60×60)와 색(orange)은 처음과 같다.
- [ ] F12 › Console 에 빨간 줄이 없다.

## 힌트

- 틀이 `display: flex` 이고 방향이 기본(row)이면 `justify-content` 가 **가로**(왼쪽·가운데·오른쪽), `align-items` 가 **세로**(위·가운데·아래)를 맡는다.
- 쓸 수 있는 값은 세 가지다. `flex-start`(앞·위), `center`(가운데), `flex-end`(끝·아래).
- 예: 상단 우측 = 가로는 오른쪽 끝, 세로는 위 → `justify-content: flex-end; align-items: flex-start;`.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 틀 너비(px) | `300` |
| 틀 높이(px) | `150` |
| 상자 한 변(px) | `60` |
| 상자 색 | `orange` |
| 1번 틀의 위치 | `상단 중앙` |
| 2번 틀의 위치 | `하단 우측` |
| 3번 틀의 위치 | `정중앙` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w05_box_position/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w05_box_position/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w05_box_position/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
