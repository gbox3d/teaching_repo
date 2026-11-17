# 웹 실습 공용 스타일

11주 2일차 `ex04`~`ex07`과 배열 심화 예제 5개는 W3.CSS를 cdnjs CDN에서 불러온다. 라이브러리를 별도 파일로 내려받지 않는다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

주소는 [cdnjs의 w3-css 목록](https://cdnjs.com/libraries/w3-css)에 있는 4.1.0 버전이다. CDN 스타일을 불러오려면 인터넷 연결이 필요하다.

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

화면을 공용 스타일로 만들 때 `body`에 `teaching-example`을 지정한다. 입력에는 `w3-input w3-border`, 버튼에는 `w3-button w3-border`를 사용한다.
체크박스는 `w3-check`와 `inline-label`을 사용해 일반 텍스트 입력의 전체 너비 규칙과 분리한다.
이 스타일을 참조하지 않는 기존 사이트와 1일차 예제에는 적용하지 않는다.
