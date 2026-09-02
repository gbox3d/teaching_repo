# 13주차 실습 — 확인 가능한 BLE 출력 제어

## 공통 시나리오

사용자가 XML View의 출력 스위치를 누르면 앱이 의미 기반 `OutputCommand`를 만들고, 제공 BLE 추상화가 fake 또는 real transport로 전달한다. UI는 `요청됨`, `확인됨`, `실패/불확실`을 구분한다.

## 실행 전 예측

| 조건 | write 호출 여부 | 예상 출력 UI | 복구 |
|---|---|---|---|
| Ready + valid command |  |  |  |
| Discovering + tap |  |  |  |
| Sending 중 연속 tap |  |  |  |
| Uncertain 중 새 tap |  |  |  |
| timeout |  |  |  |
| write 중 disconnect |  |  |  |

## 1일차 60분 — fake 명령과 reducer

### 시간표 — 합계 60분

- 0~10분: 명령 경로·Ready gate·예측표 작성
- 10~25분: `OutputCommand` validation과 출력 UiState 연결
- 25~40분: fake confirmed 경로와 중복 탭 경계 구현
- 40~55분: invalid channel·timeout·disconnect 실패 주입
- 55~60분: 증거 저장, commit, 회고

### 필수 구현

1. View는 raw payload가 아닌 `OutputChannel`과 `OutputLevel`을 전달한다.
2. use case에서 `Ready`, 유효 채널, in-flight 여부와 `RecoveryGate`를 검사한다.
3. `Sending`, `Confirmed`, `Failed`, `Uncertain`을 별도 상태로 표현한다.
4. 실패 시 이전 confirmed 값과 현재 desired 값을 구분하고, 동기화 완료 전 새 write를 차단한다.

### 검증 매트릭스

| 종류 | 주입 | 기대 관찰 | 데이터/상태 확인 |
|---|---|---|---|
| 정상 | Ready + valid HIGH | Sending → Confirmed(HIGH) | request trace 1개 |
| 경계 | Sending 중 3회 탭 | 중복 요청 없음/정책 표시 | transport count 확인 |
| 경계 | Uncertain 중 새 명령 | `BUSY` + 동기화 필요 표시 | transport count 증가 없음 |
| 경계 | 같은 confirmed level | 제공 정책대로 no-op 또는 1회 요청 | 정책 문서와 일치 |
| 실패 | invalid channel | transport 전 validation error | write count 0 |
| 실패 | timeout 또는 link lost | Uncertain/Disconnected | Ready 버튼 비활성 |

<details>
<summary>힌트 1 — 두 상태를 분리한다</summary>

연결 `LinkState`와 출력 `OutputUiState`를 한 enum에 모두 넣지 않는다. 출력 상태는 링크 상태의 영향을 받지만 서로 다른 질문에 답한다.

</details>

<details>
<summary>힌트 2 — 중복 탭</summary>

`Sending` 동안 버튼을 비활성화하고 use case에서도 in-flight를 검사한다. UI만 막는 것은 테스트 우회를 막지 못한다.

</details>

<details>
<summary>힌트 3 — timeout</summary>

```text
Sending(desired=HIGH) + Timeout
  → Uncertain(desired=HIGH, lastConfirmed=LOW)
  + RecoveryGate.RECONCILE_REQUIRED
```

`Uncertain`의 인자는 desired와 lastConfirmed 두 개뿐이다. 복구 행동은 별도 `RecoveryGate`로 표시하고, `RECONCILE_REQUIRED/RECONCILING` 동안 `setOutput`은 `BUSY`를 반환한다. 프로토콜에 상태 읽기 계약이 고정되기 전에는 임의 read UUID를 만들지 않으며, 제공 동기화가 `Confirmed(actual) + CLEAR`로 끝난 뒤에만 새 명령을 허용한다.

</details>

## 2일차 60분 — real 출력과 실패 복구

### 시간표 — 합계 60분

- 0~10분: fake 회귀·보드 라벨·Ready·프로토콜 확정 상태 확인
- 10~25분: real transport에서 출력 1회 요청과 로그 수집
- 25~40분: 반대 level 요청, UI·event·물리 관찰 상관관계 작성
- 40~55분: 요청 중 disconnect 또는 제공 failure mode 주입·복구
- 55~60분: 개인정보 마스킹, commit SHA, 제출 묶음 확인

### 필수 구현

1. real transport에서 `Ready`가 확인되기 전 버튼을 누르지 않는다.
2. 강의자 제공 출력 채널만 선택한다. 값이 미확정이면 실물 write를 중단하고 `TBD`로 보고한다.
3. 요청/transport 결과/장치 확인 가능 범위를 정확히 표현한다.
4. 실패 후 reconnect와 상태 동기화가 끝나야 다시 제어한다.

### 검증 매트릭스

| 종류 | 절차 | 기대 관찰 | 증거 |
|---|---|---|---|
| 정상 | Ready → HIGH | UI + event + 물리 변화 | 시간순 3열 기록 |
| 정상 | Ready → LOW | 동일 경로 재현 | 요청 수·최종 상태 |
| 경계 | 이미 같은 level 요청 | pinned 정책과 일치 | no-op/요청 여부 기록 |
| 실패 | write 중 보드 off | Disconnected + Uncertain | stale Confirmed 금지 |
| 복구 | reconnect/discover | Ready 뒤 상태 조정 | 새 session trace |

<details>
<summary>힌트 1 — 실물 실패 분리</summary>

fake가 통과하는지 확인한 뒤 link state, contract match, validation, write event, 물리 출력 순서로 좁힌다.

</details>

<details>
<summary>힌트 2 — 확인의 정확한 표현</summary>

프로토콜이 transport completion만 제공하면 “write 요청 처리 완료”라고 쓰고, 장치 상태 응답/읽기가 있을 때만 “출력 상태 확인”이라고 쓴다.

</details>

<details>
<summary>힌트 3 — 재시도</summary>

연결이 Ready인지 재확인하고, 가능한 경우 상태 동기화 뒤 사용자의 재시도 버튼으로 한 번 요청한다.

</details>

## 확장 문제

- 두 출력 채널이 있을 때 동시 요청을 serialize할지 병렬화할지 계약을 제안한다.
- pending 명령을 화면 회전 뒤 어떻게 표현할지 설계한다.
- idempotent 명령과 toggle 명령의 재시도 위험을 비교한다.

## 제출

- 사전 예측표와 명령 경로 그림
- fake 정상·경계·실패 trace
- real 정상과 실패/복구의 UI·event·물리 증거
- 확인 가능 범위를 정확히 쓴 5문장 설명
- `TBD` 프로토콜 계약표
- 개인 commit SHA와 3문장 회고
