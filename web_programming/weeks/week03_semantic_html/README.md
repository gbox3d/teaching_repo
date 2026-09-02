# 3주차 — 시맨틱 HTML과 form

## 이번 주 질문

> 디자인을 모두 제거해도 문서의 의미, 이동 순서, 입력 목적이 전달되는가?

## 학습 목표

1. `header`, `nav`, `main`, `section`, `article`, `footer`의 역할을 콘텐츠 관계로 선택한다.
2. 페이지마다 하나의 주 제목과 건너뛰지 않는 heading 계층을 구성한다.
3. 이동은 link, 현재 화면의 동작은 button으로 구분한다.
4. 모든 입력 control에 보이는 `label`과 적절한 `type`을 연결한다.
5. `required`, `minlength`, `maxlength`, `pattern` 등 네이티브 검증을 적용하고 경계 입력을 시험한다.
6. table에 `caption`과 header 관계를, image에 맥락에 맞는 `alt`를 제공한다.
7. 마우스 없이 목록→상세→작성→제출 오류 확인 흐름을 수행한다.

## 수업 흐름

| 수업 | 설명·시연 30분 | 문제 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | 문서 구조, landmark, heading, link/button | 프로젝트 목록·상세 화면의 HTML 골격 | 두 페이지와 키보드 이동 기록 |
| 2일차 | form, label, input type, native validation, table, alt | 작성 화면과 상태별 입력 검증 | form과 정상·경계·실패 테스트표 |

## 준비

- 2주차에 배포한 개인 repository의 새 branch 또는 별도 연습 repository
- 프로젝트 후보 주제 1개, 핵심 사용자 1명, 표시할 샘플 콘텐츠 3개
- 외부 이미지가 필요하면 원 URL과 사용 조건을 기록한다. 예제는 외부 이미지 없이 동작한다.

## 자료 안내

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [시맨틱 화면 예제](examples/README.md)

## 완료 기준

- [ ] 목록·상세·작성 화면에 페이지 목적을 설명하는 `<h1>`이 있다.
- [ ] heading level이 시각적 크기가 아니라 문서 계층을 따른다.
- [ ] landmark가 의미 없이 중첩되거나 모든 `div`를 치환하지 않는다.
- [ ] link와 button의 기대 동작이 일치한다.
- [ ] 모든 form control은 클릭 가능한 보이는 label을 가진다.
- [ ] 필수 빈 값, pattern 불일치, 경계 길이, 정상 입력을 각각 확인했다.
- [ ] Tab, Shift+Tab, Enter/Space만으로 핵심 흐름을 수행했다.
- [ ] HTML validator 또는 브라우저 파서에서 중대한 구조 오류를 점검했다.

## 제출 증거

1. 목록·상세·작성 HTML과 연결되는 Git commit
2. 키보드 이동 순서와 막힌 지점 점검표
3. 입력 정상·경계·실패 테스트표
4. 프로젝트 주제, 핵심 사용자, 콘텐츠/이미지 출처 초안

## 공식 참고

- [W3C WAI Forms Tutorial](https://www.w3.org/WAI/tutorials/forms/)
- [W3C WAI Labeling Controls](https://www.w3.org/WAI/tutorials/forms/labels/)
- [HTML Living Standard](https://html.spec.whatwg.org/)

## 다음 주 연결

이번 주 의미 구조를 바꾸지 않고 4주차에 CSS만 추가한다. 다음 수업 전 375px과 1280px에서 우선순위가 달라질 요소를 HTML 주석 또는 설계 노트에 표시한다.
