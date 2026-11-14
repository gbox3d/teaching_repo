---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 15주차"
footer: "Final practical exam · REST"
---

# 기말 개인 실기

1~14주 문제은행에서 연습하고 같은 문제를 다른 값으로 푼다.
12~14주: REST GET · POST · PATCH · DELETE

14주 레포트 검사는 없다. 레포트는 별도 공지를 따른다.

---

# 1일차 · 0–5분 — 문제은행 구조

A 화면 · B DOM · C 폼·목록 · D 브라우저 저장 · E REST

[문제은행](examples/README.md)은 13문항이다.
시험은 영역마다 한 문제씩 다섯 문제다.
POST 문항은 C 또는 E 한 곳에만 낸다.

---

# 1일차 · 5–10분 — 문항 읽기

시작 파일 → 할 일 → 확인할 것 → 이 문제의 값

화면과 보조 코드는 제공한다. TODO에 배운 요청을 작성한다.
[GET 문항](examples/w12_rest_get/README.md)
[POST 문항](examples/w13_rest_post/README.md)
[수정·삭제 문항](examples/w14_rest_edit/README.md)

---

# 1일차 · 10–15분 — 서버 준비 확인

강의자가 API 주소·공개 키·개인별 방명록을 준비한다.
학생은 설정 파일의 공개값만 바꾼다.

편집 키는 실행 화면에만 입력한다.
localhost는 현재 PC다. Pages에는 공용 HTTPS API가 필요하다.
[API 준비 안내](../../tools/guestbook-api/README.md)

---

# 1일차 · 15–20분 — 응답과 재조회

GET: 배열을 화면에 표시
POST: 201 뒤 GET으로 저장 확인
PATCH: 변경 배열과 GET의 수정값 확인
DELETE: 204 뒤 GET으로 글이 없는지 확인

204에 response.json()을 호출하지 않는다.

---

# 1일차 · 20–25분 — 제공 코드와 내 코드

`view.js`: 화면 그리기, 쓰기 문항의 재조회 제공
`app.js`: 이 문항의 요청 TODO
`config.example.js`: 공개 설정

[GET 시작 화면](examples/w12_rest_get/index.html) · [app.js](examples/w12_rest_get/app.js) · [view.js](examples/w12_rest_get/view.js)
[설정](examples/w12_rest_get/config.example.js) · [CSS](examples/w12_rest_get/styles.css)

---

# 1일차 · 25–30분 — 연습 연결

영역이 다른 세 문항을 고른다. REST 문항을 한 개 이상 포함한다.

**설명 합계: 5 + 5 + 5 + 5 + 5 + 5 = 30분**
[1일차 실습](lab.md#1일차-실습) · [따라하기](walkthrough.md)
[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

---

# 2일차 · 0–5분 — 배부 파일 확인

`web-week15/exam/`에 목차와 A~E 폴더가 있다.
자기 시험 방명록 번호와 초기 글을 확인한다.

연습 공간·다른 학생 공간을 시험에 사용하지 않는다.
편집 키를 소스에 적지 않는다.

---

# 2일차 · 5–10분 — 구현 배점

A 화면 3 · B DOM 3 · C 폼·목록 4
D 브라우저 저장 2 · E REST 3 = 구현 15점
URL 재현 3 · 구술 2 = 시연 5점

합계 20점 안. 확정 배점은 수업 공지를 따른다.
[채점표](rubric.md)

---

# 2일차 · 10–15분 — 실제 변경 확인

HTTP 상태 번호만으로 수정·삭제를 단정하지 않는다.
잘못된 키의 PATCH가 200 []일 수 있다.
잘못된 키의 DELETE가 204일 수 있다.

요청 후 같은 ID를 GET한다.
변경값 또는 빈 배열을 확인한다.

---

# 2일차 · 15–20분 — 서버 장애 처리

API가 응답하지 않으면 감독에게 알린다.
동일 계약과 초기 데이터의 대체 서버로 진행한다.
서버 장애 시간은 보정한다.

대체 환경이 없으면 REST 영역 평가를 보류한다.
서버 장애를 학생 코드 오류로 감점하지 않는다.

---

# 2일차 · 20–25분 — 제출과 구술

제출: 공개 URL · 저장소 URL · Commits 캡처

구술: 본인 코드 한 줄의 역할
키는 제출하지 않는다. 채점자가 별도 보관값을 쓴다.

POST·PATCH는 저장된 값을, DELETE는 대상의 부재를 확인한다.

---

# 2일차 · 25–30분 — 시험 연결

읽기 3분 → 구현 48분 → 올리기 5분 → 예비 4분
구술에 쓴 1분은 해당 학생 마감에서 보정한다.

**설명 합계: 5 + 5 + 5 + 5 + 5 + 5 = 30분**
[2일차 시험](lab.md#2일차-시험) · [따라하기](walkthrough.md)
[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)
