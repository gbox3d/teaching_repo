# 지도·Canvas 완성 앱

Node.js 24에서 이 폴더의 `npm start`를 실행하고 http://localhost:3000 을 연다. Git 저장소 전체가 필요하다. 설정·출처 표지·API 계약은 [예제 안내](../README.md)에 있다.

[00 접속·도움말](../00_connection/README.md)의 `.http`부터 실행하고 [01 relay 오류](../01_relay_checks/README.md)를 확인한다. 완성 앱에서는 로컬 PNG를 열어 문구 추가·실행 취소·밝기·다운로드를 먼저 실습할 수 있다. 지도 조회에는 Kakao JavaScript 키와 localhost 허용 도메인이 필요하다.

`window.aerialCanvasLab`은 브라우저 안의 JavaScript 인터페이스다. REST URL이 아니므로 Console에서 호출한다. `undo`는 텍스트·그리기를 취소한다. 회전·밝기·대비는 이전 값을 다시 적용하거나 전체 초기화로 되돌린다.

전용 Node relay가 필요하므로 GitHub Pages만으로 전체 앱을 실행할 수 없다. 정규 방명록의 Supabase 직접 호출과 서버 구성이 다르다.
