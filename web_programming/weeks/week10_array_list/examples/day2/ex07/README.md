# splice와 삭제 버튼

세 글에서 가운데 삭제를 누르면 첫째·셋째와 2개, 남은 둘도 삭제하면 0개다. 새로고침하면 제공된 세 글로 돌아간다.

## 수업 활동

강의자 시연·선택: splice(i, 1)의 1을 2로 바꾸면 해당 위치부터 두 값을 지운다. 삭제 처리의 showList만 빼면 배열은 줄지만 화면은 그대로다. 다시 그릴 때 let i가 각 버튼의 새 위치를 맡는다. 버튼 W3.CSS 클래스는 제공 코드다.

## 실행

[화면](index.html)과 [app.js](app.js)를 함께 읽는다. 저장소 루트에서 아래 서버를 시작하고 `http://localhost:8000/day2/ex07/`를 연다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

이 폴더 전체를 복사하면 독립 실행할 수 있다. 화면 스타일은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)에서 읽는다. 화면에서 결과를 먼저 확인하고 Console의 items는 보조 관찰에 쓴다. ex03에는 items 배열이 없다.

[전체 실습](../../../lab.md)
