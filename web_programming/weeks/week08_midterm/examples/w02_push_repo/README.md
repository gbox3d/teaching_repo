[8주 문제 은행](../README.md) · [15주 문제 은행](../../../week15_final_exam/examples/README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

# w02_push_repo — 고치고 올리기: add → commit → push

출처: [2주차 실습 제출](../../../week02_github_pages/lab.md#제출--캡처-네-장) · 권장 10분 · 중간 A(HTML) · 기말 A(화면(HTML·CSS·README))

2주차에 한 것처럼 저장소에 올린다. 파일을 조금 고친 뒤 `add` → `commit` → `push` 세 명령으로 GitHub 에 올리고, GitHub 화면과 공개 주소에서 바뀐 것을 확인한다.

## 시작 파일

| 파일 | 지금 상태 |
|---|---|
| `index.html` | 완성된 작은 페이지다. `<p id="note">` 의 글자가 `아직 올리기 전입니다.` 다 |

## 할 일

1. 이 문제 폴더를 내 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 안에 받아 둔다(아래 받기와 올리기).
2. `index.html` 의 `<p id="note">` 글자를 `두 번째 올리기 완료` 로 바꾸고 저장한다.
3. VS Code 터미널(저장소 맨 위)에서 `git status` 로 바뀐 파일을 본 뒤 차례로 친다.
   - `git add .`
   - `git commit -m "update note"`
   - `git push`
4. GitHub 저장소 화면을 새로고침해 이 문제 폴더와 commit 메시지 `update note` 가 보이는지 본다. 1~3분 뒤 공개 주소에서도 바뀐 글자를 본다.

## 확인할 것

- [ ] 내 PC 에서 `index.html` 을 열면 `두 번째 올리기 완료` 가 보인다. `아직 올리기 전입니다.` 는 남아 있지 않다.
- [ ] 터미널에서 `git status` 가 `nothing to commit, working tree clean` 이고, `git log --oneline` 의 첫 줄에 `update note` 가 있다.
- [ ] GitHub 저장소 화면에 이 문제 폴더가 있고, 파일 목록 위에 `update note` 가 보인다.
- [ ] 공개 주소 `https://student01.github.io/web-week08/w02_push_repo/`(15주는 `web-week15`) 에서도 `두 번째 올리기 완료` 가 보인다. 1~3분 걸릴 수 있다.

## 힌트

- 세 명령의 뜻: `add` 는 다음 기록에 넣을 파일을 담고, `commit` 은 메시지와 함께 기록을 확정하고, `push` 는 그 기록을 GitHub 로 올린다. `commit` 만 하면 GitHub 에는 아직 보이지 않는다.
- `git status` 의 빨간 글자는 아직 담지 않은 파일, 초록 글자는 담은(`add` 한) 파일이다.
- 로그인 창이 뜨면 2주차에 쓴 GitHub 계정으로 로그인한다. 공용 PC 면 끝나고 자격 증명을 지운다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 큰 제목 h1 | `올리기 연습` |
| note 의 처음 글자 | `아직 올리기 전입니다.` |
| note 의 바꿀 글자 | `두 번째 올리기 완료` |
| commit 메시지 | `update note` |

시험에서는 같은 문제를 이 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다.

## 받기와 올리기

- 이번 주 저장소(8주는 `web-week08`, 15주는 `web-week15`) 맨 위에 [server.mjs](../../../../tools/static-server/server.mjs) 가 없으면 먼저 **Raw** 로 받아 둔다.
- 저장소 안에 `w02_push_repo/` 폴더를 만든다. 교재의 이 문제 폴더에 있는 시작 파일을 하나씩 열어 **Raw** 를 누르고 Ctrl+S(macOS ⌘+S)로 같은 이름으로 저장한다. 그림도 Raw 를 누르면 그림만 보이는 화면이 열리고, 거기서 같은 방법으로 저장한다. 하위 폴더(그림·데이터)는 GitHub 에서 그 폴더를 눌러 들어가 받고, 내 폴더에도 같은 이름으로 만든다. 저장한 이름 끝에 `.txt` 가 붙었으면 지운다. 이 `README.md`(지금 읽는 문제 문장)는 받지 않는다.
- 저장소 맨 위에서 `node server.mjs` 로 열면 주소는 `http://localhost:8000/w02_push_repo/` 이다. Node 가 없는 PC 는 두 번 눌러 연다.
- `node server.mjs` 로 연 주소나 공개 주소에서는 `favicon.ico` 404 한 줄이 Console·Network 에 보여도 괜찮다(빨간 줄로 세지 않는다). 공개 주소에서 새로고침하면 Status 가 `304` 로 보일 수 있다. 이미 받은 파일을 다시 쓴다는 뜻이다.
- 올린 뒤 공개 주소는 `https://student01.github.io/web-week08/w02_push_repo/`(15주에 풀었다면 `web-week15`)이다.
- 해답은 공개하지 않는다. 위 "확인할 것"이 모두 맞으면 된 것이다.
