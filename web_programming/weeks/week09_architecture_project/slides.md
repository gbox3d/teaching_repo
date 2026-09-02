---
marp: true
theme: default
paginate: true
header: 웹프로그래밍
footer: 9주차 · 1차 과제와 풀스택 설계
---

# 정적 페이지에서 시스템으로

## 1일차: 책임과 경계를 그리기

질문: **이 기능은 어디에서 실행되어야 하는가?**

---

## 사용자가 보는 하나의 앱

```text
GitHub Pages
  ├─ HTML/CSS/JS
  ├─ image/JSON
  └─ browser state
          │
          ├─ Supabase Data API
          └─ 선택: server/Edge Function
```

하나의 화면 뒤에 실행 위치와 권한이 다른 구성요소가 있다.

---

## 먼저 책임을 문장으로

| 위치 | 잘하는 일 |
|---|---|
| 정적 asset | 자주 바뀌지 않는 공개 콘텐츠 |
| browser | 입력·표현·사용자 상호작용 |
| Supabase | 영속 데이터·인증·행 권한 |
| server API | 비밀키, 신뢰 계산, 호출 통합 |

“가능하다”보다 “누가 신뢰할 수 있는가”를 묻는다.

---

## 정적 JSON이면 충분한 경우

- 모든 사용자에게 같은 읽기 전용 데이터
- 배포 때 함께 갱신해도 됨
- 비밀값이나 개인 정보가 없음
- 복잡한 server 계산이 없음

```js
const cards = await fetch("./data/cards.json");
```

작은 요구에 backend를 추가하면 운영 지점만 늘어난다.

---

## Supabase가 필요한 경우

- 사용 중 데이터가 생성·수정됨
- 여러 기기/사용자가 같은 원본을 공유
- 로그인 사용자와 소유권을 연결
- 관계·검색·정렬을 DB에서 처리

브라우저 직접 호출은 **publishable key + 최소 권한 + RLS**가 전제다.

---

## server API가 필요한 경우

- secret key를 사용해야 함
- 브라우저가 조작하면 안 되는 계산
- 여러 외부 호출을 한 계약으로 묶음
- rate limit·감사·추가 검증이 필요

server는 “있으면 더 풀스택”인 장식이 아니라 신뢰 경계를 옮기는 도구다.

---

## 데이터 흐름에 실패를 넣는다

```text
click
 → loading
 → request
 → success / empty / unauthorized / not-found / network error
 → retry or next action
```

happy path 화살표만 있는 diagram은 구현 위험을 숨긴다.

---

## entity를 기능보다 먼저 확인

```text
Post
- id
- owner_id
- title
- body
- created_at
```

질문:

- 누가 만들고 읽고 바꾸고 지우는가?
- 공개와 개인 field는 무엇인가?
- 제목 중복이 허용되는가?
- 삭제 때 관계 데이터는 어떻게 되는가?

---

## 1일차 실습 결과

1. 문제와 핵심 사용자 한 문장
2. 세 개의 사용자 이야기
3. entity/관계/owner 표
4. architecture/data-flow diagram
5. 여섯 UI 상태표

기술 이름보다 검증 가능한 흐름이 먼저다.

---

# 2일차: 작은 범위를 실행 가능한 골격으로

프로젝트 계획은 “할 일 목록”이 아니라 **완료를 판정하는 계약**이다.

---

## scope를 세 층으로

| 층 | 의미 |
|---|---|
| Must | 학습 성과를 증명하는 최소 기능 |
| Should | Must 뒤에 가치가 큰 기능 |
| Could | 시간이 남을 때만 실험 |

Must 예: 로그인, owner CRUD, 관계 기능 하나, 상태별 UI, 공개 배포.

---

## walking skeleton

가장 얇지만 처음부터 끝까지 연결된 경로:

```text
페이지 열기
 → mock 데이터 읽기
 → 카드 목록
 → empty/error 전환
 → 공개 URL 확인
```

다음 주에는 data source만 Supabase로 교체할 수 있어야 한다.

---

## UI와 data source 사이 계약

```js
export async function listPosts() {
  return [
    { id: "p1", title: "첫 글", ownerId: "u1" }
  ];
}
```

UI는 JSON 파일인지 Supabase인지 몰라도 된다.

계약에는 성공값과 실패도 포함한다.

---

## 상태표는 구현 목록

| 상태 | 발생 조건 | 화면 | 회복 |
|---|---|---|---|
| loading | 요청 중 | 진행 안내 | 대기 |
| empty | 0행 | 첫 작성 안내 | 작성 |
| validation | 잘못된 입력 | field 안내 | 수정 |
| unauthorized | 세션/권한 없음 | 로그인 안내 | 로그인 |
| not-found | 대상 없음 | 목록 이동 | 목록 |
| network | 연결 실패 | 오류 | 재시도 |

---

## 보안 경계 표시

```text
공개 가능: URL, publishable key, 공개 asset
공개 금지: password, secret key, service role, private token
```

RLS 없는 공개 schema table을 browser에 연결하지 않는다.

이번 주 mock에는 실제 key를 넣지 않는다.

---

## 증거 중심 계획

각 Must 요구사항에 증거를 붙인다.

```text
요구: owner만 수정
증거: 본인 성공 + 타인 거부 Network/화면
```

구현 완료와 검증 완료를 분리한다.

---

## 1차 과제 산출물

- repository와 실행 URL
- architecture/data-flow diagram
- scope·사용자 이야기·상태표
- 실행 가능한 walking skeleton
- 3분 발표
- 간결한 설계 보고서

발표 5점 + 보고서 5점

---

## 오늘의 결정 질문

1. 핵심 사용자는 누구인가?
2. Must 한 줄은 무엇인가?
3. 영속화할 entity는 무엇인가?
4. 관계 기능 하나는 무엇인가?
5. 어떤 데이터가 public인가?
6. 가장 먼저 검증할 위험은 무엇인가?

작고 검증 가능한 답이면 구현으로 이동한다.
