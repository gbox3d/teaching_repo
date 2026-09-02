# 1주차 실습 — 요청과 상태를 추적하라

## 공통 규칙

- 완성 코드를 보기 전에 예상표를 작성한다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 실습에서 정상 경로와 실패 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.

## 1일차 실습 — 요청에서 화면까지 추적하기

### 상황

동료가 “페이지는 열리는데 어떤 파일이 어떤 역할을 하는지 모르겠다”고 도움을 요청했다. 예제의 요청과 실행 과정을 관찰하고, 의도적으로 만든 경로 오류를 증거로 진단하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–10분 | 파일 목록을 보고 요청과 결과 예상 |
| 정상 관찰 | 10–25분 | 서버 실행, Network/Elements/Console 관찰 |
| 오류 재현 | 25–42분 | CSS 또는 JS 경로 오류를 만들고 원인 추적 |
| 복구·변형 | 42–52분 | 최소 수정으로 복구하고 상태 문구 변형 |
| 검증·회고 | 52–60분 | 체크리스트와 관찰표 완성 |

### 준비

원본을 직접 훼손하지 않도록 `examples` 폴더를 개인 실습 폴더에 복사한다. 복사한 폴더에서 다음을 실행한다.

```powershell
node server.mjs
```

브라우저에서 `http://localhost:8000/`을 연다. 종료는 터미널에서 `Ctrl+C`다.

### 문제 1 · 실행 전 예상

다음 표를 노트에 작성한다.

| 관찰 대상 | 예상 | 실제 | 차이가 난 이유 |
|---|---|---|---|
| 최초 상태 문구 |  |  |  |
| 버튼 2회 클릭 뒤 문구 |  |  |  |
| 요청되는 파일 수 |  |  |  |
| CSS 경로가 틀렸을 때 status |  |  |  |
| JS 경로가 틀렸을 때 버튼 |  |  |  |

### 문제 2 · 정상 경로 추적

1. DevTools를 열고 Network 탭에서 `Disable cache`를 선택한다.
2. 새로고침하고 document, stylesheet, script 요청을 각각 찾는다.
3. 각 요청의 Request URL, Status, Type을 표에 기록한다.
4. Elements 탭에서 `<main>`, `<button>`, `<output>`을 찾는다.
5. Console의 준비 메시지를 확인한다.
6. 버튼을 두 번 누르고 DOM의 `<output>` 내용 변화를 관찰한다.

완료 조건:

- [ ] 세 자원의 요청 URL과 status를 기록했다.
- [ ] 소스 HTML과 실행 중 DOM의 관계를 한 문장으로 설명했다.
- [ ] 버튼 동작을 담당한 파일과 근거를 적었다.

### 문제 3 · 실패 경로 진단

복사본 `index.html`에서 아래 둘 중 하나만 선택해 의도적으로 오류를 만든다.

- `<link href="styles.css">`를 `style.css`로 바꾼다.
- `<script src="app.js">`를 `apps.js`로 바꾼다.

새로고침한 뒤 다음 순서로 진단한다.

1. 눈에 보이는 증상을 한 문장으로 적는다.
2. Network에서 실패 요청과 status를 기록한다.
3. Console의 첫 관련 메시지를 기록한다.
4. Elements에서 실제 속성값을 확인한다.
5. 한 줄만 고쳐 복구하고 실패 요청이 사라졌는지 검증한다.

금지: 원인을 확인하기 전에 여러 파일을 동시에 수정하지 않는다.

### 단계별 힌트

<details>
<summary>힌트 1 — 서버가 시작되지 않는다</summary>

`node --version`과 `Get-Location`을 확인한다. `server.mjs`가 보이는 폴더에서 명령을 실행해야 한다.
</details>

<details>
<summary>힌트 2 — Network 목록이 비어 있다</summary>

DevTools를 연 상태로 새로고침한다. 필터가 `Fetch/XHR`에만 걸려 있지 않은지 확인하고 `All`을 선택한다.
</details>

<details>
<summary>힌트 3 — 어느 경로가 잘못됐는지 모르겠다</summary>

실패 행의 Request URL 마지막 이름과 파일 탐색기의 실제 이름을 문자 단위로 비교한다.
</details>

### 검증

- 정상: 첫 화면에 `클릭 횟수: 0`, 클릭 2회 후 `클릭 횟수: 2`가 보인다.
- 경계: 새로고침하면 메모리 상태가 초기화되어 다시 0이다.
- 실패: 잘못된 파일 경로는 Network에서 404이며, 복구 후 200이다.
- 설명: HTTP 200과 JavaScript 정상 실행이 같은 뜻이 아닌 이유를 적었다.

### 확장 문제

1. `http://localhost:8000/missing.html`의 404 응답 body와 headers를 관찰한다.
2. HTML을 수정하지 않고 CSS custom property `--accent`만 바꾸어 화면 변화를 설명한다.
3. 버튼을 세 번 누를 때마다 다른 메시지를 보이게 수정하고 어떤 책임이 JavaScript에 있는지 설명한다.

## 2일차 실습 — 의미 있는 세 번의 커밋

### 상황

한꺼번에 완성한 페이지가 아니라, 제목→설명→동작의 세 의도가 드러나는 이력을 만들어야 한다. 각 시점의 Git 상태를 말로 설명하며 commit하라.

### 안전 준비

1일차 복사본과 별도의 새 폴더를 사용한다. 상위 수업 자료 저장소 안에서 `git init`하지 않는다.

```powershell
New-Item -ItemType Directory week01-practice
Set-Location week01-practice
git init
git branch -M main
```

Git이 사용자 이름과 이메일을 요구하면 강의자 안내에 따라 수업용 설정을 사용한다. 공유 PC에서는 전역 설정을 임의로 바꾸지 않는다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 저장소 준비 | 0–8분 | init, branch, 상태 확인 |
| commit 1 | 8–20분 | 페이지 구조와 제목 |
| commit 2 | 20–32분 | 설명과 링크 |
| commit 3 | 32–45분 | 버튼 동작 |
| 상태 변형 | 45–53분 | staged+unstaged 동시 상태 관찰 |
| 검증·회고 | 53–60분 | log, clean, 5문장 회고 |

### 문제 1 · commit 계획

| 순서 | 사용자에게 보이는 변화 | 수정 파일 | 예정 메시지 |
|---:|---|---|---|
| 1 | 페이지 제목과 기본 구조 | `index.html` | `Add course page structure` |
| 2 | 수업 설명과 참고 링크 | `index.html` | `Add course introduction` |
| 3 | 클릭 횟수 동작 | `index.html`, `app.js` | `Count practice button clicks` |

메시지는 그대로 써도 되지만 실제 변경과 맞지 않으면 고친다.

### 문제 2 · 매 commit의 고정 순환

각 변경마다 아래 순환을 생략하지 않는다.

```bash
git status
git diff
git add <이번 의도의 파일>
git diff --staged
git commit -m "<의도를 드러내는 메시지>"
```

각 commit 직전에 다음 질문에 답한다.

- staged diff에 이번 의도와 무관한 변경이 있는가?
- 새 파일 전체가 들어가는 것이 맞는가?
- commit 메시지만 읽어도 사용자에게 생긴 변화를 알 수 있는가?

### 문제 3 · 같은 파일의 두 상태 만들기

세 번째 commit 전에 다음 상태를 의도적으로 만든다.

1. `app.js`에 버튼 클릭 기능을 작성한다.
2. `git add app.js`로 stage한다.
3. 같은 파일 끝에 아직 commit하고 싶지 않은 주석 한 줄을 추가한다.
4. `git status`, `git diff`, `git diff --staged`를 비교한다.
5. 왜 같은 파일이 두 영역에 나타나는지 2문장으로 설명한다.
6. 주석을 직접 지우거나 별도 다음 commit으로 분리한다.

### 단계별 힌트

<details>
<summary>힌트 1 — 첫 commit에서 staged diff가 보이지 않는다</summary>

첫 commit 전에는 `HEAD`가 없지만 `git diff --staged`는 staged 새 파일을 보여 준다. 파일을 add했는지 `git status`로 확인한다.
</details>

<details>
<summary>힌트 2 — 모든 파일이 stage되었다</summary>

무조건 `git add .`를 반복하지 않는다. `git restore --staged <파일>`로 의도와 무관한 파일을 stage에서 내리고 작업 내용이 남았는지 확인한다.
</details>

<details>
<summary>힌트 3 — commit이 실패한다</summary>

오류의 첫 문장을 읽는다. identity 오류면 강의자에게 수업용 `user.name`/`user.email` 설정 범위를 확인하고, “nothing to commit”이면 `status`로 실제 변경과 stage를 확인한다.
</details>

### 최종 검증

```bash
git log --oneline --decorate -3
git status
```

- [ ] commit이 정확히 3개 이상 있다.
- [ ] 세 메시지가 서로 다른 변경 의도를 설명한다.
- [ ] 마지막 상태가 clean이다.
- [ ] 각 commit의 페이지가 실행 가능한 단위다.
- [ ] 비밀번호, 개인 토큰, 실제 개인정보가 없다.

### 5문장 회고 틀

1. working tree에는 ______ 상태의 내용이 있다.
2. staging area에는 ______ 내용이 있다.
3. commit은 ______을 확정한 기록이다.
4. `git diff`와 `git diff --staged`의 차이는 ______이다.
5. 다음에는 commit을 ______ 기준으로 나누겠다.

### 확장 문제

1. `git show HEAD~1`로 두 번째 commit의 변경과 메시지를 함께 읽는다.
2. `git log --oneline --reverse`로 사용자가 경험한 변화 순서를 설명한다.
3. 변경 일부만 stage하는 `git add -p`를 별도 연습 변경에서 사용하고 hunk 선택 결과를 확인한다.

## 제출 체크

- `observation.md`: 1일차 예상·실제·오류 진단표
- 개인 저장소: 의도별 commit 3개 이상
- `reflection.md`: Git 상태 5문장 회고
- 선택: 확장 문제 결과
