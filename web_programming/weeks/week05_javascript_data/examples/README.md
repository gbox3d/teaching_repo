# 5주차 예제 — 순수 데이터 변환

## 파일

| 파일 | 역할 |
|---|---|
| [activities.mjs](activities.mjs) | 일관된 shape의 수업용 활동 8개 |
| [transforms.mjs](transforms.mjs) | 검색·필터·정렬·view model·집계 함수 |
| [demo.mjs](demo.mjs) | 단계별 Console 관찰 |
| [transforms.test.mjs](transforms.test.mjs) | Node 내장 test와 assertion |
| [index.html](index.html) | 브라우저 module 실행 진입점 |

## Node.js 실행

```powershell
node demo.mjs
node --test transforms.test.mjs
```

외부 package나 설치가 필요 없다.

## 브라우저 실행

ES Module은 로컬 HTTP에서 연다. 수업용 정적 서버로 이 폴더를 제공한 뒤 `index.html`을 열고 DevTools Console을 확인한다. `file:`로 직접 열면 브라우저 module 보안 정책 때문에 import가 실패할 수 있다.

## 관찰 순서

1. 원본 id 순서를 적는다.
2. query `웹`, category `study`, direction `asc` 결과를 예상한다.
3. `node demo.mjs`의 단계별 length와 table을 확인한다.
4. demo 뒤 원본 id가 같은지 확인한다.
5. test 이름에서 정상·경계·실패 계약을 읽는다.
6. `sortByStartsAt(activities, 'sideways')`가 RangeError인 이유를 설명한다.

## 의도적 변형

복사본에서 `sortByStartsAt`의 `[...items]`를 `items`로 바꾸고 test를 실행한다. 원본 보존 test가 실패하는 것을 확인한 뒤 즉시 복구한다.
