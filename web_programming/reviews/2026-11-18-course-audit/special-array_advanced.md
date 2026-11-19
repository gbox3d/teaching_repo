# 배열 심화 특강 조사·검증

총괄이 기존 21개 파일을 조사했다. README·lab·walkthrough·한영 슬라이드·예제 목차와 다섯 폴더의 README·HTML·JS를 모두 읽었다. 자산과 서버 API는 없는 특강이다.

## 수업 연결과 수정

10주 문자열 배열·for·push·splice, 11주 객체를 배운 뒤 사용하는 보강 자료로 명시했다. 고급 메서드는 정규 시험에 추가하지 않는다. 기존 5개 예제와 한영 14장씩을 유지한다. 60+30은 운영 예이며 특강 시간 상한이 아니다.

Node.js 안내를 교재 공통 기준인 24 이상으로 맞췄다. reduce 표에서 375px 폭에 긴 영문 인수가 끊겨 보이는 것을 확인해 화면 열 제목은 한국어로 줄였다. accumulator·current·next의 의미와 실제 코드 설명은 README에 유지했다. W3.CSS 고정 CDN과 공용 examples.css를 사용한다.

## 실제 실행 결과

Chrome에서 다음 동작을 실행하고 README의 예상값과 비교했다. [실행 기록](evidence/array-browser.json), [reduce 375px 화면](evidence/array-reduce-375.png).

| 예제 | 확인한 결과 |
|---|---|
| 01 삽입·삭제 | push/unshift 길이 4, pop/shift 삭제값, 위치 1 삽입의 빈 반환 배열, 위치 1 삭제의 바나나 반환, 빈 배열 pop undefined |
| 01 경계 | 빈 위치·음수·소수·범위 초과 거절, HTML 모양 입력의 문자 표시, 새로고침 후 초기 배열 |
| 02 순회 | 두 방식 모두 3항목, 반복 실행해도 누적 없음, forEach 반환 undefined |
| 03 filter | 70·60·100·80에서 각각 2·3·0·2명, 원본 점수 유지, 빈 입력 안내, 선택 객체 참조 공유 |
| 04 map | 5·5·10·0·-5의 결과와 반복 비누적, 원본 80·60·90 유지, 빈 입력 안내, 새 객체 참조 |
| 05 reduce | 합계 230·콜백 3회·실제 표 3행, 빈 배열 0·0행, 다시 230으로 복구 |

다섯 화면 모두 375/1280px에서 가로 넘침이 없고 CDN 스타일시트가 로드되었다. 처리되지 않은 페이지 오류는 없었다. JS 5개 구문 검사와 한국어 UI·문서 검사도 통과했다. 설명은 [MDN filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map), [reduce](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce), [forEach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)의 반환값·참조·초깃값 설명과 대조했다.

슬라이드 전체 렌더와 링크 검사는 최종 통합 검사에서 수행한다. 실제 학생 집단의 시간은 측정하지 않았으며 Pages에 게시하지 않았다.

## 전수 파일 목록

- 루트: README.md, lab.md, walkthrough.md, slides.md, slides_en.md
- examples: README.md
- examples/01_insert_delete: README.md, index.html, app.js
- examples/02_iteration: README.md, index.html, app.js
- examples/03_filter: README.md, index.html, app.js
- examples/04_map: README.md, index.html, app.js
- examples/05_reduce: README.md, index.html, app.js
