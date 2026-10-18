[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# 8주차 따라하기 — 문제 은행 연습과 시험 날

1일차는 은행 문제 하나를 받아 풀고 확인하는 순서, 2일차는 시험 날 순서다. 문제 문장은 [문제 은행](examples/README.md)에 있고, 시간 배분은 [실습지](lab.md)에 있다.
`student01` 은 예시 아이디다. 본인 아이디로 바꿔 읽는다.

## 1일차

### 1. 폴더 만들고 server.mjs 받기

1. 바탕화면이나 작업 폴더에 새 폴더 `web-week08` 을 만든다.
2. VS Code **File › Open Folder** 로 그 폴더를 연다.
3. [server.mjs](../../tools/static-server/server.mjs) 를 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 `web-week08` 맨 위에 같은 이름으로 저장한다. Node 가 없는 PC 는 이 단계를 건너뛰고 파일을 두 번 눌러 연다.

### 2. 문제 하나 읽는 법: w04_box_style

[w04_box_style](examples/w04_box_style/README.md) 을 연다. 모든 문제가 같은 순서다.

```text
첫 줄           무엇을 다시 만드는지 한 문장 (6주차 실습의 상자)
시작 파일        받을 파일과 지금 상태. "고치지 않는다" 파일은 그대로 둔다
할 일           고칠 파일과 자리, 쓸 값. 적힌 순서대로 한다
확인할 것        화면·F12 로 스스로 맞춰 보는 목록. 해답 대신이다
힌트            막혔을 때 읽는다. 시험의 설명 물음이 여기 있는 내용이다
이 문제의 값      시험에서 바뀌는 값. w04 는 300·300·black·lightgreen·4px solid gold·8 …
받기와 올리기     web-week08/w04_box_style/ 에 Raw 로 받는다
```

"확인할 것"의 예: 배경이 `black`, 글자가 `lightgreen`, 테두리가 `4px solid gold`, 세 줄이 상자 가로·세로 가운데.
값은 표에서 **복사해 붙여 넣는다.** 한 글자만 달라도 확인할 것이 맞지 않는다.

### 3. 문제 폴더 만들고 Raw 로 받기

1. VS Code 탐색기에서 `web-week08` 안에 새 폴더 `w04_box_style` 을 만든다(문제 id 와 같게).
2. 교재의 문제 폴더에서 시작 파일(`index.html`)을 눌러 **Raw** → Ctrl+S 로 그 폴더에 같은 이름으로 저장한다. 파일이 여럿인 문제(w06·w07의 `app.js`)는 하나씩 받는다.
3. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 문제 문장 `README.md` 는 받지 않는다.

### 4. 열기

- 두 번 눌러 열기: 탐색기에서 `index.html` 을 두 번 누른다. 주소가 `file://` 로 시작한다. 대부분의 "확인할 것"은 이 화면으로 본다.
- 서버로 열기: VS Code 터미널(**Terminal › New Terminal**, 현재 폴더 `web-week08`)에서 `node server.mjs` → 브라우저에서 `http://localhost:8000/w04_box_style/` 를 연다. Network 의 Status 번호(`200`·`404`)를 보라는 항목은 이 주소에서 본다.

### 5. 할 일 하고 확인할 것 맞추기

1. "시작 파일" 표를 보고 고칠 파일을 연다. w04 는 `index.html` 의 `<style>` 안 `.box` 규칙이다.
2. 할 일 1(모양)을 쓰고 저장 → 새로고침. 색·테두리·여백이 바뀌는지 본다.
3. 할 일 2(가운데)를 쓰고 저장 → 새로고침. 세 줄이 가로·세로 가운데에 모이는지 본다.
4. "확인할 것"을 위에서부터 하나씩 한다. F12 › Elements 에서 `.box` 를 고르고 Styles 맨 아래 상자 그림의 padding·border·내용 크기를 읽는다.
5. 맞지 않는 항목이 있으면 그 항목이 가리키는 할 일로 돌아간다. 막히면 **힌트**를 읽는다. 모두 맞으면 다음 문제로 간다.

같은 순서로 w05 → w03 → w01 … 을 푼다. 문제마다 10분을 넘기면 남은 항목을 적어 두고 다음 문제로 간다.

### 6. 올리기 — w02_push_repo

[실습지 3번](lab.md#3-올리기--w02_push_repo)의 명령으로 저장소 `web-week08` 을 만들어 올린 뒤, w02 문제의 할 일대로 파일을 고쳐 `git add .` → `git commit -m "update note"` → `git push` 를 한 번 더 한다.
GitHub 저장소 화면을 새로고침해 폴더와 commit 메시지가 보이면 된 것이다. **Settings › Pages** 를 켜 두면 1~3분 뒤 `https://student01.github.io/web-week08/w04_box_style/` 로 연습한 문제를 볼 수 있다.

## 2일차

### 7. 시험 전

- 분반 공지를 다시 읽는다. 시작·끝 시각, 문제 수, 볼 수 있는 것, 내는 곳(LMS 답안 칸 또는 저장소).
- VS Code 로 `web-week08` 을 열고 브라우저와 F12 가 열리는지 본다. 저장소 제출이면 GitHub 로그인까지 해 둔다.
- 캡처 단축키를 확인한다. Windows **Win+Shift+S**, macOS **⌘+Shift+4**.

### 8. 문제 읽기와 값 표시

시험이 시작되면 문제를 끝까지 읽는다. 문제마다 "이 문제의 값"이 은행 문제와 어디가 다른지 표시한다(색·글자·위치·id·파일 이름). 아직 코드를 쓰지 않는다. 3분 안에 끝낸다.

### 9. 문제 풀기와 캡처

1. 시작 파일이 있으면 1일차와 같은 방법으로 받아 문제 폴더에 둔다.
2. 할 일을 위에서부터 한 덩어리씩 하고, 덩어리마다 저장 → 새로고침 → Console.
3. "확인할 것"을 하나씩 맞춘다. 맞춘 상태의 브라우저 화면을 **주소창이 보이게** 캡처한다. F12 를 보라는 항목은 그 패널이 보이게 한 장 더 찍는다.
4. 오래 막히면 다음 문제로 간다. 넘긴 문제는 남는 시간에 돌아온다.

### 10. 설명 쓰기

문제가 묻는 물음에 자기 말로 1~2문장을 쓴다. 힌트에 있는 내용 수준이면 된다. 예: "row 방향에서 `justify-content` 는 가로, `align-items` 는 세로를 맡는다." 코드를 베끼지 않고 무엇이 어떻게 됐는지 쓴다.

### 11. 제출

- LMS 답안 칸 방식: 문제마다 코드 → 캡처 → 설명 순서로 붙여 넣는다. 끝나기 5분 전에 빠진 것이 없는지 본다.
- 저장소 방식: `web-week08/exam/` 에 문제 폴더를 두고 `git add .` → `git commit -m "중간 실기 끝"` → `git push`. 공개 주소 `https://student01.github.io/web-week08/exam/`, 저장소 주소, GitHub **Commits** 탭 캡처(맨 위 commit 의 번호와 시각)를 낸다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 공용 PC 면 자격 증명을 지우고 나간다.

## 오류가 나면

| 증상 | 확인할 것 |
|---|---|
| 받은 파일이 `index.html.txt` 다 | 브라우저가 붙인 것이다. VS Code 탐색기에서 이름을 고친다 |
| Console 에 `Cannot read properties of null` | `querySelector` 의 `#` 과 철자를 HTML 의 `id` 와 비교한다. `script` 줄의 `defer` 도 본다 |
| 폼 버튼을 누르면 페이지가 다시 열린다 | `submit` 이벤트 안 첫 줄에 `event.preventDefault()` 를 쓴다 |
| 상자 글자가 세로 가운데가 아니다 | `text-align: center` 만 썼다. `display: flex; flex-direction: column;` 에 `justify-content: center; align-items: center;` 를 함께 쓴다 |
| push 가 거부된다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때). 시험 중이면 손을 들고 오류 메시지를 답안에 적는다 |

더 많은 증상은 [실습지 막혔을 때](lab.md#막혔을-때)에 있다.
