---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 15주차"
footer: "기말 개인 실기 · 구현 15 + 시연 5"
---

# 기말 개인 실기

14주차에 발표한 사이트는 이제 손대지 않습니다.
이번 주는 **처음 보는 starter**에 2~13주의 기능을 다시 만드는 개인 실기입니다.

```text
web-final/
  index.html       ← 뼈대·폼·목록 자리
  styles.css       ← 색·flex·@media
  app.js           ← TODO 1~4
  data/items.json  ← 추천 목록 데이터
```

1일차는 같은 형태의 **리허설**, 2일차가 **본시험 60분**입니다.

---

# 1일차 — 시험 안내와 리허설

`30분 안내 → 60분 리허설`

1. 시험 범위와 공개 starter
2. 채점표 20점
3. 제출 세 가지와 오늘 끝낼 준비
4. 허용 자료와 장애 대체

---

## 1일차 · 0–8분 ① — 시험 범위는 2~13주입니다

| 주차 | 시험에 나오는 것 |
|---|---|
| 2 | 저장소 push와 Pages 공개 |
| 3 | 뼈대·목록·표·form |
| 4 | 색·박스·`flex`·`@media` |
| 6 | 클릭 → `textContent`·`classList` |
| 7 · 10 | 폼 값 읽기·빈값 안내·목록 추가·삭제 |
| 11 | `localStorage` 저장과 복원 |
| 12 | `fetch`로 JSON 불러오기와 오류 안내 |

14주 발표 내용과 새 문법은 나오지 않습니다.

---

## 1일차 · 0–8분 ② — 공개 starter 네 파일

```text
web-final/
  index.html        h1·form·ul 자리가 다 있다
  styles.css        body.dark 규칙과 @media 하나
  app.js            TODO 1~4 (지금은 [다크 모드]만 동작)
  data/items.json   추천 3권
```

- 13주차에 공개한 [rehearsal_starter](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam/examples/rehearsal_starter)와 같은 구조입니다.
- Console 오류는 **0개**입니다. 기능이 없을 뿐 깨져 있지 않습니다.
- 저장 키는 `final-items`입니다. `my-web`의 `guestbook`과 섞이지 않게 다른 이름을 씁니다.

---

## 1일차 · 8–16분 — 채점표 20점

| 항목 | 배점 |
|---|---:|
| HTML·CSS | 3 |
| DOM 이벤트 | 3 |
| 폼·목록 추가·삭제 | 4 |
| localStorage | 2 |
| fetch·오류 안내 | 3 |
| URL 재현(채점자가 공개 주소를 연다) | 3 |
| 구술(좌석에서 1분) | 2 |

전문은 [채점표](rubric.md)에 있습니다. 배점은 승인 전 **안**입니다.

---

## 1일차 · 16–24분 ① — 제출은 세 가지입니다

```text
1. https://student01.github.io/web-final/   ← 공개 주소
2. https://github.com/student01/web-final   ← 저장소 주소
3. dd80e4c…(40자)                            ← 마지막 commit 번호
```

```bash
git log -1 --format=%H
```

- **저장하고 push해서 공개 주소에 보이는 것**이 제출본입니다.
- 캡처 1장(주소창이 보이게)을 함께 냅니다.

---

## 1일차 · 16–24분 ② — 오늘 안에 끝내는 것

1. GitHub에서 저장소 `web-final` 만들기 (**Public**, README 체크 끄기)
2. `git clone` → starter 네 파일 넣기 → `git push -u origin main`
3. **Settings › Pages** → `main` · `/(root)` → **Save** → 공개 주소 열기

- 시험 당일에는 저장소를 만들지 않고 Pages도 켜지 않습니다. 오늘 끝냅니다.
- 공용 PC의 로그인 문제도 오늘 겪고 끝냅니다(자격 증명 관리자).
- 확인의 기준은 공개 주소입니다. 로컬 미리보기(Live Server, `python3 -m http.server 8000`)는 선택입니다.

---

## 1일차 · 24–30분 ① — 허용 자료와 장애 대체

| 구분 | 내용 |
|---|---|
| 허용 | 교재 사이트 · 본인 저장소(`my-web`) · MDN. 검색·AI 도구 범위는 수업 공지 |
| 금지 | 다른 학생 코드, 메신저, 남의 저장소 답안 |
| Pages 지연 | 5분 넘게 안 보이면 로컬 화면 캡처 + commit 번호로 인정 |
| 자격 증명 충돌 | `git:https://github.com` 삭제 후 다시 로그인, 그래도 막히면 압축 제출 |
| 네트워크 차단 | 그때만 `fetch` 문항을 `app.js` 안 배열로 대체 채점 |

장애는 혼자 해결하지 말고 손을 들어 시각을 기록받습니다.

---

## 1일차 · 24–30분 ② — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--리허설과-시험용-저장소-준비-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

1. 저장소 `web-final`을 만들고 starter 네 파일을 push해 Pages를 켭니다.
2. TODO 1~4를 차례로 채웁니다. 막히면 [완성본](examples/rehearsal_solution/app.js)의 그 부분만 봅니다.
3. 끝 5분에 push하고 공개 주소를 새로고침해 확인합니다.

**설명 합계: 8+8+8+6 = 30분**

오늘 리허설은 점수에 들어가지 않습니다. 내일을 위한 연습입니다.

---

# 2일차 — 본시험 60분

`30분 안내 → 60분 시험`

1. 오늘의 절차와 제출본의 뜻
2. 구술 1문항
3. starter 실행 확인
4. 60분을 쓰는 순서

---

## 2일차 · 0–8분 ① — 오늘의 절차

1. 감독이 시험 파일 네 개를 나눠 줍니다. `web-final` 폴더에 **덮어씁니다**.
2. 문항은 어제 리허설과 같은 형태입니다. 값과 화면 주제만 다릅니다.
3. 60분 동안 구현하고 마지막 5분에 push합니다.
4. 시험 후반에 좌석으로 가서 한 줄만 물어봅니다(구술 1분).

- 어제 리허설 commit은 그대로 남아 있습니다. 덮어써도 사라지지 않습니다.
- 질문은 문항 해석과 환경 문제만 받습니다. 구현 방법은 답하지 않습니다.

---

## 2일차 · 0–8분 ② — 저장 후 새로고침해서 보이는 것이 제출본

```text
VS Code 저장 → git add . → git commit → git push
                                  │ 1~3분
                                  ▼
        https://student01.github.io/web-final/   ← 채점자가 여는 화면
```

- 저장만 하면 GitHub도 공개 주소도 바뀌지 않습니다(2주차와 같습니다).
- commit만 하고 push하지 않으면 채점자에게는 보이지 않습니다.
- `git status`에 `Your branch is ahead of 'origin/main' by 1 commit.`이 있으면 아직 push 전입니다.

---

## 2일차 · 8–16분 — 구술 1분: 이 줄이 하는 일

- 시험 후반 30분 동안 좌석을 돌며 **한 사람에 1분**씩 묻습니다.
- 강의자가 본인 화면의 한 줄을 가리킵니다. 그 줄이 하는 일을 말하면 됩니다.
- 구현 시간은 그대로 60분입니다. 손을 멈추지 않아도 됩니다.

| 가리키는 줄 | 기대하는 답 |
|---|---|
| `event.preventDefault();` | 제출할 때 페이지가 새로고침되지 않게 막는다 |
| `localStorage.setItem('final-items', …)` | 목록을 브라우저에 글자로 저장한다 |
| `if (!response.ok)` | 파일을 못 찾았을 때 안내 문구로 가게 한다 |

---

## 2일차 · 16–24분 ① — starter 실행 확인 3분

1. 어제 만든 `web-final`을 `git pull`로 받는다(폴더가 없으면 `git clone`). 시험 파일 네 개를 덮어쓴다.
2. `index.html`을 브라우저로 한 번 연다. 화면이 뜨고 Console 오류가 0인지 본다.
3. `git status`에 바뀐 파일이 보이는지 본다.

```text
Changes not staged for commit:
	modified:   app.js
	modified:   data/items.json
	modified:   index.html
```

- 바뀐 파일 수는 문항에 따라 다릅니다. 네 파일 중 몇 개가 보이면 정상입니다.
- 여기서 오류가 나면 손을 듭니다. **구현을 시작하기 전에** 해결합니다.
- 어제 켠 Pages는 그대로 살아 있습니다. 다시 켜지 않습니다.

---

## 2일차 · 16–24분 ② — 60분을 이렇게 씁니다

| 시간 | 할 일 |
|---|---|
| 0–5분 | 문항 읽기·starter 실행 확인 |
| 5–15분 | HTML·CSS 문항 |
| 15–35분 | 폼·목록 추가·삭제 |
| 35–45분 | localStorage |
| 45–52분 | fetch·오류 안내 |
| 52–57분 | push와 제출 |
| 57–60분 | 예비(Pages 반영 대기) |

한 문항에서 막히면 다음으로 넘어갑니다. 문항끼리 서로 막지 않습니다.

---

## 2일차 · 24–30분 — 질문과 시작

[2일차 실습](lab.md#2일차--본시험-구현과-제출-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

- 질문은 문항 해석과 환경 문제만 받습니다.
- 제출은 공개 주소·저장소 주소·마지막 commit 번호와 캡처 1장입니다.
- 마감 10분·5분·1분 전에 알립니다.

**설명 합계: 8+8+8+6 = 30분**

---

## 제출하기

1. 공개 주소 `https://<아이디>.github.io/web-final/`
2. 저장소 주소 `https://github.com/<아이디>/web-final`
3. 마지막 commit 번호 — `git log -1 --format=%H`의 40자
4. 캡처 1장 — 위 공개 주소가 열린 화면(주소창 포함)

캡처에 실명·학번·실제 이메일이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 한 학기를 마치며

2주차에 만든 `my-web` 하나에 15주 동안 페이지를 쌓았습니다.

```text
2주 공개 → 3주 세 페이지 → 4주 CSS → 5·6주 JS와 DOM
→ 7·10주 폼과 목록 → 11주 저장 → 12주 fetch → 13주 점검
```

`my-web`과 `web-final` 두 저장소는 지우지 않습니다.
방학에 이어서 할 것은 README에 적어 둔 "어려움과 해결" 세 줄입니다.
