# 고전 for로 목록 만들기

처음 네 값일 때 위 목록은 3개, 아래 목록은 4개다. 다시 그리기는 두 목록을 먼저 비우므로 중복되지 않는다.

## 수업 활동

필수: start.html과 app.start.js의 TODO 다섯 줄을 완성한다. items.push 줄을 주석 처리한 뒤 배열을 0·1·3개로 바꾸고 아래 목록 개수를 비교한다. 위의 고정 반복문은 없는 번호도 String(undefined)로 표시한다. 선택: 아래 반복문 <를 <=로 바꾸면 값 없는 줄이 하나 더 생긴다. const i로 바꾸면 첫 줄 뒤 증가에서 TypeError가 난다. 확인 뒤 되돌린다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day1/ex02/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. W3.CSS는 cdnjs 4.1.0 CDN, 추가 스타일은 shared/examples.css다. CDN에는 인터넷 연결이 필요하다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
