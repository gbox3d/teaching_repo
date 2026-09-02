# 3주차 실습 — CSS 없이 사용할 수 있는 세 화면

## 프로젝트 시나리오

캠퍼스 활동을 찾아보고, 한 활동의 일정을 확인하고, 새 활동을 제안하는 작은 사이트를 만든다. 본인 프로젝트 주제로 바꾸어도 되지만 목록·상세·작성이라는 정보 관계와 검증 기준은 유지한다.

## 공통 규칙

- CSS와 JavaScript를 추가하지 않는다.
- 의미가 같은 콘텐츠를 단지 배치 목적으로 중복하지 않는다.
- 실제 개인정보 대신 수업용 예시 데이터를 사용한다.
- 각 화면에서 현재 페이지 목적을 설명하는 h1을 찾을 수 있어야 한다.

## 1일차 실습 — 목록과 상세의 의미 구조

### 완료해야 할 사용자 이야기

> 사용자는 주요 메뉴를 건너 목록 제목을 찾고, 관심 활동의 명확한 link를 따라 상세 페이지로 이동하며, 일정 표를 이해하고 다시 목록으로 돌아올 수 있다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 콘텐츠 모델 | 0–10분 | 사이트명, 페이지명, 카드 3개, 상세 필드 정리 |
| 목록 구조 | 10–27분 | landmark, heading, article, link |
| 상세 구조 | 27–42분 | 설명, 정의 목록, 일정 table, 돌아가기 link |
| 키보드 점검 | 42–52분 | Tab/Shift+Tab/Enter 흐름 |
| 오류 수정 | 52–57분 | heading·중첩·중복 id 점검 |
| 회고 | 57–60분 | 태그 선택 근거 3문장 |

### 문제 1 · 콘텐츠를 구조로 번역

먼저 태그 없이 다음 정보를 적는다.

- 사이트 전체 이름
- 목록 페이지의 목적
- 독립적으로 읽히는 활동 3개: 이름, 범주, 한 문장 소개
- 상세 페이지에서만 필요한 정보: 날짜, 장소, 정원, 설명
- 사이트 전체 메뉴와 페이지 안 링크

그 뒤 다음 최소 구조를 직접 작성한다.

```text
index.html
  site header
  primary navigation
  main
    page heading
    introductory paragraph
    activity collection heading
    3 independent activity items
  footer

detail.html
  site header/navigation
  main
    activity name as page heading
    description
    term/value facts
    schedule data table
    return link
  footer
```

태그 정답표로 시작하지 말고 각 콘텐츠가 어떤 관계인지 먼저 결정한다.

### 문제 2 · link와 button 판별

다음 기능에 적절한 native 요소를 사용하고 이유를 한 줄씩 적는다.

1. 목록에서 상세 페이지로 이동
2. 상세에서 목록으로 이동
3. 작성 페이지로 이동
4. “관심 표시”처럼 현재 화면 상태를 바꾸는 미래 기능 자리

미래 기능이 아직 구현되지 않았다면 동작하지 않는 가짜 `href="#"`를 만들지 않는다. 기능 설명 문장 또는 실제 `button disabled` 중 의도를 분명히 선택한다.

### 문제 3 · 키보드 점검

마우스를 치우고 다음을 실행한다.

1. 주소창에서 Tab을 시작한다.
2. focus 순서대로 `1, 2, 3...`과 보이는 이름을 기록한다.
3. 상세 link를 Enter로 연다.
4. 상세 페이지의 table을 읽고 돌아가기 link로 복귀한다.
5. Shift+Tab으로 역방향 이동한다.

| 순서 | 요소 이름 | 요소 종류 | 예상 동작 | 실제 |
|---:|---|---|---|---|
| 1 |  |  |  |  |

### 단계별 힌트

<details>
<summary>힌트 1 — section과 article을 고르기 어렵다</summary>

카드 하나를 RSS 항목이나 별도 상세 미리보기로 떼어도 이해되면 article 후보이다. 여러 article을 “이번 주 활동”이라는 주제로 묶는 바깥 영역은 section 후보이다.
</details>

<details>
<summary>힌트 2 — heading level이 헷갈린다</summary>

h1부터 제목 텍스트만 들여쓰기해 목차를 그린다. 부모 제목보다 정확히 한 단계 아래인지 확인한다.
</details>

<details>
<summary>힌트 3 — 모든 카드 link 이름이 ‘자세히’다</summary>

주변 문장 없이 링크 텍스트만 읽어도 대상을 구별하도록 `활동 이름 + 자세히 보기`로 작성한다.
</details>

### 정상·실패 검증

- 정상: 모든 페이지와 link가 404 없이 열린다.
- 경계: 카드가 한 개여도 collection heading과 페이지 구조가 어색하지 않다.
- 실패: 의도적으로 link `href`를 틀려 404를 확인한 뒤 실제 파일명과 맞춰 복구한다.
- 구조: 중복 `id`, 닫히지 않은 주요 요소, heading 건너뜀을 검사한다.

### 확장

1. 본문 시작으로 이동하는 skip link를 추가하고 키보드로 작동을 확인한다.
2. 각 활동에 `time datetime="YYYY-MM-DD"`를 사용해 기계가 읽는 날짜와 보이는 날짜를 구분한다.
3. breadcrumb가 필요한 깊이인지 판단하고 필요하면 `nav aria-label="현재 위치"`로 추가한다.

## 2일차 실습 — 작성 form과 네이티브 검증

### 완료해야 할 사용자 이야기

> 사용자는 각 입력의 목적과 형식을 이해하고, 키보드로 활동을 작성하며, 잘못된 값이면 해당 입력에서 브라우저의 도움을 받고, 정상 제출이면 전달된 name/value를 확인할 수 있다.

### 요구 데이터

| 데이터 | 권장 control/constraint | 확인할 실패 |
|---|---|---|
| 활동 이름 | text, required, 4–30자 | 빈 값, 3자 |
| 담당 이메일 | email, required | `student` |
| 활동 날짜 | date, required | 빈 값 |
| 최대 인원 | number, 1–20 | 0, 21 |
| 범주 | select, required, 빈 기본 option | 미선택 |
| 소개 | textarea, required, 10–200자 | 9자 |
| 연락 방법 | fieldset 안 radio | 미선택 |
| 운영 규칙 동의 | checkbox, required | 미동의 |

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 입력 계약 | 0–8분 | field/name/type/constraint 표 작성 |
| form 구현 | 8–30분 | label, control, help text, submit |
| 실패 테스트 | 30–42분 | empty, format, range, length |
| 정상·경계 | 42–50분 | 최소/최대와 정상 제출 |
| 키보드 점검 | 50–56분 | label/focus/order/submit |
| 회고 | 56–60분 | 테스트 표와 commit |

### 문제 1 · form 작성

`write.html`을 만들고 `action="confirmation.html"`, `method="get"`을 사용한다. 실제 서비스에서는 개인정보를 query string에 보내지 않지만, 이번 예제는 가상 데이터의 `name=value`를 눈으로 관찰하기 위한 로컬 학습용이다.

각 control에서 다음을 확인한다.

- 고유한 `id`
- 제출 key인 `name`
- `for`가 id와 일치하는 보이는 label
- 데이터 목적에 맞는 type
- 요구사항을 표현하는 native constraint
- 예시는 placeholder에만 의존하지 않고 근처 도움말로 제공

### 문제 2 · 테스트 표

제출 버튼을 눌러 실제 브라우저 동작을 기록한다. 메시지 문구는 브라우저마다 다를 수 있다.

| 번호 | 입력 | 예상 invalid control/이유 | 실제 focus | 통과 여부 |
|---:|---|---|---|---|
| 1 | 모두 빈 값 | 첫 required |  |  |
| 2 | 이름 3자 | minlength |  |  |
| 3 | 이름 4자 | 이름 경계 통과 |  |  |
| 4 | email `student` | email type |  |  |
| 5 | 인원 0 | min |  |  |
| 6 | 인원 20 | max 경계 통과 |  |  |
| 7 | 소개 9자 | minlength |  |  |
| 8 | 모든 정상 값 | confirmation 이동 |  |  |

정상 제출 뒤 주소의 query에서 input의 `name`과 값이 어떻게 연결되는지 2개만 확인한다. 실제 개인 정보는 입력하지 않는다.

### 문제 3 · accessible name과 keyboard

1. 모든 label 텍스트를 클릭해 연결 input이 focus되는지 확인한다.
2. Tab 순서가 보이는 읽기 순서와 맞는지 확인한다.
3. radio는 화살표 키, checkbox는 Space로 조작한다.
4. submit 뒤 invalid control로 focus가 이동하는지 확인한다.
5. `tabindex` 양수로 순서를 억지로 고치지 않는다. HTML 순서를 고친다.

### 단계별 힌트

<details>
<summary>힌트 1 — label 클릭이 input으로 가지 않는다</summary>

label의 `for` 값과 input의 `id`를 대소문자까지 비교한다. `name`은 제출 key이며 label 연결 대상이 아니다.
</details>

<details>
<summary>힌트 2 — select가 미선택인데 제출된다</summary>

select에 `required`를 두고 첫 option의 `value`를 빈 문자열로 둔다. 단순 안내 문구가 실제 범주 값으로 제출되지 않게 한다.
</details>

<details>
<summary>힌트 3 — minlength 테스트가 예상과 다르다</summary>

브라우저 UI로 값을 직접 입력해 제출한다. 스크립트나 DevTools로 값만 바꾸면 사용자의 실제 입력과 validation 시점이 다를 수 있다.
</details>

### 최종 검증

- [ ] 모든 control에 보이는 label이 있다.
- [ ] radio 질문은 fieldset/legend로 묶였다.
- [ ] 빈 값, 형식 실패, 범위 실패, 길이 경계를 실제 제출로 시험했다.
- [ ] 정상 값은 confirmation 페이지로 이동한다.
- [ ] 마우스 없이 입력·선택·제출할 수 있다.
- [ ] 작성 페이지에서 목록으로 돌아갈 실제 link가 있다.

### 확장 주제

1. `autocomplete` token을 담당 이메일에 적용하고 의미를 조사한다.
2. 도움말 문장에 id를 주고 `aria-describedby`로 input과 연결한다.
3. `datalist`와 `select`의 자유 입력·제한 선택 차이를 비교한다.
4. 클라이언트 네이티브 검증을 통과해도 서버 검증이 반드시 필요한 이유를 공격자 관점에서 설명한다.

## 제출 전 출처·회고

- 프로젝트 주제와 핵심 사용자 한 문장
- 외부 텍스트·이미지의 원 URL과 사용 조건 또는 “직접 작성/외부 자산 없음”
- 키보드 점검에서 발견한 문제 한 개와 수정
- 가장 유용했던 native HTML 동작 한 개와 이유
