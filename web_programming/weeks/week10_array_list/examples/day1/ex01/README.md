# 배열·push·인덱스

처음 세 값, length 3, items[0]·items[2]와 없는 items[3]의 undefined를 확인한다. 더하기는 입력을 뒤에 붙이고 초기화는 빈 배열로 바꾼다. 초기화 뒤 모든 인덱스는 undefined다. 새로고침하면 제공된 세 값으로 돌아간다.

## 수업 활동

필수: app.js 첫째·셋째 push의 문자열 두 값만 바꾼다. showValues와 JSON.stringify는 출력용 제공 코드다. 객체·JSON 수업은 11주에 한다. 선택: 빈 문자열도 배열 값 하나이므로 더하면 개수가 늘어나는 것을 비교한다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day1/ex01/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. W3.CSS는 cdnjs 4.1.0 CDN, 추가 스타일은 shared/examples.css다. CDN에는 인터넷 연결이 필요하다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
