# 6주차 — DOM·event·브라우저 CRUD

이번 주에는 JavaScript 배열을 화면의 단일 원본 상태로 두고, 사용자 입력을 event로 받아 DOM을 다시 그리는 작은 할 일 앱을 만든다. 첫날에는 Create·Read·Delete를, 둘째 날에는 Update·`localStorage` 영속화와 예외 처리를 완성한다.

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. DOM 노드, JavaScript 상태, 화면 표현의 차이를 설명한다.
2. `querySelector`, `addEventListener`, `event.preventDefault()`를 사용한다.
3. 배열의 `map`, `filter`와 고유 `id`로 CRUD 동작을 구현한다.
4. `JSON.stringify`/`JSON.parse`로 상태를 저장하고 손상된 저장값을 복구한다.
5. 정상·빈 입력·없는 항목·손상 데이터 경로를 직접 재현한다.

## 수업 흐름

| 일차 | 30분 설명·시연 | 60분 직접 해결 |
|---|---|---|
| 1일차 | DOM, event, form 제출, 상태 → render | 할 일 Create·Read·Delete |
| 2일차 | id 기반 Update, event delegation, 저장·복구 | 수정·완료·영속화와 오류 상태 |

실습 순환은 `문제 읽기 → 결과 예상 → 구현 → DevTools 관찰 → 오류 설명 → 변형` 순서로 진행한다.

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습 문제](lab.md)
- [예제 안내](examples/README.md)
- [실습 starter](examples/starter/index.html)

## 실행

`examples/starter`에서 다음 중 하나를 실행한 뒤 표시된 URL을 연다.

```bash
python -m http.server 8000
# 또는
npx serve .
```

단순 DOM 예제라 `index.html`을 직접 열 수도 있지만, 이후 주차와 같은 조건을 만들기 위해 로컬 서버 사용을 권장한다.

## 완료 기준

- 새 항목을 추가하면 배열과 화면이 함께 바뀐다.
- 빈 문자열과 공백만 있는 입력은 거부되고 이유가 화면에 표시된다.
- 완료 전환, 제목 수정, 삭제가 고유 `id`를 기준으로 동작한다.
- 새로고침 뒤에도 데이터가 복원된다.
- 손상된 `localStorage` 값을 넣어도 앱 전체가 중단되지 않는다.
- 구현 commit과 정상·실패 경로 캡처를 남긴다.

## 다음 주 연결

현재 데이터는 한 브라우저 안에만 존재한다. 7주차에는 코드를 ES Module로 나누고 `fetch`로 외부 데이터를 읽으면서 loading·empty·error 상태를 분리한다.
