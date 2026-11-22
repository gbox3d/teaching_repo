# ex03 카드와 메뉴

`index.html`에서 이름과 메시지를 입력하고 **미리보기**를 누른다. 아래 카드에 결과가 표시된다. 메뉴의 입력, 미리보기 링크는 해당 위치로 이동한다.

`app.js`는 ex02와 같다. HTML의 배치와 클래스만 바꾼다.

| 클래스 | 적용 대상 |
| --- | --- |
| `w3-container` | 카드와 머리말의 좌우 여백 |
| `w3-card` | 카드와 메뉴의 그림자 |
| `w3-bar` | 가로 메뉴 |
| `w3-bar-item w3-button` | 메뉴 항목 |
| `w3-mobile` | 화면 너비 600px 이하에서 메뉴를 세로로 배치 |
| `w3-content w3-padding` | 본문 최대 너비와 여백 |
| `w3-margin-top` | 카드 위쪽 간격 |

브라우저 너비를 1280px과 375px로 바꾸어 메뉴와 입력 칸을 확인한다. 카드는 두 화면에서 모두 위아래로 배치된다. `id`와 JavaScript를 바꾸지 않아도 입력 결과가 같다.

- CDN: `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`

CDN을 읽으려면 인터넷 연결이 필요하다. 라이브러리 로컬 사본은 사용하지 않는다.
