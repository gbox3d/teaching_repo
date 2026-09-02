# 3주차 실습 — Activity 수명과 사용자 상태 분리하기

## 공통 규칙

- 예상 callback을 먼저 적되 실제 로그와 다르면 관찰값을 우선한다.
- callback마다 `super` 호출을 유지하고 같은 형식의 로그를 사용한다.
- `onDestroy()` 호출을 강제로 보장하거나 회전을 막는 방식으로 문제를 숨기지 않는다.
- Activity 간에는 가짜 장치명·별칭만 전달하며 실제 장치 식별 정보는 사용하지 않는다.

## 1일차 실습 — 회전으로 상태 소실을 재현하고 복원하기 (60분)

### 상황과 문제

사용자가 mock 출력 버튼을 세 번 누른 뒤 화면을 회전했더니 횟수가 0으로 돌아갔다. 어떤 Activity 객체와 callback이 관여했는지 로그로 증명하고 작은 UI 상태를 올바르게 복원하라.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 경로 예측 | 0–8분 | 8분 | 네 행동의 callback 예상 |
| 로그 계측 | 8–20분 | 12분 | 여섯 callback과 instance id 추가 |
| 시나리오 관찰 | 20–35분 | 15분 | 실행·Home·회전·Back 기록 |
| 상태 소실·복원 | 35–49분 | 14분 | 탭 횟수 저장·복원 |
| 실패·경계 확인 | 49–56분 | 7분 | 키 오류와 복원값 확인 |
| 검증·회고 | 56–60분 | 4분 | 책임 분류와 증거 정리 |
| **합계** |  | **60분** |  |

### 1. 실행 전 예측

| 시나리오 | 예상 callback 순서 | 같은 instance 예상? | 실제 로그 | 해석 |
|---|---|---|---|---|
| 최초 실행 |  |  |  |  |
| Home→복귀 |  |  |  |  |
| 세로→가로 회전 |  |  |  |  |
| Back 종료 |  |  |  |  |

### 2. callback 로그 계측

`onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy`에 다음 형식의 로그를 둔다.

```text
id=<관찰용 Activity instance id> event=<callback> taps=<현재 횟수>
```

요구사항:

- 같은 `LifecycleTrace` tag를 사용한다.
- 각 override에서 적절한 `super`를 호출한다.
- `onCreate`에서 `savedInstanceState == null` 여부도 기록한다.
- 실제 사용자나 기기 식별값을 로그에 넣지 않는다.

### 3. 네 시나리오 관찰

각 시나리오 전 Logcat에 구분 메시지를 남기거나 시간 기준을 기록한다. 앱을 정상 기준선으로 돌린 뒤 한 시나리오씩 실행한다.

관찰 질문:

1. 화면이 상호작용 가능한 시점은 어느 callback 뒤인가?
2. Home 복귀에서 instance id가 유지되는가?
3. 회전에서 이전 id와 새 id가 어떻게 보이는가?
4. Back 뒤 `onDestroy`가 보였더라도 모든 프로세스 종료에서 보장된다고 말할 수 있는가?

### 4. 상태 소실과 saved state 복원

1. 탭 횟수 3을 만든다.
2. 회전해 0으로 돌아가는 실패를 기록한다.
3. `onSaveInstanceState()`에 정수 하나를 저장한다.
4. `onCreate()`에서 같은 key로 복원한다.
5. `render()`를 호출해 화면에 복원값을 반영한다.
6. 다시 3회→회전 조건으로 검증한다.

### 5. 정상·경계·실패 확인

- **정상:** 최초 실행은 기본값 0이고 `savedInstanceState == null`이다.
- **경계:** 3회 클릭 후 연속 두 번 회전해도 3이 유지된다.
- **실패:** 저장 key와 복원 key를 별도 복사본에서 다르게 해 0으로 돌아감을 재현한 뒤 같은 key로 복구한다.
- **수명:** Home→복귀와 회전의 instance id 차이를 설명한다.

### 단계별 힌트

<details>
<summary>힌트 1 — callback 로그 순서가 섞여 보인다</summary>

현재 앱 process와 `LifecycleTrace` tag로 필터링하고 instance id별로 줄을 묶는다. 이전 실행 로그를 지운 뒤 시나리오 하나만 반복한다.
</details>

<details>
<summary>힌트 2 — 저장은 되는데 화면이 0이다</summary>

필드 복원 뒤 `render()`가 어떤 값을 읽는지 확인한다. View를 만들기 전 갱신하거나 복원 뒤 다시 0을 대입하지 않았는지도 순서대로 본다.
</details>

<details>
<summary>힌트 3 — Bundle에 enum이나 연결 객체를 넣고 싶다</summary>

이번 실습은 작은 정수만 저장한다. 연결 객체는 화면 복원 데이터가 아니며, enum은 필요한 최소 표현과 복원 정책을 먼저 설계해야 한다.
</details>

### 확장

mock 연결 enum의 이름을 문자열로 저장·복원하되 알 수 없는 문자열이면 `DISCONNECTED`로 돌아가게 한다. 왜 안전한 기본값을 택했는지 적는다.

### 1일차 제출 증거

- `day1-lifecycle.md`: 네 시나리오의 예상/실제 callback 표
- 상태 소실 전과 복원 후의 같은 회전 조건 증거
- saved state, ViewModel, 영구 저장소 책임 비교 3문장

## 2일차 실습 — 상세 Activity와 결과 계약 (60분)

### 상황과 문제

Main 화면에서 mock 장치를 선택해 상세 Activity를 열고 사용자가 별칭을 편집한다. 유효한 별칭만 Main으로 반영하며 공백, 취소, 입력 extra 누락에서는 앱이 종료되지 않고 기존 상태를 지켜야 한다.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 계약 예측 | 0–8분 | 8분 | 입력/결과/취소 표 작성 |
| Detail 화면 | 8–21분 | 13분 | Activity·XML·Manifest 선언 |
| Result 연결 | 21–36분 | 15분 | launcher, 저장 결과, render |
| 경계·실패 처리 | 36–49분 | 13분 | 공백·취소·extra 누락 |
| 회전 재검증 | 49–56분 | 7분 | Main alias 복원 확인 |
| 검증·제출 | 56–60분 | 4분 | 결과표와 코드 증거 |
| **합계** |  | **60분** |  |

### 1. 구현 전 계약표

| 입력/행동 | Detail 기대 | resultCode | Main 기대 |
|---|---|---|---|
| 정상 장치명, 유효 별칭 저장 |  |  |  |
| 정상 장치명, 공백 저장 |  |  |  |
| 정상 장치명, Back |  |  |  |
| 장치명 extra 누락 |  |  |  |

상수 이름을 먼저 정한다.

```kotlin
const val EXTRA_DEVICE_NAME = "device_name"
const val EXTRA_ALIAS = "device_alias"
```

### 2. `DeviceDetailActivity` 구현

요구사항:

1. Activity와 XML layout을 만들고 Manifest에 선언한다.
2. `intent.getStringExtra(EXTRA_DEVICE_NAME)`을 nullable로 받는다.
3. null 또는 공백이면 canceled 결과로 안전하게 종료한다.
4. 유효하면 장치명과 별칭 입력란을 보여 준다.
5. 저장 클릭 시 trim 결과가 빈 값이면 `EditText.error`를 표시하고 화면에 머문다.
6. 유효하면 `RESULT_OK`와 별칭 extra를 설정한 뒤 종료한다.

### 3. Main의 Activity Result API

- `registerForActivityResult(ActivityResultContracts.StartActivityForResult())`로 launcher를 등록한다.
- 상세 버튼에서 명시적 Intent를 만들어 `launch()`한다.
- `RESULT_OK`, nullable data, nullable alias를 각각 확인한다.
- 정상 별칭일 때만 기존 상태를 갱신하고 `render()`한다.
- `startActivityForResult()`와 `onActivityResult()`는 사용하지 않는다.

### 4. 정상·경계·실패 확인

- **정상:** `Lab Board`를 저장하면 Main 장치 별칭이 바뀐다.
- **경계:** 앞뒤 공백이 있는 `  Lab Board  `가 trim된 정책대로 표시된다.
- **실패:** 빈 입력은 Detail의 오류로 남고, extra 누락은 앱 crash 없이 canceled 종료된다.
- **취소:** 기존 별칭을 만든 뒤 Detail에서 Back을 눌러도 기존값이 유지된다.
- **회전:** 갱신된 alias를 Main의 saved state에 포함했다면 회전 후에도 유지된다.

### 단계별 힌트

<details>
<summary>힌트 1 — Activity를 찾을 수 없다는 오류가 난다</summary>

Manifest의 `<application>` 안에 `DeviceDetailActivity`가 선언됐는지, class package가 실제 파일과 일치하는지 확인한다.
</details>

<details>
<summary>힌트 2 — 결과 callback이 호출되지만 값이 없다</summary>

Detail에서 `setResult()`가 `finish()`보다 먼저인지, 결과 Intent와 Main이 같은 `EXTRA_ALIAS` 상수를 쓰는지 비교한다.
</details>

<details>
<summary>힌트 3 — Back을 누르면 별칭이 null로 바뀐다</summary>

callback에서 모든 결과를 대입하지 말고 `RESULT_OK`이고 유효 extra가 있을 때만 기존값을 교체한다.
</details>

### 확장

별칭 편집 Activity의 입력과 결과를 캡슐화한 사용자 정의 `ActivityResultContract`가 어떤 장점을 주는지 공식 문서를 바탕으로 인터페이스만 설계한다. 기본 제출에서는 built-in contract 코드가 동작하면 충분하다.

### 2일차 제출 증거

- `day2-result-matrix.md`: 네 계약 행의 예상/실제
- launcher 등록, extra 검증, 결과 설정 핵심 코드
- 정상 저장 화면과 공백 오류 화면
- deprecated 결과 API가 없음을 확인한 검색 결과 또는 설명

## 최종 제출 체크

- [ ] 여섯 핵심 callback을 실제 로그로 관찰했다.
- [ ] 상태 소실을 먼저 재현하고 같은 조건에서 복원했다.
- [ ] 정상·경계·실패·취소 결과가 분리되어 있다.
- [ ] Activity나 View 객체를 Intent extra로 전달하지 않았다.
