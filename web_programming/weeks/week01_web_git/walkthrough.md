# 1주차 따라하기 — 웹 실행 구조 관찰과 세 번의 커밋

이 문서는 1주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 30분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- Node.js LTS와 Git이 설치되어 있다. (`node --version`, `git --version`으로 확인)
- 최신 Chromium 계열 브라우저와 텍스트 편집기(VS Code 권장)를 사용한다.
- [`examples/`](examples/) 폴더를 개인 실습 폴더에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다.
- 터미널 명령은 복사한 폴더 안에서 실행한다. 현재 경로를 먼저 확인하는 습관을 들인다.

---

## 1일차 — 요청에서 화면까지 추적하기

### 단계 1. 로컬 서버 실행

**할 일**

1. 터미널에서 복사한 예제 폴더로 이동한다. (`server.mjs`가 보이는 위치)
2. 다음을 실행한다.

```powershell
node server.mjs
```

**예상 결과** — 터미널에 `Open http://localhost:8000/`이 출력되고 명령이 끝나지 않은 채 대기한다. 이 대기 상태가 서버가 켜져 있다는 뜻이다.

**확인** — [ ] 서버 종료(`Ctrl+C`)와 재시작을 한 번 해 보았다.

### 단계 2. 첫 화면으로 기준선 만들기

**할 일**

1. 브라우저에서 `http://localhost:8000/`을 연다.
2. 화면의 제목 문구와 상태 문구를 그대로 적는다.
3. 관찰 버튼을 두 번 누르고 상태 문구의 변화를 적는다.

**예상 결과** — 카드 한 장에 제목과 `클릭 횟수: 0`이 보이고, 두 번 클릭하면 `클릭 횟수: 2`가 된다.

**확인** — [ ] 새로고침하면 횟수가 다시 0으로 돌아오는 것을 확인했다. (메모리 상태는 페이지를 다시 읽으면 사라진다)

### 단계 3. Network — 한 화면은 세 번의 요청이다

**할 일**

1. DevTools를 연다. (`F12` 또는 `Ctrl+Shift+I` / `⌥⌘I`)
2. Network 탭에서 `Disable cache`를 켠다.
3. 새로고침하고 목록에서 document, stylesheet, script 요청을 각각 찾는다.
4. 각 행의 Request URL, Status, Type을 표로 기록한다.

**예상 결과** — `/`(document), `/styles.css`(stylesheet), `/app.js`(script)가 모두 status 200이다. 브라우저가 자동으로 요청하는 `/favicon.ico`의 404가 보일 수 있는데, 우리가 만든 오류가 아니다.

**확인** — [ ] URL의 scheme(`http`), host(`localhost`), port(`8000`), path(`/styles.css`)를 손으로 나누어 적었다.

### 단계 4. Elements와 Console — 구조·표현·동작 잇기

**할 일**

1. Elements 탭에서 `<main>`, `<button>`, `<output>`을 찾는다.
2. `<button>`을 선택하고 오른쪽 Styles에서 배경색을 정의한 규칙과 파일명을 확인한다.
3. Console 탭에서 준비 메시지를 확인한다.
4. 버튼을 누른 뒤 Elements에서 `<output>`의 텍스트가 바뀌는 것을 본다.

**예상 결과** — 버튼 스타일은 `styles.css`의 규칙이고, Console에는 `Web role demo ready`가 한 줄 있다. 소스 HTML 파일은 그대로인데 실행 중 DOM의 `<output>` 내용만 바뀐다.

**확인** — [ ] HTML=구조, CSS=표현, JavaScript=동작을 이 페이지의 실제 파일명으로 설명할 수 있다.

### 단계 5. 실패 하나만 재현하고 복구하기

**할 일**

1. 실행 전에 예측을 적는다: “CSS 파일 이름을 틀리게 쓰면 화면과 Network에 무엇이 보일까?”
2. 복사본 `index.html`에서 딱 한 곳만 바꾼다.

```html
<link rel="stylesheet" href="style.css">   <!-- 잠시 틀리게 바꾼다 (원래는 styles.css) -->
```

3. 새로고침하고 ① 눈에 보이는 증상 ② Network의 실패 요청과 status ③ Console의 첫 관련 메시지를 순서대로 기록한다.

**예상 결과** — 카드 모양이 사라지고 기본 브라우저 스타일로 보인다. Network에 `style.css` 404가 남고, Console에 404 로드 실패 메시지가 보인다. HTML과 JavaScript는 정상이므로 버튼 동작은 그대로다.

4. 바꾼 한 곳만 원래대로 되돌리고 새로고침해 404가 사라졌는지 확인한다.

**확인** — [ ] 원인을 확인하기 전에 여러 파일을 동시에 고치지 않았다.

### 단계 6. 404를 서버 응답으로 관찰하기

**할 일** — 페이지 하단의 `404 응답 관찰하기` 링크를 누르고, Network에서 `missing.html` 요청의 status와 Response(응답 본문)를 확인한다.

**예상 결과** — status 404, 본문은 서버가 보낸 짧은 안내 문장이다. “화면이 안 나온다”가 아니라 “서버가 404 응답을 보냈다”가 정확한 표현이다.

**확인** — [ ] `lab.md`의 1일차 관찰표를 채우고 제출 증거를 정리했다.

---

## 2일차 — 의미 있는 세 번의 커밋

1일차 폴더와 **별도의 새 폴더**에서 진행한다. 수업 자료 저장소 안에서 `git init`하지 않는다.

### 단계 1. 연습 저장소 만들기

**할 일**

```powershell
New-Item -ItemType Directory week01-practice
Set-Location week01-practice
git init
git branch -M main
git status
```

**예상 결과** — `On branch main`, `No commits yet`, `nothing to commit`이 보인다. identity 오류가 나면 강의자 안내에 따라 수업용 `user.name`/`user.email`을 설정한다(공유 PC에서 전역 설정을 임의로 바꾸지 않는다).

**확인** — [ ] `git status`의 세 줄을 자기 말로 읽었다.

### 단계 2. commit 1 — 페이지 구조와 제목

**할 일**

1. `index.html`을 만들고 최소 구조만 작성한다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>week01 연습 페이지</title>
  </head>
  <body>
    <h1>웹프로그래밍 연습</h1>
  </body>
</html>
```

2. 고정 순환을 그대로 실행한다.

```bash
git status
git diff
git add index.html
git diff --staged
git commit -m "Add course page structure"
```

**예상 결과** — 첫 commit 전 `git diff`는 비어 보이지만(추적 전 파일) `git diff --staged`는 add한 새 파일 전체를 보여 준다. commit 후 `git status`는 clean이다.

**확인** — [ ] commit 직전에 “staged diff에 이번 의도와 무관한 변경이 없는가”를 확인했다.

### 단계 3. commit 2 — 설명과 링크

**할 일** — `<h1>` 아래에 수업 설명 한 단락과 참고 링크 하나를 추가하고, 단계 2와 같은 순환으로 `Add course introduction`을 commit한다.

**예상 결과** — `git diff`에 추가한 줄만 `+`로 보인다. commit 후 `git log --oneline`에 두 줄이 쌓인다.

**확인** — [ ] 메시지만 읽어도 사용자에게 생긴 변화를 알 수 있다.

### 단계 4. commit 3 준비 — 같은 파일의 두 상태

**할 일**

1. `app.js`를 만들어 버튼 클릭 횟수 기능을 작성하고 `index.html`에 버튼·출력·`<script>`를 연결한다. (1일차 예제의 `app.js`를 참고하되 직접 타이핑한다)
2. `git add app.js index.html`로 stage한다.
3. **commit하기 전에** `app.js` 끝에 아직 commit하고 싶지 않은 주석 한 줄을 추가한다.
4. `git status`, `git diff`, `git diff --staged`를 나란히 비교한다.

**예상 결과** — `git status`에서 `app.js`가 *staged*와 *not staged* 두 영역에 동시에 나타난다. `git diff --staged`에는 기능 코드가, `git diff`에는 방금 추가한 주석 한 줄만 보인다. commit은 파일이 아니라 **stage된 스냅샷**을 기록하기 때문이다.

**확인** — [ ] 같은 파일이 두 영역에 나타나는 이유를 2문장으로 적었다.

### 단계 5. commit 3 — 동작 완성과 마무리

**할 일**

1. 주석 줄을 지우거나 별도 commit으로 분리하기로 결정한다.
2. `Count practice button clicks` 메시지로 commit한다.
3. 최종 검증을 실행한다.

```bash
git log --oneline --decorate -3
git status
```

**예상 결과** — 서로 다른 의도의 commit 3개가 보이고 마지막 상태는 clean이다. 각 commit 시점의 페이지는 그 자체로 실행 가능한 단위다.

**확인** — [ ] `lab.md`의 상태 회고 5문장을 작성했다. 비밀번호·개인정보가 파일에 없다.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| 서버가 시작되지 않는다 | 1일차 단계 1 (현재 폴더와 `node --version` 확인) |
| Network 목록이 비어 있다 | 1일차 단계 3 (DevTools를 연 채 새로고침, 필터 `All`) |
| 화면 모양이 이상하다 | 1일차 단계 5 (실패 요청의 URL과 실제 파일명 대조) |
| 버튼이 반응하지 않는다 | 1일차 단계 5 (JS 요청 status와 Console 첫 메시지) |
| commit이 실패한다 | 2일차 단계 1 (오류 첫 문장, identity 설정 확인) |
| 모든 파일이 stage되었다 | 2일차 단계 2 (`git restore --staged <파일>`로 내리기) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
