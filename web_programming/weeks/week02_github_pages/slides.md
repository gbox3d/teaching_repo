---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 2주차"
footer: "GitHub와 GitHub Pages"
---

# 2주차
## GitHub와 공개 배포

local commit을 공유하고, 공개 URL의 오류를 증거로 진단한다.

---

## 이번 주 결과물

- 저장소 URL
- branch가 갈라지고 합쳐진 log graph
- merge commit 또는 conflict 해결 commit
- GitHub Pages 공개 URL
- 오류의 증상·증거·원인·해결 표

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## local, remote, branch, merge

---

## 0–5분 · 저장소는 두 곳에 있다

```text
내 PC                                      GitHub
local repository  ─────── push ───────▶  remote repository
                  ◀────── fetch ───────
```

- GitHub는 Git의 원격 저장소를 제공하는 서비스다.
- local commit과 remote commit은 자동으로 같아지지 않는다.
- `origin`은 관례적인 remote 별칭일 뿐 URL 자체가 아니다.

---

## 5–10분 · remote와 upstream

```bash
git remote -v
git branch -vv
git push -u origin main
```

- remote URL: 어디와 통신하는가
- remote-tracking branch: 마지막으로 관찰한 원격 상태
- upstream: 현재 local branch가 기본으로 비교할 상대

`-u` 뒤에는 `git push`, `git pull`을 짧게 쓸 수 있다.

---

## 10–15분 · fetch, pull, push

| 명령 | 핵심 효과 |
|---|---|
| `fetch` | 원격 정보를 가져오되 현재 작업 branch는 합치지 않음 |
| `pull` | fetch 후 현재 branch에 통합 |
| `push` | local commit을 원격 branch로 전송 |

작업 중 변경이 있으면 무작정 pull하기 전에 `status`를 읽는다.

---

## 15–20분 · branch는 독립된 작업선

```text
             A1──A2  layout-a
            /
base ──────●
            \
             B1      layout-b
```

```bash
git switch -c layout-a
git switch main
git switch -c layout-b
```

branch는 폴더 복사본이 아니라 commit을 가리키는 움직이는 이름이다.

---

## 20–25분 · fast-forward와 merge commit

- main 뒤에 한 작업선만 있으면 pointer를 전진할 수 있다.
- 양쪽에 새 commit이 있으면 두 부모를 가진 merge commit으로 합칠 수 있다.
- 같은 파일을 바꾸어도 다른 줄이면 자동 merge가 가능하다.

```bash
git switch main
git merge layout-a
```

**질문:** 자동 merge는 의미까지 올바르다는 뜻인가?

---

## 25–30분 · conflict는 선택 요청이다

```text
marker: <<<<<<< HEAD
main 쪽 내용
marker: =======
합치려는 branch 내용
marker: >>>>>>> layout-b
```

1. marker의 두 의도를 읽는다.
2. 최종 결과를 직접 작성한다.
3. marker를 모두 제거한다.
4. 실행하고 diff를 검토한다.
5. add와 commit으로 해결을 기록한다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## GitHub Pages와 배포 진단

---

## 0–5분 · Pages의 책임

GitHub Pages는 저장소의 HTML, CSS, JavaScript 같은 정적 자산을 웹으로 게시한다.

```text
push → publishing source → Pages workflow → public URL
```

서버에서 PHP·Python을 실행하는 호스팅이 아니다.

---

## 5–10분 · 두 URL 형태

사용자/조직 사이트:

```text
repository: USER.github.io
URL:        https://USER.github.io/
```

project site:

```text
repository: campus-page
URL:        https://USER.github.io/campus-page/
```

project site에는 repository 이름이 base path로 들어간다.

---

## 10–15분 · branch에서 게시하기

현재 공식 절차의 핵심:

1. Repository **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, Folder: `/(root)`
4. source 최상위에 `index.html`
5. 저장 후 Actions의 Pages 배포 run 확인

UI 문구가 달라지면 공식 문서를 기준으로 한다.

---

## 15–20분 · 상대경로가 이동에 강하다

project URL이 `/campus-page/`일 때:

```html
<!-- project 안에서 유지 -->
<link rel="stylesheet" href="./assets/styles.css">

<!-- 도메인 root를 가리켜 project base가 빠짐 -->
<link rel="stylesheet" href="/assets/styles.css">
```

정적 프로젝트 내부 자산은 상대경로를 기본으로 한다.

---

## 20–24분 · 대소문자는 계약이다

```html
<img src="assets/Campus-Mark.svg" alt="">
```

실제 파일:

```text
assets/campus-mark.svg
```

Windows 로컬 환경에서 우연히 보이더라도 배포 환경에서는 404가 될 수 있다. 참조 문자열과 파일명을 정확히 맞춘다.

---

## 24–28분 · 진단 사다리

```text
1. URL과 증상 기록
2. latest commit이 push됐는지 확인
3. Pages workflow 성공/실패 확인
4. Network의 실패 URL·status 확인
5. 파일명·대소문자·상대경로 확인
6. 한 원인만 수정 → commit → push → 재검증
```

강력 새로고침은 원인 수정 뒤 검증 단계다.

---

## 28–30분 · 완료 조건

- 공개 URL에서 모든 local asset 요청 200
- 새로고침과 하위 link 이동 정상
- 오류 해결표에 추측이 아닌 증거 기록
- 수정 commit을 Pages가 실제 배포한 SHA와 연결

---

## 정리

```text
Git: branch의 commit을 remote와 동기화
Pages: 특정 source의 commit을 공개 URL로 배포
진단: commit → workflow → request → browser 순으로 좁히기
```
