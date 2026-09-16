---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 8주차"
footer: "중간 개인 실기 · 리허설과 본시험"
---

# 중간 개인 실기

2~7주에 배운 것을 **혼자 60분 안에** 만들어 공개 주소에 올립니다.

```text
1일차  리허설 60분 + 새 저장소·Pages 켜기   ← 준비는 오늘 끝낸다
2일차  본시험 60분 (my-web/exam/)          ← 만드는 일만 한다
```

배점은 **20점**입니다. 주차별 실습 점수가 아닙니다.

---

# 1일차 — 시험 안내와 리허설

`30분 설명 → 60분 리허설`

1. 시험 범위와 채점표
2. 제출 형식과 60분 배분
3. 본시험은 `my-web/exam/`에서
4. 허용 자료와 장애 대체

---

## 1일차 · 0–8분 — 시험 범위와 채점표

범위는 **2~7주**입니다. Pages · HTML · CSS · DOM · 폼.

| 영역 | 배점 |
|---|---:|
| Pages 배포·commit 2개 이상 | 3 |
| HTML 구조(뼈대·목록·표·폼) | 4 |
| CSS(선택자·박스·flex·`@media`) | 4 |
| DOM 이벤트(클릭 → `textContent`·`classList`) | 5 |
| 폼 입력·빈값 안내 | 3 |
| Console 오류 없음 | 1 |

범위 밖: 배열 목록(10주) · `localStorage`(11주) · `fetch`(12주) · 모듈.

---

## 1일차 · 8–16분 — 제출 형식과 60분 배분

```text
① 공개 URL   https://student01.github.io/my-web/exam/
② 저장소 URL https://github.com/student01/my-web
③ 마지막 commit SHA   git log -1 --oneline
④ 완성 화면 캡처 1장 (주소창 포함)
```

| 시험 60분 | 할 일 |
|---|---|
| 0–5 · 5–15 · 15–25 | 문제 읽기 · HTML · CSS |
| 25–50 · 50–55 · 55–60 | DOM·폼 · push · **예비** |

예비 5분은 Pages 반영(1~3분)과 로그인 다시 하기를 흡수하는 시간입니다.

---

## 1일차 · 16–24분 — 본시험은 my-web/exam/에서

```bash
cd my-web
mkdir exam
```

- 새 저장소를 만들지 않습니다. `my-web`은 **저장소·로그인·Pages가 이미 살아 있습니다**.
- 시험 중에 저장소 만들기, 브라우저 로그인, Pages 켜기를 하지 않습니다.
- 공개 주소는 폴더 이름이 그대로 붙은 `https://<아이디>.github.io/my-web/exam/`입니다.
- 저장소 만들기와 Pages 켜기는 **오늘 리허설에서** 한 번 더 해 둡니다.

```text
my-web/  index.html  about.html  guestbook.html  styles.css  …
         exam/  index.html  styles.css  app.js     ← 시험 답안
```

---

## 1일차 · 24–30분 — 허용 자료·장애 대체와 실습 인계

[1일차 실습](lab.md#1일차--리허설과-저장소-준비-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

- 볼 수 있는 것: 교재 사이트, 본인 `my-web` 저장소, MDN. 그 밖은 강의자 공지를 따릅니다.
- Pages가 늦으면 로컬 화면 캡처 + commit SHA로 대신 인정합니다.
- 오늘 할 일: 리허설 문제 4개 → 해답과 맞춰 보기 → 새 저장소 `midterm-practice` → Pages.

**설명 합계: 8+8+8+6 = 30분**

---

# 2일차 — 본시험

`30분 안내 → 60분 시험`

1. 절차와 "제출본"의 뜻
2. 장애가 나면
3. starter를 `exam/`에 복사하고 실행 확인
4. 질문 → 시험 시작

---

## 2일차 · 0–8분 — 절차와 제출본의 뜻

```text
저장 → push → 공개 주소 새로고침 → 보이는 것 = 제출본
```

- 편집기에서만 보이는 화면은 제출본이 아닙니다. **저장하지 않은 파일은 commit되지 않습니다.**
- commit하지 않은 변경은 push되지 않고, push하지 않은 commit은 공개 주소에 없습니다.
- 작업 폴더는 `my-web/exam/` 하나입니다. 다른 폴더의 파일은 채점하지 않습니다.
- 자리·좌석 이동·질문 방법은 시작 전에 안내합니다.

---

## 2일차 · 8–16분 — 장애가 나면

| 일어난 일 | 할 일 |
|---|---|
| Pages가 5분 넘게 옛 화면 | 로컬 화면 캡처 + `git log -1 --oneline` 제출 |
| `Permission ... denied to <다른 아이디>` | 자격 증명 관리자에서 `git:https://github.com` 삭제 후 다시 push |
| `! [rejected] main -> main (fetch first)` | `git pull` 뒤 다시 `git push` |
| push 자체가 안 됨 | 손을 들어 알린다. 시각을 적고 폴더를 zip으로 제출 |

혼자 10분 이상 붙잡지 않습니다. 손을 들면 **환경 문제만** 함께 봅니다.

---

## 2일차 · 16–24분 — starter를 exam 폴더에 복사하고 실행 확인

```bash
cd my-web
git pull
mkdir exam
```

1. 배포된 starter 세 파일을 `exam/`에 넣습니다.
2. 탐색기에서 `exam/index.html`을 더블클릭해 `file://`로 열립니다.
3. F12 **Console**에 빨간 줄이 없는지 봅니다.
4. `git add .` → `git commit -m "중간 실기 시작"` → `git push`로 **첫 commit**을 만듭니다.
5. 여기까지 되면 시험을 시작합니다.

- 지금 안 열리면 문제지가 아니라 **파일 위치**입니다. 세 파일이 `exam/` 안에 나란히 있어야 합니다.

---

## 2일차 · 24–30분 — 질문과 시험 시작

[2일차 실습](lab.md#2일차--중간-실기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

- 받을 질문: 문제 문장의 뜻, 파일 위치, 제출 방법, 장애.
- 받지 않는 질문: 어떻게 만드는가, 이 코드가 맞는가.
- 한 문제에 막히면 **다음 문제로 넘어갑니다.** 문제끼리는 이어져 있지 않습니다.

**설명 합계: 8+8+8+6 = 30분**

---

## 제출하기

시험이 끝나면 네 가지를 제출합니다.

```text
① https://student01.github.io/my-web/exam/
② https://github.com/student01/my-web
③ 1ea3c2e            ← git log -1 --oneline
④ 캡처 1장 (완성 화면 + 주소창)
```

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다음 주 미리 보기

9주차는 **1차 과제 발표**입니다.

오늘 만든 `exam/` 폴더가 아니라 3~7주에 만든 `my-web` 본체를 2분 동안 시연합니다.
공개 주소 열기 → 세 페이지 이동 → 버튼·폼 → GitHub **Commits** 탭.
레포트는 저장소 `README.md` 한 장입니다.
