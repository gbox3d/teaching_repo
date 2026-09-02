---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍(Android)
footer: 8주차 · 중간 개인 실기
---

# 중간 개인 실기

## 1일차 · [0–4분] 공개 범위와 시험 보안

```text
공개: 역량·구조·연습·rubric
비공개: 실제 문항·고유 값·정답·fixture·hidden test·학생 데이터
```

질문: **기능을 만들었다는 주장과 재현 가능한 증거의 차이는 무엇인가?**

---

## 1일차 · [4–9분] 평가 역량 지도

| 영역 | 관찰 가능한 행동 |
|---|---|
| XML UI | 의미·상태·입력·접근성 |
| lifecycle | 회전/복귀 뒤 상태와 View 안전성 |
| coroutine | 응답성·취소·오류 |
| Flow | 단방향 상태와 lifecycle-aware collect |
| 검증 | normal/boundary/failure 증거 |

실제 문항은 이 표에서 직접 유추할 수 없는 별도 비공개 자료다.

---

## 1일차 · [9–14분] 요구사항을 관찰로 바꾸기

```text
“연결 상태 표시”
 → 어떤 상태?
 → 어떤 event가 전이시킴?
 → 어떤 View가 바뀜?
 → 어떤 로그/화면으로 확인?
```

명사에는 상태, 동사에는 event, 조건에는 testcase를 표시한다.

---

## 1일차 · [14–20분] 최소 구현 순서

```text
실행 기준선
 → UI binding
 → UiState
 → event/ViewModel
 → fake async
 → lifecycle collect
 → 경계/실패
 → 제출 검증
```

한 번에 완성하려 하지 말고 실행 가능한 checkpoint를 유지한다.

---

## 1일차 · [20–25분] 시간 예산

| 구간 | 권장 행동 |
|---:|---|
| 초반 | 읽기·분해·기준 실행 |
| 중반 | 정상 경로 최소 완성 |
| 후반 | 경계·실패·회전 검증 |
| 마지막 | clean build/실행·제출 대조 |

구체 분 배분은 실제 시험 공지의 총 시간 `TBD`에 맞춘다.

---

## 1일차 · [25–30분] 공개 연습 진입

예측부터 기록:

- 연속 event의 마지막 의도
- 회전 뒤 최신 상태
- STOPPED 중 render 횟수
- fake 실패 뒤 복구 UI

**실습:** 실제 시험과 다른 중립 상태 패널로 통합 흐름을 연습한다.

---

# 제출·진단·설명

## 2일차 · [0–5분] 제출물은 실행 결과와 같아야 한다

```text
편집 파일 → 저장 → build/run → commit → 제출 파일 재확인
```

IDE 화면이 아니라 제출된 revision을 기준으로 검증한다.

---

## 2일차 · [5–10분] 오류 위치 좁히기

```text
build → launch → binding/event → ViewModel → coroutine → Flow → render
```

첫 실패 지점의 증거를 찾는다. 무작정 여러 파일을 동시에 바꾸지 않는다.

---

## 2일차 · [10–16분] lifecycle 검증

| 조작 | 기대 관찰 |
|---|---|
| 회전 | 상태 보존, View 재생성 |
| Home/복귀 | 숨은 View render 없음, 최신 상태 복원 |
| 뒤로가기 | View reference 정리 |

`repeatOnLifecycle(STARTED)`의 시작/취소 로그를 활용한다.

---

## 2일차 · [16–21분] 세 경로

```text
normal   : event → progress → success
boundary : empty/연속 event/회전
failure  : exception/timeout → 안내 → retry
```

성공 하나만으로 비동기 UI의 안정성을 증명할 수 없다.

---

## 2일차 · [21–26분] 1분 설명 구조

1. 상태 소유자
2. coroutine 수명과 취소
3. Flow 수집 경계
4. 재현한 실패와 복구

코드를 외우기보다 근거가 있는 선택을 설명한다.

---

## 2일차 · [26–30분] 최종 체크

- 지정 파일/이름/실행 대상
- warning보다 첫 error 확인
- 실제 제출본 재실행
- 개인정보·실제 장치 식별자 없음
- commit id와 증거 일치

실제 시험 문제와 답안은 이 공개 자료에 없다.
