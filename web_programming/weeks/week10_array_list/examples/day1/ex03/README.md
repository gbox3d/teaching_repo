# 요소 생성과 append

처음에는 2·3번 두 줄이다. 첫 요소 붙이기를 누르면 1번이 맨 뒤에 붙는다. 같은 요소를 다시 append해도 복제되지 않아 총 세 줄을 유지한다.

## 수업 활동

강의자 시연·선택: createElement의 li를 <li>로 바꾸면 InvalidCharacterError가 나고 이후 코드가 실행되지 않는다. 확인 뒤 되돌린다. 만들기·textContent·append를 구분한다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day1/ex03/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. 화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
