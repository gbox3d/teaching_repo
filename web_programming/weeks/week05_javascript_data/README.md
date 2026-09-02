# 5주차 — JavaScript 데이터와 함수

## 이번 주 질문

> 화면을 직접 고치기 전에, 입력 배열을 예측 가능한 작은 함수들로 어떻게 변환하고 검증할 수 있는가?

## 학습 목표

1. `const`와 `let`, primitive와 object reference의 차이를 실행 결과로 설명한다.
2. 함수의 parameter, return value, local scope를 분명히 설계한다.
3. Array/Object/Map/Set을 순서·record·key lookup·unique라는 목적에 맞게 선택한다.
4. destructuring과 spread로 필요한 값을 읽고 원본을 보존한 복사본을 만든다.
5. `map`, `filter`, `find`, `sort`, `reduce`의 결과 형태를 구분한다.
6. 검색·범주 필터·정렬·card view model·요약 함수를 조합한다.
7. 정상·경계·실패 입력과 원본 불변성을 Node 내장 테스트로 검증한다.

## 수업 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 | 산출물 |
|---|---|---|---|
| 1일차 | binding, type/reference, function/scope, collection 선택 | 객체 8개와 검색·필터·조회·unique 함수 | 데이터 모듈과 사례 검증 |
| 2일차 | destructuring/spread, map/filter/find/sort/reduce | 복사 정렬·view model·요약과 테스트 | 변환 함수 4개 이상과 테스트표 |

## 실행 환경

- Node.js LTS
- 최신 브라우저(선택: module을 HTTP로 열어 Console 관찰)
- 외부 package는 사용하지 않는다.

예제 실행:

```powershell
Set-Location examples
node demo.mjs
node --test transforms.test.mjs
```

## 자료 안내

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습지](lab.md)
- [데이터 변환 예제](examples/README.md)

## 완료 기준

- [ ] 객체가 최소 8개이고 모든 객체가 같은 핵심 field 계약을 따른다.
- [ ] 검색어 앞뒤 공백과 대소문자를 정규화한다.
- [ ] `all` 범주와 존재하지 않는 범주를 구분해 시험한다.
- [ ] 정렬 함수가 입력 배열의 순서를 바꾸지 않는다.
- [ ] `map` 결과는 화면이 소비할 card view model 형태다.
- [ ] 빈 배열 집계가 오류 없이 0과 빈 Map/목록을 반환한다.
- [ ] 잘못된 정렬 방향은 조용히 추측하지 않고 명확한 오류가 된다.
- [ ] 최소 4개의 named transformation function과 정상·경계·실패 테스트가 있다.

## 제출 증거

1. 데이터와 변환 함수 module
2. `node --test` 통과 결과
3. 정상·경계·실패 입력 테스트표
4. 원본 배열이 유지됨을 보이는 before/after 증거
5. 각 함수의 input → output 예시와 선택한 collection 근거

## 다음 주 연결

이번 주 함수가 반환하는 card view model을 6주차 DOM 렌더링 입력으로 사용한다. 다음 수업 전에 빈 결과일 때 표시할 문구와 카드 한 개의 HTML template을 설계한다.
