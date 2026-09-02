# 2주차 실습 — branch를 합치고 공개 URL을 복구하라

## 공통 산출물

- 저장소 URL과 Pages URL
- `git log --oneline --graph --decorate --all` 결과
- merge 또는 conflict 해결 commit
- 배포 오류 해결표

계정 비밀번호나 토큰이 터미널·캡처·commit에 포함되지 않았는지 제출 전에 확인한다.

## 1일차 실습 — 갈라진 두 작업을 합치기

### 문제 상황

한 랜딩 페이지에 두 디자인 제안이 같은 소개 문장을 다르게 수정했다. 두 branch의 이력을 보존하면서 강의 요구인 “두 핵심 표현을 모두 포함한 한 문장”으로 합치고 원격 저장소에 게시하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 원격 연결 | 0–10분 | GitHub 빈 repository, origin, 첫 push |
| branch A | 10–20분 | 소개 문장과 footer 변경·commit |
| branch B | 20–30분 | 같은 소개 문장과 title 변경·commit |
| merge | 30–43분 | 자동 merge와 conflict 관찰·해결 |
| remote 검증 | 43–52분 | push, tracking 상태, GitHub SHA 확인 |
| 설명·확장 | 52–60분 | 상태도 작성, 선택 확장 |

### 준비

1. [examples/broken-site](examples/broken-site/)를 `week02-pages`라는 별도 개인 폴더로 복사한다.
2. GitHub에서 README, `.gitignore`, license를 추가하지 않은 빈 공개 repository `week02-pages`를 만든다.
3. 개인 폴더에서 다음을 실행한다.

```bash
git init
git branch -M main
git add .
git commit -m "Add deployable landing page"
git remote add origin <본인 repository URL>
git push -u origin main
```

`<...>`는 그대로 입력하는 문자가 아니다. 본인 repository URL로 바꾼다.

### 문제 1 · 두 branch 만들기

`main`이 clean인지 확인한 뒤 다음 의도로 수정한다.

**branch A: `layout-a`**

- `index.html`의 소개 문장을 “프로젝트를 작은 단계로 배포합니다.”로 바꾼다.
- footer에 “경로를 검증합니다.”를 추가한다.
- 한 commit으로 기록한다.

**branch B: `layout-b`**

- 반드시 원래 `main`에서 새로 만든다.
- 같은 소개 문장을 “오류를 증거로 진단합니다.”로 바꾼다.
- `<title>`에 `· 공개 배포`를 추가한다.
- 한 commit으로 기록한다.

각 branch에서 commit 직전 `git diff --staged`를 읽는다.

### 문제 2 · 합치기

1. main으로 전환해 `layout-a`를 merge한다.
2. `layout-b`를 merge한다.
3. 자동으로 합쳐진 파일과 conflict 파일을 `git status`로 구분한다.
4. 소개 문장의 최종 결과를 다음 요구에 맞게 직접 작성한다.

```text
작은 단계로 배포하고, 오류를 증거로 진단합니다.
```

5. 모든 marker를 제거한다.
6. 브라우저에서 title, 소개, footer가 모두 반영됐는지 확인한다.
7. 해결 결과를 add/commit하고 main을 push한다.

### 검증

```bash
git status
git log --oneline --graph --decorate --all -10
git branch -vv
```

- [ ] 두 branch가 같은 base에서 갈라졌다.
- [ ] A의 footer와 B의 title이 모두 남았다.
- [ ] 소개 문장은 두 의도를 통합했다.
- [ ] conflict marker `<<<<<<<`, `=======`, `>>>>>>>`가 없다.
- [ ] local main과 `origin/main`이 같은 commit을 가리킨다.

### 단계별 힌트

<details>
<summary>힌트 1 — layout-b가 layout-a의 commit을 포함한다</summary>

`layout-b`를 만들기 전에 `git switch main`을 했는지 graph로 확인한다. 실습 초기라면 branch B를 삭제하기 전에 변경이 commit되어 있는지 확인하고 강의자와 안전하게 다시 만든다.
</details>

<details>
<summary>힌트 2 — merge를 시작했는데 어디가 충돌인지 모르겠다</summary>

`git status`의 `both modified` 파일을 열고 `<<<<<<<`를 검색한다. marker 사이 두 문장을 읽는다.
</details>

<details>
<summary>힌트 3 — push가 rejected다</summary>

오류의 non-fast-forward 문장을 확인한다. 원격에 예상하지 않은 commit이 있는지 `git fetch origin` 후 graph를 비교한다. 강제로 push하지 말고 강의자와 통합 방향을 확인한다.
</details>

### 실패·경계 경로

- merge 중인 상태에서 다른 branch로 switch를 시도하고 Git의 보호 메시지를 읽는다. 작업을 잃는 명령은 실행하지 않는다.
- 두 branch가 서로 다른 줄만 수정한 간단한 변경을 추가해 자동 merge와 의미 검토를 경험한다.

### 확장

1. 2인 1조로 한 GitHub repository를 clone해 각자 branch를 push하고 Pull Request의 Files changed를 비교한다.
2. `git log --left-right --oneline main...layout-b`로 어느 쪽에만 있는 commit인지 관찰한다.
3. merge 전후의 graph를 손으로 그리고 각 pointer가 가리키는 commit을 표시한다.

## 2일차 실습 — Pages 공개 URL 진단

### 문제 상황

랜딩 페이지는 localhost에서 정상인데 GitHub Pages에서는 style, image 또는 JavaScript 중 하나가 사라진다. publishing source부터 실패 요청까지 증거 사다리를 따라 원인을 한 개씩 고쳐라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| source 설정 | 0–12분 | Pages branch/root 설정, workflow 확인 |
| 정상 기준 | 12–22분 | 공개 URL과 네 자원 200 확인 |
| 오류 재현 | 22–38분 | 경로/대소문자 오류 하나를 commit·push |
| 진단·복구 | 38–50분 | 실패 URL 근거로 최소 수정 |
| 재검증 | 50–57분 | workflow, Network, 새로고침 |
| 회고 | 57–60분 | 오류 해결표 완성 |

### 문제 1 · 배포 기준선 만들기

GitHub repository에서 다음 개념을 확인하며 설정한다.

1. `Settings → Pages`
2. Source: `Deploy from a branch`
3. Branch: `main`, Folder: `/(root)`
4. Save
5. `Actions`에서 Pages 배포 run과 commit SHA 확인
6. `https://<USER>.github.io/week02-pages/` 열기

공식 UI 문구가 바뀌었으면 [publishing source 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)를 기준으로 한다.

Network에서 다음이 모두 200인지 기록한다.

- document
- `assets/styles.css`
- `assets/app.js`
- `assets/campus-mark.svg`

### 문제 2 · 오류 하나 심기

아래 중 한 종류를 선택한다. 팀원과 서로 다른 종류를 선택하면 비교하기 좋다.

| 유형 | 변경 | 예상 공개 증상 |
|---|---|---|
| base path | `./assets/styles.css` → `/assets/styles.css` | style 요청이 domain root로 감 |
| 대소문자 | `campus-mark.svg` → `Campus-Mark.svg` | image 404 가능 |
| 파일명 | `app.js` → `apps.js` | 버튼의 상태 문구가 바뀌지 않음 |

변경을 `Introduce path fault for diagnosis` 같은 명확한 메시지로 commit/push한다. 배포가 끝난 뒤 실제 증상이 예상과 같은지 확인한다.

### 문제 3 · 진단 사다리

아래 표를 채우고 한 단계씩만 진행한다.

| 항목 | 관찰 결과 |
|---|---|
| 공개 URL 전체 |  |
| main의 최신 commit SHA |  |
| Pages workflow 상태와 SHA |  |
| 실패 Request URL |  |
| HTTP status / Console 첫 오류 |  |
| 실제 repository 파일 경로 |  |
| 한 문장 원인 |  |
| 최소 수정 |  |
| 수정 commit SHA |  |
| 재검증 결과 |  |

수정은 참조 문자열 또는 파일명 한 곳으로 제한한다. 복구 commit을 push하고 새 workflow가 완료된 뒤 Network를 다시 확인한다.

### 단계별 힌트

<details>
<summary>힌트 1 — Pages URL 자체가 404다</summary>

repository 이름이 URL path에 정확히 포함됐는지, publishing source가 존재하는 main/root인지, root에 소문자 `index.html`이 있는지 확인한다.
</details>

<details>
<summary>힌트 2 — 수정 commit이 배포되지 않았다</summary>

GitHub main의 latest SHA와 local `git rev-parse --short HEAD`를 비교한다. 다르면 올바른 branch를 push했는지 확인한다.
</details>

<details>
<summary>힌트 3 — Network에서 `/assets/...`가 보인다</summary>

project site의 올바른 요청에는 `/week02-pages/assets/...`가 포함되어야 한다. 참조 앞의 `/`가 repository base를 제거했는지 본다.
</details>

### 최종 검증

- [ ] 새 브라우저 탭의 공개 URL에서 페이지가 보인다.
- [ ] 문서, CSS, JS, SVG 요청이 모두 200이다.
- [ ] 버튼을 누르면 `배포 자산 연결: 정상`으로 바뀐다.
- [ ] 강력 새로고침 뒤에도 결과가 같다.
- [ ] URL 끝의 `/`가 있는 진입과 `index.html` 직접 진입을 확인했다.
- [ ] 해결표의 원인이 실패 URL과 연결된다.

### 확장 주제

1. `about/index.html`을 만들고 `../assets/styles.css` 경로를 계산해 본다.
2. custom 404 페이지의 역할을 조사하되 실제 Pages 설정 변경은 하지 않는다.
3. branch 배포와 custom GitHub Actions 배포가 각각 적합한 경우를 표로 비교한다.
4. 공개 사이트가 private repository의 비밀 보관소가 될 수 없는 이유를 threat 관점에서 설명한다.
