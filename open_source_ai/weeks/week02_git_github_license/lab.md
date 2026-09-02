# 2주차 실습 — 제안하고, 합치고, 조건을 읽어라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 토큰·비밀번호를 명령이나 파일에 적지 않는다. GitHub 인증은 브라우저 로그인 또는 강의자가 정한 credential manager로 한다.
- `git push --force`, `git reset --hard`처럼 기록을 지우는 명령은 이번 주에 쓰지 않는다. 막히면 힌트를 읽고, 그래도 안 되면 강의자를 부른다.

## 1교시 실습 — 원격 연결과 충돌 1회 해결

### 상황

1주차에 만든 개인 연습 저장소는 아직 내 PC에만 있다. 팀 동료가 "GitHub에 올려 두면 README를 보고 제안하겠다"고 했다. 저장소를 GitHub에 올리고, 두 branch가 README의 같은 줄을 다르게 고쳤을 때 무슨 일이 생기는지 한 번 재현해 해결하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | GitHub 빈 저장소 생성, 예상표 작성 |
| 원격 연결 | 5–12분 | `remote add`, 첫 `push -u`, 추적 상태 확인 |
| 충돌 재현 | 12–20분 | `feature/readme`와 `main`에서 같은 줄 수정, merge |
| 충돌 해결 | 20–25분 | 마커 읽기, 결과 문장 작성, merge commit, push |
| 검증·기록 | 25–30분 | graph 출력, 상태 문장 기록 |

### 준비

이어받는 것: 1주차 3교시에서 `git init`하고 첫 commit을 만든 개인 연습 저장소. 1주차 실습지의 예시 경로는 `C:\classwork\osa-week01`이다. 폴더 이름은 각자 달라도 되며, 이번 주부터 문서는 이 저장소를 `osa-practice`라고 부른다(3주차 문서의 예시 경로는 `C:\classwork\osa-practice`). 이름을 맞추고 싶으면 PowerShell 창을 닫은 뒤 폴더 이름만 바꾼다. 폴더 이름을 바꿔도 Git 이력은 그대로다. 그 폴더로 이동해 상태를 확인한다.

```powershell
Set-Location <1주차 개인 연습 저장소 폴더>
git status
git log --oneline -3
```

저장소가 없거나 다른 PC라면 새로 만든다. 수업 자료 저장소 안에서 `git init`하지 않는다.

```powershell
Set-Location C:\classwork
New-Item -ItemType Directory osa-practice
Set-Location osa-practice
git init
git branch -M main
```

`README.md`가 없으면 VS Code에서 다음 두 줄로 만들고 commit한다. PowerShell의 `Out-File`은 인코딩 문제가 생길 수 있으므로 편집기로 만든다.

```text
# osa-practice
이 저장소는 실습용이다.
```

```powershell
git add README.md
git commit -m "Add README"
```

Git이 사용자 이름·이메일을 요구하면 강의자 안내에 따라 수업용 설정을 쓴다. 공유 PC에서는 전역 설정을 바꾸지 않고 저장소 안에서만 유효한 `git config user.name`, `git config user.email`을 쓴다.

### 문제 1 · 원격 연결과 첫 push

1. 실행 전에 예상표를 적는다.

| 관찰 대상 | 예상 | 실제 |
|---|---|---|
| `git remote -v` 출력 줄 수 |  |  |
| 첫 push 뒤 `git branch -vv`의 `main` 줄 |  |  |
| GitHub 저장소 페이지의 commit 수 |  |  |
| 같은 줄을 다르게 고친 두 branch를 merge한 결과 |  |  |

2. GitHub에서 빈 공개 저장소를 만든다. 이름은 `osa-practice`를 권장한다. README·`.gitignore`·license를 **추가하지 않는다**. 로컬에 이미 commit이 있기 때문이다.
3. 저장소 페이지에 표시되는 HTTPS URL로 원격을 연결하고 push한다. `<…>`는 그대로 입력하는 문자가 아니라 본인 값으로 바꾼다.

```powershell
git remote add origin <본인 저장소 HTTPS URL>
git remote -v
git push -u origin main
git branch -vv
```

4. 브라우저에서 저장소 페이지를 새로고침해 README와 commit 수를 확인한다.
5. 로컬에서 `git fetch origin`을 실행하고 작업 파일이 바뀌지 않는 것을 확인한다.

완료 조건:

- [ ] `git remote -v`에 fetch·push 두 줄이 같은 URL로 보인다.
- [ ] `git branch -vv`에서 `main`이 `[origin/main]`을 추적하고 `ahead`·`behind` 표시가 없다.
- [ ] GitHub 페이지의 최신 commit 메시지가 로컬 `git log -1`과 같다.

### 문제 2 · 같은 줄 충돌 재현과 해결

1. branch를 만들어 이동하고 `README.md` 2번째 줄을 바꾼 뒤 commit한다.

```powershell
git switch -c feature/readme
```

`README.md` 2번째 줄을 다음으로 바꾼다.

```text
이 저장소는 로컬 AI 도우미 프로젝트의 시작점이다.
```

```powershell
git add README.md
git commit -m "Describe repository purpose"
```

2. `main`으로 돌아가 **같은 줄**을 다르게 바꾸고 commit한다.

```powershell
git switch main
```

`README.md` 2번째 줄을 다음으로 바꾼다.

```text
이 저장소는 오픈소스 AI 응용 수업의 실습 기록이다.
```

```powershell
git add README.md
git commit -m "State repository scope"
```

3. merge 전에 `git log --graph --oneline --all`로 두 갈래를 확인하고, merge 결과를 예상표에 적는다.
4. merge한다. 충돌 메시지가 나오면 `git status`로 충돌 파일을 확인한다.

```powershell
git merge feature/readme
git status
```

5. `README.md`를 열어 `<<<<<<<`, `=======`, `>>>>>>>` 사이의 두 문장을 읽는다. 마커 3줄을 모두 지우고 2번째 줄을 두 의도를 합친 한 문장으로 쓴다.

```text
이 저장소는 오픈소스 AI 응용 수업의 실습 기록이며 로컬 AI 도우미 프로젝트의 시작점이다.
```

6. 해결을 확정하고 push한다. commit 메시지는 Git이 제안하는 기본 문구를 그대로 써도 된다.

```powershell
git add README.md
git commit
git log --graph --oneline --all
git push
```

`git commit`만 실행하면 편집기가 열린다. 저장하고 닫으면 commit이 완료된다. 편집기가 낯설면 `git commit -m "Merge branch 'feature/readme'"`로 대신한다.

완료 조건:

- [ ] merge 직후 `git status`에 `both modified: README.md`가 보였다.
- [ ] 결과 `README.md`에 마커가 없고 2번째 줄이 두 의도를 모두 담는다.
- [ ] graph에 `feature/readme` 갈래와 부모가 둘인 merge commit이 보이고 `origin/main`이 그 commit을 가리킨다.

### 단계별 힌트

<details>
<summary>힌트 1 — push가 rejected다, 또는 인증 창이 계속 뜬다</summary>

rejected는 원격에 로컬이 모르는 commit이 있다는 뜻이다. 저장소를 만들 때 README나 license를 추가했으면 그렇게 된다. `git fetch origin` 뒤 `git log --oneline --all`로 원격 commit을 확인하고, 강제 push 대신 `git pull --no-rebase origin main`으로 합친다. "unrelated histories" 오류가 나면 같은 명령에 `--allow-unrelated-histories`를 붙인다. 인증 창이 반복되면 credential manager 설정을 강의자에게 확인한다. 토큰을 URL에 넣지 않는다.
</details>

<details>
<summary>힌트 2 — merge했는데 충돌이 나지 않고 그냥 합쳐졌다</summary>

`git log --graph --oneline --all`에서 두 갈래가 보이는지 확인한다. `feature/readme`에서 commit한 뒤 `git switch main`을 하지 않고 같은 branch에서 두 번째 수정을 했으면 갈래가 하나뿐이어서 fast-forward가 된다. 또는 두 branch가 서로 다른 줄을 고쳤을 수도 있다. 같은 줄 번호를 고쳤는지 `git diff main feature/readme`로 확인한다.
</details>

<details>
<summary>힌트 3 — 충돌 상태에서 빠져나오고 싶다</summary>

`git merge --abort`를 실행하면 merge를 시작하기 전 상태로 돌아간다. 마커를 지우다 실수했어도 abort 뒤 다시 `git merge feature/readme`를 하면 된다. abort는 commit을 지우지 않는다.
</details>

### 검증

- 정상: `git log --graph --oneline --all`에 `main`과 `feature/readme`가 갈라졌다가 merge commit에서 합쳐지고, `origin/main`과 `main`이 같은 commit에 있다.
- 경계 또는 실패: `git merge --abort`를 한 번 실행해 merge 전 상태로 돌아가는 것을 확인한 뒤 다시 merge한다. 그리고 권한이 없는 URL(예: 짝의 저장소)로 `git push`를 한 번 시도해 거부 메시지를 읽는다.
- 설명: "충돌은 오류가 아니라 ______를 요청하는 상태다"의 빈칸을 채워 한 문장으로 적는다.

### 확장 문제

1. 다른 줄만 고친 branch `feature/title`을 만들어 merge하고, 충돌 없이 합쳐진 이유를 graph와 함께 설명한다.
2. 짝이 GitHub 웹에서 내 README를 한 줄 고쳐 commit해 주면(짝이 collaborator가 아니면 2교시 뒤에 한다) `git fetch origin` 뒤 `git log --oneline main..origin/main`으로 원격에만 있는 commit을 확인하고 `git pull`로 가져온다.
3. `examples/merge_conflict_demo.ps1`을 별도 연습 폴더에서 실행해 같은 충돌을 스크립트로 재현하고, 실습에서 손으로 한 순서와 단계별로 대응시킨다.

## 2교시 실습 — 짝 저장소에 제안하고 리뷰 받기

### 상황

짝(`student02`)의 저장소 README에는 기여 방법이 없다. 쓰기 권한이 없으므로 직접 push할 수 없다. Issue로 제안하고, fork에서 branch를 만들어 PR을 보내고, 짝의 리뷰를 받아 수정한 뒤 merge까지 가라. 동시에 짝이 내 저장소에 보내는 PR을 리뷰한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 짝 정하기, 템플릿 설치·push, 저장소 URL 교환 |
| Issue·Fork | 4–10분 | 짝 저장소에 Issue 등록, fork, fork clone |
| 브랜치·PR | 10–17분 | branch, README 수정, push, 템플릿 채운 PR |
| 리뷰·수정 | 17–25분 | 짝 PR에 코멘트·수정 요청, 내 PR 수정 push, merge |
| 검증·기록 | 25–30분 | URL 2개 기록, 상태 문장 |

### 준비

이어받는 것: 1교시에서 GitHub에 push한 개인 저장소(`osa-practice`)와 짝의 저장소 URL.

저장소 주인으로서 먼저 템플릿을 설치한다. 개인 저장소 폴더에서 실행한다. `<수업자료>`는 수업 자료 저장소를 clone한 위치다.

```powershell
git status
Copy-Item -Recurse <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\pr_template\.github .\.github
git add .github
git commit -m "Add issue and PR templates"
git push
```

짝과 저장소 URL을 교환하고, 두 사람이 모두 push를 마친 뒤 시작한다. 이후 단계는 두 사람이 **동시에** 진행한다. 한쪽이 기다리게 되면 상대의 PR을 리뷰한다.

### 문제 1 · Issue → Fork → 브랜치 → PR (제안자 역할)

1. 실행 전에 예상을 적는다. fork한 저장소의 URL에는 누구의 계정 이름이 들어가는가? PR을 열면 base와 compare에 각각 무엇이 보이겠는가?
2. 브라우저에서 **짝 저장소**의 Issues → New issue → "제안(proposal)" 템플릿을 고른다. 제목 `[제안] README에 기여 방법 절 추가`, 본문의 현재 상황·제안·기대 효과를 채워 등록한다. Issue 번호를 적어 둔다.
3. 짝 저장소 페이지 오른쪽 위 Fork → 본인 계정에 fork를 만든다.
4. **개인 저장소 폴더 밖의 별도 위치**에서 fork를 clone하고 branch를 만든다.

```powershell
git clone <본인 fork의 HTTPS URL> partner-practice
Set-Location partner-practice
git switch -c feature/contributing
```

5. `README.md` 끝에 다음 절을 추가하고 commit·push한다.

```text
## 기여 방법

1. 변경을 제안하려면 Issue를 먼저 연다.
2. fork에서 `feature/<주제>` branch를 만든다.
3. PR 템플릿을 채워 보낸다.
```

```powershell
git add README.md
git commit -m "Add contributing section to README"
git push -u origin feature/contributing
```

6. 브라우저에서 fork 페이지의 Compare & pull request를 누른다. base repository가 **짝 저장소의 `main`**, head가 **본인 fork의 `feature/contributing`**인지 확인한다. 본문에 자동으로 들어온 PR 템플릿을 채운다. 관련 Issue 칸은 `Closes #번호`로 쓴다. Create pull request를 누른다. Draft로 열었다면 Ready for review로 바꾼다.

완료 조건:

- [ ] 짝 저장소에 내 Issue가 열려 있고 번호를 기록했다.
- [ ] PR 페이지 상단에 "wants to merge 1 commit into (짝 계정):main from (내 계정):feature/contributing" 형태의 문장이 보인다.
- [ ] PR 본문의 템플릿 항목이 모두 채워져 있고 `Closes #번호`가 Issue에 연결되어 있다.

### 문제 2 · 리뷰 → 수정 → merge (리뷰어·관리자 역할)

1. 짝이 **내 저장소**에 올린 PR을 연다. Files changed 탭에서 추가된 줄에 마우스를 올려 `+`를 누르고 코멘트를 남긴다. 아래 중 하나를 골라 구체적으로 요청한다.
   - "`feature/<주제>`의 예시(`feature/contributing`)를 한 줄 추가해 주세요. 처음 보는 사람은 `<주제>`를 그대로 쓸 수 있습니다."
   - "commit 메시지 규칙(제목은 명령형, 본문에 이유) 한 줄을 추가해 주세요. 리뷰할 때 기준이 됩니다."
2. Review changes → **Request changes** → Submit review. 코멘트 오른쪽 위 메뉴의 Copy link로 코멘트 URL을 적어 둔다.
3. 제안자로서 내 PR에 달린 요청을 읽고 `partner-practice` 폴더에서 수정·commit·push한다. PR은 자동으로 갱신된다.

```powershell
git status
git add README.md
git commit -m "Address review: add branch name example"
git push
```

4. 리뷰어로서 갱신된 PR을 다시 보고 Review changes → **Approve** → Merge pull request → Confirm merge를 누른다.
5. 저장소 주인으로서 로컬 `main`을 갱신한다.

```powershell
Set-Location <개인 저장소 폴더>
git pull
git log --oneline -3
```

6. 검증·기록 단계에서 개인 저장소에 `notes/week02_links.md`를 만들어 내가 올린 Issue·PR URL, 내가 남긴 리뷰 코멘트 URL, 1교시의 `git log --graph --oneline --all` 출력을 적고 commit·push한다.

완료 조건:

- [ ] 내가 남긴 코멘트가 코드 줄에 붙어 있고 리뷰 상태가 Changes requested → Approved로 바뀌었다.
- [ ] 내 PR이 Merged 상태이고, 연결된 Issue가 자동으로 닫혔다.
- [ ] `git pull` 뒤 로컬 `main`에 짝의 commit과 merge commit이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — Issue 템플릿이나 PR 템플릿이 보이지 않는다</summary>

템플릿은 **base 저장소(짝 저장소)의 기본 branch(`main`)**에 push되어 있어야 적용된다. 짝의 저장소 페이지에서 `.github` 폴더가 보이는지 확인한다. fork에만 넣은 템플릿은 원본으로 보내는 PR에 적용되지 않는다. 템플릿 push 전에 Issue나 PR을 열었다면 `examples/pr_template/` 파일 내용을 본문에 붙여넣는다.
</details>

<details>
<summary>힌트 2 — push했는데 PR에 반영되지 않는다</summary>

`git branch -vv`로 현재 branch가 `feature/contributing`이고 `origin/feature/contributing`을 추적하는지 확인한다. 파일을 고쳤지만 `git add`·`git commit`·`git push` 중 하나를 빠뜨린 경우가 가장 많다. `git status`와 `git log --oneline -2`로 어느 단계까지 왔는지 본다.
</details>

<details>
<summary>힌트 3 — Merge 버튼이 비활성이다</summary>

Draft 상태면 Ready for review를 누른다. "This branch has conflicts"가 보이면 base의 README가 그 사이에 바뀐 것이다. 제안자가 `partner-practice` 폴더에서 `git pull <짝 저장소 HTTPS URL> main`을 실행해 1교시 절차대로 충돌을 해결하고 push한다. Request changes가 남아 있으면 리뷰어가 Approve로 바꿔야 한다.
</details>

### 검증

- 정상: PR 페이지의 Conversation 탭에 Issue 링크, 리뷰 요청, 수정 commit, Approve, Merged가 순서대로 기록되어 있다.
- 경계 또는 실패: `partner-practice` 폴더에서 권한이 없는 짝 저장소 URL로 `git push <짝 저장소 HTTPS URL> feature/contributing`을 한 번 시도하고 거부 메시지(`Permission denied` 또는 `403`)를 읽는다. 우회하지 않는다.
- 설명: "Fork와 branch 중 어느 것이 권한 문제를 해결하고, 어느 것이 작업 분리를 해결하는가"를 두 문장으로 적는다.

### 확장 문제

1. fork의 `main`을 원본과 맞춘다. GitHub 웹의 Sync fork, 또는 `git remote add upstream <짝 저장소 HTTPS URL>` → `git fetch upstream` → `git merge upstream/main`. `git remote -v`가 4줄이 되는 이유를 설명한다.
2. Draft PR을 하나 열어 Merge 버튼이 비활성인 것을 확인하고 Ready for review로 바꾼 뒤 merge하지 않고 닫는다.
3. `examples/CONTRIBUTING_sample.md`를 참고해 개인 저장소에 `CONTRIBUTING.md`를 추가하는 PR을 같은 저장소 안의 branch에서 스스로에게 보내고 merge한다.

## 3교시 실습 — 라이선스 판별과 LICENSE 추가

### 상황

짝의 PR이 merge되어 내 저장소에는 이제 다른 사람의 기여가 들어 있다. 그런데 `LICENSE`가 없어서 짝도 나도 이 코드를 어떤 조건으로 쓸 수 있는지 말할 수 없다. 판별 카드로 감을 잡고, 저장소에 LICENSE를 고르고, 앞으로 쓸 패키지·모델·데이터 후보의 조건을 표로 만들어라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–3분 | 카드 규칙 읽기, 10문항 판단 예상 |
| 판별 카드 | 3–13분 | `license_cards_answers.md` 10문항 판단·근거 |
| LICENSE 추가 | 13–19분 | MIT 또는 Apache-2.0 선택, 파일 추가, 이유 1문장, commit·push |
| 라이선스 표 | 19–26분 | `license_matrix.md` 항목 5개 이상 |
| 검증·기록 | 26–30분 | SPDX ID 대조, 설명 문장 |

### 준비

이어받는 것: 2교시에서 짝의 PR이 merge된 개인 저장소. 로컬 `main`이 최신인지 확인하고 양식을 복사한다.

```powershell
Set-Location <개인 저장소 폴더>
git pull
git status
Copy-Item <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\license_cards.md .\license_cards_answers.md
Copy-Item <수업자료>\open_source_ai\weeks\week02_git_github_license\examples\license_matrix_template.md .\license_matrix.md
```

### 문제 1 · 판별 카드 10문항

1. `license_cards_answers.md`의 규칙을 읽는다. 각 카드는 상황 → 질문 → 판단(가능·조건부·불가) → 근거 → 출처 순으로 채운다.
2. 먼저 10문항의 판단만 3분 안에 예상해 적는다.
3. 카드마다 근거를 한 문장으로 적는다. 근거에는 라이선스 이름과 조항의 핵심 단어(고지 유지, 소스 공개, 네트워크 제공, 비상업, 동일 조건, 사용 정책, 특허)를 넣는다.
4. 판단이 갈리는 카드는 choosealicense·SPDX·모델 카드에서 원문을 찾아 출처 URL을 적는다. 검색 결과 요약 페이지는 출처로 쓰지 않는다.
5. 예상과 달라진 카드 번호와 이유를 파일 끝 표에 적는다.

완료 조건:

- [ ] 10문항 모두 판단·근거가 있다.
- [ ] 최소 3문항에 출처 URL이 있다.
- [ ] 예상과 달라진 카드와 이유를 적었다.

### 문제 2 · LICENSE 추가와 라이선스 표

1. MIT와 Apache-2.0 중 하나를 고른다. 판단 기준은 셋이다. 특허 조항이 필요한가, `NOTICE` 파일과 변경 표시를 관리할 것인가, 짧고 익숙한 쪽을 원하는가.
2. GitHub 저장소 페이지에서 Add file → Create new file → 파일 이름 `LICENSE` → 오른쪽에 나타나는 Choose a license template → 고른 라이선스 → 연도와 저작권자(GitHub 계정 이름) 확인 → Commit changes(`main`에 직접 commit). GitHub 접속이 안 되면 choosealicense.com의 원문을 복사해 로컬에서 `LICENSE`를 만들고 commit한다.
3. 로컬로 가져와 확인한다.

```powershell
git pull
git log --oneline -2
Get-Content LICENSE -TotalCount 3
```

4. `README.md` 끝에 `## 라이선스` 절을 추가하고 선택 이유를 한 문장으로 쓴다. 예: "특허 조항이 필요 없고 가장 짧아 MIT를 골랐다." commit 메시지는 `Explain license choice`, push한다.
5. `license_matrix.md`를 채운다. 앞으로 이 저장소에서 쓸 후보를 코드·모델·데이터 세 종류 모두 넣어 5행 이상 만든다. 후보 예: `httpx`, `python-dotenv`(3주차에 쓴다), 기본 생성 모델 `qwen3:4b`(환경변수 `OLLAMA_MODEL`의 교재 기본값), 임베딩 모델 `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct`, `intfloat/multilingual-e5-small`, 사용 제한 조항이 있는 모델 1개(Llama·Gemma 계열), 데이터 1개(CC 계열). 정확한 모델 ID는 환경 기준표에서 확정하므로 표에는 확인한 ID를 그대로 적는다.
6. 각 행의 라이선스는 패키지의 PyPI 페이지와 저장소 LICENSE 파일, 모델은 Hugging Face 모델 카드와 Ollama 라이브러리 페이지에서 확인해 출처 URL을 적는다. SPDX 목록에 없는 라이선스는 `LicenseRef-` 접두사로 적는다.
7. commit 메시지 `Add license matrix`, push한다.

완료 조건:

- [ ] `LICENSE`가 저장소 루트에 있고 `git log`에 추가 commit이 있다.
- [ ] `README.md`에 선택 이유 1문장이 있다.
- [ ] `license_matrix.md`에 5행 이상이 있고 모든 행에 SPDX ID(또는 `LicenseRef-`)와 출처 URL이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — GitHub의 Choose a license template 버튼이 안 보인다</summary>

파일 이름을 확장자 없이 정확히 `LICENSE`로 입력해야 오른쪽에 나타난다. 그래도 안 보이면 choosealicense.com에서 해당 라이선스 페이지의 텍스트를 복사해 붙여넣고, `[year]`·`[fullname]` 자리를 연도와 GitHub 계정 이름으로 바꾼다.
</details>

<details>
<summary>힌트 2 — 모델 카드의 라이선스가 "other"이거나 이름만 있다</summary>

모델 카드 상단의 `license:` 태그와 저장소 파일 목록의 LICENSE 파일을 연다. 이름만 있으면 SPDX 목록에서 검색하고, 없으면 `LicenseRef-이름`으로 적은 뒤 재배포 조건에 "OSI 승인 아님, 사용 정책 있음"처럼 조건을 쓴다. 같은 계열이라도 크기별로 다를 수 있으니 정확한 모델 ID의 카드를 본다.
</details>

<details>
<summary>힌트 3 — 패키지 라이선스가 PyPI에 여러 개 표시된다</summary>

저장소의 LICENSE 파일을 우선한다. 두 라이선스 중 선택인 경우는 `MIT OR Apache-2.0`처럼 `OR`로 적고, 둘 다 지켜야 하는 경우는 `AND`로 적는다.
</details>

### 검증

- 정상: `license_matrix.md`의 SPDX ID를 <https://spdx.org/licenses/>에서 하나씩 검색해 모두 존재하거나 `LicenseRef-`로 표기되어 있다.
- 경계 또는 실패: 카드 6(LICENSE 없음)과 카드 8(CC BY-NC 데이터로 상용 서비스)의 판단을 짝과 비교한다. 다르면 근거 조항을 서로 읽고 결론을 낸다.
- 설명: "오픈 웨이트와 오픈소스가 다른 이유"를 한 문장으로 적는다.

### 확장 문제

1. 개인 저장소의 라이선스를 MIT에서 Apache-2.0으로(또는 반대로) 바꾸려면 무엇을 확인해야 하는지 적는다. 이미 merge된 짝의 기여가 있다는 점을 고려한다.
2. `license_matrix.md`에 "호환성" 열을 추가하고, 각 항목을 내 저장소 LICENSE와 함께 배포할 수 있는지 방향(permissive → copyleft 가능, 역방향 불가)을 표시한다.
3. `examples/CONTRIBUTING_sample.md`의 "기여물의 라이선스" 절을 읽고 내 저장소 `CONTRIBUTING.md`에 넣을 문장 초안을 쓴다.

## 제출 체크

- 개인 저장소 URL: 원격 연결, 충돌 해결 merge commit, `.github/` 템플릿, `LICENSE`, `license_matrix.md`가 모두 `main`에 있다.
- `notes/week02_links.md`: 내가 올린 Issue·PR URL, 내가 남긴 리뷰 코멘트 URL, `git log --graph --oneline --all` 출력
- `license_cards_answers.md`: 10문항 판단·근거·출처, 예상과 달라진 카드
- `license_matrix.md`: 5행 이상, SPDX ID·상업적 이용·재배포 조건·출처 URL
- `README.md`: 기여 방법 절(짝의 PR), 라이선스 선택 이유 1문장
- 선택: 확장 문제 결과
