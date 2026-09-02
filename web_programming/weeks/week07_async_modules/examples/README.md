# 7주차 예제

`starter`는 ES Module과 local JSON fetch의 최소 실행 기준점이다. 네 source를 선택해 success·empty·shape error·HTTP error를 즉시 관찰할 수 있다.

## 실행

```bash
cd starter
python -m http.server 8000
```

`http://localhost:8000`을 연다. `file://`로 직접 열지 않는다.

## 파일 책임

| 파일 | 책임 |
|---|---|
| `js/main.js` | event와 요청 흐름 조정 |
| `js/api.js` | HTTP·JSON·데이터 모양 경계 |
| `js/ui.js` | 상태별 DOM 출력 |
| `data/*.json` | 재현 가능한 응답 fixture |

starter는 네 상태의 기준 동작을 보여 주지만, 검색·통계 module과 연속 요청 방어는 [실습](../lab.md)에서 직접 추가한다.
