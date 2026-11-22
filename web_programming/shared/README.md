# 웹 실습 공용 설정

## W3.CSS

[7주 CSS 응용](../weeks/week07_form_input/README.md)에서 아래 CDN을 연결한다. 입력창은 `w3-input`, 버튼은 `w3-button`, 긴 응답을 스크롤할 영역은 `w3-responsive`를 사용한다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

## 정규 REST 예제의 제공 설정

[api-settings.js](api-settings.js)는 방명록의 설정 패널을 연결하는 제공 코드다. 이 패널을 쓰는 각 예제 폴더에는 같은 파일의 사본을 둔다. 12주 필수 예제는 키 없이 공개 API에 직접 접속한다. HTML은 이 파일을 동작 JS보다 먼저 defer로 읽는다.

12주 선택 방명록과 13주 방명록 화면에는 수업 주소가 표시된다. 배부받은 공개 키와 방명록 번호를 넣고 **설정 적용**을 누른다. 선택 방명록은 이때 첫 GET을 보낸다. 13주는 저장 버튼이나 폼으로 POST를 보낸다. 새로고침하면 키는 비워진다. 다른 화면에서 리허설 주소가 보이면 수업 주소로 바꿀 수 있다. `.http`는 해당 예제의 `.env`에서 설정을 읽는다. [설정 계약](../reviews/2026-11-18-course-audit/api-settings-contract.md)에 파일·요소 이름을 기록했다.
