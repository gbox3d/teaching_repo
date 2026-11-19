# 13주차 예제 · POST와 재조회

각 폴더 전체를 정적 서버로 열며 [따라하기](../walkthrough.md)의 사전 준비·설정 절차를 따른다. ex01은 JSON 변환만 수행한다. ex02~ex06과 완성본에는 런타임 `api-settings.js`, `.env.example`, `.gitignore`, `requests.http`, 독립 실행 README가 있다.

| 예제 | 수업 구분 | 바꾸거나 확인할 것 |
|---|---|---|
| [ex01](day1/ex01/README.md) | 시연 | 입력 → 객체 → JSON 문자열, 서버 저장 없음 |
| [ex02](day1/ex02/README.md) | 1차시 필수 요청의 비교본 | `.http` message 한 값·POST 201·서버 id |
| [ex03](day1/ex03/README.md) | 1차시 거절 비교 | 빈 문자열 400과 정상 201 |
| [ex04](day2/ex04/README.md) | 시연 | trim한 폼 값·JSON 본문 |
| [ex05](day2/ex05/README.md) | 시연 | 대기 중 버튼 잠금·실패 입력 보존 |
| [ex06](day2/ex06/README.md) | 시연 | POST 다음 GET·상태 분리 |
| [web-week13](day2/web-week13/README.md) | 2차시 필수 세 구역 수정 | 폼 값·JSON 본문·loadMessages |

## 조립과 시간

1차시는 `.http` message·POST 10분, id·GET 10분, 빈값 비교 10분이다. 2차시는 제공 `guestbook.js`의 학생 수정 세 구역 15분, 대기·실패 확인 7분, 다른 브라우저·캡처 8분이다. 각 차시 앞 강의·시연은 60분이다. 파일 배부·저장소는 사전 준비, 업로드는 수업 뒤 정리다.

[guestbook.js](day2/web-week13/guestbook.js) 하나에 GET·POST 함수와 이벤트를 모았다. `api-settings.js`는 설정 제공 파일이며 초기 조회는 모든 초기화 뒤에 실행한다. 이전 `submit.js`·`config.example.js`에는 이동 안내만 남겼고 HTML에서 읽지 않는다. 설정·이전 응답 방지 코드는 학생 평가 대상이 아니다.

모든 방명록·비교 화면은 [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)과 각 폴더의 `shared/examples.css`를 사용한다. 홈·내 정보는 이전 CSS를 이어 쓴다. 이미지·이전 캡처는 참고 자산이며 최신 서버 저장 결과는 직접 캡처한다.
