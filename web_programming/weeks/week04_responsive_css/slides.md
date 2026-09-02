---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 4주차"
footer: "CSS와 반응형 UI"
---

# 4주차
## CSS와 반응형 UI

HTML 의미 구조는 유지하고 표현 규칙만 확장한다.

---

## 이번 주 검증 화면

```text
375px:  한 열, 읽기·입력 우선, 수평 overflow 없음
1280px: 공간을 활용한 다열, 제한된 본문 폭
Keyboard: focus가 항상 보임
Motion: reduced-motion 선호 존중
```

“내 화면에서 예쁨”이 아니라 여러 조건에서 완료 기준을 확인한다.

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## Cascade와 Box Model을 예측하기

---

## 0–5분 · CSS rule의 세 부분

```css
.activity-card {
  padding: 1rem;
}
```

- selector: 누구에게
- property: 무엇을
- value: 어떻게

문법이 맞아도 selector가 대상과 맞지 않으면 적용되지 않는다.

---

## 5–11분 · cascade의 판단 순서

학습용 단순화:

1. origin과 importance
2. selector specificity
3. 같은 specificity면 source order

```css
.card { color: navy; }
main .card { color: teal; }
```

더 구체적인 selector를 계속 쌓는 것은 유지보수 해법이 아니다.

---

## 11–15분 · specificity 비교

```text
type selector       0-0-1
.class / :pseudo    0-1-0
#id                 1-0-0
inline style        별도 높은 우선순위
```

필요한 범위에서 class 중심으로 단순하게 설계한다.

`!important`는 cascade를 없애지 않고 importance 층을 추가한다.

---

## 15–19분 · inheritance

```css
body {
  color: #172033;
  font-family: system-ui, sans-serif;
}
```

- 글자 관련 속성 다수는 자식에 상속
- margin, padding, border는 기본 상속되지 않음
- DevTools Computed에서 어느 rule로부터 왔는지 확인

---

## 19–24분 · box model

```text
margin → border → padding → content
```

기본 `content-box`에서는 선언 width 밖에 padding/border가 더해진다.

```css
*, *::before, *::after { box-sizing: border-box; }
```

---

## 24–27분 · normal flow를 출발점으로

- block은 문서 흐름에서 위→아래로 쌓인다.
- inline은 문장 흐름에 참여한다.
- width를 고정하기 전에 `max-width`, 유동 폭을 고려한다.
- position으로 모든 것을 놓으면 콘텐츠 변화에 취약하다.

---

## 27–30분 · custom property와 token

```css
:root {
  --color-accent: #075985;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --radius-card: 0.75rem;
}
```

반복 값을 이름 있는 결정으로 만든다. token 수 자체가 목표는 아니다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## Layout, Responsive, Inclusive State

---

## 0–5분 · Flexbox와 Grid 선택

| 관계 | 도구 | 예시 |
|---|---|---|
| 한 축의 정렬·분배 | Flexbox | header menu, button row |
| 행과 열의 2차원 배치 | Grid | card collection |

둘 중 “더 최신”을 고르는 문제가 아니다.

---

## 5–10분 · 유연한 카드 Grid

```css
.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: var(--space-4);
}
```

content와 가용 폭에 따라 열 수가 변한다. 명시적 breakpoints와 함께 비교한다.

---

## 10–15분 · 모바일 우선 media query

```css
/* 기본: 작은 화면 한 열 */
.site-header { display: block; }

@media (min-width: 48rem) {
  .site-header {
    display: flex;
    justify-content: space-between;
  }
}
```

작은 화면 규칙을 먼저 완성하고 공간이 생길 때 확장한다.

---

## 15–19분 · viewport는 기기 이름이 아니다

- 375px과 1280px은 대표 검증점
- 콘텐츠가 깨지는 지점이 실제 breakpoint 후보
- split screen, zoom, 브라우저 side panel도 폭을 바꿈
- orientation이나 특정 제품명에 의존하지 않음

---

## 19–23분 · focus는 상태 UI

```css
:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 3px;
}
```

`outline: none`만 적용하면 키보드 사용자가 현재 위치를 잃는다.

hover와 focus는 서로 다른 입력 경로다.

---

## 23–26분 · 대비와 상태

- 본문, 보조 문구, link, button의 경계를 실제 배경과 함께 확인
- 색 하나만으로 current/error/success를 전달하지 않음
- disabled와 enabled 상태를 혼동하지 않게 함
- 자동 검사와 눈·키보드 검사를 함께 사용

---

## 26–28분 · motion 선호

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto;
    transition-duration: 0.01ms;
  }
}
```

정보 이해에 필수 아닌 motion은 줄일 수 있어야 한다.

---

## 28–30분 · overflow 실패를 일부러 만들기

테스트 데이터:

```text
https://example.invalid/this-is-a-very-long-unbroken-path...
```

```css
.card { overflow-wrap: anywhere; }
```

내용을 숨기기보다 레이아웃이 적응하도록 만든다.

---

## 정리

```text
예측: cascade + box model
배치: normal flow → flex/grid
적응: mobile-first + content breakpoint
포용: focus + contrast + reduced motion + zoom
```
