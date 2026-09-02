---
marp: true
theme: default
paginate: true
title: 11주차 ContentProvider와 센서 이력 경계
---

# 11주차

## ContentProvider와 센서 이력 경계

저장 방식이 아니라 **접근 계약**을 설계한다.

---

# 이번 주 완료 조건

- collection/item URI 구분
- fake 센서 이력 조회
- 0·1·N건과 오류 상태 표현
- 비동기 조회와 생명주기 인식 수집
- 최소 노출 정책 설명

---

<!-- _class: lead -->
# 1일차 — Provider 계약 읽기

30분 설명·라이브 시연

---

## 0–5분 — 왜 저장소를 직접 열지 않는가

두 앱이 같은 DB 파일 경로를 안다고 가정해 보자.

- 스키마 변경에 모두 깨진다.
- 접근 범위를 통제하기 어렵다.
- 호출자가 저장 구현과 결합된다.

Provider는 저장소 앞에 **명명된 CRUD 계약**을 둔다.

---

## 5–10분 — 호출 경로

```text
UI / ViewModel
      │ query(content://...)
      ▼
ContentResolver
      │ IPC 또는 앱 내부 호출
      ▼
ContentProvider ──▶ private repository
      │
      └──▶ Cursor / 오류
```

호출자는 DB 파일이 아니라 URI와 열 계약을 안다.

---

## 10–15분 — content URI 해부

```text
content://edu.example.smartio.history/readings/42
└scheme─┘ └────────authority────────┘ └path┘ └id┘
```

| URI | 의미 |
|---|---|
| `/readings` | 이력 collection |
| `/readings/42` | ID 42인 한 항목 |
| `/unknown` | 계약 밖 → 명시적 오류 |

---

## 15–20분 — Resolver와 Provider의 책임

~~~kotlin
val cursor = contentResolver.query(
    readingsUri, projection, selection, selectionArgs, sortOrder
)
~~~

| 호출 측 | 경계 | 제공 측 |
|---|---|---|
| 필요한 열 선택 | URI·MIME·열 이름 | `UriMatcher`로 대상 판별 |
| query 인자 전달 | 읽기/쓰기 정책 | `query()`에서 저장소 질의 |
| UI 상태 변환 | Cursor/예외 | `getType()`으로 MIME 계약 |

UI가 Provider 구현 클래스나 DB 객체를 직접 잡지 않는다.

---

## 20–25분 — Provider 쪽 분기 시연

~~~kotlin
when (uriMatcher.match(uri)) {
    READINGS -> queryCollection(/* projection, selection, ... */)
    READING_ID -> queryItem(uri.lastPathSegment)
    else -> error("unsupported URI")
}

override fun getType(uri: Uri): String = when (uriMatcher.match(uri)) {
    READINGS -> DIR_MIME
    READING_ID -> ITEM_MIME
    else -> error("unsupported URI")
}
~~~

- 의사코드이며 상수·MIME 값은 실제 starter 계약을 따른다.
- 느릴 수 있는 Provider query는 메인 스레드 밖에서 호출한다.

---

## 25–30분 — 예측 후 실습 인계

예측 카드:

1. 없는 ID를 조회하면 null, 빈 목록, 오류 중 무엇인가?
2. 알 수 없는 path를 조용히 빈 결과로 처리하면 무엇이 숨겨지는가?
3. 앱 내부 전용이면 반드시 Provider가 필요한가?

실습 증거: URI 분류표 + 정상/경계/실패 캡처

---

<!-- _class: lead -->
# 2일차 — 조회·권한·오류 상태

30분 설명·라이브 시연

---

## 0–5분 — 1일차 오류 회고

- collection과 item 결과 타입을 같다고 가정함
- 열 이름을 UI 문자열에 흩뿌림
- 빈 결과와 query 실패를 같은 화면으로 표시함

오늘 질문: **누가 무엇을 얼마나 읽게 할 것인가?**

---

## 5–10분 — Query는 계약이다

| 요소 | 질문 | 센서 이력 예 |
|---|---|---|
| projection | 어떤 열? | 시각·채널·값 |
| selection | 어떤 행? | 선택 채널 이후 기록 |
| args | 값은 어떻게 전달? | 사용자 입력을 분리 |
| sort | 어떤 순서? | 최신 기록 우선 |

문자열 연결 대신 제공 helper의 인자 계약을 사용한다.

Provider는 `query/insert/update/delete` CRUD 진입점을 제공할 수 있다. 이번 센서 이력 계약은 외부 **읽기 전용**으로 제한하고 쓰기 진입점은 허용하지 않는다.

---

## 10–15분 — UI 스레드를 막지 않는다

```text
XML View event
   → ViewModel coroutine
      → history client query
         → UiState(Loading / Data / Empty / NotFound / Error)
```

화면에서는 lifecycle-aware 방식으로 상태를 수집한다.

---

## 15–20분 — 공유와 노출은 별개다

- 내부 저장소는 기본적으로 앱 내부 경계에 둔다.
- 다른 앱에 제공할 때 exported 여부와 read/write 정책을 설계한다.
- 센서 이력 전체 쓰기를 외부에 열 필요가 있는지 먼저 질문한다.
- 권한을 안다는 것과 사용자가 복구 가능한 UX를 갖는 것은 다르다.

---

## 20–25분 — 실패를 상태로 바꾸기

~~~kotlin
sealed interface HistoryUiState {
    data object Loading : HistoryUiState
    data class Data(val rows: List<SensorRow>) : HistoryUiState
    data object Empty : HistoryUiState
    data class Error(val recovery: String) : HistoryUiState
}
~~~

예외 메시지를 그대로 노출하지 않고 복구 행동을 제시한다.

---

## 25–30분 — 실습 인계

반드시 확인할 세 경로:

- 정상: 최신 이력 여러 건
- 경계: 결과 0건, 존재하지 않는 item ID
- 실패: 알 수 없는 URI 또는 읽기 거부

마지막 5분에는 계약표와 증거를 제출한다.

---

# 공식 자료

- Android Developers: Content provider basics
- Android Developers: Create a content provider
- Android Developers: Lifecycle-aware coroutines for Views
