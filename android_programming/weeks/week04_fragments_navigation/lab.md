# 4주차 실습 — mock 장치 목록에서 안전하게 제어 화면으로

## 공통 규칙

- navigation graph와 입력 계약을 코드 전에 그린다.
- 실제 BLE device나 ESP32-C3를 찾지 않고 고정 mock 데이터만 사용한다.
- Fragment의 View를 `onDestroyView()` 이후 접근하지 않는다.
- 오류를 숨기기 위해 `try/catch`로 모두 삼키거나 강제 non-null(`!!`)을 쓰지 않는다.

## 1일차 실습 — Fragment/View 수명과 Navigation (60분)

### 상황과 문제

한 Activity에 섞인 장치 목록과 제어 화면을 두 Fragment로 분리해야 한다. 목록에서 선택한 mock device ID만 제어 화면에 전달하고, Back과 argument 누락에서 안전하게 동작하도록 만들어라.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 구조 예측 | 0–8분 | 8분 | graph·수명·argument 표 작성 |
| NavHost/graph | 8–20분 | 12분 | Activity host와 두 destination 구성 |
| Fragment View | 20–34분 | 14분 | 두 XML과 `onViewCreated` 구현 |
| 이동·수명 관찰 | 34–47분 | 13분 | navigate/Back과 View 로그 |
| 누락 실패 처리 | 47–56분 | 9분 | argument 없는 경로 안전화 |
| 검증·회고 | 56–60분 | 4분 | 증거와 수명 설명 정리 |
| **합계** |  | **60분** |  |

### 1. 코드 전 설계

```text
MainActivity
└─ NavHostFragment
   ├─ DeviceListFragment
   └─ DeviceControlFragment ← ARG_DEVICE_ID
```

| 시나리오 | 예상 destination | ID | List View 수명 | Control View 수명 |
|---|---|---|---|---|
| 앱 시작 |  |  |  |  |
| mock-02 선택 |  |  |  |  |
| Back |  |  |  |  |
| ID 누락 |  |  |  |  |

### 2. NavHost와 graph 구현

1. Main Activity layout에 `FragmentContainerView` 기반 NavHost를 둔다.
2. graph의 시작 목적지를 `DeviceListFragment`로 둔다.
3. `DeviceControlFragment` destination과 목록→제어 action을 추가한다.
4. system Back을 사용해 목록으로 돌아오는 기준 흐름을 확인한다.

### 3. Fragment와 View lifecycle 로그

두 Fragment에서 다음 이벤트를 같은 형식으로 기록한다.

- Fragment: `onCreate`, `onStart`, `onResume`
- View: `onCreateView`, `onViewCreated`, `onDestroyView`

```text
fragment=<List|Control> id=<fragment instance> event=<callback>
```

목록→제어→Back 후 다음을 답한다.

- 어느 Fragment의 View가 먼저 파괴되었는가?
- Back 뒤 새 목록 View가 만들어졌는가?
- Fragment instance와 View instance를 같은 것으로 볼 수 있는가?

### 4. argument 정상·누락 처리

- 목록의 임시 버튼 하나에서 `mock-02`를 전달한다.
- 제어 화면은 ID를 trim하고 빈 값이 아닌지 확인한다.
- ID가 없으면 `장치를 선택할 수 없습니다`를 표시하고 제어 버튼을 비활성화한다.
- 안전한 테스트용 action 또는 강의자 제공 경로로 argument 누락을 재현한다.
- 누락 화면에서 Back으로 목록에 돌아간다.

### 5. 정상·경계·실패 확인

- **정상:** `mock-02` 선택 시 제어 화면에 같은 ID가 보인다.
- **경계:** Back→다시 다른 mock ID 선택 흐름에서 이전 ID가 남지 않는다.
- **실패:** argument 누락에서 crash 없이 오류 문구와 비활성 버튼이 보인다.
- **수명:** `onDestroyView` 뒤 이전 View를 갱신하는 코드가 없다.

### 단계별 힌트

<details>
<summary>힌트 1 — 앱 시작 시 NavHost 오류가 난다</summary>

FragmentContainerView의 `android:name`, `app:navGraph`, `app:defaultNavHost`와 navigation resource 이름을 차례로 비교한다.
</details>

<details>
<summary>힌트 2 — action ID를 찾지 못한다</summary>

action이 list destination 내부에 선언됐는지, Kotlin의 `R.id` 이름과 XML id가 같은지 확인하고 다시 빌드한다.
</details>

<details>
<summary>힌트 3 — Back 뒤 이전 View 오류가 난다</summary>

Fragment field에 View를 오래 보관하는지 찾는다. 기본 실습에서는 `onViewCreated(view, ...)`의 지역 참조로 listener를 연결하고 수명 밖에서 사용하지 않는다.
</details>

### 확장

목록 화면의 선택 ID를 saved state 또는 ViewModel 중 어디에 둘지 수명 요구를 먼저 적고 설계안만 제시한다. 이번 기본 구현에 불필요한 공유 ViewModel을 추가하지 않는다.

### 1일차 제출 증거

- `day1-navigation.md`: graph 그림과 네 시나리오 표
- 목록→제어와 argument 누락 화면
- Fragment/View lifecycle 로그와 해석 3문장

## 2일차 실습 — RecyclerView 목록과 펄스 입력 검증 (60분)

### 상황과 문제

임시 버튼을 0개 이상의 mock 장치 목록으로 바꾸고, 선택한 장치의 제어 화면에서 펄스 시간을 검증한다. 항목 View 재사용과 잘못된 숫자 입력 때문에 다른 장치를 선택하거나 앱이 종료되어서는 안 된다.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 결과 예측 | 0–8분 | 8분 | 목록 크기·입력 매트릭스 작성 |
| RecyclerView | 8–22분 | 14분 | item XML, ListAdapter, ViewHolder |
| item navigation | 22–34분 | 12분 | 현재 item ID 전달·Back 확인 |
| 입력 검증 | 34–47분 | 13분 | 필수·형식·범위·성공 처리 |
| 경계·실패 검증 | 47–56분 | 9분 | 0/1/3 목록과 입력 7개 |
| 제출 정리 | 56–60분 | 4분 | 표·코드·화면 증거 |
| **합계** |  | **60분** |  |

### 1. 구현 전 예측

| 데이터/입력 | 예상 화면·결과 | 실제 | 근거 |
|---|---|---|---|
| 빈 목록 |  |  |  |
| mock 장치 1개 |  |  |  |
| mock 장치 3개 |  |  |  |
| pulse `100` |  |  |  |
| pulse `5000` |  |  |  |
| pulse `99` |  |  |  |
| pulse `5001` |  |  |  |
| pulse `abc` |  |  |  |
| pulse 매우 긴 숫자열 |  |  |  |
| pulse 빈 값 |  |  |  |

### 2. RecyclerView 구현

요구사항:

1. `MockDevice(id, name, ready)` 데이터 클래스를 만든다.
2. item XML에는 이름과 텍스트 상태를 둔다.
3. `ListAdapter`의 item 동일성은 `id`, 내용 동일성은 data class 값으로 비교한다.
4. `bind()`는 name과 ready 상태를 모두 갱신한다.
5. 클릭 callback은 position 숫자가 아니라 현재 `MockDevice`를 전달한다.
6. 빈 목록이면 별도 empty View를 표시한다.

### 3. 목록에서 제어 화면으로

세 가짜 장치를 submit한다.

```text
mock-01 · Lab Entrance · disconnected
mock-02 · Lab Desk · ready
mock-03 · Long Named Demonstration Device · ready
```

두 번째 항목을 선택하고 제어 화면 ID가 `mock-02`인지 확인한다. Back 후 세 번째를 선택해 이전 ID가 남지 않는지 확인한다.

### 4. 펄스 입력 검증

입력 순서를 코드 구조에 반영한다.

1. `trim()` 후 빈 값이면 필수 오류
2. 정수 정규식과 맞지 않으면 숫자 형식 오류
3. `toLongOrNull()`이 null이거나 `100L..5000L` 밖이면 범위 오류
4. 유효하면 error를 지우고 `mock-02에 500ms 펄스를 시뮬레이션함`처럼 표시

실제 GPIO나 BLE write는 호출하지 않는다.

### 5. 정상·경계·실패 확인

- **정상:** 3개 목록에서 선택한 item ID가 제어 화면과 일치하고 `500`이 mock 성공이다.
- **경계:** `100`과 `5000`은 성공한다. 빈 목록과 1개 목록도 crash 없이 의미 있는 화면이다.
- **실패:** `99`, `5001`, 매우 긴 숫자열, `abc`, 빈 값은 서로 맞는 오류이며 이전 성공 문구를 성공처럼 남기지 않는다.
- **누락:** device ID가 없으면 유효 pulse라도 실행 버튼이 비활성이다.

### 단계별 힌트

<details>
<summary>힌트 1 — 모든 행이 같은 text를 보인다</summary>

ViewHolder가 생성될 때가 아니라 `bind(item)` 안에서 현재 item의 name과 ready 표시를 모두 설정하는지 확인한다.
</details>

<details>
<summary>힌트 2 — 다른 장치 ID가 전달된다</summary>

생성 시점 position을 저장하지 않는다. `bind(item)`에서 listener가 현재 item을 callback으로 전달하게 한다.
</details>

<details>
<summary>힌트 3 — 문자 입력에서 앱이 종료된다</summary>

정수 형식을 먼저 확인하고 `toLongOrNull()`이 null이거나 허용 범위를 벗어나면 범위 오류로 처리한다. 유효 범위가 확인된 뒤에만 `toInt()`로 바꾼다.
</details>

### 확장

ready가 아닌 mock 장치를 눌렀을 때 제어 화면으로 이동할지, 목록에서 안내할지 UX 정책을 두 가지 비교하고 하나를 구현한다. 어느 정책이든 색 이외의 설명을 제공한다.

### 2일차 제출 증거

- `day2-matrix.md`: 목록 0/1/3개와 입력 7개 결과
- `MockDevice`, DiffUtil, `bind`, validation 핵심 코드
- 여러 mock 장치 목록과 정상/오류 제어 화면
- “왜 position 대신 item을 전달했는가” 2문장

## 최종 제출 체크

- [ ] 두 날의 60분 실습 결과가 구분되어 있다.
- [ ] Fragment View 수명 밖의 View 접근이 없다.
- [ ] 정상·경계·실패 입력을 모두 확인했다.
- [ ] 결과 문구가 실제 하드웨어 제어가 아닌 mock임을 명시한다.
