# ex07 탭 간 동기화

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex07/)

이 예제는 W3.CSS CDN과 [추가 공용 스타일](../../../../../shared/README.md)의 `shared/examples.css`를 사용한다. CDN 스타일을 읽으려면 인터넷 연결이 필요하다. 예제와 `web_programming/shared/`의 상대 위치를 유지한다.

1. 정적 서버에서 `index.html`을 연 뒤 **같은 페이지 새 탭**을 누른다.
2. 첫 탭에서 메모를 입력하고 **저장**한다. 두 번째 탭의 메모와 이벤트 결과가 바뀐다.
3. 두 번째 탭에서 **지우기**를 누른다. 첫 탭의 메모도 비워진다.
4. 같은 값을 연속 저장한다. 실제 값이 바뀌지 않으면 새 이벤트가 발생하지 않는다.

`storage` 이벤트는 같은 origin의 다른 문서에서 받는다. 값을 바꾼 탭에는 발생하지 않으므로 그 탭의 상태는 클릭 처리에서 직접 바꾼다. 다른 기기나 다른 브라우저와 동기화하는 기능은 아니다.

이 예제는 `week11-ex07-memo` 키 하나만 쓴다. 다른 탭에서 변경하면 이 탭에서 아직 저장하지 않은 입력도 바뀐다. 여러 사용자의 편집 충돌을 해결하는 예제는 아니다.

근거: [MDN storage 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event).
