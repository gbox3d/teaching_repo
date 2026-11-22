# showList와 빈 상태

처음 0개·빈 안내, 더하기 뒤 1개·안내 없음이다. 목록·개수·안내를 같은 함수에서 갱신한다. 빈 문자열도 값 하나로 추가한다.

## 수업 활동

강의자 시연·선택: 초기 배열에 하나를 넣고 최초 showList를 빼면 초기 화면이 갱신되지 않는다. 더하기 처리의 showList만 빼면 배열만 늘고 화면은 그대로다. 개수·빈 안내는 for 밖에 있어야 0개일 때도 실행된다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day2/ex06/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. 화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
