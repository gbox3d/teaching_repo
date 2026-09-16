# 9주차 실습 — README 1차판과 2분 발표

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

1일차에는 3~7주에 만든 `my-web`을 발표할 수 있는 상태로 정리하고, 저장소 `README.md` 1차판을 쓴다.
그 작업은 `readme` 브랜치에서 하고 main에 합친 뒤 브랜치를 양쪽에서 지운다. 2·3·6주에 한 브랜치 한 바퀴를 다시 도는 것이다.
2일차 60분이 **발표**다. 모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.

이번 주에는 `my-web`의 HTML·CSS·JavaScript를 고치지 않는다. 새로 만드는 것은 `README.md`와 `screenshots/` 폴더뿐이다.

## 1일차 — README 1차판과 브랜치 한 바퀴 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git` 뒤 `git switch -c readme` |
| 5–15분 | 세 페이지를 열어 nav·버튼·폼이 동작하는지 확인하고, 홈과 방명록 화면을 캡처해 `screenshots/`에 넣는다 |
| 15–35분 | `README.md` 1차판 5항목을 쓴다 |
| 35–45분 | `git add .` → `git commit` → `git push -u origin readme` → `git switch main` → `git merge readme` → `git push` → 저장소 첫 화면에서 README 확인 |
| 45–55분 | `git branch -d readme` → `git push origin --delete readme` → 짝과 2분 리허설 |
| 55–60분 | 끝 루틴: `git add .` → `git commit` → `git push` → 공개 주소 새로고침 → 저장소 첫 화면 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

### 1. 브랜치 만들기 (`git switch -c readme`)

받아온 뒤 오늘 작업할 브랜치를 만든다. [따라하기 1~2단계](walkthrough.md#1-저장소-받아오기)를 본다.

- 시작 전 `git status`가 `nothing to commit, working tree clean`이어야 한다. 아니면 먼저 commit한다.
- `Switched to a new branch 'readme'`가 보이고 `git branch`에 `* readme`가 있으면 된다.
- 8주차 `exam/` 폴더는 그대로 둔다. 이번 주에 보여 주는 것은 `my-web` 본체다.

### 2. 세 페이지 점검과 화면 캡처 (`screenshots/`)

세 페이지를 모두 열어 발표에 쓸 동작을 한 번씩 해 보고, 홈과 방명록 화면을 캡처한다.
[따라하기 3~5단계](walkthrough.md#3-홈-화면-세-파일-확인하기)를 본다.

| 확인할 것 | 어디서 |
|---|---|
| nav 링크 세 개가 서로 오간다 | 세 페이지 모두 |
| 버튼을 누르면 문장이 바뀌고 `클릭 N회`가 오른다 | `index.html` |
| 이름·메시지를 넣고 누르면 한 줄이 보인다 | `guestbook.html` |
| 이름을 비우고 누르면 안내가 보인다 | `guestbook.html` |

- 파일이 없거나 열리지 않으면 [따라하기 3~4단계](walkthrough.md#3-홈-화면-세-파일-확인하기)의 파일을 그대로 넣고 오늘 발표를 준비한다.
- 캡처는 **버튼을 누른 뒤**, **글을 남긴 뒤** 화면으로 찍는다. 눌러 본 것이 보여야 한다.
- 파일 이름은 `screenshots/home.png`·`screenshots/guestbook.png`로 한다. 한글 파일 이름은 링크에서 깨지기 쉽다.

### 3. README 1차판 5항목 (`#` · `-` · `[링크](https://주소)`)

저장소 루트에 `README.md`를 만들고 다섯 항목을 순서대로 쓴다. [따라하기 6단계](walkthrough.md#6-readme-1차판-쓰기)를 본다.

1. `# 제목` — 사이트 이름 한 줄
2. `## 공개 주소` — Pages 주소 링크
3. `## 페이지` — 세 페이지와 한 줄 설명
4. `## 기능` — 버튼과 폼, 두 줄
5. `## 화면` — 캡처 2장 링크 / `## 이번에 배운 것` — 3줄

- 마크다운은 세 가지만 쓴다. `#`(제목), `-`(목록), `[보이는 글](https://주소)`(링크).
- `#` 뒤에는 **띄어쓰기 한 칸**이 있어야 제목이 된다. `#제목`은 그냥 글자로 보인다.
- 실명·학번·전화번호·실제 이메일을 쓰지 않는다. 예시는 `student01@example.com`이다.

### 4. 브랜치 합치고 지우기 (`merge` · `branch -d` · `push origin --delete`)

`readme`를 push한 뒤 main으로 돌아가 합치고, 브랜치를 내 PC와 GitHub에서 각각 지운다.
[따라하기 7~9단계](walkthrough.md#7-commit하고-readme-브랜치-push-하기)를 본다.

- **push를 먼저 한 뒤 반드시 merge까지 한다.** push한 브랜치를 merge 전에 `git branch -d`로 지우면 error가 아니라 경고만 내고 그대로 지워진다(아래 「막혔을 때」의 `warning: deleting branch …` 행). `error: the branch 'readme' is not fully merged`는 push도 merge도 하지 않은 브랜치에서만 뜬다.
- `git switch main` 직후 `screenshots/`가 사라지고 `README.md`는 7주차에 만든 8줄판으로 돌아간다. 정상이다. merge하면 1차판이 돌아온다.
- merge 출력에 `Fast-forward`와 `README.md`·`screenshots/…`가 보이면 맞다.
- `git branch -d`는 내 PC, `git push origin --delete`는 GitHub다. 한쪽만 하면 다른 쪽에 이름이 남는다.

### 5. 저장소 첫 화면 확인과 2분 리허설

`https://github.com/<아이디>/my-web`을 새로고침해 README가 첫 화면 아래에 보이는지 본다.

- 캡처 두 장이 **글자 링크가 아니라 그림으로** 보여도 되고, 링크로 보여도 된다. 눌러서 열리면 통과다.
- 링크를 눌렀는데 `404`면 `screenshots/` 폴더가 push되지 않았거나 파일 이름 대소문자가 다른 것이다.
- 짝과 번갈아 2분을 재며 한 번씩 해 본다. 2분을 넘기면 어디를 줄일지 정한다.

### 6. 오늘 확인할 것

- [ ] `git branch`에 `* main`만 남아 있다.
- [ ] GitHub 브랜치 목록에도 `readme`가 없다.
- [ ] 저장소 첫 화면에 README 5항목이 보이고 캡처 2장이 열린다.
- [ ] 공개 주소에서 세 페이지·버튼·폼이 모두 동작한다.
- [ ] 저장소 첫 화면을 캡처 1장으로 저장했다.

## 2일차 — 2분 발표 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 발표 차례를 확인하고 탭 세 개(공개 주소·저장소 첫 화면·Commits 탭)를 연다. 같은 PC면 `git pull` |
| 5–47분 | **발표 2분 × 인원** — 공개 주소 → 세 페이지 → 버튼·폼 → Commits 탭 |
| 47–55분 | 총평과 10주차 예고 |
| 55–60분 | 끝 루틴: README를 고쳤으면 `git add .` → `git commit` → `git push`, 공용 PC면 자격 증명 삭제 |

21명 기준으로 발표에 42분이 든다. 인원에 따라 달라지며 **실제 차례와 시각은 수업 공지를 따른다.**

### 1. 발표 순서 (2분)

[따라하기 12단계](walkthrough.md#12-2분-시연-순서대로-해-보기)를 본다.

| 시간 | 보여 줄 것 | 말할 것 |
|---|---|---|
| 0:00 | 공개 주소를 연다 | 사이트 이름과 한 줄 소개 |
| 0:20 | nav로 세 페이지 | 어떤 페이지가 있는지 |
| 0:50 | 홈의 버튼을 누른다 | 무엇이 바뀌는지 |
| 1:10 | 방명록에 한 줄 남긴다 | 폼이 하는 일 |
| 1:30 | 이름을 비우고 누른다 | 빈값 안내 |
| 1:40 | Commits 탭과 README | 몇 번에 걸쳐 만들었는지 |

- 말하면서 누른다. 누르고 나서 설명하면 2분을 넘긴다.
- 코드 파일은 띄우지 않는다. 구술 질문을 받으면 그때 연다.
- 잘 안 되는 기능이 있으면 **되는 것부터** 보여 주고 남은 시간에 말한다.

### 2. 듣는 동안

- 채점표를 보며 듣는다. 다음 차례 두 사람은 탭 세 개를 미리 열어 둔다.
- 남의 발표 중에 자기 코드를 고치지 않는다. 수정은 55–60분 끝 루틴에서 한다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다. 다음 수업 시작 5분에 다시 확인해도 된다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| `fatal: The current branch readme has no upstream branch.` | 처음 올리는 브랜치에 `git push`만 쳤다. git이 바로 아래 줄에 `git push --set-upstream origin readme`를 알려 준다. 수업에서는 같은 뜻인 `git push -u origin readme`를 쓴다 |
| `error: the branch 'readme' is not fully merged` | push도 merge도 하지 않은 브랜치를 지우려 했다. `git push -u origin readme` → `git switch main` → `git merge readme` → `git push`를 먼저 한다. `-D`는 쓰지 않는다 |
| `error: cannot delete branch 'readme' used by worktree at '…/my-web'` | 지금 그 브랜치에 있다. `git switch main`을 먼저 한다 |
| `warning: deleting branch 'readme' that has been merged to 'refs/remotes/origin/readme', but not yet merged to HEAD` | push는 했고 merge는 안 한 채 지웠다. 위 error 대신 이것이 나오며 **경고만 내고 지워진다.** 이어서 `git merge readme`를 치면 `merge: readme - not something we can merge`가 난다. `git branch readme origin/readme`로 되살린 뒤 merge한다 |
| `error: unable to delete 'readme': remote ref does not exist` | GitHub 쪽 브랜치를 이미 지웠다. 브랜치 목록에 `readme`가 없으면 끝난 것이다 |
| `fatal: a branch named 'readme' already exists` | 이미 만든 브랜치다. `git switch readme`로 옮겨 간다 |
| `Already up to date.` | main이 아니라 `readme`에서 merge했다. `git branch`로 `*` 위치를 보고 `git switch main` |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| 저장소 첫 화면에 README가 안 보인다 | 파일이 저장소 **맨 위**에 있고 이름이 `README.md`인지 본다. 이름이 `README.md`여야 제목·목록·링크가 렌더된다. 폴더 안의 파일은 첫 화면에 보이지 않는다 |
| README의 캡처 링크가 404 | `screenshots/` 폴더가 push되지 않았거나 파일 이름의 대소문자가 다르다. GitHub에서 폴더를 열어 파일 이름을 그대로 복사해 링크에 넣는다 |
| README의 `#제목`이 그냥 글자로 보인다 | `#` 뒤에 띄어쓰기가 없다. `# 제목`으로 고친다 |
| 방명록에 남긴 글이 새로고침하면 사라진다 | 정상이다. 오늘 글은 화면에만 있다. 새로고침해도 남게 하는 것은 11주차다 |

한 번에 한 곳만 고치고 다시 확인한다. 해결되지 않으면 터미널이나 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장과 발표

**캡처 1장**: `https://github.com/<아이디>/my-web` 저장소 첫 화면. README 5항목과 캡처 2장이 함께 보이게 찍는다.

발표는 2일차 수업 시간에 한다. 채점 기준은 [채점표](rubric.md), 과제 범위는 [1차 과제 안내](project_brief.md)에 있다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- README에 `## 만든 순서` 항목을 더해 `git log --oneline`에서 commit 메시지 세 줄을 옮겨 적어 본다.
- `contact` 브랜치를 만들어 README에 한 줄을 더하고 같은 순서(`switch -c` → commit → `push -u` → `switch main` → `merge` → `push` → `branch -d` → `push origin --delete`)를 한 번 더 돌아 본다.
- 방명록에 남길 문장을 미리 정해 두고 발표용으로 20자 이내로 줄여 본다.
- 캡처를 1280px 폭으로 다시 찍어 README에서 글씨가 읽히는지 본다.

추가 과제는 선택 사항이며 채점하지 않는다.
