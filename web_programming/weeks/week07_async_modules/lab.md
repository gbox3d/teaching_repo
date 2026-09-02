# 7주차 실습 — 모듈화된 데이터 목록

## 준비와 규칙

1. [starter](examples/starter/)를 HTTP 서버에서 연다.
2. Network의 Disable cache를 켜고 Console을 함께 연다.
3. 네 데이터 source를 한 번씩 눌러 기준 동작을 관찰한다.
4. starter를 그대로 제출하지 말고 아래 변경을 작은 commit으로 남긴다.

## 1일차 60분 — module graph와 검색 통계

### 문제

데이터 요청·UI·흐름이 나뉜 starter에 순수 계산 module을 추가하고, 제목 검색과 category별 개수 표시를 구현한다. DOM module은 원본 전체 데이터의 보관 책임을 갖지 않는다.

### 먼저 그릴 구조

```text
main.js → api.js
main.js → ui.js
main.js → stats.js
```

`stats.js`는 다른 세 파일을 import하지 않는다.

### 시간 상자

| 시간 | 활동 | 검증 |
|---:|---|---|
| 0–8분 | 기존 graph 추적 | Network module 요청 |
| 8–20분 | `stats.js` 작성 | Console 입력/출력 |
| 20–35분 | 검색 form 추가 | 대소문자·공백 |
| 35–47분 | category 통계 UI | 합계 일치 |
| 47–55분 | import 오류 재현·복구 | 404 원인 기록 |
| 55–60분 | commit | 변경 목적 문장 |

### 필수 요구사항

- `stats.js`에 `filterByTitle(cards, keyword)`와 `countByCategory(cards)`를 named export한다.
- 두 함수는 DOM, fetch, 전역 상태를 사용하지 않는다.
- 빈 검색어는 전체 목록을 반환한다.
- 검색은 앞뒤 공백과 영문 대소문자 차이를 무시한다.
- 화면에 전체 개수, 현재 표시 개수, category별 개수를 구분해 보여 준다.
- `main.js`가 사용자 입력과 module 결과를 조정한다.

### 단계별 힌트

**힌트 1:** 계산 함수의 입력과 반환값 예를 먼저 작성한다.

```text
filterByTitle([{ title: "DOM" }], " do ") → 항목 1개 배열
```

**힌트 2:** 비교할 양쪽 문자열에 같은 정규화(`trim`, `toLowerCase`)를 적용한다.

**힌트 3:** category count는 빈 객체에서 시작하는 `reduce` 또는 `Map`으로 만든 뒤 새 DOM에 출력한다.

### 검증

- [ ] `dom`, ` DOM `, `DoM` 검색 결과가 같다.
- [ ] 존재하지 않는 검색어는 empty 검색 결과를 보여 준다.
- [ ] 표시 개수와 category 개수 합이 일치한다.
- [ ] 입력 배열을 함수 호출 전후 비교했을 때 바뀌지 않았다.
- [ ] import 파일명을 일부러 틀려 404를 확인하고 복구했다.

## 2일차 60분 — 네 결과 상태와 요청 경쟁

### 문제

starter의 로더를 확장하여 loading·empty·success·error가 서로 겹치지 않게 한다. HTTP 오류와 데이터 모양 오류를 구분해 개발자에게 기록하고, 사용자는 재시도할 수 있어야 한다. 연속 요청에서 가장 최근 선택만 화면에 남긴다.

### 시간 상자

| 시간 | 활동 | 검증 |
|---:|---|---|
| 0–10분 | 상태 표와 예상 작성 | source별 기대 결과 |
| 10–24분 | `response.ok`·shape 검사 | missing/wrong shape |
| 24–37분 | 네 UI 상태 | 이전 DOM 제거 |
| 37–47분 | 재시도 | 같은 source 재호출 |
| 47–55분 | request id 또는 abort | 느린 연속 요청 |
| 55–60분 | 증거·commit | Network + UI |

### 필수 요구사항

- 요청 직전 loading 문구와 `aria-busy="true"`를 설정한다.
- success일 때만 카드 목록을 표시한다.
- `[]`는 empty 안내이며 error로 취급하지 않는다.
- `response.ok`가 false이면 status code가 포함된 Error를 만든다.
- 응답 최상위가 배열이 아니면 `TypeError`를 만든다.
- 오류 시 사용자용 문구와 개발자용 `console.error`를 모두 남긴다.
- 다시 불러오기 동작이 새 요청을 시작한다.
- 오래된 요청 결과는 최신 화면을 덮지 않는다.

### 단계별 힌트

**힌트 1:** `renderState({ kind: "..." })` 한 함수만 DOM 상태를 결정하게 한다.

**힌트 2:** 요청 시작 때 증가한 숫자를 지역 변수에 저장하고, 응답 시 현재 숫자와 비교한다.

**힌트 3:** `finally`에서 버튼을 무조건 활성화하면 오래된 요청이 최신 요청 도중 버튼을 풀 수 있다. “현재 요청인가?” 조건을 함께 확인한다.

### 상태 검증표

| source | Network/파싱 관찰 | 화면 |
|---|---|---|
| `cards.json` | 200, 배열 | 카드 3개 |
| `empty.json` | 200, 빈 배열 | empty 안내 |
| `wrong-shape.json` | 200, 객체 | 형식 error |
| `missing.json` | 404 | HTTP error |

- [ ] loading 중 이전 카드와 이전 오류가 보이지 않는다.
- [ ] 네 상태 모두 재시도 뒤 정상 상태로 돌아올 수 있다.
- [ ] 연속 선택 후 마지막 source의 결과만 남는다.
- [ ] Console 오류 문구만으로 실패 단계를 구분할 수 있다.

## 제출 증거

- module graph 이미지 또는 Markdown
- 1일차·2일차 commit id
- Network에 보이는 module 요청과 JSON 요청
- success와 최소 두 실패/경계 상태 캡처
- “404와 네트워크 단절의 차이” 한 문장

## 확장 주제

1. `AbortController`로 이전 요청을 실제 취소하고 `AbortError`는 사용자 오류에서 제외한다.
2. 500ms debounce 검색을 구현하고 timer 경쟁을 설명한다.
3. schema validator 없이 필수 field를 검사하고 제외/전체 실패 정책을 비교한다.
4. URL query string에 source와 keyword를 반영해 새로고침 상태를 복원한다.
5. 동일 URL 응답을 메모리 cache하고 stale 데이터 갱신 전략을 토론한다.
