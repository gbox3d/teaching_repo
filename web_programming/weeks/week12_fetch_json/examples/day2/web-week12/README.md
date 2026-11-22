# 선택 예제 · 수업 방명록에서 글 읽기

도시별 날씨 실습을 마친 뒤 같은 GET으로 방명록의 글을 읽어 볼 수 있다. 13주에는 이 조회 함수가 포함된 시작 코드를 제공한다.

## 브라우저

[방명록](guestbook.html)에서 **API 설정**을 연다. 기본 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다. 배부받은 공개 키와 내 방명록 번호를 입력하고 **설정 적용**을 누른다. 서버가 돌려준 최근 글을 최대 50개까지 표시한다. 글이 없으면 빈 목록도 정상이다. 새로고침하면 설정을 다시 입력한다.

## VS Code REST Client

1. VS Code에 REST Client(`humao.rest-client`)를 설치한다. 이 폴더의 `.env.example`을 `.env`로 복사한다.
2. `API_BASE_URL`에 수업 주소가 있는지 확인하고, `API_PUBLIC_KEY`에 배부받은 공개 키, `BOOK_ID`에 내 방명록 번호를 입력한다.
3. [requests.http](requests.http)의 **Send Request**를 접속 확인 → 도움말 → 자기 목록 순서로 누른다. 앞의 두 응답은 API 정보와 사용법을 담은 JSON 배열이다. 목록 요청은 `200 OK`와 방명록 글 배열을 반환한다.

모든 요청의 `apikey` 헤더는 REST Client가 `.env`에서 읽는다. 401이면 키를, 404이면 기본 URL과 경로를 확인한다. 브라우저는 화면에 입력한 값을 사용한다. 실제 `.env`는 Git과 제출 파일에서 제외한다.

## 파일

[guestbook.js](guestbook.js)의 `loadMessages()`가 서버 목록을 읽고 `showList(items)`가 글을 화면에 표시한다. 홈·내 정보는 기존 페이지를 이어 쓴다. [11주 로컬 저장본](guestbook.local.html)은 같은 브라우저의 localStorage를 사용한다.
