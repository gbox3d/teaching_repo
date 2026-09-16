# 중간 개인 실기 구조

이 문서는 공개 가능한 공통 구조다. 실제 시험 문항과 학생별 정보는 비공개로 관리한다.
배점은 강의계획 비중 재배분 승인 전까지 **안**이다.

## 평가 범위

범위는 2~7주다. 아래 표 밖의 것은 출제하지 않는다.

| 영역 | 확인하는 것 | 배운 주 |
|---|---|---|
| Git·Pages | `add → commit → push`, 공개 주소에서 열림, commit 2개 이상 | 2주 |
| HTML | `header`·`nav`·`main`·`footer`, 제목·문단, `ul`·`li`, `table`·`tr`·`th`·`td`, `form`·`label for`·`input`·`button` | 3주 |
| CSS | 태그·`.class` 선택자, 색·글꼴, `padding`·`margin`·`border`, `display: flex`·`gap`, `@media (max-width: 600px)` | 4주 |
| JavaScript | `const`·`let`, 템플릿 문자열, `if`, `function` | 5주 |
| DOM | `document.querySelector('#id')`, `textContent`, `addEventListener('click', …)`, `classList` | 6주 |
| 폼 | `addEventListener('submit', …)`, `event.preventDefault()`, `input.value`, `trim()`, 빈값 안내, `focus()` | 7주 |

**출제하지 않는 것**: 배열로 목록 그리기(10주), `localStorage`(11주), `fetch`·JSON(12주), ES Module·`import`/`export`, 외부 라이브러리·CDN, 서버·데이터베이스.

## 1·2일차 운영

### 1일차 — 공개 리허설

- 30분: 범위·채점표, 제출 형식과 60분 배분, `my-web/exam/` 규칙, 허용 자료와 장애 대체.
- 60분: 공개 리허설 `examples/rehearsal_starter`의 문제 네 개를 풀고 `examples/rehearsal_solution`으로 스스로 맞춰 본다.
- 1일차에 반드시 끝내는 것: **새 저장소 만들기 → push → Pages 켜기**. 공용 PC의 자격 증명 충돌도 이날 겪고 끝낸다.
- 1일차 결과는 점수에 넣지 않는다.

### 2일차 — 본시험

- 30분: 절차·좌석, "저장 후 새로고침해서 보이는 것이 제출본", 장애 대체, starter를 `exam/`에 복사해 실행 확인.
- 60분: 본시험. 배분은 **0–5 읽기 · 5–15 HTML · 15–25 CSS · 25–50 DOM/폼 · 50–55 push · 55–60 예비**.
- 예비 5분은 Pages 반영(1~3분)과 자격 증명 재로그인을 흡수한다.

작업 폴더는 `my-web/exam/`이다. 시험 중에 저장소 생성·브라우저 로그인·Pages 켜기가 없다.
기관 시험 시간표가 다르면 총 평가 시간과 안내 시간을 나누어 미리 공지한다.

## 시험 패킷 (비공개 준비물)

1. 문제지 1장: 요구 사항 네 개와 각각의 완료 조건
2. 배포용 starter 세 파일(리허설과 같은 구조, 내용만 다름)
3. 제출 경로·파일명·마감 시각
4. 허용 자료와 도구 범위 공지문
5. 장애 발생 시 대체 제출 절차와 기록 양식
6. 채점표 20점과 판정 예시

## 학생 산출물

- `my-web/exam/index.html`·`styles.css`·`app.js`
- 공개 URL `https://<아이디>.github.io/my-web/exam/`
- 저장소 URL `https://github.com/<아이디>/my-web`
- 마지막 commit SHA (`git log -1 --oneline`)
- 완성 화면과 주소창이 함께 보이는 캡처 1장

## 시작 전 감독 체크

- 모든 PC에서 `exam/index.html`이 더블클릭으로 열리고 Console에 빨간 줄이 없다.
- 각자 `git pull`이 끝나 `my-web`이 최신이다.
- 앞 사람의 GitHub 로그인이 남아 있지 않다(자격 증명 삭제 확인).
- starter에 답안이나 이전 학생의 파일이 없다.
- 파일 이름이 모두 소문자다. 공개 주소는 대소문자를 구분한다.
- 장애 기록 시각과 대체 제출 창구가 준비됐다.

## 공정성

- 문제 문장의 뜻, 파일 위치, 제출 방법, 환경 장애는 모든 학생에게 같은 수준으로 안내한다.
- 구현 방법과 코드가 맞는지는 알려 주지 않는다.
- 추가 시간·대체 평가는 대학 규정과 공식 기록을 따른다.
- 학생 코드·점수·개인정보는 공개 저장소에 올리지 않는다.

## 공개 저장소에 두지 않는 것

- 본시험 문제지의 문구와 요구 값
- 본시험 답안과 부분 답안
- 수험생 명단, 제출 URL, 점수와 이의 신청 기록
