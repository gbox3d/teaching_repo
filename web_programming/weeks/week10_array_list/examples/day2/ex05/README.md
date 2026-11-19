# 비우고 다시 그리기

비우지 않고 그리기를 두 번 누르면 3→6줄이다. 비우고 그리기를 누르면 3줄이며 반복해도 3줄이다. 배열은 세 값 그대로다.

## 수업 활동

강의자 시연·선택: 두 번째 버튼의 innerHTML 빈 문자열 대입을 주석 처리하면 그 버튼도 매번 세 줄을 추가한다. 배열에 값 하나를 더하면 비우고 그리기는 네 줄이다. 입력 문자열을 innerHTML에 넣지 않는다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day2/ex05/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. W3.CSS는 cdnjs 4.1.0 CDN, 추가 스타일은 shared/examples.css다. CDN에는 인터넷 연결이 필요하다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
