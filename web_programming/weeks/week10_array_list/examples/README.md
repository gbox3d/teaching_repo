# 10주차 예제

1일차 필수는 ex01 문자열 두 값 수정과 ex02 시작 틀 다섯 줄이다. 2일차는 제공 방명록 시작 틀의 등록 두 줄·삭제 두 줄이다. 나머지 예제 수정은 강의자 시연 또는 선택 연습이다.

| 예제 | 확인할 동작 | 안내 |
|---|---|---|
| [ex01](day1/ex01/index.html) | 배열·push·인덱스·초기화 | [README](day1/ex01/README.md) |
| [ex02](day1/ex02/index.html) / [시작](day1/ex02/start.html) | 숫자 3과 length 비교 | [README](day1/ex02/README.md) |
| [ex03](day1/ex03/index.html) | 요소 생성과 append | [README](day1/ex03/README.md) |
| [ex04](day1/ex04/index.html) | 배열과 DOM에 추가 | [README](day1/ex04/README.md) |
| [ex05](day2/ex05/index.html) | 비우기 유무 | [README](day2/ex05/README.md) |
| [ex06](day2/ex06/index.html) | showList·빈 상태·개수 | [README](day2/ex06/README.md) |
| [ex07](day2/ex07/index.html) | 가운데 항목 삭제 | [README](day2/ex07/README.md) |
| [완성 방명록](day2/web-week10/guestbook.html) / [시작](day2/web-week10/guestbook.start.html) | 등록→재그리기→삭제 | [실습지](../lab.md) |

## 실행과 파일 복사

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

`http://localhost:8000/day1/ex01/`처럼 예제 폴더를 연다. 독립 복사할 때 각 폴더의 HTML·JS와 shared/examples.css를 함께 가져온다. 시작 파일은 같은 폴더의 제공 CSS를 사용한다. W3.CSS 라이브러리는 [cdnjs 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)으로 읽으며 인터넷 연결이 필요하다. shared/examples.css는 저장소 공통 보조 CSS의 배포 사본이다.

홈·내 정보는 9주에서 이어 쓴다. 10주 제공 방명록은 작성 시각을 붙이던 최신순 피드에서 이름·메시지 문자열의 등록순 목록으로 바뀐다. `push`한 첫 항목과 화면의 첫 줄을 대응시키고 가운데 항목을 `splice`로 지운다. W3.CSS와 폼의 입력 ID는 계속 사용한다.

`guestbook.start.html`은 guestbook.start.js를 읽는다. 학생이 작성한 네 줄을 guestbook.js로 옮긴 뒤 일반 guestbook.html을 확인한다. 완성본에는 그 네 줄이 이미 있다.

[배열 심화 특강](../../../specials/array_advanced/README.md)은 정규 필수와 별개다.
