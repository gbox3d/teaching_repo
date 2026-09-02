# 4주차 실습 — 한 HTML, 여러 사용 조건

## 공통 과제

3주차에 만든 의미 구조는 유지하고 CSS를 추가해 다음 조건을 모두 만족시킨다.

```text
좁은 화면 375px → 한 열, 핵심 흐름 우선, 수평 스크롤 없음
넓은 화면 1280px → 카드 다열, 읽기 폭 제한
키보드 → focus 위치가 명확
긴 콘텐츠/200% zoom → 겹침·잘림 없음
reduced motion → 장식 motion 최소화
```

예제 디자인을 그대로 복제하기보다 본인 콘텐츠의 문제를 해결한다.

## 1일차 실습 — cascade를 설명할 수 있는 모바일 style

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 기준선 | 0–8분 | CSS 없는 화면과 HTML 구조 확인 |
| reset/tokens | 8–18분 | box-sizing, body, color/space/radius token |
| typography/container | 18–30분 | line-height, 유동 폭, heading 간격 |
| component | 30–43분 | nav, card, link/button 기본 style |
| cascade 문제 | 43–52분 | 충돌 rule 예측·Computed 확인·수정 |
| 검증·commit | 52–60분 | 375px, 긴 문자열, 근거 기록 |

### 문제 1 · 작은 token 체계

`styles.css`를 만들고 HTML에 상대경로로 연결한다. 다음 결정을 8–12개 custom property 안에서 표현한다.

- 배경, surface, 본문, 보조, accent, focus 색
- 작은/중간/큰 spacing
- card radius
- 최대 content 폭

예시 이름은 참고만 하고 본인 값과 의미를 정한다.

```css
:root {
  --color-text: ...;
  --space-2: ...;
  --radius-card: ...;
}
```

같은 의미의 literal value가 여러 번 반복되면 token 사용 여부를 검토한다.

### 문제 2 · box model과 유동 container

다음을 구현한다.

1. pseudo-element까지 `border-box` 적용
2. body 기본 margin 제거와 읽기 좋은 line-height
3. content container는 작은 화면에서 좌우 여백을 유지하고 큰 폭을 제한
4. card는 content에 따라 높이가 늘어나며 고정 height를 쓰지 않음
5. 긴 link가 viewport 밖으로 밀어내지 않음

DevTools Box Model에서 card 하나의 content, padding, border, margin 숫자를 기록한다. `width: 100%`와 padding이 border-box 안에 포함되는지 설명한다.

### 문제 3 · cascade 진단

복사본에 아래와 같은 충돌을 잠시 만든다.

```css
.activity-card { border-color: var(--color-accent); }
main .activity-card { border-color: tomato; }
```

실행 전에 결과를 예상하고 다음을 기록한다.

| 항목 | 기록 |
|---|---|
| 두 selector의 specificity |  |
| 예상 최종 border-color |  |
| Styles에서 취소선 rule |  |
| Computed가 가리키는 source |  |
| 요구에 맞춘 단순한 수정 |  |

`!important`나 id selector를 추가해 이기는 방식은 사용하지 않는다. 중복 rule을 제거하거나 component class 하나로 의도를 분명히 한다.

### 정상·실패 검증

- 정상: 375px에서 메뉴, h1, 카드, link/button이 순서대로 보인다.
- 경계: 카드가 한 개일 때도 과도하게 늘어나거나 중앙에 고립되지 않는다.
- 실패: 80자 이상의 공백 없는 문자열을 카드에 넣어 수평 overflow를 재현한다.
- 복구: `overflow-wrap` 또는 min-size 문제를 고쳐 내용이 보존된 채 wrap된다.

### 단계별 힌트

<details>
<summary>힌트 1 — CSS가 전혀 적용되지 않는다</summary>

Network에서 CSS 요청 status와 Request URL을 확인하고, HTML의 `href`와 실제 파일명을 비교한다.
</details>

<details>
<summary>힌트 2 — 선언이 취소선이다</summary>

같은 property를 설정한 다른 matched rule을 Styles에서 찾는다. specificity가 같은지, 더 구체적인지, 뒤에 나왔는지 순서대로 설명한다.
</details>

<details>
<summary>힌트 3 — 페이지 전체가 조금 넘친다</summary>

Elements를 한 단계씩 선택하며 어느 box가 viewport보다 넓은지 확인한다. 고정 width, padding+content-box, 긴 문자열, grid item의 `min-width`를 점검한다.
</details>

### 확장

1. `clamp()`로 h1 크기를 제한된 범위 안에서 유동적으로 만들고 최소/최대 값을 확인한다.
2. system font stack과 web font의 성능·개인정보·layout shift trade-off를 비교한다.
3. CSS cascade layer가 규모가 큰 style sheet에서 해결하는 문제를 조사한다.

## 2일차 실습 — 반응형 layout과 접근성 상태

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| layout 관계 | 0–8분 | 한 축/두 축 판별 |
| mobile 기본 | 8–18분 | header/nav/card 한 열과 wrap |
| wide 확장 | 18–33분 | media query, Flex/Grid 다열 |
| focus/state | 33–43분 | hover/focus/current/disabled 구분 |
| motion/overflow | 43–52분 | reduced motion, zoom, 긴 문자열 |
| 증거·commit | 52–60분 | 375/1280 캡처와 점검표 |

### 문제 1 · Flex와 Grid를 이유로 선택

다음 관계를 구현하고 선택 이유를 한 문장씩 적는다.

- 넓은 화면의 site identity와 nav: 한 축 관계
- nav link 묶음과 button row: 한 축 + wrap 가능
- activity card collection: 행·열 관계
- 좁은 화면: DOM 순서 그대로 한 열

CSS로 보이는 순서를 `order`로 바꾸지 않는다. 의미·focus 순서가 틀리면 HTML을 수정한다.

### 문제 2 · content 기반 breakpoint

1. 320px부터 1400px까지 viewport를 천천히 늘린다.
2. card 두 열이 읽을 만해지는 첫 구간을 기록한다.
3. 가장 가까운 `rem` breakpoint를 정한다.
4. 기본 한 열, 첫 breakpoint 두 열, 필요하면 더 넓은 곳 세 열을 구현한다.
5. 375px과 1280px에서 완료 조건을 확인한다.

breakpoint 선택 기록:

| 폭 근처 | 관찰한 문제/여유 | 적용 결정 |
|---:|---|---|
|  |  |  |

### 문제 3 · 상호작용 상태

link와 button에 다음 상태를 구별해 만든다.

- 기본
- hover(가능한 장치에서)
- focus-visible
- active
- current navigation (`aria-current="page"`와 연동)
- disabled가 있다면 enabled와 혼동되지 않게 표현

마우스를 치우고 Tab으로 모든 interactive element를 이동한다. focus outline이 배경·accent surface 모두에서 보이는지 확인한다.

### 문제 4 · motion과 강건성

1. hover transition은 transform 또는 color 한두 속성으로 제한한다.
2. `prefers-reduced-motion: reduce`에서 transition을 제거하거나 최소화한다.
3. 200% zoom에서 메뉴와 카드가 겹치지 않는지 본다.
4. 제목을 40자, URL을 100자 공백 없이, 카드를 1개/8개로 바꿔 본다.
5. 내용을 숨겨 해결하지 않고 layout/wrapping을 고친다.

### 점검표

| 조건 | 결과 | 발견한 문제 | 수정 |
|---|---|---|---|
| 375px |  |  |  |
| 1280px |  |  |  |
| 200% zoom |  |  |  |
| Tab focus |  |  |  |
| 긴 문자열 |  |  |  |
| 카드 1개 |  |  |  |
| reduced motion |  |  |  |

### 단계별 힌트

<details>
<summary>힌트 1 — Grid item이 container 밖으로 넘친다</summary>

긴 콘텐츠 외에도 grid child의 기본 minimum size를 확인한다. `min-width: 0`과 `minmax(0, 1fr)`이 어떤 차이를 만드는지 DevTools에서 시험한다.
</details>

<details>
<summary>힌트 2 — focus style이 안 보인다</summary>

마우스 click이 아닌 Tab으로 focus-visible 상태를 만든다. selector가 실제 anchor/button에 match되는지 Styles에서 확인한다.
</details>

<details>
<summary>힌트 3 — media query가 항상 적용된다</summary>

`min-width` 단위와 괄호, style sheet 뒤의 닫는 중괄호를 확인한다. DevTools에서 media query rule이 회색인지 활성인지 본다.
</details>

### 확장 주제

1. `auto-fit`과 `auto-fill`의 빈 track 동작을 카드 1개일 때 비교한다.
2. container query가 viewport media query보다 component에 적합한 상황을 설계만 해 본다.
3. `prefers-color-scheme` dark theme을 추가하되 모든 상태 대비를 다시 검증한다.

## 제출 전 확인

- `style: add mobile visual system`
- `style: expand activity grid on wide screens`
- `fix: preserve focus and long content`

위와 같이 변경 의도가 구분되는 commit을 권장한다. 실제 변경과 메시지가 맞아야 한다.
