# 배열과 DOM에 추가

서로 다른 값으로 더하기 세 번이면 세 줄과 3개다. 빈 문자열도 값 하나로 추가한다. 새로고침하면 0개다.

## 수업 활동

강의자 시연·선택: push만 주석 처리하면 줄은 늘고 0개, append만 주석 처리하면 줄 없이 개수만 늘어난다. count 템플릿 문자열의 백틱을 작은따옴표로 바꾸면 ${items.length}개라는 글자가 그대로 보인다. 확인 뒤 되돌린다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day1/ex04/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. 화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
