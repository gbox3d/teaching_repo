---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 1주차"
footer: "웹 실행 구조와 Git 상태"
---

# 1주차
## 웹 실행 구조와 Git 상태

**주 2회 × 90분**<br>
매회 설명·시연 30분 + 문제 해결 60분

---

## 오늘의 두 질문

1. 주소를 입력한 뒤 화면이 보이기까지 무엇이 일어나는가?
2. 방금 고친 파일은 Git의 어느 상태에 있는가?

완성 화면보다 **관찰하고 설명하는 능력**을 먼저 평가한다.

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## 브라우저는 무엇을 실행하는가

---

## 0–4분 · URL을 읽는 법

```text
http://localhost:8000/about/index.html
└┬─┘   └───┬───┘└─┬─┘└──────┬───────┘
scheme      host   port       path
```

- scheme: 통신 방식
- host: 요청 대상
- port: 프로그램의 접수 창구
- path: 대상 안의 자원 위치

**질문:** `index.html`을 파일 탐색기에서 연 것과 무엇이 다른가?

---

## 4–9분 · 요청과 응답

```text
Browser  ── GET /index.html ──▶  Server
Browser  ◀─ 200 + HTML ────────  Server
```

- 요청: method, URL, headers, 때로는 body
- 응답: status, headers, body
- `200`: 성공, `404`: 자원 없음

화면이 이상하면 먼저 **어떤 요청이 실패했는지** 찾는다.

---

## 9–14분 · 세 언어의 책임

| 파일 | 책임 | 예시 |
|---|---|---|
| HTML | 의미와 구조 | 제목, 본문, 링크, 버튼 |
| CSS | 표현과 배치 | 색상, 간격, 반응형 배치 |
| JavaScript | 상태와 동작 | 클릭, 계산, 화면 변경 |

한 파일에 모두 쓸 수 있어도 책임을 분리하면 오류 위치를 찾기 쉽다.

---

## 14–21분 · 파싱과 추가 요청

```text
index.html
 ├─ <link href="styles.css">  → CSS 요청
 └─ <script src="app.js">     → JavaScript 요청
```

1. HTML 응답 수신
2. HTML을 DOM으로 파싱
3. 연결된 자원 추가 요청
4. CSS 적용, JavaScript 실행

**예상:** `styles.css` 이름이 틀리면 HTML도 사라질까?

---

## 21–27분 · DevTools 3개 탭

- **Elements:** 실제 DOM과 적용된 style
- **Console:** JavaScript 출력과 실행 오류
- **Network:** 요청 URL, status, 응답 종류

진단 순서:

```text
증상 재현 → Network 실패 확인 → Console 오류 확인 → Elements 상태 확인
```

---

## 27–30분 · 실습 전 예측

예제에서 다음을 먼저 예상한다.

1. 최초 상태 문구는 무엇인가?
2. 버튼을 누르면 어느 파일의 코드가 동작하는가?
3. CSS 경로를 틀리면 Network status는 무엇인가?

예측을 적은 뒤 [실습 1](lab.md#1일차-실습--요청에서-화면까지-추적하기)을 시작한다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## Git은 파일이 아니라 상태 변화를 기록한다

---

## 0–3분 · Git이 해결하는 질문

- 무엇을 바꾸었는가?
- 다음 기록에 무엇을 포함할 것인가?
- 이전 기록과 어떻게 다른가?
- 왜 이 변경을 했는가?

Git은 자동 저장 장치가 아니다. **의도 있는 스냅샷의 역사**다.

---

## 3–8분 · `git init` — 저장소와 untracked

```bash
git init          # 현재 폴더에 .git/ 을 만든다 = 저장소 본체
git branch -M main
```

```text
$ git status
On branch main
No commits yet
Untracked files:
        index.html
nothing added to commit but untracked files present
```

- `.git/`이 이력 전체다. 작업 파일과 이력은 **다른 것**이다.
- 폴더 안에 있다고 추적되지 않는다. `index.html`은 아직 **untracked**다.
- identity 오류가 나면 이 저장소에만 `git config user.name` / `user.email`을 설정한다.

---

## 8–13분 · 세 영역

```text
untracked ─┐
           ├─ git add ─▶ staging area ─ git commit ─▶ repository
modified ──┘             다음 기록 후보               확정 기록
 working tree
```

- `untracked`: Git이 아직 모르는 새 파일. `git add`로 처음 추적된다.
- `staging area(index)`: **다음 commit에 담기로 고른 것**만 모인 곳
- `HEAD`: 현재 보고 있는 commit
- 같은 파일이 staged와 unstaged 변경을 동시에 가질 수도 있다.

---

## 13–18분 · `git status`가 답을 알려 준다

```text
Changes to be committed:          ← staging area
        modified:   app.js
Changes not staged for commit:    ← working tree (추적 중)
        modified:   app.js
Untracked files:                  ← working tree (추적 전)
        notes.txt
```

- 같은 `app.js`가 위아래에 **동시에** 나온다. commit은 파일이 아니라 `git add` 한 순간의 스냅샷을 기록하기 때문이다.
- 각 제목 밑 괄호 안내문이 그 영역에서 되돌리는 명령을 알려 준다. 첫 commit 전에는 `git rm --cached`, 이후에는 `git restore --staged`다.
- 명령을 치기 전에 **"이 파일이 지금 어느 제목 아래에 있는가"**를 먼저 말한다.

---

## 18–22분 · 두 diff는 다르다

```bash
git diff
git diff --staged
```

- `git diff`: working tree ↔ staging area
- `git diff --staged`: staging area ↔ HEAD

**질문:** `git add` 뒤 첫 번째 diff가 비어도 변경이 사라진 것은 아니다. 어디에 있는가?

---

## 22–25분 · 최소 작업 순환

```bash
git status
git diff
git add index.html
git diff --staged
git commit -m "Add page heading"
git log --oneline --decorate -3
```

명령을 외우기보다 각 명령 전후에 어느 화살표가 이동하는지 말한다.

---

## 25–27분 · 좋은 commit의 크기

나쁨:

```text
update
final
여러 가지 수정
```

좋음:

```text
Add course page heading
Style primary action button
Explain click result in status text
```

한 문장으로 설명하기 어려우면 변경을 나눌 신호다.

---

## 27–29분 · 안전한 되돌리기

```bash
git restore --staged index.html  # stage에서만 내림
git restore index.html           # 작업 내용 폐기: 실행 전 diff 확인
```

`restore`는 결과가 다르다. 대상과 되돌릴 영역을 말할 수 없으면 실행하지 않는다.

---

## 29–30분 · 실습 성공 기준

- 제목, 설명, 동작을 각각 별도 commit
- 매번 `diff --staged`를 읽고 commit
- 마지막 `status`는 clean
- 세 영역을 자기 말로 5문장 설명

[실습 2](lab.md#2일차-실습--의미-있는-세-번의-커밋)를 시작한다.

---

## 이번 주 정리

```text
웹: URL → HTTP → HTML 파싱 → CSS/JS 요청 → 화면·동작
Git: working tree → stage → commit → history
```

공통점은 같다. 결과만 보지 말고 **중간 상태를 관찰**한다.
