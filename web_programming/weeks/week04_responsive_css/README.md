# 4주차 — CSS와 반응형 UI

## 이번 주 질문

> 같은 의미 구조를 유지하면서 작은 화면과 큰 화면에서 읽기 쉽고, 키보드로 조작 가능하며, 예측 가능한 style을 어떻게 만드는가?

## 학습 목표

1. cascade의 origin·importance·specificity·source order를 근거로 최종 style을 설명한다.
2. inheritance와 box model을 DevTools의 Computed/Box Model에서 확인한다.
3. `box-sizing`, custom property, 상대 단위로 작은 디자인 기준을 만든다.
4. Flexbox와 Grid를 각각 1차원 정렬과 2차원 카드 배치에 선택한다.
5. 모바일 우선 기본 style과 `min-width` media query로 375px·1280px을 지원한다.
6. `:focus-visible`, 충분한 대비, `prefers-reduced-motion`을 반영한다.
7. 긴 문자열, 확대, 빈/적은 콘텐츠에서 overflow와 레이아웃 실패를 진단한다.

## 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | cascade, specificity, inheritance, box model, tokens | 3주차 HTML에 모바일 기본 style 적용 | token 표와 Computed 근거 |
| 2일차 | Flex/Grid, media query, focus, contrast, motion | 375px 1열→1280px 다열 전환과 오류 수정 | 두 viewport 캡처와 접근성 점검표 |

## 자료 안내

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [반응형 기준 예제](examples/README.md)

## 완료 기준

- [ ] HTML heading/landmark 순서를 CSS 때문에 바꾸지 않았다.
- [ ] 전역 `box-sizing: border-box`의 효과를 실제 width 계산으로 설명했다.
- [ ] 색상·간격·radius를 custom property token으로 정의했다.
- [ ] 375px에서 수평 스크롤 없이 핵심 작업이 가능하다.
- [ ] 1280px에서 카드가 다열이고 line length가 과도하게 길지 않다.
- [ ] 키보드 focus가 배경과 구별되어 보인다.
- [ ] 200% 확대와 긴 문자열에서 콘텐츠가 잘리거나 겹치지 않는다.
- [ ] reduced-motion 선호에서 장식 transition이 제거되거나 최소화된다.

## 제출 증거

1. 375px와 1280px 캡처(DevTools viewport 크기 표시 포함)
2. 사용한 color·spacing·radius token 표
3. 최종 style을 결정한 cascade 근거 2개
4. focus·overflow·motion 점검 결과
5. 기본 기능 commit과 오류 수정 commit

## 다음 주 연결

반응형 카드에 사용할 샘플 객체를 최소 8개 설계한다. 5주차에는 화면을 직접 조작하기 전에 배열 데이터를 검색·필터·정렬하는 작은 순수 함수부터 구현한다.
