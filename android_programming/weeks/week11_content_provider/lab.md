# 11주차 실습 — 센서 이력 접근 계약

## 공통 시나리오

`Smart I/O Controller`의 fake 센서 이력을 목록으로 조회한다. UI는 저장소를 직접 알지 않고 수업용 `HistoryClient` 계약만 사용한다. 예제는 완성 Gradle 프로젝트가 아니며 실제 starter의 패키지·함수명을 따른다.

## 사전 예측

실행 전에 각 결과를 `Data / Empty / NotFound / Error` 중 하나로 적는다.

| 입력 | 예측 | 실행 결과 | 모델 수정 |
|---|---|---|---|
| `/readings`에 3행 |  |  |  |
| 존재하지 않는 item ID |  |  |  |
| `/unknown` path |  |  |  |
| 읽기 권한 거부 |  |  |  |

### 실습 공개 계약

[예제 계약](examples/README.md)의 타입을 두 실습일 모두 그대로 사용한다.

```text
HistoryTarget = Collection | Item(id) | Unknown(rawUri)
HistoryResult = Rows(rows) | NotFound | Failed(kind)
```

- `Collection` 0건: `Rows(emptyList())` → `Empty`
- 없는 `Item`: `NotFound` → `NotFound`
- 계약 밖 URI: `Unknown(rawUri)` → `Failed(UNSUPPORTED_URI)` → `Error`

## 1일차 60분 — URI와 fake resolver

### 시간표 — 합계 60분

- 0~10분: starter 실행, 호출 경로와 예상 상태 기록
- 10~25분: collection/item URI 분류 구현
- 25~40분: fake client 조회와 0·1·N건 UI 연결
- 40~55분: 알 수 없는 URI·없는 ID 실패/경계 주입
- 55~60분: 증거 캡처, commit, 3문장 회고

### 과제

1. UI 이벤트가 ViewModel을 거쳐 `HistoryClient`에 도달하도록 연결한다.
2. collection은 `Rows(0..N)`, item은 `Rows(1)` 또는 `NotFound`로 표현한다.
3. collection 0건의 `Empty`, 없는 item의 `NotFound`, 알 수 없는 URI의 `Error`를 구분한다.
4. 열 이름과 URI 문자열을 한 계약 위치에 모은다.

### 검증 매트릭스

| 종류 | 입력 | 기대 관찰 | 통과 증거 |
|---|---|---|---|
| 정상 | collection, 3행 | 최신순 3행 | 화면 + 경계 로그 |
| 경계 | collection, 0행 | Empty 안내 | 빈 화면이 아닌 명시 문구 |
| 경계 | `Item(404)` | `NotFound` | `Empty`로 합치거나 다른 행을 대신 표시하지 않음 |
| 실패 | `Unknown(rawUri)` | `Failed(UNSUPPORTED_URI)` | `Error` + 수정 안내 |

<details>
<summary>힌트 1 — 어디서 시작할까?</summary>

먼저 URI를 `HistoryTarget.Collection`, `HistoryTarget.Item(id)`, `HistoryTarget.Unknown(rawUri)` 세 값으로만 분류한다. 저장소 조회는 그 다음이다.

</details>

<details>
<summary>힌트 2 — 상태가 섞일 때</summary>

`List<SensorRow>` 하나로 모든 결과를 표현하지 말고 `Loading`, `Data`, `Empty`, `NotFound`, `Error`를 분리한다.

</details>

<details>
<summary>힌트 3 — 의사코드 뼈대</summary>

```kotlin
when (val target = parse(uri)) {
    HistoryTarget.Collection -> HistoryResult.Rows(source.all())
    is HistoryTarget.Item -> source.byId(target.id)
        ?.let { HistoryResult.Rows(listOf(it)) }
        ?: HistoryResult.NotFound
    is HistoryTarget.Unknown ->
        HistoryResult.Failed(HistoryFailure.UNSUPPORTED_URI)
}
```

실제 starter의 adapter는 이 공개 의미를 보존한다. `NotFound`나 `UNSUPPORTED_URI`를 빈 `Rows`로 바꾸지 않는다.

</details>

## 2일차 60분 — 필터·정렬·접근 실패

### 시간표 — 합계 60분

- 0~10분: 전날 결과 재실행, query 계약표 작성
- 10~25분: 채널 필터·projection·최신순 정렬 연결
- 25~40분: coroutine 조회와 lifecycle-aware UI 수집 확인
- 40~55분: 빈 결과·읽기 거부·지연 실패 검증
- 55~60분: 최종 체크리스트, commit SHA, 제출

### 과제

1. 선택 채널과 시간 조건을 제공된 query 인자로 전달한다.
2. 목록에 필요한 열만 projection에 포함한다.
3. query 동안 `Loading`, 성공 0건은 `Empty`, 접근 실패는 `Error`로 표시한다.
4. 화면을 나갔다 돌아와도 사라진 View를 직접 갱신하지 않게 한다.

### 검증 매트릭스

| 종류 | 조작 | 기대 관찰 | 데이터 보존 확인 |
|---|---|---|---|
| 정상 | 알려진 채널 선택 | 해당 이력만 최신순 표시 | 원본 fake 데이터 불변 |
| 경계 | 일치 기록 없는 조건 | Empty + 조건 해제 행동 | 이전 결과를 새 결과처럼 표시하지 않음 |
| 실패 | read denied 주입 | 권한/설정 안내 | 원본 데이터 불변 |
| 실패 | 지연 중 화면 이탈 | crash·stale View 갱신 없음 | 복귀 후 현재 상태 표시 |

<details>
<summary>힌트 1 — query 계약표</summary>

`화면 요구 → projection → selection/args → sort → UiState` 순서로 한 행씩 적는다.

</details>

<details>
<summary>힌트 2 — 비동기 위치</summary>

ViewModel에서 coroutine을 시작하고 결과를 상태로 내보낸다. repository에 Activity나 View 참조를 넘기지 않는다.

</details>

<details>
<summary>힌트 3 — 실패 문구</summary>

원시 예외 문자열 대신 `무슨 일이 일어났는지 + 사용자가 할 수 있는 행동` 두 부분을 작성한다.

</details>

## 확장 문제

- collection에 읽기 전용 pagination 계약을 제안한다.
- 외부 앱에 공유할 열과 숨길 열을 분류하고 근거를 쓴다.
- fake source를 실제 Provider client로 교체할 때 유지되어야 할 테스트를 적는다.

## 제출

- 예측·실행·모델 수정표
- 정상 1건, 경계 2건, 실패 1건의 캡처 또는 테스트 로그
- URI/query 계약표
- 호출 경로 그림
- 개인 commit SHA와 3문장 회고
