# ex01 CDN 연결 전후

`before.html`을 열고 **연결 후** 링크로 `index.html`을 연다. 두 화면에서 **클릭** 버튼을 누르면 클릭 횟수가 증가한다. 페이지를 이동하면 횟수는 0으로 돌아간다.

두 HTML은 같은 `app.js`와 `w3-button w3-teal` 버튼을 사용한다. `index.html`에만 다음 CDN 연결이 있다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

| 클래스 | 화면 변화 |
| --- | --- |
| `w3-container` | 화면 좌우 여백 |
| `w3-button` | 버튼 여백과 테두리 |
| `w3-teal` | 청록색 배경과 흰색 글자 |

연결 전에는 클래스 이름이 있어도 W3.CSS 모양이 나타나지 않는다. 연결 후에는 버튼 모양이 바뀌고 클릭 동작은 같다. 개발자 도구 Network에서 `w3.min.css` 응답을 확인한다.

CDN을 읽으려면 인터넷 연결이 필요하다. 추가 CSS와 라이브러리 로컬 사본은 사용하지 않는다.
