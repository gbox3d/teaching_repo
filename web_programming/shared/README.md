# 웹 실습 공용 스타일과 제공 설정

11주 2일차 `ex04`~`ex07`과 배열 심화 예제 5개는 W3.CSS를 cdnjs CDN에서 불러온다. 라이브러리를 별도 파일로 내려받지 않는다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

주소는 [cdnjs의 w3-css 목록](https://cdnjs.com/libraries/w3-css)에 있는 4.1.0 버전이다. CDN 스타일을 불러오려면 인터넷 연결이 필요하다.

[7주차](../weeks/week07_form_input/README.md)에서 CDN과 W3.CSS 클래스를 소개한다. 7주차 변환 후 방명록과 9~14주 완성 방명록은 이 CDN을 사용한다. 아래 추가 CSS는 11주 기본 저장 예제와 배열 심화 예제에서 직접 참조하며, 정규 REST 예제에는 독립 배포용 사본을 둔다.

## 추가 스타일

[examples.css](examples.css)는 화면 너비·간격·결과·표에 사용하는 추가 스타일이다. HTML에서 W3.CSS 다음에 연결한다.

11주 2일차 예제의 연결:

```html
<link rel="stylesheet" href="../../../../../shared/examples.css">
```

배열 심화 예제의 연결:

```html
<link rel="stylesheet" href="../../../../shared/examples.css">
```

추가 CSS의 상대 경로는 예제 폴더 위치에 맞춘다. 배포할 때도 예제와 `shared/examples.css`의 상대 위치를 유지한다.

## 로컬 실행과 배포

저장소 루트에서 `web_programming`을 정적 서버 루트로 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

- [11주 ex04](http://localhost:8111/weeks/week11_object_localstorage/examples/day2/ex04/)
- [배열 특강 01](http://localhost:8111/specials/array_advanced/examples/01_insert_delete/)

## 적용 규칙

화면을 공용 스타일로 만들 때 `body` 또는 바깥 `main`에 `teaching-example`을 지정한다. 입력에는 `w3-input w3-border`, 버튼에는 `w3-button w3-border`를 사용한다. `box-sizing: border-box`는 이 영역 안의 입력 여백과 테두리를 폭에 포함한다.
7주 변환 비교처럼 전체 레이아웃을 유지할 때는 결과 요소에 `example-output`을 붙여 긴 문자열만 줄바꿈한다. 7주 이후 독립 배포 예제는 이 보조 CSS의 사본을 포함한다. W3.CSS 라이브러리 자체는 계속 CDN으로 읽는다.
체크박스는 `w3-check`와 `inline-label`을 사용해 일반 텍스트 입력의 전체 너비 규칙과 분리한다.
이 스타일을 참조하지 않는 기존 사이트와 1일차 예제에는 적용하지 않는다.

## 정규 REST 예제의 제공 설정

[api-settings.js](api-settings.js)는 12~14주 브라우저 예제의 설정 패널을 연결하는 제공 코드다. 각 예제 폴더에는 같은 파일의 사본을 두므로 그 폴더만 배포해도 실행된다. HTML은 이 파일을 동작 JS보다 먼저 defer로 읽는다.

API 주소·공개 키·book_id는 현재 페이지의 메모리에 적용한다. 새로고침하면 로컬 연습 기본값으로 돌아간다. `.http`의 `.env`는 REST Client 전용으로 브라우저 설정과 별개다. 학생은 설정 패널을 재구현하지 않고 요청·응답 처리 구역을 수정한다. [설정 계약](../reviews/2026-11-18-course-audit/api-settings-contract.md)에 파일·요소 이름을 기록했다.
