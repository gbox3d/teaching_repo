# 15주차 실습 — 기말 실기 리허설과 본시험

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

1일차는 시험과 **같은 형태의 리허설**이다. 점수에 들어가지 않는다. 2일차가 본시험 60분이다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.
**완료 확인·캡처는 공개 주소에서만 한다.** `localStorage`와 `fetch`는 `file://`로 열면 결과가 다르다(11·12주차와 같다).
작업 중 미리 보기가 필요하면 VS Code 확장 **Live Server**(**Go Live** → `http://127.0.0.1:5500/`)를 쓰고,
설치가 막히면 터미널에서 `python3 -m http.server 8000`을 쓴다. 둘 다 없으면 **한 번에 한 가지만 고쳐 push**하고 공개 주소에서 본다.

## 1일차 — 리허설과 시험용 저장소 준비 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | GitHub에서 저장소 `web-final`(Public, README 끄기)을 만들고 `git clone https://github.com/<아이디>/web-final.git` → **File › Open Folder** |
| 5–15분 | starter 네 파일을 넣고 `git add .` → `git commit` → `git push -u origin main` → **Settings › Pages**(`main` · `/(root)`) |
| 15–28분 | TODO 1 — 폼 제출로 한 권 추가하고 빈값이면 안내 |
| 28–38분 | TODO 2 — 항목마다 [지우기] 버튼 |
| 38–46분 | TODO 3 — `final-items` 키로 저장·복원(미리 보기로 확인하고, 최종 확인은 끝 루틴 push 뒤 공개 주소에서) |
| 46–55분 | TODO 4 — `data/items.json` 불러오기와 오류 안내(미리 보기로 확인하고, 최종 확인은 끝 루틴 push 뒤 공개 주소에서) |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 확인용 캡처 → 공용 PC면 자격 증명 삭제 |

### 1. 시험용 저장소와 Pages (`git clone` · **Settings › Pages**)

`my-web`은 그대로 두고 새 저장소 `web-final`을 만든다. [따라하기 1~3단계](walkthrough.md#1-시험용-저장소-web-final-만들기)를 본다.

- 저장소는 **Public**, **Add a README file**은 체크하지 않는다. 2주차와 같은 절차다.
- clone 직후 `warning: You appear to have cloned an empty repository.`가 나오면 맞게 된 것이다. README를 체크해 버렸다면 이 줄이 나오지 않지만 그대로 이어서 하면 된다.
- 집에서 미리 만들어 왔다면 clone 대신 그 폴더에서 `git pull`을 한다.
- **오늘 안에 공개 주소가 열려야 한다.** 시험 당일에는 저장소도 Pages도 만들지 않는다.

### 2. TODO 1 — 폼 제출 (`submit` · `value` · `trim`)

`app.js`의 submit 리스너 안을 채운다. [따라하기 4단계](walkthrough.md#4-todo-1--폼으로-한-권-추가하기)를 본다.

- 순서는 7주차와 같다. 값 읽기 → 빈값이면 안내하고 `return` → 아니면 배열에 넣고 `showList()`.
- 목록 한 줄은 `제목 (날짜)` 모양이다. 날짜는 `new Date().toLocaleDateString()` 틀 한 줄이다(11주차).
- 빈 칸으로 눌렀을 때 빨간 글씨가 나오고, 다시 제대로 넣으면 그 글씨가 사라져야 한다.

### 3. TODO 2 — 지우기 버튼 (`createElement` · `splice`)

목록의 줄마다 버튼을 붙인다. [따라하기 5단계](walkthrough.md#5-todo-2--지우기-버튼-붙이기)를 본다.

- 10주차에 쓴 틀과 같다. `createElement('button')` → `textContent` → click 안에서 `splice(i, 1)` → `showList()`.
- `showList()`가 다시 그릴 때 버튼마다 번호를 새로 붙인다. 가운데 줄을 지워도 번호가 밀리지 않는다.
- 눌렀는데 목록이 그대로면 `splice` 뒤에 `showList()`를 부르지 않은 것이다.

### 4. TODO 3 — 저장과 복원 (`localStorage` · `JSON`)

두 줄이 짝이다. [따라하기 6단계](walkthrough.md#6-todo-3--localstorage로-남기기)를 본다.

- 저장은 `setItem('final-items', JSON.stringify(books))`, 복원은 `JSON.parse(localStorage.getItem('final-items')) || []`.
- 키 이름은 `final-items`다. `my-web`의 `guestbook`과 달라야 두 페이지의 목록이 섞이지 않는다.
- **확인은 공개 주소에서 한다.** `file://`에서 넣은 항목은 공개 페이지에 나타나지 않는다.
- DevTools **Application › Local Storage**에서 키와 값이 보이는지 함께 본다.

### 5. TODO 4 — 불러오기 (`fetch` · `response.ok` · `try / catch`)

`loadRecommend()` 안을 채운다. [따라하기 7단계](walkthrough.md#7-todo-4--추천-목록-불러오기)를 본다.

- 경로는 `'data/items.json'`처럼 **상대 경로**로 쓴다. `/`로 시작하면 공개 주소에서 404가 난다.
- 성공하면 `추천 3권`과 세 줄이 보이고, 실패하면 `불러오지 못했습니다.`가 보인다.
- 실패 화면을 꼭 한 번 만들어 본다. 파일 이름을 잠깐 `item.json`으로 바꿨다가 되돌린다.
- `file://`로 열면 항상 실패한다. 오류가 아니라 브라우저 규칙이다. 미리 보기 서버(**Go Live**·`python3 -m http.server 8000`)나 공개 주소에서는 나온다.

### 6. 오늘 확인할 것

- [ ] 공개 주소 `https://<아이디>.github.io/web-final/`이 열린다.
- [ ] 제목을 넣고 **추가** → 한 줄이 생기고, 빈 칸으로 누르면 안내 문구가 나온다.
- [ ] **지우기**로 그 줄만 사라진다.
- [ ] 공개 주소에서 새로고침해도 목록이 남아 있다.
- [ ] 추천 목록 3권이 보이고, 파일 이름을 틀리면 `불러오지 못했습니다.`가 보인다.
- [ ] Console에 빨간 줄이 없다.

1일차 캡처는 확인용이며 제출하지 않는다. 제출은 2일차에 한 번만 한다.

## 2일차 — 본시험 구현과 제출 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 폴더가 없으면 `git clone https://github.com/<아이디>/web-final.git` → **File › Open Folder** → 시험 파일 네 개를 덮어쓰고 `git status`와 브라우저로 실행 확인 |
| 5–15분 | HTML·CSS 문항 |
| 15–35분 | 폼·목록 추가·삭제 문항 |
| 35–45분 | localStorage 문항 |
| 45–52분 | fetch·오류 안내 문항 |
| 52–57분 | `git add .` → `git commit` → `git push` → `git log -1 --format=%H` → 공개 주소 확인·캡처 |
| 57–60분 | 예비: Pages 반영 대기와 제출 확인 |

### 1. 시작 전 3분

시험 파일을 덮어쓰고 **구현을 시작하기 전에** 실행을 확인한다. [따라하기 9단계](walkthrough.md#9-본시험-시작-전-3분)를 본다.

- 폴더가 남아 있는 PC면 `git pull`, 폴더가 없으면 `git clone https://github.com/<아이디>/web-final.git`으로 먼저 받는다. 저장소와 Pages는 어제 그대로 살아 있다.
- `git status`에 바뀐 파일이 `modified:`로 보이는지 본다. 네 파일 중 몇 개가 보이면 정상이다.
- `index.html`을 브라우저로 한 번 열어 화면이 뜨고 Console 오류가 0인지 본다.
- 여기서 오류가 나면 손을 든다. 시간은 기록되며 손해가 없다.
- 어제 리허설 commit은 저장소에 남아 있다. 덮어써도 사라지지 않는다.

### 2. 문항 푸는 순서

- 문항을 끝까지 읽고 어느 TODO 자리를 고치는지 먼저 표시한다.
- 한 문항에서 10분 넘게 막히면 다음 문항으로 넘어간다. 문항끼리 서로 막지 않는다.
- **한 번에 한 곳만 고치고** 브라우저에서 확인한다. 여러 곳을 동시에 고치면 원인을 찾을 수 없다.
- 중간에 한 번 `git add .` → `git commit`을 해 두면 마지막에 몰리지 않는다.

### 3. 제출 (공개 주소 · 저장소 주소 · commit 번호)

[따라하기 11단계](walkthrough.md#11-마지막-5분--push와-제출-세-가지)를 본다.

1. 공개 주소 `https://<아이디>.github.io/web-final/`
2. 저장소 주소 `https://github.com/<아이디>/web-final`
3. 마지막 commit 번호 — `git log -1 --format=%H`의 40자

- **저장하고 push해서 공개 주소에 보이는 것이 제출본이다.** VS Code 화면이 아니다.
- 캡처 1장(주소창이 보이게)을 함께 낸다.
- 채점 기준은 [채점표](rubric.md)에 있다.

### 4. 시험 중 규칙

- 허용: 교재 사이트, 본인 저장소(`my-web`), MDN. 검색·AI 도구의 범위는 수업 공지를 따른다.
- 금지: 다른 학생의 코드, 메신저, 남의 저장소 답안.
- 장애는 혼자 해결하지 않는다. 손을 들면 시각이 기록된다.
- 다 못 했어도 **코드를 지우고 내지 않는다.** 시도 흔적은 점수로 인정된다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. `git status`에 `Your branch is ahead of 'origin/main' by 1 commit.`이 있으면 push를 안 한 것이다 |
| `warning: You appear to have cloned an empty repository.` | 정상이다. 빈 저장소를 받았다는 뜻이며 이어서 파일을 넣고 commit한다 |
| `fatal: destination path 'web-final' already exists and is not an empty directory.` | 그 자리에 이미 폴더가 있다. clone 대신 그 폴더를 열고 `git pull`을 한다 |
| 2일차인데 `web-final` 폴더가 없거나 `git status`가 `fatal: not a git repository (or any of the parent directories): .git`으로 끝난다 | 어제 만든 저장소는 GitHub에 그대로 있다. `git clone https://github.com/<아이디>/web-final.git`으로 다시 받아 **File › Open Folder**로 열고, 그 폴더에 시험 파일을 덮어쓴다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| `file://`로 열었더니 추천 목록이 늘 `불러오지 못했습니다.`이고 Console에 `Access to fetch at 'file:///…/data/items.json' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app.` | 오류가 아니라 브라우저 규칙이다. `file://`에서는 파일을 불러올 수 없다. 공개 주소에서 확인한다 |
| Live Server 확장이 설치되지 않는다 | 터미널에서 `python3 -m http.server 8000`을 실행하고 `http://127.0.0.1:8000/`을 연다. 둘 다 막히면 한 번에 한 가지만 고쳐 push하고 공개 주소에서 확인한다 |
| `file://`에서 넣은 목록이 공개 주소에 없다 | 로컬과 공개 주소는 브라우저 저장소가 서로 다르다. 공개 주소에서 다시 넣어 확인하고 캡처한다 |
| 새로고침하면 목록이 사라진다 | `saveList()`를 부르지 않았거나 복원 줄(`JSON.parse(...) || []`)을 넣지 않았다. 두 줄이 짝이다 |
| **지우기**를 눌렀는데 새로고침하면 되살아난다 | `splice` 뒤에 `saveList()`가 없다. 화면만 바꾸고 저장하지 않았다 |
| `Uncaught SyntaxError: Expected property name or '}' in JSON at position 1 (line 1 column 2)` | 저장해 둔 값이 JSON이 아니다. DevTools **Application › Local Storage**에서 `final-items`를 지우고 새로고침한다 |
| 공개 주소인데도 추천 목록이 `불러오지 못했습니다.`로 뜬다 | 파일 이름과 폴더 이름을 본다. `data/items.json`이 저장소에 push되어 있는지 GitHub 화면에서 확인한다. 이름이 하나라도 다르면 서버가 404로 답한다 |
| 내 PC에서는 추천 목록이 나오는데 공개 주소에서만 `불러오지 못했습니다.` | 경로를 `/data/items.json`처럼 `/`로 시작하게 썼다. 공개 주소에는 저장소 이름이 앞에 붙어 그 자리에 파일이 없다. `'data/items.json'`으로 고친다 |
| 추천 목록만 `불러오지 못했습니다.`인데 Console에는 빨간 줄이 없다 | `data/items.json`의 따옴표·쉼표가 틀려 읽다가 멈춘 것이다. `try / catch`가 잡아 주기 때문에 빨간 줄이 안 보인다. **Network** 탭에서 `items.json`을 열어 큰따옴표를 본다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'innerHTML')` | `document.querySelector`가 그 자리를 못 찾았다. 오류 줄의 `app.js:줄번호`를 열어 그 줄의 `id`를 `index.html`과 대조한다(대소문자까지) |
| 추천 목록이 `불러오는 중…`에서 멈춰 있다 | `loadRecommend()` 안이 비어 있거나 `loadStatus`에 아무것도 쓰지 않았다. Console과 **Network** 탭을 함께 본다 |

한 번에 한 곳만 고치고 다시 확인한다. 해결되지 않으면 화면을 그대로 보여 주고 감독에게 말한다.

## 제출 — 캡처 한 장

`https://<아이디>.github.io/web-final/`을 열고 **주소창이 함께 보이게** 화면을 캡처한다.

- 목록에 내가 넣은 줄이 보이고 **지우기** 버튼이 붙어 있다.
- 추천 목록이 보이거나, 실패했다면 `불러오지 못했습니다.` 안내가 보인다.

캡처와 함께 공개 주소·저장소 주소·마지막 commit 번호 세 가지를 낸다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

1일차 리허설을 일찍 끝냈을 때만 한다. 채점하지 않는다.

- 목록 위에 `${books.length}권`을 표시해 본다(10주차 항목 수).
- **[전체 지우기]** 버튼을 만들어 `books = []` → `showList()` → `saveList()`를 해 본다.
- `styles.css`의 색을 바꿔 push하고 공개 주소가 따라 바뀌는지 본다.
- 375px 기기 모드에서 폼이 세로로 접히는지 확인한다.

## 확장 대신 할 일

2일차 본시험에서 일찍 끝났을 때 하는 것이다. 새 기능을 더 만들지 않는다.

- 공개 주소를 **새 시크릿 창**으로 열어 처음 보는 사람의 화면에서도 동작하는지 본다.
- 문항을 다시 읽고 빠뜨린 조건(안내 문구, 키 이름, 파일 이름)이 없는지 대조한다.
- Console을 열어 빨간 줄이 0인지 확인한다.
- `git log --oneline`으로 오늘 commit이 올라갔는지 보고, 제출한 commit 번호와 같은지 대조한다.
