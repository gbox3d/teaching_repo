# 4주차 예제 — 반응형 캠퍼스 카드

## 파일

- [index.html](index.html): 시맨틱 구조와 여러 길이의 카드 콘텐츠
- [styles.css](styles.css): token, mobile-first, Flex/Grid, focus, reduced motion

## 실행과 관찰

브라우저에서 `index.html`을 열거나 정적 서버로 제공한다. DevTools device toolbar에서 다음을 확인한다.

1. 375px: header/nav가 wrap되고 card는 한 열
2. 768px 근처: header가 한 행으로 정렬되고 card 열 수가 증가
3. 1280px: content 폭이 제한되고 card가 다열
4. Tab: link와 button에 노란 focus ring
5. 긴 URL: card 밖으로 넘치지 않고 wrap
6. reduced motion emulation: card transition 제거

## 코드 읽기 질문

- 전역 border-box는 pseudo-element까지 왜 포함하는가?
- `.activity-grid`는 Flex가 아닌 Grid가 적합한가?
- `minmax(min(100%, 16rem), 1fr)`의 안쪽 `min()`은 아주 좁은 화면에서 무엇을 막는가?
- `.activity-card`의 `min-width: 0`과 `overflow-wrap`은 어떤 실패 데이터에 대응하는가?
- media query가 없어도 작은 화면의 핵심 기능은 남는가?
