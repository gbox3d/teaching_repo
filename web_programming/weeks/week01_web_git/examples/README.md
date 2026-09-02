# 1주차 예제 — 요청·응답 관찰 페이지

## 파일 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 의미 구조와 CSS/JS 연결 |
| `styles.css` | 최소 표현과 상태 강조 |
| `app.js` | 버튼 클릭 횟수 상태 |
| `server.mjs` | 설치 없는 로컬 HTTP 서버 |

## 실행

이 폴더에서 다음을 실행한다.

```powershell
node server.mjs
```

브라우저에서 `http://localhost:8000/`을 연다. 서버 종료는 `Ctrl+C`다.

다른 프로그램이 8000번 포트를 사용하면 다음처럼 포트만 바꾼다.

```powershell
$env:PORT=8080
node server.mjs
```

## 관찰 지점

1. Network: `/`, `/styles.css`, `/app.js`의 status와 content type
2. Elements: `<output id="status">`의 text 변화
3. Console: `Web role demo ready` 메시지
4. 새로고침: 클릭 횟수가 0으로 초기화되는 경계 동작
5. `/missing.html`: 서버가 반환하는 404

## 복사 후 변형

수업 자료 원본이 아닌 개인 폴더 복사본에서 경로 오류를 만든다. 오류를 재현한 뒤 반드시 원래 파일명과 참조를 맞추어 복구한다.
