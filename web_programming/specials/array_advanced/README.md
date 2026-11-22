# 배열 심화

배열의 삽입·삭제·순회와 `filter`, `map`, `reduce`를 비교하는 보강수업 자료다. 기존 예제 5개로 원본 변화, 반환값, 콜백 인수, 빈 배열, 객체 참조를 확인한다. 정규 11주차 과제에는 포함하지 않는다.

## 학습 목표

- 원본을 바꾸는 메서드와 새 결과를 만드는 메서드를 구분한다.
- 배열의 최종 상태와 메서드 반환값을 따로 읽는다.
- 일반 `function` 콜백의 현재 항목과 누적값을 설명한다.
- 빈 배열의 결과와 객체 참조 공유를 확인한다.

선수학습은 배열·객체·함수·조건식·DOM의 `querySelector`, `textContent`, 이벤트 처리다. 화살표 함수는 필요하지 않다. 정규 10주의 문자열 배열·for·push·splice와 11주의 객체를 배운 뒤 진행한다. 정규 시험에 고급 배열 메서드를 추가하지 않는다.

## 파일 준비와 실행

한 예제 폴더의 `index.html`과 `app.js`를 함께 복사해 브라우저에서 연다. 화면은 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다.

수업용 정적 서버를 쓰려면 Node.js 24 이상에서 저장소 루트의 터미널을 열고 실행한다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

첫 예제: http://localhost:8111/specials/array_advanced/examples/01_insert_delete/

주소의 마지막 폴더명을 바꾸어 다른 예제를 연다. 파일을 편집·저장한 뒤 새로고침한다. 서버는 정적 파일만 제공하며 예제는 서버 API나 브라우저 저장소를 사용하지 않는다. 배열은 메모리에 있으므로 새로고침하면 초기 상태로 돌아간다.

## 예제와 수업 자료

| 순서 | 예제 | 비교할 것 |
|---|---|---|
| 01 | [삽입과 삭제](examples/01_insert_delete/README.md) | 변경된 배열과 길이·삭제 항목 반환값 |
| 02 | [순회](examples/02_iteration/README.md) | 반복문과 콜백·반환값 |
| 03 | [filter](examples/03_filter/README.md) | 선택된 새 배열과 유지된 원본 |
| 04 | [map](examples/04_map/README.md) | 새 객체의 점수와 원본 점수 |
| 05 | [reduce](examples/05_reduce/README.md) | 누적값·현재 항목·반환값·초깃값 |

[한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제 목록](examples/README.md)

## 수업 운영

설명·시연 60분과 실습 30분으로 운영할 수 있다. 이는 한 가지 운영 예이며 특강의 전체 시간·차시 수·자료 분량을 제한하지 않는다. 학생이 예상한 결과와 실제 결과가 다른 부분을 다시 실험한다.

각 예제에서 입력을 바꾸기 전에 원본 배열과 반환값을 예상한다. 실행 후 두 값을 비교하고 원인을 코드 한 줄과 연결한다. 실습 기록은 필요한 화면·코드·관찰 표를 사용하며 정규 과제 제출물과 분리한다.

## 확인 기준

`push`의 반환값을 배열로, `splice`의 반환값을 삽입한 항목으로 읽지 않는다. `forEach`가 새 배열을 반환하지 않는다는 점을 확인한다. `filter`의 객체 참조와 `map`의 새 객체 생성을 구분하고, 초깃값 0을 사용한 빈 배열 `reduce`의 결과를 설명한다.
